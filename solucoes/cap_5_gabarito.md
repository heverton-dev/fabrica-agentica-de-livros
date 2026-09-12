# Gabarito — Capítulo 5: Turnos agênticos

## Exercício 1 — Registro por turno

O registro mínimo precisa responder a quatro perguntas: quanto entrou, quanto saiu,
quanto veio de cache e qual ferramenta foi usada.

```json
{
  "sessao": "instrumentacao-turnos",
  "turno": 1,
  "tokens_entrada": 18420,
  "tokens_saida": 640,
  "tokens_cache_leitura": 0,
  "ferramenta": "run_tests",
  "linhas_resultado": 12,
  "duracao_s": 6.1,
  "custo_estimado_usd": 0.0649
}
```

Erro comum: registrar apenas o custo total. Sem `tokens_cache_leitura` separado, não é
possível saber se o prefixo está sendo reaproveitado.

## Exercício 2 — Teto em saída de ferramenta

A compressão correta preserva cabeça e cauda e declara quantas linhas foram omitidas.

```python
def comprimir_saida(texto, primeiras=3, ultimas=4, limite_linhas=200):
    linhas = texto.splitlines()
    if len(linhas) <= limite_linhas:
        return texto
    omitidas = len(linhas) - primeiras - ultimas
    return "\n".join(linhas[:primeiras] + [f"... [{omitidas} linhas omitidas] ..."] + linhas[-ultimas:])
```

Aceita-se também reduzir a verbosidade na origem (`pytest -q`, `git log --oneline`)
em vez de comprimir depois: atacar a fonte custa menos do que tratar o sintoma.

## Exercício 3 — Critério de pronto

Um critério de pronto verificável nomeia o comando, o resultado esperado e o limite.

```yaml
tarefa: corrigir-bug-1042
criterio_de_pronto:
  - "python -m pytest -q termina com 0 falhas"
  - "existe teste novo que falha antes da correcao"
  - "nenhum arquivo fora de app/ foi alterado"
limite_de_tentativas: 3
ao_atingir_limite: "parar e reportar a ultima falha com o comando exato"
```

Critério vago ("código funcionando") é a causa mais frequente de sessões longas.

## Checklist de aceitação

- [ ] Um JSON por turno, com `tokens_cache_leitura`
- [ ] Script de resumo calculando custo por sessão e proporção de cache
- [ ] Tetos aplicados a todas as ferramentas que devolvem texto
- [ ] Critério de pronto escrito antes da tarefa, com limite de tentativas
- [ ] Comparação antes/depois do custo por tarefa

## Registro de aprendizagem

Se a proporção de cache ficou próxima de zero mesmo com o prefixo estável, verifique
se o harness está enviando o conteúdo variável antes do estável — a ordem das partes
é o assunto do Capítulo 6.
