# Gabarito — Capítulo 10: Hooks

## Exercício 1 — Guardião de comandos

```python
#!/usr/bin/env python3
"""Bloqueia padroes destrutivos antes da execucao da ferramenta."""
import json
import sys

PADROES_PROIBIDOS = ["rm -rf /", "git push --force", "dropdb"]


def main():
    evento = json.load(sys.stdin)
    comando = (evento.get("tool_input") or {}).get("command", "")
    for padrao in PADROES_PROIBIDOS:
        if padrao in comando:
            print(f"[guard] BLOQUEADO: {padrao}", file=sys.stderr)
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
```

Critério: o hook **decide**, não executa. Código de saída 2 é o bloqueio.

## Exercício 2 — Pre-commit bloqueante

```bash
#!/usr/bin/env bash
set -euo pipefail
if ! python -m pytest -q; then
  echo "[pre-commit] BLOQUEADO: suite vermelha." >&2
  exit 1
fi
```

Instalação: copiar para `.git/hooks/pre-commit` e dar permissão de execução. Precisa
ser versionado em `scripts/hooks/` e copiado no setup, porque `.git/hooks` não é
versionado.

## Exercício 3 — Auditoria

```json
{
  "evento": "PostToolUse",
  "matcher": "*",
  "hooks": [{ "type": "command", "command": "python scripts/registrar.py >> logs/sessao.jsonl" }]
}
```

O registro deve truncar o resultado (ex.: 200 caracteres). Auditoria não é lugar de
despejar payload inteiro — e, se houver dado pessoal, não registrar em claro.

## Checklist de aceitação

- [ ] Guardião antes da ferramenta com padrões explícitos
- [ ] Pre-commit bloqueante instalado e versionado
- [ ] Hook de formatação sem bloquear
- [ ] Registro de auditoria append-only com truncamento
- [ ] Tempo de execução medido (meta < 100 ms nos eventos quentes)

## Registro de aprendizagem

Hooks lentos são desativados pelo time. Se a verificação é cara, mova para o evento
menos frequente (fim de turno ou commit) em vez de rodá-la a cada edição.
