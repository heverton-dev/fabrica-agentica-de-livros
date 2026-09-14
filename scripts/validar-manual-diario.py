#!/usr/bin/env python3
"""
V5.6 — Gate do MANUAL DIARIO (R-MDI-1 a R-MDI-8).

Um manual diario e uma obra do tipo `manual-diario`: mesma natureza do livro
(geracao EITA, custo LLM alto), mas a unidade de conteudo e o DIA, nao o
capitulo. Os dias vivem como dia-NN.md na raiz da obra, e o `sumario_macro.json`
usa a chave `dias` (rotulo `dia`) — ver `tipos_obra.chave_unidade`.

Cada dia segue o esqueleto fixo de manual (Meta do dia, A ideia em uma frase,
A explicação simples, O exemplo real, Mão na massa, Três regras que ficam,
Erros de julgamento deste dia, Checklist do dia, Para saber mais) — gatilho
contra dia rasgado ou sem o exemplo contínuo da obra.

Uso:
    python scripts/validar-manual-diario.py manuais-diarios/<slug>-iniciante
    python scripts/validar-manual-diario.py ... --estrito --json
"""

import json
import re
from pathlib import Path
import argparse
import sys

import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

MIN_REFS_DIA = 3
MIN_DIAGRAMAS_DIA = 1
MIN_CARACTERES_DIA = 1_800

# Seções obrigatórias de cada dia (padroes de cabecalho, aceitando variantes).
SECOES_DIA = [
    ("Meta do dia",                    r"^##\s+Meta do dia"),
    ("A ideia em uma frase",           r"^##\s+A ideia em uma frase"),
    ("A explicação simples",           r"^##\s+A explica[çc][ãa]o simples"),
    ("O exemplo real",                 r"^##\s+O exemplo real"),
    ("Mão na massa",                   r"^##\s+M[ãa]o na massa"),
    ("Três regras que ficam",          r"^##\s+Tr[eê]s regras"),
    ("Erros de julgamento deste dia",  r"^##\s+Erros (de julgamento|comuns)"),
    ("Checklist do dia",               r"^##\s+Checklist do dia"),
    ("Para saber mais",                r"^##\s+Para saber mais"),
]

RE_CITACAO = re.compile(r"\[\d+\]")
RE_DIAGRAMA = re.compile(r"```mermaid")
RE_SEPARADOR = re.compile(r"^-{3,}\s*$", re.MULTILINE)

REGRAS = {
    "R-MDI-1": "1 arquivo dia-NN.md por dia do sumario, sem lacuna, na ordem",
    "R-MDI-2": "todo dia tem as 9 seções fixas do manual (Meta do dia a Para saber mais)",
    "R-MDI-3": "todo dia tem secao 'O exemplo real' com o projeto-continuo da obra",
    "R-MDI-4": "todo dia referencia fontes ([N] numerica) e diagrama (```mermaid)",
    "R-MDI-5": f"todo dia tem ao menos {MIN_CARACTERES_DIA} caracteres (anti-dia-raso)",
    "R-MDI-6": "dia argumenta pontos concretos (sem placeholder/vazio na Meta e no Checklist)",
    "R-MDI-7": "manual nao contem horizontal rules (---) entre seções do dia",
    "R-MDI-8": "capa com badge de nivel + senioridade declarada no config_obra.json",
}

# \b evita falso-positivo em palavras PT-BR legitimas ("todo", "método", "protocolo").
RE_PLACEHOLDER = re.compile(r"(<\w+>|\bTBD\b|\blorem\b|\bexemplo_placeholder\b|\bTODO\b)", re.IGNORECASE)


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def _dias_declarados(sumario):
    """Lista de numeros de dia em ordem, da gramatica do sumario (chave dias)."""
    numeros = []
    for parte in sumario.get("partes", []):
        for dia in parte.get("dias", []):
            numeros.append(dia.get("dia"))
    return [str(n) for n in numeros if n is not None]


def validar(slug):
    dir_obra = TO.dir_obra(slug, DIR_OUTPUT)
    cfg = _ler_json(dir_obra / "config_obra.json")
    sumario = _ler_json(dir_obra / "sumario_macro.json")

    violacoes, avisos = [], []
    falha = lambda regra, detalhe: violacoes.append(
        {"regra": regra, "enunciado": REGRAS[regra], "detalhe": detalhe})

    arquivos = sorted(dir_obra.glob("dia-*.md"),
                      key=lambda p: int(re.search(r"dia-(\d+)", p.stem).group(1)))
    arquivos = [p for p in arquivos if not p.stem.startswith("_")]

    if not arquivos:
        falha("R-MDI-1", f"nenhum dia-*.md em {dir_obra}")
        return {"slug": slug, "conforme": False, "total_dias": 0, "violacoes": violacoes,
                "avisos": avisos, "regras": REGRAS}

    # R-MDI-1 — cobertura: dias declarados x arquivos
    numeros_declarados = _dias_declarados(sumario)
    numeros_arquivos = [re.search(r"dia-(\d+)", p.stem).group(1) for p in arquivos]
    if numeros_declarados and numeros_arquivos != [str(d) for d in numeros_declarados]:
        falha("R-MDI-1", f"arquivos {numeros_arquivos} != dias do sumario {numeros_declarados}")
    elif not numeros_declarados:
        avisos.append("sumario_macro.json sem chave 'dias' — cobertura nao verificada por sumario")

    total_dias = len(arquivos)
    for p in arquivos:
        numero = re.search(r"dia-(\d+)", p.stem).group(1)
        texto = p.read_text(encoding="utf-8", errors="replace")

        # R-MDI-2 — seções fixas
        faltantes = [nome for nome, regex in SECOES_DIA
                     if not re.search(regex, texto, re.MULTILINE)]
        if faltantes:
            falha("R-MDI-2", f"dia {numero} sem seções: {', '.join(faltantes)}")

        # R-MDI-3 — exemplo real (o projeto-continuo da obra) precisa ter conteudo
        trecho_exemplo = None
        m = re.search(r"^##\s+O exemplo real[^\n]*\n(.*?)(?=^##|\Z)", texto,
                      re.MULTILINE | re.DOTALL)
        if m and len(m.group(1).strip()) > 80:
            trecho_exemplo = m.group(1)
        if trecho_exemplo is None:
            falha("R-MDI-3", f"dia {numero}: secao 'O exemplo real' vazia ou rasteira")

        # R-MDI-4 — citacoes numericas + diagrama
        if len(RE_CITACAO.findall(texto)) < MIN_REFS_DIA:
            falha("R-MDI-4", f"dia {numero}: {len(RE_CITACAO.findall(texto))} citacao(oes) "
                  f"(minimo {MIN_REFS_DIA})")
        if len(RE_DIAGRAMA.findall(texto)) < MIN_DIAGRAMAS_DIA:
            falha("R-MDI-4", f"dia {numero}: sem bloco ```mermaid")

        # R-MDI-5 — extensao
        corpo_sem_codigo = re.sub(r"```.*?```", "", texto, flags=re.DOTALL)
        caracteres = len(re.sub(r"\s+", "", corpo_sem_codigo))
        if caracteres < MIN_CARACTERES_DIA:
            falha("R-MDI-5", f"dia {numero}: {caracteres} caracteres (minimo {MIN_CARACTERES_DIA})")

        # R-MDI-6 — placeholders
        if RE_PLACEHOLDER.search(texto):
            falha("R-MDI-6", f"dia {numero}: contem placeholder (TBD/TODO/<...>)")

        # R-MDI-7 — separadores entre seções violam o padrão de manual
        # (dias reais usam parágrafos, nao ---; a secao Tecnica usa codigo quando aplica)
        if re.search(RE_SEPARADOR, texto.split("---", 2)[-1]):
            falha("R-MDI-7", f"dia {numero}: horizontal rule (---) dentro do corpo")

    # R-MDI-8 — config minima de capa/badge
    if not (cfg.get("senioridade_obra") or "").strip():
        falha("R-MDI-8", "config_obra.json sem 'senioridade_obra' (badge de nivel)")
    return {"slug": slug, "conforme": not violacoes, "total_dias": total_dias,
            "violacoes": violacoes, "avisos": avisos, "regras": REGRAS}


def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Gate do manual diario (R-MDI-1 a R-MDI-8)")
    ap.add_argument("slug", help="ex.: manuais-diarios/<slug>")
    ap.add_argument("--estrito", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rel = validar(args.slug)
    dir_rev = TO.dir_obra(args.slug, DIR_OUTPUT) / "revisao"
    dir_rev.mkdir(parents=True, exist_ok=True)
    (dir_rev / "relatorio_gate.json").write_text(
        json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(rel, ensure_ascii=False, indent=2))
    else:
        estado = "CONFORME" if rel["conforme"] else "NAO CONFORME"
        print(f"[{estado}] {args.slug} — {rel.get('total_dias', 0)} dia(s)")
        for v in rel["violacoes"]:
            print(f"  [{v['regra']}] {v['detalhe']}")
        for a in rel["avisos"]:
            print(f"  [AVISO] {a}")

    if args.estrito and not rel["conforme"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())