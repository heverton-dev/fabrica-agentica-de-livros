# Dossiê de Pesquisa — Design, UI, Mídia Soberana e Upscaling Local

## Conceitos-chave
- **Mídia soberana (soberania digital):** capacidade de um indivíduo, empresa ou Estado de produzir, processar, armazenar e utilizar dados e mídias sem depender, de forma crítica, de infraestrutura, plataformas ou cadeias de suprimento sediadas fora de sua jurisdição.  
- **Upscaling local (super-resolução):** processo de ampliar resolução de imagem preservando bordas, texturas e legibilidade, executado em hardware local em vez de serviços em nuvem.  
- **Edição vetorial:** criação de gráficos por primitivas matemáticas (Bézier, caminhos, polígonos), permitindo escala infinita sem perda.  
- **Síntese de voz (TTS):** geração computacional de fala a partir de texto; em ambientes soberanos, prefere-se modelos locais (ex.: baseados em VITS).  
- **Edição de PDF self-hosted:** mesclar, dividir, comprimir, assinar e transformar PDFs sem enviar arquivos a serviços externos.  
- **Geração de imagens com IA local:** fluxos (Stable Diffusion/Flux/SDXL) rodando em workstation, evitando envio de prompts e dados para APIs públicas.  
- **Quadro branco colaborativo:** canvas infinito para wireframes, diagramas e ETC, preferencialmente com colaboração E2E e auto-hospedagem.  
- **Framework de ícones:** biblioteca vetorial de símbolos padronizados (estrofes, grid,WCAG), com tree-shaking e pacotes por framework.  
- **Fontes auto-hospedadas:** conjuntos tipográficos servidos do próprio domínio/Aplicação, evitando depender de CDNs externos e garantindo bloqueio de rastreadores.

## Artigos Científicos e Papers
- LEDIG, Christian et al. *Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network*. In: CVPR, 2017. Disponível em: https://arxiv.org/abs/1609.04802. Acesso em: 25 ago. 2026. (A)
- WANG, Xintao et al. *ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks*. In: ECCV 2018 Workshop. Disponível em: https://arxiv.org/abs/1809.00219. Acesso em: 25 ago. 2026. (A)
- WANG, Xintao et al. *Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data*. In: ICCVW, 2021. Disponível em: https://arxiv.org/abs/2107.10833. Acesso em: 25 ago. 2026. (A)
- HO, Jonathan; JAIN, Ajay; ABBEEL, Pieter. *Denoising Diffusion Probabilistic Models*. In: NeurIPS, 2020. Disponível em: https://arxiv.org/abs/2006.11239. Acesso em: 25 ago. 2026. (A)
- ROMBACH, Robin et al. *High-Resolution Image Synthesis with Latent Diffusion Models*. In: CVPR, 2022. Disponível em: https://arxiv.org/abs/2112.10752. Acesso em: 25 ago. 2026. (A)
- KIM, Jaehyeon; KONG, Jungil; SON, Juhee. *Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech*. In: ICML, 2021. Disponível em: https://arxiv.org/abs/2106.06103. Acesso em: 25 ago. 2026. (A)
- LIANG, Jingyun et al. *SwinIR: Image Restoration Using Swin Transformer*. In: CVPRW, 2022. Disponível em: https://arxiv.org/abs/2108.10257. Acesso em: 25 ago. 2026. (A)

## Estado da arte / ferramentas de referência
### Upscaling local
- **Real-ESRGAN:** família open-source com portabilidade via NCNN/Vulkan; forte em imagens reais, com modelos para anime e vídeos. Amplamente integrada em GUIs e ferramentas. (B)
- **ESRGAN/Real-ESRGAN-ncnn-vulkan:** caminho de execução leve para desktops sem stack pesado de Python, viabilizando upscale local em CPUs/GPUs não NVIDIA. (B)
- **Upscayl:** frontend desktop multiplataforma que orquestra Real-ESRGAN/ncnn com foco em usabilidade; exige GPU Vulkan e é forte candidato a “caso soberano” de ponta. (B)
- **SwinIR:** arquitetura transformer para restauração de imagem com ganhos consistentes em SR, denoising e compressão; boa alternativa quando se busca máxima qualidade. (A)

### Síntese de voz (TTS)
- **Piper (rhasspy/piper):** engine TTS local e rápida; repositório original arquivado e sucedido por **piper1-gpl** (Open Home Foundation), focado em executáveis e modelos locais. (B)
- **piper1-gpl:** sucessor de Piper, foco em inferência local, multi-idoma e integração com assistentes pessoais e apps offline. (B)
- **Coqui TTS / XTTS:** alternativa relevante para clonagem e síntese de voz local, com modelos que permitem operação sem dependência externa. (B)

### Design vetorial e plataformas abertas
- **Inkscape:** editor SVG/GPL para ilustração técnica e artística; exporta SVG/PDF/PNG e é referência em fluxo vetorial aberto. (B)
- **Penpot:** plataforma aberta de design/UI com colaboração, design tokens, CSS Grid/Flex e auto-hospedagem; já é referência soberana para times de produto. (B)

### Edição/manipulação de PDF
- **Stirling-PDF:** plataforma open-core auto-hospedável com interface web, API e dezenas de operações de PDF; forte candidata a substituir serviços SaaS de edição. (B)
- **qpdf:** ferramenta de baixo nível para transformação estrutural de PDF (linearização, criptografia, merge/split); útil como camada programática e determinística. (B)
- **Poppler / pdf.js:** camadas complementares de renderização e extração de PDF para integrar em soluções próprias. (B)

### Geração de imagens com IA local
- **ComfyUI:** engine modular de nós para Stable Diffusion/Flux/SDXL, com forte foco em pipelines reproduzíveis e execução local; referência para estúdios que querem controle técnico. (B)
- **AUTOMATIC1111 (stable-diffusion-webui):** interface amplamente adotada para geração local, com suporte a upscalers (Real-ESRGAN, SwinIR) e modo offline. (B)

### Quadros brancos colaborativos
- **Excalidraw:** whiteboard com estilo sketch, colaboração e criptografia ponta-a-ponta; MIT e forte ecossistema de integrações. (B)

### Ícones e fontes
- **Lucide:** biblioteca de ícones SVG leve, com tree-shaking e pacotes por framework; substitui Feather com escopo maior. (B)
- **Fontsource:** coleção de fontes open-source auto-hospedáveis via pacotes NPM, foco em performance, privacidade e versionamento local. (B)
- **Open Font License / SIL OFL:** base normativa que sustenta ecossistema de fontes abertas para uso e modificação. (A)

### Normas e mercados
- **SVG 2 (W3C):** especificação de gráficos vetoriais escaláveis para web e ferramentas, permitindo interoperabilidade aberta. (A)
- **ISO 32000-2 (PDF 2.0):** referência internacional que consolida especificações modernas de PDF. (A)
- **Estratégia de dados da UE:** marco público de soberania digital, abordando governança, compartilhamento e soberania sobre dados. (B)

## Casos de uso corporativos
- **Editoras e produtores de conteúdo:** uso de Upscayl/Real-ESRGAN para revitalizar banco de imagens de baixa resolução sem enviar ativos para cloud. (B)
- **Times de produto/design:** adoção de Penpot + Excalidraw + Lucide como stack soberana de design, prototipação e bibloteca de componentes. (B)
- **Automatizações de documentos:** Stirling-PDF e qpdf integrados a intranets para merge, assinatura e redaction de contratos sem passar por APIs externas. (B)
- **Estúdios de IA generativa local:** ComfyUI e sd-webui como backbones de pipelines internos de conceito art, licensing de estilo e controle de IP. (B)
- **Assistentes de voz corporativos:** Piper/piper1-gpl em dispositivos de atendimento ou kiosks, mantendo dados de voz e texto no ambiente local. (B)

## Limitações e controvérsias
- **Upscaling local:** exige hardware compatível (GPU/VRAM) e pode gerar bloqueios/tile artifacts; modelos podem suavizar textura se mal calibrados. (B)
- **IA generativa local:** alto custo de hardware, mobilidade limitada e manutenção contínua de dependências e drivers. (A)
- **Penpot vs Figma:** divergência de ecossistema e maturidade de plugins; migração pode exigir rework em ativos proprietários. (B)
- **Piper:** projeto original arquivado; adoção requer atenção a versões e mantenedores (piper1-gpl). (B)
- **Stirling-PDF:** projeto open-core; funcionalidades avanzadas podem exigir planos pagos ou configurações específicas. (B)
- **Soberania digital:** depender 100% de stack local pode reduzir agilidade e acesso a modelos最新; a estratégia ideal é soberania + interop controlada. (A)

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)
- WANG, Xintao; XIE, Liangbin; DONG, Chao; SHAN, Ying. *Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data*. Disponível em: https://arxiv.org/abs/2107.10833. Acesso em: 25 ago. 2026. (A)
- WANG, Xintao et al. *ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks*. Disponível em: https://arxiv.org/abs/1809.00219. Acesso em: 25 ago. 2026. (A)
- LEDIG, Christian et al. *Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network*. Disponível em: https://arxiv.org/abs/1609.04802. Acesso em: 25 ago. 2026. (A)
- HO, Jonathan; JAIN, Ajay; ABBEEL, Pieter. *Denoising Diffusion Probabilistic Models*. Disponível em: https://arxiv.org/abs/2006.11239. Acesso em: 25 ago. 2026. (A)
- ROMBACH, Robin et al. *High-Resolution Image Synthesis with Latent Diffusion Models*. Disponível em: https://arxiv.org/abs/2112.10752. Acesso em: 25 ago. 2026. (A)
- KIM, Jaehyeon; KONG, Jungil; SON, Juhee. *Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech*. Disponível em: https://arxiv.org/abs/2106.06103. Acesso em: 25 ago. 2026. (A)
- LIANG, Jingyun et al. *SwinIR: Image Restoration Using Swin Transformer*. Disponível em: https://arxiv.org/abs/2108.10257. Acesso em: 25 ago. 2026. (A)
- REAL-ESRGAN. *Real-ESRGAN*. Disponível em: https://github.com/xinntao/Real-ESRGAN. Acesso em: 25 ago. 2026. (B)
- UPSCAYL. *Upscayl*. Disponível em: https://github.com/upscayl/upscayl. Acesso em: 25 ago. 2026. (B)
- OHF-VOICE. *piper1-gpl*. Disponível em: https://github.com/OHF-Voice/piper1-gpl. Acesso em: 25 ago. 2026. (B)
- COMFY-ORG. *ComfyUI*. Disponível em: https://github.com/Comfy-Org/ComfyUI. Acesso em: 25 ago. 2026. (B)
- AUTOMATIC1111. *Stable Diffusion web UI*. Disponível em: https://github.com/AUTOMATIC1111/stable-diffusion-webui. Acesso em: 25 ago. 2026. (B)
- EXCALIDRAW. *Excalidraw*. Disponível em: https://github.com/excalidraw/excalidraw. Acesso em: 25 ago. 2026. (B)
- INKSCAPE. *Inkscape Overview*. Disponível em: https://inkscape.org/about/. Acesso em: 25 ago. 2026. (B)
- STIRLING-TOOLS. *Stirling PDF*. Disponível em: https://github.com/Stirling-Tools/Stirling-PDF. Acesso em: 25 ago. 2026. (B)
- QPDF. *qpdf*. Disponível em: https://github.com/qpdf/qpdf. Acesso em: 25 ago. 2026. (B)
- PENPOT. *Penpot*. Disponível em: https://github.com/penpot/penpot. Acesso em: 25 ago. 2026. (B)
- LUCIDE. *What is Lucide?*. Disponível em: https://lucide.dev/guide/. Acesso em: 25 ago. 2026. (B)
- FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026. (B)
- W3C. *Scalable Vector Graphics (SVG) 2*. Disponível em: https://www.w3.org/TR/SVG2/. Acesso em: 25 ago. 2026. (A)
- EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026. (A)
- R, Dr. PADMANABAN. *Speech Cloning: Text-To-Speech Using VITS*. Disponível em: https://doi.org/10.47191/etj/v9i05.10. Acesso em: 25 ago. 2026. (A)
- LĖVERIS, Vytautas; KORVEL, Gražina. *Investigation of VITS Text-to-Speech for the Lithuanian Language*. Disponível em: https://doi.org/10.15388/lmitt.2026.15. Acesso em: 25 ago. 2026. (A)
- PINE, Aidan et al. *Speech Generation for Indigenous Language Education*. Disponível em: https://doi.org/10.1016/j.csl.2024.101723. Acesso em: 25 ago. 2026. (A)
