#!/usr/bin/env python3
"""
F1 — Gate de REFERÊNCIAS REAIS (R-RF-1 a R-RF-3).

Extrai URLs e DOIs da seção 7 (Referências) de cada capítulo e confere se a
fonte existe (HEAD com cache local + fallback offline). Referência de livro
(sem URL) passa como "sem_url" — o gate verifica REAIS, não formato.

R-RF-1: toda referência com URL/DOI é conferida (ok ou não verificado).
R-RF-2: URL/DOI com resposta 4xx/5xx ou falha de DNS é REPROVADA (fonte
        inventada/inexistente).
R-RF-3: o gate nunca reprova por indisponibilidade de rede — sem conexão o
        registro vira "nao_verificado" (não vira falha).

Semântica de status por URL:
  ok              -> resposta 2xx/3xx (fonte acessível)
  falha           -> 4xx/5xx ou DNS/SSL (fonte provavelmente inexistente)
  nao_verificado  -> sem rede, timeout, 403/429 (anti-bot) ou cache ausente
                     com --sem-rede — nunca reprova

Cache: <obra>/validacao/cache_urls.json — reutilizado entre execuções; com
--sem-rede o gate consulta APENAS o cache (útil em CI offline).

Uso:
    python scripts/validar-referencias.py <slug>
    python scripts/validar-referencias.py <slug> --capitulo 7
    python scripts/validar-referencias.py <slug> --md docs/x.md
    python scripts/validar-referencias.py <slug> --estrito   # exit 1 se falha
    python scripts/validar-referencias.py <slug> --json
    python scripts/validar-referencias.py <slug> --sem-rede  # só cache

Relatório: output/<slug>/validacao/relatorio_referencias.json
"""

import argparse
import json
import random
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from secoes_eita import dividir_secoes, secao_por_nome

import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

RE_URL = re.compile(r"https?://[^\s)\]}>\"'`]+")
RE_DOI = re.compile(r"(?:doi\.org/|doi:\s*)(10\.\d{4,9}/[^\s)\]}>\"'`]+)", re.IGNORECASE)

TIMEOUT_SEGUNDOS = 12
USER_AGENT = "Mozilla/5.0 (compatible; FabricaAgentica/1.0; validacao-de-referencias)"
# Erros de servidor que não indicam fonte inexistente (anti-bot/limite) — viram
# "nao_verificado", nunca falha.
HTTP_NAO_CONCLUSIVO = {403, 429, 500, 502, 503, 504}

# Resiliencia de rede (melhorias/21-08-2026-plano-acao-tokens-sob-pericia.md,
# item C): retry curto com backoff+jitter SO para falha transitoria (timeout/
# URLError ou HTTP_NAO_CONCLUSIVO). 404/erro definitivo nunca retenta.
MAX_TENTATIVAS_URL = 2
BASE_BACKOFF_URL_SEGUNDOS = 0.3

REGRAS = {
    "R-RF-1": "referência com URL/DOI é conferida (ok ou não verificado)",
    "R-RF-2": "URL/DOI com 4xx/5xx ou DNS/SSL é reprovada (fonte inexistente)",
    "R-RF-3": "sem rede => nao_verificado, nunca falha",
}


def extrair_referencias(texto_secao):
    """[(tipo, valor)] com 'url'|'doi' extraídos da seção de referências.

    Preserva a ordem de aparição no texto. URLs https://doi.org/<doi> são
    representadas como 'doi' (a forma canônica); o par não duplica.
    """
    textos = texto_secao or ""
    achados = []  # (posicao, tipo, valor)
    for m in RE_URL.finditer(textos):
        achados.append((m.start(), "url", m.group(0).rstrip(".,;:")))
    for m in RE_DOI.finditer(textos):
        achados.append((m.start(), "doi", m.group(1).rstrip(".,;:")))
    achados.sort(key=lambda t: t[0])

    dois = {v.lower() for p, t, v in achados if t == "doi"}
    vistos, unicos = set(), []
    for _pos, tipo, valor in achados:
        if tipo == "url":
            dm = RE_DOI.search(valor)
            if dm and dm.group(1).rstrip(".,;:").lower() in dois:
                continue  # https://doi.org/<doi> já representada como DOI
        chave = (tipo, valor.lower())
        if chave in vistos:
            continue
        vistos.add(chave)
        unicos.append((tipo, valor))
    return unicos


def _tentar_urlopen(url, tentativas=MAX_TENTATIVAS_URL):
    """HEAD com retry+jitter curto em falha transitoria. Retorna
    (codigo_http, motivo) — codigo_http e None quando todas as tentativas
    esgotaram sem resposta conclusiva (motivo explica por que).
    """
    req = urllib.request.Request(
        url, method="HEAD",
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    ultimo_motivo = None
    for tentativa in range(tentativas):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SEGUNDOS) as resp:
                return resp.status, None
        except urllib.error.HTTPError as exc:
            if exc.code not in HTTP_NAO_CONCLUSIVO:
                return exc.code, None  # falha definitiva (ex.: 404) — nao insiste
            ultimo_motivo = f"HTTP {exc.code} (anti-bot/limite — não conclusivo)"
        except urllib.error.URLError as exc:
            razao = getattr(exc, "reason", exc)
            ultimo_motivo = f"rede/DNS indisponível ({razao})"
        except Exception:  # noqa: BLE001  — timeout etc. contam como não verificado
            ultimo_motivo = "falha de conexão (timeout?)"

        if tentativa < tentativas - 1:
            espera = BASE_BACKOFF_URL_SEGUNDOS * (2 ** tentativa) + random.uniform(0, 0.2)
            time.sleep(espera)

    return None, ultimo_motivo


def _checar_url(url, sem_rede, cache):
    """Consulta cache e rede; retorna (status, detalhe). Nunca levanta.

    O cache so e conclusivo para status ok/falha — um registro 'nao_verificado'
    gravado em modo offline nao bloqueia a checagem real posterior.
    """
    if url in cache and (sem_rede or cache[url]["status"] != "nao_verificado"):
        return cache[url]["status"], cache[url].get("detalhe", "cache")
    if sem_rede:
        return "nao_verificado", "sem-rede (sem cache)"

    codigo, motivo = _tentar_urlopen(url)
    if codigo is None:
        return "nao_verificado", motivo
    if 200 <= codigo < 400:
        return "ok", f"HTTP {codigo}"
    if codigo in HTTP_NAO_CONCLUSIVO:
        return "nao_verificado", f"HTTP {codigo} (anti-bot/limite — não conclusivo)"
    return "falha", f"HTTP {codigo}"


def checar_referencia(tipo, valor, sem_rede, cache):
    if tipo == "doi":
        valor = f"https://doi.org/{valor}"
    status, detalhe = _checar_url(valor, sem_rede, cache)
    # Grava apenas resultados conclusivos; 'nao_verificado' e transitorio.
    if status in ("ok", "falha"):
        cache[valor] = {"status": status, "detalhe": detalhe,
                        "em": time.strftime("%Y-%m-%d")}
    return status, detalhe


def validar_texto(texto_secao, rotulo, sem_rede, cache):
    """Valida as referências de UM texto; retorna (resultados, falhas)."""
    referencias = extrair_referencias(texto_secao)
    resultados, falhas = [], []
    if not referencias:
        # Referências apenas de livros (sem URL) ou seção vazia — não é falha
        # de realidade; o gate de forma (R14/R15) segue responsável pela presença.
        return resultados, falhas
    for tipo, valor in referencias:
        status, detalhe = checar_referencia(tipo, valor, sem_rede, cache)
        registro = {"origem": rotulo, "tipo": tipo, "valor": valor,
                    "status": status, "detalhe": detalhe}
        resultados.append(registro)
        if status == "falha":
            falhas.append(registro)
    return resultados, falhas


def alvos_da_obra(slug, dir_livro, args):
    alvos = []
    if args.md:
        p = Path(args.md)
        if not p.exists():
            print(f"[ERRO] Arquivo nao encontrado: {p}")
            return None
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
            return None
        alvos = [(c, c.stem) for c in caps]
    return alvos


def main():
    ap = argparse.ArgumentParser(
        description="Gate F1 de referencias reais: confere URL/DOI da secao 7")
    ap.add_argument("slug")
    ap.add_argument("--capitulo", help="valida apenas o capitulo N")
    ap.add_argument("--md", help="valida um markdown especifico em vez dos capitulos")
    ap.add_argument("--estrito", action="store_true", help="exit 1 se houver falha")
    ap.add_argument("--json", action="store_true", help="imprime relatorio JSON completo")
    ap.add_argument("--sem-rede", action="store_true",
                    help="apenas cache local, nunca acessa a rede")
    args = ap.parse_args()

    dir_livro = TO.dir_obra(args.slug, DIR_OUTPUT)
    if not dir_livro.exists():
        print(f"[ERRO] Obra nao encontrada: {dir_livro}")
        return 1

    dir_val = dir_livro / "validacao"
    dir_val.mkdir(exist_ok=True)
    caminho_cache = dir_val / "cache_urls.json"
    cache = {}
    if caminho_cache.exists():
        try:
            cache = json.loads(caminho_cache.read_text(encoding="utf-8"))
        except ValueError:
            cache = {}

    alvos = alvos_da_obra(args.slug, dir_livro, args)
    if alvos is None:
        return 1

    todos, falhas = [], []
    for caminho, rotulo in alvos:
        texto = caminho.read_text(encoding="utf-8", errors="replace")
        secoes = dividir_secoes(texto)
        corpo_refs = secao_por_nome(secoes, "referencias") or ""
        res, fal = validar_texto(corpo_refs, rotulo, args.sem_rede, cache)
        todos.extend(res)
        falhas.extend(fal)

    # Persiste o cache aumentado (mesmo em falha parcial) e o relatório.
    caminho_cache.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

    resumo = {}
    for r in todos:
        resumo[r["status"]] = resumo.get(r["status"], 0) + 1
    relatorio = {
        "slug": args.slug,
        "total_referencias": len(todos),
        "resumo": resumo,
        "regras": REGRAS,
        "referencias": todos,
    }
    (dir_val / "relatorio_referencias.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Gate de Referencias Reais - {args.slug}")
    print(f"  referencias com URL/DOI : {len(todos)}")
    for status in ("ok", "falha", "nao_verificado"):
        if status in resumo:
            print(f"  {status:<17}: {resumo[status]}")
    if not todos:
        print("  (nenhuma URL/DOI na secao de referencias — sem o que conferir)")

    if falhas:
        print(f"\n[FALHA] {len(falhas)} fonte(s) inacessivel(is) (4xx/5xx/DNS):")
        for f in falhas[:20]:
            print(f"  - {f['origem']}: [{f['tipo']}] {f['valor']} -> {f['detalhe']}")
        if len(falhas) > 20:
            print(f"  ... e mais {len(falhas) - 20}")
    else:
        print("\n[OK] Nenhuma fonte reprovada (referencias reais ou nao verificadas)")

    print(f"\nRelatorio: {(dir_val / 'relatorio_referencias.json').relative_to(DIR_PROJETO)}")

    if args.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    if args.estrito and falhas:
        return 1
    return 0


if __name__ == "__main__":
    console_utf8()
    sys.exit(main())
