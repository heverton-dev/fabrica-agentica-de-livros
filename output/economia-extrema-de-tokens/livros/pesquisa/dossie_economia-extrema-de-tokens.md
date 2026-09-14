# Dossie de Pesquisa — Economia Extrema de Tokens e Otimização de Contexto

**Subtema:** Metodologias, compiladores, caches e skills agênticas para cortar até 85% do custo com LLMs  
**Escopo:** Camada 01 · Eficiência de Contexto & Skills — 8 Ferramentas / Soberania Total  
**Data de coleta:** 2026-08-25  

## Fontes Primarias

- Economia Extrema de Tokens, Contexto & Skills de Eficiência (Compêndio Técnico HTML) — file:///C:/Users/trcnologia/orca/projects/open-source/docs/listas/01-economia-de-tokens.html — autoridade: Curadoria de Elite - Open Source Initiative (OSI), Linux Foundation, CNCF Landscape

## Ferramentas Principais

### 01. Skill: caveman — Agentic Reasoning Compression

- **Tipo:** Prompt Skill — Compressão de Pensamento
- **Economia declarada:** -90% de tokens no bloco <thought>
- **SaaS substituido:** Pensamentos CoT prolixos e caros
- **Licenca:** MIT / Prompt Skill
- **Custo operacional:** 0 MB RAM / Overhead zero
- **Descricao:** Força o agente a pensar em estilo telegráfico (estilo homem das cavernas), sem artigos, sem saudações e sem repetir o prompt do usuário. Usa frases curtas de 3 a 5 linhas no Chain-of-Thought, economizando até 800 tokens a cada turno de raciocínio interno.
- **Caso de uso:** Raciocínios internos de agentes; compressão de pensamento em cadeia (Chain-of-Thought)
- **Beneficio-chave:** Tokens de pensamento interno custam o mesmo que tokens de saída. Pensar de forma enxuta é a forma mais rápida de economizar.

### 02. Skill: headroom — Log & Terminal Compression

- **Tipo:** Prompt Skill — Compressão de Logs
- **Economia declarada:** -80% de tokens em logs de compilação
- **SaaS substituido:** Dumps gigantes de terminal no contexto
- **Licenca:** MIT / Prompt Skill
- **Custo operacional:** 0 MB RAM / Filtro em runtime
- **Descricao:** Monitora e trunca logs longos de compilação, testes e builds, mantendo apenas o topo do comando e o stack trace do erro. Aplica regra rígida: se a saída do comando tiver > 7 linhas, comprime em (3 linhas do topo + 4 linhas do final), preservando a causa raiz da falha sem poluir a janela de contexto.
- **Caso de uso:** Logs de compilação; output de testes; dumps de terminal; builds
- **Beneficio-chave:** A maioria dos erros de compilação tem sua causa nas últimas 4 linhas. Ler 300 linhas de warning é queimar dinheiro.

### 03. Skill: lean-ctx — Targeted Code Inspection

- **Tipo:** Prompt Skill — Inspeção Cirúrgica de Código
- **Economia declarada:** -85% de tokens de leitura de código
- **SaaS substituido:** view_file() do arquivo inteiro
- **Licenca:** MIT / Prompt Skill
- **Custo operacional:** 0 MB RAM / Disciplina de agente
- **Descricao:** Obriga o agente a usar grep_search e ler trechos específicos com intervalo de linhas em vez de ler o arquivo completo. Impõe restrição comportamental: antes de ler qualquer arquivo com mais de 50 linhas, o agente deve localizar o símbolo exato via grep ou AST e ler apenas a fatia [StartLine/EndLine].
- **Caso de uso:** Edição de funções em arquivos grandes; busca de símbolos; inspeção de código estruturado
- **Exemplo pratico:** Alterar uma função em arquivo de 1.500 linhas: grep -> view_file(StartLine=120, EndLine=145) [25 linhas vs 1.500]
- **Beneficio-chave:** A maior causa de esquecimento em conversas longas é a poluição do contexto com arquivos lidos integralmente sem necessidade.

### 04. Skill: rtk-memory — Persistent Prefix Cache Memory

- **Tipo:** Scratchpad Skill — Cache de Prefixo Duradouro
- **Economia declarada:** 100% de reuso de prefix cache da Anthropic/OpenAI
- **SaaS substituido:** Reenvio de histórico antigo no prompt
- **Licenca:** MIT / Scratchpad Skill
- **Custo operacional:** Arquivo Markdown local / 0 RAM
- **Descricao:** Persiste novos aprendizados e correções em arquivo externo (RTK-SCRATCHPAD.md) para manter as instruções base imutáveis. Mantém o arquivo de governança principal (AGENTS.md/CLAUDE.md) intacto para que os provedores de LLM façam cache do prompt de sistema. Novos aprendizados da sessão são appendados em arquivo separado consultado sob demanda.
- **Caso de uso:** Governança de agentes; cache de prefixo em chamadas de API; manutenção de aprendizados entre sessões
- **Beneficio-chave:** Modificar o system prompt invalida o cache de prefixo em provedores como Anthropic, encarecendo todas as chamadas seguintes.

### 05. Repomix — Context Packing

- **Tipo:** CLI Determinística — Empacotador de Repositórios
- **Economia declarada:** -70% de tokens por prompt (~$300/mês)
- **SaaS substituido:** Leitura manual de múltiplos arquivos
- **Licenca:** MIT
- **Custo operacional:** < 30 MB RAM / CLI sob demanda
- **Descricao:** Empacota repositórios inteiros em 1 arquivo XML/Markdown com contagem exata de tokens e filtros inteligentes de .gitignore. Varre o repositório, descarta binários, lockfiles e arquivos ignorados no Git e compila um documento único com cabeçalhos XML e numeração de linhas para leitura otimizada por LLMs.
- **Caso de uso:** Análise de arquitetura completa; feature engineering; onboarding de repositórios
- **Comando basico:** `npx repomix --style xml --output-show-line-numbers`
- **Beneficio-chave:** Remove automaticamente arquivos binários, lockfiles e assets pesados antes de enviar o contexto à LLM.
- **Repositorio:** github.com/yamadashy/repomix

### 06. ast-grep (sg) — AST Search & Rewrite

- **Tipo:** CLI Determinística — Transformação Estrutural de Código
- **Economia declarada:** 100% grátis em transformações estruturais
- **SaaS substituido:** Refatorações caras via LLM
- **Licenca:** MIT
- **Custo operacional:** Binário Rust / < 10 MB RAM
- **Descricao:** Busca e reescrita de código baseada na Árvore de Sintaxe Abstrata (AST). Não erra espaçamentos nem quebras de linha. Faz o parsing do código-fonte em nós de Árvore Sintática usando Tree-sitter em Rust, permitindo buscar e substituir estruturas com wildcards sintáticos ($$$ARGS) em microssegundos.
- **Caso de uso:** Refatoração massiva; mudança de assinatura de função; renomeação; transformações estruturais
- **Comando basico:** `sg --pattern 'function $NAME($$$ARGS) { $$$BODY }'`
- **Exemplo pratico:** Alterar 50 arquivos: sg -p 'api.get($URL)' -r 'api.fetch({url: $URL})' -w [2ms vs horas de engenharia manual]
- **Beneficio-chave:** Substitui prompts inteiros de 'renomeie/altere assinatura' por uma chamada determinística de 2ms no terminal.
- **Repositorio:** ast-grep.github.io

### 07. LiteLLM Semantic Cache / OmniRouter — AI Gateway & Cache

- **Tipo:** Gateway + Cache Semântico — Roteamento Inteligente de LLM
- **Economia declarada:** -40% a -60% na fatura de API (~$500/mês)
- **SaaS substituido:** Chamadas duplicadas em APIs de LLM
- **Licenca:** MIT
- **Custo operacional:** ~70 MB RAM em repouso
- **Descricao:** Gateway de roteamento inteligente e cache semântico de respostas de LLM em Redis com balanceamento de carga. Calcula embeddings de prompts recebidos e faz busca por similaridade de cosseno no Redis antes de disparar requisições para a OpenAI/Anthropic. Se similaridade > 0.95, devolve a resposta cacheada em 2ms.
- **Caso de uso:** Suítes de testes automatizados; CI/CD com prompts repetidos; redução de custos de API; balanceamento de carga
- **Comando basico:** `docker run -d -p 4000:4000 ghcr.io/berriai/litellm:main-latest`
- **Beneficio-chave:** Essencial para suítes de testes de software e pipelines de CI/CD que rodam os mesmos prompts repetidamente.
- **Repositorio:** litellm.ai

### 08. DSPy (Stanford) — Prompt Compiler

- **Tipo:** Biblioteca Python — Compilador de Prompts
- **Economia declarada:** Reduz tamanho de prompt em até 50%
- **SaaS substituido:** Engenharia de prompt manual cara
- **Licenca:** MIT
- **Custo operacional:** Biblioteca pura / Zero runtime RAM
- **Descricao:** Compila e otimiza automaticamente instruções e few-shots via algoritmos matemáticos para máxima acurácia no menor prompt. Modela o pipeline como grafo computacional diferenciável. Otimizadores como BootstrapFewShot testam permutações de prompts contra uma métrica e geram a versão mais enxuta e assertiva.
- **Caso de uso:** Otimização de prompts para produção; compilação de pipelines LLM; redução de tamanho de contexto
- **Comando basico:** `pip install dspy-ai`
- **Beneficio-chave:** Trata prompts como código compilável. Se você mudar de modelo, basta recompilar o pipeline sem reescrever nada.
- **Repositorio:** dspy.ai

## Pilares de Governanca

### Pilar 1: Isolamento em Containers Docker (Criticidade: Alta)

Nunca instale ferramentas diretamente no sistema host sem isolamento de rede e volumes mapeados em disco seguro. O Docker fornece isolamento completo entre aplicações e o host.

### Pilar 2: Proxy Reverso com Caddy / Traefik (Criticidade: Alta)

Aponte a borda de rede para proxies leves com renovação automática de certificados TLS sem scripts manuais. Essencial para exposição segura de serviços internos.

### Pilar 3: Backup Imutável com Restic / Borg (Criticidade: Alta)

Programe snapshots diários dos volumes para armazenamento S3 remoto compatível para restauração rápida em caso de desastre. Garante recuperabilidade dos dados de estado.

### Pilar 4: Acesso Seguro via WireGuard / Headscale (Criticidade: Alta)

Mantenha painéis de administração e bancos de dados fora da internet pública, acessíveis apenas pela VPN mesh interna. Zero-trust network access.

## Metricas de Economia Global

A combinação das 8 ferramentas permite cortar até 85% do custo com LLMs quando aplicadas simultaneamente.

| Dimensao | Economia |
|---|---|
| reasoning_compression | 90% (caveman) |
| log_compression | 80% (headroom) |
| code_inspection | 85% (lean-ctx) |
| cache_prefix | 100% (rtk-memory) |
| context_packing | 70% (Repomix) |
| ast_transformations | 100% (ast-grep) |
| ai_gateway_cache | 40-60% (LiteLLM) |
| prompt_compilation | 50% (DSPy) |

## Matriz Comparativa SaaS Proprietario vs Open Source

| Aspecto | Proprietario | Open Source |
|---|---|---|
| Taxas de assento | 10-50 USD/user/mês | 0 USD (MIT / Open Source) |
| Overhead de contexto | 80-100% do custo mensal em ruído | 15-30% (com aplicação de skills) |
| Soberania de dados | Dados armazenados em nuvem (SaaS) | 100% local ou controle próprio (S3 compatível) |
| Portabilidade de lock-in | Acoplado ao provedor SaaS | Portável entre modelos / provedores |

## Palavras-chave

economia de tokens, otimização de contexto, prompt engineering, skills agênticas, compressão de logs, cache de prefixo, AST grep, LLM gateway, prompt compiler, soberania de dados, open source, zero lock-in, infraestrutura determinística

---

# Mineracao Academica - LLM prompt compression context caching token efficiency

Mineracao deterministic a (custo LLM zero) via APIs abertas
(`scripts/fontes_academicas.py`). Gerado em: 25 ago. 2026.

## Fontes consultadas

- OpenAlex: 10 resultados (ok)
- Crossref: 10 resultados (ok)
- arXiv: 10 resultados (ok)
- Semantic Scholar: 10 resultados (ok)
- SciELO: 0 resultados (erro)
- PubMed: 0 resultados (ok)

## Fontes brutas (mineracao academica - classe A)

- FAN, Wenqi et al. *A Survey on RAG Meeting LLMs: Towards Retrieval-Augmented Large Language Models*. 2024. Disponível em: https://doi.org/10.1145/3637528.3671470. Acesso em: 25 ago. 2026. (A)
- ZHAO, Wayne Xin et al. *A Survey of Large Language Models*. In: Frontiers of Computer Science. 2026. Disponível em: https://doi.org/10.1007/s11704-026-60308-3. Acesso em: 25 ago. 2026. (A)
- JIANG, Huiqiang et al. *LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression*. 2024. Disponível em: https://doi.org/10.18653/v1/2024.acl-long.91. Acesso em: 25 ago. 2026. (A)
- JIANG, Huiqiang et al. *LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models*. 2023. Disponível em: https://doi.org/10.18653/v1/2023.emnlp-main.825. Acesso em: 25 ago. 2026. (A)
- YANG, Dongjie et al. *PyramidInfer: Pyramid KV Cache Compression for High-throughput LLM Inference*. 2024. Disponível em: https://doi.org/10.18653/v1/2024.findings-acl.195. Acesso em: 25 ago. 2026. (A)
- GRATTAFIORI, Aaron et al. *Enriching Location Representation with Detailed Semantic Information*. In: arXiv (Cornell University). 2024. Disponível em: http://arxiv.org/abs/2407.21783. Acesso em: 25 ago. 2026. (A)
- NAVEED, Humza et al. *A Comprehensive Overview of Large Language Models*. In: arXiv (Cornell University). 2023. Disponível em: http://arxiv.org/abs/2307.06435. Acesso em: 25 ago. 2026. (A)
- HAN, Tingxu et al. *Token-Budget-Aware LLM Reasoning*. 2025. Disponível em: https://doi.org/10.18653/v1/2025.findings-acl.1274. Acesso em: 25 ago. 2026. (A)
- ALIZADEH, Keivan et al. *LLM in a flash: Efficient Large Language Model Inference with Limited Memory*. 2024. Disponível em: https://doi.org/10.18653/v1/2024.acl-long.678. Acesso em: 25 ago. 2026. (A)
- JIANG, Huiqiang et al. *LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression*. In: arXiv (Cornell University). 2023. Disponível em: http://arxiv.org/abs/2310.06839. Acesso em: 25 ago. 2026. (A)
- MITCHELL, Arthur. *Explorations in LLM Prompt Compression*. Disponível em: https://doi.org/10.14264/262de91. Acesso em: 25 ago. 2026. (A)
- EDUSA, Samuel. *ConsultChain: Progressive Context Distillation Across Heterogeneous LLM Fleets for Token-Optimal Inference*. 2026. Disponível em: https://doi.org/10.21203/rs.3.rs-9368244/v1. Acesso em: 25 ago. 2026. (A)
- MOHANDOSS, Ramaswami. *Context-based Semantic Caching for LLM Applications*. In: 2024 IEEE Conference on Artificial Intelligence (CAI). 2024. Disponível em: https://doi.org/10.1109/cai59869.2024.00075. Acesso em: 25 ago. 2026. (A)
- AUTOR. *Prompt Context Caching Architecture for Cost Reduction in Large Language Model Systems*. In: International Journal of Intelligent Systems and Applications in Engineering. 2026. Disponível em: https://doi.org/10.17762/ijisae.v14i1s.8385. Acesso em: 25 ago. 2026. (A)
- JIN, Haoying; FENG, Haoyang. *Llm-Cache: an Efficient Context-Aware Semantic Caching Framework for Distributed Llm Inference Services*. In: 2026 IEEE 46th International Conference on Distributed Computing Systems Workshops (ICDCSW). 2026. Disponível em: https://doi.org/10.1109/icdcsw72724.2026.00031. Acesso em: 25 ago. 2026. (A)
- AUTOR. *Figure 6: Token-Vector clustering results obtained by Prompt-Tuning and CE-Prompt.*. Disponível em: https://doi.org/10.7717/peerj-cs.3231/fig-6. Acesso em: 25 ago. 2026. (A)
- NEGRÃO, Vinícius; BOCCI, Maíra; PITREZ, Paulo. *FEW-AI-SERIAL: A Domain-Agnostic Semantic Compression Protocol for LLM Prompt Injection and IoT Data Encoding*. 2026. Disponível em: https://doi.org/10.2139/ssrn.6491958. Acesso em: 25 ago. 2026. (A)
- LISKAVETS, Barys et al. *Prompt Compression with Context-Aware Sentence Encoding for Fast and Improved LLM Inference*. In: Proceedings of the AAAI Conference on Artificial Intelligence. 2025. Disponível em: https://doi.org/10.1609/aaai.v39i23.34639. Acesso em: 25 ago. 2026. (A)
- LEE, Jungmin; LV, Peizhuo; LEE, Yeonjoon. *PROMPRINT: Prompt Fingerprinting via First-Token Response for LLM App Cloning Detection*. In: Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 2026. Disponível em: https://doi.org/10.18653/v1/2026.acl-long.1052. Acesso em: 25 ago. 2026. (A)
- VARRICCHIO, Stefano; CALLEN, Yehuda. *Visualizing Text for Token Efficiency: Exploring Multimodal LLMs' Performance in Text-as-Image Input Compression*. 2025. Disponível em: https://doi.org/10.22541/au.176340962.25437895/v1. Acesso em: 25 ago. 2026. (A)
- FEI, Weizhi et al. *Efficient Prompt Compression with Evaluator Heads for Long-Context Transformer Inference*. In: arXiv. 2025. Disponível em: http://arxiv.org/abs/2501.12959v2. Acesso em: 25 ago. 2026. (A)
- LIN, Xiaolin et al. *CompressKV: Semantic-Retrieval-Guided KV-Cache Compression for Resource-Efficient Long-Context LLM Inference*. In: arXiv. 2026. Disponível em: http://arxiv.org/abs/2606.24467v1. Acesso em: 25 ago. 2026. (A)
- LUO, Wei et al. *Meta-Soft: Leveraging Composable Meta-Tokens for Context-Preserving KV Cache Compression*. In: arXiv. 2026. Disponível em: http://arxiv.org/abs/2605.22337v2. Acesso em: 25 ago. 2026. (A)
- HAN, Jialong; WU, You; TU, Kewei. *S$^4$R: Selective Sampling, Subspaces, and Sparse Reconstruction for Compressed Long-Context KV Caching*. In: arXiv. 2026. Disponível em: http://arxiv.org/abs/2608.00528v1. Acesso em: 25 ago. 2026. (A)
- YUAN, Jiayi et al. *KV Cache Compression, But What Must We Give in Return? A Comprehensive Benchmark of Long Context Capable Approaches*. In: arXiv. 2024. Disponível em: http://arxiv.org/abs/2407.01527v2. Acesso em: 25 ago. 2026. (A)
- METEL, Michael R.; CHEN, Boxing; REZAGHOLIZADEH, Mehdi. *Batch-Max: Higher LLM Throughput using Larger Batch Sizes and KV Cache Compression*. In: arXiv. 2024. Disponível em: http://arxiv.org/abs/2412.05693v3. Acesso em: 25 ago. 2026. (A)
- WAN, Zhongwei et al. *LOOK-M: Look-Once Optimization in KV Cache for Efficient Multimodal Long-Context Inference*. In: arXiv. 2024. Disponível em: http://arxiv.org/abs/2406.18139v1. Acesso em: 25 ago. 2026. (A)
- STANISZEWSKI, Konrad; ŁAŃCUCKI, Adrian. *KV Cache Transform Coding for Compact Storage in LLM Inference*. In: arXiv. 2025. Disponível em: http://arxiv.org/abs/2511.01815v2. Acesso em: 25 ago. 2026. (A)
- TIAN, Zhenxu et al. *Where Matters More Than What: Decoding-aligned KV Cache Compression via Position-aware Pseudo Queries*. In: arXiv. 2026. Disponível em: http://arxiv.org/abs/2603.11564v1. Acesso em: 25 ago. 2026. (A)
- YAN, Jianxin et al. *QCFuse: Query-Aware Cache Fusion via Compressed View for Efficient RAG Serving*. In: arXiv. 2026. Disponível em: http://arxiv.org/abs/2606.05875v1. Acesso em: 25 ago. 2026. (A)
- LISKAVETS, Barys et al. *Prompt Compression with Context-Aware Sentence Encoding for Fast and Improved LLM Inference*. In: AAAI Conference on Artificial Intelligence. 2024. Disponível em: https://www.semanticscholar.org/paper/7a4f8771974498f20574bfce4352cb88b2b6cd8c. Acesso em: 25 ago. 2026. (A)
- ZHANG, Tinghui; WANG, Yifan; WANG, Daisy Zhe. *SCOPE: A Generative Approach for LLM Prompt Compression*. In: arXiv.org. 2025. Disponível em: https://www.semanticscholar.org/paper/4c101e9b3a84a793b00d3ed00c5232435420142c. Acesso em: 25 ago. 2026. (A)
- SONG, Yangfan. *Cache-Aware Prompt Compression:A Two-Tier Cost Model for LLM API Caching*. 2026. Disponível em: https://www.semanticscholar.org/paper/aa8146c31d171edfe37f7d41fbc9655d2c554231. Acesso em: 25 ago. 2026. (A)
- CAMPOS, A. et al. *Lossless Prompt Compression via Dictionary-Encoding and In-Context Learning: Enabling Cost-Effective LLM Analysis of Repetitive Data*. In: arXiv.org. 2026. Disponível em: https://www.semanticscholar.org/paper/c9314e5c12102c8d489f511fd3764408229045d5. Acesso em: 25 ago. 2026. (A)
- PAN, Zhuoshi et al. *LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression*. In: Annual Meeting of the Association for Computational Linguistics. 2024. Disponível em: https://www.semanticscholar.org/paper/3d45fc603e34934fc589b9547307815f7723de34. Acesso em: 25 ago. 2026. (A)
- LONG, Lingkun et al. *SlimInfer: Accelerating Long-Context LLM Inference via Dynamic Token Pruning*. In: AAAI Conference on Artificial Intelligence. 2025. Disponível em: https://www.semanticscholar.org/paper/0fa26f527aa34404a6f043c41d2769e3a40ff56c. Acesso em: 25 ago. 2026. (A)
- TANG, Jiwei et al. *Perception Compressor: A Training-Free Prompt Compression Framework in Long Context Scenarios*. In: North American Chapter of the Association for Computational Linguistics. 2024. Disponível em: https://www.semanticscholar.org/paper/544718be71f1598d95744f30498368d16f39a3e3. Acesso em: 25 ago. 2026. (A)
- JOHNSON, Warren. *Compression Method Matters: Benchmark-Dependent Output Dynamics in LLM Prompt Compression*. In: arXiv.org. 2026. Disponível em: https://www.semanticscholar.org/paper/f8d6c67a825d43790df36d8f93f728772e3d8420. Acesso em: 25 ago. 2026. (A)
- JOHNSON, Warren. *The Compression Paradox in LLM Inference: Provider-Dependent Energy Effects of Prompt Compression*. In: arXiv.org. 2026. Disponível em: https://www.semanticscholar.org/paper/0b957220f36da0853daf61e896c3251e63a74ce5. Acesso em: 25 ago. 2026. (A)
- ZHANG, Haoran; SUN, Zhaohua. *AGORA: Adapter-Grounded Observation-Action Retention for Inference-Free Prompt Compression in LLM Agents*. In: arXiv.org. 2026. Disponível em: https://www.semanticscholar.org/paper/f474c2d0b6c1c9131f14740bc8f9d314c0e4c3a4. Acesso em: 25 ago. 2026. (A)
