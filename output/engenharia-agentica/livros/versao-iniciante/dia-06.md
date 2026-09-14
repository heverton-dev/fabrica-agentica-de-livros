# Dia 6 — Cache hit: o desconto que existe, e que uma linha instável destrói

## Meta do dia

Entender o **cache de prefixo** — o maior desconto disponível para agentes de
sessão longa — e aprender as três habilidades que fazem você ter direito a ele:
auditar estabilidade, ordenar as partes do prompt e medir a taxa de acerto.

## A ideia em uma frase

Cache hit é **arquitetura de prompt**, não configuração: quem coloca conteúdo
volátil no início do prompt paga preço cheio para sempre.

---

## A explicação simples

### Como o modelo cobra, na prática

Processar um prompt tem um custo por token. Mas o provedor reutiliza o
trabalho: se você reenviar **a mesma sequência de tokens** de novo, o modelo
não recalcula o começo — ele **lê do cache**.

Na prática existem três preços:

| Tipo de token | Custo relativo |
|---|---|
| Escrita de cache | pouco acima do token comum (você paga o armazenamento) |
| Leitura de cache | **fração pequena** do token comum |
| Token comum | o que não foi cacheado |

Um prefixo de 40 mil tokens lido inteiro de cache a cada turno custa uma
fração do mesmo prefixo pago por inteiro. A economia é de uma **ordem de
grandeza** — e durante toda a sessão.

### A condição é única e absoluta

**O prefixo precisa ser idêntico.** Não "parecido" — byte a byte, do início até
o ponto em que muda. Um único caractere diferente no começo invalida o cache
de tudo o que vem depois — inclusive dos 39.999 tokens estáveis.

Por isso a frase do dia: **a ordem das partes do prompt é uma decisão de
arquitetura, não de estilo.** A regra é uma só:

> Do **mais estável** para o **mais volátil**.

Estável primeiro (instrução persistente, ferramentas, skills, base de
conhecimento), volátil por último (histórico, resultado de ferramenta,
instrução nova do turno).

### Por que a ordem funciona

O cache é um armazenamento de **prefixos**. Se um token perto do início muda,
todo o estado a partir dele é descartado. Um único token volátil no topo joga
fora a reutilização de milhares de tokens estáveis.

O metro (os invalidadores clássicos, em ordem de frequência):

1. **Data ou timestamp no topo** do prompt de sistema.
2. Lista de ferramentas montada em ordem não determinística (ex.: um `set()`).
3. JSON serializado sem ordem estável de chaves.
4. Nome do usuário ou caminho do diretório injetado no topo.
5. Contadores ("tarefa 3 de 12") na instrução persistente.
6. Conteúdo de arquivo colado **antes** da instrução.

Todos parecem inofensivos. Todos são invisíveis no resultado. E todos mudam o
custo em uma ordem de magnitude.

### A sutileza que engana todo mundo

**Reduzir tokens nem sempre reduz custo.** Se você encurta o prefixo estável e
o torna diferente do que já estava cacheado, paga escrita de cache de novo —
e sai mais caro do que manter um prefixo maior e estável.

A métrica certa não é "tamanho do prompt": é **proporção de leitura de cache**.
Um prefixo grande lido integralmente de cache pode custar menos do que um
prefixo menor pago do zero a cada turno.

> **O alvo é a taxa de leitura de cache — não o tamanho do prompt.**

### O cache expira

Cache tem prazo de validade (por tempo ou por volume). O desconto some sem
aviso. Sem medir `tokens_cache_leitura` por sessão, você não sabe se está
economizando — ou apenas acreditando que está.

---

## O exemplo real: o AGENTS.md como prefixo estável

A fábrica aplica este dia literalmente, e a evidência está no próprio arquivo.

### O momento em que alguém leu o Dia 6

Abra o `AGENTS.md`, seção 7 (RTK SCRATCHPAD):

> "migrado em 21-08-2026 (...) **para manter este arquivo estável como
> prefixo de cache**"

O arquivo `RTK-SCRATCHPAD.md` (aprendizados de sessões anteriores) **saiu** do
AGENTS.md. Por quê? Porque toda vez que a memória mudava, o AGENTS.md mudava —
e o AGENTS.md é o **topo do prompt** de todas as sessões da fábrica. Cada
aprendizado novo quebrava o cache de tudo.

A solução foi a operação "escrever" que você verá no Dia 8: o aprendizado
mora **fora** do prefixo, num arquivo próprio, consultado sob demanda. O
prefixo fica estável; a memória continua existindo.

### A ordem das partes dentro do AGENTS.md

A estrutura do AGENTS.md já segue "do mais estável ao mais volátil":

1. Seção 0 — Economia de tokens (regra de custo, muda por release).
2. Seções 1–6 — Regras, squad, MCPs, templates, fluxo, portabilidade.
3. Seção 7 — RTK: **apenas um ponteiro** ("consultar sob demanda").

Note o detalhe de arquitetura: a memória volátil não está no arquivo estável —
está num ponteiro no fim do arquivo.

### Outra estabilização visível: Regra R6

> "R6 (Modelo Livre): nenhum modelo LLM fixo. `model: inherit` em todos os
> agents."

Cada agente da fábrica usa `model: inherit`. Isso estabiliza o prefixo de duas
formas: nenhum harness da fábrica injeta nome de modelo no prompt, e cada
arquivo de agente é curto e constante.

### Onde entra o cache compartilhado (para a Fase 2)

Na Fase 2, a fábrica dispara **lotes de subagentes** (`--lote 4`). Se todos
compartilham o mesmo pedaço de projeto (AGENTS.md + dossiê indexado), e esse
pedaço vem **primeiro** no prompt de cada subagente, o primeiro subagente paga
a escrita e os demais pagam só leitura. Para isso, três condições precisam ser
verdadeiras ao mesmo tempo:

- Prefixo **byte a byte** idêntico (um espaço a mais já derrota);
- Bloco comum **primeiro**, o específico de cada subagente depois;
- **Mesmo modelo** para os subagentes de leitura (cache não atravessa modelo).

### Os quatro sintomas de prefixo quebrado

| Sintoma no custo | O que significa |
|---|---|
| Custo/turno constante, sem queda após o turno 3 | Cache não está sendo escrito |
| Custo cai e depois **sobe** no meio da sessão | Algo reescreveu o topo no meio |
| Subagente A barato, B caro, prompts "iguais" | Prefixos não são byte a byte |
| Tudo barato e a qualidade cai | Cache servindo conteúdo **obsoleto** |

---

## Mão na massa

### Tarefa 1 — audite a estabilidade do seu prefixo

Capture o prompt montado em dois turnos diferentes de uma mesma sessão e
compare:

```bash
comando-que-despeja-o-prompt --turno 1 > /tmp/turno1.txt
comando-que-despeja-o-prompt --turno 9 > /tmp/turno9.txt
diff /tmp/turno1.txt /tmp/turno9.txt | head -20
```

Se a divergência aparece nas **primeiras 20 linhas**, você tem um invalidador
de topo — o pior tipo. Anote a linha.

### Tarefa 2 — reorganize o prompt em três blocos

Nada de código complicado: torne a **estrutura explícita**. Bloco 1 (estável:
muda por release), Bloco 2 (semi-estável: muda por sessão), Bloco 3 (volátil:
muda todo turno — sempre no fim).

```python
def montar_prompt(instrucao, ferramentas, skills, base, historico, turno_atual):
    bloco_1 = [instrucao, ferramentas, skills]   # cacheavel entre sessoes
    bloco_2 = [base]                             # cacheavel na sessao
    bloco_3 = [*historico, turno_atual]          # nunca cacheavel
    return {"estavel": bloco_1, "sessao": bloco_2, "volatil": bloco_3}
```

O ganho não é o código — é a estrutura que impede alguém de colar uma data no
topo.

### Tarefa 3 — elimine os voláteis do topo

| Item volátil | Estava em | Deve ficar em |
|---|---|---|
| Data de hoje | linha 1 do prompt | instrução do turno |
| Contador de tarefas | prompt | instrução do turno |
| Nome do usuário | prompt | instrução do turno |
| Lista de ferramentas | ordem de um `set()` | lista ordenada e determinística |
| JSON de config | `json.dumps(config)` | `json.dumps(config, sort_keys=True)` |
| Trechos de arquivo | antes da instrução | depois da instrução |

### Tarefa 4 — meça a taxa de acerto

Nenhuma dessas mudanças vale de nada sem número. Registre por turno quanto
veio de cache e calcule a proporção:

```python
def taxa_acerto(registros):
    entrada = sum(r["tokens_entrada"] for r in registros)
    cache = sum(r.get("tokens_cache_leitura", 0) for r in registros)
    escritos = sum(r.get("tokens_cache_escrita", 0) for r in registros)
    return {
        "leitura": cache,
        "comum": entrada - cache - escritos,
        "taxa": round(cache / entrada, 3) if entrada else 0.0,
    }
```

Referências de meta: **> 0,70** em sessão longa com prefixo estável; **0,30 a
0,50** em sessão curta ou com anexos; **< 0,20** é sinal de prefixo instável —
investigue agora.

### Tarefa 5 — o teste mais barato do mundo: o hash do prefixo

Antes de cada chamada, calcule um hash curto do primeiro bloco do prompt e
registre no log. Hash repete → o cache tem chance. Hash muda a cada turno →
**nenhuma política de economia vai salvar — o problema é de arquitetura, não
de preço de token.**

### O que nunca vale a pena cachear

- **Prefixos curtos** (poucas centenas de tokens) — o ganho não cobre a
  administração.
- **Conteúdo que muda a cada turno** — você paga escrita e não recebe leitura.
- **Segredos e credenciais** — além do risco, rotação de segredo derruba o
  prefixo justamente quando ele importa. Segredo vai para o ambiente, nunca
  para o prompt.

---

## Três regras que ficam com você

1. **Hash do prefixo a cada turno.** Se muda sempre, é arquitetura, não preço.
2. **Versão no topo do bloco estável.** A invalidação vira consequência, não
   tarefa (mudou o AGENTS.md → versione; o cache se perde sozinho, sem erro
   silencioso).
3. **Byte a byte, não "equivalente".** Cache não negocia com aproximação —
   compare com `diff`, nunca com os olhos.

## Erros de julgamento deste dia

- Assumir que "prompts equivalentes" geram o mesmo cache.
- Deixar caminho absoluto da máquina dentro do prefixo (prefixo único por
  estação de trabalho).
- Reordenar seções do arquivo de instruções a cada edição, invalidando o cache
  sem perceber.
- Enxugar o prefixo **antes** de estabilizá-lo — paga escrita de cache por uma
  economia menor.
- Confiar em cache sem medir — o desconto existe, mas nada garante que é você
  que está recebendo.

**Antipadrão observável:** um gráfico de custo por turno com subida no meio da
sessão. Cache saudável é uma curva monotonicamente decrescente; qualquer
subida no meio significa que algo reescreveu o topo — e o topo, na cabine, é
área de acesso restrito.

---

## Checklist do dia

- [ ] Explico por que cache exige prefixo **idêntico** byte a byte.
- [ ] Digo de memória a ordem das partes: estável → volátil.
- [ ] Rodei o `diff` entre o prompt do turno 1 e um turno tardio.
- [ ] Tirei data, caminho e contadores do topo do prompt.
- [ ] Serialização de config está determinística (`sort_keys=True`).
- [ ] Entendi por que o RTK-SCRATCHPAD mora fora do AGENTS.md.
- [ ] Meço taxa de leitura de cache antes e depois de qualquer mudança.

## Para saber mais

- `AGENTS.md` seções 0 e 7 — a política de estabilidade do prefixo e o
  arquivo de memória que saiu do prefixo de propósito.
- Skills `lean-ctx`, `headroom`, `caveman` — as táticas do Dia 7, que reduzem
  o que entra no prefixo.

No Dia 7, você fecha o ciclo econômico: as configurações reais que cortam
consumo **sem cortar qualidade** — e por que o token barato da leitura anda
junto com o preço do seu perfeccionismo.