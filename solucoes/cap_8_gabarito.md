# Gabarito — Capítulo 8: Otimização de contexto

## Exercício 1 — Arquivo de estado da tarefa

Estrutura mínima aceita:

```markdown
# Estado da tarefa: <nome>

### Decisoes tomadas
- <decisao> — motivo

### Arquivos ja analisados
- <caminho> — <conclusao em 1 linha>

### Restricoes descobertas
- <restricao>

### Proximo passo
- <acao>
```

Se falta "Restricoes descobertas", a tarefa vai repetir erro já corrigido — é a seção
que mais evita retrabalho.

## Exercício 2 — Seleção com orçamento

```python
def selecionar(consulta, arquivos, orcamento_linhas=120):
    termos = [t.lower() for t in consulta.split() if len(t) > 3]
    achados = []
    for caminho in arquivos:
        linhas = caminho.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, linha in enumerate(linhas):
            pontos = sum(linha.lower().count(t) for t in termos)
            if pontos:
                achados.append((pontos, caminho, i, linha.strip()))
    achados.sort(key=lambda x: -x[0])
    return achados[:orcamento_linhas]
```

Critério: o orçamento precisa ser parâmetro, nunca constante implícita. Seleção sem
teto vira carregamento.

## Exercício 3 — Política de compactação

```yaml
politica_compactacao:
  gatilho: "contexto acima de 70% da janela"
  preservar_sempre: ["decisoes", "restricoes", "caminhos e simbolos", "falhas abertas"]
  descartar_primeiro: ["conversa intermediaria", "resultado ja consumido"]
  registrar: "gravar resumo no arquivo de estado antes de compactar"
```

Nota obrigatória: comprimir sem persistir antes é perda definitiva.

## Exercício 4 — Contrato de isolamento

```json
{
  "limite_leitura": "sem restricao",
  "limite_retorno_tokens": 250,
  "formato_retorno": "lista: caminho:linha — motivo em ate 12 palavras",
  "proibido": ["colar trechos maiores que 3 linhas"]
}
```

## Checklist de aceitação

- [ ] Arquivo de estado criado e atualizado
- [ ] Seleção com orçamento explícito
- [ ] Varredura pesada isolada em subagente
- [ ] Política de compactação com preservação declarada
- [ ] Ordem de preferência respeitada (escrever → selecionar → isolar → comprimir)

## Registro de aprendizagem

A ordem importa porque comprimir é a única operação que perde informação. Quem começa
por comprimir nunca descobre que poderia ter selecionado.
