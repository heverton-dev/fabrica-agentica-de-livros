# Dia 12 — Orquestração: worktrees, paralelismo e o ambiente de agentes

## Meta do dia

Subir o nível do Dia 11: **várias tarefas ao mesmo tempo, cada uma em um
diretório de trabalho próprio** — usando **worktrees** de git — e reconciliar
o resultado sem corromper o estado.

## A ideia em uma frase

Para executar em paralelo, o agente precisa de **isolamento de estado**; a
worktree dá isso a custo de uma pasta — não de um repositório.

---

## A explicação simples

### O que é uma worktree

Trabalhar em paralelo significa **onde uma mudança acontece, a outra não
interfere**. Isso precisa valer em três níveis:

- **memória de conversa** → contexto isolado (Dia 11);
- **arquivos** → área de trabalho isolada (este dia);
- **git** → branch, index e HEAD isolados (este dia).

A worktree resolve os dois últimos:

> **Worktree = um diretório adicional ligado ao MESMO repositório git, com
> branch, index e estado de trabalho próprios.**

Sem precisar clonar o repositório nem trocar de máquina, cada tarefa ganha um
cantinho com checkout próprio.

### Os níveis de isolamento

| Nível | Ferramenta | Proteção |
|---|---|---|
| Diretório | pasta de trabalho dedicada | arquivos de uma tarefa não colidem com os da outra |
| Git | worktree | branch/index/HEAD por tarefa |
| Processo | sandbox / branch de processo | onde diretório e git não bastam |
| Memória | contexto isolado (Dia 11) | leituras não poluem o orquestrador |

**Isolamento mínimo:** diretório + git. Regra prática que você leva deste dia:
**superfícies concorrentes de uma TAREFA não ficam no mesmo diretório de
trabalho.**

### Por que uma worktree e não um clone?

1. **Custo:** clone duplica metadados e exige cruzar remoto a cada `sync`;
   worktree é um diretório novo apontando para o mesmo `.git`.
2. **Identidade:** clone é um repositório "outro"; worktree é o mesmo
   repositório em outro lugar.
3. **Sync:** na worktree a reconciliação volta **direto** para o repositório
   principal; no clone tudo volta por `push`/`pull`, com risco de divergir.
4. **Race de git:** dois comandos git simultâneos **no mesmo diretório**
   corrompem o `index.lock`; nas worktrees, cada uma tem o seu.

### O commit granular como padrão de reconciliação

Worktrees paralelas **reúnem trabalho em um lugar** (no repositório
principal), não **misturam trabalhos** A e B no mesmo commit. Cada mudança
validada entra em um commit próprio. Três ideias que importam:

- o momento de integração é quando a **review** termina, não quando o código
  "roda";
- cada worktree integra **incrementalmente**, por unidade de trabalho;
- conflito é problema de **design de tarefas** (arquivos compartilhados), não
  só de rotina de git.

---

## O exemplo real: worktrees e a fábrica

No ambiente de trabalho com worktrees (o mesmo em que este material é
produzido — o sistema de desenvolvimento de agentes **Orca ADE**), o
orquestrador:

1. **Cria uma worktree** para a tarefa — branch, HEAD e diretório próprios.
2. **Provisa as credenciais** de que a tarefa precisa, sem expô-las.
3. **Instala o agente e as skills** dentro da worktree.
4. Roda teste, transformação de código e geração custosa em **sandboxes
   próprias**.
5. Garante que trabalho em worktree paralela **não apaga** o que outra
   construiu ao mesmo tempo — o compromisso da reconciliação: o que uma
   isolada construiu não é descartado pela outra.

O corolário honesto: o isolamento funciona **se a tarefa realmente puder ser
separada**. Duas mudanças no mesmo arquivo VÃO gerar conflito, por melhor que
seja o setup — é problema de **design de tarefas**, e a mitigação mais barata
é **não dividir arquivos compartilhados**.

No `proj_fabrica-de-livros`, o equivalente do orquestrador é o
`pool-capitulos.py` com `--plano --lote 4`: cada capítulo é uma tarefa que só
escreve no **seu** arquivo. Cada redator trabalha num arquivo que nenhum outro
toca — é isso que permite 4 em paralelo sem conflito. O oposto — duas tarefas
escrevendo em `config_obra.json` ao mesmo tempo — seria conflito de
reconciliação na certa.

E o AGENTS.md declara os "ambientes de trabalho" da fábrica (as raízes por
tipo em `output/<obra>/` e as ferramentas em `scripts/`) como fronteiras: cada
tarefa escreve na sua raiz, nunca na do vizinho.

---

## Mão na massa

### Tarefa 1 — crie a worktree

```bash
# a partir do repositório principal
git worktree add ../b-worktarefa-tacadaA -b feat/tarefa-a
```

### Tarefa 2 — saiba o que você tem com um comando

```bash
git worktree list
```

Quanto mais worktrees abertas sem integração, maior a divergência — saber
quantas existem é o primeiro passo para não monopolizá-las.

### Tarefa 3 — combine com o contexto isolado do Dia 11

1. Cada trabalho paralelo é um **subagente** (contexto, Dia 11).
2. Cada subagente escreve em **sua worktree** (estado, este dia).
3. O orquestrador espera os retornos e **integra um a um**.

### Tarefa 4 — reconstrua o build de cada worktree ANTES de integrar

```bash
# dentro da worktree
cd ../b-worktarefa-tacadaA
python -m pytest -q  # execução na própria worktree
```

Os gates do Dia 9 precisam rodar **dentro** da worktree, não no repositório
principal — senão você valida um estoque e integra outro.

### Tarefa 5 — integre um por vez, por commit granular

```bash
# no repositório principal, a partir da worktree A
git checkout feat/tarefa-a && git rebase main
git checkout main && git merge --no-ff feat/tarefa-a
```

Integração é revisão do trabalho A e depois do trabalho B — nunca mistura de
A+B no mesmo commit.

### Tabela de decisão: quando paralelizar

| Situação | Veredito |
|---|---|
| Tarefas independentes, arquivos próprios | paralelo com worktrees |
| Tarefas que tocam o mesmo arquivo | sequencial, ou redesenhe a divisão |
| Resultado depende de decisão anterior | sequencial, com gate entre etapas |
| Custo de sincronizar > ganho | sequencial |

**A regra de ouro:** paralelismo só se paga quando o ganho supera o custo de
sincronizar — e o ganho só aparece onde existe isolamento.

---

## Três regras que ficam com você

1. **Toda tarefa concorrente tem diretório próprio.** Sem isso, paralelismo é
   corrupção de estado.
2. **Valide dentro da worktree, integre por commit granular.** Um trabalho de
   cada vez, e só o que passou no gate entra.
3. **Desenhe tarefas para não compartilhar arquivo.** Conflito é design, não
   azar.

## Erros de julgamento deste dia

- Duas tarefas mexendo no mesmo arquivo ao mesmo tempo (conflito garantido).
- Dois comandos git no mesmo diretório — travam no `index.lock`.
- Integração em lote adiada — quanto mais tempo a worktree fica parada, maior
  a divergência.
- Build rodado fora da worktree — o resultado do teste não é fidedigno.
- Paralelizar sem contexto isolado (Dia 11) — leitura duplicada no
  orquestrador.

**Antipadrão observável:** sem isolamento, paralelismo não é agilidade, é
passeio de cavalos soltos — com isolamento, você escala sem tornar o
repositório um campo de batalha.

---

## Checklist do dia

- [ ] Sei dizer por que uma worktree custa menos que um clone.
- [ ] Diferencio os 4 níveis de isolamento (dir, git, processo, memória).
- [ ] Escrevo o comando que cria e o que lista worktrees.
- [ ] Design de tarefas: cada tarefa paralela escreve em arquivos próprios.
- [ ] Build/validação executada **dentro** de cada worktree antes da integração.
- [ ] Integração por commit granular, uma tarefa por vez.
- [ ] Identifiquei um arquivo compartilhado que eu não dividiria em paralelo.

## Para saber mais

- `pool-capitulos.py` da fábrica — o fan-out por lote com arquivos exclusivos.
- `git worktree` (referência oficial do git) — `list`/`add`/`remove`.
- A skill de orquestração Orca ADE — as worktrees como "mesas de trabalho
  isoladas".

No Dia 13, o componente final da operação: **escolher qual modelo de
linguagem para cada etapa — sem regra universal, mas com critério.**