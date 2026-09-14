# Dossiê — Blocos Temáticos 5 a 8 (Parte II — O Ambiente)

---

## BLOCO 5 — Anatomia da interface (Cap. 5)

**Fatos coletados**

### 5.1 Sistema de abas e painéis [6]

- Cada aba carrega uma coisa: um terminal, um buffer de editor, um browser, um diff, um PR.
  Abas vivem dentro de um *tab group*.
- Arrastar uma aba na vertical dentro do grupo reordena; arrastar para outro grupo move.
- Fechar todos os arquivos de editor abertos no worktree ativo: `Cmd+Option+W` (macOS) ou
  `Ctrl+Alt+W` (Windows/Linux).
- Uma barra colorida marca qual painel está focado (aba ativa).
- Atalhos padrão de troca de aba em instalações novas:

  | Ação | macOS | Linux/Windows |
  |---|---|---|
  | Próxima/anterior (todos os tipos) | `Cmd+Shift+]` / `Cmd+Shift+[` | `Ctrl+Shift+]` / `Ctrl+Shift+[` |
  | Próxima/anterior (mesmo tipo) | `Cmd+Option+]` / `Cmd+Option+[` | `Ctrl+Alt+]` / `Ctrl+Alt+[` |
  | Aba recente anterior | `Ctrl+Tab` | `Ctrl+Tab` |

  Remapeáveis em `Settings → Shortcuts`; instalações antigas mantêm overrides em
  `~/.orca/keybindings.json` [6].
- **Splits**: arrastar uma aba até a borda direita divide na horizontal (esquerda/direita);
  até a borda inferior, na vertical (topo/base). Splits **aninhham**: terminal de agente à
  esquerda, diff no topo-direita e browser na base-direita, simultaneamente. "Any tab type
  can split with any other" [6].
- Terminais também dividem **dentro da aba** (menu *Split terminal right* /
  *Split terminal down*, ou botão de split no cabeçalho do painel ativo) [6].
- **Fronteiras fixas**: redimensionar a janela não embaralha o layout; as posições das
  fronteiras são salvas **por worktree** [6].
- **Grupos de abas entre worktrees**: "Each worktree owns its own tab layout. Switching
  worktrees swaps the entire pane tree — your browser tab, terminal, and diff reappear
  exactly as you left them" [6].

### 5.2 Barra lateral, quick open e navegação

- A barra lateral agrupa worktrees **por projeto** por padrão: linhas de topo são projetos
  (um projeto = um repositório Git ou um cluster relacionado), expandidos nos worktrees em
  uso. O cabeçalho tem filtro próprio, separado da busca global [4].
- *Quick open*: busca "across worktrees, files, agents, commands, and repo context without
  leaving your flow" — listado entre os recursos-chave do produto [65]. Página dedicada:
  [7].
- *Worktree Jump Palette* (`Cmd-J`): salta entre worktrees; tem filtros próprios de host e
  projeto (tecla `Tab`); a busca casa workspaces nomeados com emoji pelo fragmento derivado
  do shortcode; abrir com `Cmd-J` vazio mostra recentes e atalhos numéricos, que respeitam
  os mesmos filtros da barra lateral [4].
- Worktrees podem ser **fixados** no topo do projeto; o clique direito expõe as ações
  arquivar / dormir / deletar [4].
- Menu *Open in*: escolhe apps no menu de abertura do worktree — VS Code / Insiders habilitam
  a abertura por Remote SSH em worktrees SSH; outros editores ficam restritos a caminho
  local [49].
- Aparência configurável: tema, cor de acento, densidade, fonte da UI, minimapa do editor,
  zoom da UI, ícone do app (Classic, Watercolor, Blue) [49].

### 5.3 Edição, visualização e restauração

- Abas de arquivo: os painéis de edição incluem explorador de arquivos [21], editor Markdown
  [22], editor Monaco [23] e visualizadores [24]. O caso de uso declarado pelo produto é
  "VS Code's editor with autosave everywhere — drag files or images straight into an agent
  prompt" [65].
- *Editor Word Wrap*: padrão de quebra de linha dos editores (ligado por padrão),
  alternável pelo menu `⋯` da aba do arquivo ou `Alt+Z` — configuração **separada** de
  *Diff Word Wrap* [49].
- Fonte do editor é opt-in: vazio = segue a fonte do terminal; preencher sobrescreve
  **apenas** editores de arquivo e diffs [49].
- Arquivos podem ser **arrastados para o prompt do agente**, incluindo imagens [65].
- *Session restore*: página dedicada à restauração de sessão [8]. A promessa de produto
  equivalente aparece no terminal: "scrollback that survives restarts" [65].
- *Status bar* configurável, incluindo o *Resource Manager* (CPU/memória/sessões, controles
  de daemon, varreduras de disco por workspace) e percentuais de uso de provedor exibidos
  como % usado ou % restante [49].
- Painéis de preview ricos: "Preview Markdown, images, PDFs, and repo docs in the
  workspace" [65]; página dedicada em [24].
- *Keep computer awake*: `On` (acordado continuamente), `Agent` (acordado enquanto um agente
  trabalha) ou `Off`; o mesmo controle existe na barra de status como *Caffeinate* (ícone de
  café) e fica oculto em clientes web pareados [49].

**Arco narrativo:** a interface é um *gerenciador de contexto visual* — ela existe para que
o operador consiga assistir N agentes sem trocar de janela e sem perder o estado de cada
tarefa.

---

## BLOCO 6 — Agentes suportados e o harness agnóstico (Cap. 6)

**Fatos coletados**

- Princípio: "Orca works with any CLI agent — the agent combobox just launches a process in
  a terminal" [9]. O produto reforça: "Works with any CLI agent — if it runs in a terminal,
  it runs in Orca" [65].
- O catálogo embarcado no seletor traz **mais de 30 agentes** pré-configurados com
  lançamento/instalação em um clique, com notas sobre ganchos (hooks), status, rastreio de
  uso e troca de conta onde há suporte [9]. Lista verificada da documentação:
  Claude Code, Claude Agent Teams, Codex, Grok, GitHub Copilot CLI, OpenCode, Pi, OMP,
  Prime Agent, Gemini, Antigravity, Ante, Aider, Goose, Amp, Kilocode, Kiro, Charm Crush,
  Auggie, Autohand, Cline, Codebuff, Command Code, Continue, Cursor CLI, Devin,
  Droid (Factory), Kimi, Mistral Vibe, MiniMax, Qwen Code, Rovo Dev, Hermes, OpenClaw,
  Trae [9].
- **Integração profunda** declarada para Claude Code, Codex e Cursor CLI; **Prime Agent**
  acumula auto-setup, hooks, status e histórico de sessão; **MiniMax** soma rastreio de uso
  e de limites de taxa [9].
- **Claude Agent Teams** vem **desabilitado por padrão** — habilitar em
  `Settings → Agents` para lançar via `orca claude-teams`, com painéis nativos para cada
  teammate [9].
- **Flags de permissão pré-aplicadas**: o Orca preenche o flag de bypass de permissão de cada
  CLI suportado — `--dangerously-skip-permissions` (Claude),
  `--dangerously-bypass-approvals-and-sandbox` (Codex), `--yolo` (Gemini, Cursor, Crush,
  Kimi, Rovo Dev, Hermes, GitHub Copilot, Command Code) e o equivalente para os demais [5][9].
  Racional explícito: "worktrees are disposable: an agent running in its own checkout can
  experiment without you re-confirming every shell command, and you can still cherry-pick or
  discard the diff before merging" [9].
- **Permissões globais**: `Settings → Agents → Agent Permissions` alterna todos os agentes
  **não customizados** entre *Yolo* e *Manual*. Agentes com argumentos ou ambiente já
  sobrescritos são preservados — "Orca treats a non-empty custom value as an explicit
  override and opts that agent out of future permission-mode migrations" [9].
- Customização por agente: `Settings → Agents`, expandir a linha do agente e editar os
  argumentos de lançamento; o Orca memoriza o override e o aplica em todo lançamento
  seguinte, com botão *Reset* restaurando o flag de fábrica [5].
- **Instalação / detecção**: `Settings → Agents` lista CLIs detectadas e permite
  habilitar/desabilitar para que os menus de lançamento mostrem só o que interessa; também
  guarda as listas de contas Claude e Codex, hooks de inicialização por agente, hooks de
  status e a opção *Keep computer awake* [49].
- **Claude Code** [10]: instalação por `npm i -g @anthropic-ai/claude-code` (ou docs da
  Anthropic); login uma vez em qualquer terminal; "Orca picks up `~/.claude` automatically —
  no extra config needed". Ao lançar, o Orca usa o worktree como diretório de trabalho e um
  hook de status-line que emite eventos de título OSC usados nos indicadores de estado.
  O Orca lê o estado local de uso em `~/.claude` e mostra consumo e proximidade de limite de
  taxa na barra de status. Suporta múltiplas contas Claude com troca em um clique, inclusive
  com sessões vivas (a troca em andamento fica atrás de uma guarda para evitar refreshes de
  autenticação sobrepostos). Subagentes em background e teammates de Agent Teams aparecem
  como linhas-filhas expansíveis sob o agente líder; selecionar um filho foca o terminal
  líder.
- **Hooks e memória** [16]: o Orca lê as configurações `.claude/` e `.codex/` de cada
  repositório, e hooks existentes rodam quando o Orca lança o agente naquele repositório.
  `CLAUDE.md` e `AGENTS.md` (raiz ou aninhados) **não são tocados** — "they belong to the
  agent" — mas aparecem no explorador de arquivos para edição inline. Hooks de setup de
  worktree (`Settings → Repository → Hooks`) rodam comandos automaticamente após a criação
  do worktree (ex.: `pnpm install`, `direnv allow`, restauração de `.env`).
  `Settings → Agents → Agent status hooks` controla os hooks gerenciados que reportam
  *working / waiting / done* para a UI; desligar remove os hooks gerenciados e impede sua
  reinstalação; religar restaura **sem reiniciar** o Orca (no Windows o relay de hook do WSL
  segue a mesma chave viva). Equivalentes de CLI:
  `orca agent hooks status|on|off --json`.
- Persistência dos hooks após reinício: os endpoints são gravados em disco
  (`{userData}/agent-hooks/endpoint.env` em POSIX, `endpoint.cmd` no Windows) e re-lidos em
  cada invocação, "so long-lived agent sessions keep reaching the live Orca server even after
  an app restart — no more dead-port POSTs from a PTY that outlived the previous session" [16].
- **Troca de conta / hot-swap** [12]: superfície dedicada para trocar o login do Codex
  atrás de uma sessão ativa sem reiniciá-la; o fluxo do Claude é "identical in shape" [10].
  O chip *Restart* do Codex preserva a conta atual [5].
- **Rastreio de uso e limites** [19]: o Orca lê o estado local de uso dos provedores e mostra
  consumo e proximidade de limite de taxa na barra de status; `Settings → Appearance` permite
  exibir percentuais como % usado ou % restante [49].
- **Fronteira importante**: "Not a model. Orca runs agents you already use — bring your own
  Claude, Codex, or OpenCode subscription" [1]. O README reforça: "Run any coding agent with
  your own subscription" [65].
- **Auto-setup**: a maioria dos agentes é "Auto-setup"; alguns exigem binário específico
  instalado (`Qwen Code` via executável `qwen`; `Trae` via `traecli` / TRAE CN CLI) [9].
- **Agent Teams / subagentes**: "Nested Codex/Claude subagents can appear as expandable
  children under the parent row" no Agent Dashboard [5]; "Nested Codex/Claude subagents can
  appear as expandable children under the parent row" [5]; a leitura de subagentes vale
  o mesmo na lista do worktree [10].

**Arco narrativo:** o ADE não compete com os agentes — ele é a camada que torna possível
misturá-los. A escolha do agente deixa de ser uma decisão irreversível e passa a ser uma
variável por tarefa.

---

## BLOCO 7 — Ciclo de vida do terminal e das sessões (Cap. 7)

**Fatos coletados**

- Definição formal: "An agent session is one CLI agent running in one terminal in one
  worktree. Orca tracks its lifecycle so you always know which sessions are working and which
  are idle — without you having to click into each tab to check" [5].
- **Glifos de estado compartilhados** entre abas de agente e linhas de worktree [5]:

  | Glifo | Significado |
  |---|---|
  | Spinner | trabalhando (working) |
  | Ponto de interrogação âmbar | esperando você (permissão / precisa de entrada) |
  | Check esmeralda (dashboard) ou ponto esmeralda (barra lateral) | concluído / ativo silencioso |
  | Ponto vermelho | bloqueado, interrompido ou falhou |
  | Ponto cinza | ocioso (idle) |
  | Sem indicador | shell puro, não é uma CLI de agente reconhecida |

- A detecção de estado vem da **sequência de título OSC** do terminal e dos **hooks do
  agente**, que Claude Code, Codex e vários outros emitem [5].
- **Agent Dashboard** (experimental): kanban de agentes entre worktrees, com colunas
  *Needs You*, *Working*, *Done* e *Idle* (esta última oculta por padrão; agentes sem
  conclusão reportada por cerca de **30 minutos** caem em Idle). Clicar em um cartão abre/foca
  o terminal vivo daquele agente. Cartões mostram badge de host para workspaces SSH e
  servidores pareados (`SSH host · openclaw`, `Remote Orca host · Build Mac`); workspaces
  locais não mostram badge. Pode ser aberto *in-window* ou *pop-out*. Toolbar com busca,
  filtro multi-seleção (projeto, status do workspace, status de PR/MR) e chips removíveis.
  Cartões *Needs You* ganham tom âmbar e podem exibir o resumo da pergunta pendente; *Done*
  ganham verde; demais estados ficam neutros — "tint means 'look here'" [5].
- Atalho para *Toggle Agent Dashboard* é atribuível em `Settings → Shortcuts` (sem binding
  padrão) e funciona com terminal, editor ou browser em foco [5].
- **Ciclo de vida em cinco etapas**: Launch (escolher agente no combobox; o Orca gera a CLI)
  → Work (títulos OSC atualizam o estado; a saída rola com busca, cópia e tema Ghostty)
  → Idle (o Orca detecta a transição trabalhando→ocioso e dispara notificação de
  agente-concluído) → Exit (o processo termina; aparece o chip *Restart*) [5].
- **Terminal** [20]: base xterm.js — "the same xterm.js-based terminal VS Code uses" [20][70],
  com renderização WebGL e splits infinitos [65]. Recursos e detalhes:
  - **Ghostty-style**: importa tema, fonte e cursor do Ghostty na primeira execução;
    reexecutável em `Settings → Terminal → Import from Ghostty`.
  - **Importação de temas do Warp** (`Import themes from Warp`), com descoberta automática
    do diretório de temas por SO (`~/.warp/themes` no macOS,
    `$XDG_DATA_HOME/warp-terminal/themes` no Linux,
    `%APPDATA%\warp\Warp\data\themes` no Windows) e `Import from YAML` para qualquer pasta
    de arquivos `.yaml`/`.yml` no formato Warp.
  - **Clipboard TUI (OSC 52)**: permite que TUIs (Zellij, tmux, Neovim, fzf, Grok) escrevam
    o clipboard do sistema via PTY, funcional sobre SSH; toggle em
    `Settings → Terminal → Allow TUI Clipboard Writes (OSC 52)`.
  - **Busca**: `Cmd-F` no scrollback, com destaque, case, regex e navegação de ocorrências.
  - **Links**: clique simples abre um popover compacto de ações (Orca Browser / System
    Browser / Copy link); `Cmd`/`Ctrl`+clique abre direto; `Shift+Cmd`/`Shift+Ctrl`+clique usa
    o roteamento alternativo. *Show terminal link actions* pode ser desligado em
    `Settings → Browser`.
  - **Copy Context**: cópia de transcrição limitada do painel; *Copy Session ID* copia o
    identificador de sessão para scripts e suporte.
  - **Contraste de cor**: `Automatic`, `Off` ou `Custom` com alvo de contraste de **1 a 21**.
  - **Teclado nativo**: o Orca anuncia o **kitty keyboard protocol**, então apps de terminal
    veem `Shift+Enter`, `Ctrl+Enter` e outras teclas com modificadores como em Ghostty,
    WezTerm ou terminal nativo. Em teclados japoneses JIS no macOS há a opção de enviar
    barra invertida pela tecla Yen físico.
  - **Windows**: default entre PowerShell, Prompt de Comando e WSL; para repositórios em
    filesystem WSL (`\\wsl.localhost\...`) o Orca lança via `wsl.exe -d <distro>`; para
    repositórios em caminho Windows abertos no WSL, traduz o cwd para `/mnt/<drive>/...` e
    entrega um bash de login.
  - **Atalhos**: `Cmd-T` (novo terminal no worktree), `Cmd-Alt-T` (nova aba de agente com o
    agente padrão — sem binding no Linux/Windows), `Cmd-W` (fechar aba), `Cmd-\` (split
    direita), `Cmd-Shift-\` (split abaixo). Cada agente suportado tem sua própria ação
    "New agent tab".
  - **Terminal flutuante**: superfície global sempre a um atalho (`Cmd+Option+A` /
    `Ctrl+Alt+A`), ligada por padrão em novas instalações; hospeda abas próprias, aceita
    *orchestration setup* e permite iniciar execuções de fundo **sem ocupar um painel do
    worktree**; diretório inicial configurável (padrão `~`).
  - **Quick Commands**: comandos salvos (ex.: `npm run dev`, `pnpm test`) e **prompts de
    agente** reutilizáveis para agentes de prompt em lançamento (Claude e Codex). Cada comando
    tem rótulo, texto e escopo (*Global* ou *Project*). O botão na barra de abas abre uma aba
    de terminal nova e roda o comando; o menu de contexto insere o comando no terminal atual.
    Com servidor remoto pareado, o seletor mostra coleções locais e remotas lado a lado,
    rotuladas por host; "Saved on is where the command is stored; running a command still
    executes in the terminal or workspace where you invoke it — so a client-owned command can
    run inside a remote worktree". Servidores antigos sem suporte voltam à lista local.
- **Hibernação de agentes** [15] (experimental, desligada por padrão; habilita em
  `Settings → Experimental → Agent hibernation`):
  - Um terminal só hiberna se **todas** as condições valerem: agente em estado *done*; o
    terminal não está no worktree ativo nem em worktree renderizando terminal em primeiro
    plano; nenhuma tecla recebida desde a conclusão; o agente é de sessão retomável (Claude,
    Codex, Gemini, Antigravity, OpenCode, Pi, MiMo Code, Droid, Grok, Devin ou OMP); ocioso ao
    menos pela janela configurada (**padrão 30 minutos**); nenhuma sessão mobile dirigindo o
    terminal; nenhum Dispatch de orquestração ainda não liquidado (pendente, despachado ou
    desconhecido) — dormir volta a ser permitido após *completed*, *failed* ou
    *circuit_broken* confirmados pelo runtime; nenhum roster vivo de subagente/teammate no
    painel (o "done" do provedor sozinho não basta enquanto filhos seguem anexados).
  - Falha em qualquer verificação mantém o terminal rodando. "If a worktree has multiple
    agent panes, they hibernate together as a unit so a partially-paused worktree never
    ships."
  - Janela de ociosidade ajustável: **1 minuto a 24 horas**; o relógio começa na última
    atualização de conclusão do agente e qualquer tecla, saída nova ou retorno à aba do
    agente o reinicia.
  - Retomada: ao reabrir um worktree hibernado, o Orca relança a CLI com os mesmos flags de
    resume que usaria do histórico de sessão (`claude --resume <id>`, `codex resume <id>`…),
    reusando comando, argumentos e ambiente privado capturados no lançamento original.
  - Se a CLI não conseguir retomar (transcrição apagada, ID rotacionado pelo provedor), o
    terminal abre em prompt novo e a transcrição anterior continua no histórico.
  - Limitação declarada: só os agentes retomáveis listados hibernam — Cursor CLI, Hermes,
    Copilot, Trae e outros terminais não retomáveis ficam rodando.
  - Sono manual: pela barra lateral, incluindo *Sleep with Descendants* quando há filhos
    aninhados; o sono manual **preserva** sessões retomáveis concluídas e interrompidas [15][4].
- **Histórico de sessões** [18]: o Orca varre as transcrições que as CLIs deixam em disco e as
  lista no painel *Agent Session History* (barra lateral direita, aba *Agents*), com contador
  no formato "12 shown · 47 recent" e busca por título, diretório de trabalho, branch, modelo
  ou prévia da conversa. Escopos: *Workspace*, *Project*, *All*. Opções de visualização:
  agentes varridos (Claude, Codex, Hermes, Pi, OMP, Prime Agent, Cursor, Gemini, Antigravity,
  Rovo Dev, Copilot, OpenCode, Grok, OpenClaw, Devin, Droid, Kimi), ordenação (*Last updated*
  ou *Created*), agrupamento (*Project*, *Folder*, *Agent*) e *Hide empty sessions*.
  Ações por linha: *Resume*, *Resume in New Chat* (apenas sessões locais elegíveis de Claude
  e Codex; mover para chat estruturado **desabilita** o Resume em terminal depois), *Copy
  resume command*, *Copy session ID*, *Copy log path*, *Open log* / *Reveal log*, *Open cwd*.
  Exemplos de comandos de retomada citados pela doc: `claude --resume <id>`,
  `codex resume <id>`, `pi --session <session_file>`, `prime-agent --resume <path>`,
  `cursor-agent --resume <id>`, `acli rovodev run --restore <id>`.
  Origens: `~/.codex/sessions`, histórico do `~/.claude`, log de sessão do Cursor, sessões
  legadas do OpenCode ou `~/.local/share/opencode/opencode.db`, entre outras. Retomada só
  funciona em workspace local; em workspace remoto, o painel orienta usar
  *Copy resume command* e rodar no host.
- **Chat nativo** [17]: superfície de chat estruturado dentro do Orca; *Resume in New Chat*
  é o caminho de entrada a partir do histórico para sessões locais elegíveis de Claude e
  Codex. O release v1.4.200 destaca: "Native chat: Claude subagent activity and Codex
  background tasks are now visible in chat. Completed turns show changed files, and task
  updates stream into the composer" [66].
- **Notificações** [47]: quando um agente passa de trabalhando para ocioso, o Orca dispara
  notificação — notificação de sistema, som e um chip no worktree. O sino do cabeçalho mostra
  não lidas de todos os worktrees e clicar em uma notificação salta para worktree e painel
  correspondentes. No macOS a mesma contagem aparece como badge no ícone do Dock. Clique
  direito permite marcar como não lida. Categorias (sistema, som, apenas chip) podem ser
  desligadas em `Settings → Notifications`, onde também se escolhe som customizado por
  categoria, com formatos **MP3, WAV, OGG, M4A, AAC, FLAC** e volume de reprodução.

**Arco narrativo:** o terminal deixou de ser uma janela e virou um **objeto gerenciado com
ciclo de vida** — estado observável, pausa automática, retomada e histórico auditável.

---

## BLOCO 8 — O ciclo de revisão (Cap. 8)

**Fatos coletados**

### 8.1 Diff viewer [25]

- Declaração de propósito: "Orca's diff viewer is designed for serious review of AI-generated
  code — not a quick glance. Every worktree has a built-in diff against its start-from ref."
- Recursos: diff combinado de arquivos staged, unstaged e untracked; números de linha para
  ambos os lados (alternáveis); **diffs de imagem** em três modos (lado a lado, swipe,
  onion-skin); **preview de HTML** ("Open Preview to the Side") em diffs combinados quando a
  seção HTML ainda existe na árvore de trabalho (HTML deletado e superfícies apenas de commit
  não exibem o ícone); UI de conflito de merge com visão de três vias e resolução inline;
  **staging por hunk ou por linha** ("same as `git add -p` but visual"); **Show Whitespace**
  para revelar espaços e tabs.
- Escopo: o diff é contra o start-from ref por padrão, com troca para qualquer commit, branch
  ou a base ref na barra de ferramentas.
- *Word wrap* desligado por padrão; alternável no menu `⋯` do cabeçalho do diff ou como padrão
  global em `Settings → General → Diff Word Wrap` (os dois controles compartilham o mesmo
  ajuste).
- Árvore de arquivos recolhível ao lado dos hunks em diffs combinados, com largura
  redimensionável (lembrada entre sessões).
- Atalhos: `j`/`k` (próximo/anterior arquivo alterado), `n`/`p` (próximo/anterior hunk),
  `F7`/`Shift+F7` (próxima/anterior mudança no editor ativo), `s` (stage do hunk sob o
  cursor), `c` (iniciar comentário).

### 8.2 Annotate AI Diff [26]

- Loop de revisão inline: comentar qualquer linha de qualquer hunk gerado por IA e enviar
  tudo como **um único lote** de volta ao agente — "no copying line numbers, no
  context-switching".
- Fluxo: passar o mouse em qualquer linha → aparece um `+` na calha → clicar (ou tecla `c`)
  → escrever o feedback (Markdown suportado) → `Cmd-Enter` salva, `Esc` cancela. Comentários
  ficam fixados à linha exata e "Orca tracks them across edits so they follow the line if the
  diff shifts".
- Envio: *Send to agent* no topo do diff compõe **um único prompt** com todos os comentários
  ancorados por linha e abre o menu *Send notes to* com os agentes disponíveis no worktree
  (inclusive iniciar um novo agente). A ação *Send Review Notes to Agent* não tem binding
  padrão para não colidir com outros atalhos.
- Justificativa de design: "Sending comments one at a time causes the agent to swing back and
  forth. Batching keeps the feedback coherent: one round of thinking, one revision pass, and
  a much higher hit rate."
- Pós-revisão: comentários permanecem fixados depois que o agente revisa, para verificar a
  correção; *Resolve* colapsa a thread; comentários não resolvidos entram no próximo lote.

### 8.3 Attribution [27]

- "Orca tracks provenance on every line it sees an agent touch, so when you read a diff you
  can tell at a glance which lines were written by a human and which came from an AI."
- Mecânica: quando um agente escreve em um arquivo pela sua ferramenta, o Orca registra os
  intervalos; o diff renderiza linhas de origem IA com um marcador sutil na calha; edição
  humana sobre código de IA devolve a atribuição para humano.
- Importância declarada: saber quais partes de um PR merecem escrutínio extra; auditorias de
  segurança e conformidade podem separar código escrito por IA do escrito por humano;
  revisões ficam mais rápidas.
- Escopo: a atribuição é local ao Orca e **não é commitada**; para atribuição persistente, o
  metadado do diff pode ser exportado pela barra de ferramentas do diff.

### 8.4 Commit, push e PR [28]

- O painel de commit fica ao lado do diff viewer e é desenhado para o caso comum:
  revisar, fazer stage, commitar, empurrar, seguir em frente.
- *Generate with AI* redige a mensagem de commit a partir das mudanças em stage; `Commit` é
  `Cmd-Enter` (macOS) ou `Ctrl-Enter` (Windows/Linux) quando o foco está em Source Control.
- Hooks de pre-commit do repositório rodam normalmente; se um hook falha, o Orca mostra a
  saída inline. Falhando o commit, *Fix with AI* inicia o agente padrão no worktree ativo com
  a saída do hook, a mensagem de commit tentada e a lista de arquivos em stage — "The agent
  gets a repair prompt only — it is not asked to bypass hooks, commit, push, or open a
  review."
- Push: empurra a branch do worktree para `origin`, definindo upstream na primeira vez.
  "If the branch is behind, Orca will not silently force-push."
- Quando o histórico foi reescrito (rebase, amend, squash) e o remoto tem apenas cópias
  antigas, a UI expõe **Force push with lease** como ação explícita e separada — nunca como
  fallback do Push comum — com rótulo mostrando a contagem de commits substituídos e o nome da
  branch upstream. Usa `--force-with-lease`, de modo que uma visão local desatualizada do
  remoto aborta o push em vez de sobrescrever commits alheios.
- Revisão hospedada: depois do push, a ação de revisão do painel cria o PR/MR, com confirmação
  de base, título, descrição e estado de rascunho. Bitbucket Cloud cria PRs pelo mesmo
  compositor, mas não tem PR em rascunho, então a opção *Draft* fica oculta. Em GitHub, quando
  a base selecionada já tem PR aberto, aparece *Stack this PR above #N*.
- *Generate pull request details with AI* redige título, descrição e estado de rascunho a
  partir do diff e dos commits da branch, buscando seções curtas no estilo ELI5
  problema/solução e orientação de issue vinculada (`Fixes` vs `Refs`). O Orca mantém a base
  escolhida, rejeita descrição vazia e mostra erro claro em vez de publicar corpo em branco.
- **Receitas de ação de IA por repositório**: *Generate with AI*, *Generate pull request
  details with AI*, *Fix with AI* e *Resolve with AI* são todas apoiadas por uma *action
  recipe* que escolhe agente, argumentos de CLI e template de prompt. Editáveis em
  `Settings → Git & Source Control → Action recipes`, como padrão global ou escopo por
  repositório. Variáveis disponíveis: `{basePrompt}`, `{branch}`, `{stagedFiles}`,
  `{stagedPatch}`, `{linkedIssue}` para mensagens de commit; e para PR também
  `{baseBranch}`, `{currentTitle}`, `{currentBody}`, `{commitSummary}`, `{changedFiles}`,
  `{patch}`. `{linkedIssue}` expande para o número da issue GitHub vinculada ao workspace, ou
  vazio quando não há vínculo (inclusive workspaces puramente Linear/GitLab) — a doc
  recomenda fraseado instrucional, porque um `Fixes #{linkedIssue}` isolado vira `Fixes #`
  quando não há vínculo. Override por repositório não é afetado por mudanças no padrão
  global, e o painel de configurações avisa quais repositórios divergem e em quê.
- Amend é explícito (*Commit → Amend*) e o Orca não altera commits já empurrados sem
  confirmação.
- Painel Source Control: mesmo conjunto de ações sem sair da visão atual; caminhos renderizam
  em UTF-8 mesmo com caracteres não-ASCII; a linha de contexto de branch mostra a branch atual
  (ou detached HEAD) empilhada sobre a base de comparação (`branch → base`); quando há merge
  base utilizável, um chip compacto mostra total de linhas adicionadas e removidas contra o
  ponto de bifurcação, com detalhamento ao passar o mouse em *Source*, *Tests* e *Generated*
  (apenas heurística de caminho, não análise de conteúdo). O botão primário do rodapé muda com
  o estado: *Stage Files* quando há mudanças não preparadas, depois *Commit*, depois
  *Push*/*Pull*/*Sync*.

### 8.5 Rastreamento de trabalho e revisão hospedada [29][30][31]

- GitHub, Linear e Jira são integrações nativas: "Browse PRs, issues, and project boards
  in-app — open a worktree from any task and review without a context switch" [65].
- Um worktree pode ser vinculado a PR do GitHub, issue do Linear, MR do GitLab ou issue do
  Jira direto do campo de nome (colar URL do Jira ou buscar no modo Jira); itens vinculados
  aparecem no cartão do worktree [4].
- Ao criar a partir de uma issue do Linear, o Orca usa o nome de branch que o próprio Linear
  fornece para aquela issue como override, em vez de apenas slugificar o título [4].
- O campo *Branch name* só é oferecido quando a criação vem de nome digitado ou branch base;
  quando o workspace está atrelado a um item rastreado, a branch é derivada do item — e um PR
  do GitHub vinculado **re-resolve** a branch no envio — então o campo é ocultado para evitar
  override silenciosamente ignorado [4].
- Erros de GitHub (limites de taxa, autenticação de `gh`, escopos ausentes, acesso a
  repositório) aparecem em Source Control e no painel de Checks; a página dedicada [52]
  detalha a matriz. Checks rápidos citados: `gh auth status -h github.com`, `gh api user`,
  `gh api rate_limit --jq '.resources.core'` [51]. `Settings → Git → GitHub API Budget` mostra
  cota REST (core), Search e GraphQL do `gh` local [49].
- Depois do merge, o estado de revisão em cache aparece no rodapé do cartão do dashboard [5].

### 8.6 Browser por worktree — verificar antes de afirmar [32]

- "Every Orca worktree has its own browser. It's a real Chromium window — address bar,
  history, devtools — embedded in a pane. Tabs are scoped to the worktree."
- Controles: barra de endereço com histórico e completação difusa; texto não-URL busca com o
  *Default Search Engine* (prefixo `?` no campo `+` força busca); back/forward/reload/stop,
  com *Reload* e *Hard Reload* (bypass de cache) no clique direito ou long-press; `Cmd-F`
  (buscar na página), `Cmd-T` (nova aba no worktree), `Cmd-Shift-T` (reabrir última aba
  fechada). Links com `target=_blank` e popups sem nome abrem em aba nova usando o perfil do
  opener; popups nomeados e de OAuth ainda podem abrir em janela separada. Abas novas carregam
  em background.
- Troca de tipo: um preview de HTML expõe o caminho do documento na barra de endereço;
  digitar uma URL o converte em aba de browser no lugar; digitar um caminho HTML de workspace
  em uma aba de browser o converte de volta em preview — e o Back atravessa a conversão quando
  não há histórico intermediário.
- Escopo: abas filtradas por worktree; trocar de worktree restaura abas **e posições de
  scroll**; sessões persistem, com importação de cookies do Chrome ou Edge em um clique
  (logins do Google não são importados — é preciso entrar diretamente no Orca) [32][73].
- Perfis: páginas dedicadas a perfis de browser (`orca tab profile list|create|set|clone|
  use-default`), isolando cookies, armazenamento local e identidades logadas [32][34][36].
- Workspaces remotos: em servidor remoto pareado, novas páginas renderizam neste desktop por
  padrão enquanto tráfego HTTP(S), WebSocket, DNS e loopback passam pelo host remoto; o
  indicador de host na toolbar mostra para onde o tráfego vai; escolha
  `This device` ou `Server (streamed)` em `Settings → Browser → Remote server workspaces`
  (aplica-se só a páginas novas). Para workspaces SSH, *Browse through SSH workspace hosts*
  decide se tráfego e DNS passam pelo host SSH; downloads de página remota ficam no host
  remoto e uploads são preparados lá antes de a página recebê-los.
- Roteamento de links: `Settings → Browser → Link Routing` decide se links `http(s)` do
  terminal, Markdown e editor abrem no browser por worktree ou no navegador do sistema, com
  toggle aninhado que inverte o padrão por um clique com o modificador.
- Downloads: prateleira sob a toolbar com cancelar, abrir, mostrar na pasta e dispensar.
- *Share as artifact*: arquivos HTML locais abertos no browser do worktree podem virar link
  público pela conta Orca — **limite de 10 MiB por arquivo**; assets relativos **não** são
  enviados (compartilhar arquivo autocontido ou usar URLs absolutas) [32].
- **Emulação de viewport**: tamanho customizado por aba para testar responsividade sem
  redimensionar o painel, usando emulação de dispositivo do Chrome DevTools Protocol — a
  página vê as dimensões em `window.innerWidth` e nas media queries [32].
- *Design Mode* [33]: transforma o browser em ferramenta de "apontar para o código". Ligando o
  toggle, o cursor vira seletor e destaca o elemento sob ele; ao clicar, o Orca captura o HTML
  do elemento (outerHTML e vizinhança), o CSS computado (cores, fontes, espaçamento), um
  screenshot recortado do elemento e o arquivo/linha de origem quando há source map de
  dev-mode disponível — tudo enviado ao terminal de agente ativo como **um attachment**, sobre
  o qual o operador escreve o que quer mudar. A bandeja de anotações permite acumular várias
  notas na página antes de enviar, com *Edit*, *Save* e *Cancel* por nota. O loop fechado:
  agente edita o código → Orca recarrega → clicar de novo para verificar [33][57].

**Arco narrativo:** revisar código gerado por IA é a habilidade central do operador de frota —
e o ADE existe, em boa medida, para tornar essa revisão barata o suficiente para ser obrigatória.

---
