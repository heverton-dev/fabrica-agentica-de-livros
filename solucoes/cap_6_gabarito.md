# Gabarito — Capítulo 6: Cache hit

## Exercício 1 — Achar o invalidado de topo

Procedimento: capturar o prompt montado em dois turnos da mesma sessão e comparar.

```bash
python scripts/dump-prompt.py --sessao bug-1042 --turno 1 > /tmp/turno1.txt
python scripts/dump-prompt.py --sessao bug-1042 --turno 9 > /tmp/turno9.txt
diff /tmp/turno1.txt /tmp/turno9.txt | head
```

Resposta esperada: a primeira divergência aparece muito cedo (data, caminho de trabalho
ou contador de tarefas). Qualquer divergência nas primeiras linhas é invalidado de topo.

## Exercício 2 — Reordenar o prompt

```python
def montar_prompt(instrucao, ferramentas, skills, base, historico, turno_atual):
    estavel = [instrucao, ferramentas, skills]
    sessao = [base]
    volatil = [*historico, turno_atual]
    return {"estavel": estavel, "sessao": sessao, "volatil": volatil}
```

Critério de aceitação: data, caminho, nome de usuário e contador não podem aparecer no
bloco `estavel`. Ordem das ferramentas precisa ser determinística.

## Exercício 3 — Serialização estável

```python
import json

config_estavel = json.dumps(config, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
```

`sort_keys=True` é obrigatório: sem ele, a ordem de inserção vaza para o texto e o
prefixo muda entre processos.

## Exercício 4 — Medir a taxa de acerto

```python
def taxa_acerto(registros):
    entrada = sum(r["tokens_entrada"] for r in registros)
    cache = sum(r.get("tokens_cache_leitura", 0) for r in registros)
    return round(cache / entrada, 3) if entrada else 0.0
```

Referências de leitura: > 0,70 sessão longa e estável; 0,30-0,50 sessão curta;
< 0,20 investigar prefixo.

## Checklist de aceitação

- [ ] Diff de prompt executado em dois turnos
- [ ] Conteúdo volátil movido para o fim
- [ ] Serialização determinística aplicada
- [ ] Taxa de leitura de cache medida antes e depois
- [ ] Custo por sessão comparado

## Registro de aprendizagem

Enxugar o prefixo antes de estabilizá-lo é a armadilha clássica: você paga escrita de
cache de novo e pode terminar mais caro do que mantendo o prefixo maior e estável.
