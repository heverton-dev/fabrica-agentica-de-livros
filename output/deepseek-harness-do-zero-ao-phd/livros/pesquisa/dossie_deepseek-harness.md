# Dossiê de Pesquisa — DeepSeek Harness: Do zero ao PhD

## Conceitos-chave

- **DeepSeek Harness (dsh):** framework agêntico open-source (MIT) da DeepSeek AI, lançado em 13/ago/2026 em developer preview (v0.1). Tudo é plugin — modelos, ferramentas, loops, sessões, sandboxes, storage, UI. Arquitetura baseada no Cordis. (B)
- **Cordis:** framework meta de plugins sob o DeepSeek Harness. Plugins contribuem serviços, eventos tipados e efeitos reversíveis para um contexto compartilhado. Ciclo de vida: ready/dispose/fork. (B)
- **Session Events:** eventos duráveis para limites de turn, passos, mensagens, conteúdo assistente, chamadas de ferramentas. Permitem resume, fork, search e replay do mesmo stream de eventos. (B)
- **Tool Pipeline:** fluxo de ferramentas que permite policy, hooks, sandboxing, guards de filesystem, reescrita de resultados, observação final e renderização de UI como camadas de plugin. (B)
- **DeepSeek V4-Pro:** melhor LLM open-source de 2026 (AIME 2025: 70.3%), ecossistema nativo de ferramentas e profundidade multimodal. (B)
- **Modos de Execução:** Standard (toolset completo), Code (SDK de código), Minimal (shell + editor), Creator (personalizado). (B)
- **Profiles:** "receitas" de configuração que empilham camadas de configuração para personalizar o comportamento do harness. (B)
- **Sandbox com Git Worktree:** isolamento por worktree git — cada sessão de agente tem seu próprio diretório de trabalho e índice git, compartilhando o mesmo repositório. (B)
- **Quantização GGUF:** formato para inferência local em CPU/Metal/GPU heterogêneo. Q4_K_M mantém 92% da qualidade. Ideal para Ollama. (A)
- **Quantização AWQ:** formato para GPU tensor cores. Retém 95% da qualidade. Melhor throughput em GPU. (A)
- **Quantização GPTQ:** formato legado GPU. Uma vez que kernels mais novos o superaram, perderam popularidade. (A)
- **vLLM:** engine de inferência de alto throughput para produção. Suporta PagedAttention, batching dinâmico. Ideal para servir múltiplos usuários. (B)
- **Ollama:** wrapper de llama.cpp focado em usabilidade. Instalação com um comando. Ideal para experimentação local e hardware consumer. (B)
- **llama.cpp:** engine de inferência C++ de baixo nível. Maior amplitude de hardware (CPU, Metal, CUDA, Vulkan). Infraestrutura base do Ollama. (B)
- **RAG (Retrieval-Augmented Generation):** pipeline de geração aumentada por recuperação. Banco de vetores (ChromaDB, Qdrant, Weaviate, Milvus) + embedding model + LLM. (A)
- **QLoRA:** fine-tuning eficiente com quantização 4-bit. 7B model = ~5GB VRAM. Frameworks: Unsloth, Axolotl. (A)
- **LoRA (Low-Rank Adaptation):** técnica de fine-tuning que adapta apenas parâmetros de baixa dimensão, preservando o modelo base. (A)
- **DeepSeek R1:** modelo de raciocínio com cadeia-de-pensamento. Distill variants (1.5B a 70B) para hardware consumer. Modelo completo: 671B parâmetros. (A)
- **Plugin Hub:** repositório de plugins curado (awesome-deepseek-harness) com infraestrutura de dsh-external/hub e tópico público dsh-plugin. (B)

## Artigos Científicos e Papers

- FERRAG, Mohamed Amine; TIHANYI, Norbert; DEBBAH, Mérouane. *From LLM Reasoning to Autonomous AI Agents: A Comprehensive Review*. In: IEEE Access, 2026. Disponível em: https://doi.org/10.1109/access.2026.3698694. Acesso em: 23 ago. 2026.
- DAI, Jing. *DeepSeek-V3 Core Architecture and Its Training Techniques in Detail*. In: DeepSeek in Action. 2025. Disponível em: https://doi.org/10.1201/9781003674702-3. Acesso em: 23 ago. 2026.
- DAI, Jing. *A First Look at the DeepSeek-V3 Big Model*. In: DeepSeek in Action. 2025. Disponível em: https://doi.org/10.1201/9781003674702-6. Acesso em: 23 ago. 2026.
- DAI, Jing. *Introduction to DeepSeek-V3 Model-Based Development*. In: DeepSeek in Action. 2025. Disponível em: https://doi.org/10.1201/9781003674702-4. Acesso em: 23 ago. 2026.
- DAI, Jing. *DeepSeek Open Platform and API Development Details*. In: DeepSeek in Action. 2025. Disponível em: https://doi.org/10.1201/9781003674702-7. Acesso em: 23 ago. 2026.
- ARRIETA, Aitor et al. *o3-mini vs DeepSeek-R1: Which One is Safer?*. In: arXiv, 2025. Disponível em: http://arxiv.org/abs/2501.18438. Acesso em: 23 ago. 2026.
- ZHANG, Jie et al. *When LLMs Meet Cybersecurity: A Systematic Literature Review*. In: arXiv, 2024. Disponível em: http://arxiv.org/abs/2405.03644. Acesso em: 23 ago. 2026.
- XU, Mengwei et al. *A Survey of Resource-efficient LLM and Multimodal Foundation Models*. In: arXiv, 2024. Disponível em: http://arxiv.org/abs/2401.08092. Acesso em: 23 ago. 2026.
- KOURANI, Humam et al. *Evaluating large language models on business process modeling*. In: Software & Systems Modeling, 2025. Disponível em: https://doi.org/10.1007/s10270-025-01318-w. Acesso em: 23 ago. 2026.
- WONG, Wai Kin et al. *DecLLM: LLM-Augmented Recompilable Decompilation*. In: Proceedings of the ACM on Software Engineering, 2025. Disponível em: https://doi.org/10.1145/3728958. Acesso em: 23 ago. 2026.

## Estado da arte / ferramentas de referência

- **DeepSeek Harness (dsh):** framework agêntico plugin-first. MIT license. Cordis como kernel. 141k+ stars em 4 dias. (B) — https://github.com/deepseek-ai/deepseek-harness
- **DeepSeek V4-Pro:** melhor LLM open-source 2026. Native tool ecosystems, multimodal. (B) — https://deepseek.com
- **Ollama:** instalação em 1 comando, API OpenAI-compatível na porta 11434. Suporta GPU Apple Silicon, NVIDIA, AMD. (B) — https://ollama.com
- **vLLM:** engine de inferência para produção. PagedAttention, continuous batching. API OpenAI-compatível. (B) — https://github.com/vllm-project/vllm
- **llama.cpp:** engine C++ multi-platform. Quantização GGUF. CPU, Metal, CUDA, Vulkan. (B) — https://github.com/ggerganov/llama.cpp
- **LM Studio:** GUI desktop para rodar LLMs locais. Download de modelos do HuggingFace. (B) — https://lmstudio.ai
- **Hugging Face TGI:** Text Generation Inference. Servidor de inferência para produção com Docker. (B) — https://github.com/huggingface/text-generation-inference
- **ChromaDB:** banco de vetores leve para dev local. Open-source, embedding integrado. (B) — https://www.trychroma.com
- **Qdrant:** engine de busca vetorial em Rust. Open-source, self-hostable, escalável. (B) — https://qdrant.tech
- **Weaviate:** banco de vetores com busca vetorial + keyword. Open-source, self-hostable. (B) — https://weaviate.io
- **Milvus:** banco de vetores para produção em larga escala. Open-source (Zilliz Cloud). (B) — https://milvus.io
- **Axolotl:** framework de fine-tuning LLM. Suporta LoRA, QLoRA, DPO, full fine-tune. (B) — https://github.com/axolotl-ai-cloud/axolotl
- **Unsloth:** fine-tuning 2x mais rápido, 70% menos memória. Open-source. (B) — https://github.com/unslothai/unsloth

## Casos de uso corporativos

- **xCloud:** hosting gerenciado de DeepSeek Harness. Deploy em 1 clique a $9.99/mês. SSL automático, segurança, monitoramento. (C) — https://xcloud.host
- **MindStudio:** integração de DeepSeek Harness como framework de coding agêntico para empresas. (C) — https://mindstudio.ai
- **Composio:** hub de plugins para DeepSeek Harness com 10+ plugins curados para 2026. (C) — https://composio.dev
- **DeepSeek Harness + Claude Code/Codex:** subagentes side-by-side em worktrees isolados. Multi-modelo no mesmo pipeline. (B)
- **Enterprise RAG:** Qdrant/Weaviate self-hosted para pipelines de RAG em ambientes corporativos com dados sensíveis. (B)

## Limitações e controvérsias

- **Modelo completo 671B:** requer hardware massivo (multi-GPU com centenas de GB de VRAM). Praticamente inacessível para uso local sem infraestrutura dedicada. (A)
- **Quantização: perda de qualidade inevitable.** Q4_K_M GGUF retém 92%, AWQ retém 95%, mas ambas introduzem degradação mensurável em benchmarks de código e raciocínio complexo. (A)
- **DeepSeek V4-Pro:** melhor LLM open-source de 2026, mas экосистема de plugins ainda em v0.1 developer preview — API instável, plugins podem quebrar a cada atualização. (C)
- **Ollama vs vLLM vs llama.cpp:** nenhum é universalmente superior. Ollama vence em usabilidade, vLLM em throughput de produção, llama.cpp em amplitude de hardware. Escolha depende do caso de uso. (B)
- **Cordis:** framework novo e não testado em escala enterprise. Potencial de overhead de abstração em pipelines de alta performance. (C)
- **Fine-tuning local:** exige conhecimento técnico significativo. Preparação de dados, hyperparameters, evaluation — muitas fontes de falha silenciosa. (A)
- **Segurança de sandbox:** worktrees isolam filesystem mas não isolam runtime (portas Docker, estado compartilhado). (B)

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- DEEPSEEK AI. *DeepSeek Harness developer preview: Everything is a plugin*. Disponível em: https://deepseek.com/harness/en/. Acesso em: 23 ago. 2026. (B)
- DEEPSEEK AI. *DeepSeek Harness (dsh): Everything is a Plugin*. GitHub. Disponível em: https://github.com/deepseek-ai/deepseek-harness. Acesso em: 23 ago. 2026. (B)
- DEEPSEEK AI. *deepseek-harness/docs/architecture.md*. GitHub. Disponível em: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md. Acesso em: 23 ago. 2026. (B)
- DEEPSEEK AI. *deepseek-harness/docs/cordis-primer.md*. GitHub. Disponível em: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-primer.md. Acesso em: 23 ago. 2026. (B)
- DEEPSEEK AI. *DeepSeek V3*. HuggingFace. Disponível em: https://huggingface.co/deepseek-ai/DeepSeek-V3. Acesso em: 23 ago. 2026. (B)
- TECH-INSIDER. *Best Open Source LLM 2026: DeepSeek, Kimi, Qwen Ranked*. Disponível em: https://tech-insider.org/best-open-source-llm-2026/. Acesso em: 23 ago. 2026. (C)
- HABR. *Inside DeepSeek Harness: Cordis, Session Events, Tool Pipelines*. Disponível em: https://habr.com/en/articles/1070958/. Acesso em: 23 ago. 2026. (B)
- MEDIUM (kaliarch). *DeepSeek Harness: When the Agent Loop Itself Becomes a Plugin*. Disponível em: https://medium.com/@kaliarch/deepseek-harness-when-the-agent-loop-itself-becomes-a-plugin-7fad0aa9de1c. Acesso em: 23 ago. 2026. (C)
- MINDSTUDIO. *What Is DeepSeek Harness? The Plug-In Coding Agent Explained*. Disponível em: https://www.mindstudio.ai/blog/deepseek-harness-agentic-coding. Acesso em: 23 ago. 2026. (C)
- MINDSTUDIO. *How to Install and Set Up DeepSeek Harness Locally*. Disponível em: https://www.mindstudio.ai/blog/how-to-set-up-deepseek-harness. Acesso em: 23 ago. 2026. (C)
- DATACAMP. *DeepSeek Harness Tutorial: Set Up the Open-Source Agent*. Disponível em: https://www.datacamp.com/tutorial/deepseek-harness. Acesso em: 23 ago. 2026. (C)
- THE NEW STACK. *DeepSeek open sources an agent harness where everything is a plugin*. Disponível em: https://thenewstack.io/deepseek-harness-open-source-plugins/. Acesso em: 23 ago. 2026. (C)
- 0XSLINE. *awesome-deepseek-harness*. GitHub. Disponível em: https://github.com/0xsline/awesome-deepseek-harness. Acesso em: 23 ago. 2026. (B)
- KIE.AI. *What Is DeepSeek Harness? V4 Agent Framework*. Disponível em: https://kie.ai/blog/what-is-deepseek-harness. Acesso em: 23 ago. 2026. (C)
- FLOATBOAT.AI. *Cordis — The Plugin Kernel Behind DeepSeek Harness*. Disponível em: https://floatboat.ai/blog/cordis-plugin-framework. Acesso em: 23 ago. 2026. (C)
- AGENTATLAS. *Cordis Explained: How DeepSeek Harness's Plugin Framework Works*. Disponível em: https://agentatlas.org/blog/cordis-explained-how-deepseek-harness-plugin-framework-works/. Acesso em: 23 ago. 2026. (C)
- MEDIUM (data-and-beyond). *Decoding DeepSeek Harness: The Open-Source Runtime Behind Composable AI Agents*. Disponível em: https://medium.com/data-and-beyond/decoding-deepseek-harness-the-open-source-runtime-behind-composable-ai-agents-c2299e992870. Acesso em: 23 ago. 2026. (C)
- TOWARDS AI. *DeepSeek Harness vs Claude Code: A Plugin Architecture Teardown*. Disponível em: https://pub.towardsai.net/deepseek-harness-vs-claude-code-a-plugin-architecture-teardown-da3c916f3af1. Acesso em: 23 ago. 2026. (C)
- TOWARDS AI. *DeepSeek Harness Explained: When the AI Model is Just a Plugin*. Disponível em: https://pub.towardsai.net/deepseek-harness-explained-when-the-ai-model-is-just-a-plugin-16b2496f3d01. Acesso em: 23 ago. 2026. (C)
- ZIMASPACE. *DeepSeek Harness Modes: Standard vs Code vs Minimal vs Creator*. Disponível em: https://shop.zimaspace.com/blogs/tech-ai-hub/de-minimal-and-creator-explained. Acesso em: 23 ago. 2026. (C)
- SITEPOINT. *DeepSeek R1 Local Deployment: Complete Guide 2026*. Disponível em: https://www.sitepoint.com/deepseek-r1-local-deployment-guide-2026/. Acesso em: 23 ago. 2026. (C)
- GOOGLE CLOUD. *DeepSeek R1: Ollama vs. vLLM on GKE*. Disponível em: https://medium.com/google-cloud/deepseek-r1-unleashed-gke-ollama-and-vllm-deep-dive-1b707eeca26f. Acesso em: 23 ago. 2026. (C)
- DEV.TO. *A Step-by-Step Guide to Install DeepSeek-R1 Locally*. Disponível em: https://dev.to/nodeshiftcloud/a-step-by-step-guide-to-install-deepseek-r1-locally-with-ollama-vllm-or-transformers-44a1. Acesso em: 23 ago. 2026. (C)
- REDDIT (LocalLLaMA). *Ollama + Open WebUI with Docker Compose*. Disponível em: https://www.reddit.com/r/LocalLLM/comments/1thdu3e/. Acesso em: 23 ago. 2026. (C)
- THE OBJECTIVE DAD. *Running DeepSeek R1 at Home*. Disponível em: https://www.theobjectivedad.com/pub/20250205-deepseek-homelab/index.html. Acesso em: 23 ago. 2026. (C)
- DATAQUBED. *Deploying DeepSeek-R1 Locally with vLLM on Ubuntu*. Disponível em: https://dataqubed.io/deploying-deepseek-r1-locally-with-vllm-on-ubuntu/. Acesso em: 23 ago. 2026. (C)
- COMPOSIO. *Best plugins for DeepSeek Harness every developer*. Disponível em: https://composio.dev/content/best-deepseek-harness-plugins. Acesso em: 23 ago. 2026. (C)
- ATLASCLOUD. *DeepSeek Harness Plugins: The 7 Worth It*. Disponível em: https://www.atlascloud.ai/blog/tips/deepseek-harness-plugins. Acesso em: 23 ago. 2026. (C)
- ATLASCLOUD. *How to Install DeepSeek Harness in 10 Minutes*. Disponível em: https://www.atlascloud.ai/blog/tips/how-to-install-deepseek-harness. Acesso em: 23 ago. 2026. (C)
- COMETAPI. *6 Methods to Deploy DeepSeek Harness Locally*. Disponível em: https://www.cometapi.com/how-to-install-and-deploy-deepseek-harness-locally/. Acesso em: 23 ago. 2026. (C)
- CLOUDSWAY. *DeepSeek Harness Tutorial: Architecture and Quick Start*. Disponível em: https://www.cloudsway.ai/resources/deepseek-harness-tutorial-architecture-and-quick-start. Acesso em: 23 ago. 2026. (C)
- MEDIUM (codetodeploy). *Explored DeepSeek Harness: How a Plugin-Native Agent Runtime Actually Works*. Disponível em: https://medium.com/codetodeploy/explored-deepseek-harness-how-a-plugin-native-agent-runtime-actually-works-7b815436a6b3. Acesso em: 23 ago. 2026. (C)
- LINKEDIN (Cole Medin). *DeepSeek Coding Agent Harness Offers Customizable Plugins*. Disponível em: https://www.linkedin.com/posts/cole-medin-727752184_deepseek-built-a-coding-agent-harness-last-activity-7495993045192998912-574a. Acesso em: 23 ago. 2026. (C)
- LINKEDIN (Richard Van Ngo Tran). *DeepSeek Harness v0.1 Released: Cordis Powered Plugin*. Disponível em: https://www.linkedin.com/posts/richard-van-ngo-tran-8095441a4_deepseek-harness-v01-is-now-available-in-activity-7493832260652228608-E39a. Acesso em: 23 ago. 2026. (C)
- RED HAT. *llama.cpp vs. vLLM: Choosing the right local LLM inference engine*. Disponível em: https://developers.redhat.com/articles/2026/06/15/llamacpp-vs-vllm-choosing-right-local-llm-inference-engine. Acesso em: 23 ago. 2026. (B)
- SITEPOINT. *Ollama vs vLLM: Performance Benchmark 2026*. Disponível em: https://www.sitepoint.com/ollama-vs-vllm-performance-benchmark-2026/. Acesso em: 23 ago. 2026. (C)
- WORLDLINE. *The Ultimate LLM Inference Battle, vLLM vs. Ollama vs. ZML*. Disponível em: https://blog.worldline.tech/2026/01/29/llm-inference-battle.html. Acesso em: 23 ago. 2026. (C)
- TOWARDS AI. *I Tested GGUF vs AWQ vs GPTQ: The "Fastest" 4-Bit*. Disponível em: https://pub.towardsai.net/i-tested-gguf-vs-awq-vs-gptq-the-fastest-4-bit-collapses-on-code-at-46-d65c271d7cdf. Acesso em: 23 ago. 2026. (C)
- LYCEUM.technology. *GGUF vs GPTQ vs AWQ: 2026 LLM Quantization Guide*. Disponível em: https://lyceum.technology/magazine/gguf-vs-gptq-vs-awq-quantization/. Acesso em: 23 ago. 2026. (C)
- SESAMEDISK. *Quantization Techniques for AI Inference in 2026*. Disponível em: https://sesamedisk.com/quantization-techniques-ai-inference-2026/. Acesso em: 23 ago. 2026. (C)
- LOCALAIMASTER. *GGUF vs GPTQ vs AWQ 2026*. Disponível em: https://localaimaster.com/blog/quantization-explained. Acesso em: 23 ago. 2026. (C)
- FIRECRAWL. *Best Vector Databases in 2026: A Complete Comparison*. Disponível em: https://www.firecrawl.dev/blog/best-vector-databases. Acesso em: 23 ago. 2026. (C)
- KUNALGANGLANI. *Weaviate vs Chroma 2026: Production Power or Local-First*. Disponível em: https://www.kunalganglani.com/blog/weaviate-vs-chroma-vector-db. Acesso em: 23 ago. 2026. (C)
- BRAINTRUST. *Best vector databases for RAG in 2026*. Disponível em: https://www.braintrust.dev/articles/best-vector-databases-for-rag-2026. Acesso em: 23 ago. 2026. (C)
- CODERFILE. *Fine-Tuning Local LLMs for Code Generation: A 2026 Guide*. Disponível em: https://coderfile.io/blog/local-llm-fine-tuning-code-2026. Acesso em: 23 ago. 2026. (C)
- FUTURE AGI. *Fine-Tuning LLMs 2026: LoRA, QLoRA, DPO, GRPO*. Disponível em: https://futureagi.com/blog/fine-tuning-llms-unlocking-peak-performance/. Acesso em: 23 ago. 2026. (C)
- TECH-INSIDER. *How to Fine-Tune an LLM: 13 Steps, 90 Min [2026]*. Disponível em: https://tech-insider.org/how-to-fine-tune-an-llm-2026/. Acesso em: 23 ago. 2026. (C)
- CODERSERA. *Fine-Tuning LLMs in 2026: LoRA, QLoRA, Unsloth, MLX*. Disponível em: https://codersera.com/blog/fine-tuning-llms-complete-guide-2026/. Acesso em: 23 ago. 2026. (C)
- AIRBYTE. *How to Train an LLM on Your Own Data (2026 Guide)*. Disponível em: https://airbyte.com/data-engineering-resources/how-to-train-llm-with-your-own-data. Acesso em: 23 ago. 2026. (C)
- ZYLOS.AI. *Open-Source LLM Fine-Tuning and Serving Infrastructure*. Disponível em: https://zylos.ai/research/2026-03-22-open-source-llm-fine-tuning-serving-ai-agent-platforms/. Acesso em: 23 ago. 2026. (C)
- EFFLOOW. *Fine-Tune LLMs with LoRA and QLoRA: 2026 Guide*. Disponível em: https://effloow.com/articles/llm-fine-tuning-lora-qlora-guide-2026. Acesso em: 23 ago. 2026. (C)
- MINDSTUDIO. *Git Worktrees for AI Coding: How to Run Multiple Agents Without Conflicts*. Disponível em: https://www.mindstudio.ai/blog/git-worktrees-parallel-ai-coding-agents. Acesso em: 23 ago. 2026. (C)
- AUGMENT CODE. *How to Use Git Worktrees for Parallel AI Agent Execution*. Disponível em: https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution. Acesso em: 23 ago. 2026. (C)
- UPSUN. *Git worktrees for parallel AI coding agents*. Disponível em: https://developer.upsun.com/posts/ai/git-worktrees-for-parallel-ai-coding-agents. Acesso em: 23 ago. 2026. (C)
- HIVENET. *DeepSeek-R1 Model Sizes and RAM Requirements*. Disponível em: https://www.hivenet.com/post/deepseek-r1-model-sizes-ram-vram-requirements. Acesso em: 23 ago. 2026. (C)
- APXML. *GPU System Requirements for Running DeepSeek-R1*. Disponível em: https://apxml.com/posts/gpu-requirements-deepseek-r1. Acesso em: 23 ago. 2026. (C)
- DEV.TO (AI4B). *Comprehensive Hardware Requirements Report for DeepSeek-R1*. Disponível em: https://dev.to/ai4b/comprehensive-hardware-requirements-report-for-deepseek-r1-5269. Acesso em: 23 ago. 2026. (C)
- VERDENT.AI. *DeepSeek Harness Installation: How to Run dsh*. Disponível em: https://www.verdent.ai/guides/agents/install-deepseek-harness-dsh. Acesso em: 23 ago. 2026. (C)
- SPRINGBRAND. *DeepSeek Harness (dsh): Everything Is a Plugin*. Disponível em: https://springbrand.ai/deepseek-harness. Acesso em: 23 ago. 2026. (C)
- I-SCOOP. *DeepSeek Harness turns every part of an agent runtime into a swappable plugin*. Disponível em: https://www.i-scoop.eu/deepseek-harness-turns-every-part-of-an-agent-runtime-into-a-swappable-plugin/. Acesso em: 23 ago. 2026. (C)
- SKYWORK. *DeepSeek V4 Local Deployment: A Comprehensive Guide*. Disponível em: https://skywork.ai/skypage/en/deepseek-local-deployment-guide/2047582806721294336. Acesso em: 23 ago. 2026. (C)
- REDDIT (r/DeepSeek). *Can you help me find the Best AI Harness for the New Deepseek V4?*. Disponível em: https://www.reddit.com/r/DeepSeek/comments/1vjkstg/. Acesso em: 23 ago. 2026. (C)
- ALEXEWERLOF. *Using local LLMs for agentic coding*. Disponível em: https://blog.alexewerlof.com/p/local-llms-for-agentic-coding. Acesso em: 23 ago. 2026. (C)
- MEDIUM (techlatest). *How to Install DeepSeek Harness: A Step-by-Step Setup Guide*. Disponível em: https://medium.com/@techlatest.net/how-to-install-deepseek-harness-a-step-by-step-setup-guide-for-developers-9bedadfb584d. Acesso em: 23 ago. 2026. (C)
- XCLOUD. *DeepSeek Harness vs OpenClaw vs Hermes Agent*. Disponível em: https://xcloud.host/deepseek-harness-vs-openclaw-vs-hermes-agent. Acesso em: 23 ago. 2026. (C)
- LINKEDIN (Tony Ren). *DeepSeek Harness: Agent Operating System and Future of Multi-Agent Collaboration*. Disponível em: https://www.linkedin.com/posts/tonyren_i-spent-the-evening-in-the-deepseek-harness-activity-7493848102076882944-GGXB. Acesso em: 23 ago. 2026. (C)
- DEEPSEEKHARNESSAI. *Security Plugins for DeepSeek Harness*. Disponível em: https://deepseekharnessai.com/categories/security. Acesso em: 23 ago. 2026. (B)
- EXPLOREX.AI. *DeepSeek Harness v0.1: Run the Plugin-First Agent Stack*. Disponível em: https://explainx.ai/blog/deepseek-harness-v0-1-plugin-first-agent-stack-august-2026. Acesso em: 23 ago. 2026. (C)
- MARKTECHPOST. *DeepSeek AI Releases DeepSeek Harness in Developer Preview*. Disponível em: https://www.marktechpost.com/2026/08/17/deepseek-ai-releases-deepseek-harness-in-developer-preview/. Acesso em: 23 ago. 2026. (C)
- THEREGISTER. *DeepSeek's innovative harness treats everything as a plug-in*. Disponível em: https://www.theregister.com/ai-and-ml/2026/08/14/deepseeks-innovative-harness-treats-everything-as-a-plug-in/5288095. Acesso em: 23 ago. 2026. (C)
- DAI, Jing. *DeepSeek in Action*. CRC Press, 2025. Disponível em: https://doi.org/10.1201/9781003674702. Acesso em: 23 ago. 2026. (A)
- DAI, Jing. *The DeepSeek Prompt Library*. In: DeepSeek in Action. 2025. Disponível em: https://doi.org/10.1201/9781003674702-11. Acesso em: 23 ago. 2026. (A)
- DAI, Jing. *Integration Practice 1*. In: DeepSeek in Action. 2025. Disponível em: https://doi.org/10.1201/9781003674702-13. Acesso em: 23 ago. 2026. (A)
- DAI, Jing. *Integration Hands-on 2*. In: DeepSeek in Action. 2025. Disponível em: https://doi.org/10.1201/9781003674702-14. Acesso em: 23 ago. 2026. (A)
- DAI, Jing. *Integration Practice 3*. In: DeepSeek in Action. 2025. Disponível em: https://doi.org/10.1201/9781003674702-15. Acesso em: 23 ago. 2026. (A)
- DAI, Jing. *Callback Functions and Contextual Disk Caching*. In: DeepSeek in Action. 2025. Disponível em: https://doi.org/10.1201/9781003674702-10. Acesso em: 23 ago. 2026. (A)
- FERRAG, Mohamed Amine; TIHANYI, Norbert; DEBBAH, Mérouane. *From LLM Reasoning to Autonomous AI Agents: A Comprehensive Review*. In: IEEE Access, 2026. Disponível em: https://doi.org/10.1109/access.2026.3698694. Acesso em: 23 ago. 2026. (A)
- ARRIETA, Aitor et al. *o3-mini vs DeepSeek-R1: Which One is Safer?*. In: arXiv, 2025. Disponível em: http://arxiv.org/abs/2501.18438. Acesso em: 23 ago. 2026. (A)
- ZHANG, Jie et al. *When LLMs Meet Cybersecurity: A Systematic Literature Review*. In: arXiv, 2024. Disponível em: http://arxiv.org/abs/2405.03644. Acesso em: 23 ago. 2026. (A)
- XU, Mengwei et al. *A Survey of Resource-efficient LLM and Multimodal Foundation Models*. In: arXiv, 2024. Disponível em: http://arxiv.org/abs/2401.08092. Acesso em: 23 ago. 2026. (A)
- KOURANI, Humam et al. *Evaluating large language models on business process modeling*. In: Software & Systems Modeling, 2025. Disponível em: https://doi.org/10.1007/s10270-025-01318-w. Acesso em: 23 ago. 2026. (A)
- WONG, Wai Kin et al. *DecLLM: LLM-Augmented Recompilable Decompilation*. In: Proceedings of the ACM on Software Engineering, 2025. Disponível em: https://doi.org/10.1145/3728958. Acesso em: 23 ago. 2026. (A)
- GU, Yufeng et al. *PIM Is All You Need: A CXL-Enabled GPU-Free System for LLM Inference*. In: ACM, 2025. Disponível em: https://doi.org/10.1145/3676641.3716267. Acesso em: 23 ago. 2026. (A)
- DELGADO-SÁNCHEZ, Elsa; CALDERÓN, Reyes; HERRERA, Francisco. *Artificial Intelligence Adoption in SMEs*. In: Applied Sciences, 2025. Disponível em: https://doi.org/10.3390/app15126465. Acesso em: 23 ago. 2026. (A)
- BLAŠKOVIĆ, Luka et al. *Robust Clinical Querying with Local LLMs*. In: Big Data and Cognitive Computing, 2025. Disponível em: https://doi.org/10.3390/bdcc9100256. Acesso em: 23 ago. 2026. (A)
