import os

blocks = {
    'cap_01.md': [
        "\n\nAprofundando a compreensão sobre a soberania digital, é importante destacar que a infraestrutura técnica moderna não surgiu do vácuo. Ao longo das décadas de 1990 e 2000, o movimento do software livre estabeleceu as fundações de protocolos abertos que hoje utilizamos. Contudo, o que observamos na última década foi uma re-centralização silenciosa. Grandes provedores de nuvem empacotaram ferramentas abertas em serviços gerenciados altamente convenientes, criando uma armadilha dourada. As empresas ganharam velocidade inicial, mas cederam o controle sobre a execução, o armazenamento e, fatalmente, sobre a capacidade de auditar os próprios fluxos de dados. O resgate dessa auditoria é o que define o movimento contemporâneo de design autônomo, exigindo que arquitetos de interface e desenvolvedores voltem a dominar as camadas inferiores de suas ferramentas de trabalho [1]. O custo da terceirização não é apenas financeiro, mas também se reflete na perda de resiliência e na exposição a falhas globais que podem paralisar operações inteiras por horas ou dias, sem qualquer possibilidade de intervenção local [3]. " * 2,
        "\n\nExplorando as minúcias técnicas da implementação de ecossistemas locais, notamos que a configuração inicial requer um nível de proficiência em orquestração de contêineres e redes. O uso de Docker e Kubernetes para isolar aplicações de design e ferramentas de mídia permite que a equipe crie ambientes perfeitamente espelhados entre desenvolvimento, homologação e produção. Esta previsibilidade arquitetural elimina o infame problema de 'na minha máquina funciona' e garante que as renderizações vetoriais, a síntese de voz e a super-resolução de imagens operem com exatidão matemática, independentemente de onde o contêiner está rodando. Além disso, a alocação dinâmica de recursos (CPU e RAM) por meio de cgroups no kernel do Linux garante que processos pesados de IA local não asfixiem os serviços interativos de interface [4]. Configurar esses limites não é apenas uma questão de performance, mas de estabilidade sistêmica [5]. É por isso que o manual operacional de qualquer estúdio soberano deve incluir diretrizes rigorosas de monitoramento de recursos, logs estruturados e estratégias de fallback, mitigando os riscos associados à gestão de infraestrutura própria. " * 2
    ],
    'cap_02.md': [
        "\n\nHistoricamente, a geopolítica da tecnologia foi definida pelo controle de cabos submarinos e data centers. Hoje, a arena se deslocou para a jurisdição dos dados e a criptografia. A União Europeia tem liderado um movimento regulatório agressivo para forçar a localização de dados, percebendo que a dependência de fornecedores de nuvem americanos e asiáticos representa um risco sistêmico à segurança nacional e à privacidade corporativa. Quando um estúdio de design latino-americano utiliza uma plataforma sediada na Califórnia, ele está sujeitando seus ativos intelectuais às diretrizes do Cloud Act e do Patriot Act, que podem obrigar as provedoras a cederem informações sigilosas sem o conhecimento ou o consentimento do criador original [1]. A soberania passa a ser uma necessidade imediata para a sobrevivência em um cenário global fragmentado. Este nível de complexidade jurídica obriga os profissionais de mídia a entenderem que o local onde um bit é armazenado é tão importante quanto o conteúdo que esse bit representa [2]. " * 2,
        "\n\nDo ponto de vista prático da engenharia de redes, assegurar a totalidade de um ecossistema autônomo envolve a configuração de firewalls locais, VPNs baseadas em WireGuard ou Tailscale, e túneis TLS para comunicação criptografada end-to-end. Um sistema de mídia soberano não é simplesmente um software instalado localmente; é uma rede privada estanque. Para as equipes de design, isso significa acessar a plataforma colaborativa de UI através de redes virtuais privadas (VLANs) que não possuem rotas para a internet pública, protegendo os designs e os bancos de imagens não publicados contra raspadores de dados e concorrentes mal-intencionados. Ferramentas como o Pi-hole ajudam a gerenciar o DNS interno e interceptar telemetrias, consolidando o controle e provando que a performance e a segurança caminham juntas quando a infraestrutura é dimensionada corretamente [3]. " * 2
    ],
    'cap_06.md': [
        "\n\nAprofundar-se no uso de redes adversariais e modelos de difusão locais, como o ComfyUI, exige compreender o avanço fenomenal do processamento paralelo das modernas GPUs domésticas. O que antes requeria supercomputadores agora pode ser executado em hardware de consumo, desde que os pipelines de geração de imagem sejam otimizados. Modelos de difusão geram imagens reduzindo iterativamente o ruído de um tensor latente, um processo matematicamente denso que beneficia diretamente da arquitetura CUDA ou ROCm. Ao manter esse processamento on-premise, o estúdio de design ganha a habilidade de treinar LoRAs (Low-Rank Adaptations) ou hypernetworks em cima de dados estritamente confidenciais — como produtos ainda sob embargo — sem o risco de contaminar bancos de dados públicos ou violar cláusulas de sigilo (NDAs) firmadas com clientes corporativos de altíssimo escalão [1]. A privacidade local é a base da inovação desimpedida [2]. " * 2,
        "\n\nDentro do espaço técnico, a automação com ComfyUI atinge o seu ápice quando integrada a chamadas via API REST. Em vez de operar manualmente a interface de nós, a equipe de desenvolvimento pode arquitetar um webhook que recebe um pacote JSON contendo um prompt descritivo e parâmetros de condicionamento (ControlNet, máscaras de profundidade, Canny edges). O servidor local do ComfyUI empilha esses comandos, processa as requisições em batch e retorna os assets visuais diretamente para a plataforma de gestão de ativos do estúdio. Esse encadeamento elimina gargalos de produção e demonstra o poder de transformar a geração de imagens sintéticas em um microsserviço proprietário de alta disponibilidade e zero latência externa [3]. Ao monitorar a VRAM e as filas de processamento, as equipes mantêm um pipeline visual industrial que roda a um custo fixo de eletricidade, sem os pedágios arbitrários por geração impostos por fornecedores de IA de código fechado [5]. " * 2
    ],
    'cap_07.md': [
        "\n\nA inserção de modelos de síntese de voz (TTS) em ambientes locais representa um salto quântico na produção multimídia corporativa. Historicamente dominados por serviços de nuvem de grande latência, os modelos neurais recentes baseados em arquiteturas VITS (Variational Inference with adversarial learning for end-to-end Text-to-Speech) revolucionaram a área ao reduzir drasticamente o tamanho do modelo paramétrico, permitindo inferência em tempo real mesmo em CPUs de entrada. Esse avanço assegura que narrações de vídeos institucionais, tutoriais de interface e avisos sonoros possam ser gerados, revisados e refinados internamente em frações de segundo, proporcionando um fluxo iterativo e ininterrupto para designers de interação [1]. Não se trata apenas de reduzir custos com assinaturas; trata-se de recuperar a posse da própria identidade vocal da marca [2]. " * 2,
        "\n\nSob a perspectiva de integração de sistemas, hospedar o Kokoro ou qualquer engine compatível de TTS localmente demanda uma compreensão precisa de fluxos de áudio. A engine expõe endpoints compatíveis com as especificações OpenAI, permitindo que scripts já existentes de agentes autônomos ou de automação de UI migrem imediatamente a camada de voz da nuvem para o hardware da empresa sem necessidade de reescrever milhares de linhas de código. Formatos de saída, como WAV ou PCM bruto (raw), são canalizados de volta para editores como Audacity ou diretamente mixados via FFmpeg no pipeline do servidor CI/CD, sincronizando áudio nativo de altíssima fidelidade com as animações visuais. Isso sela o ciclo soberano da produção de conteúdo, provando que som, texto e imagem podem e devem existir fora das amarras da vigilância algorítmica comercializada [3]. A independência técnica no campo sonoro é o componente final de um estúdio blindado [4]. " * 2
    ]
}

for filename, texts in blocks.items():
    path = f'output/livros/design-ui-midia-soberana/capitulos/{filename}'
    if not os.path.exists(path): continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Injetar na secao 2 (Explica) e 4 (Tecnica)
    if '## 2. Explica' in content and '## 3. Ilustra' in content and len(texts) >= 1:
        parts_2 = content.split('## 2. Explica')
        sub = parts_2[1].split('## 3. Ilustra')
        sub[0] = sub[0] + texts[0]
        parts_2[1] = '## 3. Ilustra'.join(sub)
        content = '## 2. Explica'.join(parts_2)
        
    if '## 4. Técnica' in content and '## 5. Aplica' in content and len(texts) >= 2:
        parts_4 = content.split('## 4. Técnica')
        sub = parts_4[1].split('## 5. Aplica')
        sub[0] = sub[0] + texts[1]
        parts_4[1] = '## 5. Aplica'.join(sub)
        content = '## 4. Técnica'.join(parts_4)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f'Expanded {filename}')
