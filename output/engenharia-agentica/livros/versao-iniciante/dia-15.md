# Dia 15 — Os segredos universais: o que sobrevive a toda troca de ferramenta

## Meta do dia

Separar o que é **invariante de engenharia** do que é **detalhe de produto** —
porque a próxima ferramenta que você usar vai ter nomes diferentes, e o que faz
sentido hoje continua fazendo se o princípio estiver no lugar certo.

## A ideia em uma frase

Invariantes descrevem relações entre as partes; modas descrevem superfícies de
produto — e só os primeiros sobrevivem ao próximo lançamento.

---

## A explicação simples

### O critério de classificação

- **Invariante** quando decorre de uma relação **estrutural**: modelo
  probabilístico gera incerteza; contexto tem custo; verificação precisa ser
  independente.
- **Moda** quando decorre de uma **escolha de produto**: nome do arquivo de
  configuração, formato do arquivo de regras, evento exato do hook, extensão
  da skill.

A consequência: invariantes podem ser **ensinados e transferidos**; modas
precisam ser **consultadas na documentação** da vez. Confundir os dois é o que
faz um time reescrever o harness inteiro a cada dois anos.

### Os dez invariantes

Cada um já apareceu neste livro, geralmente demonstrado por um sintoma. Nenhum
menciona produto — é isso que prova que é invariante:

1. **O modelo é probabilístico; a confiança vem do entorno.** Nada torna a
   geração determinística; o que se garante é que o erro não passe, com
   verificação independente do gerador.
2. **Verificação independente vale mais que capacidade bruta.** Um teste
   barato impede o erro caro — é o que permite usar modelos menores e rotear.
3. **Instrução estável, ferramenta estreita, contrato explícito.**
4. **Contexto é orçamento, não recipiente.** Custo por turno, atenção que
   degrada; quatro operações: escrever, selecionar, comprimir, isolar.
5. **Ordem das partes é arquitetura.** Estável primeiro, volátil por último —
   decorre de como cache de prefixo funciona.
6. **Nada é gratuito em paralelo.** Duplicação, conflito, disputa; isolamento
   resolve parte, contrato resolve o resto.
7. **Delegação vale pela razão entre o que se lê e o que se devolve.**
8. **Toda ação precisa ser atribuível.** Quem fez, em que branch, com qual
   veredito. Sem atribuição não há investigação, só especulação.
9. **Custa-se por resultado aceito, não por token.**
10. **Configuração é código: versionada, testada, datada.**

Compare com as modas: "use `settings.json`" é moda; "toda configuração que
importa está versionada" é invariante. "Chame no evento *antes da ferramenta*"
é moda; "intercepte **antes do dano**" é invariante.

### O critério de portabilidade

> **Escreva o conteúdo em invariantes e isole a moda em uma camada fina.**

Um documento curto de princípios (invariante, durável) + adaptadores finos por
produto (moda, descartável). Times que fazem o contrário — princípios
espalhados em configurações específicas — pagam migração completa a cada troca
de ferramenta.

### O teste final, barato e honesto

> **Troque o harness mantendo o modelo.** O que quebrar é moda mal isolada. O
> que continuar funcionando é invariante bem aplicado.

Custa uma tarde e é a medida mais honesta de maturidade de engenharia agêntica.

### Três segredos que enriquecem o dia

- **Contexto mínimo suficiente:** cada bloco na janela tem que mudar pelo menos
  uma decisão possível. A pergunta que você faz ao montar: **"qual decisão
  este bloco habilita?"** Se pode ser removido sem mudar nenhum resultado, é
  peso, não contexto.
- **Reprodutibilidade:** um resultado que não se reproduz é anedota. Quatro
  componentes: entrada (hash do estado do repo), configuração (arquivos
  ativos), plano (o **que foi executado**, não o planejado) e evidência (o
  que provou cada passo). O plano é o mais negligenciado.
- **Erro barato:** sistemas que aprendem cometem erros baratos — gate no
  momento da escrita, ambiente descartável e isolado, e recompensa por
  **evidência de falha** (quem reporta o que não funcionou facilita o
  diagnóstico; quem esconde a falha produz passivo três turnos depois).

---

## O exemplo real: a fábrica é a demonstração viva

A seção 6 do `AGENTS.md` é literalmente este capítulo aplicado. Ela chama os
invariantes de "fonte" e as modas de "links/junctions":

| Invariante (fonte) | Moda (derivado) |
|---|---|
| `AGENTS.md` — um único arquivo de regras | `CLAUDE.md`, `.cursor/rules/*.mdc`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md` — todos hardlinks para o mesmo |
| `.claude/` — origem de agents, commands, skills, mcp-servers | `agentic/*`, `.opencode/*`, `.agents/*` — junctions |
| `.mcp.json` (schema raiz) | `.cursor/mcp.json` (hardlink), `.vscode/mcp.json` e `opencode.json` (GERADOS por script, preservando decisões manuais) |
| `scripts/hooks/pre-commit` (versionado) | `.git/hooks/pre-commit` (copiado por `setup-links.ps1`/`.sh`) |

Quando um produto novo (uma IDE nova) entra: o que se escreve é um adaptador
(junction/script de sincronização) — não um novo conjunto de princípios. É a
economia de conhecimento que este capítulo vende, realidade no repositório.

E o teste de portabilidade já existe como ferramenta quotidiana: a fábrica
roda a mesma obra com harnesses diferentes (Claude Code, Codex, Cursor...), e
o critério de "funcionou" é o mesmo: os gates passam. O que degrada entre
harnesses é moda mal isolada; o que se mantém são os invariantes — e o AGENTS.md
documenta por quê.

Dois invariantes explícitos no AGENTS.md, em linguagem do dia 2:

- R16 = invariante 2: verificação independente (pytest) impede o commit
  vermelho — **bloqueante, por hook mecânico**.
- R17 = fronteira: escolha do operador nunca é terceirizada — "a escolha é
  sempre do operador" (decisão humana/irreversível + automação da verificação).

### Os dez em uma página, versão fábrica

1. Agente é probabilístico; o determinismo é construído na cabine (gates).
2. Estável e verdadeiro pertence ao prefixo (AGENTS.md = instrução estável).
3. Contexto suficiente: cada bloco muda uma decisão (RAG seleciona, não acumula).
4. Custo = tokens × turnos desperdiçados (leia seções 0.1 a 0.10 do AGENTS.md).
5. Gate na escrita custa fração do gate na entrega (Fase 2.5 antes da Fase 3).
6. Delega onde comprime; faça local onde expande (regra de derivação, Dia 13).
7. Paralelismo só se paga com isolamento (Dia 12) + atribuição.
8. Roteia por natureza (Dia 13), não por preferência de modelo.
9. Toda configuração não decidida será decidida por acidente (Dia 14).
10. Se não pode ser reproduzido, não é resultado (`relatorios/` + evidência).

---

## Mão na massa

### Tarefa 1 — escreva o documento de princípios

Curto, sem nome de produto, com consequência operacional em cada linha:

```markdown
# Princípios do harness (invariantes — sem dependência de produto)

1. Nenhuma geracao entra em uso sem verificacao independente do gerador.
2. Instrucao persistente: curta, estavel, sem dado volatil no inicio.
3. Ferramenta: superficie minima, esquema fechado, teto de saida.
4. Contexto: escrever, selecionar, isolar e so entao comprimir.
5. Ordem do prompt: estavel primeiro, volatil por ultimo.
6. Paralelismo apenas para tarefas independentes, com atribuicao por tarefa.
7. Delegacao com contrato: limite de retorno e procedencia obrigatoria.
8. Custo medido por resultado aceito, nunca por token.
9. Configuracao versionada, testada e com data de revisao.
10. Trocar de modelo deve ser parametro, nunca reescrita.
```

### Tarefa 2 — isole a moda em adaptadores

Toda dependência de produto, num arquivo por produto. Descartável, mas
estrutura durável:

```yaml
# adaptadores/produto-a.yaml
produto: "harness-a"
arquivo_instrucao: "AGENTS.md"
arquivo_config: ".agent/settings.json"
eventos:
  antes_da_ferramenta: "PreToolUse"
  fim_de_sessao: "SessionEnd"
```

```yaml
# adaptadores/produto-b.yaml
produto: "harness-b"
arquivo_instrucao: ".rules/instructions.md"
arquivo_config: ".harness/config.json"
eventos:
  antes_da_ferramenta: "tool.before"
  fim_de_sessao: "session.stop"
```

Note que **os princípios não aparecem aqui** — o adaptador responde "onde" e
"como", nunca "por quê".

### Tarefa 3 — rode o teste de portabilidade

```bash
#!/usr/bin/env bash
set -euo pipefail

# 1. Tarefa representativa no harness atual
python scripts/medir-tarefa.py --tarefa exemplo-01 --saida /tmp/antes.json

# 2. A MESMA tarefa no harness alternativo, mesmos arquivos de projeto
HARNESS=alternativo python scripts/medir-tarefa.py --tarefa exemplo-01 --saida /tmp/depois.json

# 3. O que degradou = dependencia de produto; o que se manteve = invariante
python scripts/comparar-tarefa.py /tmp/antes.json /tmp/depois.json
```

| Resultado | Leitura | Ação |
|---|---|---|
| Tudo se mantém | invariantes bem aplicados | trocar modelo é decisão de custo |
| Uma etapa degrada | moda mal isolada naquela etapa | mover para adaptador |
| Tudo degrada | princípios vivem dentro do produto | reescrever o documento de princípios |

### Tarefa 4 — monte o inventário de moda

```json
{
  "inventario_moda": [
    { "item": "nome do arquivo de config", "onde": "adaptadores/produto-a.yaml", "revisado": "2026-09-12" },
    { "item": "eventos de hook", "onde": "adaptadores/produto-a.yaml", "revisado": "2026-09-12" }
  ],
  "regra": "revisar a cada release do produto ou a cada 6 meses"
}
```

O inventário transforma "moda" em lista de trabalho — cada item com lugar e
data, nada invisível.

### Tarefa 5 — aplique o teste de retirada por bloco

Monte a janela fazendo uma pergunta por bloco: **qual decisão este bloco
habilita?** Saem os blocos cuja informação nunca é consultada; no lugar, um
ponteiro para recuperá-los quando precisar.

### Tarefa 6 — registre o plano COMO EXECUTADO

Não reproduza pelo que ficou escrito na intenção: capture entrada (hash),
configuração ativa, plano executado (ordem real dos passos) e evidência de
cada passo. Três artefatos pequenos transformam "aconteceu uma vez" em
"acontece sempre que eu quiser".

---

## Três regras que ficam com você

1. **Desconfie do resultado sem rastro.** Se não há evidência, não há
   conclusão.
2. **Aprenda invariantes, não produtos.** A velocidade de mudança é alta; um
   time que aprende produtos fica permanentemente atrás do lançamento.
3. **Deixe o próximo começar sabendo.** Nota de sessão não é diário — é o
   checklist do próximo que vai pilotar.

## Erros de julgamento deste dia

- Aprender produtos em vez de princípios (defasagem garantida).
- Princípios espalhados na configuração (cada migração vira reescrita).
- **Adaptador gordo**: se o adaptador decide comportamento, a moda voltou para
  dentro do princípio.
- Inventário de moda desatualizado — pior que não ter, dá falsa sensação de
  controle.
- Contexto acumulado sem critério ("pode ser útil").
- Guardar o resultado e descartar a evidência que o sustenta.

**Antipadrão observável:** quando ninguém consegue dizer qual versão do sistema
produziu um artefato em produção. Rastro não é burocracia de auditoria — é o
instrumento que permite melhorar sem adivinhar.

---

## Checklist do dia

- [ ] Documento de princípios escrito sem nome de produto (≤ 12 linhas).
- [ ] Itens de moda movidos para adaptador.
- [ ] Teste de portabilidade executado uma vez.
- [ ] Inventário de moda com data de revisão.
- [ ] Para cada bloco usado numa janela, sei qual decisão ele habilita.
- [ ] Um resultado do meu trabalho tem entrada, configuração, plano e evidência registrados.

## Para saber mais

- Seção 6 do `AGENTS.md` — a arquitetura fonte/derivado da fábrica como caso
  completo de invariante vs moda.
- `scripts/setup-links.ps1` / `setup-links.sh` — recriar as junctions após
  clone (o adaptador da fábrica).
- `relatorios/` — a convenção V5.2 que garante o rastro de cada sessão.

No Dia 16, a montagem final: **a arquitetura completa de uma esteira agêntica
auditável, do tema à entrega** — o sistema que constrói sistemas.