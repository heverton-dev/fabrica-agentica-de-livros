#!/usr/bin/env python3
"""
V5 — Registro declarativo de TIPOS DE OBRA (substitui o dispatch `if tipo == ...`).

Antes da V5 cada tipo novo exigia editar 6 arquivos (parametros_obra, fatiar-obra,
auditar-obra, gerar-capa, metadados_livro, compilar-para-pdf). Agora um tipo novo e
UMA entrada de dicionario aqui; os 6 scripts consultam este registro.

Campos do descritor:
  rotulo                 nome humano (PT-BR)
  prefixo_curto          codigo de 2-3 letras usado no nome curto (lm, pbk, dck)
  nomes_curtos           True = usa a convencao V5.1 (scripts/nomes_curtos.py)
  raiz_output            pasta de topo em output/ (ex.: "playbooks")
  sufixo_slug            marcador do slug derivado (ex.: "--pbk"); None = obra raiz
  derivado_de            tupla de tipos-mae aceitos; () = obra raiz (nasce da pesquisa)
  natureza               "geracao" | "expansao" | "compressao" | "extracao"
  custo_llm              "alto" | "medio" | "baixo" | "zero"  (guia de token economy)
  dimensoes_capa         (largura, altura) em px, ou None se nao tem capa propria
  template_typ           nome do arquivo em templates/, ou None (usa template.typ)
  template_html          template HTML quando motor_pdf="chromium" (senao None)
  motor_pdf              "typst" (Pandoc->Typst) | "chromium" (HTML+CSS->Playwright)
  compilador             script proprio de compilacao, ou None (usa compilar-para-pdf.py)
  validador              script de gate em scripts/, ou None
  extensoes_saida        artefatos finais esperados
  min_refs_padrao        minimo de referencias por capitulo/secao
  citacao                "numerica" | "autor-data" | None
  numerar_secoes         passa --number-sections ao Pandoc
  coletor_metadados      nome da funcao em metadados_livro.py (ou None)
  variaveis_pandoc       nome da funcao de variaveis em metadados_livro.py (ou None)
  exige_cta              exige cta_url/cta_texto em config_obra.json
  membro_colecao         entra no manifesto da colecao
  perguntavel_na_fase0   /esbocar pode oferecer como obra raiz

Uso como biblioteca:
    from tipos_obra import TIPOS, descritor, tipos_validos, raiz_output, slug_completo

Uso como CLI:
    python scripts/tipos_obra.py --listar
    python scripts/tipos_obra.py playbook --json
    python scripts/tipos_obra.py --matriz        # matriz de derivacao
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"


def console_utf8():
    """Impede que um caractere fora do cp1252 derrube um script no console Windows.

    Os relatorios da V5 usam ①..⑦ (partes do card) e travessoes. Escrever isso no
    console padrao do Windows levanta UnicodeEncodeError e mata o processo no meio
    de um gate — o relatorio JSON ja foi gravado, mas o exit code se perde."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):   # fluxo redirecionado/nao reconfiguravel
            pass


TIPOS = {
    # ── OBRAS RAIZ (nascem da pesquisa; custo alto) ────────────────────────────
    "livro": {
        "rotulo": "Livro",
        "prefixo_curto": "liv",
        "nomes_curtos": False,   # V4: artefatos ja compilados no disco
        "raiz_output": "livros",
        "sufixo_slug": None,
        "derivado_de": (),
        "natureza": "geracao",
        "custo_llm": "alto",
        "dimensoes_capa": (1600, 2263),
        "template_typ": "template.typ",
        "validador": None,
        "extensoes_saida": (".pdf", ".epub"),
        "min_refs_padrao": 3,
        "citacao": "numerica",
        "numerar_secoes": True,
        "coletor_metadados": "coletar",
        "variaveis_pandoc": "variaveis_pandoc",
        "exige_cta": False,
        "membro_colecao": True,
        "perguntavel_na_fase0": True,
        # F1/F2 — gates de MERITO de conteudo (alem da estrutura R1-R15).
        # auditar-obra.py --estrito os encadeia ao final; o revisor-tecnico os
        # roda individualmente (referencias com rede, codigo com --executar).
        "gates_conteudo": (
            "validar-referencias.py",   # R-RF: fontes reais (4xx/DNS reprova)
            "validar-metricas.py",      # R-MT: metrica com valor+unidade+citacao
            "validar-escala.py",        # R-ES: limites/contorno na secao Aplica
            "validar-afirmacoes.py",    # R-AF: dado factual sem [N] no paragrafo
            "validar-fontes.py",        # R-FT: hierarquia A/B/C do dossier >= 70%
            "validar-comandos-cli.py",  # R-CLI: comandos/flags em livros tecnicos (condicional)
        ),
        # Categoria tecnica: ativa gate de comandos/CLI (livros sobre ferramentas/CLIs/frameworks)
        "categoria_tecnica_default": False,
        # Transmutacao (reescrita entre tipos) — origens aceitas para nascer
        # como livro a partir de um material existente (expansao com custo).
        # `validar_reescrita()` confere; `transmutar-obra.py` recorta e registra.
        "reescrever_de": ("ebook", "playbook", "artigo", "tcc"),
    },
    "tcc": {
        "rotulo": "TCC",
        "prefixo_curto": "tcc",
        "nomes_curtos": False,   # V4: artefatos ja compilados no disco
        "raiz_output": "tccs",
        "sufixo_slug": None,
        "derivado_de": (),
        "natureza": "geracao",
        "custo_llm": "alto",
        "dimensoes_capa": (1600, 2263),
        "template_typ": "template_tcc.typ",
        "validador": "validar-abnt-tcc.py",
        "extensoes_saida": (".pdf",),
        "min_refs_padrao": 8,
        "citacao": "autor-data",
        "numerar_secoes": False,
        "coletor_metadados": "coletar_tcc",
        "variaveis_pandoc": "variaveis_pandoc_tcc",
        "exige_cta": False,
        "membro_colecao": True,
        "perguntavel_na_fase0": True,
        # Transmutacao: TCC nasce por reframing academico de livro/ebook.
        "reescrever_de": ("livro", "ebook"),
    },

    # ── DERIVADOS POR COMPRESSAO (custo baixo) ────────────────────────────────
    "artigo": {
        "rotulo": "Artigo Científico",
        "prefixo_curto": "art",
        "nomes_curtos": False,   # V4: artefatos ja compilados no disco
        "raiz_output": "artigos",
        "sufixo_slug": "--art",
        "derivado_de": ("livro", "tcc"),
        "natureza": "compressao",
        "custo_llm": "baixo",
        "dimensoes_capa": None,
        "template_typ": "template_artigo.typ",
        "validador": None,
        "extensoes_saida": (".pdf",),
        "min_refs_padrao": 5,
        "citacao": "autor-data",
        "numerar_secoes": False,
        "coletor_metadados": "coletar_artigo",
        "variaveis_pandoc": "variaveis_pandoc_artigo",
        "exige_cta": False,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
        "reescrever_de": ("livro", "tcc", "ebook"),
    },
    "ebook": {
        "rotulo": "E-book",
        "prefixo_curto": "ebk",
        "nomes_curtos": False,   # V4: artefatos ja compilados no disco
        "raiz_output": "ebooks",
        "sufixo_slug": "--eb",
        "derivado_de": ("livro",),
        "natureza": "compressao",
        "custo_llm": "baixo",
        "dimensoes_capa": (1200, 1600),
        "template_typ": "template.typ",
        "validador": None,
        "extensoes_saida": (".epub", ".pdf"),
        "min_refs_padrao": 0,
        "citacao": "numerica",
        "numerar_secoes": False,
        "coletor_metadados": "coletar",
        "variaveis_pandoc": "variaveis_pandoc",
        "exige_cta": False,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
        # Transmutacao: reescrita de tom a partir de livro, TCC ou playbook.
        "reescrever_de": ("livro", "tcc", "playbook"),
    },

    # ── DERIVADOS POR EXTRACAO DETERMINISTICA (custo ~zero) ────────────────────
    "playbook": {
        "rotulo": "Playbook",
        "prefixo_curto": "pbk",
        "nomes_curtos": True,
        "raiz_output": "playbooks",
        "sufixo_slug": "--pbk",
        "derivado_de": ("livro",),
        "natureza": "extracao",
        "custo_llm": "zero",
        "dimensoes_capa": (1600, 2263),
        "template_typ": "template_playbook.typ",
        "validador": "validar-playbook.py",
        "extensoes_saida": (".pdf",),
        "min_refs_padrao": 0,
        "citacao": None,
        "numerar_secoes": False,
        "coletor_metadados": "coletar_playbook",
        "variaveis_pandoc": "variaveis_pandoc_playbook",
        "exige_cta": False,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
    },
    "lead-magnet": {
        "rotulo": "Lead Magnet",
        "prefixo_curto": "lm",
        "nomes_curtos": True,
        "raiz_output": "lead-magnets",
        "sufixo_slug": "--lm",
        "derivado_de": ("playbook", "livro"),
        "natureza": "extracao",
        "custo_llm": "zero",
        "dimensoes_capa": (2480, 3508),      # A4 @ 300dpi
        "dimensoes_social": (1080, 1350),    # card de anuncio/feed
        "template_typ": "template_lead_magnet.typ",   # fallback
        # Peca de marketing pede controle fino de layout (gradiente, sobreposicao,
        # tipografia de campanha) — CSS entrega isso melhor que Typst. O HTML e
        # camada INTERMEDIARIA: o entregavel continua sendo o PDF.
        "template_html": "template_lead_magnet.html",
        "motor_pdf": "chromium",
        "compilador": "gerar-lead-magnet-pdf.py",
        "validador": "validar-lead-magnet.py",
        "extensoes_saida": (".pdf", ".png"),
        "min_refs_padrao": 0,
        "citacao": None,
        "numerar_secoes": False,
        "coletor_metadados": "coletar_lead_magnet",
        "variaveis_pandoc": "variaveis_pandoc_lead_magnet",
        "exige_cta": True,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
    },
    "deck": {
        "rotulo": "Slide Deck",
        "prefixo_curto": "dck",
        "nomes_curtos": True,
        "raiz_output": "decks",
        "sufixo_slug": "--deck",
        "derivado_de": ("livro", "tcc"),
        "natureza": "extracao",
        "custo_llm": "zero",
        "dimensoes_capa": (1920, 1080),
        "template_typ": "template_deck.typ",   # fallback historico
        # V5.1: o design vem de CSS, nao de Typst nem de reference doc do Office.
        # Aqui — ao contrario do lead magnet — o .html E ENTREGAVEL: apresenta no
        # navegador, offline. O PDF 16:9 sai do MESMO HTML, entao apresentacao e
        # distribuicao ficam identicas.
        "template_html": "template_deck.html",
        "motor_pdf": "chromium",
        "compilador": "gerar-deck-html.py",
        # PPTX continua disponivel via scripts/gerar-pptx.py para quem precisa
        # editar no PowerPoint, mas NAO entra no pacote: o writer do Pandoc
        # entrega estrutura, nao design.
        "reference_pptx": "reference_deck.pptx",
        "gerador_pptx": "gerar-pptx.py",
        "validador": "validar-deck.py",
        "extensoes_saida": (".html", ".pdf"),
        "min_refs_padrao": 0,
        "citacao": None,
        "numerar_secoes": False,
        "coletor_metadados": "coletar_deck",
        "variaveis_pandoc": "variaveis_pandoc_deck",
        "exige_cta": True,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
    },
    "emails": {
        "rotulo": "Sequência de E-mails",
        "prefixo_curto": "eml",
        "nomes_curtos": True,
        "raiz_output": "emails",
        "sufixo_slug": "--eml",
        "derivado_de": ("playbook", "livro"),
        "natureza": "extracao",
        "custo_llm": "baixo",
        "dimensoes_capa": None,
        "template_typ": None,
        "validador": "validar-emails.py",
        "extensoes_saida": (".md",),
        "min_refs_padrao": 0,
        "citacao": None,
        "numerar_secoes": False,
        "coletor_metadados": None,
        "variaveis_pandoc": None,
        "exige_cta": True,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
    },
}


# ── Formatos de LEAD MAGNET ───────────────────────────────────────────────────
# Cada formato e uma QUERY DE AGREGACAO sobre os campos dos cards do playbook.
# `campo_card` None = nao vem dos cards (usa sumario_macro).
#
# `max_itens` NAO e cosmetico: sem teto, um livro XG gera "As 100 Armadilhas de X"
# — 16 paginas, acima do teto do formato e longe demais para ser acionavel. O
# corte e feito por rodizio entre capitulos (nao pelos primeiros N), para a
# cobertura continuar espalhada pela obra.
FORMATOS_LM = {
    "checklist": {
        "rotulo": "Checklist Mestre",
        "campo_card": "feito_quando",
        "titulo_padrao": "Checklist Mestre: {tema}",
        "promessa": "O checklist completo de {n} etapas para {tema}",
        "min_itens": 8,
        "max_itens": 60,
        "max_paginas": 8,
    },
    "armadilhas": {
        "rotulo": "Guia de Armadilhas",
        "campo_card": "armadilhas",
        "titulo_padrao": "As {n} Armadilhas de {tema}",
        "promessa": "Os {n} erros que travam quem está começando em {tema}",
        "min_itens": 6,
        "max_itens": 25,
        "max_paginas": 10,
    },
    "cheatsheet": {
        "rotulo": "Cheat Sheet de Comandos",
        "campo_card": "execucao",
        "titulo_padrao": "Cheat Sheet: {tema}",
        "promessa": "Todos os comandos de {tema} em uma folha de bancada",
        "min_itens": 6,
        "max_itens": 50,
        "max_paginas": 6,
    },
    "mapa": {
        "rotulo": "Mapa de Estágios",
        "campo_card": None,
        "titulo_padrao": "O Mapa de {tema}",
        "promessa": "A rota completa de {tema} em uma única folha",
        "min_itens": 3,
        "max_itens": 40,
        "max_paginas": 4,
    },
    "entregas": {
        "rotulo": "Mapa de Entregas",
        "campo_card": "entregas",
        "titulo_padrao": "Mapa de Entregas: {tema}",
        "promessa": "Todos os artefatos que você produz em {tema}",
        "min_itens": 6,
        "max_itens": 40,
        "max_paginas": 6,
    },
    "mini-guia": {
        "rotulo": "Mini-guia",
        "campo_card": None,
        "titulo_padrao": "Mini-guia: {tema}",
        "promessa": "O primeiro passo de {tema}, do início ao fim",
        "min_itens": 1,
        "max_itens": 1,
        "max_paginas": 12,
    },
}

FORMATO_LM_PADRAO = "checklist"


# ── API ───────────────────────────────────────────────────────────────────────

def tipos_validos():
    return tuple(TIPOS.keys())


def descritor(tipo):
    """Descritor do tipo; KeyError explicito se desconhecido."""
    d = TIPOS.get(tipo)
    if d is None:
        raise KeyError(
            f"tipo_obra desconhecido: {tipo!r}. Validos: {', '.join(tipos_validos())}"
        )
    return d


def campo(tipo, nome, padrao=None):
    """Leitura tolerante de um campo do descritor (nao levanta se tipo ausente)."""
    return TIPOS.get(tipo, {}).get(nome, padrao)


def raiz_output(tipo):
    return descritor(tipo)["raiz_output"]


def tipos_raiz():
    """Tipos que nascem da pesquisa (nao derivam de ninguem)."""
    return tuple(t for t, d in TIPOS.items() if not d["derivado_de"])


def tipos_derivados():
    return tuple(t for t, d in TIPOS.items() if d["derivado_de"])


def derivaveis_de(tipo_mae):
    """Tipos que podem ser gerados a partir de `tipo_mae`."""
    return tuple(t for t, d in TIPOS.items() if tipo_mae in d["derivado_de"])


def reescreviveis_de(tipo_origem):
    """Tipos-destino aceitos na TRANSMUTACAO (reescrita entre tipos).

    Diferente de `derivaveis_de` (cascata raiz->derivado), aqui o material
    ORIGEM ja existe e vira um material de outro tipo por reescrita."""
    return tuple(t for t, d in TIPOS.items()
                 if tipo_origem in d.get("reescrever_de", ()))


def validar_reescrita(tipo_destino, tipo_origem):
    """Erros (vazia = transmutacao permitida). Usa `reescrever_de`."""
    d = descritor(tipo_destino)
    permitidos = d.get("reescrever_de", ())
    if not permitidos:
        return [f"{tipo_destino} nao aceita reescrita/transmutacao"]
    if tipo_origem not in permitidos:
        return [f"{tipo_destino} reescreve-se a partir de "
                f"{' ou '.join(permitidos)}, nao de {tipo_origem}"]
    return []


def validar_derivacao(tipo_filho, tipo_mae):
    """Retorna lista de erros (vazia = derivacao permitida)."""
    d = descritor(tipo_filho)
    if not d["derivado_de"]:
        return [f"{tipo_filho} e obra raiz — nao deriva de {tipo_mae}"]
    if tipo_mae not in d["derivado_de"]:
        return [f"{tipo_filho} deriva de {' ou '.join(d['derivado_de'])}, "
                f"nao de {tipo_mae}"]
    return []


def slug_completo(tipo, slug_simples):
    """'playbook', 'meu-livro--pbk' -> 'playbooks/meu-livro--pbk'."""
    return f"{raiz_output(tipo)}/{slug_simples}"


def slug_derivado(tipo, slug_mae_simples, indice=None, sufixo_titulo=None):
    """Monta o slug simples de um derivado seguindo a convencao <mae>--<sfx>[-NN][-titulo]."""
    sufixo = descritor(tipo)["sufixo_slug"]
    if sufixo is None:
        return slug_mae_simples
    partes = [f"{slug_mae_simples}{sufixo}"]
    if indice is not None:
        partes.append(f"{indice:02d}")
    if sufixo_titulo:
        partes.append(sufixo_titulo)
    return "-".join(partes)


def usa_nomes_curtos(tipo):
    return bool(campo(tipo, "nomes_curtos"))


def prefixo_curto(tipo):
    return campo(tipo, "prefixo_curto", tipo[:3])


def slug_curto(tipo, slug_mae_simples, sequencia=1, nome=None, base=None):
    """Slug V5.1 relativo a output/: '<raiz>/<codigo-obra>/<pfx>-<seq>-<nome>'.

    Substitui o slug longo da V5, que repetia o nome da obra-mae na pasta e no
    arquivo e produzia caminhos de ~197 chars (MAX_PATH do Windows e 260).

    Quando a obra-mae vive no layout POR OBRA (output/<obra>/...), o derivado
    nasce nessa obra: '<obra>/<raiz>/<pfx>-<seq>-<nome>' (sem o nivel <codigo>,
    que a reorg por obra nao repete).
    `base` e o output-raiz (por padrao tipos_obra.DIR_OUTPUT)."""
    from nomes_curtos import caminho_material, codigo_obra, nome_material
    material = nome_material(prefixo_curto(tipo), sequencia, nome or tipo)
    obra = _obra_raiz(slug_mae_simples, base)
    if obra is not None:
        return f"{obra.name}/{raiz_output(tipo)}/{material}"
    return caminho_material(raiz_output(tipo), codigo_obra(slug_mae_simples), material)


def listar_materiais(tipo, base=None):
    """Slugs de todos os materiais de um tipo no disco, relativos a output/.

    Fonte unica da varredura: os tipos V5.1 vivem em <raiz>/<codigo>/<material>
    (2 niveis) e os V4 em <raiz>/<slug> (1 nivel). Quem varrer com `iterdir()`
    direto encontra as pastas de CODIGO no lugar dos materiais.

    A partir da reorg por obra, os materiais tambem vivem em
    output/<obra>/<raiz>/<material> (1 nivel sob <raiz>, sem o <codigo>). A
    varredura cobre os dois layouts e devolve slugs que `dir_obra` resolve.
    `base` e o output-raiz (por padrao tipos_obra.DIR_OUTPUT); os scripts passam
    o proprio DIR_OUTPUT para honrar redirecionamento nos testes."""
    base = Path(base) if base is not None else DIR_OUTPUT
    raiz_nome = raiz_output(tipo)
    padrao = "*/*" if usa_nomes_curtos(tipo) else "*"
    alvos = []
    # layout plano: output/<raiz>/...
    dir_flat = base / raiz_nome
    if dir_flat.exists():
        for d in dir_flat.glob(padrao):
            if d.is_dir() and (d / "config_obra.json").exists():
                alvos.append(str(d.relative_to(base)).replace("\\", "/"))
    # layout por obra: output/<obra>/<raiz>/... (material a 1 nivel sob <raiz>)
    for obra in _sereis(base):
        dir_serie = obra / raiz_nome
        if not dir_serie.exists():
            continue
        for d in dir_serie.glob("*"):
            if d.is_dir() and (d / "config_obra.json").exists():
                alvos.append(str(d.relative_to(base)).replace("\\", "/"))
        # obra RAIZ single-book: config direto em <obra>/<raiz>/ -> slug <raiz>/<obra>
        if tipo in tipos_raiz() and (dir_serie / "config_obra.json").exists():
            alvos.append(f"{raiz_nome}/{obra.name}")
    return sorted(set(alvos))


def nome_arquivo(slug_curto_do_material):
    """Nome-base do artefato: o ultimo segmento do slug ('lm-1-armadilhas')."""
    return Path(slug_curto_do_material).name


def tipo_por_prefixo(slug):
    """'playbooks/foo--pbk' -> 'playbook'. None se o prefixo nao for de nenhum tipo."""
    prefixo = Path(slug).parts[0] if "/" in slug or "\\" in slug else None
    if prefixo is None:
        return None
    for tipo, d in TIPOS.items():
        if d["raiz_output"] == prefixo:
            return tipo
    return None


def _sereis(base=None):
    """Diretorios-raiz de OBRA em output/ (cada um e um nucleo/projeto).

    Exclui arquivos e dirs estruturais de topo que nao sao obra (distribuicao).
    `base` permite resolver contra um output-raiz alternativo (usado nos testes,
    que monkeypatcham o DIR_OUTPUT do script chamador).
    """
    base = Path(base) if base is not None else DIR_OUTPUT
    if not base.exists():
        return []
    try:
        return [p for p in sorted(base.iterdir())
                if p.is_dir() and p.name not in _TOPO_NAO_OBRA]
    except OSError:
        return []


_TOPO_NAO_OBRA = {"distribuicao"}


def _raizes_tipo():
    """Conjunto de raizes_output dos tipos que sao OBRA RAIZ (livros, tccs)."""
    return {raiz_output(t) for t in tipos_raiz()}


def _obra_raiz(slug_mae_simples, base=None):
    """Dir-raiz da obra (output/<obra>) para um livro/tcc-mae; None se layout plano.

    - single-book por obra: output/<obra>/<raiz>  (obra == nome do mae)
    - multi-book por obra:  output/<obra>/<raiz>/<mae>
    """
    base = Path(base) if base is not None else DIR_OUTPUT
    mae = str(slug_mae_simples).replace("\\", "/").split("/")[-1]
    for raiz in _raizes_tipo():
        if (base / mae / raiz).exists():            # single-book
            return base / mae
        for obra in _sereis(base):                  # multi-book
            if (obra / raiz / mae).exists():
                return obra
    return None


def dir_obra(slug, base=None):
    """Resolve um slug (obra raiz ou derivado) para o diretorio real em output/.

    Layouts suportados:
      - plano:        output/<tipo>/<slug>
      - por obra:     output/<obra>/<tipo>/<slug>        (derivado)
      - raiz single:  output/<obra>/<tipo>               (obra == nome do slug)
    Quando nada existe, devolve o caminho plano (fallback de escrita).
    `base` permite resolver contra um output-raiz alternativo (testes).

    V5.1: procura em todos os hubs de colecao e subpastas de tipo.
    Prioriza pastas de tipo (ebooks, artigos) sobre campanhas.
    """
    base = Path(base) if base is not None else DIR_OUTPUT
    slug = str(slug).replace("\\", "/")
    direto = base / slug
    if direto.exists():
        return direto
    tipo, sep, resto = slug.partition("/")
    if not sep or not resto:
        # Procurar em todos os hubs de colecao (para slugs sem /)
        # Priorizar pastas de tipo (ebooks, artigos) sobre campanhas
        TIPOS_PRIORIDADE = ["ebooks", "artigos", "playbooks", "lead-magnets", "decks", "emails"]
        for hub in base.iterdir():
            if hub.is_dir() and hub.name not in _raizes_tipo():
                # Primeiro: procurar em pastas de tipo (prioridade)
                for tipo_dir in TIPOS_PRIORIDADE:
                    subdir = hub / tipo_dir
                    if subdir.exists():
                        # Procurar na raiz do tipo
                        cand = subdir / slug
                        if cand.exists():
                            return cand
                        # Procurar em subpastas do tipo
                        for subsubdir in subdir.iterdir():
                            if subsubdir.is_dir() and subsubdir.name == slug:
                                return subsubdir
                # Segundo: procurar em outras pastas (campanhas, etc.)
                for subdir in hub.iterdir():
                    if subdir.is_dir() and subdir.name not in TIPOS_PRIORIDADE:
                        cand = subdir / slug
                        if cand.exists():
                            return cand
        return direto
    for obra in _sereis(base):                       # multi-book raiz
        cand = obra / tipo / resto
        if cand.exists():
            return cand
    if tipo in _raizes_tipo():                       # single-book raiz
        cand = base / resto / tipo
        if cand.exists():
            return cand
    return direto


def template_de(tipo):
    """Caminho do template Typst; cai no template.typ do livro se o proprio nao existir."""
    nome = campo(tipo, "template_typ")
    if not nome:
        return None
    caminho = DIR_PROJETO / "templates" / nome
    if caminho.exists():
        return caminho
    return DIR_PROJETO / "templates" / "template.typ"


def validador_de(tipo):
    nome = campo(tipo, "validador")
    return (DIR_PROJETO / "scripts" / nome) if nome else None


def motor_pdf(tipo):
    """'typst' (Pandoc->Typst, padrao) ou 'chromium' (HTML+CSS->Playwright)."""
    return campo(tipo, "motor_pdf", "typst")


def compilador_de(tipo):
    """Script proprio de compilacao do tipo, ou None (usa compilar-para-pdf.py)."""
    nome = campo(tipo, "compilador")
    return (DIR_PROJETO / "scripts" / nome) if nome else None


def template_html_de(tipo):
    nome = campo(tipo, "template_html")
    return (DIR_PROJETO / "templates" / nome) if nome else None


def referencia_pptx(tipo):
    """Reference doc do writer pptx do Pandoc (portador da identidade visual)."""
    nome = campo(tipo, "reference_pptx")
    return (DIR_PROJETO / "templates" / nome) if nome else None


def dimensoes_capa(tipo, variante=None):
    """variante=None -> capa padrao; variante='social' -> card 1080x1350."""
    chave = "dimensoes_social" if variante == "social" else "dimensoes_capa"
    return campo(tipo, chave)


def usa_citacao_autor_data(tipo):
    return campo(tipo, "citacao") == "autor-data"


def exige_referencias(tipo):
    return bool(campo(tipo, "min_refs_padrao", 0))


def defaults_config(tipo, slug_mae_simples=None, extra=None):
    """config_obra.json minimo e coerente para um tipo (usado por fatiar-obra.py)."""
    d = descritor(tipo)
    cfg = {
        "tipo_obra": tipo,
        "min_referencias_por_capitulo": d["min_refs_padrao"],
        "tamanho_obra": None,
        "gerar_artigos": False, "qtd_artigos": 0,
        "gerar_ebooks": False, "qtd_ebooks": 0,
        "gerar_playbook": False,
        "gerar_lead_magnets": False, "formatos_lm": [],
        "gerar_deck": False,
        "gerar_emails": False,
    }
    if slug_mae_simples:
        cfg["livro_mae"] = slug_mae_simples      # chave historica (series_capa.py)
        cfg["obra_mae"] = slug_mae_simples
    if extra:
        cfg.update(extra)
    return cfg


def matriz_derivacao():
    """Lista [(mae, filho, natureza, custo)] para relatorio/documentacao."""
    linhas = []
    for filho, d in TIPOS.items():
        for mae in d["derivado_de"] or ("(raiz)",):   # ASCII: console Windows
            linhas.append((mae, filho, d["natureza"], d["custo_llm"]))
    return linhas


def matriz_reescrita():
    """Lista [(origem, destino, natureza, custo)] da TRANSMUTACAO (V5.2).

    Leitura inversa de `derivado_de`: cada par `reescrever_de` vira uma linha
    origem -> destino. Natureza/custo sao do DESTINO (quanto custa produzir)."""
    linhas = []
    for destino, d in TIPOS.items():
        for origem in d.get("reescrever_de", ()) or ():
            linhas.append((origem, destino, d["natureza"], d["custo_llm"]))
    return linhas


# ── Versionamento (R17 — CAMPANHA/MAQUINA sao opcionais e versionaveis) ────

def proxima_versao_arquivada(dir_versoes, prefixo):
    """1 + maior N ja em `dir_versoes/<prefixo>-vN` (1 se nao houver nenhuma)."""
    maior = 0
    padrao = re.compile(rf"^{re.escape(prefixo)}-v(\d+)$")
    dir_versoes = Path(dir_versoes)
    if dir_versoes.exists():
        for p in dir_versoes.iterdir():
            m = padrao.match(p.name)
            if m:
                maior = max(maior, int(m.group(1)))
    return maior + 1


def arquivar_para_versoes(origem, dir_versoes, prefixo):
    """Move a pasta `origem` para `dir_versoes/<prefixo>-v{N}/` (N seguinte).

    Usado pelo `--versionar` de criar-campanha.py/criar-maquina-vendas.py: a
    pasta canonica (campanhas/, maquina/) sai do caminho antes da nova
    criacao, sem que nenhum outro script precise saber sobre versionamento.
    Devolve o caminho da versao arquivada, ou None se `origem` nao existe."""
    origem = Path(origem)
    if not origem.exists():
        return None
    dir_versoes = Path(dir_versoes)
    n = proxima_versao_arquivada(dir_versoes, prefixo)
    dir_versoes.mkdir(parents=True, exist_ok=True)
    destino = dir_versoes / f"{prefixo}-v{n}"
    shutil.move(str(origem), str(destino))
    return destino


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Registro declarativo de tipos de obra (V5)")
    ap.add_argument("tipo", nargs="?", help="tipo a inspecionar (ex.: playbook)")
    ap.add_argument("--listar", action="store_true", help="lista todos os tipos")
    ap.add_argument("--matriz", action="store_true", help="matriz de derivacao mae -> filho")
    ap.add_argument("--formatos-lm", action="store_true", help="lista formatos de lead magnet")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.matriz:
        if args.json:
            print(json.dumps({
                "cascata": matriz_derivacao(),
                "transmutacao": matriz_reescrita(),
            }, ensure_ascii=False, indent=2))
            return 0
        print("CASCATA (raiz -> derivado, por extracao/compressao):")
        print(f"{'MAE':<12} {'FILHO':<14} {'NATUREZA':<12} CUSTO LLM")
        print("-" * 52)
        for mae, filho, natureza, custo in matriz_derivacao():
            print(f"{mae:<12} {filho:<14} {natureza:<12} {custo}")
        print()
        print("TRANSMUTACAO (reescrita entre tipos, V5.2):")
        print(f"{'ORIGEM':<12} {'DESTINO':<14} {'NATUREZA':<12} CUSTO LLM")
        print("-" * 52)
        for origem, destino, natureza, custo in matriz_reescrita():
            print(f"{origem:<12} {destino:<14} {natureza:<12} {custo}")
        return 0

    if args.formatos_lm:
        if args.json:
            print(json.dumps(FORMATOS_LM, ensure_ascii=False, indent=2))
            return 0
        for chave, f in FORMATOS_LM.items():
            fonte = f["campo_card"] or "sumario_macro"
            print(f"{chave:<12} {f['rotulo']:<26} fonte: {fonte}")
        return 0

    if args.listar or not args.tipo:
        if args.json:
            print(json.dumps(TIPOS, ensure_ascii=False, indent=2))
            return 0
        print(f"{'TIPO':<14} {'RAIZ':<14} {'DERIVA DE':<18} {'NATUREZA':<12} CUSTO")
        print("-" * 70)
        for tipo, d in TIPOS.items():
            deriva = ", ".join(d["derivado_de"]) or "(raiz)"
            print(f"{tipo:<14} {d['raiz_output']:<14} {deriva:<18} "
                  f"{d['natureza']:<12} {d['custo_llm']}")
        return 0

    try:
        d = descritor(args.tipo)
    except KeyError as exc:
        print(f"[ERRO] {exc}")
        return 1

    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    for k, v in d.items():
        print(f"{k:<22}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
