#!/usr/bin/env python3
"""
Upgrade 5 (metadados) — Capa profissional, ficha catalografica e sinopse.

Deriva de forma determinística todas as variaveis que o `templates/template.typ`
consome para montar capa grafica, folha de rosto, ficha catalografica (CIP
ficticia) e contracapa:

    cor_acento, cip_sobrenome, cip_nome, cip_cutter, cip_ano, cip_paginas,
    cip_palavras, cip_cdd, cip_isbn, cip_local, cip_editora, sinopse

Importavel (usado por compilar-para-pdf.py) e executavel:

    python scripts/metadados_livro.py <slug>                  # inspecao humana
    python scripts/metadados_livro.py <slug> --pandoc-args    # 1 arg por linha
    python scripts/metadados_livro.py <slug> --json
"""

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
import tipos_obra as TO

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from series_capa import resolver_cor, resolver_serie_key  # noqa: E402

AUTOR_PADRAO = "Heverton Eduardo Peres"

RE_DOLLAR_SOLTO = re.compile(r"(?<!\\)\$(?!\$)")


def _escapar_typst(valor):
    r"""Escapa `$` solitario (nao precedido de `\` nem seguido de outro `$`) para
    o Pandoc/Typst nao interpretar como abertura de modo matematico — mesma
    regra ja aplicada ao corpo do livro em `converter-md-pdf.ps1`, mas que
    faltava nas variaveis -V (sinopse, titulo etc.) do caminho Python."""
    return RE_DOLLAR_SOLTO.sub(r"\\$", valor)
LOCAL_PADRAO = "São Paulo"
EDITORA_PADRAO = "Fábrica Agêntica de Livros"

CARACTERES_POR_PAGINA = 2500  # aproximacao ABNT (A4, Times 12pt, margens 3/2cm)

# Heuristica de classificacao decimal (CDD) por dominio da obra
TABELA_CDD = [
    (("agente", "agentic", "llm", "ia ", "inteligencia artificial", "prompt", "rag",
      "machine learning", "deep learning", "gpt", "claude", "deepseek"), "006.3"),
    (("banco de dados", "sql", "postgres", "mysql", "modelagem de dados",
      "data warehouse", "dados"), "005.74"),
    (("seguranca", "pentest", "criptografia", "hacking", "vulnerabilidade"), "005.8"),
    (("devops", "kubernetes", "docker", "cloud", "infraestrutura", "sre",
      "observabilidade", "terraform"), "004.6"),
    (("javascript", "typescript", "python", "java", "golang", "rust", "codigo",
      "programacao", "framework", "react", "node", "git", "software",
      "desenvolvimento", "fullstack", "frontend", "backend", "api"), "005.1"),
    (("marketing", "trafego", "anuncio", "vendas", "growth", "funil", "seo"), "658.8"),
    (("planejamento", "estrategia", "gestao", "negocio", "produto", "okr",
      "lideranca", "empreendedorismo"), "658.4"),
    (("perfume", "perfumaria", "cosmetico", "fragrancia", "aroma"), "668.54"),
    (("financas", "investimento", "contabilidade", "economia"), "332"),
]

STOPWORDS_TITULO = {
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos", "e",
    "em", "entre", "na", "nas", "no", "nos", "o", "os", "para", "pela", "pelo",
    "por", "que", "sem", "sob", "sobre", "um", "uma", "ate", "seu", "sua",
    "guia", "livro", "completo", "pratico", "parte", "capitulo", "introducao",
    "conclusao", "zero", "profissional", "avancado", "basico", "moderno",
    "definitivo", "essencial", "fundamentos", "dominando", "domine", "todos",
}


def sem_acento(texto):
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


def partir_autor(autor):
    partes = [p for p in autor.strip().split() if p]
    if len(partes) < 2:
        return autor.strip(), ""
    return partes[-1], " ".join(partes[:-1])


def cutter(sobrenome, titulo):
    """Notacao de Cutter ficticia, estavel e plausivel (ex.: P437f)."""
    inicial = (sem_acento(sobrenome)[:1] or "X").upper()
    digest = hashlib.sha1(sem_acento(sobrenome + titulo).lower().encode("utf-8")).digest()
    numero = 100 + (int.from_bytes(digest[:2], "big") % 900)
    primeira_titulo = ""
    for palavra in re.findall(r"[A-Za-zÀ-ÿ]+", titulo):
        if sem_acento(palavra).lower() not in STOPWORDS_TITULO:
            primeira_titulo = sem_acento(palavra)[:1].lower()
            break
    return f"{inicial}{numero}{primeira_titulo}"


def isbn_ficticio(slug):
    """ISBN-13 ficticio com digito verificador valido, prefixo 978-65-00000-xx-x."""
    digest = hashlib.sha1(slug.encode("utf-8")).digest()
    corpo = f"9786500000{digest[0] % 100:02d}"  # 12 digitos
    soma = sum((1 if i % 2 == 0 else 3) * int(d) for i, d in enumerate(corpo))
    verificador = (10 - soma % 10) % 10
    return f"978-65-00000-{digest[0] % 100:02d}-{verificador}"


def palavras_chave(titulo, sumario):
    """Assuntos da CIP a partir do titulo e dos titulos de capitulo."""
    fonte = [titulo]
    for parte in sumario.get("partes", []):
        fonte.append(parte.get("titulo_parte", ""))
        for cap in TO.unidades_da_parte(parte):
            fonte.append(cap.get("titulo", ""))

    contagem = Counter()
    original = {}
    for texto in fonte:
        for palavra in re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9\-\+#\.]{2,}", texto or ""):
            chave = sem_acento(palavra).lower().strip(".-")
            if chave in STOPWORDS_TITULO or len(chave) < 4:
                continue
            contagem[chave] += 1
            original.setdefault(chave, palavra.strip(".,;:"))

    escolhidas = [original[c] for c, _ in contagem.most_common(4)]
    if not escolhidas:
        escolhidas = ["Literatura técnica"]
    itens = [f"{i}. {termo[:1].upper() + termo[1:]}." for i, termo in enumerate(escolhidas, 1)]
    return " ".join(itens) + " I. Título."


def classificar_cdd(titulo, sumario):
    alvo = sem_acento(" ".join([
        titulo,
        " ".join(p.get("titulo_parte", "") for p in sumario.get("partes", [])),
        " ".join(c.get("titulo", "")
                 for p in sumario.get("partes", [])
                 for c in TO.unidades_da_parte(p)),
    ])).lower()
    for termos, cdd in TABELA_CDD:
        if any(t in alvo for t in termos):
            return cdd
    return "001.2"


def extrair_sinopse(dir_livro, sumario, limite=620):
    """Sinopse da contracapa: introducao do sumario ou 1o paragrafo do prefacio."""
    texto = (sumario.get("introducao") or "").strip()
    if not texto:
        md = dir_livro / "livro_final.md"
        if md.exists():
            conteudo = md.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"^#\s*(Pref[áa]cio|Introdu[çc][ãa]o).*?\n(.*?)(?=\n#|\Z)",
                          conteudo, re.DOTALL | re.MULTILINE | re.IGNORECASE)
            if m:
                for par in re.split(r"\n\s*\n", m.group(2)):
                    par = par.strip()
                    if len(par.split()) > 25 and not par.startswith(("!", "|", ">", "#")):
                        texto = par
                        break
    texto = re.sub(r"\s+", " ", texto).strip()
    texto = re.sub(r"\[\d+\]", "", texto)
    if len(texto) > limite:
        corte = texto[:limite].rsplit(". ", 1)
        texto = (corte[0] + ".") if len(corte) > 1 else texto[:limite].rstrip() + "..."
    return texto


def contar_paginas_pdf(pdf_path):
    try:
        dados = Path(pdf_path).read_bytes()
        return len(re.findall(rb"/Type\s*/Page[^s]", dados))
    except Exception:  # noqa: BLE001
        return 0


def coletar(slug, autor=AUTOR_PADRAO, paginas=None, dir_livro=None):
    """Monta o dicionario completo de metadados da obra."""
    dir_livro = Path(dir_livro) if dir_livro else TO.dir_obra(slug, DIR_OUTPUT)

    sumario = {}
    caminho_sumario = dir_livro / "sumario_macro.json"
    if caminho_sumario.exists():
        try:
            sumario = json.loads(caminho_sumario.read_text(encoding="utf-8"))
        except ValueError:
            sumario = {}

    titulo = sumario.get("titulo_obra") or slug
    md = dir_livro / "livro_final.md"
    if not sumario.get("titulo_obra") and md.exists():
        m = re.search(r"^#\s+(.+)$", md.read_text(encoding="utf-8", errors="replace"),
                      re.MULTILINE)
        if m:
            titulo = m.group(1).strip()

    subtitulo = sumario.get("subtitulo", "") or ""

    if paginas is None:
        pdf = dir_livro / "livro_final.pdf"
        paginas = contar_paginas_pdf(pdf) if pdf.exists() else 0
        if not paginas and md.exists():
            paginas = max(1, round(len(md.read_text(encoding="utf-8", errors="replace"))
                                   / CARACTERES_POR_PAGINA))

    sobrenome, nome = partir_autor(autor)
    ano = str(sumario.get("ano") or __import__("datetime").date.today().year)

    config_obra = {}
    caminho_config = dir_livro / "config_obra.json"
    if caminho_config.exists():
        try:
            config_obra = json.loads(caminho_config.read_text(encoding="utf-8"))
        except ValueError:
            config_obra = {}
    cor_acento = resolver_cor(resolver_serie_key(config_obra, slug), slug)

    # Capa grafica: verifica se existe imagens/capa_livro.png ou imagens/capa.png
    capa_imagem = ""
    for nome_capa in ("capa_livro.png", "capa.png"):
        caminho_capa = dir_livro / "imagens" / nome_capa
        if caminho_capa.exists():
            # Typst requer path relativo ao diretorio do livro (rejeita absolutos no Windows)
            capa_imagem = f"imagens/{nome_capa}"
            break

    return {
        "titulo": titulo,
        "subtitulo": subtitulo,
        "autor": autor,
        "cor_acento": cor_acento,
        "cip_sobrenome": sobrenome,
        "cip_nome": nome,
        "cip_cutter": cutter(sobrenome, titulo),
        "cip_ano": ano,
        "cip_paginas": str(paginas or ""),
        "cip_palavras": palavras_chave(titulo, sumario),
        "cip_cdd": classificar_cdd(titulo, sumario),
        "cip_isbn": isbn_ficticio(slug),
        "cip_local": LOCAL_PADRAO,
        "cip_editora": EDITORA_PADRAO,
        "sinopse": extrair_sinopse(dir_livro, sumario),
        "capa_imagem": capa_imagem,
    }


CHAVES_PANDOC = (
    "cor_acento", "cip_sobrenome", "cip_nome", "cip_cutter", "cip_ano", "cip_paginas",
    "cip_palavras", "cip_cdd", "cip_isbn", "cip_local", "cip_editora", "sinopse",
    "capa_imagem",
)

# ── V4: metadados de TCC (folha de rosto/aprovacao, resumo/abstract) ──────────

CAMINHO_TCC_METADADOS = "tcc_metadados.json"
CHAVES_PANDOC_TCC = (
    "resumo", "palavras_chave", "abstract_en", "keywords_en",
    "instituicao", "curso", "orientador", "local", "ano",
)


def coletar_tcc(slug, autor=AUTOR_PADRAO, dir_livro=None):
    """Metadados de TCC: le output/<slug>/tcc_metadados.json (gravado pelo
    compilador-tcc na Fase 3) com defaults minimos se ainda nao existir."""
    dir_livro = Path(dir_livro) if dir_livro else TO.dir_obra(slug, DIR_OUTPUT)
    caminho = dir_livro / CAMINHO_TCC_METADADOS
    dados = {}
    if caminho.exists():
        try:
            dados = json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            dados = {}

    titulo = slug
    sumario_path = dir_livro / "sumario_macro.json"
    if sumario_path.exists():
        try:
            sumario = json.loads(sumario_path.read_text(encoding="utf-8"))
            titulo = sumario.get("titulo_obra", slug)
        except ValueError:
            pass

    ano = str(dados.get("ano") or __import__("datetime").date.today().year)
    return {
        "titulo": titulo,
        "autor": autor,
        "resumo": dados.get("resumo", ""),
        "palavras_chave": dados.get("palavras_chave", ""),
        "abstract_en": dados.get("abstract_en", ""),
        "keywords_en": dados.get("keywords_en", ""),
        "instituicao": dados.get("instituicao", ""),
        "curso": dados.get("curso", ""),
        "orientador": dados.get("orientador", ""),
        "local": dados.get("local", LOCAL_PADRAO),
        "ano": ano,
    }


def variaveis_pandoc_tcc(dados):
    args = []
    for chave in CHAVES_PANDOC_TCC:
        valor = (dados.get(chave) or "").strip()
        if valor:
            args += ["-V", f"{chave}={_escapar_typst(valor)}"]
    return args


# ── V4: metadados de Artigo Cientifico (resumo/abstract, sem folha de rosto) ──

CAMINHO_ARTIGO_METADADOS = "artigo_metadados.json"
CHAVES_PANDOC_ARTIGO = ("resumo", "palavras_chave", "abstract_en", "keywords_en")


def coletar_artigo(slug, autor=AUTOR_PADRAO, dir_livro=None):
    """Metadados de artigo: le <dir_livro>/artigo_metadados.json (gravado pelo
    compilador-artigo na Fase 3) com defaults minimos se ainda nao existir."""
    dir_livro = Path(dir_livro) if dir_livro else TO.dir_obra(slug, DIR_OUTPUT)
    caminho = dir_livro / CAMINHO_ARTIGO_METADADOS
    dados = {}
    if caminho.exists():
        try:
            dados = json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            dados = {}

    titulo = slug
    sumario_path = dir_livro / "sumario_macro.json"
    if sumario_path.exists():
        try:
            sumario = json.loads(sumario_path.read_text(encoding="utf-8"))
            titulo = sumario.get("titulo_obra", slug)
        except ValueError:
            pass

    return {
        "titulo": titulo,
        "autor": autor,
        "resumo": dados.get("resumo", ""),
        "palavras_chave": dados.get("palavras_chave", ""),
        "abstract_en": dados.get("abstract_en", ""),
        "keywords_en": dados.get("keywords_en", ""),
    }


def variaveis_pandoc_artigo(dados):
    args = []
    for chave in CHAVES_PANDOC_ARTIGO:
        valor = (dados.get(chave) or "").strip()
        if valor:
            args += ["-V", f"{chave}={_escapar_typst(valor)}"]
    return args


# ── V5: derivados de extracao (playbook, lead magnet, deck) ───────────────────
# Sem ISBN/CIP/CDD: nenhum dos tres e obra catalogada. As chaves alimentam os
# templates templates/template_{playbook,lead_magnet,deck}.typ.
CHAVES_PANDOC_PLAYBOOK = ("objetivo_material", "livro_mae", "total_passos",
                          "persona", "cor_acento", "capa_imagem", "badge_nivel")
CHAVES_PANDOC_LEAD_MAGNET = ("promessa", "livro_mae", "formato_lm", "cta_url",
                             "cta_texto", "cor_acento", "capa_imagem", "badge_nivel")
CHAVES_PANDOC_DECK = ("livro_mae", "total_slides", "cta_url", "cta_texto",
                      "cor_acento", "capa_imagem", "badge_nivel")

ROTULOS_NIVEL = {"iniciante": "PARA INICIANTES", "intermediario": "NÍVEL INTERMEDIÁRIO",
                 "intermediário": "NÍVEL INTERMEDIÁRIO", "avancado": "NÍVEL AVANÇADO",
                 "avançado": "NÍVEL AVANÇADO", "tecnico": "NÍVEL TÉCNICO",
                 "técnico": "NÍVEL TÉCNICO"}


def _contexto_derivado(slug, dir_livro=None):
    """Bloco comum aos tres derivados: config + sumario + capa + cor da colecao."""
    dir_livro = Path(dir_livro) if dir_livro else TO.dir_obra(slug, DIR_OUTPUT)
    config = _ler_json_seguro(dir_livro / "config_obra.json")
    sumario = _ler_json_seguro(dir_livro / "sumario_macro.json")

    capa = ""
    for nome in ("capa_livro.png", "capa.png"):
        if (dir_livro / "imagens" / nome).exists():
            capa = f"imagens/{nome}"
            break

    try:
        cor = resolver_cor(resolver_serie_key(config, slug), slug)
    except Exception:  # noqa: BLE001 — cor e cosmetica, nao bloqueia a compilacao
        cor = ""

    nivel = (config.get("senioridade_obra") or "").strip().lower()
    return {
        "dir": dir_livro,
        "config": config,
        "sumario": sumario,
        "titulo": sumario.get("titulo_obra") or config.get("tema") or slug,
        "livro_mae": TO.resolver_slug_mae(config) or sumario.get("slug_livro_mae", ""),
        "capa_imagem": capa,
        "cor_acento": cor,
        "badge_nivel": ROTULOS_NIVEL.get(nivel, nivel.upper()),
    }


def _ler_json_seguro(caminho):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return {}
    return {}


def coletar_playbook(slug, autor=AUTOR_PADRAO, dir_livro=None):
    ctx = _contexto_derivado(slug, dir_livro)
    passos = len(list((ctx["dir"] / "passos").glob("passo_*.json"))) \
        if (ctx["dir"] / "passos").exists() else 0
    motivo = ctx["sumario"].get("motivo_condutor") or {}
    objetivo = (ctx["sumario"].get("objetivo_material")
                or motivo.get("descricao")
                or f"Executar os passos práticos de {ctx['titulo']} do início ao fim.")
    return {
        "titulo": ctx["titulo"], "autor": autor,
        "objetivo_material": objetivo,
        "livro_mae": ctx["livro_mae"],
        "total_passos": str(passos),
        "persona": motivo.get("persona_leitor", ""),
        "cor_acento": ctx["cor_acento"],
        "capa_imagem": ctx["capa_imagem"],
        "badge_nivel": ctx["badge_nivel"],
    }


def coletar_lead_magnet(slug, autor=AUTOR_PADRAO, dir_livro=None):
    ctx = _contexto_derivado(slug, dir_livro)
    return {
        "titulo": ctx["titulo"], "autor": autor,
        "promessa": ctx["sumario"].get("subtitulo", ""),
        "livro_mae": ctx["livro_mae"],
        "formato_lm": ctx["config"].get("formato_lm", ""),
        "cta_url": ctx["config"].get("cta_url", ""),
        "cta_texto": ctx["config"].get("cta_texto", ""),
        "cor_acento": ctx["cor_acento"],
        "capa_imagem": ctx["capa_imagem"],
        "badge_nivel": ctx["badge_nivel"],
    }


def coletar_deck(slug, autor=AUTOR_PADRAO, dir_livro=None):
    ctx = _contexto_derivado(slug, dir_livro)
    return {
        "titulo": ctx["titulo"], "autor": autor,
        "livro_mae": ctx["livro_mae"],
        "total_slides": str(ctx["sumario"].get("total_slides", "")),
        "cta_url": ctx["config"].get("cta_url", ""),
        "cta_texto": ctx["config"].get("cta_texto", ""),
        "cor_acento": ctx["cor_acento"],
        "capa_imagem": ctx["capa_imagem"],
        "badge_nivel": ctx["badge_nivel"],
    }


def _variaveis(dados, chaves):
    args = []
    for chave in chaves:
        valor = (dados.get(chave) or "").strip()
        if valor:
            args += ["-V", f"{chave}={_escapar_typst(valor)}"]
    return args


def variaveis_pandoc_playbook(dados):
    return _variaveis(dados, CHAVES_PANDOC_PLAYBOOK)


def variaveis_pandoc_lead_magnet(dados):
    return _variaveis(dados, CHAVES_PANDOC_LEAD_MAGNET)


def variaveis_pandoc_deck(dados):
    return _variaveis(dados, CHAVES_PANDOC_DECK)


def variaveis_pandoc(metadados):
    """Lista achatada de argumentos ['-V', 'chave=valor', ...] para o Pandoc."""
    args = []
    for chave in CHAVES_PANDOC:
        valor = (metadados.get(chave) or "").strip()
        if valor:
            args += ["-V", f"{chave}={_escapar_typst(valor)}"]
    return args


def main():
    ap = argparse.ArgumentParser(description="Metadados de capa/CIP da obra")
    ap.add_argument("slug")
    ap.add_argument("--autor", default=AUTOR_PADRAO)
    ap.add_argument("--paginas", type=int, default=None)
    ap.add_argument("--pandoc-args", action="store_true",
                    help="imprime um argumento por linha (consumivel por PowerShell)")
    ap.add_argument("--titulo", action="store_true",
                    help="imprime apenas o titulo canonico da obra")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not (TO.dir_obra(args.slug, DIR_OUTPUT)).exists():
        print(f"[ERRO] Livro nao encontrado: {TO.dir_obra(args.slug, DIR_OUTPUT)}")
        return 1

    dados = coletar(args.slug, args.autor, args.paginas)

    if args.titulo:
        print(dados["titulo"])
        return 0
    if args.pandoc_args:
        for item in variaveis_pandoc(dados):
            print(item)
        return 0
    if args.json:
        print(json.dumps(dados, ensure_ascii=False, indent=2))
        return 0

    for chave, valor in dados.items():
        print(f"{chave:<16}: {valor}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
