# Dossiê — Blocos Temáticos 1 a 8

> Parte I (Fundamentos) e Parte II (O Ambiente) do livro `livros/orca-ade`.
> Cada bloco reúne os fatos verificados que sustentam um capítulo, com o número da
> fonte entre colchetes (ver `dossie_orca-ade.md` §2).

---

## BLOCO 1 — A crise do trabalho serial (Cap. 1)

**Fatos coletados**

- Categoria oficial do produto: "Orca is a desktop IDE for running multiple AI coding
  agents side by side. Every task gets its own git worktree, its own agent terminal, and
  its own browser tab — so you can fan out work across Claude Code, Codex, Cursor CLI,
  and friends without stashing, branch-juggling, or losing flow" [1].
- Casos de uso declarados: (a) rodar três agentes no mesmo bug em paralelo e escolher o
  vencedor; (b) revisar a sério diffs gerados por IA antes de publicar; (c) já pagar por
  Claude Code, Codex ou Cursor CLI e querer um único lugar para orquestrá-los; (d) rodar
  agentes remotos (SSH, servidor Orca próprio, VM sob demanda) sem abandonar a IDE [1].
- Público-alvo declarado: "people who already write code for a living and want to use AI
  as leverage — not as a replacement. It assumes you read diffs, care about commits, and
  keep a worktree tidy" [1].
- Negativas de posicionamento (fronteiras explícitas): **não é um modelo** (roda agentes
  com a assinatura do operador); **não substitui o git** (todo worktree é um git worktree
  real, inspecionável com git puro); **não é um produto de VPS hospedado** (roda no desktop
  por padrão; o remoto usa máquinas e contas de nuvem do próprio usuário) [1].
- O fluxo canônico, em sete verbos, é declarado como "the whole of Orca":
  `add → worktree → agent → split → diff → ship`, e "every other page in these docs is a
  deeper look at one of those steps" [3].
- Racional econômico do paralelismo: "Different agents make different mistakes. Running
  the same task in parallel is cheaper than sequential retries and surfaces disagreement
  as a signal. Where three agents agree, the answer is probably right. Where they split,
  you've found the hard part" [53].
- Escala de adoção verificável: repositório com **67,2 mil estrelas** e **4,4 mil forks**;
  release mais recente **v1.4.200**, em **11 de setembro de 2026**, com cadência de
  publicação praticamente diária [65][66].
- Distinção conceitual entre *workflow* e *agente*: "Workflows are systems where LLMs and
  tools are orchestrated through predefined code paths. Agents [...] are systems where LLMs
  dynamically direct their own processes and tool usage" [63]. O Orca opera no segundo
  regime e por isso precisa de isolamento físico, não apenas de disciplina.
- Recomendação de engenharia: "we recommend finding the simplest solution possible, and
  only increasing complexity when needed", reconhecendo que sistemas agênticos trocam
  latência e custo por desempenho [63].

**Arco narrativo do capítulo:** o gargalo deixa de ser a geração de código e passa a ser a
**serialização** do trabalho — um agente, um terminal, um repositório, uma fila.

---

## BLOCO 2 — O que é o Orca ADE (Cap. 2)

**Fatos coletados**

- O fluxo mínimo completo, "do app vazio a três agentes em paralelo em menos de cinco
  minutos", tem seis passos nomeados: (1) adicionar repositório; (2) criar worktree;
  (3) escolher agente; (4) correr três agentes na mesma tarefa; (5) dividir painéis para
  assistir a todos; (6) escolher vencedor, revisar o diff e publicar [3].
- Ao adicionar um repositório, o Orca "reads the repo's git state and picks up your default
  branch as its base ref — the ref every new worktree branches from", alterável depois nas
  configurações do repositório [3].
- O lançador de workspace abre com o agente padrão pré-selecionado (configurável em
  `Settings → Agents`) ou um terminal vazio [3].
- Ao criar um worktree, o Orca "creates a real git worktree under its managed directory,
  checks out the branch, and opens it" [3].
- Ao lançar um agente, o Orca "will launch the agent's CLI with the correct working
  directory and forward your subscription credentials" [3].
- Três branches, três diffs, o mesmo prompt — e o perdedores são removidos "with one
  click; their branches go with them" [3].
- O produto se autodescreve no repositório como "The AI Orchestrator for 100x builders.
  Run Codex, ClaudeCode, OpenCode or Pi side-by-side — each in its own worktree, tracked in
  one place" [65].
- Distribuição: macOS (Apple Silicon e Intel), Windows (instalador), Linux (AppImage, .deb,
  .rpm), além de cask Homebrew `brew install --cask stablyai/orca/orca`; versões antigas no
  GitHub Releases [2].
- Primeiro lançamento: pede acesso ao diretório home para adicionar repositórios, oferece
  importar `~/.claude`, `~/.codex` e configurações do terminal Ghostty, e entrega uma tela
  vazia onde o primeiro repositório é adicionado [2].
- Canais de atualização: estável (vetado) e RC (release candidate, "often daily"). Não há
  opt-in permanente no app: cliques modificadores em *Check for Updates* —
  `Shift+click` inclui o RC mais recente; `Cmd/Ctrl+click` traz o último pré-release com
  tag de performance; `Option+click` (só macOS) escolhe um build local validado pelos
  testes de compatibilidade [2][49].
- Nota de plataforma: no Linux "the Linux CLI is named `orca-ide` so it does not conflict
  with the GNOME Orca screen reader" [2].
- No Windows, o shell padrão é configurável entre PowerShell, Prompt de Comando e WSL,
  sendo WSL oferecido automaticamente quando `wsl.exe --status` tem sucesso [20].
- Nomeação: se o nome do worktree é deixado em branco, o Orca o nomeia com um nome de
  criatura marinha; há configuração de prefixo customizado (`Default new-worktree name`) [3][49].
- O app traz idiomas de interface: System, English, 中文（简体）, 한국어, 日本語, Español,
  e a busca de configurações também casa palavras nativas para "language" [49].
- Ecossistema: aplicativo iOS na App Store e TestFlight, **APK Android na versão 0.0.48**,
  e runtime remoto [65][46].

**Arco narrativo:** vocabulário mínimo necessário e arquitetura de três camadas
(hub de worktrees → painéis de agentes → camada de revisão), sem exigir que o leitor
escreva uma linha de código.

---

## BLOCO 3 — Instalação e primeira sessão (Cap. 3)

**Fatos coletados**

- Requisitos de horário e esforço declarados pela própria doc: "From empty app to three
  agents running in parallel in under five minutes" [3].
- Instalação por plataforma: macOS assinado e notarizado (o macOS pode ainda pedir
  confirmação na primeira execução, "normal for Electron-based apps"); no Windows o shell
  padrão é configurável; no Linux a AppImage é a via para autoatualização, enquanto .deb e
  .rpm apenas reportam atualizações e entregam o comando do gerenciador de pacotes [2].
- O app é Electron (embute Chromium e Node.js) [71] e o terminal é baseado em xterm.js —
  "the same xterm.js-based terminal VS Code uses" [20][70].
- Ao criar um worktree, a criação roda em segundo plano: "Submitting the Create Worktree
  dialog closes it immediately — the git fetch and git worktree add work continues in the
  background while you keep using Orca", com linha de progresso na barra lateral, status ao
  vivo na aba, possibilidade de cancelar e *Retry* em caso de falha [4].
- O seletor *start-from* aceita: base ref do repositório (caminho rápido), outra branch
  local (útil para empilhar trabalho sobre um PR em revisão), um SHA de commit específico,
  ou uma branch remota existente que o Orca busca e faz checkout [4].
- Nomes de branch com emoji: a UI aceita shortcodes estilo Slack (`:rocket:`) com popover
  de sugestão; ao derivar o nome de branch, emojis conhecidos são reescritos para
  shortcodes legíveis (🚀 → rocket) e a busca do *Jump Palette* casa esses fragmentos [4].
- O diálogo de criação usa comboboxes com *type-ahead* para *Project* e *Run on*;
  digitar filtra, `Enter` confirma a linha armada. *Project* sempre mantém
  "Add a new project" fixado no rodapé, para que a criação nunca termine em beco sem saída [4].
- *Run on* lista hosts prontos e recipes, além de hosts que ainda precisam de configuração
  de projeto naquela máquina; em host "setup-needed" é possível escolher
  "Set project location" sem sair do formulário de criação [4].
- Em um worktree novo, a aba mostra um chip de *Restart* quando o agente sai (limpo ou por
  crash); um clique reidrata o mesmo agente no mesmo diretório de trabalho [5].
- "Hybrid stub" de skills: após `npx skills add`, o agente lê um stub curto e resolve o guia
  completo com `orca skills get <topic>` (ou `--full` para o guia longo) [38].
- Verificação de runtime do CLI: `command -v orca` e `orca status --json`; se o Orca não
  estiver rodando, `orca open --json` [36].
- Troubleshooting de primeiros passos documentado: agente que não inicia (rodar a CLI
  manualmente; conferir `PATH` em `Settings → Agents`; usar o chip *Restart*);
  worktree que falha na criação (rodar `git fetch origin`; branch já existente);
  CLI "command not found" (registrar em `Settings → General → Orca CLI`; no macOS instala um
  shim em `~/.local/bin`, que precisa estar no `PATH`) [51].

**Arco narrativo:** tutorial completo, do download ao PR, com pontos de falha reais e o
que fazer em cada um.

---

## BLOCO 4 — Git worktrees como fundação (Cap. 4)

**Fatos coletados**

- Declaração de arquitetura: "Orca is worktree-native. Instead of branching and stashing on
  one checkout, every task gets its own on-disk copy of the repo via `git worktree`. This is
  what makes parallel agents safe — they never step on each other's files" [4].
- O modelo tem três invariantes: cada repositório tem uma **base ref** (usualmente
  `origin/main`); cada worktree tem um **start-from ref**; cada worktree tem **branch
  própria, arquivos próprios em disco e terminais de agente próprios** [4].
- Ciclo de vida por funcionalidade, em cinco fases nomeadas: **Create** (nome da tarefa,
  seletor start-from, vínculo opcional a GitHub/Linear/Jira/GitLab), **Work** (terminais de
  agente, abas de editor, abas de browser e painéis de terminal escopados ao worktree),
  **Review** (diff contra o start-from ref, Annotate AI Diff, Attribution),
  **Ship** (commit, push, abrir PR, aguardar checks — tudo inline),
  **Archive or delete** (um clique remove worktree e branch) [4].
- Deleção: "Deleting a worktree removes both the directory and the branch (with
  confirmation). If git keeps a local branch because it may still have unmerged commits,
  Orca can offer a review step" (*Preserved branches*) [4].
- Git por trás: `git worktree` é comando nativo do Git ("Manage multiple working trees"),
  cuja assinatura inclui `git worktree add [-f] [--detach] [--checkout] [--lock [--reason
  <string>]] [--orphan] [(-b | -B) <new-branch>]`, documentado desde versões antigas e sem
  mudanças entre 2.54.0 (2026-04-20) e 2.55.0 [62].
- **Diretórios compartilhados e arquivos gitignored** — o problema real de um checkout novo:
  "A brand-new worktree is a clean checkout. Dependencies, caches, and local secrets that
  live in gitignored paths are missing until you recreate them." O Orca preenche a lacuna de
  três formas complementares [4]:
  1. **Worktree Shared Paths** (por repositório, em `Settings → Repository`) — caminhos
     materializados do checkout primário para cada novo worktree (clone-copy APFS no macOS
     quando possível; caso contrário, symlink).
  2. **`worktree.sharedDirectories` em `orca.yaml`** — lista versionada no repositório de
     diretórios gitignored a compartilhar do mesmo modo (symlink/share, não cópia). Serve
     para árvores grandes e reconstruíveis como `node_modules` ou `.cache`. Entradas
     precisam existir como diretórios no checkout primário **e** ser gitignored; caminhos
     rastreados ou ausentes são ignorados.
  3. **`.worktreeinclude` na raiz do repositório** — lista de arquivos ou diretórios
     gitignored a **copiar** (não linkar) em cada worktree novo, para que cada worktree
     tenha a sua cópia. Entradas típicas: `.env`, configurações locais em `.vscode/`.
     Linhas em branco e comentários `#` são permitidos. **Apenas caminhos literais são
     suportados hoje** — globs e negação são ignorados com aviso. Caminhos rastreados,
     ausentes ou não-gitignored não são copiados.
  - Regra de precedência: entradas de `orca.yaml` **somam-se** à lista por usuário
    (nunca a substituem), e caminhos já compartilhados/linkados não são recopiados a partir
    do `.worktreeinclude` [4].
- Exemplo literal da documentação [4]:
  ```yaml
  # orca.yaml (raiz do repositório)
  worktree:
    sharedDirectories:
      - node_modules
      - .cache
  ```
  ```text
  # .worktreeinclude (raiz do repositório)
  .env
  .env.local
  .vscode/settings.json
  ```
- **Worktrees aninhados (parent/child)**: ao criar um worktree **de dentro** de um worktree
  gerenciado pelo Orca, o novo passa a ser registrado como filho quando a relação é
  inferível; `--parent-worktree active` explicit a relação e `--no-parent` declara trabalho
  independente [36]. O campo *Parent workspace* no drawer *Advanced* apenas aninha os
  workspaces na barra lateral — **não** altera histórico nem branches do Git; o Orca exclui
  workspaces arquivados e escolhas que criariam ciclo [4].
- Exclusão por teclado: com o cursor sobre um worktree ou pasta, `Cmd-Shift-Backspace`
  (macOS) ou `Ctrl-Shift-Backspace` (Windows/Linux) inicia a deleção, mantendo o diálogo de
  confirmação. `Cmd`/`Ctrl` + clique adiciona itens à multi-seleção; `Shift` seleciona um
  intervalo contíguo; o clique direito aplica a ação a **toda** a seleção [4].
- Filtros da barra lateral: cabeçalho com filtro próprio (separado da busca global) e um
  menu que agrupa escopo de host/projeto sob uma seção **Show**, além dos toggles
  *Sleeping workspaces*, *Except default branch*, *Default branch workspaces*,
  *Automation-created workspaces*, *CLI-created workspaces*, *Other-client workspaces* e
  *Detached HEAD workspaces*. Um contador de filtros ativos aparece no controle e
  *Clear* reseta apenas os filtros ligados [4].
- Importação de pastas com múltiplos repositórios Git: o Orca pode importá-los
  separadamente ou agrupá-los sob um único grupo de projeto [4].
- Detalhe de usabilidade: worktrees não lidos aparecem **em negrito**, não com badge; o
  botão *Search* no topo da barra lateral abre o *Worktree Jump Palette* (`Cmd-J`) para quem
  prefere clique a teclado [4].

**Arco narrativo:** por que `git worktree` (e não `git stash`, clonagem ou troca de branch)
é a única base que torna o paralelismo de agentes seguro; inclui o tratamento do problema
mais traiçoeiro — dependências e segredos ausentes em checkouts limpos.

---
