# Gabarito — Capítulo 7: Economia severa de tokens

## Exercício 1 — Hierarquia de leitura

Resposta esperada na instrução persistente:

```markdown
### Ordem obrigatoria de leitura
1. Declarar o alvo antes de abrir qualquer arquivo.
2. Buscar por padrao para localizar a linha.
3. Ler apenas o intervalo necessario.
4. Abrir arquivo inteiro somente com menos de 200 linhas.
```

Erro comum: escrever "evite ler arquivos grandes". Regra sem procedimento não muda
comportamento — a hierarquia precisa nomear as operações em ordem.

## Exercício 2 — Teto em toda ferramenta

```python
def teto(texto, primeiras=3, ultimas=4, limite=200):
    linhas = texto.splitlines()
    if len(linhas) <= limite:
        return texto
    omitidas = len(linhas) - primeiras - ultimas
    return "\n".join(linhas[:primeiras] + [f"... [{omitidas} linhas omitidas] ..."] + linhas[-ultimas:])
```

Critério: nunca omitir o cabeçalho do erro. Se o erro vem nas primeiras 3 linhas,
`primeiras=3` é o mínimo seguro.

## Exercício 3 — Limpeza de resultado consumido

```json
{
  "politica_resultado_ferramenta": {
    "apos_consumo": "substituir por resumo de 1 linha",
    "exemplo": "[resultado de run_tests: 34 passaram, 0 falharam]"
  }
}
```

Regra de segurança: manter integral o resultado que ainda será referenciado dentro da
mesma tarefa (ex.: diff que será commitado).

## Exercício 4 — Orçamento por fase

```yaml
orcamento_por_fase:
  descoberta: { tokens_saida_alvo: 800, regra: "listar achados" }
  geracao: { tokens_saida_alvo: 6000, regra: "sem preambulo" }
  verificacao: { tokens_saida_alvo: 300, regra: "veredito e localizacao" }
```

## Checklist de aceitação

- [ ] Hierarquia de leitura na instrução persistente
- [ ] Teto aplicado a todas as ferramentas de saída textual
- [ ] Limpeza de resultado consumido ativa
- [ ] Orçamento por fase declarado
- [ ] Comparação antes/depois de tokens por entrega

## Registro de aprendizagem

A maior economia raramente está na compressão: está em não buscar. Um harness que
busca antes de abrir reduz a entrada em uma ordem de magnitude sem perder informação
acionável.
