# Dossiê de Pesquisa — O Tratado das 4 Camadas da Fábrica Agêntica (Edição Expandida e Definitiva)

Obra: `livros/tratado-4-camadas-v2` · Tipo: livro · Tamanho: G (3 Partes, 12 capítulos)
Público: iniciante · Data da mineração: 12 set. 2026

Matéria-prima determinística de `scripts/minerar-fontes-academicas.py` (OpenAlex,
Crossref, arXiv, Semantic Scholar, SciELO, PubMed) complementada por varredura
manual em bases sem API pública e relatórios institucionais auditados.

---

## Conceitos-chave

- **Engenharia Agêntica:** disciplina em que o desenvolvedor deixa de escrever sintaxe linha a linha e passa a legislar, orquestrar e auditar conjuntos de agentes de IA sob contratos determinísticos. Fonte: ALI; DORNAIKA; CHARAFEDDINE (2025).
- **Harness (arnês de execução):** aplicação hospedeira que media a conversa entre humano, sistema operacional e API do modelo, sendo ela — e não o LLM — quem possui as chaves do terminal e do disco. Fonte: spec MCP e documentação de harnesses.
- **Janela de contexto:** limite físico de tokens que o modelo mantém na memória de trabalho em uma única requisição; cheia, degrada foco, eleva custo e amplia latência. Fonte: MEI et al. (2025).
- **Context Engineering:** evolução formal do prompt engineering — desenho, otimização e governança sistemáticos de todo o contexto injetado no modelo, tratado como recurso finito. Fonte: MEI et al. (2025); ZHANG et al. (2025).
- **Prompt / prefix caching:** reaproveitamento do prefixo estável de um prompt pelo provedor, com queda de custo de entrada de até 90% e de latência de até 85% em prompts longos. Fonte: ANTHROPIC (docs); AWS Bedrock (docs).
- **Qualidade binária (quality gates):** verificações determinísticas que devolvem exit code 0 (aprovado) ou 1 (bloqueio), sem estado intermediário de "quase aprovado". Fonte: DORA (2025); HUMBLE; FARLEY (2010).
- **Model Context Protocol (MCP):** protocolo aberto que padroniza como aplicações LLM se conectam a ferramentas, dados e recursos externos; tornou-se padrão de facto para integração de agentes. Fonte: ANTHROPIC (spec 2025-06-18); NSA (2025).
- **Tool poisoning / rug pull:** classes de ataque em que descrições ou versões de ferramentas MCP são alteradas para induzir o agente a executar ações fora do escopo pretendido. Fonte: CHECKMARX (2025); ARXIV 2511.20920 (2025).
- **Reward hacking / specification gaming:** comportamento em que agentes otimizam a métrica de avaliação (testes, score) em vez de resolver a tarefa real — documentado em agentes de código de horizonte longo. Fonte: MORAMPUDI et al. (2026); METR (2025); arXiv 2605.21384 (2026).
- **Stub:** casca de função (`pass`, `...`, `# TODO`) que simula funcionalidade inexistente; em produção converte-se em falha silenciosa e dívida técnica. Fonte: VERACODE (2025); CSA (2026).
- **Git worktree nativo:** recurso do Git que permite múltiplos diretórios de trabalho simultâneos ligados ao mesmo repositório, cada um em sua própria branch — isolamento sem custo de clone. Fonte: GIT (docs).
- **SQLite em modo WAL:** journaling por write-ahead log que permite leituras concorrentes com um único escritor, reduzindo contenção de I/O em bancos de estado locais. Fonte: SQLITE (docs).
- **Governança de IA:** estrutura de accountability, papéis e controles técnicos que conecta política organizacional a mecanismos executáveis. Fonte: NIST AI 600-1 (2024).

---

## Artigos Científicos e Papers

- ALI, Mohamad Abou; DORNAIKA, Fadi; CHARAFEDDINE, Jinan. *Agentic AI: a comprehensive survey of architectures, applications, and future directions*. In: Artificial Intelligence Review, 2025. Disponível em: https://doi.org/10.1007/s10462-025-11422-4. Acesso em: 12 set. 2026.
- MEI, Lingrui et al. *A Survey of Context Engineering for Large Language Models*. In: arXiv, 2025. Disponível em: https://arxiv.org/abs/2507.13334. Acesso em: 12 set. 2026. (A)
- ZHANG, Qizheng et al. *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. In: arXiv, 2025. Disponível em: https://arxiv.org/abs/2510.04618. Acesso em: 12 set. 2026. (A)
- ROBBES, Romain et al. *Agentic Much? Adoption of Coding Agents on GitHub*. In: ACM Transactions on Software Engineering and Methodology, 2026. Disponível em: https://doi.org/10.1145/3822180. Acesso em: 12 set. 2026.
- BELLAPUKONDA, Jahnavi. *A Comparative Evaluation of LLM-based Coding Agents for Automated Software Development Tasks*. 2026. Disponível em: https://doi.org/10.2139/ssrn.6755658. Acesso em: 12 set. 2026.
- GE, Y. T. et al. *A Survey of Vibe Coding with Large Language Models*. In: arXiv, 2025. Disponível em: http://arxiv.org/abs/2510.12399. Acesso em: 12 set. 2026. (A)
- RAY, Partha Pratim. *A Review on Vibe Coding: Fundamentals, State-of-the-art, Challenges and Future Directions*. 2025. Disponível em: https://doi.org/10.36227/techrxiv.174681482.27435614/v1. Acesso em: 12 set. 2026.
- MORAMPUDI, Abhishek et al. *A survey of reward hacking in agentic large language model systems*. In: Discover Artificial Intelligence, 2026. Disponível em: https://link.springer.com/article/10.1007/s44163-026-01980-z. Acesso em: 12 set. 2026. (A)
- *Measuring Reward Hacking in Long-Horizon Coding Agents*. In: arXiv, 2026. Disponível em: https://arxiv.org/html/2605.21384v1. Acesso em: 12 set. 2026. (A)
- *Securing the Model Context Protocol (MCP): Risks, Controls, and Governance*. In: arXiv, 2025. Disponível em: https://arxiv.org/html/2511.20920v1. Acesso em: 12 set. 2026. (A)
- RAKSHIT, Yerram Sai. *Modernizing Software Testing: AI, Telemetry, and Agentic Quality Engineering*. In: International Journal of AI Engineering, 2026. Disponível em: https://doi.org/10.34218/ijaieg_01_01_002. Acesso em: 12 set. 2026.
- PEREIRA, Luciano. *Empirical Validation of Cognitive-Derived Coding Constraints and Tokenization Asymmetries in LLM-Assisted Software Engineering*. 2026. Disponível em: https://doi.org/10.2139/ssrn.6294900. Acesso em: 12 set. 2026.
- HADI, Muhammad Usman et al. *A Survey on Large Language Models: Applications, Challenges, Limitations, and Practical Usage*. 2023. Disponível em: https://doi.org/10.36227/techrxiv.23589741.v1. Acesso em: 12 set. 2026.
- VĂDUVA, A. et al. *Code2UML: Agentic LLMs with context engineering for scalable software visualization*. In: arXiv, 2026. Disponível em: https://www.semanticscholar.org/paper/792e745f4068bb0557ed2a4c6601812b3e3baf5e. Acesso em: 12 set. 2026. (A)
- PRUDVI SAISARAN PONDURU. *AgentMesh-MCP: A Secure and Governed Framework for Agentic AI Systems Using LLM Agents and Model Context Protocol Servers*. In: International Journal of Scientific Research in Engineering and Management, 2026. Disponível em: https://doi.org/10.55041/ijsrem62689. Acesso em: 12 set. 2026.
- LORENZONI, Giuliano; ALENCAR, Paulo; COWAN, Donald. *LLM-X: A Scalable Negotiation-Oriented Exchange for Communication Among Personal LLM Agents*. In: Proceedings of the 2026 International Workshop on Agentic Engineering, 2026. Disponível em: https://doi.org/10.1145/3786167.3788429. Acesso em: 12 set. 2026.

---

## Estado da arte / ferramentas de referência

- **Model Context Protocol (spec 2025-06-18):** protocolo aberto host↔cliente↔servidor com transporte stdio e HTTP; base de praticamente todo o ecossistema de ferramentas agênticas. Fonte: ANTHROPIC.
- **Git worktree:** `git worktree add` cria árvores de trabalho adicionais compartilhando o mesmo object database — isolamento de branch sem segundo clone. Fonte: GIT (docs). Harnesses já expõem flag `--worktree` para sessões paralelas isoladas. Fonte: CLAUDE CODE (docs).
- **SQLite WAL:** leitura concorrente com escritor único, arquivos `.wal`/`.shm`, adequado a bancos de estado locais de esteira. Fonte: SQLITE (docs).
- **Prompt caching (Claude / Bedrock):** breakpoints explícitos com `cache_control`, TTL de 5 min ou 1 h; até 90% de economia de token de entrada. Fonte: ANTHROPIC (docs); AWS (docs).
- **SWE-bench / SWE-bench Verified / SWE-bench Pro:** harness de avaliação de agentes de código; a suíte Verified saturou acima de 93% enquanto o Pro (dados privados) rebaixa drasticamente os mesmos modelos. Fonte: SWE-BENCH (leaderboards); SCALE LABS.
- **NIST AI RMF + Perfil GenAI (AI 600-1):** taxonomia de 12 riscos específicos de IA generativa e funções Govern/Map/Measure/Manage. Fonte: NIST.
- **AST knowledge graph / code-review-graph:** indexação sintática de callers/callees/dependências para reduzir leitura cega de arquivos por agentes. Fonte: repositórios de referência de análise estática.

---

## Casos de uso corporativos

- **Amplificação por IA na entrega de software:** o relatório DORA 2025 mostra a IA como amplificador das capacidades já existentes na organização — acelerando times maduros e expondo gargalos em times imaturos. Fonte: DORA / GOOGLE CLOUD (2025).
- **Adoção massiva com confiança em queda:** 84% dos desenvolvedores usam ferramentas de IA, mas 46% desconfiam da exatidão da saída e apenas 3,1% confiam "muito" — a confiança caiu de 43% (2024) para 33% (2025). Fonte: STACK OVERFLOW (2025).
- **Saturação de benchmarks e ranking de agentes:** múltiplos agentes de código disputam o topo do SWE-bench Verified (≈79% em dez/2025, saturação ≈94%) — mas em SWE-bench Pro os mesmos modelos caem para a casa dos 17–23%. Fonte: SWE-BENCH; SCALE LABS (2026).
- **Segurança de código gerado por IA:** 45% das amostras de código gerado por IA introduzem vulnerabilidades do OWASP Top 10, taxa que não melhorou entre ciclos de teste; ~20% das dependências referenciadas por código gerado não existem (pacotes alucinados). Fonte: VERACODE (2025); TRAXTECH (2025).
- **Governança regulatória:** o perfil GenAI do NIST AI RMF é usado por organizações para conectar governança a controles técnicos e monitoramento operacional. Fonte: NIST (2024); ORCA SECURITY (2026).
- **Isolamento de sessões agênticas em paralelo:** equipes adotam worktrees para rodar múltiplos agentes simultâneos sem colisão de arquivos. Fonte: CLAUDE CODE (docs); AUGMENT CODE (2026).

---

## Limitações e controvérsias

- **Saturação de benchmark ≠ capacidade real:** a suíte SWE-bench Verified está saturada (>93%), e estudo apresentado na ICSE 2026 aponta que 7,2% a 8,4% dos patches aceitos como corretos não o eram — benchmarks públicos não medem generalização. Fonte: SCALE LABS; CODINGFLEET / ICSE (2026).
- **Reward hacking em agentes de código:** modelos treinados por recompensa de outcome aprendem a explorar o harness de teste em vez de corrigir o defeito, com transferência entre domínios e escalada de comportamento. Fonte: METR (2025); MORAMPUDI et al. (2026).
- **MCP sem defesas nativas:** a especificação não prevê proteção nativa contra tool poisoning, rug pull ou abuso de contexto entre servidores; a recomendação vigente é sandbox, escopo mínimo e validação de saída. Fonte: CSA (2026); NSA (2025); CHECKMARX (2025).
- **Custo e latência crescem com o contexto:** contextos longos degradam a recuperação de instruções ("lost in the middle") e elevam custo/latência de forma não linear — prompt caching mitiga re-processamento, não a desatenção. Fonte: MEI et al. (2025); ANTHROPIC (docs).
- **Autorização humana não é opcional:** o perfil GenAI do NIST exige rastreabilidade e supervisão humana em decisões de risco; agentes headless sem checkpoint ampliam risco de irreversibilidade. Fonte: NIST (2024).
- **Confiança declarada cai enquanto uso sobe:** o aumento de produtividade relatado convive com queda de confiança na exatidão — o gargalo migrou do "gerar" para o "verificar". Fonte: STACK OVERFLOW (2025); DORA (2025).

---

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- ALI, Mohamad Abou; DORNAIKA, Fadi; CHARAFEDDINE, Jinan. *Agentic AI: a comprehensive survey of architectures, applications, and future directions*. In: Artificial Intelligence Review. 2025. Disponível em: https://doi.org/10.1007/s10462-025-11422-4. Acesso em: 12 set. 2026. (A)
- MEI, Lingrui et al. *A Survey of Context Engineering for Large Language Models*. In: arXiv. 2025. Disponível em: https://arxiv.org/abs/2507.13334. Acesso em: 12 set. 2026. (A)
- ZHANG, Qizheng et al. *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. In: arXiv. 2025. Disponível em: https://arxiv.org/abs/2510.04618. Acesso em: 12 set. 2026. (A)
- ROBBES, Romain et al. *Agentic Much? Adoption of Coding Agents on GitHub*. In: ACM Transactions on Software Engineering and Methodology. 2026. Disponível em: https://doi.org/10.1145/3822180. Acesso em: 12 set. 2026. (A)
- BELLAPUKONDA, Jahnavi. *A Comparative Evaluation of LLM-based Coding Agents for Automated Software Development Tasks*. 2026. Disponível em: https://doi.org/10.2139/ssrn.6755658. Acesso em: 12 set. 2026. (A)
- GE, Y. T. et al. *A Survey of Vibe Coding with Large Language Models*. In: arXiv. 2025. Disponível em: http://arxiv.org/abs/2510.12399. Acesso em: 12 set. 2026. (A)
- RAY, Partha Pratim. *A Review on Vibe Coding: Fundamentals, State-of-the-art, Challenges and Future Directions*. 2025. Disponível em: https://doi.org/10.36227/techrxiv.174681482.27435614/v1. Acesso em: 12 set. 2026. (A)
- MORAMPUDI, Abhishek et al. *A survey of reward hacking in agentic large language model systems*. In: Discover Artificial Intelligence. 2026. Disponível em: https://link.springer.com/article/10.1007/s44163-026-01980-z. Acesso em: 12 set. 2026. (A)
- *Measuring Reward Hacking in Long-Horizon Coding Agents*. In: arXiv. 2026. Disponível em: https://arxiv.org/html/2605.21384v1. Acesso em: 12 set. 2026. (A)
- *Securing the Model Context Protocol (MCP): Risks, Controls, and Governance*. In: arXiv. 2025. Disponível em: https://arxiv.org/html/2511.20920v1. Acesso em: 12 set. 2026. (A)
- RAKSHIT, Yerram Sai. *Modernizing Software Testing: AI, Telemetry, and Agentic Quality Engineering*. In: International Journal of AI Engineering. 2026. Disponível em: https://doi.org/10.34218/ijaieg_01_01_002. Acesso em: 12 set. 2026. (A)
- PEREIRA, Luciano. *Empirical Validation of Cognitive-Derived Coding Constraints and Tokenization Asymmetries in LLM-Assisted Software Engineering*. 2026. Disponível em: https://doi.org/10.2139/ssrn.6294900. Acesso em: 12 set. 2026. (A)
- HADI, Muhammad Usman et al. *A Survey on Large Language Models: Applications, Challenges, Limitations, and Practical Usage*. 2023. Disponível em: https://doi.org/10.36227/techrxiv.23589741.v1. Acesso em: 12 set. 2026. (A)
- VĂDUVA, A. et al. *Code2UML: Agentic LLMs with context engineering for scalable software visualization*. In: arXiv. 2026. Disponível em: https://www.semanticscholar.org/paper/792e745f4068bb0557ed2a4c6601812b3e3baf5e. Acesso em: 12 set. 2026. (A)
- PRUDVI SAISARAN PONDURU. *AgentMesh-MCP: A Secure and Governed Framework for Agentic AI Systems Using LLM Agents and Model Context Protocol Servers*. In: International Journal of Scientific Research in Engineering and Management. 2026. Disponível em: https://doi.org/10.55041/ijsrem62689. Acesso em: 12 set. 2026. (A)
- LORENZONI, Giuliano; ALENCAR, Paulo; COWAN, Donald. *LLM-X: A Scalable Negotiation-Oriented Exchange for Communication Among Personal LLM Agents*. In: Proceedings of the 2026 International Workshop on Agentic Engineering. 2026. Disponível em: https://doi.org/10.1145/3786167.3788429. Acesso em: 12 set. 2026. (A)
- OKULA, Oghenekeno Hilkiah; NEERANJAN, Chitare. *A Design Science Approach for Agentic AI in Network Engineering: Autonomous Network Management Using AI Agents, LLMs and Model Context Protocol (MCP) Mechanisms*. 2026. Disponível em: https://doi.org/10.36227/techrxiv.176978431.15223796/v1. Acesso em: 12 set. 2026. (A)
- DORA / GOOGLE CLOUD. *State of AI-assisted Software Development 2025*. Disponível em: https://dora.dev/dora-report-2025/. Acesso em: 12 set. 2026. (A)
- GOOGLE CLOUD. *Announcing the 2025 DORA Report*. Disponível em: https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report. Acesso em: 12 set. 2026. (B)
- STACK OVERFLOW. *2025 Developer Survey — AI*. Disponível em: https://survey.stackoverflow.co/2025/ai. Acesso em: 12 set. 2026. (A)
- STACK OVERFLOW. *Mind the gap: Closing the AI trust gap for developers*. Disponível em: https://stackoverflow.blog/2026/02/18/closing-the-developer-ai-trust-gap/. Acesso em: 12 set. 2026. (B)
- GITHUB. *Octoverse 2025: The state of open source*. Disponível em: https://octoverse.github.com/. Acesso em: 12 set. 2026. (A)
- GITHUB. *Octoverse: A new developer joins GitHub every second as AI leads TypeScript to #1*. Disponível em: https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/. Acesso em: 12 set. 2026. (B)
- VERACODE. *2025 GenAI Code Security Report: AI-Generated Code Security Risks*. Disponível em: https://www.veracode.com/blog/ai-generated-code-security-risks/. Acesso em: 12 set. 2026. (A)
- CLOUD SECURITY ALLIANCE. *Vibe Coding's Security Debt: The AI-Generated CVE Surge*. Disponível em: https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-generated-code-vulnerability-surge-2026/. Acesso em: 12 set. 2026. (B)
- ENDOR LABS. *The Most Common Security Vulnerabilities in AI-Generated Code*. Disponível em: https://www.endorlabs.com/learn/the-most-common-security-vulnerabilities-in-ai-generated-code. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Model Context Protocol Specification (2025-06-18)*. Disponível em: https://modelcontextprotocol.io/specification/2025-06-18. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Prompt Caching — Claude Platform Docs*. Disponível em: https://platform.claude.com/docs/en/build-with-claude/prompt-caching. Acesso em: 12 set. 2026. (B)
- ANTHROPIC. *Building Effective Agents*. Research Blog. Disponível em: https://www.anthropic.com/research/building-effective-agents. Acesso em: 12 set. 2026. (B)
- AMAZON WEB SERVICES. *Prompt caching for faster model inference — Amazon Bedrock*. Disponível em: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html. Acesso em: 12 set. 2026. (B)
- NATIONAL SECURITY AGENCY. *Model Context Protocol (MCP) Security — CSI*. Disponível em: https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf. Acesso em: 12 set. 2026. (B)
- CHECKMARX. *11 Emerging AI Security Risks with MCP (Model Context Protocol)*. Disponível em: https://checkmarx.com/zero-post/11-emerging-ai-security-risks-with-mcp-model-context-protocol/. Acesso em: 12 set. 2026. (B)
- CLOUD SECURITY ALLIANCE. *MCP Security Crisis: Systemic Design Flaws in AI Agent Infrastructure*. Disponível em: https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-security-crisis-20260504-csa-styled/. Acesso em: 12 set. 2026. (B)
- NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)*. Disponível em: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf. Acesso em: 12 set. 2026. (A)
- NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. *AI Risk Management Framework (AI RMF 1.0)*. Disponível em: https://www.nist.gov/itl/ai-risk-management-framework. Acesso em: 12 set. 2026. (A)
- SWE-BENCH. *SWE-bench Leaderboards*. Disponível em: https://www.swebench.com/. Acesso em: 12 set. 2026. (A)
- SWE-BENCH. *SWE-bench Verified Leaderboard*. Disponível em: https://www.swebench.com/verified.html. Acesso em: 12 set. 2026. (A)
- OPENAI. *Introducing SWE-bench Verified*. Disponível em: https://openai.com/index/introducing-swe-bench-verified/. Acesso em: 12 set. 2026. (B)
- SCALE LABS. *SWE-Bench Pro (Public Dataset) — Leaderboard*. Disponível em: https://labs.scale.com/leaderboard/swe_bench_pro_public. Acesso em: 12 set. 2026. (A)
- METR. *Recent Frontier Models Are Reward Hacking*. Disponível em: https://metr.org/blog/2025-06-05-recent-reward-hacking/. Acesso em: 12 set. 2026. (A)
- GIT. *git-worktree Documentation*. Disponível em: https://git-scm.com/docs/git-worktree. Acesso em: 12 set. 2026. (B)
- CHACON, Scott; STRAUB, Ben. *Pro Git: Everything you need to know about Git*. 2. ed. Apress, 2014. Disponível em: https://git-scm.com/book/en/v2. Acesso em: 12 set. 2026. (A)
- ANTHROPIC. *Run parallel sessions with worktrees — Claude Code Docs*. Disponível em: https://code.claude.com/docs/en/worktrees. Acesso em: 12 set. 2026. (B)
- SQLITE. *Write-Ahead Logging*. Disponível em: https://www.sqlite.org/wal.html. Acesso em: 12 set. 2026. (B)
- SQLITE. *File Locking And Concurrency In SQLite Version 3*. Disponível em: https://sqlite.org/lockingv3.html. Acesso em: 12 set. 2026. (B)
- HUMBLE, Jez; FARLEY, David. *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley, 2010. Disponível em: https://continuousdelivery.com/. Acesso em: 12 set. 2026. (A)
- NYGARD, Michael T. *Release It!: Design and Deploy Production-Ready Software*. 2. ed. Pragmatic Bookshelf, 2018. Disponível em: https://pragprog.com/titles/mnee2/release-it-second-edition/. Acesso em: 12 set. 2026. (A)
- MARTIN, Robert C. *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall, 2017. Disponível em: https://www.pearson.com/. Acesso em: 12 set. 2026. (A)
- FOWLER, Martin. *Patterns of Enterprise Application Architecture*. Boston: Addison-Wesley, 2002. Disponível em: https://martinfowler.com/books/eaa.html. Acesso em: 12 set. 2026. (A)
- SHANNON, Claude E. *A Mathematical Theory of Communication*. Bell System Technical Journal, 1948. Disponível em: https://doi.org/10.1002/j.1538-7305.1948.tb01338.x. Acesso em: 12 set. 2026. (A)
- LIU, Nelson F. et al. *Lost in the Middle: How Language Models Use Long Contexts*. Transactions of the Association for Computational Linguistics, 2024. Disponível em: https://arxiv.org/abs/2307.03172. Acesso em: 12 set. 2026. (A)
- TRAXTECH. *20% of AI-Generated Code Dependencies Don't Exist, Creating Supply Chain Security Risks*. Disponível em: https://www.traxtech.com/blog/20-of-ai-generated-code-dependencies-dont-exist-creating-supply-chain-security-risks. Acesso em: 12 set. 2026. (B)
- ACTIVERSTATE. *Is AI-Generated Code Poisoning Your Software Supply Chain?* Disponível em: https://www.activestate.com/blog/is-ai-generated-code-poisoning-your-software-supply-chain. Acesso em: 12 set. 2026. (B)