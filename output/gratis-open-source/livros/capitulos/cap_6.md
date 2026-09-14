# Capítulo 6: Vídeo e Nuvem: Editando e Guardando Seus Arquivos Sem Assinatura

## 1. Introdução

No capítulo anterior, a oficina aprendeu a produzir peças visuais — imagens, vetores e interfaces — sem pagar licença. Agora a bancada enfrenta dois dos aluguéis mais caros da lista: o editor de vídeo que cobra mensalidade ou esconde o preço na forma de uma versão gratuita que não é sua, e a nuvem que guarda seus arquivos enquanto o cartão de crédito continuar valendo. Este capítulo trata das duas trocas — e, como nos anteriores, com a honestidade que a Oficina Digital exige: existem categorias em que a substituição é madura, e existem casos em que o rótulo "open source" é usado de forma errada.

Você vai aprender, nesta ordem: como editar vídeo de verdade com ferramentas livres (Shotcut e Kdenlive) e por que o DaVinci Resolve — gratuito, mas proprietário — não pertence à sua prateleira, e sim à loja de aluguel; como montar a sua própria nuvem com Nextcloud e Seafile, devolvendo o controle dos dados à sua bancada; e o orçamento oculto que toda assinatura de armazenamento escondia dentro da mensalidade, com a matemática real de disco, backup e banda. Ao final, você terá um pipeline de vídeo funcionando e uma nuvem própria no ar — e saberá exatamente quanto cada um deles custa para manter.

## 2. Explica

A primeira distinção que este capítulo precisa fazer é a mais ignorada em listas de "alternativas open source": grátis não é o mesmo que aberto, e aberto não é o mesmo que seu. O DaVinci Resolve é o exemplo perfeito. Ele é distribuído gratuitamente pela Blackmagic Design, mas é software proprietário, em modelo freemium: não existe repositório público de código-fonte, você não pode ler, modificar nem redistribuir nada [135]. A versão gratuita é uma vitrine cuidadosamente calibrada — ela cobre edição, correção de cor, efeitos e áudio até UHD 60fps sem marca d'água, o que é generoso, mas deixa de fora justamente os recursos que movem o profissional para o pagamento: inteligência artificial, exportação DCI 4K/6K/8K, aceleração multi-GPU e HDR [135][137][138]. É o modelo clássico da loja de aluguel: você usa a furadeira de graça, mas os acessórios que fazem o serviço profissional custam, e o motor continua sendo da loja. Tratar o Resolve como "open source" na sua oficina seria o mesmo que pendurar na prateleira uma peça que continua alugada.

As ferramentas que realmente pertencem à sua bancada são Shotcut e Kdenlive — ambas 100% open source, sob licença GPLv3, e ambas construídas sobre o mesmo motor: o MLT Framework, uma biblioteca de edição não linear que faz o trabalho pesado de timeline, codecs e filtros [130][131]. Isso importa na prática porque os dois projetos herdam os mesmos pontos fortes e as mesmas limitações do MLT. Os requisitos de hardware são honestos e modestos: Windows 10 64-bit, macOS 12+ ou Linux, de 4 a 16 GB de RAM e uma GPU com suporte a OpenGL 2.0 — qualquer computador razoável monta a bancada de edição [126]. As reviews independentes confirmam o amadurecimento: a do Shotcut, na PCWorld, classifica o editor como "impressionante" apesar de uma interface que ainda parece datada [127], e a do TechRadar reforça o mesmo veredito [128]. A instabilidade histórica, porém, é real e documentada — há issues públicas no rastreador do MLT registrando crashes ao adicionar vídeos longos à timeline [129], e o Kdenlive sofreu por anos com cenários de travamento que só as releases recentes corrigiram em massa [132][133]. A verdade incômoda: para produções longas e pesadas, ou projetos que dependem do ecossistema Adobe, a troca ainda perde — e o capítulo 5 desta parte mostrou como reconhecer esse limite antes de migrar [134].

A segunda peça de vocabulário é a nuvem self-hosted. Nextcloud é um servidor completo de sincronização e compartilhamento: você instala em uma VPS ou num servidor caseiro, e os clientes de desktop e celular sincronizam pastas como o Google Drive ou o Dropbox fariam — mas os arquivos vivem em infraestrutura sua, sem cobrança por usuário [139][140][141]. O custo oficial mínimo é baixo, mas a prática recomenda 2 a 4 GB de RAM para uso doméstico e 8 GB ou mais para times [140]. A limitação honesta: a criptografia ponta-a-ponta ainda não está totalmente implementada — os arquivos são criptografados em trânsito e em repouso no servidor, mas o servidor, sendo seu, é o limite da sua confiança [142]. Seafile ocupa o mesmo nicho com uma arquitetura diferente — núcleo em C, sincronização por blocos — e exigência ainda mais modesta: 2 núcleos de CPU e 2 GB de RAM para a edição comunitária [144][145]. Sua criptografia client-side usa AES-256-CBC por biblioteca, mas não funciona no navegador nem nos clientes de nuvem — um limite que qualquer review independente acaba apontando [146]. E há ainda o Syncthing, que não é uma nuvem: é sincronização ponto a ponto, sem servidor central, sem limite de armazenamento e sem mensalidade [148][151] — mas a própria documentação oficial insiste que ele não substitui backup, e o capítulo 5 deste capítulo vai mostrar por quê [149][150].

## 3. Ilustra

A imagem mental deste capítulo é a de uma oficina que recebe matéria-prima bruta — o vídeo gravado no cartão de memória — e a transforma em peça acabada que vai para a prateleira. No modelo alugado, você entrega a matéria-prima a uma loja (a nuvem ou o editor do fabricante), recebe o produto pronto, e a loja fica com a peça, o molde e os lucros do serviço recorrente. Na sua oficina, o caminho é outro: o arquivo bruto entra pela bancada de montagem (Shotcut ou Kdenlive), sai como vídeo finalizado, e termina na estante central da sua própria nuvem — com uma cópia externa de segurança que é a única coisa que sobrevive a um desastre.

Essa primeira analogia resolve a mecânica de posse. Mas, como no capítulo anterior, a segunda lente é a que revela o custo escondido: a mensalidade da nuvem comprava, silenciosamente, um pacote completo de infraestrutura — disco, replicação em múltiplos data centers, banda de upload abundante e peças de reposição instantâneas quando um drive morria. Nenhuma dessas coisas é mágica; todas têm etiqueta de preço. Ao trocar o Google Drive pelo Nextcloud, você não elimina esses custos — você os separa em três contas visíveis que passam a ser suas: a conta do disco, a conta do backup e a conta da banda. O diagrama abaixo resume esse fluxo, da matéria-prima à prateleira com redundância.

```mermaid
%% legenda: Da materia-prima a prateleira: o caminho do arquivo na Oficina Digital
flowchart LR
  A[Cartao de memoria: video bruto] --> B{Bancada de montagem}
  B --> C[Shotcut: editor livre]
  B --> D[Kdenlive: editor livre]
  C --> E[Video finalizado]
  D --> E
  E --> F{Guarda onde?}
  F --> G[Nextcloud: estante central propria]
  F --> H[Seafile: estante leve]
  G --> I[Backup externo 3-2-1]
  H --> I
  I --> J[Prateleira segura: o desastre nao leva tudo]
```

## 4. Técnica

Esta seção segue o padrão do material-fonte: verificação de hardware antes da instalação, sessões de terminal com comando e saída esperada, um manifesto Docker Compose completo para a nuvem própria, e um script de backup comentado linha a linha — sem código de programação, porque o que você precisa aqui é operar a oficina, não desenvolvê-la.

### Montando a Bancada de Vídeo

Antes de instalar qualquer editor, confira se a bancada tem o mínimo que o MLT Framework exige. O comando abaixo mostra o sistema operacional, a memória e o suporte a OpenGL — os três requisitos do Shotcut e do Kdenlive [126][131]:

```console
$ uname -a
Linux oficina 6.8.0-45-generic #45-Ubuntu SMP x86_64 GNU/Linux
$ free -h
               total        used        free
Mem:           15GiB       3,2GiB       11GiB
$ glxinfo | grep "OpenGL version"
OpenGL version string: 4.6 (Core Profile) Mesa 24.0.5
```

Com os requisitos confirmados, a instalação no Linux é um comando — o Kdenlive é empacotado pela KDE e disponível nos repositórios oficiais da maioria das distribuições:

```console
$ sudo apt install kdenlive
$ kdenlive --version
kdenlive 25.08.1
```

O Shotcut, por sua vez, distribui um instalador para cada plataforma — no Windows, o arquivo MSI oficial instala e cria o atalho da bancada [127]:

```console
C:\Users\artesao> shotcut.exe --version
Shotcut version 25.05.30
```

### A Estante Central: Nextcloud Self-Hosted

A nuvem da oficina começa com um manifesto Docker Compose. A base mínima de produção recomendada pela documentação oficial do Nextcloud usa três serviços: a aplicação, o banco de dados e um volume persistente — a prateleira física onde os dados duram [141]:

```yaml
# docker-compose.yml — Nextcloud self-hosted (referência mínima)
version: "3.9"

services:
  db:
    image: mariadb:11
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: nextcloud
      MYSQL_USER: nextcloud
      MYSQL_PASSWORD: troque-esta-senha
      MYSQL_ROOT_PASSWORD: troque-esta-root
    volumes:
      - db:/var/lib/mysql

  app:
    image: nextcloud:stable
    restart: unless-stopped
    ports:
      - "8080:80"
    environment:
      MYSQL_HOST: db
      MYSQL_DATABASE: nextcloud
      MYSQL_USER: nextcloud
      MYSQL_PASSWORD: troque-esta-senha
    volumes:
      - nextcloud:/var/www/html
    depends_on:
      - db

volumes:
  db:
  nextcloud:
```

Subir a estante é um comando, e o primeiro login define a conta de administrador — a chave da oficina:

```console
$ docker compose up -d
[+] Running 3/3
 ✔ Container db  Started
 ✔ Container app  Started
$ curl -sI http://localhost:8080 | head -1
HTTP/1.1 302 Found
```

A manutenção da estante também passa pelo terminal: a interface de linha de comando do próprio Nextcloud (o comando `occ`) executa as tarefas de rotina — declaração de manutenção antes de atualizar, e a conferência de erros do sistema:

```console
$ docker compose exec -u www-data app php occ maintenance:mode --on
Maintenance mode enabled
$ docker compose exec -u www-data app php occ status
  - installed: true
  - version: 30.0.1
```

### A Prateleira Externa: Backup com a Regra 3-2-1

A lição mais cara deste capítulo é também a mais simples: estante não é backup. O Syncthing sincroniza, mas se um ransomware criptografar os arquivos em todos os dispositivos, a sincronização propaga o desastre [149][150]. Backup de verdade segue a regra 3-2-1 — três cópias, em dois meios diferentes, uma delas fora do ambiente — e o `restic` executa isso de forma automatizada e verificável:

```console
# backup-oficina.sh — regra 3-2-1 na pratica (exemplo didatico: requer restic instalado)
# Copia 1 e 2: estante Nextcloud + disco local (ja existem)
# Copia 3: repositorio restic em disco externo, fora do ambiente

export RESTIC_REPOSITORY=/media/disco-externo/restic-oficina
export RESTIC_PASSWORD="senha-do-cofre"

# 1. Faz o snapshot criptografado de toda a prateleira
restic backup /srv/nextcloud/data

# 2. Verifica a integridade do cofre (nada de confiar cegamente)
restic check

# 3. Política de retenção: 7 diarios, 4 semanais, 6 mensais
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune
```

### A Estante Leve: Seafile para o Autônomo

O Nextcloud é a estante completa, mas nem toda oficina precisa de calendário, contatos e edição colaborativa embutidos. O Seafile ataca exatamente esse espaço: um núcleo em C focado em sincronização de blocos, rápido e econômico, com a edição comunitária exigindo apenas 2 núcleos de CPU e 2 GB de RAM [144][145]. A instalação via Docker segue o mesmo padrão dos manifestos anteriores, com um detalhe que vale registrar: o Seafile usa uma única imagem oficial que sobe o servidor e o banco interno juntos, e a configuração inicial é feita pelo assistente web na primeira execução [144]. A criptografia client-side existe e usa AES-256-CBC, mas a própria documentação e as reviews deixam claro o limite: ela não funciona no navegador nem nos clientes de nuvem — só no desktop —, então quem vive de acesso pelo celular acaba guardando os arquivos sem essa camada de proteção [146].

A escolha entre Nextcloud e Seafile é, portanto, a escolha entre a estante completa e a prateleira enxuta: o comparativo independente da CloudBasedBackup resume o veredito com uma frase — o Nextcloud vence em colaboração e ecossistema, o Seafile vence em velocidade e simplicidade de recursos [147]. O teste da Speed-Drain reforça a mesma conclusão para quem compara as três opções self-hosted do mercado: o Syncthing é o mais leve, o Seafile o mais rápido para pastas grandes e o Nextcloud o mais completo em funcionalidades [152]. Para o Artesão Digital que roda um VPS de 2 GB, essa diferença de peso decide a escolha antes mesmo da interface.

### Vídeo Não É Só Cortar: O Fluxo de Produção Completo

Editar vídeo na bancada própria vai além de arrastar clipes na timeline. O fluxo completo de produção tem etapas que o usuário de assinatura nunca enxergou porque a loja fazia tudo: capturar (o cartão de memória), transferir (a velocidade de leitura do leitor), organizar (a árvore de pastas do projeto), editar (o corte), exportar (o codec e o formato de destino) e distribuir (o upload para a plataforma). Cada uma dessas etapas cobra um recurso diferente da sua oficina — e a seção 5 deste capítulo mostrou como o orçamento aparece em cada uma. O que vale fixar aqui é a ordem: o iniciante quer pular direto para a edição e esquece que a maior parte do tempo real de um projeto está na captura e na organização. O Kdenlive facilita o trabalho com uma árvore de projeto clara, mas a disciplina de nomear arquivos, versões e cortes é sua [131][133]. O Shotcut, por sua vez, brilha na simplicidade do fluxo de exportação, com perfis prontos para YouTube e Vimeo que escondem a matemática de bitrate e resolução [127][128] — e esconder essa matemática é exatamente o que o iniciante precisa nos primeiros projetos, antes de aprender a calcular o tamanho de arquivo por minuto.

```console
$ ffprobe -v error -show_entries format=duration,bit_rate -of default=noprint_wrappers=1 projeto-final.mp4
duration=300.500000
bit_rate=8250000
$ ls -lh projeto-final.mp4
-rw-r--r-- 1 artesao artesao 313M ago 20 07:00 projeto-final.mp4
```

O comando acima — uma linha de `ffprobe` — responde à pergunta que todo editor precisa fazer antes de subir um vídeo: quanto pesa o arquivo, quanto dura e a que bitrate foi exportado. São as três informações que decidem se o upload para a plataforma vai levar cinco minutos ou cinco horas na banda da sua conexão [152]. E é também a diferença entre bater cabeça com o "vídeo traveou na timeline" e saber, antes de editar, que o arquivo de 60 minutos em 4K bruto vai exigir proxies ou cortes em partes: a instabilidade documentada do MLT em arquivos longos não é mistério — é uma propriedade mensurável do formato e do hardware [129][133]. E é por isso que a produção de vídeo na oficina própria é, antes de tudo, um exercício de medição: medir antes de editar, medir antes de exportar e medir antes de subir. Cada medição evita uma hora de retrabalho — e nenhuma delas depende de licença.

### A Rotina de Manutenção da Estante: Sincronização e Saúde do Servidor

A estante própria não entrega valor apenas no dia da montagem — entrega na rotina. Depois do Nextcloud no ar, a manutenção tem um ritmo mensal com três frentes que a documentação oficial cobre e que a assinatura escondia na mensalidade: aplicar as atualizações do servidor, verificar a saúde dos serviços e conferir o estado da sincronização [141][143]. A primeira frente é o comando `occ` — a linha de comando administrativa do Nextcloud — que já apareceu na seção de instalação e que também executa a verificação de integridade da instalação:

```console
$ docker compose exec -u www-data app php occ maintenance:mode --off
Maintenance mode disabled
$ docker compose exec -u www-data app php occ app:update --all
  [OK] Atualizacoes aplicadas para: 3 apps
$ docker compose exec -u www-data app php occ status
  - installed: true
  - version: 30.0.1
```

A segunda frente é a saúde visível no painel do servidor: uso de disco, memória e a fila de trabalhos agendados do Nextcloud (os cron jobs que processam notificações, uploads e expirações de compartilhamento). A sessão abaixo mostra como conferir a fila e o estado do disco de uma só vez — os dois números que decidem se a estante está saudável ou se está uma bomba-relógio:

```console
$ docker compose exec -u www-data app php occ background:cron
$ df -h /srv/nextcloud
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        50G   31G   19G  62% /
$ docker compose logs --since 24h app | grep -c "ERROR"
0
```

O hábito que fechar a rotina é a conferência do log: zero erros nas últimas 24 horas é o sinal verde, e qualquer ERROR repetido é um alerta que a assinatura teria resolvido sem você ver — e que agora é problema da sua bancada [143]. É esse tripé — atualização, saúde e log — que transforma a estante de "projeto do fim de semana" em "infraestrutura de verdade", e é exatamente o mesmo tripé que a seção 5 do capítulo 8 vai aplicar à oficina inteira, em escala.

## 5. Aplica

A jornada prática deste capítulo é a primeira semana do Artesão Digital migrando vídeo e arquivos. O cenário: você terminou de editar um vídeo curto para o canal da sua área — algo de cinco minutos, com cortes, texto sobreposto e áudio limpo — e gravou os arquivos brutos de um projeto inteiro na pasta sincronizada da nuvem.

**Erro comum:** você confia na sincronização como se ela fosse backup. Edita o vídeo direto da pasta sincronizada do Nextcloud em dois dispositivos, apaga os arquivos brutos "para liberar espaço", e quando o drive da VPS morre — ou um erro de sincronização propaga a exclusão para todos os lados — descobre que o projeto inteiro existia em uma única cópia. O diagnóstico é sempre o mesmo: sincronizar replica; backup preserva. São funções diferentes, e este capítulo mostrou que até a documentação do Syncthing avisa que ele não é ferramenta de backup [149][150].

**Prática correta:** a pasta sincronizada recebe apenas o material de trabalho corrente. O projeto bruto gravado no cartão vai direto para a estante — e o `backup-oficina.sh` roda na madrugada, criando o snapshot criptografado no disco externo. A rotina semanal inclui um `restic check` real, porque backup que nunca é verificado é apenas uma esperança. Quando o desastre finalmente acontece — e algum dia acontece — a restauração é um comando: `restic restore latest --target /restauracao`. Você perde horas, não anos.

**A decisão que fecha a semana:** com o pipeline montado, chega a hora de calcular a conta real — e comparar o que a assinatura do Drive/Dropbox escondia: o disco da estante, o disco externo do cofre e a banda de upload da sua conexão, que agora sobe arquivos de projeto inteiros, não apenas fotos comprimidas no celular. A revisão da seção 2 já deu os números de referência: o Nextcloud prático pede 2 a 4 GB de RAM doméstico [140], o Seafile roda com 2 núcleos e 2 GB [145], e a sua conexão residencial de upload assimétrico decide se a estante fica em casa ou numa VPS. Quando a soma dessas três contas ainda ficar abaixo do que a mensalidade cobrava, a troca está paga — e a peça é sua.

Essa conta tem um teto, e é importante reconhecê-lo antes de prometer a troca para o time: a partir de um punhado de pessoas subindo e baixando arquivo de vídeo pesado o dia inteiro, o gargalo deixa de ser o disco e passa a ser a banda de upload residencial, que é assimétrica e não escala como a de um data center. Nesse cenário — equipe grande, volume alto e constante de arquivo bruto — a nuvem alugada com replicação em múltiplos data centers ainda compensa a mensalidade; a estante própria continua sendo a escolha certa para o Artesão solo e para o time pequeno deste capítulo, não para a operação em escala.

## 6. Conclusão

Este capítulo fechou duas das trocas mais emocionais da oficina. Na edição de vídeo, você aprendeu a diferença entre o gratuito que é seu (Shotcut e Kdenlive, GPLv3, com limites documentados e honestos) e o gratuito que é vitrine de outra loja (DaVinci Resolve, proprietário, com tetos calibrados para empurrar a versão paga) [135][137]. Na nuvem, você montou a estante central com Nextcloud ou Seafile, e aprendeu o orçamento oculto: disco, backup e banda que a mensalidade comprava silenciosamente agora são contas suas — mas são contas que você enxerga, mede e decide [141][145]. E descobriu a regra que vale para a oficina inteira: sincronizar replica, backup preserva, e a única cópia que sobrevive a um desastre é a que está fora do ambiente [149][150].

O Artesão Digital que sai deste capítulo não é o que acha que "open source é grátis". É o que sabe orçar a manutenção, distingue posse real de vitrine gratuita, e calcula — ferramenta por ferramenta — quando a troca vale o esforço. Essa régua é exatamente a que o próximo capítulo vai usar para medir as peças que organizam e analisam o trabalho da oficina: BI e gestão de projetos sem licença por usuário.

## 7. Referências Bibliográficas

[126] SHOTCUT.ORG. *Frequently Asked Questions*. Disponível em: https://www.shotcut.org/FAQ/. Acesso em: 19 ago. 2026.
[127] AXON, Samuel. *Shotcut review: This open-source video editor is impressive*. PCWorld. Disponível em: https://www.pcworld.com/article/407690/shotcut-review.html. Acesso em: 19 ago. 2026.
[128] TECHRADAR. *Shotcut review*. Disponível em: https://www.techradar.com/reviews/shotcut. Acesso em: 19 ago. 2026.
[129] MLTFRAMEWORK. *Issue #1786: Shotcut crashes when adding or keeping a long video file on timeline*. Disponível em: https://github.com/mltframework/shotcut/issues/1786. Acesso em: 19 ago. 2026.
[130] KDE. *kdenlive: Free and open source video editor, based on MLT Framework and KDE Frameworks*. Disponível em: https://github.com/KDE/kdenlive. Acesso em: 19 ago. 2026.
[131] KDE. *Installation — Kdenlive 26.04 Manual*. Disponível em: https://docs.kdenlive.org/en/getting_started/installation.html. Acesso em: 19 ago. 2026.
[132] KDENLIVE.ORG. *Kdenlive 25.08.1 released*. Disponível em: https://kdenlive.org/news/releases/25.08.1/. Acesso em: 19 ago. 2026.
[133] KDE. *Bug 462777 — kdenlive crashes after a few clicks on the clips in the timeline*. Disponível em: https://bugs.kde.org/show_bug.cgi?id=462777. Acesso em: 19 ago. 2026.
[134] FIXTHEPHOTO. *Kdenlive vs Adobe Premiere Pro: Which Is NOT Intuitive?*. Disponível em: https://fixthephoto.com/kdenlive-vs-adobe-premiere-pro.html. Acesso em: 19 ago. 2026.
[135] BLACKMAGIC DESIGN. *DaVinci Resolve*. Disponível em: https://www.blackmagicdesign.com/products/davinciresolve. Acesso em: 19 ago. 2026.
[136] TECHRADAR. *DaVinci Resolve 21 (2026) review: Our top free video editing app gets big improvements*. Disponível em: https://www.techradar.com/pro/software-services/davinci-resolve-21-2026-video-editing-software-review. Acesso em: 19 ago. 2026.
[137] TOOLFARM. *In Depth: DaVinci Resolve Studio vs Free (Updated for 21)*. Disponível em: https://www.toolfarm.com/tutorial/in-depth-davinci-resolve-studio-vs-the-free-version/. Acesso em: 19 ago. 2026.
[138] DIGITAL CAMERA WORLD. *DaVinci Resolve 18 free vs Resolve Studio 18: which is the best option for you?*. Disponível em: https://www.digitalcameraworld.com/buying-guides/davinci-resolve-18-free-vs-resolve-studio-18-which-is-the-best-option-for-you. Acesso em: 19 ago. 2026.
[139] NEXTCLOUD. *server: Nextcloud server, a safe home for all your data*. Disponível em: https://github.com/nextcloud/server. Acesso em: 19 ago. 2026.
[140] NEXTCLOUD. *System requirements — Nextcloud Administration Manual*. Disponível em: https://docs.nextcloud.com/server/stable/admin_manual/installation/system_requirements.html. Acesso em: 19 ago. 2026.
[141] NEXTCLOUD. *Installation and server configuration — Nextcloud Administration Manual*. Disponível em: https://docs.nextcloud.com/server/stable/admin_manual/installation/index.html. Acesso em: 19 ago. 2026.
[142] CYBERINSIDER. *Nextcloud Review (2026 Test Results)*. Disponível em: https://cyberinsider.com/cloud-storage/reviews/nextcloud/. Acesso em: 19 ago. 2026.
[143] CONTABO. *Nextcloud vs. Competitors: A Deep Dive into Self-Hosted Alternatives*. Disponível em: https://contabo.com/blog/nextcloud-vs-competitors/. Acesso em: 19 ago. 2026.
[144] HAIWEN. *seafile-server: Seafile Server Core*. Disponível em: https://github.com/haiwen/seafile-server. Acesso em: 19 ago. 2026.
[145] SEAFILE. *System requirements — Seafile Admin Manual*. Disponível em: https://manual.seafile.com/13.0/setup/system_requirements/. Acesso em: 19 ago. 2026.
[146] PROPRIVACY. *Seafile Review*. Disponível em: https://proprivacy.com/cloud/review/seafile. Acesso em: 19 ago. 2026.
[147] CLOUDBASEDBACKUP. *Nextcloud vs Seafile: Which Cloud Storage Is Better*. Disponível em: https://cloudbasedbackup.com/en/blog/nextcloud-vs-seafile-which-cloud-storage-is-better. Acesso em: 19 ago. 2026.
[148] SYNCTHING. *syncthing: Open Source Continuous File Synchronization*. Disponível em: https://github.com/syncthing/syncthing. Acesso em: 19 ago. 2026.
[149] SYNCTHING. *Getting Started — Syncthing documentation*. Disponível em: https://docs.syncthing.net/intro/getting-started.html. Acesso em: 19 ago. 2026.
[150] SYNCTHING. *Security Principles — Syncthing documentation*. Disponível em: https://docs.syncthing.net/users/security.html. Acesso em: 19 ago. 2026.
[151] XDA DEVELOPERS. *I replaced Dropbox with Syncthing, and learned these 5 things*. Disponível em: https://www.xda-developers.com/replaced-dropbox-with-syncthing-learned-these-things/. Acesso em: 19 ago. 2026.
[152] SPEED-DRAIN. *Best Self-Hosted Cloud Storage 2026: Nextcloud vs Seafile vs Syncthing Comparison*. Disponível em: https://speed-drain.com/blog/best-self-hosted-cloud-storage-2026-nextcloud-seafile-syncthing/. Acesso em: 19 ago. 2026.