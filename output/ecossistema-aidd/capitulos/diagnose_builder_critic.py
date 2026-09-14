# diagnose_builder_critic.py — detecta sintoma de builder=critic em repo
# Critério objetivo, sem nuance de LLM. Baseado em ferramentas e fluxo, não em intenção.

import os
import sys
import json
from pathlib import Path
from collections import defaultdict


def carregar_reviews(caminho_repo: Path) -> list[dict]:
    """Carrega lista de reviews de .gitreviews.json (formato livre — adapte ao seu repo).
    Se o repo não tiver esse artefato, a peça 1 ainda é válida — o diagnóstico pergunta
    'o que eu teria que instrumentar para saber que builder=critic acontece?'.
    """
    arquivo = caminho_repo / ".gitreviews.json"
    if not arquivo.exists():
        return []
    with open(arquivo, encoding="utf-8") as f:
        return json.load(f)


def agrupar_por_pr(reviews: list[dict]) -> dict[str, list[dict]]:
    grupos = defaultdict(list)
    for r in reviews:
        pr = r.get("pull_request") or r.get("pr") or "desconhecido"
        grupos[pr].append(r)
    return dict(grupos)


def sintomas_builder_critic(reviews: list[dict]) -> list[dict]:
    """Detecta reviews onde autor do PR revisou/aprovou seu próprio PR.
    Critério objetivo: quem abriu == quem aprovou. Sem nuance de LLM.
    """
    resultados = []
    for review in reviews:
        autor = review.get("author") or review.get("quem_abriu") or ""
        revisor = review.get("reviewer") or review.get("quem_aprovou") or ""
        if autor and revisor and autor.lower().strip() == revisor.lower().strip():
            resultados.append({
                "arquivo": review.get("arquivo") or "desconhecido",
                "pr": review.get("pull_request") or review.get("pr") or "desconhecido",
                "autor": autor,
                "revisora": revisor,
                "data": review.get("data") or "desconhecida",
            })
    return resultados


def main(caminho: str) -> int:
    repo = Path(caminho)
    if not repo.is_dir():
        print(f"ERRO: {caminho} não é diretório", file=sys.stderr)
        return 2
    reviews = carregar_reviews(repo)
    if not reviews:
        print("AVISO: sem .gitreviews.json — peça 1 não pode ser diagnosticada numericamente.\n"
              "Instrumentar coleta de reviews é o primeiro passo para tornar builder=critic auditável.\n"
              "Veja capítulo 3 para critérios objetivos de classificação builder/critic/ambíguo.")
        return 0
    por_pr = agrupar_por_pr(reviews)
    sintomas = sintomas_builder_critic(reviews)
    print(f"Reviews carregados: {len(reviews)}")
    print(f"PRs distintas: {len(por_pr)}")
    print(f"Sintomas builder=critic: {len(sintomas)}")
    for s in sintomas[:10]:
        print(f"  - PR {s['pr']}: {s['autor']} aprovou próprio {s['arquivo']} em {s['data']}")
    if len(sintomas) > 10:
        print(f"  ... mais {len(sintomas) - 10} sintoma (ver perfil completo)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python diagnose_builder_critic.py <caminho-do-repo>", file=sys.stderr)
        sys.exit(2)
    raise SystemExit(main(sys.argv[1]))
