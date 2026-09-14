# Dossiê de Pesquisa — ORCA ADE: O Guia Definitivo do Ambiente de Desenvolvimento Agêntico

> Obra: `livros/orca-ade` · Tipo: Livro · Tamanho: GG (4 Partes, 16 capítulos, ~160 páginas)
> Público: Iniciante · Mínimo de referências por capítulo: 20
> Data da mineração: 12 set. 2026 · Fonte primária: documentação oficial `onorca.dev/docs`

---

## 1. Metodologia e escopo

### 1.1 Pergunta de pesquisa

Como um desenvolvedor que nunca operou múltiplos agentes de código constrói, do zero,
um **ambiente de desenvolvimento agêntico (ADE)** capaz de conduzir uma frota de agentes
de IA em paralelo, com isolamento, revisão séria de diffs e entrega soberana — e como
projetar esse fluxo para durar além da ferramenta que o hospeda hoje?

### 1.2 Estratégia de coleta

1. **Varredura integral do sitemap oficial** (`https://www.onorca.dev/sitemap.xml`) —
   inventário de **61 URLs** publicadas, com `lastmod` de 11-09-2026. Todas as URLs
   citadas nesta obra foram extraídas desse inventário ou verificadas individualmente
   (HTTP 200) durante esta mineração.
2. **Leitura profunda de 25 páginas** da documentação oficial, cobrindo instalação,
   primeira sessão, modelo de worktrees, agentes, terminal, revisão, browser, CLI,
   orquestração, automações, computer use, SSH, servidores remotos, configuração e
   solução de problemas.
3. **Mineração acadêmica determinística** via APIs abertas (`scripts/minerar-fontes-academicas.py`):
   10 fontes classe A recuperadas no Crossref (OpenAlex, PubMed e SciELO devolveram
   zero resultados relevantes; arXiv e Semantic Scholar falharam por timeout/HTTP 429).
4. **Verificação de fontes externas** por requisição direta, preservando o título
   oficial e a URL final após redirecionamentos (Git, Anthropic, MCP, Tailscale, NIST,
   xterm.js, Electron, SQLite, MDN, GitHub).

### 1.3 Critério de fidelidade

- Todo dado factual apresentado na obra é rastreável a uma fonte desta lista.
- Onde a documentação oficial **não** afirma algo, a obra marca explicitamente como
  inferência de engenharia ou lacuna declarada (ver §7 — Lacunas e ressalvas).
- Comandos de CLI (gate R-CLI) têm **fonte A** — foram copiados literalmente da
  documentação oficial.

### 1.4 Fronteiras de escopo (o que esta obra NÃO é)

- Não é um tutorial de programação — o leitor não precisa escrever código de produção,
  mas precisa saber ler diffs e operar um terminal.
- Não é um manual de um modelo de linguagem específico: o Orca é agnóstico de agente e
  de assinatura (o operador traz a sua).
- Não é documentação oficial nem publicação da Stably AI — é obra didática de terceiro,
  fundamentada na documentação pública.

---

## 2. Inventário de fontes

Legenda de classe (hierarquia R-FT):
**A** = documentação oficial do produto, especificação técnica ou publicação primária
verificável; **B** = documentação técnica de terceiro com autoridade reconhecida;
**C** = material de apoio, secundário ou de contexto.

### 2.1 Documentação oficial do Orca (classe A) — 61 URLs

| # | Título | URL |
|---|---|---|
| [1] | What is Orca? | https://www.onorca.dev/docs |
| [2] | Install | https://www.onorca.dev/docs/install |
| [3] | Your first 3-agent session | https://www.onorca.dev/docs/first-session |
| [4] | Worktrees | https://www.onorca.dev/docs/model/worktrees |
| [5] | Agents & sessions | https://www.onorca.dev/docs/model/agents-sessions |
| [6] | Tabs, panes & split layouts | https://www.onorca.dev/docs/model/tabs-panes-splits |
| [7] | Quick open | https://www.onorca.dev/docs/model/quick-open |
| [8] | Session restore | https://www.onorca.dev/docs/model/session-restore |
| [9] | Supported agents | https://www.onorca.dev/docs/agents/supported |
| [10] | Claude Code in Orca | https://www.onorca.dev/docs/agents/claude-code |
| [11] | Codex in Orca | https://www.onorca.dev/docs/agents/codex |
| [12] | Hot-swap Codex accounts | https://www.onorca.dev/docs/agents/codex-hot-swap |
| [13] | Cursor CLI in Orca | https://www.onorca.dev/docs/agents/cursor-cli |
| [14] | GLM agent | https://www.onorca.dev/docs/agents/glm-agent |
| [15] | Agent hibernation | https://www.onorca.dev/docs/agents/hibernation |
| [16] | Agent hooks & memory | https://www.onorca.dev/docs/agents/hooks-memory |
| [17] | Native chat | https://www.onorca.dev/docs/agents/native-chat |
| [18] | Agent session history | https://www.onorca.dev/docs/agents/session-history |
| [19] | Usage & rate-limit tracking | https://www.onorca.dev/docs/agents/usage-tracking |
| [20] | Terminal | https://www.onorca.dev/docs/terminal |
| [21] | File explorer | https://www.onorca.dev/docs/editing/file-explorer |
| [22] | Markdown | https://www.onorca.dev/docs/editing/markdown |
| [23] | Monaco editor | https://www.onorca.dev/docs/editing/monaco |
| [24] | Viewers | https://www.onorca.dev/docs/editing/viewers |
| [25] | Diff viewer | https://www.onorca.dev/docs/review/diff-viewer |
| [26] | Annotate AI Diff | https://www.onorca.dev/docs/review/annotate-ai-diff |
| [27] | Attribution | https://www.onorca.dev/docs/review/attribution |
| [28] | Commit & push from Orca | https://www.onorca.dev/docs/review/commit-push |
| [29] | GitHub in Orca | https://www.onorca.dev/docs/review/github |
| [30] | Linear in Orca | https://www.onorca.dev/docs/review/linear |
| [31] | Jira in Orca | https://www.onorca.dev/docs/review/jira |
| [32] | Per-worktree browser | https://www.onorca.dev/docs/browser/overview |
| [33] | Design Mode | https://www.onorca.dev/docs/browser/design-mode |
| [34] | Browser-use profiles | https://www.onorca.dev/docs/browser/profiles |
| [35] | Orca CLI overview | https://www.onorca.dev/docs/cli/overview |
| [36] | Orca CLI reference | https://www.onorca.dev/docs/cli/reference |
| [37] | Orchestration | https://www.onorca.dev/docs/cli/orchestration |
| [38] | Skills registry & MCP | https://www.onorca.dev/docs/cli/skills |
| [39] | Worktree checkpoints | https://www.onorca.dev/docs/cli/worktree-checkpoints |
| [40] | Scheduled automations | https://www.onorca.dev/docs/cli/automations |
| [41] | Computer use | https://www.onorca.dev/docs/cli/computer-use |
| [42] | Ways to run Orca | https://www.onorca.dev/docs/ways-to-run |
| [43] | SSH worktrees | https://www.onorca.dev/docs/ssh |
| [44] | Remote Orca Servers | https://www.onorca.dev/docs/remote-servers |
| [45] | Mobile | https://www.onorca.dev/docs/mobile |
| [46] | Android APK | https://www.onorca.dev/docs/android-apk |
| [47] | Notifications & Inbox | https://www.onorca.dev/docs/notifications |
| [48] | Activity | https://www.onorca.dev/docs/activity |
| [49] | Settings reference | https://www.onorca.dev/docs/settings |
| [50] | Telemetry | https://www.onorca.dev/docs/telemetry |
| [51] | Troubleshooting & FAQ | https://www.onorca.dev/docs/troubleshooting |
| [52] | Troubleshooting GitHub errors | https://www.onorca.dev/docs/github-errors |
| [53] | Recipe: Race three agents | https://www.onorca.dev/docs/recipes/parallel-agents |
| [54] | Recipe: Jump between worktrees | https://www.onorca.dev/docs/recipes/jump-worktrees |
| [55] | Recipe: Remote worktrees | https://www.onorca.dev/docs/recipes/remote-worktrees |
| [56] | Recipe: Review an AI diff | https://www.onorca.dev/docs/recipes/review-ai-diff |
| [57] | Recipe: Fix a UI bug with Design Mode | https://www.onorca.dev/docs/recipes/design-mode-fix |
| [58] | Download | https://www.onorca.dev/download |
| [59] | Enterprise | https://www.onorca.dev/enterprise |
| [60] | Changelog | https://www.onorca.dev/changelog |
| [61] | Site raiz | https://www.onorca.dev |

### 2.2 Fontes externas verificadas (classe A/B)

| # | Referência | URL | Verificação |
|---|---|---|---|
| [62] | GIT. *git-worktree(1)* — Manual de referência, v2.54.0 (2026-04-20) | https://git-scm.com/docs/git-worktree | 200 |
| [63] | ANTHROPIC. *Building effective agents* | https://www.anthropic.com/engineering/building-effective-agents | 200 (redirect) |
| [64] | MODEL CONTEXT PROTOCOL. *What is MCP?* | https://modelcontextprotocol.io/introduction | 200 |
| [65] | STABLY AI. *Orca* — repositório oficial (67,2 mil estrelas; 4,4 mil forks) | https://github.com/stablyai/orca | 200 |
| [66] | STABLY AI. *Orca Releases* — v1.4.200 (11 set. 2026) | https://github.com/stablyai/orca/releases | 200 |
| [67] | TAILSCALE. *What is Tailscale?* | https://tailscale.com/docs/concepts/what-is-tailscale | 200 |
| [68] | NIST. *AI Risk Management Framework* | https://www.nist.gov/itl/ai-risk-management-framework | 200 |
| [69] | ANTHROPIC. *Claude Code — Overview* | https://code.claude.com/docs/en/overview | 200 (redirect) |
| [70] | XTERM.JS. *Xterm.js* — terminal front-end | https://xtermjs.org/ | 200 |
| [71] | ELECTRON. *Build cross-platform desktop apps* | https://www.electronjs.org/ | 200 |
| [72] | SQLITE. *Write-Ahead Logging* | https://sqlite.org/wal.html | 200 |
| [73] | MDN. *Using HTTP cookies* | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies | 200 |

### 2.3 Fontes mineradas em bases acadêmicas (classe A)

| # | Referência | Identificador |
|---|---|---|
| [74] | MALISZEWSKI, A. et al. *Ambiente de Nuvem Computacional Privada para Teste e Desenvolvimento de Programas Paralelos*. ERAD/RS, 2021. | https://doi.org/10.5753/sbc.6150.4.5 |
| [75] | ROSSI, E. G. *Ambiente de apoio ao desenvolvimento de aplicações distribuídas e reconfiguráveis...*. USP, 2009. | https://doi.org/10.11606/d.18.2009.tde-24092009-154121 |
| [76] | SANT'ANA, T. D. *ASTRAL — Ambiente de Simulação e Teste de pRogramas paraLelos*. USP, 2018. | https://doi.org/10.11606/d.55.2018.tde-24012018-111858 |
| [77] | LAINE, J. M. *Desenvolvimento de modelos para predição de desempenho de programas paralelos MPI*. USP, 2003. | https://doi.org/10.11606/d.3.2003.tde-28082003-184400 |
| [78] | BIANCHINI, C. de P. *Um ambiente para programação orientada a objetos distribuídos e paralelos em grades computacionais*. USP, 2009. | https://doi.org/10.11606/t.3.2009.tde-26032009-171120 |
| [79] | CORTÉS, O. A. C. *Desenvolvimento e Avaliação de Algoritmos Numéricos Paralelos*. USP, 2018. | https://doi.org/10.11606/d.55.2018.tde-09032018-135249 |
| [80] | OKUDA, K. *Desenvolvimento formal de algoritmos paralelos sistólicos*. USP, 1989. | https://doi.org/10.11606/d.45.1989.tde-20220712-113641 |
| [81] | ENCINAS, D. O. *Modelización y simulación basada en agentes aplicada a la arquitectura de entrada/salida de los computadores paralelos*. UNLP, 2024. | https://doi.org/10.35537/10915/194710 |
| [82] | ANDRADE, F. M. R. de; BARRETO, T. B.; HENRIQUES, A. B. *Crise climática na cidade do Rio de Janeiro: agentes e territórios de informação no Twitter*. Desenvolvimento e Meio Ambiente, 2023. | https://doi.org/10.5380/dma.v62i0.86679 |
| [83] | MOLINA, F. A. L. *Ambiente de simulação de manipuladores paralelos*. UNICAMP, 2008. | https://doi.org/10.47749/t/unicamp.2008.437988 |

### 2.4 Avaliação crítica da base

- **Força:** a documentação oficial é excepcionalmente detalhada em comportamento de
  produto, com nomes exatos de painéis, flags de CLI e regras de ciclo de vida. É a
  melhor fonte possível para um livro operacional.
- **Fraqueza estrutural:** documentação de produto é **efêmera**. A obra neutraliza isso
  ensinando o *modelo mental* (worktree como unidade de isolamento; agente como processo
  descartável; diff como contrato de revisão) antes de ensinar o botão que o executa.
- **Fraqueza da mineração acadêmica:** as bases abertas retornam predominantemente
  dissertações brasileiras sobre *computação paralela clássica* (MPI, grades, algoritmos),
  não sobre orquestração de agentes de LLM. Sua contribuição legítima aqui é conceitual:
  paralelismo, isolamento de recursos e ambientes descartáveis são problemas antigos com
  vocabulário novo. Foram classificadas como A por serem publicações primárias revisadas,
  mas o uso será de **contexto histórico**, nunca de sustentação de fatos sobre o Orca.

---

## 3. Glossário canônico (vocabulário da obra)

| Termo | Definição operacional (fonte) |
|---|---|
| **ADE** (Agent Development Environment) | Ambiente integrado cujo objeto de trabalho não é um arquivo, mas um **agente** rodando em um contexto isolado. O próprio repositório se autodescreve como "the ADE for working with a fleet of parallel agents" [65]. |
| **Worktree** | Cópia de trabalho em disco criada por `git worktree`, ligada ao mesmo repositório, com branch própria. É a unidade de isolamento — o que impede dois agentes de pisarem nos arquivos um do outro [4][62]. |
| **Base ref** | Referência do repositório (usualmente `origin/main`) da qual novos worktrees ramificam por padrão [3][4]. |
| **Start-from ref** | Referência específica escolhida na criação do worktree: base ref, branch local, SHA ou branch remota [4]. |
| **Sessão de agente** | Uma CLI de agente rodando em um terminal, em um worktree [5]. |
| **Harness** | A aplicação hospedeira que intermedeia humano, sistema operacional e modelo. O Orca é um harness-agnóstico: "bring your own Claude, Codex, or OpenCode subscription" [1][65]. |
| **Run** | Namespace durável de orquestração com caixa de entrada própria. Nunca agenda nem posiciona workers [37]. |
| **Task** | Item de trabalho com spec, dependências e status (`pending`, `ready`, `dispatched`, `completed`, `failed`, `blocked`) [37]. |
| **Dispatch** | Uma tentativa de executar uma task em um terminal; detém a autoridade sobre `worker_done`/`heartbeat` [37]. |
| **Decision gate** | Pergunta de propriedade do coordenador que bloqueia uma task até ser resolvida [37]. |
| **Skill** | Pacote de instruções instalável no diretório de skills do agente. No Orca, os pacotes públicos são *stubs híbridos*: apontam para o guia vivo no binário, para que as flags nunca divirjam da versão do app [38]. |
| **Attribution** | Registro local de procedência por linha, distinguindo o que veio de agente do que veio de humano. Não é commitado [27]. |
| **Hibernação** | Pausa automática de terminais de agente ociosos, com retomada da mesma sessão ao reabrir o worktree [15]. |
| **Checkpoint de worktree** | Campo de texto livre por worktree, visível na UI, mantido por humanos e agentes para registrar o estado atual do trabalho [39]. |

---
