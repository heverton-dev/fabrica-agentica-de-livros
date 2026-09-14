# Dia 1 — O agente não é o modelo

## Meta do dia

Identificar as **5 peças da cabine** (o harness) que existem em volta de um
modelo de IA dentro de um projeto real — e localizar cada uma delas no
repositório `proj_fabrica-de-livros`.

## A ideia em uma frase

O modelo de IA é só o motor; a qualidade do seu resultado depende da
**cabine** que você constrói em volta dele — e a cabine é feita de arquivos
e configurações que você *controla*.

---

## A explicação simples

Quando alguém diz "uso a IA para programar", a frase esconde o essencial.
O modelo de linguagem (LLM) é, literalmente, uma função:

> Recebe texto → devolve texto.

Ele não lembra de nada entre uma chamada e outra. Ele não sabe qual pasta
seu projeto está. Ele não sabe suas regras. Toda a impressão de que ele
"entende e continua de onde parou" é **reconstruída a cada vez**, enviando
de novo o histórico anterior na entrada.

Então o que você realmente usa no dia a dia — a coisa que lê seus arquivos,
roda seus testes e respeita suas regras — **não é o modelo**. É uma camada de
software construída em volta dele. Essa camada tem um nome: **harness**.

Pense em um avião:

- O **piloto** é o modelo: potente, esperto, capaz de improvisar.
- A **cabine** é o harness: painel, checklists, alarmes, piloto automático.

Ninguém entrega um avião a um piloto sem cabine. Ninguém deveria entregar um
projeto a um modelo sem harness. Voar bem não é "pilotar melhor" — é ter uma
cabine melhor.

## As 5 peças da cabine

Todo harness que funciona bem tem estas 5 peças:

### 1. Instrução persistente — o que o agente "é"

É o texto que define papel, limites e regras do agente. Ele é reinjetado
**a cada turno** — por isso se chama persistente: vive para sempre na
conversa, mesmo quando você não o menciona.

Mora em arquivos de projeto como `AGENTS.md`, em arquivos de regras como
`CLAUDE.md`, ou no prompt de sistema.

### 2. Ferramentas — o que o agente pode fazer

São funções que o modelo pode chamar: ler um arquivo, editar, rodar um
comando, buscar na web, consultar um banco.

Sem ferramentas, o agente só conversa. Com ferramentas, ele age no mundo.

### 3. Contexto — o que o agente enxerga agora

É o recorte do mundo colocado na janela a cada turno: trechos de código,
saídas de comando, resultados de busca.

É o **recurso mais escasso** do sistema — e o mais mal gerenciado.

### 4. Estado — o que sobrevive entre sessões

É o que ele lembra *fora* da conversa: arquivos de tarefa, bancos de dados,
memória externa. O modelo não tem estado; o harness fabrica um.

### 5. Política — as regras que não dependem de boa vontade

São as regras **garantidas por código**: permissões de ferramenta, hooks,
gates de validação, limites de custo e tempo.

A diferença entre instrução e política é a mais importante deste dia:

- **Instrução** é um pedido: "rode os testes antes de terminar". O modelo
  pode esquecer.
- **Política** é uma lei: um hook impede o commit se os testes falharem.
  O modelo pode até tentar esquecer — o código não deixa.

---

## O exemplo real: a cabine do `proj_fabrica-de-livros`

O `proj_fabrica-de-livros` é uma **fábrica de publicações**: uma esteira onde
agentes pesquisam, escrevem, revisam e compilam livros, TCCs, artigos,
e-books, playbooks, lead magnets, decks e e-mails. E adivinhe: ele é ele
próprio um grande harness. Dá para encontrar as 5 peças nele com poucos
minutos de exploração.

| Peça | Onde está no projeto real |
|---|---|
| instrução persistente | `AGENTS.md` na raiz (que vira `CLAUDE.md` por link) |
| ferramentas | os scripts em `scripts/` (ex.: `auditar-obra.py`) e os MCPs em `.mcp.json` |
| contexto | os dossiês indexados de cada obra em `output/<obra>/pesquisa/` |
| estado | `config_obra.json` e `pool-estado.json` de cada obra |
| política | `.claude/settings.json` (hooks) e o hook git em `scripts/hooks/pre-commit` |

Abra cada um desses arquivos agora, mesmo que não entenda tudo. O ato de
localizar a peça já ensina: a fábrica inteira depende menos do modelo e mais
desses arquivos.

Vejamos um exemplo concreto de política, retirado do `.claude/settings.json`
real do projeto. Ele configura que, **sempre que** um arquivo for editado ou
escrito, um script de validação roda sozinho:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash scripts/validar_capitulo.sh $FILE 2>/dev/null && echo '[GATES OK]' || echo '[GATES FALHOU - Revisar capítulo]'",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Leia em voz alta o que isso faz: *depois de qualquer edit ou write, o script
`validar_capitulo.sh` roda; se falhar, o agente escuta "GATES FALHOU".*

Isso é **política**: não é uma instrução, é um gatilho automático. O agente
pode esquecer de validar — a cabine não deixa.

---

## Mão na massa

Abra o terminal na pasta `proj_fabrica-de-livros` e faça:

1. Liste os arquivos de instrução:

   ```bash
   ls AGENTS.md CLAUDE.md
   ```

2. Abra o começo do `AGENTS.md` e encontre uma seção que começa com regras
   ou "R1", "R2" — são instruções persistentes.

3. Liste os scripts (as ferramentas determinísticas):

   ```bash
   ls scripts/ | grep -E "auditar|validar|indexar"
   ```

4. Abra `.claude/settings.json` e conte quantos hooks existem.
   (Você deve encontrar 3 no bloco `PostToolUse` + 1 em `SessionStart`.)

5. Procure o estado de uma obra, por exemplo `config_obra.json` dentro de
   `output/engenharia-agentica/livros/`, e leia o campo `tema`.

---

## Checklist do dia

- [ ] Sei a diferença entre modelo, harness e agente.
- [ ] Consigo dizer as 5 peças da cabine de memória.
- [ ] Sei qual é a diferença entre instrução (pedido) e política (lei).
- [ ] Localizei as 5 peças dentro de `proj_fabrica-de-livros`.
- [ ] Expliquei, com as minhas palavras, o que o hook do `settings.json` faz.

---

## Aposta de entendimento

Tente responder antes de seguir:

1. Por que um agente pode dar a impressão de "lembrar" o que aconteceu no
   chat anterior, se o modelo não tem memória?
2. Se você trocar o modelo de IA do projeto por outro, o que provavelmente
   continua funcionando? E o que pode quebrar?

**Respostas de referência:** (1) porque o harness reenvia o histórico a cada
chamada. (2) As peças de cabine — instruções, scripts, hooks — continuam;
o que muda é só o "piloto". Se algo quebrar, o problema provavelmente está
na cabine, não no modelo.

---

## Para saber mais

- `AGENTS.md` — o padrão aberto de arquivo de instruções: github.com/agentsmd/agents.md
- "Effective context engineering for AI agents" — Anthropic Engineering Blog
- O arquivo `docs/manual-completo-fabrica.md` do próprio projeto, se quiser
  ver a esteira completa por dentro.

No Dia 2, vamos responder a pergunta que este dia deixou aberta: o que deve
ser decidido pelo modelo (probabilístico) e o que deve ser garantido por
código (determinístico).