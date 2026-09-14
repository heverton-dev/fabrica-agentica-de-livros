#!/usr/bin/env python3
"""
V5 / Fase E — Gate do PLAYBOOK (R-PBK-0 a R-PBK-8).

Impede o modo de falha mais provavel desta etapa: o playbook virar um RESUMO do
livro em vez de um documento de bancada. R-PBK-0 e o coracao — mede a
similaridade de cada card contra a TEORIA do capitulo-fonte (§1 Introducao,
§2 Explica, §3 Ilustra) e reprova quando o card esta repetindo prosa.

Uso:
    python scripts/validar-playbook.py playbooks/<slug>--pbk
    python scripts/validar-playbook.py playbooks/<slug>--pbk --estrito
    python scripts/validar-playbook.py playbooks/<slug>--pbk --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

from secoes_eita import (dividir_secoes, normalizar, secao_por_nome, sem_codigo)

from tipos_obra import console_utf8
import tipos_obra as TO

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

LIMIAR_TEORIA = 0.25       # R-PBK-0: Jaccard de shingles card x teoria
MIN_FEITO = 3              # R-PBK-4
MAX_FEITO = 7
MAX_LINHAS_PARTE = 25      # R-PBK-5

REGRAS = {
    "R-PBK-0": "playbook nao repete teoria (§1, §2, §3 e §7 fora)",
    "R-PBK-1": "todo card tem as 7 partes (① a ⑦)",
    "R-PBK-2": "todo card cita ao menos 1 entrega com caminho de arquivo",
    "R-PBK-3": "todo card tem 1 comando de verificacao executavel",
    "R-PBK-4": f"'Feito quando' tem de {MIN_FEITO} a {MAX_FEITO} itens binarios",
    "R-PBK-5": f"nenhuma parte do card excede {MAX_LINHAS_PARTE} linhas",
    "R-PBK-6": "capa com badge de nivel + ilustracao no motivo condutor",
    "R-PBK-7": "1 card por capitulo do livro-mae, na mesma ordem, sem lacuna",
    "R-PBK-8": "vocabulario do motivo_condutor presente nos nomes de estagio",
}


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def shingles(texto, n=6):
    palavras = normalizar(sem_codigo(texto)).split()
    if len(palavras) < n:
        return set()
    return {" ".join(palavras[i:i + n]) for i in range(len(palavras) - n + 1)}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def texto_do_card(card):
    """Prosa do card (sem codigo) — o que R-PBK-0 compara contra a teoria."""
    partes = [card.get("objetivo", "")]
    partes += card.get("feito_quando", [])
    partes += card.get("armadilhas", [])
    partes += [b.get("titulo", "") for b in card.get("execucao", [])]
    return "\n".join(p for p in partes if p)


def linhas_das_partes(card):
    """Numero de linhas de cada uma das 7 partes (R-PBK-5)."""
    execucao_linhas = sum(len(b.get("codigo", "").splitlines()) + 2
                          for b in card.get("execucao", []))
    return {
        "objetivo": len((card.get("objetivo") or "").splitlines()) or (1 if card.get("objetivo") else 0),
        "pre_requisito": 1 if card.get("pre_requisito") else 0,
        "entregas": len(card.get("entregas", [])),
        "execucao": execucao_linhas,
        "gate": 1 if card.get("gate") else 0,
        "feito_quando": len(card.get("feito_quando", [])),
        "armadilhas": len(card.get("armadilhas", [])),
    }


def validar(slug, limiar_teoria=LIMIAR_TEORIA):
    dir_pbk = TO.dir_obra(slug, DIR_OUTPUT)
    config = _ler_json(dir_pbk / "config_obra.json")
    sumario = _ler_json(dir_pbk / "sumario_macro.json")
    dir_passos = dir_pbk / "passos"

    violacoes = []
    def falha(regra, detalhe, passo=None):
        violacoes.append({"regra": regra, "enunciado": REGRAS[regra],
                          "passo": passo, "detalhe": detalhe})

    if not dir_passos.exists():
        return {"slug": slug, "conforme": False, "total_passos": 0,
                "violacoes": [{"regra": "R-PBK-7", "enunciado": REGRAS["R-PBK-7"],
                               "passo": None, "detalhe": f"pasta inexistente: {dir_passos}"}],
                "avisos": [], "regras": REGRAS}

    cards = [_ler_json(p) for p in sorted(
        dir_passos.glob("passo_*.json"),
        key=lambda p: int(re.search(r"passo_(\d+)", p.stem).group(1)))]
    total = len(cards)

    # ── Contexto do livro-mae (para R-PBK-0 e R-PBK-7) ────────────────────────
    slug_mae_simples = TO.resolver_slug_mae(config) or sumario.get("slug_livro_mae")
    dir_mae = None
    if slug_mae_simples:
        # V5 (HUB POR COLECAO): o livro-mae vive em output/<colecao>/livros/<slug>,
        # nao em output/livros/<slug>. dir_obra resolve plano, por-obra e hub.
        for raiz in ("livros", "tccs"):
            candidato = TO.dir_obra(f"{raiz}/{slug_mae_simples}", DIR_OUTPUT)
            if candidato.exists():
                dir_mae = candidato
                break

    avisos = []

    # ── R-PBK-7: 1 card por capitulo, mesma ordem, sem lacuna ─────────────────
    def _caminho_capitulo(numero):
        """A fabrica grava tanto cap_1.md quanto cap_01.md — aceite os dois."""
        for nome in (f"cap_{str(numero).zfill(2)}.md", f"cap_{int(numero)}.md"):
            caminho = dir_mae / "capitulos" / nome
            if caminho.exists():
                return caminho
        return None

    if dir_mae is not None:
        caps_mae = sorted(
            int(re.search(r"cap_(\d+)", p.stem).group(1))
            for p in (dir_mae / "capitulos").glob("cap_*.md")
            if not p.stem.startswith("_")
        ) if (dir_mae / "capitulos").exists() else []
        numeros = [int(c.get("numero", 0)) for c in cards]
        if caps_mae and numeros != caps_mae:
            faltando = sorted(set(caps_mae) - set(numeros))
            sobrando = sorted(set(numeros) - set(caps_mae))
            falha("R-PBK-7",
                  f"cards={numeros} vs capitulos={caps_mae}"
                  + (f" · faltando {faltando}" if faltando else "")
                  + (f" · sobrando {sobrando}" if sobrando else ""))
    else:
        avisos.append("livro-mae nao localizado — R-PBK-0 e R-PBK-7 nao verificados")

    # ── R-PBK-8: vocabulario do motivo condutor nos estagios ──────────────────
    vocab = ((sumario.get("motivo_condutor") or {}).get("vocabulario")) or []
    if vocab:
        nomes = normalizar(" ".join(c.get("estagio", "") for c in cards))
        if not any(normalizar(t) in nomes for t in vocab):
            falha("R-PBK-8", f"nenhum termo de {vocab[:5]} aparece nos nomes de estagio")
    else:
        avisos.append("obra sem motivo_condutor.vocabulario — R-PBK-8 nao aplicavel (V3)")

    # ── Regras por card ───────────────────────────────────────────────────────
    for card in cards:
        n = card.get("numero", "??")

        partes_vazias = [k for k, v in {
            "① objetivo": card.get("objetivo"),
            "② pre_requisito": card.get("pre_requisito"),
            "③ entregas": card.get("entregas"),
            "④ execucao": card.get("execucao"),
            "⑤ gate": card.get("gate"),
            "⑥ feito_quando": card.get("feito_quando"),
            "⑦ armadilhas": card.get("armadilhas"),
        }.items() if not v]
        if partes_vazias:
            falha("R-PBK-1", f"partes vazias: {', '.join(partes_vazias)}", n)

        if not card.get("entregas"):
            falha("R-PBK-2", "nenhum caminho de arquivo citado", n)

        if not card.get("gate"):
            falha("R-PBK-3", "nenhum comando de verificacao executavel", n)

        qtd_feito = len(card.get("feito_quando", []))
        if not (MIN_FEITO <= qtd_feito <= MAX_FEITO):
            falha("R-PBK-4", f"{qtd_feito} item(ns) em 'Feito quando'", n)

        excedidas = {k: v for k, v in linhas_das_partes(card).items() if v > MAX_LINHAS_PARTE}
        if excedidas:
            falha("R-PBK-5", f"partes acima de {MAX_LINHAS_PARTE} linhas: {excedidas}", n)

        # R-PBK-0 — o card nao pode ser prosa reciclada da teoria
        if dir_mae is not None:
            cap_path = _caminho_capitulo(n)
            if cap_path is not None:
                secoes = dividir_secoes(cap_path.read_text(encoding="utf-8", errors="replace"))
                teoria = "\n".join(secao_por_nome(secoes, a)
                                   for a in ("introducao", "explica", "ilustra"))
                sim = round(jaccard(shingles(texto_do_card(card)), shingles(teoria)), 3)
                if sim > limiar_teoria:
                    falha("R-PBK-0", f"similaridade com a teoria = {sim} "
                                     f"(limiar {limiar_teoria})", n)

    # ── R-PBK-6: badge de nivel + capa ────────────────────────────────────────
    if not (config.get("senioridade_obra") or "").strip():
        falha("R-PBK-6", "config_obra.json sem 'senioridade_obra' (badge obrigatorio)")
    # A capa pode ter sido gravada como capa.png (padrao do gerar-capa.py, usado
    # por /criar-capa) ou como capa_livro.png (nome que o empacotador procura).
    # Mesmo criterio de metadados_livro.py: aceitar os dois nomes.
    if not any((dir_pbk / "imagens" / nome).exists()
               for nome in ("capa_livro.png", "capa.png")):
        avisos.append("capa ainda nao gerada — rode scripts/gerar-capa.py --tipo playbook")

    return {
        "slug": slug,
        "conforme": not violacoes,
        "total_passos": total,
        "violacoes": violacoes,
        "avisos": avisos,
        "regras": REGRAS,
    }


def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Gate do playbook (R-PBK-0 a R-PBK-8)")
    ap.add_argument("slug", help="ex.: playbooks/meu-livro--pbk")
    ap.add_argument("--limiar-teoria", type=float, default=LIMIAR_TEORIA)
    ap.add_argument("--estrito", action="store_true", help="exit 1 se NAO CONFORME")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rel = validar(args.slug, limiar_teoria=args.limiar_teoria)

    dir_rev = TO.dir_obra(args.slug, DIR_OUTPUT) / "revisao"
    dir_rev.mkdir(parents=True, exist_ok=True)
    (dir_rev / "relatorio_playbook.json").write_text(
        json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(rel, ensure_ascii=False, indent=2))
    else:
        estado = "CONFORME" if rel["conforme"] else "NAO CONFORME"
        print(f"[{estado}] {args.slug} — {rel['total_passos']} passo(s), "
              f"{len(rel['violacoes'])} violacao(oes)")
        for v in rel["violacoes"]:
            alvo = f"passo {v['passo']}" if v["passo"] else "obra"
            print(f"  [{v['regra']}] {alvo}: {v['detalhe']}")
        for a in rel["avisos"]:
            print(f"  [AVISO] {a}")

    if args.estrito and not rel["conforme"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
