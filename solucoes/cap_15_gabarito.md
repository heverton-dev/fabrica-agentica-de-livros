# Gabarito — Capítulo 15: Segredos universais

## Exercício 1 — Princípios sem nome de produto

Resposta aceita (até doze linhas, sem nenhum nome de ferramenta):

```markdown
1. Nenhuma geracao entra em uso sem verificacao independente do gerador.
2. Instrucao persistente curta, estavel e sem dado volatil no inicio.
3. Ferramenta com superficie minima, esquema fechado e teto de saida.
4. Contexto: escrever, selecionar, isolar e so entao comprimir.
5. Ordem do prompt: estavel primeiro, volatil por ultimo.
6. Paralelismo apenas para tarefas independentes, com atribuicao.
7. Delegacao com limite de retorno e procedencia obrigatoria.
8. Custo medido por resultado aceito.
9. Configuracao versionada, testada e datada.
10. Trocar de modelo e parametro, nunca reescrita.
```

Critério de reprovação: qualquer linha que cite nome de arquivo, nome de evento ou
sintaxe específica de um produto. Isso é moda, não princípio.

## Exercício 2 — Adaptador por produto

```yaml
produto: "harness-x"
arquivo_instrucao: "AGENTS.md"
arquivo_config: ".agent/settings.json"
eventos:
  antes_da_ferramenta: "PreToolUse"
  depois_da_ferramenta: "PostToolUse"
```

Se o adaptador contém regra de comportamento (e não apenas "onde" e "como"), a moda
vazou para dentro do princípio.

## Exercício 3 — Teste de portabilidade

```bash
python scripts/medir-tarefa.py --tarefa exemplo-01 --saida /tmp/antes.json
HARNESS=alternativo python scripts/medir-tarefa.py --tarefa exemplo-01 --saida /tmp/depois.json
python scripts/comparar-tarefa.py /tmp/antes.json /tmp/depois.json
```

Leitura: degradação localizada indica moda mal isolada; degradação total indica
princípios presos ao produto anterior.

## Checklist de aceitação

- [ ] Documento de princípios sem nome de produto
- [ ] Adaptador por produto criado
- [ ] Item de moda movido para o adaptador
- [ ] Teste de portabilidade executado
- [ ] Inventário de moda com data de revisão

## Registro de aprendizagem

O tempo de migração entre harnesses é a métrica mais honesta de maturidade: dias
indicam invariantes bem isolados; semanas indicam princípios escondidos na configuração.
