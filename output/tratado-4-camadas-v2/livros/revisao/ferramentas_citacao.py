#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utilitário de bancada (não é script da esteira).

1. Monta o pool de referências REAIS da obra a partir do dossiê de pesquisa e
   dos capítulos já validados (backup), deduplicando entradas idênticas.
2. Aplica nos capítulos os marcadores `[ref:chave]` / `[ref:a, b]`, numerando
   as referências pela ordem de primeira aparição e gravando a seção
   `## 7. Referências Bibliográficas` com exatamente as obras citadas.

Isso elimina três modos de falha dos gates: citação órfã (R14), ordem não
ascendente (R15) e referência sem citação.

Uso:
    python revisao/ferramentas_citacao.py --listar
    python revisao/ferramentas_citacao.py --aplicar capitulos/cap_5.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
OBRA = AQUI.parent
POOL_PATH = AQUI / "pool-referencias.json"

STOPWORDS = {
    "de", "da", "do", "das", "dos", "e", "in", "the", "of", "a", "o", "os",
    "as", "for", "para", "com", "on", "em", "um", "uma", "to", "and",
}


def slug(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-zA-Z0-9]+", "-", texto).strip("-").lower()
    return texto


def _chave_de(entrada: str) -> str:
    """Chave legível: instituição/sobrenome + 2 primeiras palavras do título."""
    limpo = re.sub(r"\[(\d+)\]\s*", "", entrada).strip()
    autor = re.split(r"\.\s", limpo)[0]
    titulo = ""
    m = re.search(r"\*([^*]+)\*", limpo)
    if m:
        titulo = m.group(1)
    partes = [p for p in re.findall(r"[A-Za-zÀ-ÿ0-9]+", titulo) if p.lower() not in STOPWORDS]
    tokens = [slug(autor)[:28]] if autor else []
    tokens += [slug(p) for p in partes[:2]]
    chave = "-".join(t for t in tokens if t)[:60] or slug(limpo)[:60]
    return chave or "referencia"


def _mapa_por_classe(texto: str) -> dict[str, str]:
    """Associa cada fonte do dossiê à sua classe A/B/C (marcador `(X)` no fim)."""
    classes = {}
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha.startswith("- "):
            continue
        m = re.search(r"\(([ABC])\)\s*$", linha)
        if m:
            classes[re.sub(r"\(([ABC])\)\s*$", "", linha[2:]).strip()] = m.group(1)
    return classes


def coletar_fontes_dossie() -> list[str]:
    texto = (OBRA / "pesquisa" / f"dossie_{OBRA.name}.md")
    if not texto.exists():
        return []
    return [
        l.strip()[2:].strip()
        for l in texto.read_text(encoding="utf-8").splitlines()
        if l.strip().startswith("- ") and "Disponível em:" in l
    ]


def coletar_fontes_capitulos_antigos() -> list[str]:
    fontes = []
    for pasta in sorted((OBRA / "revisao" / "backups").glob("*-obra")):
        for cap in sorted(pasta.glob("cap_*.md")):
            texto = cap.read_text(encoding="utf-8")
            if "## 7." not in texto:
                continue
            secao = texto.split("## 7.", 1)[1]
            for linha in secao.splitlines():
                linha = linha.strip()
                if re.match(r"^\[\d+\]", linha):
                    fontes.append(re.sub(r"^\[\d+\]\s*", "", linha))
    return fontes


def _normalizar(entrada: str) -> str:
    t = unicodedata.normalize("NFKD", entrada)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()[:110]


def construir_pool() -> dict[str, str]:
    bruto = coletar_fontes_dossie() + coletar_fontes_capitulos_antigos()
    pool: dict[str, str] = {}
    vistos: dict[str, str] = {}
    for entrada in bruto:
        chave_norm = _normalizar(entrada)
        if chave_norm in vistos:
            continue
        chave = _chave_de(entrada)
        sufixo = 2
        while chave in pool:
            chave = f"{_chave_de(entrada)}-{sufixo}"
            sufixo += 1
        pool[chave] = entrada
        vistos[chave_norm] = chave
    return dict(sorted(pool.items()))


def carregar_pool() -> dict[str, str]:
    if not POOL_PATH.exists():
        pool = construir_pool()
        POOL_PATH.write_text(
            json.dumps(pool, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return pool
    return json.loads(POOL_PATH.read_text(encoding="utf-8"))


RE_MARCADOR = re.compile(r"\[ref:\s*([a-z0-9\-,\s]+?)\s*\]")
CABECALHO_REFS = "## 7. Referências Bibliográficas"


def aplicar(caminho: Path, pool: dict[str, str]) -> tuple[int, int]:
    texto = caminho.read_text(encoding="utf-8")

    # Idempotencia: capitulo ja numerado nao tem marcadores e NAO pode ser
    # reprocessado — reprocessar apagaria a secao 7 (perda de rastreabilidade).
    if not RE_MARCADOR.search(texto):
        citacoes = len(re.findall(r"\[\d+\]", texto.split(CABECALHO_REFS)[0]))
        print(f"[skip] {caminho.name}: sem marcadores [ref:...] — secao 7 preservada")
        return 0, citacoes

    texto = texto.split(CABECALHO_REFS)[0].rstrip() + "\n"
    ordem: list[str] = []
    faltando: set[str] = set()

    def substituir(m: re.Match) -> str:
        chaves = [k.strip() for k in m.group(1).split(",") if k.strip()]
        numeros = []
        for chave in chaves:
            if chave not in pool:
                faltando.add(chave)
                continue
            if chave not in ordem:
                ordem.append(chave)
            numeros.append(str(ordem.index(chave) + 1))
        return " ".join(f"[{n}]" for n in numeros)

    corpo = RE_MARCADOR.sub(substituir, texto)
    if faltando:
        raise SystemExit(f"[ERRO] chaves ausentes no pool: {sorted(faltando)}")

    linhas = [f"[{i}] {pool[chave]}" for i, chave in enumerate(ordem, 1)]
    final = corpo.rstrip() + "\n\n" + CABECALHO_REFS + "\n\n" + "\n".join(linhas) + "\n"
    caminho.write_text(final, encoding="utf-8")
    return len(ordem), sum(1 for c in corpo.split("] ") if True) and len(re.findall(r"\[\d+\]", corpo))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--aplicar", nargs="+", type=Path)
    args = ap.parse_args()

    pool = carregar_pool()

    if args.listar:
        for chave, entrada in pool.items():
            print(f"{chave}\n    {entrada[:150]}")
        print(f"\ntotal: {len(pool)}")
        return

    for caminho in args.aplicar or []:
        refs, citacoes = aplicar(caminho, pool)
        print(f"[ok] {caminho.name}: {refs} referências, {citacoes} citações inline")


if __name__ == "__main__":
    main()
