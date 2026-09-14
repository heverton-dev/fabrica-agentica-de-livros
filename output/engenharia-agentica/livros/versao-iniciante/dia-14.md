# Dia 14 — As configurações que nunca te contam

## Meta do dia

Conhecer o território onde quase ninguém olha: configurações que **já
existem**, que têm efeito real sobre custo, segurança e comportamento, e que
**não produzem nenhum aviso** quando estão erradas. Nenhum erro no console,
nenhum teste vermelho — só um sistema que se comporta de um jeito que ninguém
escolheu.

## A ideia em uma frase

Configuração silenciosa é aquela cujo efeito aparece só na fatura, no
incidente ou no vazamento — nunca no aviso.

---

## A explicação simples

### Por que configuração silenciosa existe: precedência

Todo harness combina camadas de configuração: padrões do produto, configuração
do usuário, configuração do projeto, variáveis de ambiente, argumentos de
linha de comando. Quem decide o comportamento é a **última camada avaliada** —
não a que você escreveu com cuidado no repositório. Um valor definido no
projeto é anulado por uma variável de ambiente herdada do shell, e ninguém
entende por que o comportamento mudou.

### Por que ela persiste: assimetria de feedback

Configuração errada que gera **erro** é corrigida em minutos. Configuração
errada que gera **degradação** não gera sinal nenhum: o timeout que corta uma
resposta validada no meio, o teto de saída que trunca um relatório, o nível de
log que descarta a evidência de que você precisa. O sistema funciona — só
funciona pior.

### Os cinco grupos perigosos

| Grupo | Efeito silencioso |
|---|---|
| Orçamento de contexto (janela, limite de compactação, teto de saída, teto de ferramenta) | truncamento: o texto corta no meio e o modelo conclui com informação parcial, sem aviso |
| Tempo e retentativa (timeout, retries, backoff) | falha intermitente que parece flutuação de rede, mas é o harness abortando operação legítima e lenta |
| Permissão e sandbox (rede, escrita, shell, ambiente) | superfície de ataque aberta sem ninguém ter decidido |
| Persistência e telemetria (histórico em disco, envio ao provedor, retenção, nível de log) | dado sensível em repouso além do necessário — ou auditoria que não existe quando você precisa |
| Comportamento automático (compactação, fallback, atualização) | o sistema muda de comportamento sem release, sem changelog, sem ninguém mexer |

### Os três padrões perigosos

- **Permissivo:** o produto vem configurado para "funcionar rápido" — rede
  ligada, sandbox amplo, timeout longo — e o time nunca revê.
- **Herdado:** a configuração foi copiada de outro projeto e carrega decisões
  que não se aplicam.
- **Invisível:** o valor efetivo vem de uma variável de ambiente na máquina de
  uma pessoa, versionada em lugar nenhum.

### O método em um princípio

> **Nunca confie no valor que você escreveu; confie no valor efetivo.**

Auditar configuração é comparar o que o harness **realmente usa** com o que o
repositório declara. A diferença é o seu passivo. Duas regras acompanham:
versione o que afeta custo/segurança/retenção (com **data de revisão**), e dê
**teste** a toda configuração importante — um teste que falha quando alguém
remove a negação de `git push` vale mais que qualquer documentação.

---

## O exemplo real: as configurações da fábrica

O `proj_fabrica-de-livros` é portátil entre múltiplas IDEs — e isso o obriga a
viver exatamente este capítulo. Cada tool lê configuração de um lugar
diferente:

| Camada de precedência | Onde mora na fábrica |
|---|---|
| Instrução (estável) | `AGENTS.md` (fonte única; hardlink para `CLAUDE.md`) |
| Regras do produto | `.cursor/rules/fabrica-agentica.mdc`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md` |
| Hook do harness | `.claude/settings.json` e `.opencode/plugins/fabrica-hooks.ts` |
| MCP servers | `.mcp.json`, `.cursor/mcp.json`, `.vscode/mcp.json`, `opencode.json` |

A seção 6 do AGENTS.md define quem é **fonte** (`.claude/`) e quem é
**junction/link** derivado (`agentic/*`, `.opencode/*`, `.agents/*`). É o
princípio do capítulo em carne e osso: **uma fonte versionada, várias
configurações derivadas** — e a divergência entre elas é o passivo
(`scripts/sincronizar-mcp-*.mjs` existem justamente para comparar e
reconciliar, sem sobrescrever decisões manuais).

E as configurações silenciosas do livro aparecem aqui com consequência real:

- **`console_utf8()` em todo script Python** (seção 0.11 do AGENTS.md): sem
  isso, `print` com emoji quebra em cp1252. Uma configuração que "funciona até
  o dia que não funciona", sem aviso.
- **`model: inherit` (R6):** nenhum agente fixa modelo. A escolha é camada de
  configuração, não texto de agente.
- **Hook git `pre-commit`** mecanizando R16: bloqueia commit se a suíte
  falhar. É um teste de invariante de pé: "commit vermelho NÃO acontece".
- **`scripts/setup-links.ps1` / `setup-links.sh`** recopiam o hook após clone —
  porque `.git/hooks` não aceita hardlink/junction de forma confiável. Uma
  decisão de distribuição que, esquecida, silenciosamente desarma o R16.
- **`.agents/` recebe só `agents/` e `commands/` (somente `.md`):** skills e
  MCP servers NÃO vão lá, porque o Codebuff/Freebuff **importa e executa**
  `.js`/`.mjs` encontrados ali — `compilar-livro.mjs` rodaria na importação e
  derrubaria o CLI. Uma configuração que, no lugar errado, vira execução
  automática — a "superfície de ataque por conveniência" do capítulo.

A auditoria de oito perguntas deste dia, aplicada à fábrica, tem resposta
declarada para quase todas: o vetor de resposta é o próprio AGENTS.md, que é
**versionado, testado (gates + pre-commit + `auditar-obra.py --estrito`) e com
data** no histórico do repositório.

---

## Mão na massa

### Tarefa 1 — descubra o valor efetivo, não o declarado

```bash
# Dump da configuração efetiva do harness (adaptar ao seu)
agent config dump --json > /tmp/efetiva.json

# Compare com o que está versionado no projeto
python - <<'EOF'
import json
from pathlib import Path

efetiva = json.loads(Path("/tmp/efetiva.json").read_text(encoding="utf-8"))
projeto = json.loads(Path(".agent/settings.json").read_text(encoding="utf-8"))

for chave, valor in sorted(projeto.items()):
    real = efetiva.get(chave, "<ausente>")
    marca = "OK " if real == valor else "DIF"
    print(f"[{marca}] {chave}: projeto={valor!r} efetiva={real!r}")
EOF
```

Toda linha `DIF` é passivo: alguém opera com valor diferente do que o time
escreveu. O `DIF` mais comum: variável de ambiente herdada do shell.

### Tarefa 2 — a auditoria em oito perguntas

| # | Pergunta | Resposta saudável |
|---|---|---|
| 1 | Qual é o valor efetivo da precedência? | testado, não presumido |
| 2 | Qual é o teto de tokens de saída? | declarado e compatível com o maior artefato |
| 3 | Qual é o timeout por ferramenta? | maior que o p95 real da operação mais lenta |
| 4 | O agente tem acesso à rede? | negado por padrão; permitido por exceção |
| 5 | Há leitura de variáveis de ambiente sensíveis? | negada |
| 6 | O histórico é gravado em disco? Por quanto tempo? | política de retenção documentada |
| 7 | Há compactação ou fallback automático? | limiar conhecido e monitorado |
| 8 | Quem revisa essas decisões, e quando? | data de revisão registrada |

Vinte minutos. Em quase todo harness auditado pela primeira vez, encontra pelo
menos uma surpresa relevante.

### Tarefa 3 — transforme decisão em teste

Configuração importante precisa de verificação automática — o próximo a mexer
desfaz sem perceber:

```python
INVARIANTES = [
    ("permissions.deny", "Bash(git push*)", "push deve ser proibido para agentes"),
    ("permissions.deny", "Write(migrations/*)", "migracao nao pode ser editada a mao"),
    ("limites.tokens_saida_max", 8000, "teto de saida precisa ser explicito"),
    ("rede.allow", False, "rede deve estar negada por padrao"),
    ("retencao.historico_dias", 30, "retencao declarada"),
]
```

O detalhe que faz valer: o teste não verifica se a chave **existe**, verifica
se o **valor** é o esperado. Configuração presente com valor errado é tão
perigosa quanto ausente.

### Tarefa 4 — registre a decisão, com data

```markdown
### 2026-09-12 — teto de saida em 8000 tokens
Motivo: maior artefato gerado tem ~6500 tokens; 8000 da margem sem truncar.
Revisar em: 2027-03-12 ou quando o maior artefato crescer 20%.
Dono: time de plataforma.
```

A data de revisão é o que impede que uma decisão boa para setembro vire uma
armadilha em março.

### Tabela de decisão: sintoma → configuração suspeita

| Sintoma | Configuração suspeita |
|---|---|
| Resposta cortada no meio | teto de tokens de saída |
| Operação legítima "falhou" com erro de rede | timeout por ferramenta |
| Comportamento muda entre máquinas | variável de ambiente herdada |
| Custo subiu sem mudar o volume | compactação ou fallback automático |
| Falta trilha para investigar incidente | nível de log e retenção |
| Segredo apareceu em log | leitura de ambiente e registro de payload |

### Tarefa 5 — preencha a matriz de exposição

Cinco linhas cobrem o que a documentação padrão omite. Linha em branco =
pendência real (aquela dimensão será decidida por acidente, provavelmente no
dia do incidente):

| Dimensão | Pergunta de controle |
|---|---|
| Credencial | Onde mora, como é injetada, quando roda? |
| Dados | O que entra no contexto e o que sai dele? |
| Histórico | O que fica gravado, onde e por quanto tempo? |
| Execução | Onde o código roda e o que ele alcança? |
| Publicação | O que vai para fora e com qual revisão? |

---

## Três regras que ficam com você

1. **Padrão de fábrica não é decisão.** Toda chave herdada relevante precisa
   ser reavaliada uma vez.
2. **Retenção é risco, não operação.** Definir prazo e expurgo automático é
   parte do projeto — arriscar em junho custa mais que decidir.
3. **Matriz de exposição com linha em branco é pendência.** O que não foi
   decidido será decidido por acidente.

## Erros de julgamento deste dia

- Confiar no declarado em vez do efetivo.
- Teto de saída copiado de outro projeto — trunca o artefato maior do seu.
- Rede habilitada "para testar" e nunca revista.
- Log sem retenção definida — existe para tudo, menos para a investigação que
  você precisa.
- Atualização automática sem revisão — comportamento muda sem release.
- Supor que "onde ficam as credenciais" tem resposta única — se varia entre os
  membros do time, a configuração não está sob controle.

**Antipadrão observável:** quando o time **culpa o modelo** por "alucinar"
dados que, na verdade, eram a resposta truncada de uma ferramenta — o harness
cavou o buraco e o modelo preencheu. A correção é config (explicitar o corte,
subir o teto, testar o invariante), nunca prompt.

---

## Checklist do dia

- [ ] Diff entre configuração efetiva e versionada executado.
- [ ] Oito perguntas respondidas, com surpresas anotadas.
- [ ] Dois testes de invariante escritos.
- [ ] Decisões de configuração registradas com dono e data de revisão.
- [ ] Truncamento de saída tornado explícito em todas as ferramentas.
- [ ] Matriz de exposição sem linha em branco.

## Para saber mais

- Seção 6 do `AGENTS.md` (Portabilidade Multi-IDE) — fonte vs junction vs
  link, e o que `.agents/` pode executar ao ser listado.
- `.claude/settings.json` e `.opencode/plugins/fabrica-hooks.ts` — hooks e
  decisões de precedência da fábrica.
- `scripts/sincronizar-mcp-vscode.mjs` / `sincronizar-mcp-opencode.mjs` —
  reconciliar geração e decisões manuais sem sobrescrever.

No Dia 15, você separa o que sobrevive a toda troca de ferramenta do que é
**moda**: os princípios universais, aplicáveis a qualquer harness.