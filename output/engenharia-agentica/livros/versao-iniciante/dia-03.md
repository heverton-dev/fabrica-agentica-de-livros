# Dia 3 — O arquivo que todo agente lê: AGENTS.md, config.json e rules

## Meta do dia

Escrever as **três camadas de instrução persistente** que dizem ao agente o
que ele precisa saber *antes* de começar qualquer tarefa: um `AGENTS.md`
enxuto, regras condicionais e a configuração que bloqueia.

## A ideia em uma frase

Instrução persistente é o único componente do harness que melhora todos os
turnos de uma vez — e o único que pode destruí-los se for mal escrito.

---

## A explicação simples

O modelo não tem memória. Toda sessão começa do zero. Então existe uma classe
de informação que precisa ser **reinjetada a cada turno**: quem é o projeto,
como se roda, o que é proibido, qual o contrato de qualidade.

Isso é a **instrução persistente**.

E ela tem uma consequência econômica que quase todo iniciante ignora:

> Tudo que está na instrução persistente é **pago a cada turno**.

Uma regra de 200 tokens, numa sessão de 30 turnos = 6.000 tokens só para
repetir a mesma frase. Multiplique por todos os turnos, por todas as sessões,
por todas as pessoas do time. Instrução mal escrita é um imposto invisível
sobre tudo.

### As três leis da instrução persistente

**Lei 1 — Densidade, não volume.**

A recomendação que emergiu da prática é manter o arquivo de instruções curto e
operacional — um *README para agentes*. Comandos que funcionam, convenções que
importam, armadilhas do projeto. Regras genéricas de estilo ("escreva código
limpo") ocupam contexto e não mudam comportamento. Contratos verificáveis
("todo teste passa antes do commit") mudam.

**Lei 2 — Estabilidade do prefixo.**

Provedores cobram muito menos por tokens que já foram processados antes,
desde que o **início** do prompt permaneça idêntico (vamos ver isso em detalhe
no Dia 6). Instrução que muda a cada sessão — com data no topo, contador de
tarefas, nome de usuário — destrói esse desconto silenciosamente.

Instrução persistente estável é, literalmente, dinheiro.

**Lei 3 — Separação por camada de escopo.**

Um harness maduro organiza a instrução em três níveis (ver abaixo). A cura para
o arquivo-enciclopédia é a pergunta: *isto vale para toda tarefa, ou só para
uma parte do repositório?* Se vale só para uma parte, não é camada 1.

## As três camadas

### Camada 1 — Escopo de projeto, sempre ativo

O `AGENTS.md` na raiz. Aplica-se a tudo, carrega sempre, deve ser curto (o
custo é universal).

### Camada 2 — Escopo de projeto, condicional

Regras que só valem para certos caminhos, tipos de arquivo ou frameworks.
Convenção de migração de banco, padrão de componente de UI, regras de uma
pasta legada. **Essa camada custa zero quando não se aplica.**

> O ponto contraintuitivo: a camada 2 é frequentemente **mais valiosa** que a
> camada 1. Ela permite ser específico e detalhado sem poluir o orçamento
> global. Time que só conhece camada 1 escreve pouco e vago; time que domina
> camada 2 escreve muito e preciso, sem pagar por isso.

### Camada 3 — Escopo de harness, comportamental

O arquivo de configuração do agente: permissões, hooks, limites, escolha de
modelo. Não ensina; **restringe e habilita**. É aqui que você define o que o
agente **não pode** fazer.

Instrução de camada 1 **pede**; configuração de camada 3 **impede**. Você já
sabe qual das duas é confiável.

Voltando à cabine: o checklist de pré-voo é camada 1 (curto, universal, lido
em todo voo). Os procedimentos específicos de tipo de aeronave são camada 2
(quem voa jato regional não abre o manual do wide-body). O painel de
configuração é camada 3 (não ensina, só liga/bloqueia).

---

## O exemplo real: as três camadas da fábrica

O `proj_fabrica-de-livros` pratica as três camadas de forma explícita.

### Camada 1 da fábrica — o `AGENTS.md`

Abra o `AGENTS.md` na raiz do projeto. Você vai encontrar exatamente o que
este capítulo manda:

- **Projeto** — a primeira linha diz o que é: "Fábrica Agêntica de Publicações".
- **Comandos** — `python -m pytest -q`, scripts de produção em `scripts/`.
- **Squad** — quem faz o quê (pesquisador, arquiteto, estrategista, redator...).
- **Fluxo operacional** — a ordem das fases (0 até 10 + entrega).
- **Regras R1 a R17** — contratos de qualidade verificáveis.

E repare na economia: o arquivo **não** tenta explicar como funciona cada
script do zero. Ele aponta para o registro declarativo (`scripts/tipos_obra.py`
para tipos de obra) — uma regra por vez, no lugar que ela pertence.

Um detalhe que é uma aula de "Lei 2": a fábrica mantém o aprendizado de
sessões passadas num arquivo separado (`RTK-SCRATCHPAD.md`), "não lido
automaticamente pelo agente; consultar sob demanda". Ou seja: **memória barata
não polui o prefixo caro**. Isso é separação de camadas em ação.

### Camada 2 da fábrica — regras condicionais na prática

O projeto usa regras por tipo de obra. Em vez de colocar no `AGENTS.md` os
detalhes de livro, TCC, artigo, e-book, playbook, lead magnet, deck e e-mails,
ele declara tudo num registro único (`scripts/tipos_obra.py`) e os pontos de
dispatch consultam esse registro. Uma entrada por tipo — não oito arquivos
para editar.

A mesma ideia: a regra só é carregada quando o tipo de obra casa com a tarefa.

### Camada 3 da fábrica — o `settings.json`

Já vimos no Dia 1 o `.claude/settings.json` com hooks que rodam depois de
qualquer `Edit|Write`. Mas a fábrica tem uma decisão de camada 3 ainda mais
forte, e está no git — não na máquina de ninguém:

O hook de **pré-commit** em `scripts/hooks/pre-commit` (mecaniza a regra R16:
bloqueia o commit se `pytest -q` falhar). Leia a regra R16 no AGENTS.md e
depois abra o script:

```bash
cat scripts/hooks/pre-commit
```

O que você vai encontrar: um script que, antes de qualquer commit, roda a
suíte. Se falhar, **o commit é barrado** — devolve código de saída diferente
de zero. Não é um pedido no prompt; é uma lei no git. Camada 3 no estado mais
puro da palavra.

Repare também no detalhe de portabilidade do AGENTS.md: "Não é link: `.git/hooks`
não aceita hardlink/junction de forma confiável — recopiar". Isso é um time que
aprendeu que config que existe só na máquina de alguém não é arquitetura.

---

## Mão na massa

### Tarefa 1 — o teste de aceitação de cada linha

Abra um `AGENTS.md` (use o da própria fábrica ou um seu). Para 3 linhas
qualquer, faça o teste de remoção:

> *Se eu remover esta linha, algo quebra?*

Se a resposta é não, a linha é decoração — candidata a sair (ou a migrar de
camada).

### Tarefa 2 — escreva a camada 1 em ≤ 40 linhas

Use este formulário mínimo:

```markdown
### Projeto
<uma frase: o que é, linguagem, banco, dependências externas>

### Comandos
- testes: <comando exato>
- rodar local: <comando exato>
- migracao: <comando exato>

### Contratos verificados
- <regra 1 — e onde ela é verificada>
- <regra 2 — e onde ela é verificada>

### Armadilhas
- <comportamento surpreendente que só vale para este repositório>
```

Os contratos devem apontar para verificações reais — a instrução descreve o
que o CI já garante. O agente sabe antes; o CI garante depois.

### Tarefa 3 — transforme uma regra em impedimento (camada 3)

Escolha uma regra que hoje é um pedido ("nunca alterar X") e transforme em
permissão negada. No formato do harness da fábrica:

```json
{
  "permissions": {
    "allow": ["Bash(python -m pytest*)", "Read(**)"],
    "deny": ["Bash(git push*)", "Write(migrations/*)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [{ "type": "command", "command": "python scripts/validar.py" }]
      }
    ]
  }
}
```

A pergunta de controle: *se o agente tentar desobedecer, o sistema recusa, ou
apenas avisa?* Se avisa, ainda é prosa. Se recusa, é camada 3.

### Tarefa 4 — descubra a ordem de precedência

Todo harness tem uma ordem entre config de usuário, projeto e sistema.
Descubra a sua **empiricamente**:

```bash
# 1. Defina um valor no escopo de usuario
echo '{"model": "valor-do-usuario"}' > ~/.agent/settings.json
# 2. Defina outro no escopo de projeto
echo '{"model": "valor-do-projeto"}' > .agent/settings.json
# 3. Pergunte qual venceu
agent config get model
```

Se o projeto vence, a config do time é lei. Se o usuário vence e um hook de
segurança pode ser anulado por config pessoal, mova a restrição para um
mecanismo não sobrescrevível (hook versionado), em vez de só documentar a
precedência.

---

## Como migrar um arquivo-enciclopédia

Se o `AGENTS.md` do seu projeto já virou depósito de 900 linhas, a correção é
mecânica, numa tarde:

| Classificação da linha | Destino | Teste de decisão |
|---|---|---|
| Vale para todo trabalho | camada 1 | "se aplica a um PR de CSS e a uma migração?" |
| Vale só para parte do repositório | camada 2 condicional | "posso declarar um glob para isso?" |
| Restrição executável | camada 3 (permissão/hook) | "existe comando que verifica isso?" |
| Contexto histórico/decisão antiga | `docs/decisoes/` | "ensina ação ou explica passado?" |
| Exemplo de código longo | arquivo de referência | "precisa ser pago a cada turno?" |

A pergunta que resolve 90% dos casos: **vale para todo trabalho?** Tudo que
responde "não" sai da camada 1 — e o arquivo encolhe sem perder informação,
apenas a realoca para onde ela custa menos.

## Sintomas de instrução morta (o antipadrão)

- O agente cita uma regra que o time não lembra ter escrito.
- O agente se desculpa por violar uma convenção que já foi abandonada.

Isso é **instrução morta na cabine** — instrução persistente apodrece como
toda documentação, só que em silêncio. A fábrica tem esse ritual de
manutenção: ver a seção 7 do AGENTS.md, onde o aprendizado vai para um
arquivo separado em vez de inflar o prefixo.

---

## Checklist do dia

- [ ] Escrevi/revisei a camada 1 em ≤ 40 linhas.
- [ ] Cada linha sobreviveu ao teste de remoção.
- [ ] Identifiquei pelo menos uma regra que pertence à camada 2 (condicional).
- [ ] Uma regra virou permissão negada ou hook (camada 3).
- [ ] Descobri a ordem de precedência do meu harness na prática.
- [ ] Entendi por que `RTK-SCRATCHPAD.md` fora do AGENTS.md economiza tokens.

## Para saber mais

- `AGENTS.md` da própria fábrica — leia as Regras Globais (R1 a R17) e
  identifique qual delas você usaria na camada 3.
- `docs/manual-completo-fabrica.md` — seção de estrutura de pastas do projeto.

No Dia 4, o agente descobre capacidade sem inflar a janela: skills, MCPs e a
arte de escrever o gatilho certo.