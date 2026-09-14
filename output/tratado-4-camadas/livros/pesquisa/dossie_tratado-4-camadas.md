# Dossiê de Pesquisa — O Tratado das 4 Camadas da Fábrica Agêntica

## Conceitos-chave

- **IA / LLM (Large Language Model):** Cérebro probabilístico da máquina; digitador ultrarrápido que tenta adivinhar palavras com base em treinamento. (Livro-ref)
- **Token:** Unidade de cobrança (~4 letras). Toda entrada/saída de IA é cobrada em tokens. (Livro-ref)
- **Context Window:** Memória de curto prazo da IA — total de palavras "enxergáveis" em uma conversa. (Livro-ref)
- **KV-Cache (Prompt Caching):** Reutilização de cálculos quando prefixo do prompt é 100% idêntico → até 90% de desconto em input tokens. (Digital Applied 2026, Anthropic 2024)
- **ADE (Agentic Development Environment):** Ambiente onde agentes trabalham (Claude Code, Orca, Antigravity). (Livro-ref)
- **MCP (Model Context Protocol):** Padrão aberto para IA conversar com bancos de dados, navegadores e ferramentas externas de forma padronizada. (Anthropic 2024)
- **Pre-Commit Hook:** Segurança digital que inspeciona código antes do commit; bloqueia se encontrar defeito. (TruffleHog 2023, GitHub Community 2025)
- **Prompt Engineering:** Otimização de instruções para interação single-turn com LLM. (Atlan 2026, Augment 2026)
- **Context Engineering:** Disciplina de dar ao modelo a informação certa para a tarefa seguinte — cobre múltiplos turns. (Databricks 2026, Martin Fowler 2026)
- **Harness Engineering:** Engenharia do sistema completo ao redor do modelo — inclui prompt e context engineering, circuit breakers, sandbox e loops. (Martin Fowler 2026, Augment 2026, codecentric 2026)
- **Idempotência:** Propriedade donde f(f(x)) = f(x) — scripts podem rodar 1.000 vezes sem quebrar estado. (Medium 2026, Ganglani 2026)
- **Lost in the Middle:** Fenômeno onde LLMs ignoram informação no meio de contextos longos — attendance U-shaped. (Liu et al. 2023, 6019 citações)
- **SWE-bench:** Benchmark para avaliação de capacidade de software engineering de agentes IA. (SWE-bench.com)
- **Agent Script (Salesforce):** Controle determinístico para workflows de IA enterprise — comportamento previsível com flexibilidade de LLM. (Salesforce Engineering 2026)

## Artigos Científicos e Papers

- LIU, Nelson F.; LIN, Kevin et al. *Lost in the Middle: How Language Models Use Long Contexts*. In: arXiv, 2023. Disponível em: https://arxiv.org/abs/2307.03172. Acesso em: 25 ago. 2026. (A)
- HUZITA, Elisa Hatsue Moriya; OLIVEIRA, Hélio Marci de; LAINE, Jean Marcos. *Uma proposta de arquitetura de software baseada em agentes*. In: LA Referencia. 2000. Disponível em: http://www.periodicos.uem.br/ojs/index.php/ActaSciTechnol/article/view/3131. Acesso em: 25 ago. 2026. (A)
- BORDINI, Rafael H.; VIEIRA, Renata. *Linguagens de programação orientadas a agentes: uma introdução baseada em AgentSpeak(L)*. In: Lume (UFRGS). 2003. Disponível em: http://hdl.handle.net/10183/19885. Acesso em: 25 ago. 2026. (A)
- FERREIRA, Gustavo Guilherme de Souza et al. *Engenharias e inteligência artificial – arquiteturas cognitivas para projetos, tomada de decisão, gestão de riscos e soluções sistêmicas*. In: OBSERVATÓRIO DE LA ECONOMÍA LATINOAMERICANA. 2025. Disponível em: https://doi.org/10.55905/oelv23n7-097. Acesso em: 25 ago. 2026. (A)
- FERNANDES, Robson dos Santos. *INTELIGÊNCIA ARTIFICIAL APLICADA EM ENGENHARIA DE SOFTWARE*. In: Inovações Multidisciplinares na Engenharia. 2025. Disponível em: https://doi.org/10.63330/aurumpub.005-009. Acesso em: 25 ago. 2026. (A)
- ROBERTO SANTOS, CLÁUDIO. *IDENTIFICAÇÃO, DELEGAÇÃO AUTENTICADA E RESPONSABILIDADE: UMA PROPOSTA CONSTITUCIONAL PARA A GOVERNANÇA DE AGENTES AUTÔNOMOS DE INTELIGÊNCIA ARTIFICIAL NO BRASIL*. 2026. Disponível em: https://doi.org/10.17771/pucrio.acad.77233. Acesso em: 25 ago. 2026. (A)
- CRUZ, Mathews Henrique da. *Delegação de Trabalho de Governança de Segurança da Informação a Agentes Autônomos de Inteligência Artificial*. 2026. Disponível em: https://doi.org/10.37497/opsbrazil.42. Acesso em: 25 ago. 2026. (A)
- ARAÚJO, Fábia Melo de; RAYOL, Rayane Araújo Castelo Branco. *inteligência artificial e os seus impactos no mundo do trabalho*. In: Revista do TST. 2024. Disponível em: https://doi.org/10.70405/rtst.v90i3.90. Acesso em: 25 ago. 2026. (A)
- SILVA, ANDRÉ AZEVEDO DA. *AUTOMAÇÃO DE PROCESSOS LOGÍSTICOS COM AGENTES DE INTELIGÊNCIA ARTIFICIAL*. In: Anais ENEGEP. 2025. Disponível em: https://doi.org/10.14488/enegep2025_tn_st_425_2082_51150. Acesso em: 25 ago. 2026. (A)
- *Toward Agentic Software Engineering Beyond Code*. In: arXiv, 2026. Disponível em: https://arxiv.org/html/2510.19692v2. Acesso em: 25 ago. 2026. (A)
- *AI-Native Software Engineering and the Evolution of the Agentic Engineer*. In: arXiv, 2026. Disponível em: https://arxiv.org/html/2606.28791v1. Acesso em: 25 ago. 2026. (A)

## Estado da arte / ferramentas de referência

- **Anthropic — Building Effective Agents (2024):** Guia de referência para patterns de agentes: tool use, orchestration, agentic loops. Recomenda começar com APIs diretas antes de frameworks. (anthropic.com/engineering)
- **Martin Fowler — Harness Engineering for Coding Agents (2026):** Artigo definitivo que define harness engineering como a discipliplina de orquestrar o sistema ao redor do modelo. (martinfowler.com)
- **Model Context Protocol — Padrão aberto (2024-2026):** Protocolo universal para conexão de IA a sistemas externos. Suportado por Claude, Cursor, Copilot. (modelcontextprotocol.io)
- **Augment Code — Harness Engineering Guide (2026):** Guia prático com constraints, retry policies, e loop engineering para coding agents. (augmentcode.com)
- **Databricks — What is an AI Agent Harness (2026):** Define que prompt e context engineering vivem DENTRO do harness engineering. (databricks.com/blog)
- **SWE-bench Verified & Pro:** Benchmark padrão para capacidade de software engineering de agentes IA. Claude Code atinge 80.8%. (swebench.com)
- **Salesforce Agent Script (2026):** Controle determinístico para workflows de IA enterprise — comportamento previsível com flexibilidade. (engineering.salesforce.com)
- **Prompt Caching — Anthropic/OpenAI (2024-2026):** Reduz custos de input tokens em até 90% e latência em até 85% quando prefixos de prompt são reutilizados. (Digital Applied 2026, Introl 2026)
- **Kunal Ganglani — 4-Tier AI Agent Memory & State Management (2026):** Framework de 4 camadas de memória: in-memory, SQLite, vector store, external. (kunalganglani.com)
- **Codecentric — Loop, Harness, Context Engineering Explained (2026):** Diferenciação clara entre as três disciplinas com exemplos práticos. (codecentric.de)
- **Atlan — Prompt vs Context vs Harness Engineering (2026):** Comparativo completo: Prompt=molda instruções, Context=molda o que o modelo vê, Harness=molda o sistema completo. (atlan.com)
- **Keep Agentic AI Simple — Tim Deschryver (2026):** Workflow prático com AGENTS.md, Agent Skills e specs para melhorar velocidade e qualidade. (timdeschryver.dev)
- **MindStudio — Portable AI Agent Stack (2026):** Guia para evitar vendor lock-in usando agents.md, skill.md e MCP connections. (mindstudio.ai)
- **4-Tier AI Agent Memory (Ganglani 2026):** SQLite como camada intermediária de memória para agentes — determinístico, rápido, persistente.

## Casos de uso corporativos

- **Fábrica Universal / Arsenal Open Source:** Projeto real que produziu 49 compêndios técnicos cobrindo 680+ motores de código aberto, usando a arquitetura das 4 camadas para custo quase zero. (Livro-ref)
- **Claude Code — SWE-bench Verified (2026):** 80.8% de acurácia em bugs reais do GitHub, demonstrando que harness engineering bem feito entrega resultados industriais. (swebench.com)
- **Salesforce Agentforce (2026):** Implementação enterprise de controle determinístico para agentes de IA com Agent Script. (engineering.salesforce.com)
- **Portabilidade Multi-IDE (Reddit 2026):** Desenvolvedores usando AGENTS.md como camada de governança portátil entre Claude Code, Cursor e Copilot sem vendor lock-in.

## Limitações e controvérsias

- **Lost in the Middle persistente:** Apesar de janelas de contexto crescentes (128K-200K tokens), LLMs ainda perdem informação no meio do contexto — 6019 citações no paper original. (Liu et al. 2023)
- **Vendor lock-in em aceleração:** Cada IDE de IA exige arquivo diferente (CLAUDE.md, .cursorrules, .windsurfrules). Hardlinks/junctions resolvem parcialmente, mas não totalmente. (Reddit 2026, MindStudio 2026)
- **Custo explosivo sem harness:** Equipes sem harness engineering gastam centenas/milhares de dólares em APIs de LLMs por uso proliixo. (Reddit r/LLMDevs 2026)
- **Alucinação de validação:** IA afirma que corrigiu código perfeitamente, mas o sistema não inicia — fenômeno comum sem gates determinísticos. (Livro-ref)
- **Limitações de rate limit:** APIs de LLMs impõem HTTP 429 — sistemas sem fallback graceful param de funcionar. Semantic Scholar e SciELO bloquearam acesso durante mineração. (Dados da mineração)
- **Governança de agentes autônomos:** Debate em curso no Brasil sobre identificação, delegação e responsabilização de agentes IA — marco regulatorio incipiente. (Santos 2026, Cruz 2026)

## Fontes brutas

- LIU, Nelson F.; LIN, Kevin et al. *Lost in the Middle: How Language Models Use Long Contexts*. Disponível em: https://arxiv.org/abs/2307.03172. Acesso em: 25 ago. 2026. (A)
- HUZITA, Elisa Hatsue Moriya; OLIVEIRA, Hélio Marci de; LAINE, Jean Marcos. *Uma proposta de arquitetura de software baseada em agentes*. Disponível em: http://www.periodicos.uem.br/ojs/index.php/ActaSciTechnol/article/view/3131. Acesso em: 25 ago. 2026. (A)
- BORDINI, Rafael H.; VIEIRA, Renata. *Linguagens de programação orientadas a agentes: uma introdução baseada em AgentSpeak(L)*. Disponível em: http://hdl.handle.net/10183/19885. Acesso em: 25 ago. 2026. (A)
- FERREIRA, Gustavo Guilherme de Souza et al. *Engenharias e inteligência artificial – arquiteturas cognitivas para projetos, tomada de decisão, gestão de riscos e soluções sistêmicas*. Disponível em: https://doi.org/10.55905/oelv23n7-097. Acesso em: 25 ago. 2026. (A)
- FERNANDES, Robson dos Santos. *INTELIGÊNCIA ARTIFICIAL APLICADA EM ENGENHARIA DE SOFTWARE*. Disponível em: https://doi.org/10.63330/aurumpub.005-009. Acesso em: 25 ago. 2026. (A)
- ROBERTO SANTOS, CLÁUDIO. *IDENTIFICAÇÃO, DELEGAÇÃO AUTENTICADA E RESPONSABILIDADE: UMA PROPOSTA CONSTITUCIONAL PARA A GOVERNANÇA DE AGENTES AUTÔNOMOS DE INTELIGÊNCIA ARTIFICIAL NO BRASIL*. Disponível em: https://doi.org/10.17771/pucrio.acad.77233. Acesso em: 25 ago. 2026. (A)
- CRUZ, Mathews Henrique da. *Delegação de Trabalho de Governança de Segurança da Informação a Agentes Autônomos de Inteligência Artificial*. Disponível em: https://doi.org/10.37497/opsbrazil.42. Acesso em: 25 ago. 2026. (A)
- ARAÚJO, Fábia Melo de; RAYOL, Rayane Araújo Castelo Branco. *inteligência artificial e os seus impactos no mundo do trabalho*. Disponível em: https://doi.org/10.70405/rtst.v90i3.90. Acesso em: 25 ago. 2026. (A)
- SILVA, ANDRÉ AZEVEDO DA. *AUTOMAÇÃO DE PROCESSOS LOGÍSTICOS COM AGENTES DE INTELIGÊNCIA ARTIFICIAL*. Disponível em: https://doi.org/10.14488/enegep2025_tn_st_425_2082_51150. Acesso em: 25 ago. 2026. (A)
- COLDEBELLA, Henrique; ROSSINI, Flávio Luiz. *Desenvolvimento e Implementação do Método dos MQR-FE Acoplado a um Sistema de CAMR*. Disponível em: https://doi.org/10.37423/230107095. Acesso em: 25 ago. 2026. (A)
- GONÇALVES, Leticia Vieira et al. *FERRAMENTAS DE INTELIGÊNCIA ARTIFICIAL GENERATIVA NA EDUCAÇÃO: UM ESTUDO COMPARATIVO*. Disponível em: https://doi.org/10.47820/recima21.v7i2.7247. Acesso em: 25 ago. 2026. (A)
- LUCENA, Percival. *SemanticAgent, uma plataforma para desenvolvimento de agentes inteligentes*. Disponível em: https://doi.org/10.11606/d.55.2003.tde-01082003-102927. Acesso em: 25 ago. 2026. (A)
- REIS, Mariana De Luca; ANDRADE, Kleber de Oliveira. *ÁREAS DE PESQUISA E TÉCNICAS DE INTELIGÊNCIA ARTIFICIAL EM JOGOS DIGITAIS*. Disponível em: https://doi.org/10.47283/244670492022100171. Acesso em: 25 ago. 2026. (A)
- BRITTO, Ricardo; MEDEIROS, Adelardo Adelino Dantas de; ALSINA, Pablo Javier. *Uma arquitetura distribuída de hardware e software para controle de um robô móvel autônomo*. Disponível em: https://www.rcaap.pt/detail.jsp?id=oai:agregador.ibict.br.RI_UFRN:oai:repositorio:1/6117. Acesso em: 25 ago. 2026. (A)
- NARDIN, Luis G. *Uma arquitetura de apoio à interoperabilidade de modelos de reputação de agentes*. Disponível em: https://doi.org/10.11606/d.3.2009.tde-13072009-154149. Acesso em: 25 ago. 2026. (A)
- SANTOS, Tiago Cesar dos. *Uma proposta de arquitetura de software para a simulação e experimentação de veículos autônomos*. Disponível em: https://doi.org/10.11606/d.55.2016.tde-12122016-103140. Acesso em: 25 ago. 2026. (A)
- MAIA, Leticia Toledo. *Um estudo sobre aplicação de técnicas de inteligência artificial e engenharia de software à construção de um sistema de supervisão e controle*. Disponível em: https://doi.org/10.26512/2007.d.1453. Acesso em: 25 ago. 2026. (A)
- SANCHEZ, Maria Luiza d'Almeida; MAFFEO, Bruno. *Software Design Baseado em Subsistemas Autônomos - Focalizando o Reuso*. Disponível em: https://doi.org/10.5753/sbes.1996.24449. Acesso em: 25 ago. 2026. (A)
- CONCEIÇÃO, Gabriel Borges da. *ARQUITETURA DE SOFTWARE PARA UM TIME DE FUTEBOL DE ROBÔS AUTÔNOMOS*. Disponível em: https://doi.org/10.47879/ed.ep.2024653p24. Acesso em: 25 ago. 2026. (A)
- ALVES, PAULO HENRIQUE CARDOSO. *AGENTES DE SOFTWARE COM TRAÇOS DE PERSONALIDADE BASEADOS NA ARQUITETURA BDI PARA TOMADA DE DECISÕES NORMATIVAS*. Disponível em: https://doi.org/10.17771/pucrio.acad.32008. Acesso em: 25 ago. 2026. (A)
- KROTH, Eduardo; HEUSER, Carlos Alberto. *Uma arquitetura de software para reuso de componentes*. Disponível em: https://doi.org/10.5753/sbes.2000.25929. Acesso em: 25 ago. 2026. (A)
- ANTHROPIC. *Building Effective Agents*. Disponível em: https://www.anthropic.com/engineering/building-effective-agents. Acesso em: 25 ago. 2026. (B)
- ANTHROPIC. *Introducing the Model Context Protocol*. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 25 ago. 2026. (B)
- MODEL CONTEXT PROTOCOL. *What is MCP?*. Disponível em: https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro. Acesso em: 25 ago. 2026. (B)
- IBM. *What is Model Context Protocol (MCP)?*. Disponível em: https://www.ibm.com/think/topics/model-context-protocol. Acesso em: 25 ago. 2026. (B)
- FOWLER, Martin. *Harness Engineering for Coding Agents*. Disponível em: https://martinfowler.com/articles/harness-engineering.html. Acesso em: 25 ago. 2026. (B)
- PRINCETON UNIVERSITY. *SWE-bench Verified & Pro*. Disponível em: https://www.swebench.com. Acesso em: 25 ago. 2026. (A)
- SALESFORCE ENGINEERING. *Agentforce's Agent Script*. Disponível em: https://engineering.salesforce.com/agentforces-agentscript-building-deterministic-control-for-enterprise-ai-workflows/. Acesso em: 25 ago. 2026. (B)
- DIGITAL APPLIED. *Prompt Caching in 2026: Cut LLM Costs, Keep Quality*. Disponível em: https://www.digitalapplied.com/blog/prompt-caching-2026-cut-llm-costs-engineering-guide. Acesso em: 25 ago. 2026. (C)
- ATLAN. *Prompt vs Context vs Harness Engineering: Key Differences*. Disponível em: https://atlan.com/know/harness-engineering-vs-prompt-engineering/. Acesso em: 25 ago. 2026. (C)
- AUGMENT CODE. *Harness Engineering for AI Coding Agents*. Disponível em: https://www.augmentcode.com/guides/harness-engineering-ai-coding-agents. Acesso em: 25 ago. 2026. (B)
- DATABRICKS. *What is an AI Agent Harness?*. Disponível em: https://www.databricks.com/blog/ai-harness. Acesso em: 25 ago. 2026. (B)
- GANGLANI, Kunal. *4-Tier AI Agent Memory & State Management (2026)*. Disponível em: https://www.kunalganglani.com/blog/ai-agent-memory-state-management. Acesso em: 25 ago. 2026. (C)
- CODECENTRIC. *Loop, Harness, Context Engineering: The Terms Explained*. Disponível em: https://www.codecentric.de/en/knowledge-hub/blog/loop-harness-context-engineering-explained. Acesso em: 25 ago. 2026. (B)
- DESCHRYVER, Tim. *Keep Agentic AI Simple: A Practical Workflow*. Disponível em: https://timdeschryver.dev/blog/keep-agentic-ai-simple-a-practical-workflow-for-software-development. Acesso em: 25 ago. 2026. (C)
- MINDSTUDIO. *How to Build a Portable AI Agent Stack*. Disponível em: https://www.mindstudio.ai/blog/portable-ai-agent-stack-avoid-vendor-lock-in. Acesso em: 25 ago. 2026. (C)
- TRUFFLE SECURITY. *Do Pre-Commit Hooks Prevent Secrets Leakage?*. Disponível em: https://trufflesecurity.com/blog/do-pre-commit-hooks-prevent-secrets-leakage. Acesso em: 25 ago. 2026. (B)
- *Toward Agentic Software Engineering Beyond Code*. Disponível em: https://arxiv.org/html/2510.19692v2. Acesso em: 25 ago. 2026. (A)
- *AI-Native Software Engineering and the Evolution of the Agentic Engineer*. Disponível em: https://arxiv.org/html/2606.28791v1. Acesso em: 25 ago. 2026. (A)
