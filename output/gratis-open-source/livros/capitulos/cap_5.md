# Capítulo 5: Design Gráfico e Edição de Imagem: Sem Canva, Sem Photoshop, Sem Illustrator

## 1. Introdução

No Capítulo 4, a Oficina Digital ganhou a primeira peça que trabalha sozinha: o n8n, montado na sua bancada, passou a mover dados e disparar fluxos sem assinatura mensal. Agora chegou a vez das peças que produzem as artes. Canva, Photoshop e Illustrator são, hoje, as ferramentas mais populares de design e edição de imagem do planeta — e também três das assinaturas mais caras que um Artesão Digital pode carregar no cartão, todo mês, sem nunca ter parado para somar o total. Este capítulo faz essa conta e monta a substituição peça por peça: GIMP no lugar do Photoshop, Inkscape no lugar do Illustrator, Krita para pintura digital e Penpot no lugar do Figma e do Canva colaborativo.

A promessa aqui não é a mesma dos vídeos de marketing que prometem substituir o Photoshop em poucos cliques, sem esforço nenhum. A promessa é mais honesta e mais útil: você vai aprender exatamente o que cada ferramenta cobre bem, onde a curva de aprendizado assusta o iniciante, como instalar tudo sem pagar um centavo de licença e como percorrer um fluxo de trabalho completo — do zero até uma peça de marketing pronta. Ao final, a pergunta "qual ferramenta eu uso para isso?" terá uma resposta sua, baseada em dado, não em hábito.

## 2. Explica

Comece pela pergunta que a maioria pula: o que exatamente você compra quando assina o Canva ou a Creative Cloud da Adobe? Não é o software — é o acesso ao software, hospedado ou licenciado sob um contrato que acaba quando o pagamento para. É o mesmo modelo da loja de equipamentos que aluga furadeiras: você paga para usar a peça, mas ela nunca é sua, e no dia em que o aluguel vence sem renovação, a peça some da sua bancada. No caso do Canva, os seus projetos ficam sob custódia da empresa; no caso da Creative Cloud, os programas param de abrir. A mensalidade não compra posse — compra permanência temporária.

Open source resolve exatamente essa parte do problema, e é importante ser preciso sobre o que isso significa. Código aberto quer dizer que o código-fonte do programa é público, licenciado para leitura, modificação e redistribuição. O Penpot, por exemplo, é mantido pela Kaleidos sob licença MPL-2.0, com um repositório ativo que já soma 58,9 mil estrelas no GitHub [1] — você pode ler o código, contribuir e, se quiser, hospedar a sua própria instância. GIMP, Inkscape e Krita seguem o mesmo princípio, com repositórios oficiais abertos em GitLab e GitHub [10][15][19][20]. Isso é diferente de "gratuito": muita ferramenta gratuita não é aberta, e projeto aberto pode ter camada paga por cima — o que importa é que o núcleo é seu.

Agora, a parte que ninguém conta nos vídeos de comparação: a curva de aprendizado. GIMP, Inkscape e Krita são aplicativos desktop nativos, gratuitos e sem modelo de assinatura, que cobrem boa parte do fluxo raster, vetor e pintura do dia a dia [18]. A cobertura é real — reviews independentes estimam que o trio cobre cerca de 85% do fluxo vetor e raster diário sem custo [18]. Mas a interface não é o Canva: não existe caixa de pesquisa que monta o layout para você. No GIMP você trabalha com camadas, canais e máscaras; no Inkscape, com nós, caminhos e curvas de Bézier; no Krita, com pincéis e motores de pintura. Cada um desses conceitos tem um custo de aprendizado inicial — e é exatamente esse custo que assusta o iniciante na primeira hora de uso.

A curva assusta, mas a direção dela é a certa: ela sobe. O GIMP 3.0, lançado vinte anos depois do 2.0, foi recebido por reviews independentes com nota de evolução de interface, embora o port para Windows tenha sido historicamente inferior ao do Linux [11][12]. O Krita 5.2.6 foi classificado por uma review dedicada como "finalmente uma alternativa real" ao Photoshop — no seu nicho, pintura digital [23]. O Inkscape segue como a referência livre de desenho vetorial, com instalador MSI oficial para Windows [14][16]. O que separa quem desiste na primeira semana de quem domina a ferramenta não é talento: é entender que essas peças exigem montagem — instalação, configuração de espaço de trabalho, atualizações — e que essa responsabilidade, antes embutida no aluguel da loja, agora é sua.

Vale também ser preciso sobre as lacunas, porque escondê-las seria desonesto e inútil para você. As três lacunas reais da categoria, confirmadas por reviews independentes, são: produção profissional para impressão (GIMP e Inkscape não têm suporte nativo a CMYK, o que afeta quem precisa de saída certificada para gráfica) [11][13][17]; edição de RAW fotográfico (o GIMP não tem suporte nativo, exigindo ferramenta auxiliar como darktable); e IA generativa (nenhuma das quatro ferramentas tem equivalente maduro ao Generative Fill do Photoshop) [11][13]. Entender essas fronteiras antes de trocar é o que separa o Artesão Digital do amador que troca por fé — e é o assunto da seção Aplica deste capítulo.

## 3. Ilustra

Pense na sua oficina montando uma mesa de trabalho de design. Na loja de aluguel, você recebia três peças emprestadas, sempre prontas, sempre atualizadas: a bancada de fotografia (Photoshop), a bancada de desenho técnico (Illustrator) e a bancada de montagem rápida (Canva). O aluguel cobria manutenção, garantia e um atendente que resolvia quando algo travava. Ao comprar as suas próprias peças, você ganha posse — mas ganha também a responsabilidade de montar cada bancada, ler o manual, calibrar as ferramentas e manter a garantia por conta própria, na documentação e nos fóruns da comunidade.

Agora dê um nome às peças compradas. A bancada de fotografia é o GIMP: raster, edição de imagem, retoque, composição de camadas — o equivalente direto do Photoshop para o fluxo do dia a dia [8][9]. A bancada de desenho técnico é o Inkscape: vetor, logotipos, ícones, diagramas e qualquer arte que precise ser redimensionada sem perder qualidade [14][15]. A bancada de pintura é o Krita: desenho digital, ilustração e concept art, com mais de 120 pincéis com emulação realista [22][23]. E a bancada colaborativa é o Penpot: design de interface rodando no navegador, com edição em equipe em tempo real — o equivalente aberto do Figma, com a diferença crucial de que o Inspect Mode, pago no Figma, é gratuito nele [5].

É exatamente essa troca que acontece quando você sai do aluguel do Canva para o Penpot: a peça deixa de ser um serviço na nuvem de outra empresa e passa a ser uma ferramenta que você pode hospedar onde quiser, ou usar na nuvem oficial gratuita [2]. Como Artesão Digital, é essa segunda lente que você vai treinar no restante do livro: perguntar não apenas "essa peça funciona?", mas "que garantia eu perco ao trocar, e estou disposto a assumir essa manutenção?".

O diagrama abaixo resume o fluxo de decisão que guia este capítulo — da ideia da peça de marketing até a peça pronta na bancada.

```mermaid
%% legenda: Rota da peça de marketing na Oficina Digital: do vetor no Inkscape ao raster no GIMP, com o Krita como opção de pintura e o Penpot na colaboração de interface
flowchart TB
  A[Ideia da peca de marketing] --> B{O que a peca precisa}
  B -->|Vetor, logo ou icone| C[Inkscape: desenho vetorial]
  B -->|Foto, retoque ou composicao| D[GIMP: edicao raster]
  B -->|Ilustracao ou pintura digital| E[Krita: pintura]
  B -->|Interface ou colaboracao em equipe| F[Penpot: design no navegador]
  C --> G[Exportar SVG ou PNG]
  D --> H[Exportar PNG ou JPG]
  E --> H
  F --> I[Inspect Mode gratuito para o dev]
  G --> J[Revisar e publicar a peca]
  H --> J
  I --> J
  J --> K[Peca pronta na bancada do Artesao Digital]
```

## 4. Técnica

Esta seção é onde a Oficina Digital sai do papel. Você vai instalar as quatro peças, subir o Penpot com Docker Compose e montar o fluxo real de produção de uma peça de marketing — tudo com comandos que pode copiar e colar, sem código de programação, porque o que você precisa aqui é operar as ferramentas, não desenvolvê-las.

### Instalando as Peças Desktop: GIMP, Inkscape e Krita

Os três aplicativos são nativos para Windows, macOS e Linux [9][14][22]. No Windows, o caminho mais rápido é o instalador oficial: o Inkscape oferece MSI oficial [16], o GIMP e o Krita distribuem instaladores próprios a partir dos sites oficiais [8][21]. Se você prefere gerenciar tudo por linha de comando, o winget resolve as três instalações:

```console
$ winget install GIMP.GIMP
$ winget install Inkscape.Inkscape
$ winget install KDE.Krita
```

No Linux (Ubuntu/Debian), os três estão nos repositórios oficiais e a instalação é um único comando por ferramenta:

```console
sudo apt update
sudo apt install -y gimp inkscape krita # exemplo didatico: requer um ambiente Linux com sudo
```

### Subindo o Penpot com Docker Compose

O Penpot é a peça colaborativa da bancada: design de interface no navegador, com edição em equipe em tempo real. A rota self-hosted recomendada é Docker Compose, com PostgreSQL como banco e um volume persistente para os assets [3][4]. O manifesto abaixo é a base mínima documentada:

```yaml
# docker-compose.yml — Penpot self-hosted (referência mínima de produção)
services:
  penpot_postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_INITDB_ARGS: "--data-checksums"
      POSTGRES_DB: penpot
      POSTGRES_USER: penpot
      POSTGRES_PASSWORD: "troque-esta-senha"
    volumes:
      - penpot_pg_data:/var/lib/postgresql/data

  penpot_backend:
    image: penpotapp/backend:latest
    restart: unless-stopped
    depends_on:
      - penpot_postgres
    environment:
      PENPOT_FLAGS: "enable-registration enable-login-with-password"
      PENPOT_DATABASE_URI: "postgresql://penpot:troque-esta-senha@penpot_postgres/penpot"
      PENPOT_PUBLIC_URI: "https://design.suaoficina.dev"
      PENPOT_ASSETS_STORAGE_BACKEND: "assets-fs"
      PENPOT_ASSETS_STORAGE_FS_DIRECTORY: "/opt/data/assets"
      PENPOT_TELEMETRY_ENABLED: "false"
    volumes:
      - penpot_assets:/opt/data/assets

  penpot_frontend:
    image: penpotapp/frontend:latest
    restart: unless-stopped
    depends_on:
      - penpot_backend
    ports:
      - "8080:8080"

volumes:
  penpot_pg_data:
  penpot_assets:
```

Suba a stack e confirme que os serviços entraram no ar:

```console
$ docker compose up -d
[+] Running 3/3
 ✔ Container penpot_postgres  Started
 ✔ Container penpot_backend   Started
 ✔ Container penpot_frontend  Started

$ docker compose ps
NAME                 STATUS
penpot_postgres      Up 5 seconds (healthy)
penpot_backend       Up 4 seconds
penpot_frontend      Up 3 seconds
```

Depois disso, o passo seguinte é o mesmo da documentação oficial de self-hosting: apontar um reverse proxy com HTTPS para a porta 8080 e criar a primeira conta pela interface [3][4]. Se você não quer administrar servidor nenhum, a nuvem oficial gratuita do Penpot elimina essa etapa — o trade-off é exatamente o aluguel que você está tentando deixar para trás, então a escolha é sua [2].

### Do Zero a uma Peça de Marketing Pronta

O fluxo completo de uma peça de marketing típica — um banner para redes sociais — usa as quatro bancadas em sequência:

1. **Inkscape**: desenhe o logotipo ou os ícones em vetor. Vetor significa que a arte é definida por caminhos matemáticos, não por pixels: você pode redimensionar para o tamanho de um outdoor sem perder qualidade [14]. Exporte como SVG.
2. **GIMP**: monte a composição final — fundo, foto, logotipo vetorial importado como camada e textos. Trabalhe sempre em camadas separadas; é o equivalente a guardar cada peça da sua bancada em uma gaveta própria [9].
3. **Krita**: se a peça pedir uma ilustração ou pintura original (um personagem, uma textura desenhada à mão), produza aqui, com os pincéis de emulação realista [23].
4. **Penpot**: se a peça for parte de uma interface maior — um banner de site, um card de produto, uma tela de app — monte a estrutura no Penpot e use o Inspect Mode gratuito para repassar medidas e cores a quem for implementar [5].

O ciclo de exportação fecha o fluxo: PNG para imagens com transparência, JPG para fotos e publicações que não precisam de transparência, SVG para vetores que vão ser reutilizados. Nenhuma das quatro ferramentas cobra um centavo por exportação — no Canva, recursos como fundo transparente e exportação em alta resolução ficam atrás do paywall; aqui, são botões padrão.

### Tabela de Decisão: Qual Peça Pegar na Prateleira

| Ferramenta | Licença | Modelo | Melhor uso | Evite se... |
|---|---|---|---|---|
| GIMP | Aberta [10] | Desktop nativo | Retoque, composição raster e edição de imagem [8] | Fluxo exige CMYK nativo ou RAW sem ferramenta auxiliar [11][13] |
| Inkscape | Aberta [15] | Desktop nativo | Vetor, logotipos, ícones e diagramas escaláveis [14] | Arquivos vetoriais muito grandes (instabilidade documentada) [17] |
| Krita | Aberta [19] | Desktop nativo | Pintura digital e ilustração (120+ pincéis) [22] | Uso principal é edição fotográfica, não pintura [23] |
| Penpot | MPL-2.0 [1] | Self-hosted ou nuvem gratuita | Design de interface colaborativo no navegador [2] | Time depende do marketplace de plugins do Figma ou de templates prontos do Canva [6][7] |

Use a tabela como ponto de partida, não como veredito final. Ela resume o que a documentação oficial e os reviews independentes desta seção já mostraram: o trio desktop cobre cerca de 85% do fluxo vetor e raster do dia a dia sem custo [18], e o Penpot já é considerado um substituto viável do Figma para design colaborativo — mas cada peça tem o seu perímetro exato de uso [5][6].

### A Automação da Bancada: Scripts que Preparam e Exportam

A bancada de design ganha velocidade quando as tarefas repetitivas viram scripts — e o Artesão Digital que já conhece o básico de terminal do capítulo 4 pode automatizar a parte mais chata do fluxo: a preparação dos arquivos para publicação. O `ImageMagick`, companheiro de linha de comando do GIMP e do Inkscape, redimensiona, converte e aplica efeitos em lote com um comando — e a sessão abaixo mostra o caso mais comum, a geração de todas as variações de uma peça para as redes sociais a partir do arquivo mestre:

```console
$ mkdir -p publicacao && cd publicacao
$ convert ../peca-mestre.png -resize 1080x1080^ -gravity center -extent 1080x1080 post-quadrado.png
$ convert ../peca-mestre.png -resize 1080x1920^ -gravity center -extent 1080x1920 story-vertical.png
$ convert ../peca-mestre.png -resize 1200x630^ -gravity center -extent 1200x630 link-preview.png
$ ls -lh
-rw-r--r-- 1 artesao artesao 412K ago 20 07:00 link-preview.png
-rw-r--r-- 1 artesao artesao 489K ago 20 07:00 post-quadrado.png
-rw-r--r-- 1 artesao artesao 812K ago 20 07:00 story-vertical.png
```

O comando `convert` do ImageMagick faz o redimensionamento com corte central (o trecho `^` combinado com `-extent`), mantendo o enquadramento da peça em cada formato — o mesmo efeito que o Canva faz por clique, mas em lote e sem depender de internet [8][12]. A linha de baixo mostra o resultado: três formatos prontos a partir de um único arquivo mestre, sem abrir nenhum programa gráfico. A automação não substitui o design — substitui a repetição, e libera o tempo do Artesão Digital para o que nenhum script faz: a decisão visual.

### A Curva de Aprendizado: O Que Realmente Custava Caro

A fatura escondida do software de design nunca foi o preço da licença — foi o tempo para aprender a usar a ferramenta. O Photoshop e o Illustrator cobram mensalidade; o GIMP e o Inkscape cobram horas de estudo. A revisão da Creative Bloq sobre o Krita 5.2.6 resume a virada: depois de anos sendo tratado como alternativa "de nicho", o Krita finalmente foi reconhecido como uma alternativa real ao Photoshop para pintura digital [23] — mas o reconhecimento não elimina a curva. Os requisitos são honestos: o Krita recomenda 8 GB de RAM, e 16 GB para telas 4K [22]; o GIMP e o Inkscape rodam em máquinas modestas, mas lidam mal com arquivos muito grandes, com instabilidade documentada em projetos pesados [17]. A régua da seção 5 decide quando a curva vale a pena: para o fluxo diário de marketing, a curva é curta e o retorno é imediato; para a produção profissional de impressão com saída CMYK certificada, a curva continua íngreme em qualquer ferramenta gratuita, e a troca não compensa [11][17]. A transparência dessa régua é o que separa a oficina séria da promessa de marketing: o open source é grátis, mas nada nele é instantâneo.

## 5. Aplica

Imagine a cena: você acabou de instalar as quatro peças, animado com a conta que vai economizar, e precisa entregar uma peça de marketing para a semana de lançamento — um banner para uma postagem patrocinada. Você abre o GIMP pela primeira vez e a interface mostra dezenas de janelas flutuantes, painéis de camadas, canais, caminhos e histórico. Você tenta "simplesmente" recortar o produto da foto de fundo com a ferramenta de seleção livre, erra o contorno, tenta desfazer, o recorte fica serrilhado, e em vinte minutos você está convencido de que open source não vale o esforço e de que "o Photoshop era melhor".

Pare. Esse é o erro clássico, e o diagnóstico é simples: você está usando a bancada certa do jeito errado. A curva de aprendizado do GIMP não é sobre inteligência — é sobre conceito. Recortar um objeto de uma foto não se faz com seleção livre à mão livre; faz-se com o caminho de Bézier (a ferramenta "Caminhos"), que desenha curvas suaves ao redor do objeto, converte o caminho em seleção e aplica a máscara. É o mesmo método que os profissionais usam no Photoshop, e ele leva algumas horas de prática para fluir — não vinte minutos. A correção não é voltar para o aluguel: é aceitar que a primeira peça de marketing vai levar o dobro do tempo, e que isso é investimento, não prejuízo.

Além da cena acima, vale registrar as outras armadilhas comuns dessa migração:

- **Trocar a ferramenta pelo fluxo errado**: usar o GIMP para desenhar um logotipo que vai ser impresso em vários tamanhos. Logotipo é vetor — a peça certa é o Inkscape, que exporta SVG e escala sem perda [14]. O GIMP é raster; ampliar um logotipo em raster é pedir serrilhado.
- **Prometer paridade CMYK para a gráfica**: GIMP e Inkscape não têm suporte nativo a CMYK [11][13][17]. Se o seu fluxo principal é impressão profissional certificada, essa é a lacuna honesta — mantenha o aluguel para esse fluxo específico ou contorne com plugins e ferramentas auxiliares, e deixe isso combinado com a gráfica antes de prometer a troca para o time.
- **Depender de IA generativa**: o Generative Fill do Photoshop não tem equivalente maduro nas quatro ferramentas [11][13]. Se a sua rotina depende de preenchimento generativo de imagens, nenhuma das peças desta bancada substitui esse fluxo hoje — planeje o contorno (remover o elemento manualmente com carimbo e clonagem) antes de migrar.
- **Subestimar o ecossistema**: o Penpot tem base de usuários menor e menos plugins de terceiros que o Figma, e o Canva vende templates prontos que não têm equivalente direto [6][7]. Times que vivem de marketplace de plugins ou de templates prontos vão sentir a troca — o contorno é construir a sua própria biblioteca de componentes no Penpot, e isso também é trabalho de bancada.

O profissional — o Artesão Digital que você está se tornando — não mede a troca pelo preço, mede pelo fluxo. Antes de migrar qualquer equipe, rode o piloto sozinho: produza três peças reais do início ao fim, cronometre, anote onde cada ferramenta travou e onde fluiu. Só depois disso a decisão entre manter o aluguel para um fluxo específico e comprar a peça para o resto é uma decisão com dado na mesa — e é exatamente essa disciplina que separa quem brinca de open source de quem administra uma oficina.

## 6. Conclusão

Três ideias sustentam este capítulo. Primeira: o trio GIMP, Inkscape e Krita cobre cerca de 85% do fluxo vetor e raster diário sem custo [18], e o Penpot já é um substituto viável do Figma para design colaborativo [5] — a bancada completa de design da Oficina Digital existe, é gratuita e é sua. Segunda: a curva de aprendizado é real e assusta o iniciante, mas é uma curva de conceitos — camadas, caminhos, vetores — que se domina com prática deliberada, e o retorno é a posse definitiva da peça, sem mensalidade para sempre [11][12][23]. Terceira: as lacunas honestas — CMYK nativo, RAW, IA generativa e ecossistema de plugins — definem o perímetro da troca, e conhecê-las antes de prometer a migração para o seu time é o que separa o Artesão Digital do amador [6][11][13][17].

Como desafio prático: produza a sua primeira peça de marketing completa com as quatro bancadas — um vetor no Inkscape, uma composição no GIMP, uma ilustração no Krita (se a peça pedir) e uma tela no Penpot, hospedado onde você escolher. Cronometre o tempo total e anote as três dores que aparecerem. Esse registro é o seu mapa de manutenção da bancada, e ele vai servir para todas as trocas que ainda vêm.

No próximo capítulo, a bancada ganha uma peça de outro tipo: edição de vídeo e armazenamento em nuvem. Você vai descobrir por que o DaVinci Resolve — a ferramenta mais famosa da categoria — é, na verdade, uma armadilha de licença para quem busca open source de verdade, e como Shotcut, Kdenlive, Nextcloud e Seafile ocupam os espaços que ela não cobre.

## 7. Referências Bibliográficas

[1] AWESOME-SELFHOSTED. *A list of Free Software network services and web applications which can be hosted on your own servers*. Disponível em: https://github.com/awesome-selfhosted/awesome-selfhosted. Acesso em: 19 ago. 2026.

[2] PENPOT/KALEIDOS. *penpot: The open-source design platform for Product teams that need scalable collaboration*. Disponível em: https://github.com/penpot/penpot. Acesso em: 19 ago. 2026.

[3] PENPOT. *Self-Host Penpot: Deploy it anywhere*. Disponível em: https://penpot.app/self-host. Acesso em: 19 ago. 2026.

[4] PENPOT. *Self-hosting Guide — Help center*. Disponível em: https://help.penpot.app/technical-guide/getting-started/. Acesso em: 19 ago. 2026.

[5] PENPOT. *Install with Docker — Help center*. Disponível em: https://help.penpot.app/technical-guide/getting-started/docker/. Acesso em: 19 ago. 2026.

[6] JONKER, Nolen. *I tried a free, open-source, browser-based alternative to Figma, and it blew my mind*. XDA Developers. Disponível em: https://www.xda-developers.com/tried-free-open-source-browser-based-alternative-figma/. Acesso em: 19 ago. 2026.

[7] XDA DEVELOPERS. *I replaced Figma with four open-source alternatives for a week, and only one actually stuck*. Disponível em: https://www.xda-developers.com/replaced-figma-with-open-source-alternatives-only-one-stuck/. Acesso em: 19 ago. 2026.

[8] SLASHDOT. *Compare Canva vs. Figma vs. Penpot in 2026*. Disponível em: https://slashdot.org/software/comparison/Canva-vs-Figma-vs-penpot/. Acesso em: 19 ago. 2026.

[9] GIMP TEAM. *GIMP — GNU Image Manipulation Program*. Disponível em: https://www.gimp.org/. Acesso em: 19 ago. 2026.

[10] GIMP TEAM. *GIMP Documentation*. Disponível em: https://docs.gimp.org/. Acesso em: 19 ago. 2026.

[11] GNOME. *gimp: GNU Image Manipulation Program (source)*. GitLab. Disponível em: https://gitlab.gnome.org/GNOME/gimp. Acesso em: 19 ago. 2026.

[12] CREATIVE BLOQ. *GIMP 3.0 review: 20 years on from 2.0, has GIMP kept up with the times?*. Disponível em: https://www.creativebloq.com/photography/photo-editing-software/gimp-3-0-review-20-years-on-from-2-0-has-gimp-kept-up-with-the-times. Acesso em: 19 ago. 2026.

[13] CREATIVE BLOQ. *How I really feel about GIMP, now the dust has settled*. Disponível em: https://www.creativebloq.com/photography/photo-editing-software/how-i-really-feel-about-gimp-now-the-dust-has-settled. Acesso em: 19 ago. 2026.

[14] GEEKSFORGEEKS. *GIMP vs Photoshop*. Disponível em: https://www.geeksforgeeks.org/blogs/gimp-vs-photoshop/. Acesso em: 19 ago. 2026.

[15] INKSCAPE PROJECT. *Inkscape: Draw Freely*. Disponível em: https://inkscape.org/. Acesso em: 19 ago. 2026.

[16] INKSCAPE PROJECT. *inkscape/inkscape (repositório de código)*. GitLab. Disponível em: https://gitlab.com/inkscape/inkscape. Acesso em: 19 ago. 2026.

[17] INKSCAPE PROJECT. *Installing Inkscape — Inkscape Wiki*. Disponível em: https://wiki.inkscape.org/wiki/Installing_Inkscape. Acesso em: 19 ago. 2026.

[18] VECTEEZY. *Inkscape vs. Illustrator: A Head-to-Head Comparison*. Disponível em: https://www.vecteezy.com/blog/design-tips/inkscape-vs-illustrator. Acesso em: 19 ago. 2026.

[19] CREATIVE BLOQ. *Tired of Adobe and the big tech giants? Here's how I created my ideal Open Source Creative Workstation*. Disponível em: https://www.creativebloq.com/art/digital-art-software/tired-of-adobe-and-the-big-tech-giants-i-created-my-ideal-open-source-creative-workstation-p-s-its-very-cheap. Acesso em: 19 ago. 2026.

[20] KDE. *krita* (mirror). GitHub. Disponível em: https://github.com/KDE/krita. Acesso em: 19 ago. 2026.

[21] KDE. *Graphics / Krita* (repositório oficial). GitLab (invent.kde.org). Disponível em: https://invent.kde.org/graphics/krita. Acesso em: 19 ago. 2026.

[22] KRITA FOUNDATION. *Krita — Digital Painting. Creative Freedom*. Disponível em: https://krita.org/en/. Acesso em: 19 ago. 2026.

[23] KRITA FOUNDATION. *Installation — Krita Manual*. Disponível em: https://docs.krita.org/en/user_manual/getting_started/installation.html. Acesso em: 19 ago. 2026.

[24] CREATIVE BLOQ. *Krita 5.2.6 review: finally, a real Photoshop alternative*. Disponível em: https://www.creativebloq.com/reviews/krita. Acesso em: 19 ago. 2026.

[25] AWESOME-SELFHOSTED. *A list of Free Software network services and web applications which can be hosted on your own servers*. Disponível em: https://github.com/awesome-selfhosted/awesome-selfhosted. Acesso em: 19 ago. 2026.

[26] SOLVOHQ. *awesome-self-host-saas-alternatives: Curated list of strictly self-hostable open-source alternatives to popular SaaS*. Disponível em: https://github.com/SolvoHQ/awesome-self-host-saas-alternatives. Acesso em: 19 ago. 2026.
