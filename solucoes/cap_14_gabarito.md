# Gabarito — Capítulo 14: Configurações que nunca te contam

## Exercício 1 — Diff entre efetiva e versionada

```bash
agent config dump --json > /tmp/efetiva.json
python - <<'EOF'
import json
from pathlib import Path

efetiva = json.loads(Path("/tmp/efetiva.json").read_text(encoding="utf-8"))
projeto = json.loads(Path(".agent/settings.json").read_text(encoding="utf-8"))
for chave, valor in sorted(projeto.items()):
    real = efetiva.get(chave, "<ausente>")
    print(f"[{'OK ' if real == valor else 'DIF'}] {chave}: projeto={valor!r} efetiva={real!r}")
EOF
```

Resposta esperada: pelo menos uma linha `DIF`, quase sempre por variável de ambiente
herdada do shell.

## Exercício 2 — Auditoria em oito perguntas

Respostas mínimas aceitáveis:

| # | Resposta |
|---|---|
| 1 | Precedência testada empiricamente, não presumida |
| 2 | Teto de saída declarado e compatível com o maior artefato |
| 3 | Timeout acima do p95 real da operação mais lenta |
| 4 | Rede negada por padrão |
| 5 | Leitura de ambiente sensível negada |
| 6 | Retenção de histórico documentada |
| 7 | Compactação e fallback com limiar conhecido |
| 8 | Data de revisão e dono registrados |

## Exercício 3 — Teste de invariante

```python
import json
from pathlib import Path

INVARIANTES = [
    ("permissions.deny", "Bash(git push*)", "push proibido"),
    ("rede.allow", False, "rede negada por padrao"),
]


def verificar(caminho=".agent/settings.json"):
    cfg = json.loads(Path(caminho).read_text(encoding="utf-8"))
    falhas = []
    for chave, esperado, motivo in INVARIANTES:
        atual = cfg
        for parte in chave.split("."):
            atual = atual.get(parte, {}) if isinstance(atual, dict) else {}
        if esperado not in atual and esperado != atual:
            falhas.append(f"{chave}: {motivo}")
    return falhas
```

Critério: verificar o **valor**, não a presença da chave.

## Checklist de aceitação

- [ ] Diff efetiva/versionada executado
- [ ] Oito perguntas respondidas com surpresas anotadas
- [ ] Dois invariantes cobertos por teste
- [ ] Decisões registradas com dono e data de revisão
- [ ] Truncamento explicitado nas ferramentas

## Registro de aprendizagem

O caso clássico de "alucinação" que não é alucinação: teto de saída truncando o
resultado da ferramenta sem marcar o corte. O modelo preenche o buraco e leva a culpa.
