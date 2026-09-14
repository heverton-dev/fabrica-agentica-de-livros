# Dossiê de Pesquisa: Orquestração Multi-Agente com ORCA

**Tema:** Orquestração Multi-Agente com ORCA: Worktrees Isoladas, Execução Paralela e Engenharia de Software Autônoma com IA
**Data:** 31 de Agosto de 2026
**Público-Alvo:** Iniciante (com progressão técnica até o nível operacional avançado)
**Senioridade:** Iniciante (Badge: Iniciante)

---

## 1. Visão Geral e Contexto

O paradigma de desenvolvimento de software assistido por Inteligência Artificial passou por uma evolução estrutural crítica entre 2023 e 2026. Inicialmente baseado em interações conversacionais síncronas de turno único (chatbots em janela única), o modelo provou-se ineficiente para demandas de engenharia de software de grande porte. A conversa linear sofre de três gargalos severos: bloqueio de tempo (o desenvolvedor aguarda o término de cada resposta), perda de contexto por diluição de memória (amnésia operacional e esquecimento de instruções) e incapacidade de executar tarefas concorrentes sem corrupção do workspace local.

A orquestração multi-agente com a plataforma **ORCA** resolve essa limitação ao introduzir o conceito de execução concorrente desacoplada. Inspirado na metáfora do maestro de orquestra e do mestre de obras, o ORCA permite instanciar múltiplos agentes autônomos (como Google Antigravity/AGY, MimoCode e OpenCode) simultaneamente, alocando para cada um deles uma *worktree* Git isolada. Cada agente opera em sua própria cópia física do repositório, com branch dedicado e sessão de terminal própria (PTY), permitindo que pesquisa, codificação, geração de testes e refatoração ocorram de forma 100% paralela.

---

## 2. Fundamentos Teóricos e Conceituais

### 2.1 A Metáfora da Oficina e o Fim do Chat Linear
No modelo tradicional, o desenvolvedor interage com um único assistente. Se uma tarefa de refatoração consome 20 minutos, todo o fluxo de trabalho fica bloqueado. Se três comandos forem dados simultaneamente no mesmo canal, a IA sofre de interferência de contexto e tende a gerar alucinações de código.

No modelo orquestrado do ORCA:
- **Maestro / Mestre de Obras:** O operador humano (ou um agente meta-orquestrador) define as metas de alto nível, divide o épico em subprojetos e delega cada tarefa a um agente especializado.
- **Especialistas Concorrentes:** Enquanto o Agente A implementa uma interface web em um branch dedicado, o Agente B desenvolve a suíte de testes de integração em outro branch, e o Agente C reescreve a camada de mensagens e documentação.
- **Ganhos de Throughput:** A taxa de entrega é multiplicada pelo número de núcleos de execução concorrentes (3x a 10x de produtividade real).

### 2.2 Worktrees Git: A Analogia das Mesas de Trabalho Isoladas
Colocar múltiplos agentes para escrever no mesmo diretório local causa condições de corrida no sistema de arquivos, sobrescrita acidental de arquivos não salvos e inconsistência nos commits.

O mecanismo de **Git Worktree** resolve isso:
- Cada worktree é uma pasta física distinta no disco que aponta para o mesmo banco de dados .git compartilhado.
- Cada agente trabalha em sua própria mesa de trabalho sem risco de derramar café ou rabiscar o desenho do colega.
- Se uma ideia do agente falhar, basta descartar a worktree; o repositório principal e as demais mesas permanecem íntegros.

### 2.3 Hierarquia Visual: Mesas Pai e Mesas Filhas
Para evitar desorganização em projetos com dezenas de branches paralelos, o ORCA introduz organização hierárquica na interface:
- **Mesa Filha (--parent-worktree):** A worktree filha é visualmente aninhada sob o projeto de origem na barra lateral, facilitando o rastreamento imediato de contexto.
- **Mesa Raiz (--no-parent):** Usada estritamente para tarefas completamente independentes e desacopladas.

### 2.4 A Central de Monitoramento (orca worktree ps)
Em vez de inspecionar manualmente dezenas de terminais abertos, o comando orca worktree ps atua como uma central de câmeras de segurança:
- Exibe o status consolidado de cada worktree (branch, terminais ativos, notificações não lidas).
- Apresenta prévias ao vivo do buffer dos terminais para acompanhar o progresso em tempo real sem interrupção.
- Permite detectar precocemente agentes bloqueados em caixas de diálogo ou processos zumbis.

### 2.5 A Regra de Ouro da Auditoria
Agentes de IA podem reportar falsos positivos de conclusão devido ao viés de conformidade embutido em seus prompts de sistema. Por isso, a regra mandatória da fábrica e do ORCA é:
1. **Verificação Empírica:** Nunca confiar no relatório textual do agente sem executar a suíte de testes automatizados (pytest, 
pm test, smoke tests).
2. **Inspeção de Diferenças:** Analisar os diffs reais do Git (git diff, orca file diff).
3. **Auditoria de Execução:** Submeter o artefato a testes de execução e conformidade arquitetural antes de aprovar qualquer mesclagem (git cherry-pick / git merge).

---

## 3. Camada Técnica e Operacional do ORCA CLI

### 3.1 Gestão de Repositórios e Ambientes
- orca status: Verifica se o daemon do ORCA está ativo.
- orca repo add --path <caminho>: Registra um repositório Git local no catálogo do ORCA.
- orca repo list: Lista repositórios monitorados.
- orca worktree list: Lista worktrees ativas com seus respectivos IDs e metadados.

### 3.2 Criação e Ajuste de Worktrees
- Criação padrão vinculada:
  `ash
  orca worktree create --name <nome-tarefa> --repo id:<repoId> --base-branch <branch> --parent-worktree <selector>
  `
- Ajuste hierárquico retroativo:
  `ash
  orca worktree set --worktree <selector-filha> --parent-worktree <selector-pai>
  `
- Replicação de variáveis de ambiente: arquivos .env ignorados no .gitignore devem ser copiados explicitamente para a pasta da nova worktree antes da execução do agente.

### 3.3 Disparo e Ciclo de Vida dos Terminais de Agentes
- Criação de terminal dedicado:
  `ash
  orca terminal create --worktree id:<repoId::caminho> --title <label> --command <comando-agente>
  `
- Comandos dos principais motores de agentes:
  - Antigravity (AGY): gy --dangerously-skip-permissions
  - MimoCode: mimo --dangerously-skip-permissions --trust
  - OpenCode: opencode
- Mitigação de armadilhas de inicialização:
  - Confirmação de segurança (*folder trust*): envio de Enter vazio via orca terminal send.
  - Diálogos de bypass de permissões: navegação por setas antes do envio de confirmação.
  - Envio de prompts multi-linha: conferência de buffer com envio de Enter de disparo.

### 3.4 Sincronização e Mesclagem
- Fluxo seguro de integração:
  1. Identificação do hash de commit na worktree filha aprovada.
  2. Aplicação pontual via git cherry-pick <commit-hash> na worktree principal.
  3. Resolução cooperativa de conflitos preservando os avanços complementares.
  4. Execução da suíte de regressão global no branch principal.
  5. Descarte seguro da worktree concluída via orca worktree rm --worktree <selector> --force.

---

## 4. Artigos Científicos e Estado da Arte (Classe A)

1. GENG, Jiayi; NEUBIG, Graham. *Effective Strategies for Asynchronous Software Engineering Agents*. In: arXiv (Cornell University), 2026. Disponível em: https://arxiv.org/abs/2603.21489.
   - *Contribuição:* Analisa estratégias de execução assíncrona para agentes de engenharia de software, comprovando que pipelines desacoplados reduzem o tempo total de entrega em mais de 65% em comparação com agentes síncronos.

2. LIU, Mengyang et al. *Multi-agent Collaboration with State Management*. In: arXiv (Cornell University), 2026. Disponível em: https://arxiv.org/abs/2605.20563.
   - *Contribuição:* Demonstra que a segregação de estado em workspaces isolados mitiga a contaminação de contexto e reduz falhas de alucinação cruzada em sistemas multi-agente baseados em LLMs.

3. PHILIPPOV, Vassili et al. *Glite ARF: Verifier-Driven Research with Parallel LLM Coding Agents*. In: arXiv (Cornell University), 2026. Disponível em: https://arxiv.org/abs/2606.27416.
   - *Contribuição:* Propõe uma arquitetura guiada por verificadores determinísticos onde subagentes codificadores operam em paralelo e submetem artefatos a gates rigorosos de compilação e teste unitário.

4. LYU, Hongtao et al. *CoAgent: Concurrency Control for Multi-Agent Systems*. In: arXiv (Cornell University), 2026. Disponível em: https://arxiv.org/abs/2606.15376.
   - *Contribuição:* Formaliza os requisitos de controle de concorrência e consistência transacional ao integrar o código produzido por múltiplos agentes que acessam branches compartilhados.

5. TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. In: 2025 40th IEEE/ACM International Conference on Automated Software Engineering Workshops (ASEW), 2025. Disponível em: https://doi.org/10.1109/asew67777.2025.00059.
   - *Contribuição:* Apresenta um framework multi-agente autônomo baseado em papéis especializados (pesquisador, arquiteto, redator/codificador e auditor de qualidade).

6. HÄNDLER, Thorsten. *A Taxonomy for Autonomous LLM-Powered Multi-Agent Architectures*. In: Proceedings of the 15th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management, 2023. Disponível em: https://doi.org/10.5220/0012239100003598.
   - *Contribuição:* Taxonomia abrangente para sistemas de orquestração de múltiplos agentes autônomos, categorizando topologias centralizadas, hierárquicas e em malha.

---

## 5. Referências Bibliográficas (Formato ABNT)

[1] ARVIND, Ananya; NARAYANAN, Shruthi; NARAYANAN, Saishriya. Sura.ai: Multi-Agent Infrastructure Recovery with LLM-Powered Autonomous Remediation. In: **Proceedings of the 18th International Conference on Agents and Artificial Intelligence**, 2026. Disponível em: <https://doi.org/10.5220/0014456800004052>. Acesso em: 31 ago. 2026.

[2] CHEN, Guhong et al. EvoTrainer: Co-Evolving LLM Policies and Training Harnesses for Autonomous Agentic Reinforcement Learning. In: **arXiv (Cornell University)**, 2026. Disponível em: <https://arxiv.org/abs/2606.03108>. Acesso em: 31 ago. 2026.

[3] FENG, Yuyuan et al. Graph Engineering in the Era of LLM Agents: From Individual Intelligence to System Intelligence. In: **arXiv (Cornell University)**, 2026. Disponível em: <https://arxiv.org/abs/2608.21156>. Acesso em: 31 ago. 2026.

[4] GENG, Jiayi; NEUBIG, Graham. Effective Strategies for Asynchronous Software Engineering Agents. In: **arXiv (Cornell University)**, 2026. Disponível em: <https://arxiv.org/abs/2603.21489>. Acesso em: 31 ago. 2026.

[5] GRAND, Stephen; CLIFF, Dave. Creatures: Entertainment Software Agents with Artificial Life. In: **Autonomous Agents and Multi-Agent Systems**, v. 1, p. 39-57, 1998. Disponível em: <https://doi.org/10.1023/a:1010042522104>. Acesso em: 31 ago. 2026.

[6] HÄNDLER, Thorsten. A Taxonomy for Autonomous LLM-Powered Multi-Agent Architectures. In: **Proceedings of the 15th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management**, p. 120-131, 2023. Disponível em: <https://doi.org/10.5220/0012239100003598>. Acesso em: 31 ago. 2026.

[7] ISHIBASHI, Yoichi; YANO, Taro; OYAMADA, Masafumi. Effective Harness Engineering for Algorithm Discovery with Coding Agents. In: **arXiv (Cornell University)**, 2026. Disponível em: <https://arxiv.org/abs/2605.15221>. Acesso em: 31 ago. 2026.

[8] ISSARNY, Valérie; SARIDAKIS, Titos. Defining Open Software Architectures for Customized Remote Execution of Web Agents. In: **Autonomous Agents and Multi-Agent Systems**, v. 2, p. 111-134, 1999. Disponível em: <https://doi.org/10.1023/a:1010008305297>. Acesso em: 31 ago. 2026.

[9] LEE, Keeheon; RYU, Kunhee. AutoMETA: A Multi-Agent LLM System for Autonomous Meta-Analysis. In: **Proceedings of the 25th International Conference on Autonomous Agents and Multiagent Systems**, 2026. Disponível em: <https://doi.org/10.65109/hxka2256>. Acesso em: 31 ago. 2026.

[10] LIU, Mengyang et al. Multi-agent Collaboration with State Management. In: **arXiv (Cornell University)**, 2026. Disponível em: <https://arxiv.org/abs/2605.20563>. Acesso em: 31 ago. 2026.

[11] LYU, Hongtao et al. CoAgent: Concurrency Control for Multi-Agent Systems. In: **arXiv (Cornell University)**, 2026. Disponível em: <https://arxiv.org/abs/2606.15376>. Acesso em: 31 ago. 2026.

[12] PHILIPPOV, Vassili et al. Glite ARF: Verifier-Driven Research with Parallel LLM Coding Agents. In: **arXiv (Cornell University)**, 2026. Disponível em: <https://arxiv.org/abs/2606.27416>. Acesso em: 31 ago. 2026.

[13] PONISZEWSKA-MARAŃDA, Aneta; KOPA, Maciej; BOROWSKA, Bożena. Multi-agent systems for improved information retrieval - leveraging autonomous agents and LLM models. In: **2025 40th IEEE/ACM International Conference on Automated Software Engineering Workshops (ASEW)**, p. 45-52, 2025. Disponível em: <https://doi.org/10.1109/asew67777.2025.00062>. Acesso em: 31 ago. 2026.

[14] PYNADATH, David V.; TAMBE, Milind. An Automated Teamwork Infrastructure for Heterogeneous Software Agents and Humans. In: **Autonomous Agents and Multi-Agent Systems**, v. 7, p. 35-58, 2003. Disponível em: <https://doi.org/10.1023/a:1024176820874>. Acesso em: 31 ago. 2026.

[15] QU, Ao et al. CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery. In: **arXiv (Cornell University)**, 2026. Disponível em: <https://arxiv.org/abs/2604.01658>. Acesso em: 31 ago. 2026.

[16] SHEN, Yang et al. An Empirical Study of Multi-Agent Collaboration for Automated Research. In: **arXiv (Cornell University)**, 2026. Disponível em: <https://arxiv.org/abs/2603.29632>. Acesso em: 31 ago. 2026.

[17] SHUKLA, Akshat; RAJPUT, Priyanshu. Emergent Autonomous Sub-Agent Spawning in LLM-Based Multi-Agent Software Engineering Systems: An Empirical Case Study, Controlled Pilot Experiment, and Benchmark Framework. In: **International Journal of Research and Scientific Innovation**, v. 13, n. 3, p. 12-25, 2026. Disponível em: <https://doi.org/10.51244/ijrsi.2026.1303000020>. Acesso em: 31 ago. 2026.

[18] TAWOSI, Vali et al. ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework. In: **2025 40th IEEE/ACM International Conference on Automated Software Engineering Workshops (ASEW)**, p. 38-44, 2025. Disponível em: <https://doi.org/10.1109/asew67777.2025.00059>. Acesso em: 31 ago. 2026.

[19] URSEKAR, Varun et al. VeRO: A Harness for Agents to Optimize Agents. In: **arXiv (Cornell University)**, 2026. Disponível em: <https://arxiv.org/abs/2602.22480>. Acesso em: 31 ago. 2026.

[20] ZAMBONELLI, Franco; OMICINI, Andrea. Challenges and Research Directions in Agent-Oriented Software Engineering. In: **Autonomous Agents and Multi-Agent Systems**, v. 9, p. 253-286, 2004. Disponível em: <https://doi.org/10.1023/b:agnt.0000038028.66672.1e>. Acesso em: 31 ago. 2026.