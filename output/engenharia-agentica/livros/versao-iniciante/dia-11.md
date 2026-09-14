# Dia 11 — Agents e subagentes: delegação com contexto isolado

## Meta do dia

Entender o **subagente** — uma instância com janela de contexto própria —
e aprender o que delegar, o que **nunca** delegar, e o **contrato de retorno**
que faz a delegação economizar contexto em vez de inflá-lo.

## A ideia em uma frase

Subagente vale quando a razão entre o que ele lê e o que ele conclui é alta —
e o contrato de retorno é o que garante isso.

---

## A explicação simples

### O que define um subagente

Um **subagente** é uma instância separada, com janela de contexto própria,
prompt de sistema próprio e lista de ferramentas própria. Ele executa uma
tarefa e devolve ao agente principal **apenas o resultado — não o histórico**.

> **O que acontece dentro do subagente não entra no contexto do pai. Só o
> retorno entra.**

Sem isolamento, toda leitura pesada que o agente faz permanece no histórico e
é reprocessada em todos os turnos seguintes (o efeito do Dia 5). Com
isolamento, a leitura pesada acontece **uma vez**, em outro contexto, e o
contexto principal recebe só a conclusão.

### A métrica que decide se a delegação valeu

> **Razão de compressão = tokens lidos ÷ tokens devolvidos.**

Referências práticas:

| Razão | Veredito |
|---|---|
| acima de 10 | excelente |
| 5 a 10 | compensa |
| abaixo de 3 | delegação por gosto, não por economia |

### O que COMPENSA delegar

1. **Varredura ampla com conclusão estreita.** "Em quais lugares deste
   repositório o contrato `/login` é consumido?" — lê dezenas de arquivos,
   devolve quinze linhas.
2. **Execução isolada e ruidosa.** "Rode a suíte e diga quais falharam" — a
   saída bruta é enorme, a conclusão é curta. Bônus: o ruído fica fora do pai.
3. **Trabalho paralelo independente.** Três investigações que não dependem
   entre si rodam ao mesmo tempo, cada uma em seu contexto.

### O que NÃO compensa delegar

1. **Tarefa que precisa de contexto compartilhado.** O subagente não sabe o
   que o pai sabe — reconstruir o contexto custa tokens e ainda resulta em
   decisão desalinhada.
2. **Escrita longa e coerente.** Um capítulo, um relatório, um documento com
   voz única: o isolamento destrói a consistência interna.
3. **Tarefa pequena.** Delegação tem custo fixo (prompt, ferramentas,
   retorno); abaixo de certo tamanho, só adiciona latência.

### A assimetria de informação (declarar no contrato!)

O subagente **não sabe** o que o pai sabe: deixa o histórico, as decisões, as
restrições descobertas. Se isso importa, **precisa viajar no pedido** — e é um
custo de entrada que entra na conta. Delegar bem é, em boa medida, escrever
um briefing **completo e curto**.

O contraponto que faz a delegação funcionar: o pai **também não sabe** o que o
subagente lê. O contrato de retorno controla o lado que importa.

### Dois efeitos colaterais valiosos

- **Filtro de ruído:** stack trace, log de build e erro verboso ficam no
  subagente; o pai recebe "a falha é X na linha Y". Qualidade de decisão
  melhora — o pai trabalha com sinais, não matéria-prima.
- **A armadilha:** subagente que não verifica. Como ninguém vê o que ele leu,
  um retorno errado é praticamente indetectável. A mitigação: **exigir
  procedência** (caminho e linha) em todo retorno, para reconferir com um
  comando barato.

---

## O exemplo real: a delegação na fábrica

O `proj_fabrica-de-livros` é um caso de estudo de fan-out por decomposição de
tarefa. O AGENTS.md, seção 2, lista os subagentes, e cada um obedece às
classes deste capítulo:

### Fan-out por capítulo (o "paralelo independente")

> `subagente-redator-capitulo` — "manufatura tática completa de 1 capítulo em
> paralelo (Estratégia + Redação EITA + Diagrama Mermaid + CI de Código +
> Auto-Validação de Qualidade)".

Cada capítulo tem **janela própria**, e na Fase 2 `pool-capitulos.py` dispara
em **lotes de 4**. O orquestrador nunca paga as leituras internas de cada
redator — só o capítulo pronto. É o fan-out da tabela do capítulo.

### O mesmo padrão, em todos os tipos

- `subagente-pesquisador` — a varredura de fontes acontece isolada.
- `subagente-redator-secao-tcc` — mesmo desenho para TCC.
- `subagente-adaptador-ebook` — a reescrita de tom dos capítulos, isolada.
- `subagente-revisor-tecnico` — corrige **em paralelo um lote** de capítulos
  apontados como defeituosos pela auditoria.

### Delegação dentro da delegação

O AGENTS.md regra 4:

> "Delegação Cavecrew: subagentes comprimidos para buscas/edições extensas
> **(nunca para prosa)**."

Três ensinamentos do capítulo, em uma linha:

- a delegação é para o que **comprime** (busca, edição);
- a escrita longa coerente é **proibida** de delegar (prosa);
- o subagente que devolve pouco é o desenho por padrão.

### O contrato de retorno é a disciplina do AGENTS.md

A regra 0.4 (headroom) aplica-se a tudo que volta: "logs/builds >7 linhas →
comprimir (3 topo + 4 fim)". E o gate de retorno é determinístico: exige-se
que o retorno do subagente caiba no formato contratado — porque um retorno
longo é custo do pai, e o pai não deve pagar por leitura que já aconteceu.

### O revisor adversarial que a fábrica executa por script

A Fase 2.5 roda `auditar-obra.py --estrito` e o `revisor-tecnico` trata cada
achar como defeito com **localização** — o revisor não corrige o aceite, ele
razão pelo critério. É o passo 7 do capítulo no mundo real: quem julga não
produz; quem produz não julga — e a régua (os gates) vem do repositório, não
do autor.

### A fronteira de autonomia

O AGENTS.md define o que o subagente decide e o que confirma: o fluxo é
**100% autônomo** (R3) **depois que o operador define o tema** — mas a escolha
inicial (tema, e se entra CAMPANHA/MÁQUINA, R17) é sempre humana. Justamente
a fronteira do dia: **delegação ≠ terceirização de risco.**

---

## Mão na massa

### Tarefa 1 — escreva o contrato ANTES do prompt

O artefato central. Define o que entra, o que sai, o que é proibido:

```json
{
  "papel": "investigador-de-consumidores",
  "pergunta": "Quais modulos consomem o contrato de /login e como?",
  "contexto_necessario": [
    "contrato atual de /login: POST com {usuario, senha}",
    "restricao: clientes moveis dependem do formato de resposta"
  ],
  "limite_retorno_tokens": 250,
  "formato_retorno": "tabela: caminho:linha | tipo de consumo | risco (alto/medio/baixo)",
  "obrigatorio": ["citacao de caminho e linha para cada afirmacao"],
  "proibido": [
    "colar trechos maiores que 3 linhas",
    "sugerir implementacao",
    "resumir arquivos nao consultados"
  ]
}
```

`contexto_necessario` resolve a assimetria de informação; `obrigatorio` exige
procedência — retorno verificável por comando barato, não por confiança.

### Tarefa 2 — o retorno com esquema FIXO

O erro nº 1 de quem começa: receber um relatório em prosa longo que o pai lê
inteiro para extrair duas informações. Solução: formato fixo, campos nomeados
(veredito + evidência + lista de arquivos). O pai consome **por campo**, não
por leitura. Bônus: o formato obriga o subagente a **decidir antes de
escrever** — sem "em cima do muro".

### Tarefa 3 — valide o limite de retorno como ERRO

```python
def delegar(contrato, executor_subagente):
    retorno = executor_subagente(contrato)
    if len(retorno.split()) > contrato["limite_retorno_tokens"]:
        return {"erro": "retorno acima do limite", "bruto": retorno[:500]}
    return {"resultado": retorno}
```

Retorno acima do limite é **erro**, não sucesso parcial. Sem isso o contrato
vira sugestão e o ganho some na primeira execução verbosa.

### Tarefa 4 — meça a razão de compressão

```python
def razao_compressao(registros):
    lidos = sum(r["tokens_lidos"] for r in registros)
    devolvidos = sum(r["tokens_devolvidos"] for r in registros)
    if not devolvidos:
        return {"razao": float("inf"), "lidos": lidos, "devolvidos": 0}
    return {
        "razao": round(lidos / devolvidos, 1),
        "veredito": "vale" if lidos / devolvidos >= 8 else "nao compensa",
    }
```

Delegação que não é medida não é gerenciada.

### Tarefa 5 — reconfira procedência por amostragem

```bash
sed -n '142p' app/routes/legacy.py | grep -n "login" && echo "[OK] procedencia confirmada"
```

Uma linha. A diferença entre **confiar e verificar** — um item por retorno é
suficiente na prática.

### Tarefa 6 — o revisor adversarial

O subagente mais valioso **contradiz**. Três regras para que ele funcione:

- recebe **os critérios**, não o resumo do autor (senão revisa o resumo);
- **não corrige nada** — se corrigir, vira coautor e perde independência;
- responde com **evidência**, não opinião (local exato + critério violado).

Um sistema com produtor + revisor adversarial tem **controle interno**; dois
produtores têm só redundância.

### Tabela de decisão: quando NÃO delegar

| Situação | Motivo |
|---|---|
| Tarefa de um único passo | custo de montar a delegação > tarefa |
| Decisão que exige o contexto inteiro | o isolamento destrói a informação |
| Trabalho estritamente sequencial | só latência acrescentada |
| Resultado com rastreabilidade linha a linha | o retorno comprimido perde o detalhe |

**A regra geral do livro:** delegue onde o trabalho **comprime** ou
**paraleliza**; faça local onde ele **expande** e depende de contexto
acumulado.

### A fronteira de autonomia (listê por projeto)

Escreva a lista do que o subagente pode fazer **sozinho** e o que exige
**confirmação**. Essa lista é o que separa delegação de terceirização de
risco.

---

## Três regras que ficam com você

1. **Contrato antes da delegação.** Defina o formato de retorno antes de
   disparar o subagente.
2. **Pergunta estreita, não área ampla.** "Revise o módulo de rede" produz
   relatório genérico; "quais chamadas ignoram erro de rede?" produz correção
   utilizável.
3. **Produtor e revisor são papéis distintos.** Quem corrige não é quem julga.

## Erros de julgamento deste dia

- Delegar para ganhar velocidade **sem definir o formato do retorno**.
- Usar subagente para tarefa que exige o contexto acumulado da conversa.
- Não registrar qual versão do subagente produziu o resultado.
- Confundir número de subagentes com capacidade — três sem contrato produzem
  menos que um bem instruído.
- Delegar sem briefing — o subagente decide sem as restrições e volta
  desalinhado.
- Confiar sem procedência — retorno errado é indetectável sem caminho e linha.

**Antipadrão observável:** o agente principal **reescreve** o resultado
recebido antes de usá-lo. O contrato de retorno está errado — um bom contrato
devolve exatamente o que o próximo passo consome, e nada mais.

---

## Checklist do dia

- [ ] Explico a propriedade definidora: só o retorno entra no contexto do pai.
- [ ] Digo as 3 tarefas que compensam e as 3 que não compensam delegar.
- [ ] Escrevi um contrato com pergunta, contexto, limite, esquema e proibições.
- [ ] Razão de compressão medida (≥ 8 compensa; < 3 é prejuízo).
- [ ] Procedência exigida e conferida por amostragem.
- [ ] Caso identificado em que delegar foi revertido por não compensar.

## Para saber mais

- `AGENTS.md` seção 2 (Subagentes) e regra 4 (Delegação Cavecrew) — o
  catálogo de subagentes e a regra "nunca para prosa".
- `pool-capitulos.py` — o fan-out por lote da Fase 2 na prática.
- Fase 2.5 (revisor-técnico) — o revisor adversarial com régua determinística.

No Dia 12, você escala: **várias tarefas ao mesmo tempo, cada uma em seu
próprio diretório de trabalho** — sem que os agentes se atropelem.