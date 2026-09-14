# Dossiê — Blocos Temáticos 9 a 16 (Partes III e IV) + Métricas, Limites e Lacunas

---

## BLOCO 9 — O Orca CLI (Cap. 9)

**Fatos coletados** [35][36]

- Definição: "The Orca CLI is the `orca` command-line interface for scripting a running Orca
  editor from any shell. Use it to create and inspect worktrees, drive agent terminals, open
  files and diffs, automate the built-in browser, run scheduled automations, share HTML/
  Markdown artifacts, and control Orca-native tools from scripts or AI agents."
- "The `orca` CLI talks to a running Orca runtime" — ou seja, é um **cliente**, não um
  substituto do app.
- Instalação/registro: vem com o app desktop; registrar em `Settings → General → Orca CLI`
  (a página de referência cita também `Settings → Experimental → CLI`).
- Verificação: `command -v orca`; `orca status --json`; se o Orca não estiver rodando,
  `orca open --json` seguido de `orca status --json`.
- No macOS o registro instala um shim em `~/.local/bin`, que precisa estar no `PATH` [51].
- No Linux o binário do CLI chama-se `orca-ide` para não conflitar com o leitor de tela
  GNOME Orca [2].
- Regra de ouro: **`--json`** sempre que outra ferramenta for parsear; saída legível só para
  inspeção humana rápida [36].
- **Seletores**: aceitos no lugar de IDs longos [36]:
  - `id:<repoId>` / `path:/abs/path` / `branch:feature-name` / `issue:123`
  - `active` e `current` resolvem para o worktree gerenciado que contém o diretório atual.
  - "Use explicit selectors in scripts that may run outside the target worktree. For remote
    runtimes, prefer full server-side selectors such as `id:<repoId>::<absolute-worktree-path>`
    or `path:<absolute-server-path>` because the local shell's current directory may not exist
    on the runtime host."
- **Seleção de host**: `orca host list --json` inclui a própria máquina, alvos SSH
  registrados e servidores Orca pareados; `--host local`, `--host ssh:<target-id>`,
  `--environment <server-name>`. Rótulos SSH e nomes de servidor pareado também resolvem
  quando únicos; se um nome for colocado no flag errado, "Orca reports the matching machine
  and the flag to use instead of returning an empty result".
- **Comandos de runtime**: `orca open`, `orca status`, `orca serve` (inicia um servidor de
  runtime em primeiro plano **sem abrir a janela desktop**, para servidores remotos ou
  ambientes headless; encerra com `Ctrl-C`).
- **Repos**: `repo list`, `repo add --path`, `repo show --repo`, `repo set-base-ref --ref`,
  `repo search-refs --query --limit`. Conselho explícito: "Set the repo base ref before
  creating lots of worktrees so new tasks branch from the right place by default."
- **Worktrees**: `worktree list`, `ps`, `current`, `show`, `create`, `set`, `rm --force`.
  Flags de criação relevantes: `--agent` (lança o agente escolhido no primeiro terminal),
  `--prompt` (envia trabalho inicial ao agente), `--setup run|skip|inherit` (controla hooks de
  setup do repositório; `inherit` segue a política do repo), `--parent-worktree active` /
  `--no-parent`.
- **Terminais**: `terminal list|show|read|send|wait|create|split|rename|switch|close`.
  - Handles de terminal são **escopados ao runtime**: se o Orca reinicia ou o comando reporta
    handle obsoleto, rodar `orca terminal list --json` e readquirir.
  - `terminal list` reporta `executionHostId` quando verificável, mais um `hostScope` no nível
    do resultado com hosts cobertos e omitidos. "Treat a missing host identity or scope as
    unverifiable, not local. A missing terminal is evidence that it exited only when its
    execution host is listed in `hostScope.hostIds`."
  - `terminal read` retorna o stream acumulado com escapes removidos (programas que
    redesenham linhas podem aparecer como fragmentos empilhados); `--screen` traz o quadro
    atual renderizado, com `source` identificando `stream`, `screen` ou `screen-unavailable`;
    `--screen` e `--cursor` são mutuamente exclusivos. Para saída longa, usar leituras por
    cursor: salvar `nextCursor` de uma leitura de stream e reenviá-lo com `--cursor`.
  - Boa prática: "Read before sending when you are not sure what the terminal is waiting for."
- **Arquivos**: `file open`, `file diff --staged`, `file open-changed --mode both` (lê o
  `git status` e abre arquivos alterados em edição, diff ou ambos); caminhos relativos ao
  worktree selecionado.
- **Browser embutido**: comandos controlam a aba de browser do worktree selecionado — **não**
  controlam Chrome, Safari ou a UI do Orca. Loop obrigatório
  *snapshot → agir → snapshot*: `orca goto --url`, `orca snapshot --json` (devolve refs como
  `@e1`, `@e3`), `orca click --element @e3`, `orca fill --element @e1 --value`,
  `orca wait --text`, `orca screenshot`. Refs `@eN` vêm do snapshot e é preciso **nova
  snapshot** após navegação, troca de aba, cliques que mudam a página e qualquer erro de ref
  obsoleta. Comandos complementares: `tab list|create|switch`, `capture start`, `console`,
  `network`, `full-screenshot`, `pdf`, `set device --name "iPhone 12"`. `orca exec --command`
  é reservado a ações de browser sem comando tipado ainda.
- **Computer use**: `orca computer permissions|list-apps|get-app-state|click|set-value|
  type-text|press-key|hotkey|paste-text|scroll|drag|perform-secondary-action`, com suporte a
  `--window-id`, `--element-index`, `--x/--y` e stdin para segredos [41].
- **Emulador mobile**: `orca emulator list|attach|tap|type|gesture|button|rotate|exec|kill|
  shutdown`, escopados ao worktree ativo, com coordenadas **normalizadas de 0 a 1** [36][45].
- **Artifacts**: `orca artifacts share|update|list|delete` — publica HTML ou Markdown como
  links públicos de visualização pela conta Orca assinada; publicação é opt-in em
  `Settings → Artifacts` [35][49].
- **Skills**: `orca skills install|update|list|get|show|installed|share` (ver Bloco 11) [38].
- **Automações**: `orca automations create|list|show|edit|run|runs|remove` [40].
- **Linear**: superfície `orca linear` usada por agentes via skill `orca-linear`; preferir
  `--json`; worktrees vinculados resolvem com `--current` [36].
- Receita oficial para entregar trabalho: "Read before sending", usar `--json`, e não inventar
  flags de memória — carregar o guia da versão com `orca skills get <topic>` [38].

---

## BLOCO 10 — Orquestração supervisionada (Cap. 10)

**Fatos coletados** [37]

- Definição: "Orchestration is Orca's structured multi-agent layer: a Run (namespace +
  coordinator inbox), Tasks, Dispatches, supervised workers, messages, and decision gates."
- **Quando usar** (tabela de decisão da própria doc):
  - Para prompts pontuais: `orca terminal send`.
  - Para handoffs completos de propriedade sem supervisão: comandos de worktree/terminal da
    skill `orca-cli`.
  - Para orquestração estruturada com propriedade, rastreio de conclusão ou DAG: Run + Tasks +
    workers.
- Pré-requisitos: habilitar orquestração em `Settings → Experimental`; o CLI fala com o
  runtime em execução, então `orca status --json` precisa funcionar antes.
- **Comandos legados aposentados**: `orca orchestration run` e `run-stop` (e
  `coordinator-start` / `coordinator-stop`) **não produzem efeito**; retornam texto de
  recuperação apontando para `orca skills get orchestration --full`. O fluxo correto é
  Run + worker-start.
- **Modelo de dados**:
  - **Run** — namespace durável e caixa de entrada principal. "Never schedules or places
    workers."
  - **Task** — item com spec, dependências e status: `pending`, `ready`, `dispatched`,
    `completed`, `failed`, `blocked`.
  - **Dispatch** — uma tentativa da task em um terminal; autoridade de ciclo de vida sobre
    `worker_done` / `heartbeat`.
  - **Message** — correio da caixa de entrada: `status`, `dispatch`, `worker_done`,
    `escalation`, `question`, `heartbeat`, entre outros.
  - **Decision gate** — pergunta de propriedade do coordenador que bloqueia a task até ser
    resolvida.
  - "Completion authority comes from the active dispatch context. Worker completion and
    heartbeat messages should include both taskId and dispatchId."
- **Loop supervisionado preferido** (sequência literal da doc):
  ```bash
  orca orchestration run-create --objective "Split checkout QA and summarize blockers" --json
  orca orchestration task-create --spec "Audit billing settings for mobile layout" --task-title "Billing audit" --json
  orca orchestration worker-start --task <taskId> --worktree current --agent codex --json
  # ou, em worktree novo:
  orca orchestration worker-start --task <taskId> --worktree new-child --name billing-audit --agent codex --setup run --json
  # modelo/esforço por worker (apenas Claude, Codex, Cursor; não com --terminal):
  orca orchestration worker-start --task <taskId> --worktree current --agent claude --model <opaque-model-id> --effort high --json
  ```
- **`--model`** aceita IDs opacos do provedor para Claude, Codex e Cursor. **`--effort`** exige
  `--model` e só se aplica quando aquele agente/modelo suporta o nível. Nenhum dos dois pode
  combinar com `--terminal` (reuso de painel existente). "Overrides apply to that launch only
  and show under `launch.requested` / `launch.effective` in the start receipt. Federated starts
  need a worker host that advertises launch-preference support."
- **Espera por conclusões** (mensagens são consumidas em *Delivery*, do mais antigo para o mais
  novo; replay até `--ack`):
  ```bash
  orca orchestration check --wait --types worker_done,escalation,question --timeout-ms 900000 --json
  orca orchestration check --ack <deliveryId> --wait --types worker_done,escalation,question --timeout-ms 900000 --json
  ```
- **Conclusão pelo worker** (do painel do worker, com IDs injetados):
  ```bash
  orca orchestration send \
    --type worker_done \
    --subject "Completed mobile audit" \
    --body "Fixed footer overlap; no follow-ups." \
    --task-id <taskId> \
    --dispatch-id <dispatchId> \
    --outcome succeeded \
    --files-modified "src/app/settings/Billing.tsx" \
    --json
  ```
  `worker_done` exige `--outcome succeeded|failed`.
- **Inspeção e recuperação**: `worker-show --dispatch`, `worker-read --dispatch --limit`,
  `worker-stop --dispatch`, `worker-release --dispatch` (arquiva a saída inspecionável e fecha
  **apenas** aquele terminal de agente de propriedade do coordenador), `worker-retain
  --dispatch` (mantém um worker parado vivo para depuração quando o usuário pediu para
  retê-lo). A doc alerta: "Do not leave completed worker terminals open just to re-read output
  — use `worker-read` after `worker-release`. Do not substitute a broad terminal close when
  release returns `release_pending` or `release_unknown`; follow the receipt's recovery action."
  Retentativa é explícita: `worker-start --retry-of <dispatchId>` — "`--retry-of` does not
  inherit `--on`/worktree".
- **Workers federados** (opcional, entre hosts):
  ```bash
  orca orchestration worker-start --task <taskId> --on windows --worktree new-top-level \
    --repo <exact_remote_repo_selector> --name remote-worker --agent codex --setup run --json
  orca orchestration send --to dispatch:<dispatchId> --subject "Follow-up" --body "…" --json
  ```
  "Later commands route by Dispatch ID; do not repeat `--on`."
- **Dispatch de baixo nível** (topologia customizada):
  ```bash
  orca worktree create --name billing-audit --agent codex --json
  orca terminal wait --terminal <workerHandle> --for tui-idle --timeout-ms 60000 --json
  orca orchestration dispatch --task <taskId> --to <workerHandle> --inject --json
  ```
- **Regras de mensageria**: o check padrão é a Delivery não confirmada mais antiga do Run
  vinculado (FIFO); `--peek` / `--all` **não** consomem correio. Endereços de grupo: `@all`,
  `@idle`, `@claude`, `@codex`, `@opencode`, `@gemini`, `@droid`, `@grok`, `@cursor`,
  `@worktree:<id>` — **nunca** para `worker_done` / `heartbeat`. No PowerShell, colocar
  endereços de grupo entre aspas (`--to "@all"`). Durante uma espera ativa, o CLI emite
  pequenas linhas JSON de heartbeat no **stderr** a cada **15 segundos**; o stdout permanece o
  resultado final do comando.
- **Contrato do worker** (preâmbulo injetado no worker despachado):
  1. Enviar `worker_done` **exatamente uma vez**, mesmo em falha, com `--outcome`.
  2. Incluir um `--body` curto: o que foi feito, o que foi encontrado, o que resta.
  3. Incluir **ambos** os IDs (task e dispatch) para que retentativas obsoletas não concluam o
     dispatch errado.
  4. Enviar mensagens de `heartbeat` durante trabalho longo.
  5. Usar `orca orchestration ask` para perguntas bloqueantes em vez de prompts locais de TUI.
  ```bash
  orca orchestration ask --to <coordinatorHandle> \
    --question "Should I update the shared component or only this page?" \
    --options "shared,page-only" --timeout-ms 600000 --json
  ```
  Com `--json`, `ask` imprime um único objeto JSON, permitindo `jq -r .answer`.
- **Decision gates** (para DAGs): `ask` é worker→coordenador; gates explícitos bloqueiam uma
  task até que uma decisão seja registrada:
  ```bash
  orca orchestration gate-create --task <taskId> \
    --question "Merge the shared button change into the task branch?" \
    --options '["yes","no"]' --json
  orca orchestration gate-resolve --id <gateId> --resolution "yes" --json
  ```
- **Recuperação**: `dispatch-show --task`, `dispatch-show --preamble`, `task-list`,
  `task-update --id --status blocked --result '{"reason":"waiting on credentials"}'`.
  Reset somente ao abandonar intencionalmente o estado: `orca orchestration reset --tasks`,
  `--messages`, `--all` — "reset affects runtime-global orchestration state. Do not run it while
  another coordinator is active unless that is the intended cleanup."
- **Rastreabilidade na UI**: "Task IDs printed in terminals, such as `task_...`, are clickable
  links. Clicking one asks the Orca runtime for the task's current dispatch and focuses the
  assigned terminal, including when the task lives in a remote or SSH runtime."
- Release v1.4.200 reforça a evolução da área: "Orchestration: Worker-terminal ownership is
  established at creation. Startup, mobile input, and older federation coordinators have
  additional recovery safeguards" [66].
- Existe também a skill local de orquestração (`npx skills add ... --skill orchestration`),
  cujo aviso é explícito: "Always load `orca skills get orchestration --full` before mutating
  orchestration state — the legacy orchestration run command is retired" [38].

---

## BLOCO 11 — Skills, MCP, memória e checkpoints (Cap. 11)

**Fatos coletados** [38][16][39]

- **O que são as skills do Orca**: "Orca ships skills that agents install into their skill
  directories. Public install packages are hybrid discovery stubs: short `SKILL.md` files that
  tell the agent when to engage Orca and how to load the full guide from the running CLI.
  Command flags live in the binary so they cannot drift from the app version."
- **Registro instalável** (7 skills): `orca-cli` (worktrees, terminais, arquivos, automações,
  browser embutido), `orchestration` (Runs, tasks, workers supervisionados, mensagens, gates),
  `computer-use` (apps desktop via árvores de acessibilidade), `orca-linear` (leitura/escrita
  de tickets), `orca-emulator` (iOS Simulator), `orca-emulator-android` (emulador/dispositivo
  Android via adb), `orca-per-workspace-env` (recipes de ambiente por workspace).
- Instalação: `npx skills add https://github.com/stablyai/orca --skill <nome> --global`.
  "Default agent setup usually installs `orca-cli`, `computer-use`, and `orchestration`."
- **Stub híbrido** — comportamento declarado para o agente: (1) resolver o executável do CLI
  para a sessão (`ORCA_CLI_COMMAND`, `orca-dev`, `orca-ide` no Linux, senão `orca`);
  (2) carregar o guia completo com `orca skills get <topic>` (`--full` para o guia longo);
  (3) preferir `--json` e **não inventar flags de memória**.
- Comandos de consulta: `orca skills list`, `orca skills get orca-cli`,
  `orca skills get orchestration --full`, `orca skills get orca-linear --json`;
  `skills show` é alias de `skills get`.
- **Atualização**: o app avisa quando um pacote mais novo existe, pode abrir *Update skills*
  (lista de instalações e motivos de skip) e rodar
  `npx --yes skills update <names> --global -y` de forma headless, **em background** (fechar o
  diálogo não cancela a execução, com progresso em segmento da barra de status). Equivalente
  manual: `npx skills update orca-cli orchestration computer-use --global`.
- **Hosts headless** (SSH, containers, CI, `orca serve`) sem UI de Settings usam os wrappers
  locais, que resolvem os mesmos comandos npx, acrescentam flags não interativas e **não
  exigem runtime do Orca rodando**: `orca skills install` (lista nomes instaláveis),
  `orca skills install --skill orca-cli --skill orchestration`,
  `orca skills install --skill orca-cli --agent claude-code,codex`, `orca skills install --all
  --dry-run`, `orca skills update --all`, `orca skills update --skill orca-cli --dry-run`.
  O escopo padrão é global (`--global`); `--local` limita ao projeto atual. `install` mira os
  agentes detectados no host (mais o diretório compartilhado `.agents/skills`), com
  `--agent <name>` ou `--agent universal` para sobrepor; `--dry-run` imprime o comando
  resolvido e `--json` só é válido com listagem / `--dry-run`. `update` só atualiza skills já
  instaladas.
- **Compartilhar skills privadas**: `Skills → Share skills` publica uma skill ou um bundle
  atrás de **um único link não listado e revogável** (requer conta Orca). É possível revisar
  arquivos incluídos, scripts, executáveis, digest e notas de versão antes de publicar;
  **cada versão publicada é imutável**, então edições locais posteriores não alteram o que os
  destinatários instalam. "Anyone with an active link can inspect and install the shared skills
  without signing in, so treat the link like a credential." O destinatário escolhe todas ou um
  subconjunto, e o escopo global ou de workspace nesta máquina, em runtime Orca pareado, WSL ou
  host SSH; skills modificadas existentes ficam em *Keep local* por padrão.
  `Skills → Manage installs` permite atualizar, reverter ou remover; `Settings → Share Skills`
  copia ou revoga links ativos — revogar bloqueia acesso futuro mas **não remove cópias já
  instaladas**.
- Publicação por agentes exige permissão separada, desligada por padrão
  (`Settings → Share Skills → Allow agents and the Orca CLI to publish skill links`); depois:
  `orca skills installed --json` e
  `orca skills share --skill frontend --skill testing --bundle-name "Team Toolkit" --json`.
  `skills installed` devolve seletores seguros **sem expor caminhos locais**; `skills share`
  aceita IDs exatos de descoberta ou nomes inequívocos e **não** aceita caminhos arbitrários
  nem `--all`.
- **MCP**: a página de registro de skills é "Skills registry & MCP" — o Orca expõe suas
  capacidades a agentes por skills e por CLI, no padrão aberto Model Context Protocol, descrito
  como "an open-source standard for connecting AI applications to external systems [...] a
  USB-C port for AI applications" [38][64].
- **Memória do agente** [16]: `CLAUDE.md` (Claude) e `AGENTS.md` (Codex), na raiz ou
  aninhados, são preservados e editáveis inline; hooks por repositório (`.claude/`, `.codex/`)
  são lidos e executados; hooks de setup de worktree automatizam `pnpm install`, `direnv allow`
  e restauração de `.env`; hooks de status alimentam os indicadores da UI, com chave
  `orca agent hooks on|off|status --json` e endpoints persistidos em
  `{userData}/agent-hooks/endpoint.env` / `endpoint.cmd`.
- **Worktree checkpoints** [39]: "Every Orca worktree carries a lightweight, free-text comment
  field visible in the UI — a status snapshot of what the worktree is doing right now. Agents
  can update it from the CLI, and it's the pattern we recommend for keeping human collaborators
  in the loop without forcing chat."
  ```bash
  orca worktree set --worktree active --comment "reproduced auth failure; testing credential-chain fix" --json
  orca worktree set --worktree active --comment "fix implemented; running integration tests" --workspace-status in-progress --json
  ```
  Status de cartão: `todo`, `in-progress`, `in-review`, `completed` (ou um id custom do
  workspace). Momentos recomendados para checkpoint: fim de uma fatia significativa de
  implementação; hipótese confirmada ou refutada; revisão de código concluída; bloqueio
  atingido (espera por entrada externa, bug upstream, acesso ausente); transição de investigação
  para correção, ou de correção para verificação.
  **Formato**: a primeira linha é a ação — o que acabou de acontecer, onde, e o status ou
  próximo passo:
  ```bash
  orca worktree set --worktree active --comment "added debounce to SearchBar onChange (src/components/SearchBar.tsx); ready for review
  goal: reduce redundant API calls per #298" --json
  ```
  Boa prática obrigatória: "If the comment might have user-written context, read it first so you
  don't clobber goals or constraints" (`orca worktree current --json`); preservar o que continua
  válido, descartar o obsoleto e tecer a atualização.

---

## BLOCO 12 — Automações, notificações e artefatos (Cap. 12)

**Fatos coletados** [40][47][35][49]

- Proposta das automações: "Orca automations run a prompt on a schedule from the CLI, so
  recurring triage, review, and maintenance tasks can start without you opening a worktree by
  hand."
- Primeira automação segura (a doc recomenda criar **desabilitada** para calibrar prompt e alvo):
  ```bash
  orca automations create \
    --name "Weekday triage" \
    --trigger weekdays \
    --time 09:00 \
    --prompt "Triage new issues and summarize blockers" \
    --provider codex \
    --repo my-repo \
    --disabled \
    --json
  ```
- `--trigger` aceita presets (`hourly`, `daily`, `weekdays`, `weekly`), expressões **cron** e
  strings **RRULE**; `--timezone <tz>` fixa fuso IANA em vez do padrão do runtime.
- **Alvo**: `--repo <selector>` quando cada execução deve criar/selecionar trabalho em um
  repositório; `--workspace <selector>` quando deve rodar dentro de um worktree existente.
  Omitindo ambos, "Orca resolves the enclosing worktree from the current shell directory when
  it can".
- **Precheck** — pula trabalho agendado quando uma sonda de shell barata falha (saída não-zero
  registra execução *skipped*):
  ```bash
  orca automations create --name "PR review" --trigger hourly \
    --precheck "gh pr list --json number -q .[0].number" \
    --prompt "Review requested PRs" --provider codex --repo my-repo --disabled --json
  ```
- Alvos de host/projeto: `--project <projectId>` + `--host <hostId>`, ou
  `--project-host-setup <id>` quando já existe um setup; `--source-context '<json>'` fixa dados
  de task/provider a um host/conta (`null` limpa na edição).
- **Multi-host**: a página de automações carrega agendamentos desta máquina e de hosts Orca
  conectados suportados em uma única tabela, com coluna *Host* e filtro por host. Ao criar na
  UI, *Create on* escolhe o host **antes** do projeto. Hosts que precisam de servidor mais novo
  permanecem visíveis porém desabilitados, com mensagem *Update server*.
- **Grace de execução perdida**: `orca automations edit <id> --missed-run-grace-minutes 30 --json`.
- **Reuso de sessão**: `--reuse-session` faz execuções seguintes continuarem no terminal de
  automação vivo anterior em vez de começar de um terminal em branco;
  `--fresh-session` reverte para terminal novo por execução.
- Revisão antes de habilitar: `orca automations list --json`,
  `orca automations show <id> --json`, `orca automations edit <id> --enabled --json`.
  Execução sob demanda: `orca automations run <id> --json` e
  `orca automations runs --id <id> --json`. Se uma execução falha antes de abrir workspace ou
  reconectar ao alvo, abrir a execução no Orca e clicar *Rerun`.
- Navegação por teclado na lista e nos detalhes: `Enter` abre o item selecionado,
  `ArrowUp`/`ArrowDown` percorrem o histórico de execuções (ou a seleção na lista),
  `ArrowLeft`/`ArrowRight` alternam *Overview* e *Runs*, `Escape` volta à lista.
- Automações externas em host SSH continuam gerenciáveis (inclusive exclusão) mesmo com o host
  desconectado — "you do not need an active SSH session just to remove a schedule".
- **Notificações**: ver Bloco 7 (agente-concluído, sino persistente, badge no Dock do macOS,
  marcar como não lida, categorias desligáveis, sons customizados em MP3/WAV/OGG/M4A/AAC/FLAC
  com volume) [47].
- **Activity**: página dedicada de atividade/feed, complementando notificações e o feed de
  agentes da barra lateral [48][5].
- **Artifacts**: `orca artifacts share|update|list|delete` publica HTML/Markdown como link
  público de visualização pela conta assinada; opt-in em `Settings → Artifacts`; no browser do
  worktree há a ação *Share as artifact* com **limite de 10 MiB por arquivo** e sem upload de
  assets relativos [35][32][49].
- **Clipboard e contexto**: `Copy Context` (transcrição limitada do painel) e `Copy Session ID`
  no menu de contexto do terminal [20].

---

## BLOCO 13 — Computer use e emuladores (Cap. 13)

**Fatos coletados** [41][36][45]

- Proposta: "The `orca computer` CLI lets an agent inspect and control native desktop apps —
  list running apps, read accessibility trees, click controls, set values, type text, scroll,
  and take screenshots. Use it when a task needs to operate the OS or a third-party app rather
  than a terminal or the built-in browser."
- Estágio: **Beta**; traz helpers nativos por plataforma e exige permissão de **Acessibilidade**
  (e, no macOS, **Gravação de Tela**). "The command surface is stable enough for skills to build
  against, but flag names may still shift."
- Setup: `orca status --json`, `orca computer permissions --json`,
  `orca computer capabilities --json`; se faltar permissão, conceder nas Configurações do
  Sistema e reexecutar `permissions --json` para confirmar.
- **Loop snapshot → agir → snapshot**: ler o estado atual do app, agir sobre um elemento
  específico, reler o estado para verificar o resultado.
  ```bash
  orca computer list-apps --json
  orca computer get-app-state --app com.spotify.client --json
  orca computer click --app com.spotify.client --element-index 42 --json
  ```
- Regra crítica: "Element indexes are scoped to the latest `get-app-state` result and may be
  sparse. In `--json` output, read the tree from `result.snapshot.treeText`. Do not invent
  indexes from `elementCount`. Refresh state after navigation, focus changes, scrolling, or any
  app re-render before reusing an index."
- **Apps com múltiplas janelas**: `orca computer list-windows --app <id> --json` e uso de
  `--window-id <id>` (preferir id estável) ou `--window-index`.
- **Seleção de app**: preferir bundle IDs de `list-apps`; nomes funcionam quando inequívocos
  (`--app Spotify`); `--app pid:<number>` só quando bundle ID e nome colidem.
- **Ações disponíveis**: `click`, `set-value`, `type-text`, `press-key`, `hotkey`,
  `paste-text`, `scroll`, `drag`, `perform-secondary-action`. Recomendação explícita: "Prefer
  semantic actions (`click`, `set-value`, `perform-secondary-action`) over raw `type-text` or
  `press-key` — they target accessibility elements directly and survive focus changes that
  keyboard input doesn't." Quando o alvo por acessibilidade falha, há fallback por coordenadas
  (`--x`/`--y`, `--from-element-index`/`--to-element-index`).
- **Entrada sensível**: passar segredos por stdin para não ficarem no histórico do shell:
  `printf '%s' "$TEXT" | orca computer set-value --app <app> --element-index 7 --value-stdin --json`;
  `--text-stdin` faz o mesmo para `type-text` e `paste-text`.
- **Screenshots**: `get-app-state` devolve árvore de acessibilidade e, por padrão, um
  screenshot; com `--json` os bytes vão para disco e o caminho volta em `screenshot.path`
  (em vez de embutido na resposta). `--no-screenshot` evita pixels (mais rápido e menor);
  `--restore-window` traz janela oculta ou minimizada para a frente antes da captura.
- Skill: `npx skills add https://github.com/stablyai/orca --skill computer-use` [38].
- **Emulador iOS** [36][45]: ponte escopada ao worktree ativo, para que agentes e scripts
  anexem um simulador, toquem em coordenadas normalizadas, digitem, enviem gestos, girem o
  dispositivo e o encerrem sem sair do Orca:
  ```bash
  orca emulator list --json
  orca emulator attach "<device-name-or-udid>" --json
  orca emulator tap 0.5 0.7 --json
  orca emulator type "hello" --json
  orca emulator gesture '[{"type":"begin","x":0.5,"y":0.8},{"type":"move","x":0.5,"y":0.4},{"type":"end","x":0.5,"y":0.2}]' --json
  orca emulator rotate landscape_left --json
  ```
  `--device <udid-or-name>` ou `--emulator <id>` quando o script precisa de alvo explícito.
- **Duas decisões de fronteira** que a doc deixa explícitas: o browser embutido **não** controla
  Chrome, Safari ou a UI do Orca — é preciso `computer use` para apps desktop e `browser` para
  páginas; e `orca computer` é para apps nativos fora do browser embutido [36][41].

---

## BLOCO 14 — Rodando remoto (Cap. 14)

**Fatos coletados** [42][43][44][55]

- Premissa: "Orca is not locked to your laptop. Every worktree runs somewhere — on the machine
  in front of you, on a box you already own, on a shared always-on server, or on a fresh cloud
  VM spun up for that one workspace."
- **Quatro modos** (tabela oficial):

  | Modo | Onde vivem arquivos e agentes | Quem é dono da máquina | Melhor para |
  |---|---|---|---|
  | Local | Seu desktop | Você | Dia a dia, iteração rápida |
  | Alvo SSH | Host remoto via SSH | Você (ou o time) | Dev boxes, hosts GPU, VPS always-on |
  | Servidor Orca Remoto | Máquina rodando Orca desktop ou `orca serve` | Você (ou o time) | Runtime compartilhado persistente, mobile, automação |
  | VM de nuvem / ambiente por workspace | VM/sandbox descartável por workspace | Sua conta de nuvem (BYO) | Computação de agente isolada e efêmera |

  E a fronteira de negócio: "Orca does not sell managed VPS hosting. Remote modes always use
  machines and cloud accounts you control."
- **SSH** [43]: "Orca can drive agents on remote machines over SSH — useful for long-running
  builds, GPU boxes, or any environment where your laptop isn't the right place to run the
  work." Quando o worktree é criado com alvo SSH, o Orca cria o `git worktree` **no host
  remoto**, roda os agentes remotamente e sincroniza eventos de arquivo para que editor, diff
  e browser continuem parecendo locais.
  - Adição de alvo: `Settings → SSH` → *Add Target* (formulário em modal); campos host, user,
    port e identity file opcional, ou seletor do `~/.ssh/config` (incluindo arquivos
    `Include`) que pré-preenche o formulário; hosts já salvos mostram badge *In Orca*.
    Chave com passphrase gera prompt na primeira vez. *Test* verifica conectividade, *Save*
    grava. Formulários sujos ignoram cliques fora para não descartar campos.
  - **Verificação de host key**: o Orca confere conexões contra os arquivos `known_hosts` do
    OpenSSH e chaves que ele mesmo salvou; correspondências existentes conectam em silêncio.
    Na política padrão, aceita e memoriza um host no primeiro contato exibindo a impressão
    digital; `StrictHostKeyChecking yes` rejeita hosts desconhecidos; `no`/`off` aceita sem
    gravar registro de confiança. "A changed, revoked, or unexpectedly different key type is
    rejected before Orca asks for a password or key passphrase." Em caso de mismatch, o Orca
    fornece o comando `ssh-keygen -R` apropriado.
  - Opções avançadas: proxy, jump host e override de multiplexação; *Reuse SSH connection*
    (ligado por padrão) usa reuso de conexão OpenSSH no macOS e Linux para que comandos de
    setup não paguem um novo handshake cada; desligar apenas em hosts que rejeitam sessões
    multiplexadas.
  - Passphrases ficam em memória pelo tempo da sessão do Orca (limpas ao fechar), com TTL maior
    opcional.
  - **Status**: chip com estado vivo — verde conectado, amarelo reconectando, vermelho
    desconectado. "Disconnects don't kill running agents; Orca reconnects and re-attaches,
    replaying scrolling output and restoring full-screen app panes from their rendered frame
    instead of returning them blank or fragmented." Cartão de workspace afetado mostra controle
    inline *Connect*/*reconnect*. Falha de relay do tipo "Multiplexer disposed" é recuperada
    automaticamente. Estado de agente (working/idle/blocked) propaga por SSH como localmente.
  - **Sessões sobrevivem ao fechamento do app**: "Remote terminal sessions are leased through
    the relay running on the remote host, so they survive Orca closing on your laptop." Ao
    reabrir e reconectar, PTYs (*pseudo-terminais*) alugados voltam às suas abas no estado
    anexado, com scrollback intacto; há **período de graça de 5 minutos por padrão**,
    configurável por alvo, antes de encerrar sessões desanexadas.
  - Download de arquivos/pastas por clique direito no explorador SSH: *File → Download* e
    *Folder → Download Folder* (recursivo, apenas desktop). "Folder download appears only when
    the connection advertises recursive folder transfer (typically full SFTP)."
  - Abertura de worktrees SSH em VS Code Remote-SSH e uso de arquivos/git mesmo quando o remoto
    não compila nativos de terminal — nesse caso, instalar ferramentas de build
    (`make`, `g++`/`clang++`, `python3`) para que shells funcionem [43][51].
- **Servidor Orca Remoto** [44]: um computador faz o trabalho e outro dá a interface. "The server
  keeps the projects, worktrees, terminals, tabs, provider accounts, and agent sessions. Your
  laptop connects to that running Orca instance."
  - Caminho recomendado: app desktop nos dois computadores + **Tailscale** na mesma tailnet
    (endereço privado começando tipicamente em `100.`); não é preciso `orca serve`.
  - Passos: no servidor, `Settings → Remote Orca Servers → Advertise this app as a server →
    New Link`, escolher o endereço Tailscale, *Generate Access Link* e copiar o link; no
    cliente, `Add Server`, nome reconhecível e colar o link. "The pairing URL grants access to
    this Orca runtime. Treat it like a password and send it only to the client you intend to
    pair."
  - Adicionar um servidor **não** força todo projeto novo nele; `Advanced → Active Server` torna
    o roteamento padrão quando desejado.
  - **Segurança**: token separado e revogável por cliente em *Shared Server Access*; revogar
    desconecta clientes ativos imediatamente; gerar outro link substitui o anterior **não
    usado**, e clientes já pareados mantêm seus grants até revogação. Recomendações explícitas:
    manter ACLs de Tailscale o mais estreitas possível; **não** encaminhar a porta do Orca
    diretamente para a internet (preferir Tailscale, WireGuard, LAN confiável, encaminhamento
    SSH ou túnel autenticado); **não** escolher `127.0.0.1` para outro computador.
  - `orca serve --pairing-address <ip-ou-hostname-tailscale>` para host headless ou VM gerenciada
    por serviço, por exemplo `orca serve --pairing-address 100.64.1.20`.
  - Contas em host headless: `orca account add --agent claude`, `orca account add --agent codex`,
    `orca account list` (o cliente remoto **desabilita** *Add account*); skills sem UI:
    `orca skills install --skill orca-cli --skill orchestration` e `orca skills update --all`.
  - O que muda na prática: agentes continuam rodando quando o laptop cliente dorme ou
    desconecta; o servidor precisa do repositório, ferramentas e credenciais; precisa
    permanecer acordado e conectado à tailnet; reconectar devolve o workspace, aba e estado de
    painéis do servidor sem duplicar abas pareadas; projetos apagados no servidor desaparecem
    de todos os clientes pareados.
  - Beta declarado: "Keep the server and client on a private network path you control, such as
    the same Tailscale tailnet or LAN."
  - Comparativo oficial SSH × Servidor Orca Remoto: dono do runtime (laptop Orca × máquina
    remota), desconexão (agentes seguem no host e o laptop reanexa × estado completo vive no
    servidor), multi-cliente (um laptop dirige o host × laptop, web, mobile e automação
    compartilham o mesmo runtime) e configuração típica (importar config SSH e escolher *Run
    on* × compartilhar o servidor ou rodar `orca serve` e parear por URL).
- **VM de nuvem / ambiente por workspace** [42]: "Each worktree can boot its own on-demand
  environment — a cloud sandbox, VM, or local Docker container — from a recipe checked into the
  repo (`orca.yaml` + lifecycle scripts). Create spins it up; suspend/resume/destroy tear it
  down. Orca is a thin wrapper: your provider account, images, and billing stay yours."
  - Na UI o rótulo é *Cloud VM* sob `Settings → Experimental`; recipes continuam criando
    ambientes por workspace.
  - Provedores citados como usados hoje: **Vercel Sandbox, Fly, Modal**, hosts SSH simples e
    **Docker local**. A conexão é por (a) servidor Orca — a recipe inicia `orca serve` e devolve
    uma URL de pareamento — ou (b) SSH — a recipe devolve detalhes de conexão que o Orca disca.
  - Fluxo: habilitar *Cloud VM* em `Settings → Experimental`; instalar/atualizar a skill
    *Cloud VM / per-workspace environment*; pedir ao agente "Use the `orca-per-workspace-env`
    skill to set up a per-workspace environment for this repo" — a skill percorre pré-requisitos
    → snapshot base → autenticação do agente → recipe em `orca.yaml` → validação com `doctor`.
  - Regra operacional peculiar: "Recipes only show up for workspace create once the
    `environmentRecipes` entry is on the project's primary checkout of `orca.yaml` (not only a
    feature branch). Doctor and live provision can still run from any branch while you iterate
    on scripts."
  - Fronteira: "Cloud VMs do not give you an Orca-hosted VPS. You bring the provider (and pay
    that provider)."
- **Como escolher** (heurística oficial): ficar local se o laptop é rápido o suficiente e os
  agentes são de vida curta; SSH se já existe VPS/dev box e se quer agentes lá sem instalar um
  segundo runtime Orca; Servidor Orca Remoto se se quer um runtime Orca always-on para mobile,
  browser e automação; VM de nuvem/ambiente por workspace se cada tarefa deve ganhar um sandbox
  novo definido por recipe que morre com o worktree. "You can mix modes in one install: local
  worktrees for quick edits, SSH for a GPU box, and a recipe for CI-like isolation."

---

## BLOCO 15 — Mobile, telemetria, configuração e segurança (Cap. 15)

**Fatos coletados** [45][46][50][49][68][67]

- **Mobile**: "Monitor and steer your agents from your phone — get notified when an agent
  finishes and send follow-ups from anywhere" [65]. Distribuição: **App Store**, **TestFlight**
  e **APK Android 0.0.48** [65][46]. A doc de mobile [45] cobre reconexão às mesmas sessões de
  um servidor Orca remoto, o que exige runtime always-on. A lista de *Quick Commands* sincroniza
  com o companheiro mobile [20][49]. No servidor, `Settings → Agents → Keep computer awake` tem
  o controle explícito de manter a máquina acordada; o badge *Caffeinate* fica **oculto** em
  clientes web pareados [49].
- **Notificações no mobile**: a promessa central é ser avisado quando o agente termina e poder
  responder de qualquer lugar [65][47].
- **Telemetria**: existe página dedicada de telemetria [50], logo a coleta é uma preocupação
  documentada do produto. Controles de privacidade relacionados: *Share Skills* exige permissão
  explícita para agentes publicarem links [38]; *Artifacts* é opt-in em
  `Settings → Artifacts` [49].
- **Configuração como superfície de operação** [49]: tudo é pesquisável com `Cmd-,` e digitando
  uma palavra. Painéis: *General* (Orca CLI, Updates, Open in menu, UI zoom, Default
  new-worktree name, Editor Word Wrap), *Appearance* (tema, cor de acento, densidade, fonte da
  UI, minimapa, status bar com Resource Manager, percentuais de uso, ícone, idioma),
  *Git* (base ref padrão, assinatura de commit, editor externo, Auto-Rename Branch From Work,
  GitHub API Budget), *Terminal* (fonte, tema, cursor, padding, importações Ghostty/Warp, JIS,
  shell Windows, OSC 52), *Quick Commands* (com escopo e controle de cópia),
  *Agents* (agentes instalados, permissões, contas Claude/Codex, hooks de inicialização, hooks
  de status, Keep computer awake, freshness de skills), *Browser* (perfis, zoom padrão,
  defaults de Design Mode, devtools opt-in, obraspaces de servidor remoto, tráfego por SSH),
  *Notifications* (categorias e sons), *Shortcuts* (com overrides em
  `~/.orca/keybindings.json`), *Repository* (Worktree Shared Paths, Hooks), *SSH*, *Remote Orca
  Servers*, *Experimental* (Agent Dashboard, Agent hibernation, Cloud VM, CLI, orchestration),
  *Artifacts*, *Share Skills*.
- *Auto-Rename Branch From Work*: renomeia branches geradas com nomes de criatura depois que o
  agente começa a trabalhar [49].
- *Resource Manager* na barra de status: CPU, memória, sessões, controles de daemon e
  varreduras de disco por workspace — o instrumento natural para operar uma frota [49].
- **Governança e risco** [68]: o NIST AI RMF fornece o vocabulário de governança de risco de IA
  (mapear, medir, gerenciar, governar) que o operador de frota pode usar para justificar
  políticas: quais worktrees podem rodar com bypass de permissão, o que pode ser enviado a
  modelo externo, e como auditar o que foi gerado por IA (ligação direta com *Attribution* [27]).
- **Rede privada como pré-requisito de segurança** [67]: Tailscale é "a Zero Trust identity-based
  connectivity platform" que "enables encrypted point-to-point connections using the open source
  WireGuard protocol", criando uma malha peer-to-peer (tailnet) sem centralização; é o caminho
  recomendado pela doc do Orca para pareamento remoto [44].
- **Custo e licenciamento como decisão de arquitetura**: o Orca não vende modelos nem hosting —
  "bring your own Claude, Codex, or OpenCode subscription" [1][65]; VMs de nuvem são pagas ao
  provedor do operador [42]. A obra deve tratar essas duas faturas (assinaturas de agente +
  computação) como parte explícita do desenho da frota.
- **Enterprise**: existe página dedicada a uso corporativo [59], evidência de que o produto
  reconhece adoção em time, com as questões de governança, contas compartilhadas e auditoria
  que acompanham esse cenário [65].

---

## BLOCO 16 — Manutenção, diagnóstico e o playbook do operador (Cap. 16)

**Fatos coletados** [51][52][49][66][60][65]

- **Matriz oficial de problemas e correções** [51]:

  | Sintoma | Diagnóstico/correção documentada |
  |---|---|
  | Agente não inicia | Rodar a CLI do agente manualmente no terminal (se falhar ali, é auth/instalação da CLI, não do Orca); conferir `PATH` visível em `Settings → Agents`; usar o chip *Restart* |
  | Diff errado ou travado | Ícone de refresh na barra do diff (o Orca relê o worktree); operações de git externas (rebase, reset) podem acontecer entre refreshes |
  | Criação de worktree falha | O start-from ref pode não estar buscado — rodar `git fetch origin` no repositório; o diretório alvo pode já ter worktree daquela branch |
  | CLI "command not found" | Registrar em `Settings → General → Orca CLI`; no macOS o shim vai para `~/.local/bin`, que precisa estar no `PATH` |
  | SSH conecta mas terminais remotos falham | Confirmar Node e rede no remoto para a instalação do relay; no Linux instalar toolchain C/C++ (`make`, `g++`/`clang++`, `python3`) e reconectar |
  | SSH funciona para arquivos mas não para *Download Folder* | Download de pasta exige SFTP recursivo; alternativas: `tar`/`scp` por terminal |
  | *Open in VS Code* desabilitado ou só local | Usar worktree SSH (não runtime de servidor remoto ativo); definir o comando de abertura como VS Code/Insiders; atualizar alvos SSH se o host mudou |
  | Login Kerberos falha | Garantir ticket válido com `klist`; confirmar `GSSAPIAuthentication yes` no Host do OpenSSH e reimportar/retestar o alvo |
  | Browser diz `browser_no_tab` | Nenhuma aba aberta no worktree atual — abrir com `orca tab create --url ...` ou abrir o painel e navegar |
  | Performance e memória | Fechar worktrees não usados (cada um mantém file watchers vivos); layouts com muitas abas de browser são os maiores consumidores de RAM |
  | PR/Checks/Tasks com erro | Limites de taxa, auth de `gh`, escopos e acesso a repositório — ver [52]; checagens rápidas `gh auth status -h github.com`, `gh api user`, `gh api rate_limit --jq '.resources.core'` |

- **Logs e suporte**: `Help → Open Logs` abre o diretório de logs (anexar ao reportar bug);
  `Help → Send Feedback` aceita screenshots coladas ou arrastadas, com miniaturas antes do
  envio; issues e pedidos de recurso no GitHub; ajuda em tempo real no Discord [51]. A doc
  sugere anexar logs "when the bug is hard to reproduce" [51].
- **Cadência de releases e risco de versão**: releases estáveis são "vetted"; builds RC "ship
  new features first, often daily"; releases de v1.4.193 a v1.4.200 em sequência, sendo
  v1.4.200 de 11 set. 2026, e a nota de que "It usually takes 48–72 hours for a landed PR to be
  released (except P0+ fixes)" [2][66]. Consequência prática para o operador: o changelog é a
  lista real de features ("we ship daily, so this list is perpetually behind. The changelog is
  the real feature list") [65][60].
- **Retorno de versão**: versões antigas estão sempre no GitHub Releases e "Orca will not
  force-downgrade your worktree data if you go back" [2].
- **Dados de adoção e vitalidade** (para contexto de risco de escolha de ferramenta):
  **67,2 mil estrelas**, **4,4 mil forks**, releases praticamente diárias, app mobile ativo
  (APK Android 0.0.48) [65][66][46].
- **Higiene de frota recomendada pelo conjunto da doc** (síntese que a obra pode apresentar como
  playbook do operador): usar checkpoints de worktree para deixar estado legível [39]; habilitar
  hibernação para conter memória [15]; limitar worktrees abertos e abas de browser [51]; fixar
  worktrees de trabalho longo [4]; usar *Auto-Rename Branch From Work* para branches legíveis
  [49]; manter skills atualizadas para que as flags não divirjam da versão do app [38];
  revisar permissões por agente em vez de aceitar o bypass global [9]; e nunca encaminhar a
  porta do runtime remoto para a internet pública [44].

---

## 4. Métricas verificáveis extraídas da documentação (para o gate R-MT)

Todas as métricas abaixo têm valor, unidade e fonte; qualquer capítulo pode ancorar sua
métrica obrigatória em uma delas.

| Métrica | Valor | Fonte |
|---|---|---|
| Tempo declarado para a primeira sessão com três agentes | "under five minutes" | [3] |
| Agentes embarcados no seletor pré-configurado | mais de 30 CLIs | [9] |
| Agentes com integração profunda (uso, hot-swap, hooks) | 3 (Claude Code, Codex, Cursor CLI) | [9] |
| Janela padrão de ociosidade para hibernar um agente | 30 minutos | [15] |
| Faixa configurável da janela de hibernação | 1 minuto a 24 horas | [15] |
| Agentes com sessão retomável elegíveis à hibernação | 11 | [15] |
| Tempo de conclusão reportado para ocioso no Dashboard | ~30 minutos | [5] |
| Heartbeat de espera da orquestração no stderr | a cada 15 segundos | [37] |
| Timeout usado nos exemplos oficiais de `check --wait` | 900000 ms (15 min) | [37] |
| Timeout usado nos exemplos de `terminal wait` | 300000 ms (5 min) | [36] |
| Timeout do exemplo de `ask` (worker→coordenador) | 600000 ms (10 min) | [37] |
| Período de graça padrão de PTYs remotos após fechar o app | 5 minutos por alvo | [43] |
| Limite de tamanho por artefato compartilhado | 10 MiB | [32] |
| Alvo de contraste de cor do terminal (modo Custom) | 1 a 21 | [20] |
| Coordenadas do emulador mobile | normalizadas de 0 a 1 | [36] |
| Estrelas do repositório oficial | 67,2 mil | [65] |
| Forks do repositório oficial | 4,4 mil | [65] |
| Release mais recente no momento da coleta | v1.4.200 (11 set. 2026) | [66] |
| Versão do APK Android | 0.0.48 | [46] |
| Janela declarada entre PR mesclado e release | 48 a 72 horas (exceto correções P0+) | [66] |
| Idade do `git worktree` sem mudança entre versões | 2.54.0 (2026-04-20) até 2.55.0 | [62] |
| Versão do SQLite que introduziu WAL | 3.7.0 (21 jul. 2010) | [72] |
| Formatos de som de notificação suportados | 6 (MP3, WAV, OGG, M4A, AAC, FLAC) | [47] |
| Skills instaláveis no registro público do Orca | 7 | [38] |
| Status válidos de uma Task de orquestração | 6 (pending, ready, dispatched, completed, failed, blocked) | [37] |
| Status de cartão de workspace | 4 (todo, in-progress, in-review, completed) + custom | [39] |
| Glifos de estado de sessão de agente | 6 | [5] |
| Idiomas de interface | 6 (System, English, 中文（简体）, 한국어, 日本語, Español) | [49] |
| Modos de execução remota | 4 (Local, SSH, Servidor Orca, VM de nuvem) | [42] |
| URLs publicadas no sitemap oficial no momento da coleta | 61 | [61] |

---

## 5. Comandos verificados (gate R-CLI — fonte A)

Todos foram copiados literalmente da documentação oficial; nenhum flag foi inferido.

### Worktree e repositório [36]
```bash
orca status --json
orca open --json
orca repo list --json
orca repo add --path /abs/path/to/repo --json
orca repo set-base-ref --repo id:<repoId> --ref origin/main --json
orca repo search-refs --repo id:<repoId> --query main --limit 10 --json
orca worktree ps --json
orca worktree current --json
orca worktree create --repo id:<repoId> --name fix-login --json
orca worktree create --name child-task --agent codex --prompt "Investigate the flaky login test" --json
orca worktree create --name review-api --agent claude --setup run --json
orca worktree set --worktree active --comment "reproduced bug" --json
orca worktree rm --worktree id:<worktreeId> --force --json
```

### Terminal [36]
```bash
orca terminal list --json
orca terminal read --json
orca terminal send --text "continue" --enter --json
orca terminal wait --for tui-idle --timeout-ms 30000 --json
orca terminal create --worktree path:/projects/app --command "npm test" --json
orca terminal split --direction vertical --command "npm run dev" --json
orca terminal read --terminal <handle> --screen --json
orca terminal read --terminal <handle> --cursor <cursor> --limit 1000 --json
```

### Arquivos, host e runtime [36]
```bash
orca file open src/App.tsx
orca file diff src/App.tsx --staged
orca file open-changed --mode both
orca host list --json
orca serve --port 6768 --pairing-address 100.64.1.20 --json
```

### Browser embutido, emulador e artefatos [35][36]
```bash
orca goto --url https://example.com --json
orca snapshot --json
orca click --element @e3 --json
orca fill --element @e1 --value "[email protected]" --json
orca screenshot --json
orca set device --name "iPhone 12" --json
orca tab profile list --json
orca emulator list --json
orca emulator attach "<device-name-or-udid>" --json
orca emulator tap 0.5 0.7 --json
```

### Orquestração [37]
```bash
orca orchestration run-create --objective "..." --json
orca orchestration task-create --spec "..." --task-title "..." --json
orca orchestration worker-start --task <taskId> --worktree current --agent codex --json
orca orchestration worker-start --task <taskId> --worktree new-child --name billing-audit --agent codex --setup run --json
orca orchestration worker-start --task <taskId> --worktree current --agent claude --model <opaque-model-id> --effort high --json
orca orchestration check --wait --types worker_done,escalation,question --timeout-ms 900000 --json
orca orchestration check --ack <deliveryId> --wait --types worker_done,escalation,question --timeout-ms 900000 --json
orca orchestration send --type worker_done --subject "..." --body "..." --task-id <taskId> --dispatch-id <dispatchId> --outcome succeeded --files-modified "src/app/settings/Billing.tsx" --json
orca orchestration worker-show --dispatch <dispatchId> --json
orca orchestration worker-read --dispatch <dispatchId> --limit 50 --json
orca orchestration worker-stop --dispatch <dispatchId> --json
orca orchestration worker-release --dispatch <dispatchId> --json
orca orchestration worker-retain --dispatch <dispatchId> --json
orca orchestration worker-start --task <taskId> --retry-of <dispatchId> --worktree current --agent codex --json
orca orchestration send --to @all --subject "Heads up" --body "Pausing dispatches for a review." --json
orca orchestration ask --to <coordinatorHandle> --question "..." --options "shared,page-only" --timeout-ms 600000 --json
orca orchestration gate-create --task <taskId> --question "..." --options '["yes","no"]' --json
orca orchestration gate-resolve --id <gateId> --resolution "yes" --json
orca orchestration dispatch-show --task <taskId> --preamble --json
orca orchestration task-list --json
orca orchestration task-update --id <taskId> --status blocked --result '{"reason":"waiting on credentials"}' --json
orca orchestration reset --all --json
```

### Skills [38]
```bash
orca skills list
orca skills get orca-cli
orca skills get orchestration --full
orca skills get orca-linear --json
orca skills install --skill orca-cli --skill orchestration
orca skills install --skill orca-cli --agent claude-code,codex
orca skills install --all --dry-run
orca skills update --all
orca skills installed --json
orca skills share --skill frontend --skill testing --bundle-name "Team Toolkit" --json
```

### Automações, computer use e hooks [40][41][16]
```bash
orca automations create --name "Weekday triage" --trigger weekdays --time 09:00 --prompt "Triage new issues and summarize blockers" --provider codex --repo my-repo --disabled --json
orca automations create --name "PR review" --trigger hourly --precheck "gh pr list --json number -q .[0].number" --prompt "Review requested PRs" --provider codex --repo my-repo --disabled --json
orca automations edit <automationId> --missed-run-grace-minutes 30 --json
orca automations edit <automationId> --enabled --json
orca automations run <automationId> --json
orca automations runs --id <automationId> --json
orca computer permissions --json
orca computer list-apps --json
orca computer get-app-state --app com.spotify.client --json
orca computer click --app com.spotify.client --element-index 42 --json
orca computer set-value --app <app> --element-index 7 --value-stdin --json
orca agent hooks status|on|off --json
orca claude-teams
```

### Instalação das skills (npm) [38][41]
```bash
npx skills add https://github.com/stablyai/orca --skill orca-cli --global
npx skills add https://github.com/stablyai/orca --skill orchestration --global
npx skills add https://github.com/stablyai/orca --skill computer-use --global
npx skills add https://github.com/stablyai/orca --skill orca-per-workspace-env --global
npx skills update orca-cli orchestration computer-use --global
```

---

## 6. Limites, contornos e ressalvas declaradas (para o gate R-ES)

Limites explícitos da documentação que **devem** aparecer na obra como restrições honestas:

| Limite | Consequência prática | Fonte |
|---|---|---|
| `.worktreeinclude` só aceita caminhos literais — globs e negação são ignorados com aviso | Não é possível incluir `*.env` nem excluir por padrão; listar arquivo por arquivo | [4] |
| `worktree.sharedDirectories` ignora caminhos rastreados ou ausentes e exige gitignored | Uma entrada errada falha silenciosamente | [4] |
| Diretórios compartilhados usam symlink/share, `.worktreeinclude` copia | Editar um segredo compartilhado afeta **todos** os worktrees; copiado, não | [4] |
| `orca orchestration run` / `run-stop` / `coordinator-*` estão aposentados e não têm efeito | Scripts antigos falham em silêncio; usar Run + worker-start | [37] |
| `--effort` exige `--model`; ambos são incompatíveis com `--terminal` | Otimização de custo não é possível ao reusar um painel existente | [37] |
| Flags por launch (`--model`, `--effort`) valem só para aquele lançamento | Não há herança para retentativas | [37] |
| `worker_done`/`heartbeat` não aceitam endereços de grupo | Broadcast não substitui o reporte individual obrigatório | [37] |
| `reset` afeta estado de orquestração global do runtime | Rodá-lo com outro coordenador ativo destrói trabalho alheio | [37] |
| `--peek`/`--all` não consomem correio; replay exige `--ack` | Mensagens não confirmadas são reprocessadas — e podem ser processadas duas vezes se o coordenador não for idempotente | [37] |
| Handles de terminal são escopados ao runtime | Após reinício do Orca, handles antigos são inválidos e precisam ser readquiridos | [36] |
| `--screen` e `--cursor` são mutuamente exclusivos; leitura por stream pode fragmentar TUIs que redesenham linhas | Diagnóstico de TUI exige escolher entre quadro atual e histórico incremental | [36] |
| Ausência de host/escopo em `terminal list` é "não verificável", não "local" | Scripts não podem assumir execução local | [36] |
| Só agentes com sessão retomável hibernam (Cursor CLI, Hermes, Copilot, Trae ficam rodando) | O ganho de memória é parcial em frotas heterogêneas | [15] |
| Hibernação é experimental e desligada por padrão | Não contar com ela sem habilitar e calibrar a janela | [15] |
| Retomada de sessão só funciona em workspace local | Em remoto, é preciso copiar o comando e rodar no host | [18] |
| *Resume in New Chat* desabilita o Resume em terminal para aquela sessão | Escolha irreversível por sessão | [18] |
| `worker-release` pode retornar `release_pending` / `release_unknown` | Não substituir por fechamento amplo de terminal; seguir a ação de recuperação do recibo | [37] |
| Compute use é Beta, exige permissões de Acessibilidade (e Gravação de Tela no macOS) e nomes de flag ainda podem mudar | Automação de UI desktop é o elo mais frágil da pilha | [41] |
| Índices de elemento são escopados ao último `get-app-state` e podem ser esparsos | Reusar índice sem novo snapshot produz cliques errados | [41] |
| `elementCount` não é fonte de índices válidos | Nunca gerar índices programaticamente | [41] |
| Artefatos: 10 MiB por arquivo e **sem** upload de assets relativos | Só arquivo autocontido ou URL absoluta | [32] |
| Android: distribuição por APK (0.0.48) e TestFlight, não necessariamente pelas lojas plenas | Processo de instalação diferente do iOS da App Store | [65][46] |
| Servidor Orca Remoto é Beta | Exige rede privada (Tailscale/LAN) e token revogável; não expor porta | [44] |
| Adicionar um servidor não o torna padrão | É preciso ativar *Active Server* para rotear projetos | [44] |
| VMs de nuvem não são VPS hospedado pelo Orca | Fatura do provedor é do operador; imagens e billing próprios | [42] |
| Recipes só aparecem na criação de workspace quando `environmentRecipes` está no checkout primário de `orca.yaml` | Recipe em branch de feature não aparece até ir para o primário | [42] |
| Download recursivo de pasta exige SFTP completo | Em conexões só-OpenSSH, usar `tar`/`scp` | [43][51] |
| *Download Folder* é só desktop (web client não expõe) | Operação de transferência depende do app nativo | [43] |
| *Open in VS Code* exige worktree SSH e comando configurado como VS Code/Insiders | Não funciona com runtime de servidor remoto ativo nem com comandos multi-arg | [51] |
| `Folder download` e `Add account` indisponíveis em cliente remoto | Gestão de contas migra para o shell do servidor | [44] |
| Login do Google não é importado para o browser do worktree | É preciso entrar diretamente no Orca | [32] |
| Attribution é local e **não** commitada | Auditoria exige exportar metadado do diff | [27] |
| Atribuição marca linhas que o agente tocou via ferramenta | Edição humana sobre código de IA devolve a marca para humano — o registro é mutável | [27] |
| Força de push só como ação explícita com `--force-with-lease` | Reescrever histórico exige confirmação consciente | [28] |
| `{linkedIssue}` vazio quando não há vínculo — `Fixes #` mal formado | Templates precisam de fraseado condicional | [28] |
| Bitbucket Cloud não tem PR em rascunho | *Draft* fica oculto nessa plataforma | [28] |
| Agentes não customizados migram de modo de permissão em massa | Um override não-vazio opta o agente para fora de migrações futuras | [9] |
| Claude Agent Teams vem desabilitado por padrão | Recurso precisa ser ligado explicitamente | [9] |
| Em orquestração, `--model` só existe para Claude, Codex e Cursor; `--effort` depende do suporte do modelo | Não há paridade de controle de custo entre todos os agentes | [37] |
| Sessões SSH sobrevivem ao fechamento do app por período de graça (5 min padrão) | Depois disso, sessões desanexadas são encerradas | [43] |
| Não há opt-in permanente para o canal RC | Canal de pré-release exige gesto modificador a cada verificação | [2] |
| Documentação de produto é perecível; flags evoluem com o app | Sempre carregar o guia da versão: `orca skills get <topic> --full` | [38] |

---

## 7. Lacunas e ressalvas (o que a obra NÃO pode afirmar)

Registrado para que nenhum capítulo invente fato:

1. **Preços e licenciamento do Orca** não foram objeto desta mineração (a página
   `/enterprise` existe [59], mas não foi lida em profundidade nesta etapa). A obra **não**
   deve afirmar valores, planos ou modelo de cobrança.
2. **Requisitos mínimos de hardware** não são declarados na documentação consultada. Não
   afirmar RAM, CPU ou disco mínimos.
3. **Telemetria**: a página existe [50], mas o conteúdo detalhado (o que é coletado, como
   desligar) **não** foi lido. A obra deve tratar o tema como "há uma página oficial de
   telemetria; consulte-a" e não descrever o que é coletado.
4. **Mobile** [45] e **Android APK** [46]: conhecidos o canal de distribuição e o número de
   versão do APK, mas o detalhamento funcional não foi lido. Não descrever telas específicas do
   app mobile.
5. **GitHub/Linear/Jira** [29][30][31]: a obra conhece o vínculo de worktree a itens e as
   ações de revisão hospedada [4][28], mas as páginas dedicadas não foram lidas em
   profundidade. Não descrever fluxos específicos de cada integração além do que consta aqui.
6. **Quick open** [7], **session restore** [8], **file explorer** [21], **markdown** [22],
   **Monaco** [23], **viewers** [24], **native chat** [17], **GLM agent** [14],
   **hot-swap** [12] detalhado, **cursor-cli** [13], **codex** [11], **browser profiles** [34],
   **activity** [48], **github-errors** [52] e as **recipes** [54][55][56][57]: existem e são
   citáveis, mas a obra deve tratá-las no nível declarado aqui, sem inventar telas ou passos.
7. **Concorrência e limites do app** (número máximo de worktrees, agentes simultâneos, consumo
   de memória por aba) **não** são documentados como números. Não inventar limites; usar
   apenas a orientação qualitativa de [51] ("close worktrees you're not actively using") e o
   *Resource Manager* [49] como instrumento de medição.
8. **A sinergia histórica com a Fábrica Agêntica de Publicações** (o ecossistema deste
   repositório, que já possui skills `orca-cli`, `orchestration`, `computer-use` e
   `orca-orchestrator`) é um fato local do projeto do autor, não da documentação oficial.
   Se citada, deve ser apresentada como experiência de aplicação, nunca como recurso do
   produto.
9. **A mineração acadêmica** (§2.3) não contém estudos sobre orquestração de agentes de LLM em
   ADEs. Qualquer uso dessas fontes deve ser de contexto histórico sobre paralelismo e
   ambientes descartáveis, jamais como evidência sobre o Orca.

---
