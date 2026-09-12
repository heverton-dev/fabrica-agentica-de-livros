# Gabarito — Capítulo 12: Orquestração, worktrees e Orca ADE

## Exercício 1 — Worktrees por tarefa

```bash
git worktree add ../wt-bug-1042 -b fix/bug-1042
git worktree add ../wt-bug-1101 -b fix/bug-1101
git worktree list
```

Regras: fora do diretório principal, nome com identificador da tarefa, remoção com
`git worktree remove` ao final.

## Exercício 2 — Detecção de sobreposição

```python
def sobreposicao(frota):
    conflitos = []
    for i, a in enumerate(frota):
        for b in frota[i + 1:]:
            comuns = set(a.get("arquivos_provaveis", [])) & set(b.get("arquivos_provaveis", []))
            if comuns:
                conflitos.append({"a": a["tarefa"], "b": b["tarefa"], "arquivos_comuns": sorted(comuns)})
    return conflitos
```

Critério: rodar **antes** do fan-out. Detecção depois do merge já é prejuízo pago.

## Exercício 3 — Reconciliador com gate nos dois lados

```bash
#!/usr/bin/env bash
set -euo pipefail
for WT in ../wt-bug-1042 ../wt-bug-1101; do
  (cd "$WT" && python -m pytest -q) || { echo "[ABORTA] gate do worktree falhou"; exit 1; }
  git merge --no-ff "$(git -C "$WT" rev-parse --abbrev-ref HEAD)"
  python -m pytest -q || { echo "[ABORTA] suite principal quebrou"; exit 1; }
done
```

## Exercício 4 — Política de recursos compartilhados

```json
{
  "politica_recursos": {
    "banco_de_testes": { "modo": "fila", "concorrencia_maxima": 1 },
    "limite_api": { "modo": "teto", "requisicoes_por_minuto": 60 }
  }
}
```

Sem fila no banco de testes, falhas fantasma aparecem e o time persegue bug que é
artefato da concorrência.

## Checklist de aceitação

- [ ] Dois worktrees criados e depois removidos
- [ ] Plano de frota com `arquivos_provaveis`
- [ ] Sobreposição detectada antes do fan-out
- [ ] Recursos compartilhados com política
- [ ] Reconciliador sequencial com gate duplo
- [ ] Painel de frota com arquivos realmente tocados

## Registro de aprendizagem

Paralelize o independente; serialize o que compartilha estado. A regra é simples e
quase sempre violada porque o paralelismo parece gratuito até a primeira colisão.
