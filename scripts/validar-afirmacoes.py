#!/usr/bin/env python3
"""
F2 — Gate de AFIRMAÇÕES FUNDAMENTADAS (R-AF-1).

Nenhum parágrafo do corpo (seções 1-6, fora de código/tabela/citação) pode
carregar dado factual — percentual, unidade de medida, valor monetário ou
superlativo — sem citação [N] no MESMO parágrafo. Impede o modo de falha de
afirmações soltas ("reduz 30% dos custos") sem âncora na literatura.

R-AF-1: parágrafo com disparador factual (número+unidade, %, superlativo,
        garantia) precisa de citação [N] no mesmo parágrafo.

Disparadores considerados:
  - percentuais (30%, 2,5%)
  - valores com unidade (200 ms, 10 GB, 50 req/s, R$ 0,002, 1 milhão)
  - superlativos de liderança (o maior, líder de mercado, record, primeiro)
  - garantias absolutas (sempre, nunca, impossível, garantido)

Uso:
    python scripts/validar-afirmacoes.py <slug>
    python scripts/validar-afirmacoes.py <slug> --capitulo 7
    python scripts/validar-afirmacoes.py <slug> --md docs/x.md
    python scripts/validar-afirmacoes.py <slug> --estrito   # exit 1 se falha
    python scripts/validar-afirmacoes.py <slug> --json

Relatório: output/<slug>/validacao/relatorio_afirmacoes.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

from secoes_eita import dividir_secoes, sem_codigo

import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

RE_DADO = re.compile(
    r"\d+(?:[.,]\d+)?\s*%|"
    r"\d+(?:[.,]\d+)?\s*(?:ms|s\b|min|h\b|GB|MB|KB|TB|GHz|MHz|Hz|"
    r"rps|qps|req/s|tps|tokens?|milh[õo]es?|bilh[õo]es?|trilh[õo]es?)|"
    r"R\$\s?\d+(?:[.,]\d+)*|\$\s?\d+(?:[.,]\d+)*",
    re.IGNORECASE,
)
# Superlativos: regex com boundary para NAO casar "maioria" ("a maior" ∈ "a maioria")
# nem unicidade técnica ("único identificador") nem "primeiro arquivo".
# "primeir[oa] a <verbo-r>" preserva reivindicação de pioneirismo ("primeiro a lançar").
# Negative lookahead em "parte"/"parcela"/"fatia": "a maior parte" é o idiomatico
# "most of" (quantificador vago), não reivindicação de liderança/superlativo —
# mesma categoria de ajuste que excluiu "a maioria" (RTK 2026-08-11).
RE_SUPERLATIVO = re.compile(
    r"\b(?:o|a|os|as)\s+maior(?:es)?\b(?!\s+(?:parte|parcela|fatia)\b)|"
    r"l[íi]der(?:es)?\s+do?\s+mercado|\brecorde\b|\brecord\b|"
    r"imposs[íi]vel|primeir[oa]\s+a\s+[a-zà-ÿ]+r\b",
    re.IGNORECASE,
)
GARANTIAS = ("garantid", "obrigatoriamente", "100% dos", "100% das")
RE_CITACAO = re.compile(r"\[\d+(?:\s*,\s*\d+)*(?:\s*-\s*\d+)?\]")
# Aparato didático do template EITA-V2 (seção Aplica): cena narrativa, seus
# rótulos de comentário fixos (Métricas, Armadilhas comuns, Erros de
# julgamento, Antipadrão observável, Síntese operacional, Nota do revisor,
# "Três regras...") e exercícios ("Desafio") carregam números do PRÓPRIO
# livro — ilustrativos do exemplo construído, não uma afirmação empírica
# externa a citar. É o mesmo caso já aberto pelo "**Desafio" original,
# generalizado para os demais rótulos do template. (Ajuste calibrado
# 2026-08-11 — RTK: "superlativos de ênfase e garantias técnicas não são
# disparadores factuais (ruído)" — e 2026-09-12: rótulos fixos do Aplica.)
RE_CENA_AUTOR = re.compile(
    r"^(?:-\s*\[\s?\]|\*\*Situa[çc][ãa]o|"
    r"\*\*(?:A\s+|Primeira\s+|Segunda\s+|Terceira\s+)?[Cc]ena\b|"
    r"\*\*Desafio|Desafio opcional|"
    r"\*\*M[ée]tricas(?:\s+de\s+sucesso)?\b|\*\*Armadilhas comuns\b|"
    r"\*\*Erros de julgamento\b|\*\*Antipadr[ãa]o observ[áa]vel\b|"
    r"\*\*S[íi]ntese\b|\*\*Nota do revisor\b|Tr[êe]s regras\b|"
    r"-\s*\*\*[A-ZÁ-Ú]|"
    r"Voc[êe]\s+(?:é|está|investiga|percebe|decide|abre|trabalha|descobre)|Em termos práticos)",
    re.IGNORECASE,
)
RE_LISTA_INSTRUCAO = re.compile(r"^\d+\.\s+\*\*[A-ZÁ-Ú]+")

REGRAS = {
    "R-AF-1": "parágrafo com dado factual (%, unidade, superlativo) exige "
              "citação [N] no mesmo parágrafo",
}


def _paragrafos(texto):
    """Parágrafos fora de código; descarta headings, tabelas, citações diretas,
    o aparato didático do Aplica (Cena/Métricas/Armadilhas/.../Nota do revisor
    — números do próprio exemplo construído, não fato externo a citar) e sua
    continuação em prosa (parágrafo sem rótulo próprio que dá sequência a uma
    cena já aberta)."""
    limpo = sem_codigo(texto or "")
    saida = []
    em_cena = False
    for p in re.split(r"\n\s*\n", limpo):
        p = p.strip()
        if not p:
            continue
        primeira = p.splitlines()[0].strip()
        if primeira.startswith(("#", "|", ">")):
            continue
        if RE_CENA_AUTOR.match(primeira):
            em_cena = True
            continue
        if em_cena or RE_LISTA_INSTRUCAO.match(primeira):
            continue
        saida.append(p)
    return saida


def _tem_disparador(paragrafo):
    if RE_DADO.search(paragrafo):
        return True
    if RE_SUPERLATIVO.search(paragrafo):
        return True
    baixo = paragrafo.lower()
    return any(g in baixo for g in GARANTIAS)


def validar_capitulo(texto, rotulo):
    """R-AF-1 por parágrafo; seção 7 (referências) fica fora do escopo."""
    secoes = dividir_secoes(texto)
    violacoes = []
    for numero in range(1, 7):  # 1-6: corpo; 7 = referências, não exige citação
        secao = secoes.get(numero)
        if secao is None:
            continue
        for p in _paragrafos(secao["corpo"]):
            if not _tem_disparador(p):
                continue
            if RE_CITACAO.search(p):
                continue
            trecho = re.sub(r"\s+", " ", p)[:220]
            violacoes.append({
                "regra": "R-AF-1", "enunciado": REGRAS["R-AF-1"],
                "origem": rotulo, "secao": numero,
                "trecho": trecho})
    return violacoes


def main():
    ap = argparse.ArgumentParser(
        description="Gate F2 de afirmacoes fundamentadas: dado factual sem citacao")
    ap.add_argument("slug")
    ap.add_argument("--capitulo", help="valida apenas o capitulo N")
    ap.add_argument("--md", help="valida um markdown especifico em vez dos capitulos")
    ap.add_argument("--estrito", action="store_true", help="exit 1 se houver falha")
    ap.add_argument("--json", action="store_true", help="imprime relatorio JSON completo")
    args = ap.parse_args()

    dir_livro = TO.dir_obra(args.slug, DIR_OUTPUT)
    if not dir_livro.exists():
        print(f"[ERRO] Obra nao encontrada: {dir_livro}")
        return 1

    alvos = []
    if args.md:
        p = Path(args.md)
        if not p.exists():
            print(f"[ERRO] Arquivo nao encontrado: {p}")
            return 1
        alvos.append((p, p.name))
    else:
        caps = sorted((dir_livro / "capitulos").glob("cap_*.md"),
                      key=lambda p: int(re.search(r"cap_(\d+)", p.stem).group(1)))
        if args.capitulo:
            caps = [c for c in caps
                    if re.search(r"cap_(\d+)", c.stem).group(1).lstrip("0")
                    == str(args.capitulo).lstrip("0")]
        if not caps:
            print(f"[ERRO] Nenhum capitulo encontrado em {dir_livro / 'capitulos'}")
            return 1
        alvos = [(c, c.stem) for c in caps]

    todos = []
    for caminho, rotulo in alvos:
        texto = caminho.read_text(encoding="utf-8", errors="replace")
        todos.extend(validar_capitulo(texto, rotulo))

    por_capitulo = {}
    for v in todos:
        por_capitulo.setdefault(v["origem"], 0)
        por_capitulo[v["origem"]] += 1

    relatorio = {
        "slug": args.slug,
        "capitulos": len(alvos),
        "total_violacoes": len(todos),
        "por_capitulo": por_capitulo,
        "regras": REGRAS,
        "violacoes": todos,
    }
    dir_val = dir_livro / "validacao"
    dir_val.mkdir(exist_ok=True)
    (dir_val / "relatorio_afirmacoes.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Gate de Afirmacoes Fundamentadas - {args.slug}")
    print(f"  capitulos analisados : {len(alvos)}")
    print(f"  violacoes            : {len(todos)}")
    for rotulo, n in por_capitulo.items():
        print(f"    {rotulo:<12}: {n}")

    if todos:
        print("\n[FALHA] Violações (dado factual sem [N] no parágrafo):")
        for v in todos[:15]:
            print(f"  - {v['origem']} §{v['secao']}: {v['trecho']}...")
        if len(todos) > 15:
            print(f"  ... e mais {len(todos) - 15}")
    else:
        print("\n[OK] Nenhum dado factual sem citação no mesmo parágrafo")

    print(f"\nRelatorio: {(dir_val / 'relatorio_afirmacoes.json').relative_to(DIR_PROJETO)}")

    if args.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    if args.estrito and todos:
        return 1
    return 0


if __name__ == "__main__":
    console_utf8()
    sys.exit(main())
