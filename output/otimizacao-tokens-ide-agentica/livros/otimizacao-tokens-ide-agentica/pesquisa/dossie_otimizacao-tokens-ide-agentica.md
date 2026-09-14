# Dossiê Técnico — Otimização de Tokens em IDEs Agênticas Locais

Levantamento de fontes técnicas (Fase 1 da Fábrica Agêntica) para sustentar um livro que
faz a **auditoria** do manual de terceiros `agent-token-optimization-manual-v3.1.md` e
extrai dele o **núcleo real e verificável** de técnicas de economia de tokens em IDEs
agênticas locais. O manual mistura mecanismos genuínos (cache de prompt real da
Anthropic, Ollama, llmlingua, gptcache, paralelismo, circuit breaker, chezmoi, e até
produtos reais pouco conhecidos — Hermes Agent, Google Antigravity, Oh My Pi, Freebuff,
Orca ADE) com nomenclatura, caminhos de arquivo e sintaxe de comando **fabricados ou
incorretos**. Este dossiê documenta o que é real; o arquivo irmão `auditoria_manual_v3.1.md`
cruza cada afirmação do manual, LAB a LAB, com veredito e correção.

**Nota metodológica:** não houve mineração acadêmica relevante para este tema (é um tema
de ferramental de engenharia, não um campo de pesquisa com produção peer-reviewed) — a
sustentação é majoritariamente documentação oficial (classe A) e repositórios/pacotes
oficiais (classe B). Blogs de terceiros sem afiliação ao projeto entram como classe C,
usados só para contexto de uso real, nunca como fonte isolada de números. Classificação:
**(A)** documentação oficial/API primária do próprio fornecedor; **(B)** repositório
oficial do projeto/PyPI/npm; **(C)** terceiros (blogs, wikis, agregadores, imprensa
especializada).

**Aviso de janela temporal:** parte deste dossiê (TEMA 11) cobre produtos lançados ou
atualizados entre novembro/2025 e agosto/2026 (Google Antigravity, Grok Build, Oh My Pi,
Freebuff, MiMo Code) — posteriores ao corte de conhecimento do modelo que redigiu este
material. Todas as afirmações desses itens vêm de busca web ao vivo (data de acesso: 20
ago. 2026) e devem passar por nova conferência pontual do revisor técnico antes da
publicação final, dado o ritmo de mudança do ecossistema.

---

## TEMA 1 — Prompt Caching real (Anthropic Claude API)

### Resumo técnico

O cache de prompt da Anthropic é real e documentado, mas funciona de forma bem mais
restrita do que o manual descreve. O campo `cache_control` com `{"type": "ephemeral"}`
existe de fato na Messages API, mas é um campo do **payload da chamada de API** (JSON do
request), não um toggle de configuração de usuário em um arquivo `settings.json` de IDE.
Ele pode ser colocado (a) no nível raiz do request (cache automático do bloco mais recente
elegível) ou (b) em blocos de conteúdo individuais (`system`, `messages`, último item de
`tools[]`) como breakpoint explícito [1]. O TTL padrão é 5 minutos; existe variante de 1
hora com premium de preço maior [1]. O mínimo cacheável é 1024 tokens — blocos menores não
são cacheados mesmo com o marcador [1].

Os números reais são **multiplicadores de preço**, não um "desconto genérico de até 90%"
solto no ar como o manual sugere sem base: leitura de cache custa 0,1× o preço de input
padrão (ou seja, 90% mais barato), escrita de cache custa 1,25× (TTL 5 min) ou 2× (TTL 1h)
o preço de input padrão [1]. A documentação oficial **não publica um percentual fixo de
redução de latência** — fala apenas em melhora de time-to-first-token para documentos
longos, sem cifra fechada [1][2]. Isso significa que a alegação do manual de "até 90% de
desconto" é aproximadamente correta para cache **read**, mas a forma como o manual
generaliza (como se fosse um número universal de economia, incluindo em latência) exagera
o que a doc afirma.

O Claude Code (ferramenta CLI da Anthropic) lê configuração de usuário em
`~/.claude/settings.json` (global) e `.claude/settings.json`/`.claude/settings.local.json`
(projeto) — **não** em `~/.config/claude-code/settings.json` como o manual afirma [3].
Esse arquivo real aceita campos como `model`, `permissions`, `env`, `hooks`,
`apiKeyHelper`, `cleanupPeriodDays`, entre dezenas de outros — **não existe campo
`cacheControl` nem `systemPrompt` exposto ao usuário nesse arquivo** [3]. O prompt caching
do Claude Code é automático, gerenciado internamente pela ferramenta/API, sem toggle
manual de usuário. Hooks reais do Claude Code vivem dentro do próprio `settings.json`
(chave `hooks`), com eventos nomeados como `PreToolUse`/`PostToolUse`/`SessionStart`/`Stop`
— não em um arquivo separado `hooks.json` com campo `preProcess` como o manual descreve no
LAB 4 [4]. O que é real e documentado é que um arquivo `CLAUDE.md` na raiz do projeto é
lido e incluído automaticamente no contexto de cada sessão — isso o manual acerta [3].

### Fontes do tema (1–4)

1. ANTHROPIC. *Prompt caching*. Disponível em: https://platform.claude.com/docs/en/build-with-claude/prompt-caching. Acesso em: 20 ago. 2026. (A)
2. AGENTBRISK. *Prompt Caching Deep Dive: How to Cut Anthropic API Costs by 90%*. Disponível em: https://agentbrisk.com/blog/prompt-caching-deep-dive-2026/. Acesso em: 20 ago. 2026. (C)
3. ANTHROPIC. *Claude Code settings*. Disponível em: https://code.claude.com/docs/en/settings. Acesso em: 20 ago. 2026. (A)
4. ANTHROPIC. *Hooks reference*. Disponível em: https://code.claude.com/docs/en/hooks. Acesso em: 20 ago. 2026. (A)

---

## TEMA 2 — OpenCode e "OpenCode Zen"

### Resumo técnico

OpenCode é um projeto real de IDE agêntica (opencode.ai) e "Zen" é de fato o nome real do
gateway/marketplace de modelos hospedado pelo próprio time do OpenCode [5]. Até aqui o
manual acerta a existência da coisa. O que é fabricado é a **nomenclatura dos modelos**:
não existe nenhum modelo com sufixo `opencode-zen-free-tiny/small/medium/large/xlarge/
prompt/coder` — essa é uma convenção de nomes inventada. Os modelos reais do Zen seguem o
padrão `opencode/<model-id>` e incluem, entre pagos e gratuitos por tempo limitado:
GPT-5.x, Claude (Opus/Sonnet/Haiku), Gemini 3.x, Grok, Qwen3.x, DeepSeek-v4, Kimi-k, e como
gratuitos rotativos "Big Pickle" (modelo stealth para agentes de código), "Grok Code Fast
1", "MiMo-V2 Flash Free" (modelo aberto da Xiaomi), "Nemotron 3 Super/Ultra Free" (NVIDIA)
e variantes [6][7]. **Nota de confusão categorial:** "MiMo" citado pelo manual como uma
das "12 IDEs" do público-alvo é, dentro do próprio catálogo Zen, o nome de um MODELO
(Xiaomi MiMo) — mas a Xiaomi também mantém separadamente um produto de CLI de codificação
chamado "MiMo Code" (ver TEMA 11); são duas coisas relacionadas, mas distintas, e o manual
não deixa claro qual das duas está descrevendo.

O arquivo de configuração real do OpenCode não é `~/.config/opencode/config.json` com
campos `cacheControl`/`defaultModel`/`maxTokens` — é `opencode.json` (ou `.jsonc`), que
pode ficar em `~/.config/opencode/opencode.json(c)` (global) ou na raiz do projeto
(`./opencode.json`) [8]. O campo de modelo padrão real é `model` (formato
`provider/model-id`), não `defaultModel`; não existe campo `cacheControl` nem `maxTokens`
no nível raiz do schema documentado [8]. O schema real inclui campos como `$schema`,
`model`, `agent`, `permission`, `mcp`, entre outros [8].

### Fontes do tema (5–8)

5. OPENCODE. *Zen*. Disponível em: https://opencode.ai/docs/zen/. Acesso em: 20 ago. 2026. (A)
6. MAXIMAL STUDIO. *OpenCode Zen Free Models 2026: Every Free Provider and How to Use Them*. Disponível em: https://www.maximalstudio.in/blog/opencode-zen-free-models. Acesso em: 20 ago. 2026. (C)
7. BSWEN. *What Free AI Models Are Available in OpenCode and Which One Should You Use*. Disponível em: https://docs.bswen.com/blog/2026-04-21-free-models-opencode/. Acesso em: 20 ago. 2026. (C)
8. OPENCODE. *Config*. Disponível em: https://opencode.ai/v2/docs/config. Acesso em: 20 ago. 2026. (A)

---

## TEMA 3 — Aider e Codex CLI (config real)

### Resumo técnico

Aider é real e tem cache de prompt real — mas ativado via flag `--cache-prompts` (ou o
mesmo campo em `.aider.conf.yml`), que apenas liga o **cache automático do provider**
(Anthropic para modelos Claude), sem exposição de um campo `cache_control` granular ao
usuário [9]. Existe também `--cache-keepalive-pings` para manter o cache "quente" com
pings periódicos [10]. O Aider organiza o histórico do chat (system prompt, arquivos
read-only, repo map, arquivos editáveis) de forma otimizada para maximizar cache hit no
provider — isso é real e é essencialmente o mesmo princípio do TEMA 6 (context
engineering) [10]. O arquivo `~/.aider.conf.yml` é real e documentado [9].

O Codex CLI (OpenAI) usa de fato `~/.codex/config.toml`, mas os campos de modelo ficam no
**nível raiz do arquivo** (`model`, `model_provider`, `model_reasoning_effort`,
`model_context_window`, `wire_api`, etc.), não dentro de uma seção `[codex]` como o manual
afirma; a seção real para provedores customizados é `[model_providers.<id>]` [11][12]. A
API usada pelo Codex CLI moderno é a *Responses API* (`wire_api = "responses"` — suporte a
Chat Completions foi descontinuado) [12]. Não há evidência de um campo `cache_prompts`
documentado no Codex CLI — o prompt caching da OpenAI, quando aplicável, é automático.

### Fontes do tema (9–12)

9. AIDER. *YAML config file*. Disponível em: https://aider.chat/docs/config/aider_conf.html. Acesso em: 20 ago. 2026. (A)
10. AIDER. *Prompt caching*. Disponível em: https://aider.chat/docs/usage/caching.html. Acesso em: 20 ago. 2026. (A)
11. OPENAI. *codex/docs/config.md*. Disponível em: https://github.com/openai/codex/blob/main/docs/config.md. Acesso em: 20 ago. 2026. (B)
12. OPENAI. *Configuration Reference — Codex CLI*. Disponível em: https://developers.openai.com/codex/config-basic. Acesso em: 20 ago. 2026. (A)

---

## TEMA 4 — Ferramentas de tracking de tokens: ccusage, agenttrace, agentlytics

### Resumo técnico

`ccusage` é real, mas é uma ferramenta **Node/npm**, não um pacote Python instalável via
`pipx` — o uso real é `npx ccusage@latest <subcomando>` (sem instalação prévia necessária)
ou `npm install -g ccusage` [13]. Ela lê diretamente os arquivos JSONL locais que o Claude
Code (e, em versões recentes, Codex CLI) já gravam localmente (`~/.claude/projects/**`),
sem chamadas de API externas [13]. Subcomandos reais confirmados: `daily`, `weekly`,
`monthly`, `session`, `blocks` (janelas de 5h) [13][14]. Ela de fato reporta tokens de
cache separadamente (`cacheCreationTokens`, `cacheReadTokens`, `cacheHitRate`), então a
menção do manual a métricas de cache no `ccusage session` tem lastro real — só o método de
instalação (`pipx`), o nome exato do subcomando (`ccusage log --date`, inexistente) e o
nome exato do campo (`cache_hit_ratio`, o real é `cacheHitRate`) não conferem.

`agenttrace` **existe de verdade** no PyPI (`pip install agenttrace`), mantido pela
Tensorstax — é uma lib de observabilidade/tracing leve para agentes de IA [15]. `agentlytics`
**também existe de verdade**, mas é um projeto **completamente diferente**: um pacote npm
(`npx agentlytics`) que lê o histórico local de várias IDEs agênticas (Cursor, Windsurf,
Claude Code, VS Code Copilot, Zed, OpenCode) e apresenta um dashboard de custo/uso [16].
Ou seja: o manual instala `agenttrace` via pipx e depois verifica com `agentlytics
--version`/`agentlytics init`/`agentlytics status` — são **dois produtos reais e
distintos, de ecossistemas diferentes (PyPI vs. npm), sendo tratados como se fossem o
mesmo**. Nenhuma fonte primária confirma que qualquer um dos dois tenha exatamente os
subcomandos `init`/`status` citados pelo manual.

### Fontes do tema (13–16)

13. RYOPPIPPI. *ccusage: A CLI tool for analyzing Claude Code/Codex CLI usage from local JSONL files*. Disponível em: https://github.com/ryoppippi/ccusage. Acesso em: 20 ago. 2026. (B)
14. CLAUDELOG. *What is ccusage tool for Claude Code*. Disponível em: https://claudelog.com/faqs/what-is-ccusage-tool/. Acesso em: 20 ago. 2026. (C)
15. TENSORSTAX. *agenttrace: lightweight observability library to trace and evaluate agentic systems*. Disponível em: https://github.com/tensorstax/agenttrace. Acesso em: 20 ago. 2026. (B)
16. F. *agentlytics: Comprehensive analytics dashboard for AI coding agents*. Disponível em: https://github.com/f/agentlytics. Acesso em: 20 ago. 2026. (B)

---

## TEMA 5 — Compressão de prompt: LLMLingua real

### Resumo técnico

O pacote é real: `pip install llmlingua`, projeto oficial da Microsoft Research
(microsoft/LLMLingua no GitHub), com resultado publicado em EMNLP'23/ACL'24 e alegação
oficial de "até 20× de compressão com perda mínima de performance" [17]. A classe Python
real é `PromptCompressor` (`from llmlingua import PromptCompressor`), **não** `Llmlingua`
como o manual escreve [17]. O parâmetro real do método `compress_prompt` é `rate` (float
0–1; ou `target_token`), **não** `preservation_rate` [18]. "LongLLMLingua" não é um pacote
pip separado — é um modo de uso da mesma classe `PromptCompressor` (ex.: parâmetro
`rank_method="longllmlingua"`, reordenação de contexto para mitigar "lost in the middle"),
então `pipx install longllmlingua` como comando separado não corresponde à distribuição
real [17]. Não há evidência de uma CLI standalone `python -m llmlingua` na documentação
oficial do projeto — o uso documentado é via API Python, não terminal.

### Fontes do tema (17–18)

17. MICROSOFT. *LLMLingua* (repositório oficial). Disponível em: https://github.com/microsoft/LLMLingua. Acesso em: 20 ago. 2026. (B)
18. PYTHON PACKAGE INDEX. *llmlingua*. Disponível em: https://pypi.org/project/llmlingua/. Acesso em: 20 ago. 2026. (B)

---

## TEMA 6 — Response caching semântico: GPTCache real

### Resumo técnico

GPTCache é real (`pip install gptcache`, projeto Zilliztech), atua como um "memcache para
aplicações de IA generativa", com backend de similaridade semântica via embedding + vetor
(FAISS é uma das opções suportadas) [19]. A forma real de uso documentada é **inteiramente
programática**: `from gptcache import cache; from gptcache.adapter import openai;
cache.init(); cache.set_openai_key()` — não há evidência de uma **CLI de terminal** com
subcomandos `init`/`list`/`add`/`query`/`stats`/`clear` como o manual descreve; o único
processo de linha de comando real documentado é `gptcache_server -s <host> -p <porta>`
(modo servidor HTTP, com endpoints `/put`/`/get`) [19]. Não há confirmação de um arquivo de
configuração padrão em `~/.gptcache/config.yaml` — a configuração documentada é via
objeto/parâmetros Python (`Config(similarity_threshold=...)`), não YAML externo. O
conceito central (cache de resposta por similaridade semântica, evitando regerar respostas
para perguntas parecidas) é genuíno e vale manter no livro; a "camada de CLI" do manual é
fabricada.

### Fontes do tema (19)

19. ZILLIZTECH. *GPTCache: A Library for Creating Semantic Cache for LLM Queries* (docs/usage.md). Disponível em: https://github.com/zilliztech/GPTCache/blob/main/docs/usage.md. Acesso em: 20 ago. 2026. (B)

---

## TEMA 7 — Paralelismo real: asyncio, xargs, GNU parallel, circuit breaker, backoff

### Resumo técnico

Este é o tema com menor risco de fabricação no manual — todos os mecanismos são reais e
amplamente documentados. `asyncio.gather` e `asyncio.Semaphore` são API real da biblioteca
padrão do Python, usados corretamente pelo manual para orquestrar chamadas concorrentes
com limite de concorrência [20]. `xargs -P N -I {}` é sintaxe real do GNU findutils para
paralelismo de shell (comportamento documentado em `man xargs`). GNU parallel (`parallel -j
N 'cmd {}' ::: arg1 arg2`) é uma ferramenta real e madura, com `-j` para número de jobs e
`:::` para lista de argumentos de entrada [21]. O padrão circuit breaker (estados
CLOSED/OPEN/HALF_OPEN) é um padrão de arquitetura de resiliência real e amplamente
documentado [22]. Backoff exponencial com jitter para retry em rate limit também é prática
real e documentada [23]. A implementação de código do manual (classe `CircuitBreaker`,
`RateLimiter`, `call_with_exponential_backoff`) é conceitualmente correta e não precisa de
correção — é o único bloco grande do manual que não fabrica nada. A única ressalva é a
cifra "economia de 80% do tempo" com paralelismo 5×, que é uma ilustração matemática
genérica, não um número documentado por nenhuma fonte (depende do overhead real e do rate
limit do provider).

### Fontes do tema (20–23)

20. PYTHON SOFTWARE FOUNDATION. *asyncio — Asynchronous I/O*. Disponível em: https://docs.python.org/3/library/asyncio.html. Acesso em: 20 ago. 2026. (A)
21. GNU. *GNU Parallel*. Disponível em: https://www.gnu.org/software/parallel/. Acesso em: 20 ago. 2026. (A)
22. MICROSOFT. *Circuit Breaker pattern — Azure Architecture Center*. Disponível em: https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker. Acesso em: 20 ago. 2026. (A)
23. AMAZON WEB SERVICES. *Timeouts, retries and backoff with jitter — Builders' Library*. Disponível em: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/. Acesso em: 20 ago. 2026. (A)

---

## TEMA 8 — Ollama, llama.cpp e vLLM (modelos locais offline)

### Resumo técnico

Ollama é real (github.com/ollama/ollama), com CLI real confirmada: `ollama pull <modelo>`,
`ollama run <modelo>`, `ollama list`, `ollama serve`, `ollama --version`, porta padrão
11434 [24]. Os 7 modelos citados pelo manual — `qwen2.5-coder`, `codestral`, `llama3.1`,
`zephyr`, `mistral`, `dolphin-mistral`, `starcoder2` — são famílias de modelo confirmadas
na Ollama library oficial (verificado individualmente: `codestral` 22B, `starcoder2`
3B/7B/15B, `zephyr` incluindo tag `7b`, `dolphin-mistral` 7B/15B) [25]. Os tamanhos de
RAM/download citados no manual são plausíveis e compatíveis com a ordem de grandeza real de
modelos quantizados de 3B–22B parâmetros em GGUF (ex.: 7B ≈ 4-5GB), mas devem ser
reconferidos na página de cada modelo no momento da publicação (os tags mudam de
disponibilidade com o tempo).

O comando de instalação real do Ollama no Linux é `curl -fsSL https://ollama.com/install.sh
| sh`, que bate exatamente com o que o manual usa [24]. `llama.cpp` é real e hoje mantido
sob a organização **`ggml-org`** no GitHub (antes associado a `ggerganov`) [26]. O binário
`./main` citado pelo manual foi **renomeado para `llama-cli`** desde a PR #7809 (junho de
2024) — junto com `server` → `llama-server`; a flag de contexto também tende a aparecer
como `-c` em vez de `-ctx-size` nas versões atuais [26]. O `vLLM` real usa o comando `vllm
serve <modelo> --gpu-memory-utilization 0.9 --host 0.0.0.0 --port 8000` (CLI dedicada) —
não `python -m vllm.server` como o manual afirma (esse módulo não existe); a forma antiga
`python -m vllm.entrypoints.openai.api_server` apareceu em versões anteriores, mas nunca se
chamou `vllm.server` [27].

### Fontes do tema (24–27)

24. OLLAMA. *ollama/ollama*. Disponível em: https://github.com/ollama/ollama. Acesso em: 20 ago. 2026. (B)
25. OLLAMA. *Library* (catálogo de modelos). Disponível em: https://ollama.com/library. Acesso em: 20 ago. 2026. (B)
26. GGML-ORG. *llama.cpp*. Disponível em: https://github.com/ggml-org/llama.cpp. Acesso em: 20 ago. 2026. (B)
27. VLLM PROJECT. *CLI Reference — serve*. Disponível em: https://docs.vllm.ai/en/stable/cli/serve/. Acesso em: 20 ago. 2026. (A)

---

## TEMA 9 — Hermes Agent (NousResearch): o achado mais delicado do dossiê

### Resumo técnico

Este é o ponto mais importante do dossiê para o livro: **"Hermes" citado pelo manual como
uma "IDE agêntica" com skills, cron, delegação, memória e busca em sessões corresponde, de
fato, a um produto real** — Hermes Agent, da NousResearch (mesma empresa por trás dos
modelos Hermes de LLM), um agente pessoal de IA com CLI, TUI, gateway multi-plataforma
(Telegram/Discord/Slack/WhatsApp) e integração de IDE (VS Code/Zed/JetBrains via ACP), com
memória persistente entre sessões, sistema de "Skills" auto-gerado a cada ~15 chamadas de
ferramenta, cron scheduler nativo e delegação para subagentes paralelos [28][29][30]. A
doc oficial explicita que Hermes **não é um copiloto de IDE tradicional** — é um agente
pessoal de propósito geral que também sabe programar.

Onde o manual erra: os **nomes exatos de campo e a sintaxe de comando não batem** com a CLI
real documentada.

- **Skills:** o verbo real é `install`/`browse`/`list` (`hermes skills install <id>`,
  comando `skills` no plural) — não existe `hermes skill activate <nome>` [29].
- **Cron:** a sintaxe real documentada é posicional, `hermes cron create "<agenda>"
  "<prompt>"` (ou `hermes cron create "<prompt>" [--skill NOME]`, conforme a versão da
  doc), com subcomandos `list/edit/pause/resume/run/remove/status` — não existem flags
  `--name`/`--schedule`/`--deliver` na forma exata do manual [29][30].
- **Memória:** os comandos reais são `hermes memory setup/status/off` (configuração de
  provedor de memória) — não existe `hermes memory add --target user --content "..."` [29].
- **Sessões:** o subcomando real é `sessions` no **plural**
  (`hermes sessions list/browse/export/delete/prune/rename/stats`, e retomada via `hermes
  --resume <id>`/`hermes -r`) — não existe `hermes session search --query`/`hermes session
  read --session-id` no singular como o manual descreve [29].
- **Config:** o arquivo `~/.hermes/config.yaml` é real (o manual acerta o caminho), com
  campos documentados como `model`, `terminal`, `memory`, `skills`, `agent`,
  `prompt_caching`, `runtime`, `worktree` — mas **não** `system_prompt` nem
  `cache_control: {type: ephemeral}` como o manual escreve [30].

**Implicação para o livro:** este é o melhor "gancho de ensino" do manual — mostra que uma
fabricação parcial (sintaxe errada) em cima de um produto real (existência confirmada) é
mais perigosa que uma fabricação total, porque o operador confia no nome real e copia o
comando errado sem desconfiar.

### Fontes do tema (28–30)

28. NOUSRESEARCH. *hermes-agent*. Disponível em: https://github.com/NousResearch/hermes-agent. Acesso em: 20 ago. 2026. (B)
29. NOUSRESEARCH. *CLI Interface — Hermes Agent*. Disponível em: https://hermes-agent.nousresearch.com/docs/user-guide/cli. Acesso em: 20 ago. 2026. (A)
30. NOUSRESEARCH. *Configuration — Hermes Agent*. Disponível em: https://hermes-agent.nousresearch.com/docs/user-guide/configuration. Acesso em: 20 ago. 2026. (A)

---

## TEMA 10 — Dotfiles: chezmoi real

### Resumo técnico

`chezmoi` é uma ferramenta real e madura de gerenciamento de dotfiles (twpayne/chezmoi,
chezmoi.io) [31]. Comandos reais confirmados: `chezmoi init`, `chezmoi add <arquivo>`,
`chezmoi status` — batem com o que o manual descreve [31]. O único ponto impreciso é o
**instalador**: o manual usa `curl -sL https://git.io/chezmoi | sh` (um encurtador
antigo/legado, `git.io` foi descontinuado pelo GitHub para criação de novos links desde
2022, embora links legados possam continuar redirecionando); o instalador oficial atual
documentado é `sh -c "$(curl -fsLS https://get.chezmoi.io)"` [31]. Outro ponto de atenção:
`chezmoi commit -m "..."` **não é um subcomando nativo do chezmoi** — o commit acontece
dentro do diretório-fonte gerenciado pelo Git (via `chezmoi cd` seguido de `git commit`, via
`chezmoi git commit -- -m "..."`, ou automaticamente se `autoCommit: true` estiver
configurado) [31]. Fora do escopo de suspeita do manual, mas verificado por completude: o
1Password CLI (`op signin`, `op item create --title ... --vault ... --generate-password`,
`op read "op://Private/API Key/password"`) é real e bate com a sintaxe documentada da CLI
v2, incluindo o formato de referência de secret `op://vault/item/field` [32].

### Fontes do tema (31–32)

31. CHEZMOI. *Install* e *Daily operations*. Disponível em: https://www.chezmoi.io/install/. Acesso em: 20 ago. 2026. (A)
32. 1PASSWORD. *op signin — CLI command reference*. Disponível em: https://developer.1password.com/docs/cli/reference/commands/signin. Acesso em: 20 ago. 2026. (A)

---

## TEMA 11 — As "outras 7 IDEs": produtos reais, caminhos de config não confirmados

### Resumo técnico

O manual lista, além de Claude Code/OpenCode/Aider/Codex/Hermes, mais 7 "IDEs agênticas":
MiMo, Antigravity, Google CLI, Oh My Pi, Freebuff, Grok e Orca, cada uma com um caminho de
config e campo de cache_control na tabela do LAB 1. Investigação individual mostra que
**nenhuma das 7 é fabricada como produto** — todas correspondem a ferramentas reais
lançadas ou atualizadas entre nov./2025 e mai./2026 — mas em **6 dos 7 casos o caminho de
configuração citado não foi confirmado** em documentação primária, e em 2 casos o **nome
do produto está impreciso**.

- **MiMo** → produto real é **MiMo Code** (Xiaomi, `XiaomiMiMo/MiMo-Code`), CLI de
  codificação por agente. Config real observada é `mimocode.json` por projeto (não
  `~/.mimo/config.yaml` como o manual afirma) [33]. Ver também TEMA 2: "MiMo" é também o
  nome de um modelo gratuito do catálogo OpenCode Zen — duas coisas relacionadas (mesmo
  fabricante), mas distintas.
- **Antigravity** → **Google Antigravity**, IDE agent-first anunciada em preview público em
  18 nov. 2025 junto ao Gemini 3 Pro, fork do VS Code construído por ex-equipe Windsurf
  [34][35]. Caminho `~/.antigravity/settings.json` citado pelo manual **não foi confirmado**
  em fonte primária.
- **"Google CLI"** → não existe produto com esse nome exato; a ferramenta real do Google é
  o **Gemini CLI** (`google-gemini/gemini-cli`), com config real em
  `~/.gemini/settings.json` [36][37] — o manual erra tanto o nome do produto quanto o
  caminho (`~/.google-ai/configurerc`, **fabricado**).
- **Oh My Pi** → real: "omp" (Oh My Pi), fork do framework Pi (Mario Zechner), agente de
  terminal open-source [38][39]. Caminho `~/.oh-my-pi/config.toml` **não confirmado** em
  fonte primária.
- **Freebuff** → real: Freebuff CLI, agente de codificação gratuito (YC-backed), instalado
  via `npm install -g freebuff` [40][41]. Caminho `~/.freebuff/config.json` **não
  confirmado** em fonte primária.
- **Grok** → o produto real de codificação da xAI chama-se **Grok Build**
  (`xai-org/grok-build`, lançado mai. 2026) [42][43] — "Grok" sozinho é o nome do
  modelo/chat, não do CLI de codificação; o manual usa um nome impreciso. Caminho
  `~/.grok/config.yaml` **não confirmado**.
- **Orca** → real: **Orca ADE** (onorca.dev), ambiente open-source (MIT) para rodar
  múltiplos agentes (Claude Code, Codex, OpenCode, Cursor CLI) em worktrees paralelos —
  bate com a descrição geral do público-alvo do manual [44][45]. Caminho
  `~/.orca/config.json` **não confirmado** em fonte primária.

**Implicação para o livro:** o padrão de erro aqui é o mesmo do TEMA 9 (Hermes) em escala
menor — produto real + caminho de configuração inventado/não verificável. Nenhum desses 7
itens deve ser citado com o caminho de arquivo exato do manual sem a ressalva de "não
confirmado nesta auditoria".

### Fontes do tema (33–45)

33. XIAOMIMIMO. *MiMo-Code*. Disponível em: https://github.com/XiaomiMiMo/MiMo-Code. Acesso em: 20 ago. 2026. (B)
34. GOOGLE. *Build with Google Antigravity — our new agentic development platform*. Disponível em: https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/. Acesso em: 20 ago. 2026. (A)
35. WIKIPEDIA. *Google Antigravity*. Disponível em: https://en.wikipedia.org/wiki/Google_Antigravity. Acesso em: 20 ago. 2026. (C)
36. GOOGLE-GEMINI. *gemini-cli*. Disponível em: https://github.com/google-gemini/gemini-cli. Acesso em: 20 ago. 2026. (B)
37. GOOGLE. *Gemini CLI — Configuration*. Disponível em: https://geminicli.com/docs/reference/configuration/. Acesso em: 20 ago. 2026. (A)
38. OH MY PI. *omp.sh*. Disponível em: https://omp.sh/. Acesso em: 20 ago. 2026. (B)
39. BETTERSTACK. *Oh My Pi: a deep dive into the AI coding agent*. Disponível em: https://betterstack.com/community/guides/ai/oh-my-pi-ai-coding-agent/. Acesso em: 20 ago. 2026. (C)
40. FREEBUFF. *Freebuff CLI*. Disponível em: https://freebuff.com/cli. Acesso em: 20 ago. 2026. (B)
41. Y COMBINATOR. *Freebuff*. Disponível em: https://www.ycombinator.com/companies/freebuff. Acesso em: 20 ago. 2026. (C)
42. XAI-ORG. *grok-build*. Disponível em: https://github.com/xai-org/grok-build. Acesso em: 20 ago. 2026. (B)
43. XAI. *Introducing Grok Build*. Disponível em: https://x.ai/news/grok-build-cli. Acesso em: 20 ago. 2026. (A)
44. ORCA. *Orca ADE*. Disponível em: https://www.onorca.dev/. Acesso em: 20 ago. 2026. (A)
45. ORCA. *Docs*. Disponível em: https://www.onorca.dev/docs. Acesso em: 20 ago. 2026. (A)

---

## Síntese para o arquiteto (o que sobra de real após a auditoria)

Núcleo genuíno e ensinável, por ordem de solidez de fonte:

1. Prompt caching real da Anthropic (TEMA 1) — mecanismo, payload, multiplicadores de preço reais (~90% de desconto em cache read).
2. Paralelismo com asyncio/xargs/GNU parallel + circuit breaker + backoff exponencial (TEMA 7) — 100% correto no manual, zero correção necessária.
3. Ollama + modelos locais como fallback offline (TEMA 8) — real, com pequenas correções de comando (`llama-cli`, `vllm serve`).
4. chezmoi para versionamento de dotfiles (TEMA 10) — real, só o instalador e o `commit` diferem.
5. LLMLingua e GPTCache como bibliotecas Python reais de compressão/cache semântico (TEMAS 5–6) — reais, mas usados errado como se tivessem CLI/API que não têm.
6. ccusage como ferramenta real de análise de uso do Claude Code via npm/npx (TEMA 4).
7. Hermes Agent como produto real com memória/skills/cron/delegação (TEMA 9) — a lição mais valiosa do livro: nome e conceito reais, sintaxe fabricada.
8. OpenCode Zen como gateway real de modelos gratuitos — mas com nomenclatura de modelo 100% inventada (TEMA 2).
9. As demais 7 "IDEs" citadas (TEMA 11) — todas produtos reais de 2025-2026, mas caminhos de configuração majoritariamente não confirmáveis; 2 delas usam nome impreciso do produto (Google CLI → Gemini CLI; Grok → Grok Build).

O núcleo do livro é ensinar o leitor a nunca copiar comando de manual de terceiros sem
verificar contra a documentação oficial — e este dossiê + a auditoria anexa são a evidência
central desse argumento.
