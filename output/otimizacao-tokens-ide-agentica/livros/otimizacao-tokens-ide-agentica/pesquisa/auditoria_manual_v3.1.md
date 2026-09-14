# Auditoria — `agent-token-optimization-manual-v3.1.md`

Base factual OBRIGATÓRIA para arquiteto e redatores: cruzamento item a item de cada
afirmação verificável do manual de terceiros contra fontes primárias (numeração [N] remete
a `dossie_otimizacao-tokens-ide-agentica.md`). Vereditos: **CONFIRMADO** (bate com a fonte
primária), **PARCIALMENTE CORRETO** (o conceito/ferramenta é real, mas nome de
campo/comando/caminho está errado), **FABRICADO** (não existe base real, nome/comando
inventado), **NÃO VERIFICÁVEL** (não há fonte primária pública para confirmar nem refutar).

**Regra de uso pelos redatores:** nunca reproduzir uma linha marcada **FABRICADO** ou
**PARCIALMENTE CORRETO** como se fosse comando real — sempre usar a coluna "Correção".

---

## LAB 0 — Setup e Verificação

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| `pip install pipx` / `pipx ensurepath` (Windows admin) | Sintaxe de instalação do pipx | CONFIRMADO | (B) pypa/pipx — documentação oficial | Correto como descrito. |
| `pipx install ccusage` | ccusage instalável via pipx | **FABRICADO** | [13] ccusage é pacote npm/Node, não Python | Usar `npx ccusage@latest <subcomando>` ou `npm install -g ccusage`. pipx só instala pacotes Python — o comando falha. |
| `pipx install agenttrace` | agenttrace instalável via pipx | CONFIRMADO | [15] pacote real no PyPI | Comando correto — mas ver linha abaixo sobre a verificação. |
| `pipx install llmlingua` | Instalação via pipx | PARCIALMENTE CORRETO | [17][18] pacote real no PyPI, mas biblioteca Python sem CLI standalone | pipx é pensado para instalar CLIs isoladas; llmlingua é lib importável — instalar com `pip install llmlingua` em ambiente de projeto, não gera comando de terminal utilizável. |
| `pipx install gptcache` | Instalação via pipx | PARCIALMENTE CORRETO | [19] pacote real, biblioteca pura sem CLI de subcomandos | Mesma ressalva — `pip install gptcache` em ambiente de projeto; único binário real é `gptcache_server` (modo servidor). |
| `pipx install ollama` | Ollama instalável via pipx | **FABRICADO** | [24] Ollama é binário nativo, não pacote Python | Instalar via `curl -fsSL https://ollama.com/install.sh \| sh` (Linux) ou instalador nativo `.exe`/`.dmg`. |
| `agentlytics --version` verificando o pacote instalado como `agenttrace` | Comando de verificação | **FABRICADO** (confusão de produtos) | [15][16] `agenttrace` (PyPI/Tensorstax) e `agentlytics` (npm) são dois produtos reais e distintos | Verificar `agenttrace` com o comando do próprio pacote Python; `agentlytics` é outro produto (`npx agentlytics`), sem relação com o `pipx install` anterior. |
| `ccusage --version` deve retornar >= 0.5 | — | NÃO VERIFICÁVEL | [13] ferramenta real | Número de versão mínima citado é arbitrário, sem marco documentado. |

---

## LAB 1 — Prompt Caching por IDE

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| Desconto de cache "pode chegar a 90% em prompts grandes" | Conceito geral | CONFIRMADO | [1] cache read = 0,1× preço padrão = 90% de desconto | Especificar que é 90% no **read**; write tem premium de 1,25×–2×. Latência não tem percentual fixo documentado — não generalizar. |
| Arquivo Claude Code `~/.config/claude-code/settings.json` com `systemPrompt`/`cacheControl` | Local e campos de config | **FABRICADO** | [3] caminho real é `~/.claude/settings.json` (usuário) / `.claude/settings.json` (projeto); campos reais incluem `model`, `permissions`, `env`, `hooks` — sem `cacheControl`/`systemPrompt` | Usar `~/.claude/settings.json`; cache é automático via API, não é toggle de usuário. |
| `CLAUDE.md` incluído automaticamente no contexto | — | CONFIRMADO | [3] | Correto, e é a mesma convenção usada por este projeto. |
| Arquivo OpenCode `~/.config/opencode/config.json` com `cacheControl`/`defaultModel`/`maxTokens` | Config real do OpenCode | **FABRICADO** (nome de arquivo e campos) | [8] arquivo real é `opencode.json`/`.jsonc`; campo real de modelo é `model` (`provider/model-id`) | Usar `opencode.json` com `{"model": "opencode/<id>"}`; sem `cacheControl`/`maxTokens` no schema. |
| Aider `~/.aider.conf.yml` com `cache-prompts: true` | — | CONFIRMADO | [9][10] | Correto — default `false`, habilitável via `cache-prompts: true` ou `--cache-prompts`. |
| Codex `~/.codex/config.toml` seção `[codex]` com `cache_prompts`/`model`/`max_tokens` | Config real do Codex CLI | PARCIALMENTE CORRETO | [11][12] caminho do arquivo certo; campos reais ficam no nível raiz, não em seção `[codex]`; `cache_prompts` não documentado | Usar `model = "..."` no nível raiz; provedores customizados em `[model_providers.<id>]`; não criar seção `[codex]`. |
| Hermes `~/.hermes/config.yaml` com `system_prompt`/`cache_control.type: ephemeral` | Config real do Hermes | PARCIALMENTE CORRETO | [30] caminho do arquivo é real; existe campo real `prompt_caching`, mas não `system_prompt` nem `cache_control.type` | Consultar campos reais: `model`, `memory`, `skills`, `prompt_caching`, `agent`, `terminal`, `runtime`, `worktree`. |
| Tabela das outras 7 IDEs (MiMo, Antigravity, Google CLI, Oh My Pi, Freebuff, Grok, Orca) com caminho/campo de cache | Caminhos de config para 7 ferramentas | PARCIALMENTE CORRETO | [33]-[45] todas as 7 são produtos reais (MiMo Code, Google Antigravity, Gemini CLI, Oh My Pi/omp, Freebuff CLI, Grok Build, Orca ADE), mas os caminhos de config exatos do manual **não foram confirmados** em fonte primária para nenhuma das 7; "Google CLI" e "Grok" usam nome impreciso do produto real | Corrigir nomes (Google CLI → Gemini CLI, config `~/.gemini/settings.json` confirmado [36][37]; Grok → Grok Build); tratar os demais 5 caminhos como não confirmados, exigindo conferência pontual antes de publicar. |
| `ccusage session` mostra `cache_hit_ratio`/`cached_tokens` | Métricas de cache disponíveis | PARCIALMENTE CORRETO | [13] `ccusage session --json` expõe `cacheCreationTokens`, `cacheReadTokens`, `cacheHitRate` | Nome real do campo é `cacheHitRate`, não `cache_hit_ratio`/`cache_hit` — conceito correto, nomenclatura errada. |

---

## LAB 2 — Modelos Free + Roteamento

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| "OpenCode Zen" existe como gateway de modelos gratuitos | — | CONFIRMADO | [5] gateway curado de modelos para agentes de código, camada gratuita sem cartão de crédito | — |
| 7 modelos `opencode-zen-free-tiny/small/medium/large/xlarge/prompt/coder` + tabela de specs | Nomes exatos e especificações | **FABRICADO** | [5][6][7] nomenclatura real é `opencode/<model-id>` (ex.: Big Pickle, Grok Code Fast 1, MiMo-V2 Flash Free, Nemotron 3 Free) | Substituir pelos nomes reais do catálogo Zen vigente no momento da escrita (catálogo muda com frequência — checar `opencode.ai/docs/zen/` antes de publicar). Tabela de specs é consequência direta do erro — não há como ser real para modelo inexistente. |
| `~/.config/claude-code/settings.json` com `model: "opencode-zen-free-medium"` | Config de modelo do Claude Code | **FABRICADO** | [3] caminho errado (ver LAB 1) e nome de modelo inexistente | Além da correção de caminho, apontar Claude Code para modelo de terceiro exige configuração de provider customizado, não uma chave simples. |
| Aliases bash (`cc-tiny`...`cc-xlarge`) trocando `$CLAUDE_MODEL`/`$OPENCODE_MODEL`/etc. | Troca de modelo via variável de ambiente | NÃO VERIFICÁVEL | — | Nenhuma das 4 ferramentas documenta oficialmente essas variáveis de ambiente para seleção de modelo — cada uma tem seu próprio mecanismo (`/model` no REPL do Claude Code, flag `--model`, campo `model` no config). Não presumir env var sem checar a doc de cada ferramenta. |

---

## LAB 3 — Prompt Compression (llmlingua)

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| Compressão de prompt reduz tokens preservando significado | Conceito geral | CONFIRMADO | [17] até 20× de compressão, EMNLP'23/ACL'24 | — |
| `from llmlingua import Llmlingua; Llmlingua().compress_prompt(prompt, preservation_rate=0.5)` | API Python | **FABRICADO** | [17] classe real é `PromptCompressor` | `from llmlingua import PromptCompressor; compressor = PromptCompressor(); compressor.compress_prompt(prompt, rate=0.5)`. |
| `python -m llmlingua --help` / `--preserve` | CLI de terminal | **FABRICADO** | [17][18] sem interface `__main__` documentada | Não existe CLI — reescrever o wrapper `compress-prompt` para importar `PromptCompressor` em Python. |
| `pipx install longllmlingua` como pacote separado | — | **FABRICADO** | [17] é modo de uso da mesma classe (`rank_method="longllmlingua"`) | Usar `PromptCompressor` com o parâmetro de reordenação de contexto longo, não instalação separada. |
| Tabela de benchmarks de compressão por tipo de conteúdo (70-85%, 40-60% etc.) | Taxas por categoria | NÃO VERIFICÁVEL | — | Sem lastro em benchmark publicado por categoria de conteúdo — plausível, mas não documentado pelo projeto. Usar a cifra oficial "até 20×" como teto, não os percentuais por categoria. |

---

## LAB 4 — Response Caching Semântico (gptcache)

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| GPTCache guarda respostas e reutiliza por similaridade semântica (SQLite + FAISS + embeddings) | Conceito geral | CONFIRMADO | [19] arquitetura modular real, vector store/storage plugáveis | — |
| `gptcache init`/`list`/`add --prompt...`/`query --prompt...`/`stats`/`clear` | CLI de terminal | **FABRICADO** | [19] não existe CLI com esses subcomandos | Usar API Python (`cache.init()`, `cache.data_manager`, adapters); único binário real é `gptcache_server -s <host> -p <porta>`. |
| `gptcache.cache_init()` / `gptcache.GPTCache(namespace=..., similarity_threshold=...)` | API Python | **FABRICADO** | [19] classe real é `Cache`, inicializada via `.init(...)` | Usar `from gptcache import cache; cache.init(...)` — sem parâmetro `namespace` nativo dessa forma. |
| Arquivo `~/.gptcache/config.yaml` com `similarity_threshold`/`ttl`/`namespace`/`vector_compare_method` | Config declarativa YAML | **FABRICADO** | [19] configuração é 100% programática (objetos Python) | Configurar via `Config(similarity_threshold=...)` no próprio script — não há YAML externo documentado. |
| Hook `~/.config/claude-code/hooks.json` com campo `preProcess` | Mecanismo de hook do Claude Code | **FABRICADO** | [4] hooks reais vivem em `settings.json` (chave `hooks`), eventos `PreToolUse`/`PostToolUse` | Configurar hooks dentro de `~/.claude/settings.json`, sem arquivo separado nem evento `preProcess`. |

---

## LAB 5 — Batch e Paralelismo

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| `asyncio.gather` + `asyncio.Semaphore` | Código de paralelismo | CONFIRMADO | [20] | — |
| `xargs -P 5 -I {}` | Sintaxe shell | CONFIRMADO | GNU findutils, `man xargs` | — |
| GNU `parallel -j 5 'cmd {}' ::: a b c` | Sintaxe shell | CONFIRMADO | [21] | — |
| "Hermes delegation" para paralelismo (Task → subagente) | Delegação de subtarefas | CONFIRMADO (conceito) | [28][29] Hermes Agent tem delegação real para subagentes | Sintaxe exata de invocação não documentada publicamente com a forma do manual — tratar como conceito, não copiar sintaxe literal. |
| RateLimiter + backoff exponencial com jitter | Padrão de engenharia | CONFIRMADO | [23] | — |
| "Economia de 80% do tempo" com paralelismo 5× | — | NÃO VERIFICÁVEL como número universal | — | Matemática genérica válida como ilustração, mas depende do overhead real e rate limit do provider — apresentar como exemplo, não garantia. |

---

## LAB 6 — Context Engineering (CLAUDE.md)

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| CLAUDE.md estático e ordem fixa de blocos maximizam cache hit | Conceito | CONFIRMADO | [1][3] decorre diretamente da mecânica real de cache (prefixo idêntico byte-a-byte) | — |
| Não incluir timestamp dinâmico no system prompt (invalida cache) | Erro comum | CONFIRMADO | [1] qualquer alteração no prefixo cacheado invalida o cache a partir dali | — |
| Hash SHA-256 do CLAUDE.md para detectar mudança | Script de verificação | CONFIRMADO (técnica genérica) | — | `sha256sum` é utilitário padrão; técnica válida, não depende de ferramenta fabricada. |

---

## LAB 7 — Orçamento / Hard Limits

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| Script `token-guard` usando `ccusage log --date`/`ccusage session` | — | PARCIALMENTE CORRETO | [13] subcomandos reais são `daily`/`weekly`/`monthly`/`session`/`blocks`; não há `log --date` | Usar `ccusage daily --json` (com filtro de data) ou `ccusage session --json` e adaptar o parsing. |
| Conceito de hard limit / circuit breaker financeiro | — | CONFIRMADO (engenharia genérica) | — | Script `token-guard` é legítimo, desde que corrija a chamada ao ccusage. |
| Cron via `crontab -e` | Mecanismo de agendamento Linux | CONFIRMADO | — | Real e padrão em sistemas Unix. |

---

## LAB 8 — Fallback e Resiliência

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| Circuit breaker (CLOSED/OPEN/HALF_OPEN) | — | CONFIRMADO | [22] | — |
| Fallback para Ollama local (`ollama run qwen2.5-coder:7b`) | — | CONFIRMADO | [24][25] | — |
| `ollama pull qwen2.5-coder:7b`, `codestral:22b`, `llama3.1:8b`, `zephyr:7b`, `mistral:7b`, `dolphin-mistral:7b`, `starcoder2:3b` | Modelos/tags existem na library | CONFIRMADO | [25] confirmado individualmente: codestral 22B, starcoder2 3B/7B/15B, zephyr (tag `7b`), dolphin-mistral 7B/15B; qwen2.5-coder/llama3.1/mistral são famílias amplamente disponíveis | — |
| Backoff exponencial com jitter | — | CONFIRMADO | [23] | — |

---

## LAB 9 — Hermes Avançado

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| Hermes existe como agente real com skills/cron/delegação/memória/session search | Existência do produto | CONFIRMADO | [28][29][30] Hermes Agent (NousResearch) real, open-source | Não é produto fabricado, ao contrário da suspeita inicial. |
| `~/.hermes/skills/<nome>/SKILL.md` + `hermes skill activate <nome>` | Sintaxe de ativação de skill | **FABRICADO** (sintaxe; mecanismo real) | [29] verbo real é `install`/`browse`/`list`; Skills são majoritariamente auto-geradas pelo próprio agente | `hermes skills install <id>` — não existe `skill activate`. |
| `hermes cron create --name ... --schedule "..." --prompt "..." --deliver origin` | Sintaxe de criação de cron | **FABRICADO** (sintaxe; mecanismo real) | [29][30] sintaxe real é posicional (`hermes cron create "<prompt>" [--skill NOME]`), sem flags `--name`/`--schedule`/`--deliver` | Usar `hermes cron create "<prompt/agenda>"` e checar `hermes cron --help` para as flags da versão instalada. |
| `hermes cron list` / `hermes cron remove <id>` | — | CONFIRMADO | [29] subcomandos `list`/`remove` existem | — |
| `hermes memory add --target user --content "..."` / `hermes memory list --target user` | Comandos de memória | **FABRICADO** (sintaxe) | [29] comandos reais são `hermes memory setup`/`status`/`off` | Usar `hermes memory setup` para configurar o provedor de memória — gestão fina é interna ao agente, não via flags `--target`/`--content`. |
| `hermes session search --query "..." --limit N` / `hermes session read --session-id <ID>` | Comandos de busca de sessão | **FABRICADO** (sintaxe) | [29] subcomando real é `sessions` (plural): `list/browse/export/delete/prune/rename/stats`; retomada via `hermes --resume <id>` | Usar `hermes sessions browse` ou `hermes sessions list` com filtros reais — não existe `session search`/`session read` no singular. |

---

## LAB 10 — Dotfiles, Equipe e Versionamento

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| `chezmoi init`, `chezmoi add <arquivo>` | Comandos reais | CONFIRMADO | [31] | — |
| `chezmoi commit -m "..."` | Subcomando nativo de commit | **FABRICADO** | [31] chezmoi não tem subcomando `commit` nativo | Usar `chezmoi cd && git commit -m "..."`, `chezmoi git commit -- -m "..."`, ou configurar `autoCommit: true`. |
| `curl -sL https://git.io/chezmoi \| sh` | Método de instalação | PARCIALMENTE CORRETO | [31] `git.io` é encurtador legado (sem novos links desde 2022) | Usar `sh -c "$(curl -fsLS https://get.chezmoi.io)"`. |
| 1Password CLI: `op signin`, `op item create --title ... --vault ... --generate-password`, `op read "op://Private/API Key/password"` | Comandos reais do `op` | CONFIRMADO | [32] sintaxe compatível com CLI v2 documentada; `op://vault/item/field` é formato real de secret reference | — |

---

## LAB 11 — Benchmarks Práticos

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| Tabela de latência/tokens/qualidade por "modelo" `opencode-zen-free-*` | Dados de benchmark | **FABRICADO** (dado sintético para modelo inexistente) | Herda o problema do LAB 2 — modelos não existem com esses nomes | Refazer a tabela com os modelos reais do catálogo Zen vigente no momento da publicação. |
| Script `benchmark-model` cronometrando com `date +%s%N` | Técnica de medição em bash | CONFIRMADO (engenharia genérica) | — | Válida — só trocar os nomes de modelo do exemplo pelos reais. |

---

## LAB 12 — Modelos Locais Offline

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| Tabela de 7 modelos Ollama com RAM mínima/tamanho de download | Especificações | CONFIRMADO (modelos existem; tamanhos plausíveis) | [25] | Conferir tags exatas no momento da publicação (podem mudar). |
| `curl -fsSL https://ollama.com/install.sh \| sh` | Instalação real | CONFIRMADO | [24] | — |
| `./main -m models/... -p "..." -ngl 32 -ctx-size 4096` (llama.cpp) | Nome do binário e flags | PARCIALMENTE CORRETO | [26] binário renomeado para `llama-cli` desde jun/2024 (PR #7809); repositório migrado para org `ggml-org` | Usar `./llama-cli -m ... -p ... -ngl 32 -c 4096` (verificar `--help` da versão instalada para a flag de contexto). |
| `python -m vllm.server --model ... --gpu-memory-utilization 0.9 --host ... --port ...` | Comando de servidor vLLM | **FABRICADO** (módulo inexistente) | [27] | Usar `vllm serve <modelo> --gpu-memory-utilization 0.9 --host 0.0.0.0 --port 8000`. |
| Estratégia híbrida com `ping api.openai.com`/`ping api.anthropic.com` | Detecção de conectividade | CONFIRMADO (engenharia genérica, mérito técnico) | — | Técnica válida, embora frágil (ICMP pode estar bloqueado mesmo com API acessível via HTTPS). |

---

## LAB 13 — Troubleshooting

| Item | Afirmação do manual | Veredito | Evidência/fonte | Correção |
|---|---|---|---|---|
| `gptcache clear` para limpar cache | Comando de manutenção | **FABRICADO** | [19] | Mesma falha do LAB 4 — sem CLI `gptcache` com esse subcomando. |
| `ollama serve &`, `ollama list`, checar porta 11434 | Diagnóstico | CONFIRMADO | [24] Ollama expõe API na porta 11434 por padrão | — |
| `hermes skill activate daily-flow` (troubleshooting) | Comando de ativação | **FABRICADO** (mesma ressalva do LAB 9) | [29] | Ver LAB 9 — mecanismo real de skill é diferente. |
| `agentlytics init`/`agentlytics status` para corrigir "Agent-trace não está logando" | Comandos de diagnóstico | **FABRICADO** (confusão de produtos, de novo) | [15][16] | Mesmo erro do LAB 0 — separar claramente `agenttrace` (PyPI) de `agentlytics` (npm). |
| Demais itens de troubleshooting (cache, modelo, compressão, rate limit, RAM, CLAUDE.md, cron, PATH) | — | CONFIRMADO (diagnósticos genéricos coerentes com mecanismos já auditados) | Ver LABs 1, 2, 3, 5, 6, 9, 12 | Manter — não dependem de nomenclatura fabricada. |

---

## LAB 14 e LAB 15 — Checklists e Resumo

Ambos os LABs são compilações/resumos dos itens já auditados — não introduzem afirmações
técnicas novas. Herdam os vereditos já registrados (ex.: checklist do LAB 1 herda o
veredito FABRICADO do caminho `~/.config/claude-code/settings.json`; a tabela "ferramenta ×
config global × config projeto" do LAB 15 repete os mesmos caminhos/nomes já corrigidos e
deve ser reescrita com os caminhos reais consolidados neste documento).

---

## Resumo quantitativo

| Veredito | Ocorrências aproximadas |
|---|---|
| CONFIRMADO | 26 |
| PARCIALMENTE CORRETO | 13 |
| FABRICADO | 18 |
| NÃO VERIFICÁVEL | 4 |

O manual tem núcleo técnico real relevante (por volta de 40% dos itens auditados), mas erra
sistematicamente em três frentes: (1) nomenclatura de modelo (OpenCode Zen), (2) caminho de
arquivo de configuração (Claude Code, OpenCode, e as 7 IDEs do TEMA 11), e (3) sintaxe de
CLI de ferramentas que existem de verdade mas foram documentadas de memória/aproximação
(Hermes Agent, llmlingua, gptcache, ccusage/agenttrace/agentlytics). O livro deve usar
exatamente esse padrão de erro como o argumento central: **ferramenta real + sintaxe
inventada é o modo de fabricação mais perigoso**, porque passa despercebido por quem só
reconhece o nome do produto.
