#!/usr/bin/env python3
"""
V5.4 — Minerador academico (Fase 1). Custo LLM ZERO.

Consulta as fontes academicas do registro declarativo `fontes_academicas.py`
(OpenAlex, Crossref, arXiv, Semantic Scholar, SciELO, PubMed) via APIs abertas
e grava em `output/<obra>/pesquisa/`:

  mineracao_academica_<slug>.json   registros normalizados + cobertura
  mineracao_academica_<slug>.md     fontes ABNT classe (A), pronto p/ dossier
  cache_academica.json              cache local p/ --sem-rede e reexecucao

O .md nasce ja no contrato do `validar-fontes.py` (linha com "Disponivel em:"
+ classe (A)): entra automaticamente na proporcao A/B do dossier. O pesquisador
(LLM) usa o JSON como materia-prima e complementa com WebSearch nas bases sem
API publica (Google Scholar, ACM DL, IEEE Xplore, Springer).

Uso:
    python scripts/minerar-fontes-academicas.py "<tema>" --slug <obra>
    python scripts/minerar-fontes-academicas.py "<tema>" --slug <obra> --fontes arxiv,scielo
    python scripts/minerar-fontes-academicas.py "<tema>" --slug <obra> --max 5 --json
    python scripts/minerar-fontes-academicas.py "<tema>" --slug <obra> --sem-rede
    python scripts/minerar-fontes-academicas.py "<tema>" --saida docs/mineracao_<tema>
"""

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import fontes_academicas as FA
import tipos_obra as TO
from tipos_obra import console_utf8


def _buscar_fonte_worker(idx, fonte, tema, max_por_fonte, sem_rede, cache):
    """Worker para paralelismo: busca uma fonte e retorna (idx, registros)."""
    chave = f"{fonte}|{tema}"
    if sem_rede:
        if chave in cache:
            regs = cache[chave].get("registros", [])
            status, erro = "cache", None
        else:
            regs, status, erro = [], "sem-rede", "sem cache local"
    else:
        try:
            regs = FA.buscar(fonte, tema, max_por_fonte)
            cache[chave] = {"em": FA.data_hoje_abnt(), "registros": regs}
            status, erro = "ok", None
        except FA.FonteIndisponivel as exc:
            regs, status, erro = [], "erro", str(exc)
        except Exception as exc:  # noqa: BLE001
            regs, status, erro = [], "erro", str(exc)
    return idx, fonte, status, erro, len(regs), regs


def minerar(tema, fontes, max_por_fonte, sem_rede, cache):
    """Roda as fontes em paralelo (max 3 workers) e devolve (registros_dedup, cobertura, cache_atualizado)."""
    cobertura = {}
    todos = []
    max_workers = min(3, len(fontes))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(_buscar_fonte_worker, idx, fonte, tema, max_por_fonte, sem_rede, cache)
            for idx, fonte in enumerate(fontes)
        ]
        # Agregar resultados mantendo ordem original
        resultados = [(f.result(), idx) for idx, f in enumerate(futures)]
        resultados.sort(key=lambda x: x[0][0])  # Ordenar pelo índice original

        for (idx, fonte, status, erro, n, regs), _ in resultados:
            cobertura[fonte] = {"status": status, "erro": erro, "n": n}
            todos.extend(regs)

    return FA.deduplicar(todos), cobertura, cache


def escrever_artefatos(base, tema, unicos, cobertura, data):
    """Grava <base>.json e <base>.md; retorna os caminhos."""
    base = Path(base)
    dir_alvo = base.parent
    dir_alvo.mkdir(parents=True, exist_ok=True)

    json_alvo = base.with_suffix(".json")
    json_alvo.write_text(json.dumps({
        "tema": tema,
        "gerado_em": data,
        "fontes_consultadas": [f for f in cobertura],
        "cobertura": cobertura,
        "total_unicos": len(unicos),
        "registros": unicos,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    linhas_md = [
        f"# Mineracao Academica - {tema}",
        "",
        "Mineracao deterministic a (custo LLM zero) via APIs abertas",
        "(`scripts/fontes_academicas.py`). Gerado em: " + data + ".",
        "",
        "## Fontes consultadas",
        "",
    ]
    for fonte, cov in cobertura.items():
        linhas_md.append(f"- {FA.descritor(fonte)['nome']}: {cov['n']} resultados ({cov['status']})")
    linhas_md += [
        "",
        "## Fontes brutas (mineracao academica - classe A)",
        "",
    ]
    linhas_md += [FA.formato_abnt(r, data_acesso=data) for r in unicos]

    md_alvo = base.with_suffix(".md")
    md_alvo.write_text("\n".join(linhas_md) + "\n", encoding="utf-8")
    return json_alvo, md_alvo


def _exibir(caminho):
    """Caminho relativo ao projeto quando possivel; absoluto caso contrario."""
    try:
        return str(caminho.relative_to(TO.DIR_PROJETO))
    except ValueError:
        return str(caminho)


def main():
    ap = argparse.ArgumentParser(
        description="Minerador academico: consulta APIs abertas e gera dossier ABNT (custo zero)")
    ap.add_argument("tema", help="tema/query da busca academica")
    ap.add_argument("--slug", help="obra alvo (resolvida via tipos_obra.dir_obra)")
    ap.add_argument("--saida", help="caminho base alternativo (sem extensao)")
    ap.add_argument("--fontes", help="subconjunto de fontes separado por virgulas")
    ap.add_argument("--max", type=int, default=None,
                    help="max de resultados por fonte (default: do registro)")
    ap.add_argument("--sem-rede", action="store_true",
                    help="usa apenas o cache local, nunca acessa a rede")
    ap.add_argument("--json", action="store_true", help="imprime relatorio JSON completo")
    args = ap.parse_args()

    if not args.slug and not args.saida:
        print("[ERRO] Informe --slug <obra> ou --saida <caminho base>.")
        return 1

    if args.fontes:
        fontes = [f.strip() for f in args.fontes.split(",") if f.strip()]
        desconhecidas = [f for f in fontes if f not in FA.fontes_validas()]
        if desconhecidas:
            print(f"[ERRO] Fontes desconhecidas: {', '.join(desconhecidas)}.")
            print(f"       Validas: {', '.join(FA.fontes_validas())}.")
            return 1
    else:
        fontes = list(FA.fontes_validas())

    if args.saida:
        base = Path(args.saida)
        dir_pesquisa = base.parent
    else:
        dir_obra = TO.dir_obra(args.slug, TO.DIR_OUTPUT)
        dir_pesquisa = dir_obra / "pesquisa"
        base = dir_pesquisa / f"mineracao_academica_{Path(args.slug).name}"
    dir_pesquisa.mkdir(parents=True, exist_ok=True)

    caminho_cache = dir_pesquisa / "cache_academica.json"
    cache = {}
    if caminho_cache.exists():
        try:
            cache = json.loads(caminho_cache.read_text(encoding="utf-8"))
        except ValueError:
            cache = {}

    data = FA.data_hoje_abnt()
    unicos, cobertura, cache = minerar(args.tema, fontes, args.max, args.sem_rede, cache)
    caminho_cache.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

    json_alvo, md_alvo = escrever_artefatos(
        base, args.tema, unicos, cobertura, data)

    print(f"Mineracao Academica - {args.tema}")
    print(f"  fontes consultadas     : {', '.join(fontes)}")
    for fonte, cov in cobertura.items():
        detalhe = "" if cov["erro"] is None else f" ({cov['erro']})"
        print(f"  {fonte:<18}: {cov['n']} resultados ({cov['status']}){detalhe}")
    print(f"  total unicos (dedup)   : {len(unicos)}")
    print(f"\n  JSON: {_exibir(json_alvo)}")
    print(f"  MD  : {_exibir(md_alvo)}")

    if args.json:
        print(json.dumps({
            "tema": args.tema,
            "cobertura": cobertura,
            "total_unicos": len(unicos),
            "registros": unicos,
        }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    console_utf8()
    sys.exit(main())
