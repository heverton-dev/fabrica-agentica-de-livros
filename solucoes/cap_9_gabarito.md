# Gabarito — Capítulo 9: Scripts e gates

## Exercício 1 — Gate de contrato com motivo localizado

```python
import re
import sys
from pathlib import Path

MIN_REFERENCIAS = 20


def verificar(caminho, minimo=MIN_REFERENCIAS):
    texto = Path(caminho).read_text(encoding="utf-8", errors="replace")
    secoes = re.split(r"^##\s*\d*\.?\s*", texto, flags=re.MULTILINE)
    corpo, refs = "\n".join(secoes[:-1]), secoes[-1]
    citadas = set(re.findall(r"\[(\d{1,3})\]", corpo))
    listadas = set(re.findall(r"^\[(\d{1,3})\]", refs, re.MULTILINE))
    erros = []
    orfas = sorted(citadas - listadas, key=int)
    if orfas:
        erros.append(f"{caminho}: citacoes sem referencia -> {', '.join(orfas)}")
    if len(listadas) < minimo:
        erros.append(f"{caminho}: {len(listadas)} referencias (minimo {minimo})")
    return erros


if __name__ == "__main__":
    problemas = verificar(sys.argv[1])
    for p in problemas:
        print(f"[CONTRATO] {p}")
    sys.exit(1 if problemas else 0)
```

Critério de aceitação: o motivo precisa nomear **os números das citações órfãs**, não
apenas dizer "referências inválidas".

## Exercício 2 — Encadeador

```bash
#!/usr/bin/env bash
set -euo pipefail
ARTEFATO="${1:?uso: auditar.sh <arquivo>}"
python scripts/gate_forma.py "$ARTEFATO"
python scripts/gate_contrato.py "$ARTEFATO"
python scripts/gate_merito.py "$ARTEFATO"
echo "[OK] $ARTEFATO aprovado nos tres niveis"
```

Ordem obrigatória: forma → contrato → mérito. Inverter queima execução em artefato
já condenado.

## Exercício 3 — Bloqueio mecânico

Exemplo de hook de pré-commit que executa o encadeamento:

```bash
#!/usr/bin/env bash
set -euo pipefail
python -m pytest -q
```

Instalado em `.git/hooks/pre-commit` (ou via gerenciador de hooks). Sem essa etapa,
o gate continua sendo sugestão.

## Checklist de aceitação

- [ ] Um gate por família (forma, contrato, mérito)
- [ ] Motivo sempre com arquivo/linha ou identificador
- [ ] Encadeamento com parada no primeiro erro
- [ ] Bloqueio mecânico ativo
- [ ] Registro de auditoria com gates não executados
- [ ] Taxa de reprovação monitorada

## Registro de aprendizagem

Gate com 0% de reprovação não indica excelência: indica ausência de verificação.
Comportamento saudável fica entre 5% e 40% dos artefatos.
