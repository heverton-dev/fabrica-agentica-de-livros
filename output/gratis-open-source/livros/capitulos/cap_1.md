# Capítulo 1: Anotações e Produtividade: Saindo do Aluguel do Notion e do Evernote

## 1. Introdução

Toda oficina começa com a primeira ferramenta comprada — e para o Artesão Digital que está deixando de alugar software, essa primeira peça quase sempre é o lugar onde ele anota, organiza e planeja o próprio trabalho. Notion e Evernote resolveram isso tão bem, por tanto tempo, que a maioria de nós nunca parou para calcular quanto já pagou por eles em assinaturas mensais. Este capítulo existe para fazer essa conta e, em seguida, mostrar exatamente como substituir essa peça alugada por uma peça própria, montada e mantida na sua própria bancada.

Você vai aprender três coisas, nesta ordem: o que realmente muda — na prática, não na teoria — quando você troca uma ferramenta de anotações paga por uma auto-hospedada; como instalar e configurar as seis alternativas mais maduras do mercado (AppFlowy, Logseq, Joplin, Outline, Trilium Notes e Standard Notes); e onde essa troca ainda não vale a pena, para que você decida com os olhos abertos, não com fé em promessas de marketing. Ao final, você terá pelo menos uma ferramenta rodando na sua própria infraestrutura e um critério claro para repetir essa decisão em qualquer categoria de software que vier depois.

## 2. Explica

Comece pela pergunta que a maioria pula: o que exatamente você compra quando assina o Notion ou o Evernote? Não é o software — é o *acesso* ao software, hospedado em servidores que você nunca vê, com dados que ficam sob custódia de outra empresa, entregue enquanto o pagamento mensal continuar entrando. É o mesmo modelo de uma loja de aluguel de ferramentas: você paga para usar a furadeira, mas a furadeira nunca é sua, e no dia em que parar de pagar, ela some da sua bancada — no caso do software, "some" significa que sua conta é suspensa e seu acesso aos dados originais pode ficar condicionado a exportações limitadas ou a prazos de carência.

"Open source" resolve uma parte específica desse problema, e é importante ser preciso sobre qual parte. Código aberto significa que o código-fonte do programa está publicamente disponível para leitura, modificação e redistribuição, sob uma licença que garante esses direitos — o AppFlowy, por exemplo, é distribuído como projeto aberto sob termos que permitem exatamente isso [4], e o Logseq segue licença AGPL-3.0, que impõe até a obrigação de manter aberto qualquer serviço derivado que ofereça o software pela rede [13]. Isso é diferente de "gratuito": muita ferramenta gratuita não é aberta (você não pode ler nem alterar o código), e o inverso também existe — projeto aberto pode ter uma camada paga (suporte, hospedagem gerenciada) por cima do núcleo livre.

A segunda peça de vocabulário que você precisa é "self-hosted" versus "local-first". Self-hosted significa que você mesmo hospeda o servidor da aplicação — em uma VPS, num Raspberry Pi, num NAS doméstico — em vez de depender do servidor da empresa que criou o software. Local-first é uma escolha de arquitetura diferente e complementar: o aplicativo funciona primeiro a partir dos dados salvos localmente no seu dispositivo, com sincronização como recurso opcional por cima, não como dependência obrigatória para o programa nem abrir. Logseq, Trilium Notes e Standard Notes seguem essa filosofia local-first; AppFlowy e Outline são desenhados para rodar como serviço cloud-capable, mesmo quando você mesmo hospeda esse serviço [1][3].

Essa distinção importa porque ela determina onde o "custo do aluguel" reaparece depois que você troca de ferramenta. Ao trocar um serviço SaaS por uma alternativa auto-hospedada, você não elimina custo — você o transforma. Deixa de pagar uma mensalidade previsível e passa a pagar, em vez disso, com tempo de administração: manter o servidor no ar, aplicar atualizações de segurança, fazer backup, configurar domínio e certificado, e resolver o que quebrar tarde da noite numa sexta-feira. Esse padrão se repete em praticamente toda categoria de substituição SaaS por open source, e por isso ele abre este primeiro capítulo em vez de ficar escondido numa nota de rodapé.

## 3. Ilustra

Pense na diferença entre alugar uma furadeira numa loja de equipamentos e comprar a sua própria. Alugada, você paga por hora ou por dia, devolve limpa, e a loja é responsável por manutenção, calibração e substituição se ela quebrar — você nunca vê o motor por dentro. Comprada, a furadeira é sua para sempre: você decide quando usá-la, pode abri-la e trocar uma peça se quiser, e ninguém pode tirá-la de você por falta de pagamento. Mas agora *você* é quem precisa guardá-la em local seco, lubrificar as partes móveis e substituir a escova de carvão quando gastar. É exatamente essa troca que acontece quando você sai do Notion (a furadeira alugada, sempre pronta, sempre mantida por outra pessoa) para o AppFlowy auto-hospedado (a furadeira comprada, sua para sempre, mas sua responsabilidade).

Essa primeira analogia explica a mecânica geral — posse contra aluguel — mas ela ainda deixa escondido o ponto mais contraintuitivo da troca, que merece uma segunda lente. Pense agora não na furadeira em si, mas na *garantia* que vinha embutida no aluguel. Quando você aluga, a loja garante que a ferramenta funciona: se travar, eles trocam; se você não souber usar, eles orientam. Ao comprar sua própria peça para a bancada, essa garantia desaparece — e é substituída pela documentação do fabricante, pelo fórum da comunidade e pela sua própria capacidade de diagnosticar o problema. É exatamente o que acontece quando o Logseq trava ao abrir um grafo de notas grande demais: não existe suporte pago te chamando de volta, existe uma issue pública no rastreador do próprio projeto, ainda aberta, documentando exatamente esse limite de desempenho [12]. A "garantia" virou "transparência" — você vê o problema real, em vez de recebê-lo maquiado por trás de um SLA.

Como Artesão Digital, é essa segunda lente que você vai treinar ao longo de todo este livro: perguntar não apenas "essa peça própria funciona?", mas "que garantia eu perco ao trocar, e estou disposto a assumir essa responsabilidade sozinho?".

O diagrama abaixo resume o fluxo de decisão que guia o restante deste capítulo — da ferramenta alugada até a peça montada e funcionando na sua própria bancada.

```mermaid
%% legenda: Fluxo de decisão na Oficina Digital: da ferramenta alugada à peça própria montada na bancada
flowchart TB
  A[Ferramenta alugada: Notion ou Evernote] --> B{Colaboracao tempo real ou app mobile e critico?}
  B -->|Sim, indispensavel hoje| C[Mantenha o aluguel por enquanto]
  B -->|Nao, ou aceita o contorno| D[Escolha a peca para a bancada]
  D --> E[AppFlowy: tudo em um]
  D --> F[Logseq ou Trilium: notas locais]
  D --> G[Joplin: sync proprio]
  D --> H[Outline: wiki de equipe]
  D --> I[Standard Notes: seguranca auditada]
  E --> J[Monte via Docker Compose na sua VPS]
  F --> J
  G --> J
  H --> J
  I --> J
  J --> K[Peca propria: bancada, manutencao e garantia sao suas]
```

## 4. Técnica

Esta seção é onde a Oficina Digital sai do papel. Ela segue o padrão do material-fonte: configuração real em `docker-compose.yml`, sessões de terminal mostrando o comando e a saída esperada, e uma tabela de decisão ao final — sem código de programação, porque o que você precisa aqui é operar a ferramenta, não desenvolvê-la.

### Preparando a Bancada: Requisitos Antes de Montar Qualquer Peça

Antes de escolher qual alternativa instalar, verifique se a sua bancada tem a base mínima. A stack self-hosted completa do AppFlowy exige Docker Engine na versão 24.0 ou superior, Docker Compose na versão 2.20 ou superior, um domínio próprio configurado e no mínimo cinco serviços rodando em paralelo: banco de dados Postgres, cache Redis, armazenamento de objetos MinIO, autenticação GoTrue e a API principal [1][4]. Essa é a exigência mais pesada entre as seis ferramentas deste capítulo — o Outline pede uma pilha parecida (Node.js, Postgres 9.5 ou superior, Redis 4 ou superior e um bucket compatível com S3 como o MinIO para anexos) [15][14], enquanto Standard Notes, Joplin, Logseq e Trilium Notes rodam com bem menos.

Confirme a versão do Docker instalada antes de seguir:

```console
$ docker --version
Docker version 24.0.7, build afdd53b
$ docker compose version
Docker Compose version v2.23.0
```

Se a versão do seu servidor for anterior a essas, atualize antes de continuar — os manifestos abaixo assumem a sintaxe do Compose V2 (`docker compose`, sem hífen).

### Montando o AppFlowy Self-Hosted

AppFlowy é o caso de referência deste capítulo porque cobre a fatia mais ampla dos casos de uso do Notion: documentos, bases de dados relacionais e quadros kanban, tudo a custo de licença zero [1][3]. Comparativos técnicos independentes estimam que ele já reproduz cerca de 85% dos fluxos de trabalho centrais de um workspace típico do Notion [19] — o que sobra fora desse percentual é justamente o assunto da seção 5 deste capítulo.

O manifesto abaixo é a base mínima de produção recomendada pela documentação oficial, adaptada para uma única VPS:

```yaml
# docker-compose.yml — AppFlowy self-hosted (referência mínima de produção)
version: "3.9"

services:
  appflowy_postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: appflowy
      POSTGRES_PASSWORD: "troque-esta-senha"
      POSTGRES_DB: appflowy
    volumes:
      - appflowy_pg_data:/var/lib/postgresql/data

  appflowy_redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - appflowy_redis_data:/data

  appflowy_minio:
    image: minio/minio:latest
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: appflowy
      MINIO_ROOT_PASSWORD: "troque-esta-senha-tambem"
    volumes:
      - appflowy_minio_data:/data

  appflowy_gotrue:
    image: appflowyinc/gotrue:latest
    restart: unless-stopped
    depends_on:
      - appflowy_postgres
    environment:
      GOTRUE_SITE_URL: "https://notas.suaoficina.dev"
      GOTRUE_DB_DRIVER: postgres

  appflowy_cloud:
    image: appflowyinc/appflowy_cloud:latest
    restart: unless-stopped
    depends_on:
      - appflowy_postgres
      - appflowy_redis
      - appflowy_minio
      - appflowy_gotrue
    ports:
      - "8000:8000"
    environment:
      APPFLOWY_DATABASE_URL: "postgres://appflowy:troque-esta-senha@appflowy_postgres/appflowy"
      APPFLOWY_REDIS_URI: "redis://appflowy_redis:6379"
      APPFLOWY_S3_ENDPOINT: "http://appflowy_minio:9000"

volumes:
  appflowy_pg_data:
  appflowy_redis_data:
  appflowy_minio_data:
```

Suba a stack e confirme que todos os serviços entraram no ar antes de apontar o domínio para o servidor:

```console
$ docker compose up -d
[+] Running 5/5
 ✔ Container appflowy_postgres  Started
 ✔ Container appflowy_redis     Started
 ✔ Container appflowy_minio     Started
 ✔ Container appflowy_gotrue    Started
 ✔ Container appflowy_cloud     Started

$ docker compose ps
NAME                 STATUS
appflowy_postgres    Up 12 seconds (healthy)
appflowy_redis       Up 12 seconds (healthy)
appflowy_minio       Up 11 seconds (healthy)
appflowy_gotrue      Up 9 seconds
appflowy_cloud       Up 8 seconds
```

Depois desse ponto, o passo seguinte é o mesmo descrito na documentação oficial de instalação: apontar um reverse proxy (Traefik, Caddy ou Nginx) com TLS para a porta 8000, criar a primeira conta de administrador pela interface e importar seu workspace exportado do Notion.

### As Outras Cinco Peças da Bancada

Nem toda alternativa exige uma stack tão pesada quanto a do AppFlowy. Abaixo, o que muda em cada uma na hora de montar:

**Logseq** — não roda como serviço web por padrão: é um aplicativo local-first, distribuído como executável de desktop que lê e grava arquivos Markdown/Org-mode direto no seu disco [13][11]. Não há `docker-compose.yml` para "instalar o servidor" porque não existe servidor — a sincronização entre dispositivos depende de uma pasta compartilhada via Git ou de um serviço de arquivos externo [12]. É a peça mais simples de montar e a mais limitada em sincronização nativa.

**Joplin** — para ter paridade com a sincronização em nuvem do Evernote, você precisa rodar o Joplin Server, cuja rota de produção recomendada é Docker Compose com PostgreSQL como banco:

```yaml
# docker-compose.yml — Joplin Server
version: "3.9"

services:
  joplin_db:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: joplin
      POSTGRES_PASSWORD: "troque-esta-senha"
      POSTGRES_DB: joplin
    volumes:
      - joplin_pg_data:/var/lib/postgresql/data

  joplin_server:
    image: joplin/server:latest
    restart: unless-stopped
    depends_on:
      - joplin_db
    ports:
      - "22300:22300"
    environment:
      APP_BASE_URL: "https://notas.suaoficina.dev"
      DB_CLIENT: pg
      POSTGRES_HOST: joplin_db
      POSTGRES_USER: joplin
      POSTGRES_PASSWORD: "troque-esta-senha"
      POSTGRES_DATABASE: joplin

volumes:
  joplin_pg_data:
```

Instalado o servidor, cada cliente Joplin (desktop, mobile) aponta para essa URL nas configurações de sincronização [8]. Um plugin de OCR está disponível desde a versão 2.14, mas seu desempenho em imagens complexas ainda é fraco, e a busca full-text em anexos não chega ao nível do Evernote [10][9].

**Outline** — exige obrigatoriamente autenticação via OAuth (Slack, Google ou OIDC): não existe login usuário/senha nativo [14]. A stack mínima documentada é Node.js, Postgres 9.5+, Redis 4+ e um bucket compatível com S3 para anexos — normalmente MinIO em instalações auto-hospedadas [14]. O limite padrão de upload de arquivo é de apenas 1 MB e precisa ser reconfigurado manualmente na variável de ambiente correspondente antes de qualquer uso real com anexos maiores [14][6]. Guias independentes de instalação passo a passo, como o de Karan Sharma, documentam esse ajuste como um dos primeiros passos pós-instalação [17].

**Trilium Notes** — como o Logseq, é local-first e roda como aplicativo desktop ou servidor pessoal leve; a diferença é que a colaboração multiusuário foi explicitamente recusada pelo mantenedor do projeto TriliumNext como complexidade fora do escopo — não é uma limitação técnica temporária, é uma decisão de design permanente [26][27]. Não há app mobile oficial [26]. Se sua bancada é individual, essa peça é uma das mais estáveis da lista; se você precisa de colaboração em equipe, ela está fora de questão [16].

**Standard Notes** — o setup self-hosted de referência (v2) roda em uma VPS pequena, de apenas 2 GB de RAM e 1 vCPU, graças a uma reescrita anunciada pela própria equipe como 70% mais eficiente em memória que a versão anterior [20][21]. É a única ferramenta deste capítulo com auditoria de segurança independente publicada: um pentest e uma revisão de criptografia conduzidos pela Cure53 [23]. Em troca dessa robustez de segurança, o foco é texto simples criptografado ponta a ponta — não espere dele o mesmo suporte a anexos multimídia ricos e clipper web que o Evernote oferece [22].

### Tabela de Decisão: Qual Peça Escolher Primeiro

| Ferramenta | Licença | Modelo | Melhor uso | Evite se... |
|---|---|---|---|---|
| AppFlowy | Aberta [4] | Cloud-capable auto-hospedado | Substituir o Notion quase por completo | Equipe é majoritariamente mobile-first |
| Logseq | AGPL-3.0 [13] | Local-first, sem servidor | Notas pessoais em grafo/Markdown | Grafo vai crescer além de ~300 MB [12] |
| Joplin | Aberta [8] | Local-first + servidor de sync opcional | Substituir o Evernote com sync próprio | Precisa de OCR ou busca robusta em anexos [10] |
| Outline | Aberta [15] | Cloud-capable auto-hospedado | Wiki de equipe com OAuth corporativo | Não tem provedor OAuth disponível [14] |
| Trilium Notes | Aberta [27] | Local-first, mantenedor único | Base de conhecimento pessoal e estável | Precisa de colaboração multiusuário [26] |
| Standard Notes | Aberta [22] | Local-first criptografado | Texto simples com segurança auditada | Depende de anexos multimídia ricos [22] |

Use essa tabela como ponto de partida, não como veredito final — ela resume o que a documentação oficial e os comparativos independentes desta seção já mostraram em detalhe. A ferramenta certa para a sua bancada depende do que você prioriza: abrangência de recursos (AppFlowy), simplicidade local (Logseq/Trilium), paridade de sincronização (Joplin), colaboração de equipe (Outline) ou segurança auditada (Standard Notes).

## 5. Aplica

Imagine a cena: você acabou de instalar o AppFlowy seguindo os passos da seção anterior, ficou satisfeito com o resultado no seu próprio teste solo, e decide migrar o workspace inteiro da sua equipe de oito pessoas no mesmo fim de semana — afinal, a ferramenta "cobre 85% do Notion" [19], então por que esperar? Na segunda-feira, três colegas abrem o mesmo documento de planejamento ao mesmo tempo para revisar a pauta da reunião das 9h. As edições de um sobrescrevem silenciosamente as do outro. Ninguém percebe até a reunião já ter começado com informação desatualizada na tela.

O diagnóstico está na teoria da seção 2: você tratou uma ferramenta cloud-capable como se ela tivesse a mesma maturidade de colaboração em tempo real do Notion, mas "cobrir 85% dos casos de uso" não significa "cobrir 85% de cada caso de uso individualmente" — os 15% que faltam se concentram justamente em colaboração simultânea polida, exatamente o ponto que os comparativos técnicos já sinalizavam como fraqueza antes mesmo da instalação [19][5]. Você comprou a peça certa para a bancada errada: uma peça pensada para uso individual ou colaboração assíncrona, aplicada a um fluxo que exigia edição síncrona em tempo real.

A correção não é abandonar o AppFlowy — é sequenciar a migração. Rode um piloto com uma pessoa ou uma dupla por duas semanas, documentando explicitamente quais fluxos dependem de edição simultânea. Só depois disso migre o restante da equipe, e mantenha, para os poucos documentos que realmente exigem edição ao vivo por várias pessoas, uma ferramenta híbrida ou um fluxo assíncrono acordado ("um edita, avisa no chat, o próximo edita depois"). É um ajuste de processo barato que evita o prejuízo caro de uma decisão tomada em uma reunião sem a informação certa.

Esse tipo de armadilha se repete, com pequenas variações, nas outras cinco ferramentas deste capítulo. Vale sintetizar os limites honestos antes de fechar o capítulo:

- **Colaboração em tempo real polida** é onde toda a categoria perde para o Notion. AppFlowy até cobre parte disso, mas Logseq, Trilium Notes e Standard Notes são desenhados como local-first e não escalam para edição multiusuário simultânea — no caso do Trilium, essa limitação nem é um roadmap futuro, é uma decisão de design definitiva do mantenedor [26]. Não force esse uso: equipes que dependem de colaboração ao vivo devem manter a ferramenta paga para esse fluxo específico, mesmo adotando alternativas abertas para o resto [5].
- **Apps mobile maduros** são o segundo limite real. O comparativo entre AppFlowy e Notion aponta especificamente o aplicativo mobile como sensivelmente menos polido que o do concorrente pago [19], e o Trilium Notes simplesmente não tem app mobile oficial [26]. Se sua equipe trabalha primariamente em celular, teste esse fluxo específico antes de migrar — não assuma que a experiência desktop se repete lá.
- **OCR e busca em anexos de nível Evernote** ainda não têm equivalente maduro nesta lista. O Joplin oferece um plugin de OCR desde a versão 2.14, mas com desempenho fraco em imagens complexas, e sem a busca full-text robusta em anexos que o Evernote entrega nativamente [10][9]. Quem depende de digitalizar recibos, cartões de visita ou documentos escaneados como parte do fluxo de trabalho principal ainda sente essa lacuna.

Curadorias independentes de projetos auto-hospedáveis, como a lista `awesome-selfhosted` [5] e a lista específica de alternativas a SaaS populares [18], confirmam esse mesmo padrão em outras categorias além de notas — e é por isso que este capítulo trata esses três limites como regra geral de como avaliar qualquer substituição futura, não como exceção isolada das ferramentas de anotação.

## 6. Conclusão

Você chegou ao final deste primeiro capítulo com três peças montadas na sua bancada mental: primeiro, que trocar SaaS por open source não elimina custo, apenas o transforma de assinatura mensal em tempo de manutenção — e essa conta precisa ser feita antes da migração, não depois. Segundo, que a instalação real dessas ferramentas é acessível com Docker Compose e algumas horas de atenção, com o AppFlowy cobrindo a fatia mais ampla dos casos de uso do Notion e as outras cinco peças (Logseq, Joplin, Outline, Trilium Notes e Standard Notes) preenchendo nichos específicos de sincronização, segurança e simplicidade. Terceiro, que colaboração em tempo real, apps mobile maduros e OCR de qualidade ainda são pontos honestos de fraqueza — e ignorar isso é o erro mais caro que você pode cometer nesta categoria.

Como desafio prático, antes de seguir para o próximo capítulo: suba o `docker-compose.yml` do AppFlowy (ou do Joplin Server, se preferir sincronização mais simples) em uma VPS real ou até numa máquina local, e migre para lá apenas as suas próprias notas pessoais — não as da sua equipe ainda. Use por uma semana inteira antes de considerar qualquer migração coletiva.

No próximo capítulo, a Oficina Digital ganha sua segunda peça: você vai aprender a montar sua própria stack de e-mail marketing e vai descobrir por que essa categoria escondeu, até agora, a conta mais traiçoeira de toda a substituição SaaS — a reputação de domínio e a deliverability, o motivo pelo qual "montar o servidor" é, ali, apenas o primeiro passo de um processo muito mais longo do que parece.

## 7. Referências Bibliográficas

[1] APPFLOWY. *Docker | AppFlowy Docs*. Disponível em: https://docs.appflowy.io/docs/appflowy/install-appflowy/installation-methods/installing-with-docker. Acesso em: 19 ago. 2026.

[2] APPFLOWY. *Self-Hosting AppFlowy*. Disponível em: https://docs.appflowy.io/docs/guides/appflowy. Acesso em: 19 ago. 2026.

[3] APPFLOWY-IO. *AppFlowy-Cloud*. Disponível em: https://github.com/AppFlowy-IO/AppFlowy-Cloud. Acesso em: 19 ago. 2026.

[4] APPFLOWY-IO. *AppFlowy: Bring projects, wikis, and teams together with AI*. Disponível em: https://github.com/AppFlowy-IO/AppFlowy. Acesso em: 19 ago. 2026.

[5] AWESOME-SELFHOSTED. *A list of Free Software network services and web applications which can be hosted on your own servers*. Disponível em: https://github.com/awesome-selfhosted/awesome-selfhosted. Acesso em: 19 ago. 2026.

[6] CONTABO. *Docmost vs Outline vs Notion: Which Wiki Should You Self-Host?*. Disponível em: https://contabo.com/blog/docmost-vs-outline-vs-notion/. Acesso em: 19 ago. 2026.

[7] DASROOT. *Obsidian vs Logseq vs Notion: PKM Systems Compared 2026*. Disponível em: https://dasroot.net/posts/2026/03/obsidian-logseq-notion-pkm-systems-compared-2026/. Acesso em: 19 ago. 2026.

[8] JOPLIN. *laurent22/joplin*. Disponível em: https://github.com/laurent22/joplin. Acesso em: 19 ago. 2026.

[9] JOPLIN. *Plugins — documentação oficial*. Disponível em: https://joplinapp.org/plugins/. Acesso em: 19 ago. 2026.

[10] JOPLIN FORUM. *Still some way to go for OCR*. Disponível em: https://discourse.joplinapp.org/t/still-some-way-to-go-for-ocr/42964. Acesso em: 19 ago. 2026.

[11] LOGSEQ. *Documentation*. Disponível em: https://docs.logseq.com/. Acesso em: 19 ago. 2026.

[12] LOGSEQ. *Issue #8544: Logseq locks up trying to load large graphs*. Disponível em: https://github.com/logseq/logseq/issues/8544. Acesso em: 19 ago. 2026.

[13] LOGSEQ. *logseq/logseq: A privacy-first, open-source platform for knowledge management and collaboration*. Disponível em: https://github.com/logseq/logseq. Acesso em: 19 ago. 2026.

[14] OUTLINE. *outline/outline: The fastest knowledge base for growing teams*. Disponível em: https://github.com/outline/outline. Acesso em: 19 ago. 2026.

[15] OUTLINE. *Outline – Team knowledge base & wiki*. Disponível em: https://www.getoutline.com/. Acesso em: 19 ago. 2026.

[16] PISTACK. *Joplin vs Trilium Notes vs AFFiNE: Best Self-Hosted Note-Taking 2026*. Disponível em: https://www.pistack.xyz/posts/2026-04-21-joplin-vs-trilium-vs-affine-self-hosted-note-taking-guide-2026/. Acesso em: 19 ago. 2026.

[17] SHARMA, Karan. *Self Hosting Outline Wiki*. Disponível em: https://mrkaran.dev/posts/setting-outline/. Acesso em: 19 ago. 2026.

[18] SOLVOHQ. *awesome-self-host-saas-alternatives: Curated list of strictly self-hostable open-source alternatives to popular SaaS*. Disponível em: https://github.com/SolvoHQ/awesome-self-host-saas-alternatives. Acesso em: 19 ago. 2026.

[19] STACKALTS. *AppFlowy vs Notion (2026): The Local-First Workspace That Owns Your Data*. Disponível em: https://stackalts.com/appflowy-vs-notion.html. Acesso em: 19 ago. 2026.

[20] STANDARD NOTES. *Introducing our new self-hosting setup with 70% more memory efficiency — Decrypted*. Disponível em: https://standardnotes.com/blog/introducing-self-hosting-v2. Acesso em: 19 ago. 2026.

[21] STANDARD NOTES. *Self-hosting with Docker*. Disponível em: https://standardnotes.com/help/self-hosting/docker. Acesso em: 19 ago. 2026.

[22] STANDARD NOTES. *standardnotes/docs: Documentation for Standard Notes users and developers*. Disponível em: https://github.com/standardnotes/docs. Acesso em: 19 ago. 2026.

[23] STANDARD NOTES. *Standard Notes Completes Penetration Test and Cryptography Audit (Cure53) — Decrypted*. Disponível em: https://standardnotes.com/blog/standard-notes-security-audits-2021. Acesso em: 19 ago. 2026.

[24] TECHJOCKEY. *Compare Evernote VS Joplin*. Disponível em: https://www.techjockey.com/us/compare/evernote-vs-joplin. Acesso em: 19 ago. 2026.

[25] TRILIUMNEXT. *Docs*. Disponível em: https://docs.triliumnotes.org/. Acesso em: 19 ago. 2026.

[26] TRILIUMNEXT. *FAQ – User Guide*. Disponível em: https://docs.triliumnotes.org/user-guide/faq. Acesso em: 19 ago. 2026.

[27] TRILIUMNEXT. *Trilium: Build your personal knowledge base with Trilium Notes*. Disponível em: https://github.com/TriliumNext/Trilium. Acesso em: 19 ago. 2026.
