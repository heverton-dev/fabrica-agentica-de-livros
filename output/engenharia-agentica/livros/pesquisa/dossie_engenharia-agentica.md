# Dossiê de Pesquisa — Engenharia Agêntica: configurações, segredos e arquitetura dos agentes reais

Dossiê principal da obra. Cobre o harness (configurações, skills, rules, `AGENTS.md`,
`settings.json`, MCPs, agents/subagentes, scripts, gates, hooks), a fronteira
determinismo × probabilismo, economia severa de tokens, orquestração (Orca ADE,
worktrees, turnos agênticos), cache de prompt, roteamento de LLM, otimização de
contexto e os segredos universais portáveis entre harnesses. As fontes mineradas
por API aberta estão nos dossiês `dossie_min_*.md` (mesmo diretório) e são
incorporadas integralmente pela seção "Fontes brutas" abaixo.

## Conceitos-chave

- **Harness agêntico:** o conjunto de configurações, prompts de sistema, ferramentas,
  hooks e políticas que transforma um LLM stateless em um agente com memória
  operacional. É o objeto central da obra: o modelo é probabilístico, o harness é o
  que se pode tornar determinístico (ANTHROPIC, *Effective context engineering for AI agents*).
- **Engenharia de contexto:** curadoria do conjunto ótimo de tokens durante a
  inferência — não apenas "escrever o prompt", mas decidir o que entra, o que é
  comprimido, o que é isolado e o que é descartado (ANTHROPIC; LANGCHAIN,
  *Context Engineering* — taxonomia escrever/selecionar/comprimir/isolar).
- **Divulgação progressiva (*progressive disclosure*):** princípio de design que faz
  o agente carregar metadados baratos (nome + descrição de uma skill) e só então,
  por decisão própria, ler o corpo completo das instruções (ANTHROPIC, *Equipping
  agents for the real world with Agent Skills*).
- **Skill:** diretório com `SKILL.md` (frontmatter YAML + corpo Markdown) que
  empacota um procedimento reutilizável; é a unidade de divulgação progressiva
  (ANTHROPIC, *Agent Skills — overview*).
- **Rule:** instrução persistente carregada automaticamente na sessão (ex.:
  `.cursor/rules/*.mdc`), com escopo de projeto ou de usuário (CURSOR, *Rules*).
- **`AGENTS.md`:** padrão aberto de arquivo de instruções na raiz do repositório —
  "um README para agentes" — portável entre harnesses (AGENTS.MD, *agentsmd/agents.md*).
- **Configuração que nunca te contam:** chaves de configuração cujo efeito é silencioso
  no turno (ex.: ordem de precedência de `settings.json`, timeouts de hook, limites de
  contexto, orçamento de saída). Precisam de auditoria explícita porque não geram erro
  visível quando mal configuradas (ANTHROPIC, *All settings — settings-reference*).
- **Hook:** comando de shell (ou hook baseado em prompt/agente) disparado em eventos do
  ciclo de vida do agente — o mecanismo que insere **determinismo** na esteira
  probabilística (ANTHROPIC, *Hooks guide* / *Hooks reference*).
- **Gate:** verificação determinística de contrato (script) que reprova o artefato antes
  da fase seguinte. Complementa o hook: o hook intercepta a ação, o gate valida o produto.
- **Subagente:** instância isolada, com janela de contexto própria, prompt de sistema
  próprio e lista de ferramentas própria; devolve ao pai apenas o resumo — modelo de
  "contexto isolado, retorno resumido" (ANTHROPIC, *Subagents in the SDK*).
- **Turno agêntico:** uma iteração completa percepção → raciocínio → chamada de
  ferramenta → observação. É a unidade de custo real de um agente (cada turno reenvia
  o prefixo de contexto, salvo cache).
- **Cache de prompt (*prompt caching*):** reaproveitamento do prefixo já processado;
  leitura de cache custa uma fração do token de entrada comum, escrita custa mais
  (GOOGLE CLOUD, *Prompt caching*; ANTHROPIC, *Prompt caching*).
- **Cache hit:** quando o prefixo solicitado já existe em cache. O determinismo da
  ordem das partes do prompt é o que decide o hit — daí "configurações que nunca te contam"
  afetarem diretamente a conta.
- **Orçamento de contexto:** o teto prático de tokens úteis antes de degradação de
  atenção; gerenciado por compactação, memória externa e *tool clearing*
  (ANTHROPIC, *Context engineering: memory, compaction, and tool clearing*).
- **Worktree:** diretório de trabalho adicional ligado ao mesmo repositório git,
  permitindo N branches/agentes em paralelo sem colisão de arquivos
  (GIT, *git-worktree*; ANTHROPIC, *Run parallel sessions with worktrees*).
- **Orca ADE:** *Agent Development Environment* — cada tarefa recebe seu próprio
  worktree, terminal de agente e browser; o orquestrador coordena uma frota de agentes
  (ORCA, *What is Orca?*).
- **MCP (*Model Context Protocol*):** protocolo aberto que expõe *resources*, *prompts*
  e *tools* de um servidor para o modelo (MODEL CONTEXT PROTOCOL, *Specification*).
- **Roteamento de LLM:** escolher dinamicamente entre modelo forte e fraco por consulta,
  otimizando custo/qualidade (ONG et al., *RouteLLM*).

## Artigos Científicos e Papers

- WANG, Lei et al. *A survey on large language model based autonomous agents*. In: Frontiers of Computer Science, 2024. (A)
- XI, Zhiheng et al. *The Rise and Potential of Large Language Model Based Agents: A Survey*. arXiv:2309.07864, 2023. (A)
- XU, Weikai et al. *LLM-Based Agents for Tool Learning: A Survey*. In: Data Science and Engineering, 2025. (A)
- MOHAMMADI, Mahmoud et al. *Evaluation and Benchmarking of LLM Agents: A Survey*. 2025. (A)
- SAPKOTA, Ranjan; ROUMELIOTIS, Konstantinos I.; KARKEE, Manoj. *AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications and Challenges*. In: Information Fusion, 2025. (A)
- KWON, Woosuk et al. *Efficient Memory Management for Large Language Model Serving with PagedAttention*. In: SOSP '23 / arXiv:2309.06180, 2023. (A)
- ONG, Isaac et al. *RouteLLM: Learning to Route LLMs with Preference Data*. arXiv:2406.18665 / ICLR 2025. (A)
- ANONYMOUS/ARXIV. *Agent Skills for Large Language Models: Architecture, Acquisition and Progressive Disclosure*. arXiv:2602.12430, 2026. (A)
- GRESHAKE, Kai et al. *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. 2023. (A)
- OPENAI et al. *GPT-4 Technical Report*. arXiv:2303.08774, 2023. (A)
- Os 20 artigos adicionais minerados nas buscas temáticas (ferramentas, contexto,
  cache, orquestração, engenharia de software autônoma e custos) estão consolidados
  nos dossiês `dossie_min_*.md` e na seção "Fontes brutas" abaixo. (A)

## Estado da arte / ferramentas de referência

- **Claude Code (Anthropic):** harness de referência para hooks, subagentes, skills,
  worktrees, janela de contexto e precedência de `settings.json`
  (ANTHROPIC, *Hooks guide*, *Subagents in the SDK*, *All settings*, *Run parallel
  sessions with worktrees*, *Explore the context window*).
- **Agent Skills:** padrão aberto de empacotamento de procedimentos com divulgação
  progressiva (ANTHROPIC, *Agent Skills — overview*; ARXIV:2602.12430).
- **Cursor Rules (`.cursor/rules/*.mdc`):** regras de projeto com escopo por arquivo
  e por framework (CURSOR, *Rules*).
- **`AGENTS.md`:** padrão de instruções portável, adotado por múltiplos harnesses
  (AGENTS.MD, *agentsmd/agents.md*; INFOQ).
- **MCP:** protocolo de integração com servidores de ferramentas, recursos e prompts
  (MODEL CONTEXT PROTOCOL, *Specification*, *Tools*, *Resources*, *Prompts*).
- **git worktree:** isolamento de sessões paralelas por diretório de trabalho
  (GIT, *git-worktree*).
- **Orca ADE:** ambiente de desenvolvimento de agentes com frota em worktrees
  paralelos, coordenador e gate de revisão (ORCA; STABLY AI, `stablyai/orca`).
- **vLLM / PagedAttention:** economia de memória do KV cache — a base de infraestrutura
  que torna o cache de prefixo economicamente viável em escala (KWON et al.; VLLM).

## Casos de uso corporativos

- **Frota paralela em worktrees:** executar N agentes (Claude Code, Codex, OpenCode)
  simultaneamente, cada um isolado em seu worktree, com um agente coordenador e gate
  determinístico de conclusão (ORCA, *What is Orca?*; ANTHROPIC, *Run parallel sessions
  with worktrees*).
- **Redução de custo por cache de prefixo:** reaproveitamento do prefixo estável
  (prompt de sistema + regras + ferramentas) entre turnos da mesma sessão; leitura de
  cache custa uma fração do token de entrada (GOOGLE CLOUD, *Prompt caching*;
  ANTHROPIC, *Prompt caching*).
- **Contexto longo sob controle:** memória externa + compactação + *tool clearing*
  para agentes de longa duração, decidindo quando cada estratégia compensa
  (ANTHROPIC, *Context engineering: memory, compaction, and tool clearing*).
- **Instruções portáveis entre harnesses:** um único `AGENTS.md` servindo Claude Code,
  Cursor, Codex e afins, com hardlinks/geração por script para os formatos específicos
  (AGENTS.MD; TESSL; AIHERO).
- **Casos práticos do autor (Fábrica Agêntica de Publicações):** esteira de 16 capítulos
  com gates de conteúdo encadeados, economia severa de tokens (caveman/headroom/lean-ctx),
  subagentes comprimidos e hooks git que bloqueiam commit com suíte vermelha — caso de
  campo descrito na obra como estudo de caso, não como fonte externa.

## Limitações e controvérsias

- **Determinismo parcial:** nenhuma configuração torna o LLM determinístico; o ganho
  vem de mover verificações para scripts e hooks, mantendo o modelo na camada criativa.
- **Isolamento de subagente corta contexto:** subagentes perdem o histórico da conversa
  pai; para tarefas de escrita longa a coordenação pode custar mais do que economiza.
- **Cache é frágil a mudanças de prefixo:** qualquer alteração no início do prompt
  invalida o cache e transforma "hit" em "write" (mais caro que o normal).
- **Injeção indireta de prompt:** ferramentas que leem conteúdo externo ampliam a
  superfície de ataque (GRESHAKE et al., 2023).
- **Métricas infladas de adoção:** relatórios de produtividade com IA variam muito por
  metodologia; a obra evita números sem fonte primária auditável.
- **Divulgação progressiva ≠ graça:** skills mal descritas não são carregadas; o
  ganho de contexto depende da qualidade do texto de gatilho.

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- ANTHROPIC. *Effective context engineering for AI agents*. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Equipping agents for the real world with Agent Skills*. Disponível em: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Agent Skills — Overview*. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Automate actions with hooks — Claude Code Docs*. Disponível em: https://code.claude.com/docs/en/hooks-guide. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Hooks reference — Claude Code Docs*. Disponível em: https://code.claude.com/docs/en/hooks. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Intercept and control agent behavior with hooks — Agent SDK*. Disponível em: https://code.claude.com/docs/en/agent-sdk/hooks. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *All settings — Claude Code Docs*. Disponível em: https://code.claude.com/docs/en/settings-reference. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Subagents in the SDK — Claude Code Docs*. Disponível em: https://code.claude.com/docs/en/agent-sdk/subagents. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Explore the context window — Claude Code Docs*. Disponível em: https://code.claude.com/docs/en/context-window. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Run parallel sessions with worktrees — Claude Code Docs*. Disponível em: https://code.claude.com/docs/en/worktrees. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Context engineering: memory, compaction, and tool clearing*. Disponível em: https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools. Acesso em: 12 set. 2026. (B)
- GOOGLE CLOUD. *Prompt caching — Claude partner models*. Disponível em: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/prompt-caching. Acesso em: 12 set. 2026. (B)
- MODEL CONTEXT PROTOCOL. *Specification (2025-06-18)*. Disponível em: https://modelcontextprotocol.io/specification/2025-06-18. Acesso em: 12 set. 2026. (B)
- MODEL CONTEXT PROTOCOL. *Server Features — Tools*. Disponível em: https://modelcontextprotocol.io/specification/2026-07-28/server/tools. Acesso em: 12 set. 2026. (B)
- MODEL CONTEXT PROTOCOL. *Server Features — Resources*. Disponível em: https://modelcontextprotocol.io/specification/2026-07-28/server/resources. Acesso em: 12 set. 2026. (B)
- MODEL CONTEXT PROTOCOL. *Server Features — Prompts*. Disponível em: https://modelcontextprotocol.io/specification/2026-07-28/server/prompts. Acesso em: 12 set. 2026. (B)
- AGENTS.MD. *agentsmd/agents.md — Repositório oficial do padrão*. Disponível em: https://github.com/agentsmd/agents.md. Acesso em: 12 set. 2026. (B)
- CURSOR. *Rules — Cursor Docs*. Disponível em: https://cursor.com/docs/rules. Acesso em: 12 set. 2026. (B)
- GIT. *git-worktree — Referência oficial*. Disponível em: https://git-scm.com/docs/git-worktree. Acesso em: 12 set. 2026. (B)
- ORCA. *What is Orca? — Orca Docs*. Disponível em: https://www.onorca.dev/docs. Acesso em: 12 set. 2026. (B)
- ORCA. *Orca — The agent development environment*. Disponível em: https://www.onorca.dev/. Acesso em: 12 set. 2026. (B)
- STABLY AI. *stablyai/orca — GitHub*. Disponível em: https://github.com/stablyai/orca. Acesso em: 12 set. 2026. (B)
- VLLM. *Easy, Fast, and Cheap LLM Serving with PagedAttention*. Disponível em: https://vllm.ai/blog/2023-06-20-vllm. Acesso em: 12 set. 2026. (B)
- KWON, Woosuk et al. *Efficient Memory Management for Large Language Model Serving with PagedAttention*. Disponível em: https://arxiv.org/abs/2309.06180. Acesso em: 12 set. 2026. (A)
- ONG, Isaac et al. *RouteLLM: Learning to Route LLMs with Preference Data*. Disponível em: https://arxiv.org/abs/2406.18665. Acesso em: 12 set. 2026. (A)
- LANGCHAIN. *Context Engineering*. Disponível em: https://www.langchain.com/blog/context-engineering-for-agents. Acesso em: 12 set. 2026. (B)
- ARXIV. *Agent Skills for Large Language Models: Architecture, Acquisition and Progressive Disclosure*. Disponível em: https://arxiv.org/html/2602.12430v3. Acesso em: 12 set. 2026. (A)
- INFOQ. *AGENTS.md Emerges as Open Standard for AI Coding Agents*. Disponível em: https://www.infoq.com/news/2025/08/agents-md/. Acesso em: 12 set. 2026. (C)
- AIHERO. *A Complete Guide To AGENTS.md*. Disponível em: https://www.aihero.dev/a-complete-guide-to-agents-md. Acesso em: 12 set. 2026. (C)
- TESSL. *Agents.md: an open standard for AI coding agents*. Disponível em: https://tessl.io/blog/the-rise-of-agents-md-an-open-standard-and-single-source-of-truth-for-ai-coding-agents. Acesso em: 12 set. 2026. (C)
- SOURCEGRAPH. *Context Engineering: A Practical Guide for AI Agents*. Disponível em: https://sourcegraph.com/blog/context-engineering. Acesso em: 12 set. 2026. (C)
- KONISHI, Hidekazu. *Anthropic Claude API Prompt Caching and Token Efficiency*. Disponível em: https://hidekazu-konishi.com/entry/anthropic_claude_api_prompt_caching_and_token_efficiency.html. Acesso em: 12 set. 2026. (C)
- RED HAT DEVELOPERS. *How PagedAttention resolves memory waste of LLM systems*. Disponível em: https://developers.redhat.com/articles/2025/07/24/how-pagedattention-resolves-memory-waste-llm-systems. Acesso em: 12 set. 2026. (C)
