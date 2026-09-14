# Dia 8 — Otimização de contexto: escrever, selecionar, comprimir, isolar

## Meta do dia

Deixar de tratar economia de contexto **caso a caso** e aprender o método por
trás de todas as decisões dos Dias 5–7: **quatro operações** — escrever,
selecionar, comprimir, isolar — ordenadas da mais barata à mais cara, e
aplicáveis a qualquer projeto.

## A ideia em uma frase

Otimizar contexto é **escolher uma das quatro operações antes de colocar
qualquer coisa na janela** — e nunca confundir contexto com memória.

---

## A explicação simples

### As quatro operações, com um nome para cada

| Operação | O que faz | Custo |
|---|---|---|
| **Escrever** | tirar da janela o que não precisa ser relido e guardar em arquivo | o mais barato e o mais ignorado |
| **Selecionar** | trazer para a janela **apenas o trecho** que responde à pergunta | barato, proporcional ao repo |
| **Comprimir** | reduzir o volume do que já está na janela | **aceita perda** — a única que perde informação |
| **Isolar** | processar em outro contexto (subagente) e trazer só o resultado | o mais poderoso e o mais subutilizado |

### A ordem de preferência não é estética, é econômica

1. **Escreva** o que não precisa ficar (decisões, arquivos já analisados).
2. **Selecione** o mínimo necessário.
3. **Isole** quando a desproporção leitura/conclusão for grande.
4. **Comprima** por último — porque comprimir perde informação, e perda é
   irreversível.

O mnemônico do fluxo de decisão (o caminho do diagrama do capítulo):

```
Conteúdo candidato → será relido depois?  SIM → ESCREVER
                  → pode ser recuperado por busca?  SIM → SELECIONAR
                  → leitura grande com conclusão pequena?  SIM → ISOLAR
                  → senão → COMPRIMIR (com perda declarada)
```

### O diagnóstico mais importante do capítulo

**A maior parte dos problemas de contexto é problema de alocação entre
camadas**, não de tamanho de janela. Um harness maduro tem pelo menos quatro
camadas onde o contexto pode viver:

| Camada | Custo | Persistência |
|---|---|---|
| Janela (o que está visível agora) | caro | volátil |
| Estado em arquivo (`decisoes.md`) | barato | persistente |
| Índice consultável (grafo, busca) | barato | seletivo |
| Memória de longo prazo entre sessões | barato | durável |

"Contexto poluído" quase sempre é informação que **deveria estar em arquivo,
mas está na janela** — ou que deveria estar no índice, mas é carregada inteira.
A cura começa perguntando "onde isso deveria morar?", não "como enxugar?".

### Contexto não é memória

- **Memória** é o que persiste entre sessões.
- **Contexto** é o que está visível agora.

Um agente com ótima memória e contexto poluído decide mal. Um agente com
memória pobre e contexto limpo decide bem e esquece rápido. O equilíbrio
correto é **memória externa generosa, contexto enxuto**.

### Quando contexto grande é inevitável

Refatoração ampla, migração de framework, auditoria de segurança: tarefas que
precisam de visão global **não cabem numa janela**. Nesses casos, nada de
cortar às cegas — **fatia**: divida a tarefa em unidades que caibam em janelas
separadas, com um **contrato explícito** entre elas. É o princípio que
reaparece no Dia 11 (subagentes) e no Dia 12 (worktrees).

---

## O exemplo real: as quatro operações na fábrica

O `proj_fabrica-de-livros` usa as quatro operações sem se dar conta — o que
prova que são o molde natural de um harness maduro.

### Escrever = o RTK-SCRATCHPAD e os relatórios

- `RTK-SCRATCHPAD.md` (memória entre sessões): aprendizado que custou
  tentativas é **gravado em arquivo** e sobrevive ao fim da sessão. O critério
  de promoção deste dia vale exatamente: "se levou mais de duas tentativas ou
  tocou algo não óbvio, vira nota."
- `relatorios/` (notas de sessão, convenção V5.2): cada sessão encerra com um
  relatório MD+PDF — o que foi decidido, o que ficou em aberto, o próximo
  passo. É a lista de verificação do **próximo piloto**, não um diário.

Ambos são "escrever" puro: a informação que será necessária de novo vive em
arquivo, não no histórico.

### Selecionar = o dossiê indexado e o grafo

- `indexar-dossie.py` (RAG): na Fase 1, a pesquisa vira um **índice
  consultável**. O redator não lê a web de novo — **recupera o trecho** que
  responde à dúvida.
- A skill `lean-ctx` e a regra "Busca via Grafo: usar `.code-review-graph`
  antes de tools de leitura/busca": hierarquia de recuperação — símbolo antes
  de assinatura, assinatura antes de corpo, corpo antes de arquivo inteiro.

### Comprimir = headroom com fidelidade

- `headroom` (3 topo + 4 fim, >7 linhas) com a **exceção deliberada** da regra
  8: `output/**` e dados de obra nunca comprimem. É a política de compactação
  com **lista de preservação** — o essencial (restrição, decisão, evidência)
  nunca é descartado; o descartável (log, miolo de build) é sempre.

A hierarquia de classes que o capítulo usa — e a fábrica pratica:

| Classe de informação | Destino | Nunca fazer |
|---|---|---|
| Restrição e proibição | estado, íntegro | comprimir junto com dados |
| Decisão tomada | uma linha no estado | repetir o raciocínio completo |
| Dado bruto consultado | ponteiro reproduzível | manter o conteúdo na janela |
| Evidência de validação | fim da janela, preservada | descartar antes da entrega |
| Convenção do projeto | prefixo estável | reordenar a cada edição |

### Isolar = os subagentes do fluxo

- Regra 4 do AGENTS.md: "**Delegação Cavecrew: subagentes comprimidos** para
  buscas/edições extensas". O subagente lê bastante e **devolve resumo**.
- Na Fase 2, cada capítulo é manufaturado por um **subagente-redator** com
  contexto próprio; o orquestrador nunca paga as leituras internas do
  subagente — só o resultado.
- Na Fase 2.5, o `subagente-revisor-tecnico` corrige em paralelo, isolado.

A regra de ouro do isolamento, que a fábrica pratica: **isolamento só funciona
com contrato** — papel, pergunta, teto de retorno (250 tokens), formato de
retorno e proibições. Sem contrato, o subagente devolve um texto longo e o
ganho morre.

### Fatiar com contrato = o pool de capítulos

Quando o todo é grande demais (uma obra inteira), a fábrica **fatia**: 16
capítulos, cada um uma unidade que cabe numa janela, com contrato explícito
(EITA + estratégia + validação) entre elas. Não corta às cegas — fatia com
fronteira definida. É o mesmo princípio dos worktrees do Dia 12.

---

## Mão na massa

### Tarefa 1 — o arquivo de estado da tarefa

Toda tarefa longa (mais de um punhado de turnos) merece um arquivo de estado.
Ele é a memória externa que substitui o histórico:

```markdown
# Estado da tarefa: <nome da tarefa>

### Decisoes tomadas
- <o que foi decidido e o motivo>

### Arquivos ja analisados
- <caminho> — <o que extraiu de cada um>

### Restricoes descobertas
- <o que nao pode ser feito / contratos a respeitar>

### Proximo passo
- <a primeira acao da proxima sessao>
```

Quando a sessão morrer ou o contexto estourar, **este arquivo é o contexto que
sobrevive.**

### Tarefa 2 — recuperação por níveis (não leia, procure)

Escolha um símbolo do seu projeto e responda uma pergunta sobre ele percorrendo
a hierarquia, comparando o consumo:

1. **Busca** do símbolo (definição e referências) — custa frações.
2. **Assinatura** — nome, parâmetros e tipos dizem o que a unidade faz.
3. **Janela** — algumas dezenas de linhas em volta da linha localizada.
4. **Índice do projeto**, se existir — "quem usa isso" sem abrir arquivo.

A regra: **cada nível só é aberto quando o anterior foi insuficiente para
decidir.**

### Tarefa 3 — política de compactação com lista de preservação

Escreva, em uma página, o que **nunca** comprime e o que **sempre** é
descartável:

```yaml
politica_compactacao:
  gatilho: "contexto acima de 70% da janela"
  preservar_sempre:
    - "decisoes tomadas e seu motivo"
    - "restricoes e contratos declarados"
    - "caminhos de arquivo e nomes de simbolos"
    - "falhas nao resolvidas"
  descartar_primeiro:
    - "conversa intermediaria de ajuste"
    - "resultados de ferramenta ja consumidos"
    - "repeticoes de leitura"
  registrar: "gravar resumo no arquivo de estado antes de compactar"
```

O último campo é o mais importante: **compactar sem persistir é perder.**
Grave primeiro, compacte depois.

### Tarefa 4 — contrato de isolamento (um pedaço de JSON)

Antes de delegar qualquer varredura pesada, escreva o contrato:

```json
{
  "papel": "investigador-de-codigo",
  "pergunta": "<a pergunta objetiva>",
  "limite_leitura": "sem restricao",
  "limite_retorno_tokens": 250,
  "formato_retorno": "lista: caminho:linha — motivo em ate 12 palavras",
  "proibido": ["colar trechos maiores que 3 linhas", "sugerir implementacao"]
}
```

Sem teto de retorno e sem formato, o isolamento se transforma em
carregamento disfarçado.

### Tarefa 5 — rastro de descarte

Sempre que remover um bloco da janela, registre três coisas: **o que saiu, por
que saiu, como recuperar.** Isso transforma o contexto em instrumento com
histórico — e impede que um resultado errado vire arqueologia ("quem jogou
essa informação fora?"). Documente evidência de validação como a última coisa
a sair.

### Tarefa 6 — orçamento de janela por fase

A janela é finita; gastá-la sem plano é aceitar que a fase de **decisão**
acontecerá com contexto poluído. Um plano para quatro fases:

| Fase | Participação da janela | Conteúdo dominante |
|---|---|---|
| Compreender | 40% | instruções estáveis, estado, restrições |
| Investigar | 30% | resultados de busca, já comprimidos |
| Decidir | 20% | síntese, opções, critério |
| Executar e verificar | 10% | diff, saída de teste, evidência |

O estável fica no começo (e sobrevive a tarefa inteira — como você aprendeu
no Dia 6); o volumoso e descartável fica no meio (e é limpo cedo); o que
**prova** o resultado fica no fim (e é o último a ser comprimido). Uma sessão
que começa despejando 200 arquivos não tem plano de contexto — tem só
esperança.

---

## Três regras que ficam com você

1. **Recupere por nível.** Símbolo antes de assinatura, assinatura antes de
   corpo, corpo antes de arquivo inteiro.
2. **Registre o descarte.** O que saiu da janela precisa deixar rastro de como
   voltar.
3. **Proteja o que prova.** O que sustenta a afirmação de conclusão é o
   último a ser comprimido.

## Erros de julgamento deste dia

- **Comprimir por volume, não por função** — a tesoura vai onde ocupa mais
  espaço e corta a restrição (curta) junto com o log (longo e descartável). O
  desvio nº 1 da prática: comprima por função.
- **Leitura integral como primeiro reflexo** — abrir o arquivo inteiro para
  responder pergunta de uma linha é o maior consumidor isolado da janela.
- **Selecionar sem teto** — recuperação que devolve tudo é carregamento
  disfarçado.
- **Isolar tarefa que precisa de contexto compartilhado** — o subagente decide
  sem ver o todo e volta com conclusão desalinhada.
- **Fatiar sem contrato** — dividir a tarefa e não definir o que cada fatia
  entrega.
- **Descartar evidência de validação por ser "detalhe técnico"** — é exatamente
  o que sustenta a conclusão.

**Antipadrão observável:** o agente relembra, trinta turnos depois, um dado
que já tinha recebido. Contexto foi comprimido de forma cega — perdeu-se a
restrição e manteve-se a tabela. O certo é o inverso: mantém-se a restrição,
descarta-se a tabela.

---

## Checklist do dia

- [ ] Explico as 4 operações na ordem de preferência (escrever → selecionar →
      isolar → comprimir).
- [ ] Criei o arquivo de estado da tarefa e o atualizo em checkpoints.
- [ ] Recuperei um símbolo por níveis e comparei consumo com leitura integral.
- [ ] Escrevi a política de compactação com lista de preservação.
- [ ] Deleguei uma varredura pesada com contrato (teto de retorno + formato).
- [ ] Registrei um descarte com rastro (o que, por que, como recuperar).
- [ ] Sei dizer qual camada (janela/arquivo/índice/memória) cada informação
      deveria ocupar.

## Para saber mais

- `RTK-SCRATCHPAD.md` — a memória de longo prazo da fábrica: o "escrever" que
  sobrevive à sessão.
- `relatorios/` — as notas de sessão (convenção V5.2) que fecham todo dia de
  trabalho.
- `AGENTS.md` regra 4 (delegação cavecrew) e regra 9 (busca via grafo) — o
  "isolar" e o "selecionar" como política de empresa.

No Dia 9, você sai do contexto e entra na esteira: **scripts e gates** que
fazem o trabalho se verificar sozinho — para o agente deixar de ser a última
linha de defesa.