# Dia 10 — Hooks: a camada que intercepta o agente

## Meta do dia

Entender a diferença entre **verificar depois** e **interceptar durante** —
os hooks — e aprender a escolher entre hook de comando, de prompt e de
agente, incluindo o mais importante de todos: **o pre-commit que bloqueia
suíte vermelha**.

## A ideia em uma frase

Hook é a politica do harness virando **mecânica** — o único jeito de uma
regra não depender de boa vontade.

---

## A explicação simples

### O que é um hook

Um **hook** é um comando que o harness executa **automaticamente** quando um
evento do ciclo de vida do agente acontece. Enquanto o gate avalia um artefato
*depois* (Dia 9), o hook se pendura *no ponto exato* em que o evento ocorre —
inclusive **antes** do dano.

O ciclo de vida tem pontos definidos, e cada um resolve um problema:

| Momento | O que o hook resolve |
|---|---|
| Início de sessão | injetar estado da tarefa, regras do dia |
| Antes da submissão do pedido | enriquecer/validar a entrada |
| **Antes da execução de ferramenta** | **bloquear ação perigosa, comando destrutivo, escrita proibida** |
| Depois da execução de ferramenta | formatar, validar, registrar, disparar verificação |
| Fim da sessão / fim de turno | rodar suíte, gerar relatório, checar pendências |

### Interceptar versus observar

- Hook de **observação** registra.
- Hook de **interceptação** pode **impedir**.

O mecanismo é sempre o mesmo: **código de saída diferente de zero interrompe a
ação.** É por isso que todo capítulo insiste em código de saída — é a única
linguagem que o harness e o shell entendem sem interpretação.

### Os três tipos de hook

| Tipo | O que faz | Custo | Pode bloquear? |
|---|---|---|---|
| **Comando** | executa um programa determinístico | milissegundos | **sim** — o único confiável |
| **Prompt** | usa o LLM para avaliar condição ("edição respeita o padrão?") | mais caro | só triagem — veredito probabilístico |
| **Agente** | delega a um subagente com contexto próprio | mais caro | sim, mas só o que exige raciocínio |

A regra de escolha é objetiva:

> O que é **objetivo** vira comando; o que é **ambíguo** pode virar prompt; o
> que **exige exploração** pode virar agente. E só o primeiro bloqueia de
> forma confiável (você já sabe disso desde o Dia 2).

### A regra operacional que decide o sucesso

**Tempo de execução.** O hook roda em toda ação relevante; um hook lento
transforma a experiência do time em espera. Metas práticas:

- Hook de comando: **abaixo de 100 ms**.
- Suíte de testes: **só** no fim de turno ou no commit, nunca a cada edição.

Hooks lentos são desativados — não por indisciplina, mas por economia de
paciência. **Hooks precisam ser baratos o suficiente para nunca valer a pena
desligá-los.**

### O hook que todo time deveria ter no dia 1

O **pre-commit que bloqueia suíte vermelha**. Ele resolve o que nenhuma
instrução de prompt resolve de forma confiável: por melhor que seja "só
commite com os testes passando", instrução é probabilística; **o hook é
binário**. É a materialização mais pura da fronteira do Dia 2.

### Segurança (importante)

**Hook é código que roda com o seu nível de permissão.** Um hook que executa
conteúdo vindo da resposta do modelo — sem validação — cria uma via de
execução arbitrária (o problema de *injeção indireta*). Hooks devem ser
**estáticos, versionados e auditados** como qualquer código de produção.

---

## O exemplo real: os hooks da fábrica

O `.claude/settings.json` do `proj_fabrica-de-livros` é o Dia 10 em produção.
Ele tem **três hooks `PostToolUse` e um `SessionStart`** — todos **comando**,
nenhum prompt. Veja o padrão:

### Hook 1 — o atualizador de documentação

```json
{
  "matcher": "docs/template",
  "hooks": [
    {
      "type": "command",
      "command": "python scripts/atualizar-documentacao.py --se-sujo --silencioso"
    }
  ]
}
```

A edição toca `docs/template` → o hook roda o script — que só recompila se
houver sujeira (`--se-sujo`) e em silêncio (`--silencioso`). É o formatador
pós-edição do capítulo, sem travar nada.

### Hook 2 — o validado de capítulo

```json
{
  "matcher": "output/*/livros/*/capitulos/cap_*.md",
  "hooks": [
    { "type": "command",
      "command": "bash scripts/validar_capitulo.sh $FILE" }
  ]
}
```

Um capítulo é salvo → o script valida na hora. Estilo, seções, estrutura do
capítulo: **o modelo não decide mais sobre isso — o código garante.**

### Hook 3 — o pre-commit da fábrica (o clássico)

A fábrica tem **mais** que o exemplo do capítulo: o pre-commit está
**versionado** em `scripts/hooks/pre-commit` e é **copiado** para
`.git/hooks/pre-commit` por `scripts/setup-links.ps1` (Win) ou
`setup-links.sh` (Mac/Linux).

Dois detalhes que mostram o capítulo vivido:

- **Não é link** ("`.git/hooks` não aceita hardlink/junction de forma
  confiável") → é copiado, recriado no setup pós-clone. Hook versionado e
  reproduzível na equipe inteira — o "antipadrão hook só na sua máquina"
  combatido por construção.
- **Mecaniza a R16**: o `AGENTS.md` explica — "bloqueia commit se `pytest -q`
  falhar". A regra que o Dia 9 tratou como lei vira **mecânica**: o commit nem
  acontece. A instrução "só commite verde" deixa de depender de boa vontade.

### O mapa de ciclo de vida real

| Evento | Hook da fábrica | Tipo |
|---|---|---|
| Início de sessão | `SessionStart` (injetar software?) | comando |
| Depois da ferramenta | docs/template → atualizar docs | comando |
| Depois da ferramenta | `cap_*.md` → `validar_capitulo.sh` | comando |
| Antes do commit | `pre-commit` → `python -m pytest -q` | comando |

Repare: **todos de comando**. A fábrica consegue rodar verificação de estilo
de capítulo com determinismo total — e é exatamente o que o capítulo ordena:
o objetivo vira comando, e só o que exige raciocínio sobe para o modelo.

### Portable Multi-IDE = hooks para todos

A seção 6 do AGENTS.md explica que os hooks vivem em `.opencode/plugins/
fabrica-hooks.ts` (versionado) e espelham o `.claude/settings.json`. Hooks
fazem parte do **contrato do projeto** — existem para cada IDE que o time
usa, não só para a de quem os criou.

---

## Mão na massa

### Tarefa 1 — o guardião de comandos (antes da ferramenta)

Recebe o comando na entrada padrão e decide: pode rodar ou não. **Ele nunca
executa — só decide.** Essa separação é deliberada: hook simples é hook
confiável.

```python
import json
import sys

PADROES_PROIBIDOS = [
    "rm -rf /",
    "git push --force",
    "dropdb",
    "DROP TABLE",
    "> /dev/sda",
]

def main():
    evento = json.load(sys.stdin)
    comando = (evento.get("tool_input") or {}).get("command", "")
    for padrao in PADROES_PROIBIDOS:
        if padrao in comando:
            print(f"[guard] BLOQUEADO: padrao proibido -> {padrao}", file=sys.stderr)
            sys.exit(2)  # != 0 interrompe a acao
    sys.exit(0)

if __name__ == "__main__":
    main()
```

A mensagem diz **qual comando foi barrado e por quê** — recusa visível, nunca
silenciosa.

### Tarefa 2 — o pre-commit bloqueante (o que importa hoje)

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "[pre-commit] rodando suite de testes..."
if ! python -m pytest -q; then
  echo "[pre-commit] BLOQUEADO: suite vermelha. Corrija e tente novamente." >&2
  exit 1
fi
echo "[pre-commit] suite verde — commit liberado"
```

Instale-o em `.git/hooks/pre-commit`. Ele vale **para humanos e para agentes**
— é o gate do Dia 9 no lugar certo: na **porta de saída do trabalho**.

### Tarefa 3 — o injetor de contexto com teto

Sessão começa, contexto útil entra — sem ocupar a instrução persistente:

```json
{
  "evento": "SessionStart",
  "hooks": [
    { "type": "command",
      "command": "cat docs/estado-tarefa.md 2>/dev/null | head -40" }
  ]
}
```

O `head -40` é a proteção de orçamento: hook que injeta contexto precisa de
**teto** (lembra do Dia 8?).

### Tarefa 4 — o registrador de auditoria (a caixa-preta)

Toda chamada de ferramenta vira uma linha de registro:

```python
import json
import sys
from datetime import datetime, timezone

def main():
    evento = json.load(sys.stdin)
    linha = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "ferramenta": evento.get("tool_name"),
        "sessao": evento.get("session_id"),
        "resultado": str(evento.get("tool_response"))[:200],
    }
    print(json.dumps(linha, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

O truncamento em 200 caracteres é intencional — auditoria não é lugar de
despejar resultado de ferramenta. Quando um incidente acontecer, essa trilha é
a diferença entre investigar e especular.

### Tarefa 5 — o teste de falha

Desabilite um hook de propósito e verifique se o trabalho continua correto.
Se o trabalho continua correto sem ele, pode estar no lugar errado do ciclo
de vida.

### Tabela de decisão: qual hook usar

| Necessidade | Tipo | Pode bloquear? |
|---|---|---|
| Impedir comando destrutivo | comando | sim |
| Formatar após edição | comando | não deve |
| Julgar padrão subjetivo de código | prompt | sim, com ressalva |
| Conferir contrato entre módulos | agente | sim, com custo |
| Injetar estado da tarefa no início | comando | não |
| Registrar trilha de auditoria | comando | não |

---

## Três regras que ficam com você

1. **Hook é determinístico.** Se depende de julgamento do modelo, é gate de
   mérito — não hook.
2. **Hook barato o suficiente para nunca valer a pena desligar.** Hook lento
   vira hook desabilitado.
3. **Hook versionado.** Comportamento que só existe na sua máquina não é
   contrato de projeto.

## Erros de julgamento deste dia

- Hook lento em evento quente (suíte a cada edição).
- Hook que falha **silenciosamente** — trate erro do hook como bloqueio, nunca
  ignore.
- Hook que executa saída do modelo — via direta para execução arbitrária.
- Hook só na máquina de quem configurou — versionar é obrigatório.
- Muitos hooks de prompt — veredito variável e custo por ação.
- Hook com efeito colateral amplo (limpar diretório, reinstalar dependência)
  quando o objetivo era só verificar — verificação e mutação em hooks
  distintos.

**Antipadrão observável:** quando ninguém no time sabe dizer quais hooks
estão ativos na máquina, o comportamento do agente varia por estação. Hook é
contrato do projeto — versionado com os demais arquivos de configuração.

---

## Checklist do dia

- [ ] Conto os eventos do ciclo de vida e o problema que cada hook resolve.
- [ ] Digo a ordem: comando para o objetivo, prompt para o ambíguo, agente
      para o que exige exploração.
- [ ] Instalei o pre-commit que bloqueia suíte vermelha.
- [ ] Escrevi um guardião de comandos com padrões proibidos explícitos.
- [ ] Hook de início de sessão injetando estado com teto.
- [ ] Registro de auditoria append-only ativo.
- [ ] Sei de memória os 4 hooks do `.claude/settings.json` da fábrica.

## Para saber mais

- `.claude/settings.json` do projeto — 3 hooks `PostToolUse` + 1
  `SessionStart`, todos de comando.
- `scripts/hooks/pre-commit` + `scripts/setup-links.ps1`/`.sh` — o
  pre-commit versionado e recriado pós-clone.
- `AGENTS.md` seção 6 (Portabilidade Multi-IDE) — hooks espelhados em
  `.opencode/plugins/fabrica-hooks.ts`.

No Dia 11, você aprende a delegar: **subagentes** com contexto isolado — e o
contrato que faz a delegação economizar em vez de multiplicar custo.