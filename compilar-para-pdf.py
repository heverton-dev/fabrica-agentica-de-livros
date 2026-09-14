#!/usr/bin/env python3
"""
Compila livro_final.md com conteudo real dos capitulos e converte para PDF.
Usa Pandoc + Typst com template ABNT para gerar PDF profissional.

Pipeline (V3):
  1. Renderiza os diagramas Mermaid dos capitulos em PNG (Upgrade 2)
  2. Deriva capa grafica, ficha catalografica e sinopse (Upgrade 5)
  3. Converte para PDF via Pandoc + Typst com template ABNT

Uso: python compilar-para-pdf.py [slug1 slug2 ...] [opcoes]
     (omita slugs para processar todos os livros cadastrados)

Opcoes:
  --sem-diagramas   pula a renderizacao Mermaid (usa o markdown como esta)
  --sem-capa        desativa capa/contracapa graficas (visual ABNT sobrio)
  --paginas-exatas  compila duas vezes para gravar a paginacao real na ficha CIP
"""

import os
import re
import shutil
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "scripts"))


def import_opcional(nome_modulo):
    """Importa um modulo opcional de scripts/; devolve None se ausente.

    Reduz o boilerplate `try: import X except ImportError: X = None` repetido
    para cada dependencia opcional deste script.
    """
    try:
        return __import__(nome_modulo)
    except ImportError:  # pragma: no cover
        return None


metadados_livro = import_opcional("metadados_livro")
parametros_obra = import_opcional("parametros_obra")
tipos_obra = import_opcional("tipos_obra")

# Catalogo estatico de livros da fabrica (serie principal, ver SLUGS abaixo).
# Obras derivadas via /criar-livro sao aceitas dinamicamente em main() mesmo
# sem estar nesta lista, desde que existam em output/.

DIR_RAIZ = Path(__file__).parent / "output"
DIR_PROJETO = Path(__file__).parent

# Pandoc/Typst: resolvidos via PATH (shutil.which); com fallback para variavel
# de ambiente quando o binario nao esta no PATH (instalacao fora do padrao).
# Mesmo padrao ja usado em scripts/gerar-relatorio-sessao.py.
PANDOC = shutil.which("pandoc") or os.environ.get("FABRICA_PANDOC_BIN", "pandoc")
TYPST = shutil.which("typst") or os.environ.get("FABRICA_TYPST_BIN", "typst")
TEMPLATE = DIR_PROJETO / "templates" / "template.typ"
TEMPLATE_TCC = DIR_PROJETO / "templates" / "template_tcc.typ"
TEMPLATE_ARTIGO = DIR_PROJETO / "templates" / "template_artigo.typ"
RENDERIZADOR = DIR_PROJETO / "scripts" / "renderizar-diagramas.py"

# Flags globais (definidas em main() a partir da linha de comando)
RENDERIZAR_DIAGRAMAS = True
CAPA_GRAFICA = True
PAGINAS_EXATAS = False
TIPO_OVERRIDE = None  # --tipo livro|tcc|artigo|playbook|lead-magnet|deck (None = auto)

# V5 — derivados de extracao trazem o Markdown final com nome proprio.
FONTE_MD_POR_TIPO = {
    "playbook": "playbook.md",
    "lead-magnet": "lead_magnet.md",
    "deck": "deck.md",
}


def resolver_tipo(slug):
    """Tipo de obra do slug: --tipo tem prioridade; senao le config_obra.json."""
    if TIPO_OVERRIDE:
        return TIPO_OVERRIDE
    if parametros_obra is not None:
        return parametros_obra.carregar_config(slug).get("tipo_obra", "livro")
    return "livro"


def template_para_tipo(tipo):
    """V5: o template sai do registro (tipos_obra.template_de), com fallback para
    o template do livro quando o arquivo declarado ainda nao existe."""
    if tipos_obra is not None:
        try:
            caminho = tipos_obra.template_de(tipo)
            if caminho and Path(caminho).exists():
                return Path(caminho)
        except KeyError:
            pass
    if tipo == "tcc" and TEMPLATE_TCC.exists():
        return TEMPLATE_TCC
    if tipo == "artigo" and TEMPLATE_ARTIGO.exists():
        return TEMPLATE_ARTIGO
    return TEMPLATE

SLUGS = [
    # Serie Agentes CLI
    "revolucao-agentes-cli",
    "modelos-avancados-terminal",
    "roteamento-llms-gratuito",
    "fluxos-profissionais",
    # Serie LLMs (nota: diretorio real com prefixo B3-)
    "llms-freetiers",  # symlink aponta para B3-llms-freetiers no disco local
    # Serie Segredos
    "segredos-opencode",
    "segredos-freebuff",
    "segredos-oh-my-pi",
    "segredos-mimocode",
    # Serie AIDD
    "00-mega-livro-todos-aidd",
    "01-aidd-ai-driven-development",
    "01-transicao-dev-aidd",
    "02-harness-camada-orquestracao",
    "03-harness-suas-camadas",
    "04-motor-cognitivo-llm-core",
    "05-economia-tokens-cache",
    "06-rules-restricoes-globais",
    "07-specs-spec-driven",
    "08-skills-conhecimento-sob-demanda",
    "09-prompts-engenharia-interacao",
    "10-subagentes-workflows-paralelos",
    "11-mcp-rag",
    "12-guardrails-governanca",
    "13-higiene-contexto",
    "14-arvore-decisao-auditoria",
    "A-opencode-personalizacoes-escondidas",
    # Serie Camadas AIDD
    "00-eita-metodo",
    "C1-transicao-dev-aidd",
    "C2-camada-interface",
    "C3-camada-harness",
    "C4-camada-operarios",
    "C5-camada-llm-core",
]

def copiar_pdf_com_nome_slug(slug, dir_livro):
    """Copia livro_final.pdf para <nome>.pdf no mesmo diretorio.

    `slug` pode ser um caminho aninhado (ex.: "livro/artigos/artigo_1" para
    artigos/ebooks derivados) — usa so o ultimo componente como nome de arquivo.
    """
    import shutil
    nome = Path(slug).name
    origem = dir_livro / "livro_final.pdf"
    destino = dir_livro / f"{nome}.pdf"
    if origem.exists():
        shutil.copy2(origem, destino)
        tamanho_kb = destino.stat().st_size / 1024
        print(f"  [OK] PDF copiado: {destino.name} ({tamanho_kb:.1f} KB)")
        return True
    return False


def extrair_frontmatter(texto):
    """Extrai YAML frontmatter do markdown."""
    match = re.match(r'^---\n(.*?)\n---\n', texto, re.DOTALL)
    if match:
        return match.group(1), texto[match.end():]
    return '', texto


def renderizar_diagramas(slug, dir_livro, md_path):
    """Upgrade 2: converte blocos ```mermaid em PNG e devolve o MD com figuras.

    Nao destrutivo e tolerante a falha: se o mermaid-cli nao estiver disponivel
    ou o renderizador falhar, devolve o markdown original.
    """
    if not RENDERIZAR_DIAGRAMAS or not RENDERIZADOR.exists():
        return md_path
    try:
        conteudo = md_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return md_path
    if "```mermaid" not in conteudo.lower():
        return md_path

    saida = dir_livro / "livro-render.md"
    try:
        resultado = subprocess.run(
            [sys.executable, str(RENDERIZADOR), slug,
             "--md", str(md_path), "--saida", str(saida)],
            capture_output=True, text=True, timeout=900,
        )
    except Exception as e:  # noqa: BLE001
        print(f"  [AVISO] Renderizacao de diagramas ignorada: {e}")
        return md_path

    if saida.exists() and saida.stat().st_size > 0:
        for linha in resultado.stdout.strip().split("\n")[-2:]:
            if linha.strip():
                print(f"  {linha.strip()}")
        return saida
    print("  [AVISO] Diagramas nao renderizados; blocos mermaid seguem como codigo")
    return md_path


def flag_config(dir_livro, nome):
    """True quando config_obra.json declara `nome: true` (opt-in editorial V5.5)."""
    caminho = dir_livro / "config_obra.json"
    if not caminho.exists():
        return False
    import json
    try:
        config = json.loads(caminho.read_text(encoding="utf-8"))
    except ValueError:
        return False
    return bool(config.get(nome, False))


def variaveis_visuais(slug, dir_livro, paginas=None, tipo=None):
    """Metadados injetados no template: capa/CIP comercial (livro) ou
    resumo/abstract/folha de aprovacao (TCC/artigo) — Upgrade 5 + Fase B/C (V4)."""
    tipo = tipo or "livro"
    args = []

    # V5: coletor/variaveis saem do registro. Os tipos que usam o coletor padrao
    # do livro ("coletar"/"variaveis_pandoc") caem no fluxo classico abaixo, que
    # tambem resolve a capa grafica.
    if tipos_obra is not None and metadados_livro is not None:
        nome_coletor = tipos_obra.campo(tipo, "coletor_metadados")
        nome_vars = tipos_obra.campo(tipo, "variaveis_pandoc")
        if nome_coletor and nome_vars and nome_coletor != "coletar":
            coletor = getattr(metadados_livro, nome_coletor, None)
            montar = getattr(metadados_livro, nome_vars, None)
            if coletor and montar:
                try:
                    return montar(coletor(slug, dir_livro=dir_livro))
                except Exception as e:  # noqa: BLE001
                    print(f"  [AVISO] Metadados de {tipo} indisponiveis: {e}")
                    return []

    if tipo == "tcc" and metadados_livro is not None:
        try:
            dados = metadados_livro.coletar_tcc(slug, dir_livro=dir_livro)
            return metadados_livro.variaveis_pandoc_tcc(dados)
        except Exception as e:  # noqa: BLE001
            print(f"  [AVISO] Metadados de TCC indisponiveis: {e}")
            return []
    if tipo == "artigo" and metadados_livro is not None and hasattr(metadados_livro, "coletar_artigo"):
        try:
            dados = metadados_livro.coletar_artigo(slug, dir_livro=dir_livro)
            return metadados_livro.variaveis_pandoc_artigo(dados)
        except Exception as e:  # noqa: BLE001
            print(f"  [AVISO] Metadados de artigo indisponiveis: {e}")
            return []
    if metadados_livro is not None:
        try:
            dados = metadados_livro.coletar(slug, paginas=paginas, dir_livro=dir_livro)
            args += metadados_livro.variaveis_pandoc(dados)
        except Exception as e:  # noqa: BLE001
            print(f"  [AVISO] Metadados de capa/CIP indisponiveis: {e}")
    # Capa em imagem (padrao visual da serie): sobrepoe a capa tipografica do template
    capa_img = dir_livro / "imagens" / "capa_livro.png"
    if CAPA_GRAFICA and capa_img.exists() and "-V" not in args and "capa_imagem=imagens/capa_livro.png" not in args:
        # adiciona apenas se metadados_livro nao ja tiver adicionado capa_imagem
        tem_capa_imagem = any(isinstance(a, str) and a.startswith("capa_imagem=") for a in args)
        if not tem_capa_imagem:
            args += ["-V", "capa_imagem=imagens/capa_livro.png"]
    if not CAPA_GRAFICA:
        args += ["-V", "sem_capa_grafica=1"]
    # Regra editorial (V5.5): LIVRO pode pular a folha de rosto (capa -> CIP direto)
    # quando config_obra.json declara "sem_folha_rosto": true (opt-in por obra).
    if tipo == "livro" and flag_config(dir_livro, "sem_folha_rosto"):
        args += ["-V", "sem_folha_rosto=1"]
    return args


AUTOR_PADRAO = "Heverton Eduardo Peres"


def resolver_autor(dir_livro):
    """Autor do PDF: config_obra.json["autor"] tem prioridade; sem o campo,
    usa AUTOR_PADRAO (compatibilidade com obras que nao declararam autor)."""
    caminho = dir_livro / "config_obra.json"
    if caminho.exists():
        import json
        try:
            config = json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            config = {}
        autor = config.get("autor")
        if autor:
            return autor
    return AUTOR_PADRAO


def comando_pandoc(md_path, saida, dir_livro, titulo, extras, tipo=None):
    """Comando Pandoc que gera o Typst intermediario (sem --pdf-engine: ver
    converter_via_typst para o motivo)."""
    tipo = tipo or "livro"
    template = template_para_tipo(tipo)
    comando = [
        PANDOC,
        str(md_path),
        "-o", str(saida),
        "--template", str(template),
        "--toc",
        "--toc-depth", "3",
    ]
    # TCC/Artigo ja trazem numeracao progressiva manual (NBR 6024) escrita pelo
    # redator-academico — "--number-sections" duplicaria a numeracao. Playbook,
    # lead magnet e deck tambem nao numeram. V5: a decisao vem do registro.
    numerar = (tipos_obra.campo(tipo, "numerar_secoes", tipo == "livro")
               if tipos_obra is not None else tipo == "livro")
    if numerar:
        comando.append("--number-sections")
    comando += [
        "--from", "markdown-citations",
        "--wrap", "preserve",
        "-V", f"title={titulo}",
        "-V", f"author={resolver_autor(dir_livro)}",
        "-V", "subtitle=",
        "--resource-path", str(dir_livro),
    ]
    return comando + extras


def converter_via_typst(md_path, pdf_path, dir_livro, titulo, extras, timeout=300, tipo=None):
    """Pandoc -> .typ -> typst compile.

    Caminho principal desde a V3. O modo `pandoc --pdf-engine=typst` extrai as
    imagens para uma pasta temporaria e reescreve os caminhos em forma ABSOLUTA,
    o que o Typst rejeita no Windows ("path contains invalid component C:").
    Gerando o .typ intermediario dentro da pasta do livro, os caminhos relativos
    das figuras (imagens/diagramas/*.png) continuam validos.
    """
    typ_path = dir_livro / "livro-compilado.typ"
    resultado = subprocess.run(
        comando_pandoc(md_path, typ_path, dir_livro, titulo, extras, tipo=tipo),
        capture_output=True, text=True, timeout=timeout,
    )
    if not typ_path.exists() or typ_path.stat().st_size == 0:
        return False, f"pandoc nao gerou .typ: {(resultado.stderr or '').strip()[-300:]}"

    resultado = subprocess.run(
        [TYPST, "compile", "--root", str(dir_livro), str(typ_path), str(pdf_path)],
        capture_output=True, text=True, timeout=timeout,
    )
    if pdf_path.exists() and pdf_path.stat().st_size > 0:
        typ_path.unlink(missing_ok=True)
        return True, ""
    erro = (resultado.stderr or resultado.stdout or "").strip()
    return False, erro[-600:] or "typst nao gerou PDF"


def converter_md_direto(slug, dir_livro, md_path, pdf_path):
    """Converte livro_final.md pre-compilado diretamente para PDF via Pandoc+Typst."""
    tipo = resolver_tipo(slug)
    print(f"  Convertendo MD pre-compilado -> PDF... (tipo_obra={tipo})")

    # Extrair titulo do sumario
    titulo = slug
    sumario_path = dir_livro / "sumario_macro.json"
    if sumario_path.exists():
        import json
        with open(sumario_path, 'r', encoding='utf-8') as f:
            try:
                sumario = json.load(f)
                titulo = sumario.get('titulo_obra', slug)
            except:
                pass

    md_render = renderizar_diagramas(slug, dir_livro, md_path)
    extras = variaveis_visuais(slug, dir_livro, tipo=tipo)

    try:
        ok, erro = converter_via_typst(md_render, pdf_path, dir_livro, titulo, extras, tipo=tipo)

        if ok and PAGINAS_EXATAS and tipo == "livro" and metadados_livro is not None:
            paginas = metadados_livro.contar_paginas_pdf(pdf_path)
            if paginas:
                print(f"  Segunda passagem: gravando {paginas} paginas na ficha CIP")
                converter_via_typst(md_render, pdf_path, dir_livro, titulo,
                                    variaveis_visuais(slug, dir_livro, paginas, tipo=tipo),
                                    tipo=tipo)

        if ok:
            tamanho_kb = pdf_path.stat().st_size / 1024
            print(f"  [OK] PDF gerado: {pdf_path.name} ({tamanho_kb:.1f} KB)")
            copiar_pdf_com_nome_slug(slug, dir_livro)
            return True

        print(f"  [FALHA] PDF nao foi criado")
        for linha in erro.split("\n")[-5:]:
            if linha.strip():
                print(f"  STDERR: {linha.strip()}")
        return False

    except subprocess.TimeoutExpired:
        print(f"  [ERRO] Timeout - conversao excedeu 300s")
        return False
    except Exception as e:
        print(f"  [ERRO] Falha na conversao: {e}")
        return False


def compilar_por_motor_proprio(slug, tipo):
    """Delega aos tipos que NAO usam Pandoc->Typst (V5).

    Hoje so o lead magnet: peca de marketing renderiza melhor por HTML+CSS no
    Chromium. Devolve None quando o tipo usa o motor padrao."""
    if tipos_obra is None:
        return None
    compilador = tipos_obra.compilador_de(tipo)
    if compilador is None or not Path(compilador).exists():
        return None
    print(f"  motor_pdf={tipos_obra.motor_pdf(tipo)} -> delegando para {Path(compilador).name}")
    return subprocess.run([sys.executable, str(compilador), slug]).returncode == 0


def compilar_livro(slug):
    """Compila livro com capitulos reais e gera PDF profissional via Pandoc+Typst."""
    tipo = resolver_tipo(slug)
    resultado_proprio = compilar_por_motor_proprio(slug, tipo)
    if resultado_proprio is not None:
        return resultado_proprio

    # V5: resolve no HUB POR COLECAO via tipos_obra.dir_obra (layout plano era
    # output/<tipo>/<slug>; o hub e output/<colecao>/<tipo>/<slug>).
    dir_livro = (tipos_obra.dir_obra(slug, DIR_RAIZ)
                 if tipos_obra is not None else DIR_RAIZ / slug)

    # Gap 8: se dir_livro aponta para o HUB (output/<colecao>/) mas nao tem
    # capitulos/ nem livro_final.md, tenta o subdir do tipo (single-book layout:
    # output/<obra>/<tipo>/ — ex.: output/gratis-open-source/livros/).
    if not (dir_livro / "capitulos").exists() and not (dir_livro / "livro_final.md").exists():
        for raiz_tipo in ("livros", "tccs", "artigos", "ebooks", "playbooks",
                          "lead-magnets", "decks", "emails", "manuais-diarios"):
            cand = dir_livro / raiz_tipo
            if cand.exists() and ((cand / "capitulos").exists() or (cand / "livro_final.md").exists()):
                dir_livro = cand
                break
        # Ou: o slug sem prefixo resolve se anexarmos livros/ (layout plano)
        if not (dir_livro / "capitulos").exists() and not (dir_livro / "livro_final.md").exists():
            cand = DIR_RAIZ / "livros" / slug
            if cand.exists() and ((cand / "capitulos").exists() or (cand / "livro_final.md").exists()):
                dir_livro = cand

    dir_caps = dir_livro / "capitulos"
    dir_imagens = dir_livro / "imagens"

    # Caminho do PDF final
    pdf_path = dir_livro / "livro_final.pdf"

    print(f"\n{'='*60}")
    print(f"  COMPILANDO: {slug}")
    print(f"{'='*60}")

    # V5: derivados de extracao trazem o Markdown pronto com nome proprio
    # (playbook.md / lead_magnet.md / deck.md) — nao passam por merge de capitulos.
    md_precompilado = dir_livro / "livro_final.md"
    fonte_propria = FONTE_MD_POR_TIPO.get(tipo)
    if fonte_propria and (dir_livro / fonte_propria).exists():
        md_precompilado = dir_livro / fonte_propria

    if md_precompilado.exists():
        # Preferir o livro_final.md pre-compilado: contem titulo, prefacio, sumario,
        # cabecalhos de Parte, capitulos e conclusao (estrutura ABNT completa).
        print(f"  Usando livro_final.md pre-compilado (estrutura completa)")
        return converter_md_direto(slug, dir_livro, md_precompilado, pdf_path)

    # --- Caminho legado: apenas para livros SEM livro_final.md (montagem por capítulos) ---
    # Ler todos os capitulos ordenados
    caps = sorted(
        dir_caps.glob("cap_*.md"),
        key=lambda p: int(re.search(r'cap_(\d+)', p.stem).group(1))
    )

    if not caps:
        print(f"  [SKIP] {slug}: nenhum capitulo ou livro_final.md encontrado")
        return False

    print(f"  Capitulos encontrados: {len(caps)}")

    # Montar conteudo completo: introducao + capitulos + conclusao
    partes = []

    # 1. Introducao
    intro_path = dir_livro / "introducao.md"
    if intro_path.exists():
        with open(intro_path, 'r', encoding='utf-8') as f:
            partes.append(f.read())
        print(f"  + Introducao incluida")

    # 2. Capitulos (sanitizar frontmatter interno e adicionar)
    for cap_path in caps:
        with open(cap_path, 'r', encoding='utf-8') as f:
            conteudo = f.read().strip()
        # Remover qualquer frontmatter YAML interno que possa conflitar
        conteudo = re.sub(r'^---\n.*?\n---\n', '', conteudo, flags=re.DOTALL)
        partes.append(conteudo)

    # 3. Conclusao
    conclusao_path = dir_livro / "conclusao.md"
    if conclusao_path.exists():
        with open(conclusao_path, 'r', encoding='utf-8') as f:
            partes.append(f.read().strip())
        print(f"  + Conclusao incluida")

    # Juntar tudo - Typst/Pandoc cuidam das quebras de pagina naturalmente
    # (o template ja insere pagebreak antes de cada h1)
    todo_conteudo = '\n\n'.join(partes)

    # Extrair titulo do sumario_macro.json para metadados
    titulo = slug
    sumario_path = dir_livro / "sumario_macro.json"
    if sumario_path.exists():
        import json
        with open(sumario_path, 'r', encoding='utf-8') as f:
            try:
                sumario = json.load(f)
                titulo = sumario.get('titulo_obra', slug)
            except:
                pass

    # Criar frontmatter YAML completo para o Pandoc
    frontmatter = f"""---
title: "{titulo}"
author: "{resolver_autor(dir_livro)}"
date: "Julho 2026"
lang: pt-BR
---
"""

    # Montar MD final
    md_final = frontmatter + '\n' + todo_conteudo

    # Salvar MD compilado
    md_compilado = dir_livro / "livro-compilado.md"
    with open(md_compilado, 'w', encoding='utf-8') as f:
        f.write(md_final)

    # Converter para PDF via Pandoc + Typst
    tipo = resolver_tipo(slug)
    print(f"  Convertendo MD -> PDF (Pandoc + Typst)... (tipo_obra={tipo})")

    md_compilado = renderizar_diagramas(slug, dir_livro, md_compilado)
    extras = variaveis_visuais(slug, dir_livro, tipo=tipo)

    try:
        ok, erro = converter_via_typst(md_compilado, pdf_path, dir_livro, titulo,
                                       extras, timeout=180, tipo=tipo)

        # Segunda passagem (--paginas-exatas): grava contagem real na ficha CIP
        # no caminho legado (chapters) — o mesmo que converter_md_direto já faz.
        if ok and PAGINAS_EXATAS and tipo == "livro" and metadados_livro is not None:
            paginas = metadados_livro.contar_paginas_pdf(pdf_path)
            if paginas:
                print(f"  Segunda passagem: gravando {paginas} paginas na ficha CIP")
                converter_via_typst(md_compilado, pdf_path, dir_livro, titulo,
                                    variaveis_visuais(slug, dir_livro, paginas, tipo=tipo),
                                    timeout=180, tipo=tipo)

        if ok:
            tamanho_kb = pdf_path.stat().st_size / 1024
            print(f"  [OK] PDF gerado: {pdf_path.name} ({tamanho_kb:.1f} KB)")
            copiar_pdf_com_nome_slug(slug, dir_livro)

            # Limpar temporario
            if md_compilado.exists():
                md_compilado.unlink()

            return True
        else:
            print(f"  [FALHA] PDF nao foi criado")
            for linha in erro.split("\n")[-5:]:
                if linha.strip():
                    print(f"  STDERR: {linha.strip()}")
            return False

    except subprocess.TimeoutExpired:
        print(f"  [ERRO] Timeout - conversao excedeu 180s")
        return False
    except Exception as e:
        print(f"  [ERRO] Falha na conversao: {e}")
        return False


def main():
    global RENDERIZAR_DIAGRAMAS, CAPA_GRAFICA, PAGINAS_EXATAS, TIPO_OVERRIDE

    argumentos = sys.argv[1:]
    RENDERIZAR_DIAGRAMAS = "--sem-diagramas" not in argumentos
    CAPA_GRAFICA = "--sem-capa" not in argumentos
    PAGINAS_EXATAS = "--paginas-exatas" in argumentos
    if "--tipo" in argumentos:
        i = argumentos.index("--tipo")
        TIPO_OVERRIDE = argumentos[i + 1] if i + 1 < len(argumentos) else None
        argumentos = argumentos[:i] + argumentos[i + 2:]
    slugs_alvo = [a for a in argumentos if not a.startswith("--")]

    # Verificar pre-requisitos
    for cmd, nome in [(PANDOC, "Pandoc"), (TYPST, "Typst")]:
        if not os.path.exists(cmd):
            print(f"[ERRO] {nome} nao encontrado em: {cmd}")
            sys.exit(1)

    if not TEMPLATE.exists():
        print(f"[ERRO] Template Typst nao encontrado em: {TEMPLATE}")
        sys.exit(1)

    # Verificar se temos slugs validos
    if slugs_alvo:
        slugs = [s for s in SLUGS if s in slugs_alvo]
        # Obras novas (criadas por /criar-livro) ainda nao estao no catalogo
        # estatico: aceita qualquer slug que exista em output/ (plano ou hub).
        for alvo in slugs_alvo:
            if alvo not in slugs:
                if (DIR_RAIZ / alvo).is_dir():
                    slugs.append(alvo)
                elif tipos_obra is not None and tipos_obra.dir_obra(alvo, DIR_RAIZ).exists():
                    slugs.append(alvo)
        if not slugs:
            print(f"Slug(s) nao encontrado(s) no catalogo nem em {DIR_RAIZ}")
            sys.exit(1)
    else:
        slugs = SLUGS

    print(f"Iniciando compilacao de {len(slugs)} livro(s)...")
    print(f"  Pandoc: {PANDOC}")
    print(f"  Typst: {TYPST}")
    print(f"  Template: {TEMPLATE}")
    print(f"  Diagramas Mermaid: {'ativos' if RENDERIZAR_DIAGRAMAS else 'desativados'}")
    print(f"  Capa grafica: {'ativa' if CAPA_GRAFICA else 'desativada'}")

    sucessos = 0
    falhas = 0

    for slug in slugs:
        if compilar_livro(slug):
            sucessos += 1
        else:
            falhas += 1

    print(f"\n{'='*60}")
    print(f"  RESUMO: {sucessos} OK, {falhas} falha(s)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
