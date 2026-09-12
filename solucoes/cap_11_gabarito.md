# Gabarito — Capítulo 11: Agents e subagentes

## Exercício 1 — Contrato de delegação

```json
{
  "papel": "investigador",
  "pergunta": "quais modulos consomem o contrato de /login?",
  "contexto_necessario": ["contrato atual de /login", "restricao: clientes moveis dependem do formato"],
  "limite_retorno_tokens": 250,
  "formato_retorno": "tabela: caminho:linha | tipo | risco",
  "obrigatorio": ["caminho e linha para cada afirmacao"],
  "proibido": ["colar trechos maiores que 3 linhas", "sugerir implementacao"]
}
```

Os três campos não negociáveis: `contexto_necessario` (o subagente não sabe o que o pai
sabe), `limite_retorno_tokens` (sem limite, a economia desaparece) e `obrigatorio`
(procedência conferível).

## Exercício 2 — Razão de compressão

```python
def razao_compressao(registros):
    lidos = sum(r["tokens_lidos"] for r in registros)
    devolvidos = sum(r["tokens_devolvidos"] for r in registros)
    if not devolvidos:
        return {"razao": float("inf"), "veredito": "vale"}
    razao = lidos / devolvidos
    return {"razao": round(razao, 1), "veredito": "vale" if razao >= 8 else "nao compensa"}
```

Referência: > 10 excelente; 5-10 compensa; < 3 não compensa.

## Exercício 3 — Procedência conferível

```bash
sed -n '142p' app/routes/legacy.py | grep -n "login" && echo "[OK] procedencia confirmada"
```

Amostragem de 1 item por retorno é suficiente para detectar subagente que inventa
referências.

## Exercício 4 — Serial ou paralelo

| Situação | Decisão |
|---|---|
| 3 varreduras independentes | paralelo |
| tarefas que compartilham achados | serial com estado em arquivo |
| escrita longa coerente | sem delegação |
| 12 artefatos independentes | paralelo com fan-out |

## Checklist de aceitação

- [ ] Contrato escrito com contexto, limite e proibições
- [ ] Retorno acima do limite tratado como erro
- [ ] Razão de compressão registrada
- [ ] Procedência conferida por amostragem
- [ ] Caso de delegação revertido por não compensar documentado

## Registro de aprendizagem

Delegar escrita longa é o erro silencioso mais comum: o retorno parece bom e o
documento final perde coerência, porque nenhum subagente viu o todo.
