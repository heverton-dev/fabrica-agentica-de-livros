#!/usr/bin/env python3
"""
Fase A (V4) — Parametros compartilhados por tipo de obra.

Modulo importado por auditar-obra.py, arquiteto (via scripts), validar-abnt-tcc.py,
fatiar-obra.py e gerar-epub.py. Centraliza:
  - leitura de output/<slug>/config_obra.json (schema da Fase 0 / `/esbocar`; <slug>
    inclui o prefixo de tipo, ex. livros/<slug-livro>, tccs/<slug-tcc>)
  - tabela de tamanhos de livro (P/M/G/GG/XG) -> capitulos e caracteres minimos
  - padroes de citacao por tipo de obra (numerica [N] vs autor-data)
  - valores-padrao para obras V3 sem esboco/ (retrocompatibilidade)

Uso como biblioteca:
    from parametros_obra import carregar_config, TAMANHOS, RE_CITACAO_NUMERICA, \
        RE_CITACAO_AUTOR_DATA, citacao_regex, minimos_livro

Uso como CLI (inspecao rapida):
    python scripts/parametros_obra.py <slug>
    python scripts/parametros_obra.py <slug> --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

import tipos_obra as TO

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

# V5: a lista de tipos deixou de ser literal aqui — vem do registro declarativo
# scripts/tipos_obra.py. Adicionar um tipo novo NAO exige tocar neste arquivo.
TIPOS_VALIDOS = TO.tipos_validos()
TIPOS_PERGUNTAVEIS = tuple(t for t in TIPOS_VALIDOS if TO.campo(t, "perguntavel_na_fase0"))
SENIORIDADES_VALIDAS = ("iniciante", "intermediario", "avancado", "tecnico")

# V5.6 — modo de composicao da secao 4 (Tecnica) do EITA:
#   codigo       -> bloco de codigo de programacao obrigatorio (padrao historico)
#   hibrido      -> codigo curto OU config/artefato tecnico (yaml/json/bash/sql)
#   operacional  -> artefato tecnico (config real, comando console, tabela de
#                   decisao, diagrama, passos numerados); codigo opcional.
# Ideal p/ publicos iniciantes e nao-programadores: a Tecnica deixa de exigir
# Python e passa a usar configs/operacoes reais do dominio (ex.: n8n, VPS,
# docker-compose) — ver templates/template_eita.md secao 4.
ESTILOS_TECNICA = ("codigo", "hibrido", "operacional")

# Tabela de tamanhos de LIVRO (Fase 0, pergunta Q5). Caracteres ~2.500/pagina ABNT.
TAMANHOS = {
    "P": {"partes": 1, "capitulos": 4, "paginas": 40, "caracteres": 100_000},
    "M": {"partes": 2, "capitulos": 8, "paginas": 80, "caracteres": 200_000},
    "G": {"partes": 3, "capitulos": 12, "paginas": 120, "caracteres": 300_000},
    "GG": {"partes": 4, "capitulos": 16, "paginas": 160, "caracteres": 400_000},
    "XG": {"partes": 5, "capitulos": 20, "paginas": 200, "caracteres": 500_000},
}
TAMANHO_PADRAO = "M"

# Tabela de tamanhos de MANUAL DIARIO (tipo_obra=manual-diario). A unidade de
# conteudo e o DIA, nao o capitulo. Um dia e tipicamente mais curto que um
# capitulo de livro (~1.800-2.200 chars), entao a soma para a mesma paginacao
# alvo fica maior que a do livro classico.
TAMANHOS_DIARIO = {
    "P": {"partes": 1, "dias": 5, "paginas": 40, "caracteres": 90_000},
    "M": {"partes": 2, "dias": 10, "paginas": 80, "caracteres": 180_000},
    "G": {"partes": 2, "dias": 14, "paginas": 110, "caracteres": 250_000},
    "GG": {"partes": 4, "dias": 16, "paginas": 160, "caracteres": 360_000},
    "XG": {"partes": 5, "dias": 20, "paginas": 200, "caracteres": 450_000},
}

# Retrocompatibilidade: obras V3 sem esboco/config_obra.json usam os minimos originais
MIN_CAPITULOS_V3 = 16
MIN_CARACTERES_V3 = 175_000
MIN_REFS_V3 = 3

# Derivado do registro (V5): {"livro": {"min_refs": 3}, ..., "playbook": {"min_refs": 0}}
DEFAULTS_POR_TIPO = {
    tipo: {"min_refs": TO.campo(tipo, "min_refs_padrao", MIN_REFS_V3)}
    for tipo in TIPOS_VALIDOS
}

# Campos de derivacao adicionados pela V5 (retrocompatibilidade por setdefault)
DERIVADOS_V5 = {
    "gerar_playbook": False,
    "gerar_lead_magnets": False,
    "formatos_lm": [],
    "gerar_deck": False,
    "gerar_emails": False,
    "gerar_campanha": False,
    "gerar_maquina": False,
    "cta_url": "",
    "cta_texto": "",
    "modo_producao": "obra-unica",   # obra-unica | cascata
    "obra_raiz": None,               # preenchido quando modo_producao=cascata
    # V5.7 (melhorias/21-08-2026-plano-acao-tokens-sob-pericia.md, item A):
    # opt-in do operador na entrevista para livros TECNICOS (ferramentas/CLIs/
    # frameworks/DevOps/IA) — ativa validar-comandos-cli.py (R-CLI-1) no
    # auditar-obra --estrito. Retrocompativel: obras sem o campo => False,
    # gate pulado sem falhar.
    "categoria_tecnica": False,
}

# Citacao numerica (livro/ebook): [1], [23]...
RE_CITACAO_NUMERICA = re.compile(r"\[\d{1,3}\]")

# Citacao autor-data (TCC/artigo, NBR 10520): parenteses "(SOBRENOME, 2024)" ou
# "(SOBRENOME; SOBRENOME2, 2024)" ou narrativa "Sobrenome (2024)".
RE_CITACAO_AUTOR_DATA = re.compile(
    r"\([A-ZÀ-Ý][A-ZÀ-Ýa-zà-ÿ\'\-]+(?:\s*;\s*[A-ZÀ-Ý][A-ZÀ-Ýa-zà-ÿ\'\-]+)*,\s*\d{4}[a-z]?\)"
    r"|[A-ZÀ-Ý][A-Za-zà-ÿ\'\-]+\s*\(\d{4}[a-z]?\)"
)

# Entrada de referencia ABNT autor-data: linha comecando com SOBRENOME e contendo um ano
# (suporta "SOBRENOME, Nome; SOBRENOME2, Nome2" e autores institucionais "ORG. Titulo")
RE_REF_AUTOR_DATA = re.compile(
    r"^((?:[A-ZÀ-Ý][A-ZÀ-Ýa-zà-ÿ\'\-]+(?:\s*,\s*[^;.,]+)?)"
    r"(?:\s*;\s*[A-ZÀ-Ý][A-ZÀ-Ýa-zà-ÿ\'\-]+(?:\s*,\s*[^;.,]+)?)*)"
    r"\.?\s*.*?(\d{4})", re.MULTILINE
)

# Numeracao progressiva de secao (NBR 6024): "1", "1.1", "2.3.4"...
RE_NUMERACAO_PROGRESSIVA = re.compile(r"^#{1,6}\s*(\d+(?:\.\d+)*)\.?\s+\S", re.MULTILINE)


def usa_citacao_autor_data(tipo_obra):
    """V5: o padrao de citacao vem do registro (campo `citacao` do descritor)."""
    return TO.usa_citacao_autor_data(tipo_obra)


def citacao_regex(tipo_obra):
    return RE_CITACAO_AUTOR_DATA if usa_citacao_autor_data(tipo_obra) else RE_CITACAO_NUMERICA


def minimos_livro(tamanho):
    """Minimos de LIVRO por tamanho (P/M/G/GG/XG). Mantido p/ retrocompat."""
    return TAMANHOS.get((tamanho or TAMANHO_PADRAO).upper(), TAMANHOS[TAMANHO_PADRAO])


def minimos_manual_diario(tamanho):
    """Minimos de MANUAL DIARIO por tamanho (P/M/G/GG/XG) — unidade = dias."""
    padrao = TAMANHOS_DIARIO[TAMANHO_PADRAO]
    return TAMANHOS_DIARIO.get((tamanho or TAMANHO_PADRAO).upper(), padrao)


def minimos_do_tipo(tipo, tamanho):
    """Minimos corretos para o `tipo`: livros usam TAMANHOS, manuais diarios usam
    TAMANHOS_DIARIO e qualquer tipo sem tabela propria cai no TAMANHOS do livro."""
    if tipo == "manual-diario":
        return minimos_manual_diario(tamanho)
    return minimos_livro(tamanho)


def caminho_config(slug):
    return TO.dir_obra(slug, DIR_OUTPUT) / "config_obra.json"


def carregar_config(slug):
    """Le config_obra.json; devolve defaults retrocompativeis se nao existir (obra V3)."""
    caminho = caminho_config(slug)
    if not caminho.exists():
        return {
            "tema": slug,
            "tipo_obra": "livro",
            "min_referencias_por_capitulo": MIN_REFS_V3,
            "tamanho_obra": None,
            "senioridade_obra": "iniciante",
            "gerar_artigos": False,
            "qtd_artigos": 0,
            "gerar_ebooks": False,
            "qtd_ebooks": 0,
            # copia dos mutaveis: dois carregamentos nao podem partilhar a lista
            **{k: (list(v) if isinstance(v, list) else v)
               for k, v in DERIVADOS_V5.items()},
            "_origem": "default_v3_sem_esboco",
        }
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados.setdefault("tipo_obra", "livro")
    dados.setdefault("min_referencias_por_capitulo",
                     DEFAULTS_POR_TIPO.get(dados["tipo_obra"], {}).get("min_refs", MIN_REFS_V3))
    dados.setdefault("tamanho_obra", TAMANHO_PADRAO if dados["tipo_obra"] == "livro" else None)
    dados.setdefault("senioridade_obra", "tecnico" if dados["tipo_obra"] in ("tcc", "artigo") else "intermediario")
    dados.setdefault("estilo_tecnica", "codigo")
    dados.setdefault("cor_primaria", "")
    dados.setdefault("subtitulo", "")
    dados.setdefault("edition_tag", "")
    dados.setdefault("gerar_artigos", False)
    dados.setdefault("qtd_artigos", 0)
    dados.setdefault("gerar_ebooks", False)
    dados.setdefault("qtd_ebooks", 0)
    for chave, padrao in DERIVADOS_V5.items():
        dados.setdefault(chave, list(padrao) if isinstance(padrao, list) else padrao)
    dados["_origem"] = "esboco"
    return dados


def gravar_config(slug, config):
    caminho = caminho_config(slug)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    limpo = {k: v for k, v in config.items() if not k.startswith("_")}
    caminho.write_text(json.dumps(limpo, ensure_ascii=False, indent=2), encoding="utf-8")
    return caminho


def validar_config(config):
    """Valida config_obra.json contra as faixas da Fase 0. Retorna lista de erros (vazia = ok).

    V5: as faixas que dependem do tipo saem do registro (tipos_obra.py). Configs de
    obras DERIVADAS (artigo, ebook, playbook, lead-magnet, deck, emails) sao gravadas
    por fatiar-obra/gerar-* e validadas pelas regras do proprio tipo, nao pelas da
    Fase 0 (que so pergunta livro|tcc)."""
    erros = []
    tipo = config.get("tipo_obra")

    if tipo not in TIPOS_VALIDOS:
        erros.append(f"tipo_obra invalido: {tipo!r}. Validos: {', '.join(TIPOS_VALIDOS)}")
        return erros

    derivado = bool(TO.campo(tipo, "derivado_de"))
    if not derivado and tipo not in TIPOS_PERGUNTAVEIS:
        erros.append(f"tipo_obra deve ser {' ou '.join(TIPOS_PERGUNTAVEIS)}, recebido: {tipo!r}")

    # Referencias so sao exigidas nos tipos que as usam (playbook/LM/deck usam 0).
    if TO.exige_referencias(tipo):
        refs = config.get("min_referencias_por_capitulo")
        if not isinstance(refs, int) or not (1 <= refs <= 20):
            erros.append(f"min_referencias_por_capitulo deve estar entre 1 e 20, recebido: {refs!r}")
        elif not derivado and refs < 5:
            erros.append(f"min_referencias_por_capitulo da Fase 0 deve estar entre 5 e 20, recebido: {refs!r}")

    sen = config.get("senioridade_obra")
    if sen not in SENIORIDADES_VALIDAS:
        erros.append(f"senioridade_obra deve ser 'iniciante', 'intermediario', 'avancado' ou 'tecnico', recebido: {sen!r}")

    estilo = config.get("estilo_tecnica")
    if estilo is not None and estilo not in ESTILOS_TECNICA:
        erros.append(f"estilo_tecnica deve ser 'codigo', 'hibrido' ou 'operacional', recebido: {estilo!r}")

    if tipo == "livro":
        tam = config.get("tamanho_obra")
        if tam not in TAMANHOS:
            erros.append(f"tamanho_obra deve ser P, M, G, GG ou XG quando tipo_obra=livro, recebido: {tam!r}")
        
        # Gap 3: campos obrigatorios de capa para livro
        for campo_obrig, nome in [("cor_primaria", "cor_primaria"), ("subtitulo", "subtitulo"), ("edition_tag", "edition_tag")]:
            val = config.get(campo_obrig)
            if not val or (isinstance(val, str) and not val.strip()):
                erros.append(f"{nome} eh obrigatorio para tipo_obra=livro (Gap 3: capa sem fallback errado)")

    if tipo == "manual-diario":
        tam = config.get("tamanho_obra")
        if tam not in TAMANHOS_DIARIO:
            erros.append(
                f"tamanho_obra deve ser P, M, G, GG ou XG quando tipo_obra=manual-diario, "
                f"recebido: {tam!r}"
            )
        for campo_obrig, nome in [("cor_primaria", "cor_primaria"), ("subtitulo", "subtitulo"), ("edition_tag", "edition_tag")]:
            val = config.get(campo_obrig)
            if not val or (isinstance(val, str) and not val.strip()):
                erros.append(f"{nome} eh obrigatorio para tipo_obra=manual-diario (Gap 3: capa sem fallback errado)")

    if config.get("gerar_artigos"):
        qtd = config.get("qtd_artigos")
        if not isinstance(qtd, int) or not (1 <= qtd <= 5):
            erros.append(f"qtd_artigos deve estar entre 1 e 5, recebido: {qtd!r}")
    if config.get("gerar_ebooks"):
        qtd = config.get("qtd_ebooks")
        if not isinstance(qtd, int) or not (1 <= qtd <= 10):
            erros.append(f"qtd_ebooks deve estar entre 1 e 10, recebido: {qtd!r}")

    # ── V5 ────────────────────────────────────────────────────────────────────
    if config.get("gerar_lead_magnets"):
        formatos = config.get("formatos_lm")
        if not isinstance(formatos, list) or not formatos:
            erros.append("formatos_lm deve ser lista nao vazia quando gerar_lead_magnets=true")
        else:
            invalidos = [f for f in formatos if f not in TO.FORMATOS_LM]
            if invalidos:
                erros.append(f"formatos_lm invalido(s): {invalidos}. "
                             f"Validos: {', '.join(sorted(TO.FORMATOS_LM))}")

    modo = config.get("modo_producao", "obra-unica")
    if modo not in ("obra-unica", "cascata"):
        erros.append(f"modo_producao deve ser 'obra-unica' ou 'cascata', recebido: {modo!r}")
    if modo == "cascata":
        raiz = config.get("obra_raiz")
        if raiz not in TIPOS_PERGUNTAVEIS:
            erros.append(f"obra_raiz deve ser {' ou '.join(TIPOS_PERGUNTAVEIS)} "
                         f"quando modo_producao=cascata, recebido: {raiz!r}")

    # CTA e obrigatorio nos tipos de conversao (lead magnet, deck, emails)
    if TO.campo(tipo, "exige_cta") and not (config.get("cta_url") or "").strip():
        erros.append(f"cta_url obrigatorio para tipo_obra={tipo} (R-LM-1 / R-DK-3 / R-EM-2)")

    return erros


def main():
    ap = argparse.ArgumentParser(description="Parametros de obra por tipo (Fase 0 / V4)")
    ap.add_argument("slug")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--validar", action="store_true", help="valida config_obra.json e retorna exit 1 se invalido")
    args = ap.parse_args()

    config = carregar_config(args.slug)

    if args.validar:
        erros = validar_config(config)
        if erros:
            for e in erros:
                print(f"[ERRO] {e}")
            return 1
        print("[OK] config_obra.json valido")
        return 0

    if args.json:
        print(json.dumps(config, ensure_ascii=False, indent=2))
        return 0

    for k, v in config.items():
        print(f"{k:<32}: {v}")
    if config["tipo_obra"] == "livro":
        m = minimos_livro(config.get("tamanho_obra"))
        print(f"\nMinimos derivados (tamanho {config.get('tamanho_obra')}): "
              f"{m['capitulos']} capitulos, {m['partes']} partes, "
              f"{m['caracteres']:,} caracteres".replace(",", "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
