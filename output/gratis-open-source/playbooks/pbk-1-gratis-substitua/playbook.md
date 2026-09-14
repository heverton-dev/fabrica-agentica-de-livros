---
title: "Playbook — Grátis: Substitua Ferramentas Pagas por Open Source de Verdade"
subtitle: "Guia de bancada · 8 passos práticos"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Objetivo do Material

Apresentar o argumento central do livro: o software 'grátis para sempre' que a internet promete geralmente cobra em outra moeda — tempo de administração —, e preparar o leitor para decidir, categoria por categoria, quando essa troca vale a pena e quando não vale.

# Como usar este playbook

Você é o **Artesão Digital**. Cada passo é um card independente com sete partes: objetivo, pré-requisito, entregas, execução, gate de verificação, critério de conclusão e armadilhas.

Este documento **não repete a teoria** do livro. Quando precisar do porquê, siga a referência cruzada do card para o capítulo correspondente.

# Mapa dos Estágios

| # | Estágio | Passos |
|---|---|---|
| 1 | Oficina | 1, 2, 3, 4 |
| 2 | Bancada | 5, 6, 7, 8 |

# Passos Práticos

## Passo 1 — Anotações e Produtividade: Saindo do Aluguel do Notion e do Evernote

> **Estágio:** Oficina  ·  **Origem:** Cap. 1 — Anotações e Produtividade: Saindo do Aluguel do Notion e do Evernote

### ① Objetivo do passo

Apresentar a lógica geral da troca (o que se ganha, o que se perde) através do caso mais comum — notas e produtividade — e guiar a instalação da primeira alternativa self-hosted.

### ② Pré-requisito

Nenhum — este é o ponto de partida

### ③ Entregas

- `docker-compose.yml`

### ④ Execução

**Preparando a Bancada: Requisitos Antes de Montar Qualquer Peça**

```console
$ docker --version
Docker version 24.0.7, build afdd53b
$ docker compose version
Docker Compose version v2.23.0
```

**Montando o AppFlowy Self-Hosted**

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

**As Outras Cinco Peças da Bancada**

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

### ⑤ Verificação / Gate

```bash
docker --version
```

### ⑥ Feito quando…

- [ ] Colaboração em tempo real polida** é onde toda a categoria perde para o Notion. AppFlowy até cobre parte disso, mas Logseq, Trilium Notes e Standard Notes são desenhados como local-first e não escalam para edição multiusuário simultânea — no caso do Trilium, essa limitação nem é um roadmap futuro, é uma decisão de design definitiva do mantenedor [26]. Não force esse uso: equipes que dependem de colaboração ao vivo devem manter a ferramenta paga para esse fluxo específico, mesmo adotando alternativas abertas para o resto [5]
- [ ] Apps mobile maduros** são o segundo limite real. O comparativo entre AppFlowy e Notion aponta especificamente o aplicativo mobile como sensivelmente menos polido que o do concorrente pago [19], e o Trilium Notes simplesmente não tem app mobile oficial [26]. Se sua equipe trabalha primariamente em celular, teste esse fluxo específico antes de migrar — não assuma que a experiência desktop se repete lá
- [ ] OCR e busca em anexos de nível Evernote** ainda não têm equivalente maduro nesta lista. O Joplin oferece um plugin de OCR desde a versão 2.14, mas com desempenho fraco em imagens complexas, e sem a busca full-text robusta em anexos que o Evernote entrega nativamente [10][9]. Quem depende de digitalizar recibos, cartões de visita ou documentos escaneados como parte do fluxo de trabalho principal ainda sente essa lacuna

### ⑦ Armadilhas

- _(a completar)_

## Passo 2 — E-mail Marketing: Enviando Campanhas Sem Depender do Mailchimp

> **Estágio:** Oficina  ·  **Origem:** Cap. 2 — E-mail Marketing: Enviando Campanhas Sem Depender do Mailchimp

### ① Objetivo do passo

Ensinar a montar uma stack própria de e-mail marketing e a lidar com o desafio real dessa categoria — reputação de domínio e deliverability.

### ② Pré-requisito

Passo 1 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**O selo de garantia: publicando SPF, DKIM e DMARC**

```yaml
# registros-dns-campanhas.yaml
dominio: campanhas.suaoficina.com.br
registros:
  - tipo: TXT
    nome: campanhas.suaoficina.com.br
    valor: "v=spf1 include:_spf.postal.suaoficina.com.br ~all"
  - tipo: TXT
    nome: postal-dkim._domainkey.campanhas.suaoficina.com.br
    valor: "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC"
  - tipo: TXT
    nome: _dmarc.campanhas.suaoficina.com.br
    valor: "v=DMARC1; p=quarantine; rua=mailto:dmarc@suaoficina.com.br"
```

**Montando a bancada: Listmonk, Mautic e Postal — o que cada um resolve**

```yaml
# docker-compose.yml
services:
  listmonk-db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: listmonk
      POSTGRES_PASSWORD: "<senha-forte-aqui>"
      POSTGRES_DB: listmonk
    volumes:
      - listmonk-data:/var/lib/postgresql/data
  listmonk:
    image: listmonk/listmonk:latest
    restart: unless-stopped
    ports:
      - "9000:9000"
    environment:
      LISTMONK_db__user: listmonk
      LISTMONK_db__password: "<senha-forte-aqui>"
      LISTMONK_db__database: listmonk
      LISTMONK_db__host: listmonk-db
    depends_on:
      - listmonk-db
volumes:
  listmonk-data:
```

**Auditando a licença: o contraexemplo do EmailEngine e o alerta do Mailtrain**

```json
{
  "ferramenta": "EmailEngine",
  "licenca": "source-available (nao FOSS)",
  "trial_dias": 14,
  "ultimo_release": "ativo, mas sob licenca comercial apos o trial",
  "veredito": "nao usar como base gratuita de producao"
}
```

### ⑤ Verificação / Gate

```bash
docker compose run --rm listmonk ./listmonk --install
```

### ⑥ Feito quando…

- [ ] Publique os três registros DNS (SPF, DKIM, DMARC) do seu domínio de envio e confirme a propagação com `dig` ou `nslookup`
- [ ] Suba o Listmonk com Docker Compose, rode o instalador e envie uma campanha de teste para uma lista pequena (menos de 20 contatos)
- [ ] Rode o script `validar_spf` deste capítulo contra o registro SPF real do seu domínio
- [ ] Monte o checklist de auditoria de licença (formato JSON deste capítulo) para duas ferramentas "open source" que você usa ou pretende usar

### ⑦ Armadilhas

- _(a completar)_

## Passo 3 — CRM: Vendendo e Atendendo Sem Pagar Salesforce

> **Estágio:** Oficina  ·  **Origem:** Cap. 3 — CRM: Vendendo e Atendendo Sem Pagar Salesforce

### ① Objetivo do passo

Mostrar até onde um CRM open source cobre as funções essenciais de vendas e atendimento, e onde a lacuna com as soluções corporativas ainda é real.

### ② Pré-requisito

Passo 2 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**O que a gaveta de automação já resolve sem você escrever uma linha de código**

```json
{
  "event": "Opportunity.stageChanged",
  "entityId": "64f21a3b9c7d4",
  "previousStage": "Negotiation",
  "currentStage": "ClosedWon",
  "daysInPreviousStage": 9,
  "ownerId": "usr-0231"
}
```

**Colocando o EspoCRM de pé com Docker**

```yaml
version: "3.8"
services:
  espocrm:
    image: espocrm/espocrm:latest
    ports:
      - "8080:80"
    environment:
      ESPOCRM_DATABASE_HOST: espocrm-db
      ESPOCRM_DATABASE_NAME: espocrm
      ESPOCRM_DATABASE_USER: espocrm
      ESPOCRM_DATABASE_PASSWORD: "<sua-senha-forte>"
      ESPOCRM_ADMIN_USERNAME: admin
      ESPOCRM_ADMIN_PASSWORD: "<senha-do-admin>"
      ESPOCRM_SITE_URL: "http://localhost:8080"
    volumes:
      - espocrm-data:/var/www/html
    depends_on:
      - espocrm-db
  espocrm-db:
    image: mariadb:10.11
    environment:
      MARIADB_ROOT_PASSWORD: "<senha-root>"
      MARIADB_DATABASE: espocrm
      MARIADB_USER: espocrm
      MARIADB_PASSWORD: "<sua-senha-forte>"
    volumes:
      - espocrm-db-data:/var/lib/mysql
volumes:
  espocrm-data:
  espocrm-db-data:
```

**Twenty: a bancada mais nova, com a fatura de infraestrutura mais alta**

```bash
#!/usr/bin/env bash
RAM_MB=$(free -m 2>/dev/null | awk '/^Mem:/ {print $2}')
RAM_MB=${RAM_MB:-0}
if [ "$RAM_MB" -ge 2048 ]; then
  echo "RAM suficiente para o Twenty (Docker Compose oficial)"
else
  echo "RAM insuficiente para o Twenty - prefira EspoCRM ou SuiteCRM neste servidor"
fi
```

### ⑤ Verificação / Gate

```bash
docker compose up -d
```

### ⑥ Feito quando…

- [ ] Migrar contatos e negócios de uma planilha ou de outro CRM sem mapear os campos personalizados antes — o resultado é um funil com metade dos negócios "sem estágio definido"
- [ ] Subestimar o tempo de configuração de automação de e-mail transacional: o EspoCRM já inclui campanhas de e-mail na base gratuita [5], mas a configuração de SMTP e autenticação de domínio (o mesmo tema do Capítulo 2) continua sendo seu trabalho
- [ ] Escolher a ferramenta pela nota de benchmark de código sem checar a nota de maturidade de mercado: o Twenty tem ótimo código [4], mas ainda carece de recursos que uma equipe de vendas grande considera básicos [11]

### ⑦ Armadilhas

- _(a completar)_

## Passo 4 — Automação de Fluxos: Trocando o Zapier pelo n8n

> **Estágio:** Oficina  ·  **Origem:** Cap. 4 — Automação de Fluxos: Trocando o Zapier pelo n8n

### ① Objetivo do passo

Demonstrar por que a automação de fluxos é a categoria mais madura da lista, guiando a construção do primeiro fluxo de ponta a ponta.

### ② Pré-requisito

Passo 3 concluído

### ③ Entregas

- `docker-compose.yml`

### ④ Execução

**Por que Docker e por que PostgreSQL desde o primeiro dia**

```yaml
# docker-compose.yml — bancada minima para produção do n8n
version: "3.8"

services:
  postgres:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: "troque-esta-senha-no-deploy"
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data

  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_DATABASE: n8n
      DB_POSTGRESDB_USER: n8n
      DB_POSTGRESDB_PASSWORD: "troque-esta-senha-no-deploy"
      N8N_ENCRYPTION_KEY: "<chave-de-32-caracteres-gerada-no-deploy>"
      WEBHOOK_URL: "https://automacao.suaoficina.com.br/"
      GENERIC_TIMEZONE: "America/Sao_Paulo"
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

volumes:
  postgres_data:
  n8n_data:
```

**Subindo a bancada e testando o primeiro gatilho**

```console
$ docker compose up -d
[+] Running 2/2
 - Container oficina-postgres-1  Started
 - Container oficina-n8n-1       Started

$ docker compose ps
NAME               IMAGE                         STATUS
oficina-postgres-1 postgres:16                   Up 12 seconds (healthy)
oficina-n8n-1      docker.n8n.io/n8nio/n8n:latest Up 10 seconds

$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5678/healthz
200
```

**O fluxo de ponta a ponta: gatilho, nó, credencial e deploy**

```json
{
  "name": "Pedido recebido -> normaliza -> reenvia",
  "nodes": [
    {
      "id": "gatilho-webhook",
      "name": "Gatilho: Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [240, 300],
      "parameters": {
        "path": "pedido-novo",
        "httpMethod": "POST",
        "responseMode": "lastNode"
      }
    },
    {
      "id": "no-transformacao",
      "name": "Normaliza payload",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [460, 300],
      "parameters": {
        "assignments": {
          "assignments": [
            { "name": "cliente", "type": "string", "value": "={{$json.nome}}" },
            { "name": "valor_pedido", "type": "number", "value": "={{$json.total}}" }
          ]
        }
      }
    },
    {
      "id": "no-autenticado",
      "name": "Reenvia com credencial",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [680, 300],
      "parameters": {
        "method": "POST",
        "url": "https://api.parceiro-externo.com/pedidos",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth"
      },
      "credentials": {
        "httpHeaderAuth": {
          "id": "1",
          "name": "Cofre - Parceiro Externo"
        }
      }
    }
  ],
  "connections": {
    "Gatilho: Webhook": {
      "main": [[{ "node": "Normaliza payload", "type": "main", "index": 0 }]]
    },
    "Normaliza payload": {
      "main": [[{ "node": "Reenvia com credencial", "type": "main", "index": 0 }]]
    }
  }
}
```

**Backup da bancada: o script que evita perder o fluxo montado**

```bash
#!/usr/bin/env bash
set -euo pipefail

DATA=$(date +%F)
DESTINO="/backups/n8n/n8n-${DATA}.sql.gz"

mkdir -p /backups/n8n

docker exec oficina-postgres-1 pg_dump -U n8n n8n | gzip > "${DESTINO}"

echo "Backup gravado em ${DESTINO}"

find /backups/n8n -name "n8n-*.sql.gz" -mtime +30 -delete
```

### ⑤ Verificação / Gate

```bash
docker compose up -d
```

### ⑥ Feito quando…

- [ ] Suba o `docker-compose.yml` desta seção em uma VPS de teste (2 GB RAM é suficiente para começar)
- [ ] Importe o fluxo JSON do webhook e ative-o
- [ ] Dispare o webhook com `curl` usando um payload diferente do exemplo e confirme a resposta
- [ ] Crie a credencial do nó `HTTP Request` pelo painel de credenciais do n8n — nunca em texto livre no nó
- [ ] Configure o script de backup via `cron` e confirme que o arquivo `.sql.gz` é gerado no dia seguinte
- [ ] Escreva, em uma frase, quem na sua equipe (ou você mesmo) fica de guarda se esse fluxo falhar às 3h da manhã

### ⑦ Armadilhas

- _(a completar)_

## Passo 5 — Design Gráfico e Edição de Imagem: Sem Canva, Sem Photoshop, Sem Illustrator

> **Estágio:** Bancada  ·  **Origem:** Cap. 5 — Design Gráfico e Edição de Imagem: Sem Canva, Sem Photoshop, Sem Illustrator

### ① Objetivo do passo

Apresentar as ferramentas open source de design e imagem com curva de aprendizado honesta, do zero até uma peça de marketing pronta.

### ② Pré-requisito

Passo 4 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Instalando as Peças Desktop: GIMP, Inkscape e Krita**

```console
$ winget install GIMP.GIMP
$ winget install Inkscape.Inkscape
$ winget install KDE.Krita
```

**Subindo o Penpot com Docker Compose**

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

**A Automação da Bancada: Scripts que Preparam e Exportam**

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

### ⑤ Verificação / Gate

```bash
docker compose up -d
```

### ⑥ Feito quando…

- [ ] Trocar a ferramenta pelo fluxo errado**: usar o GIMP para desenhar um logotipo que vai ser impresso em vários tamanhos. Logotipo é vetor — a peça certa é o Inkscape, que exporta SVG e escala sem perda [14]. O GIMP é raster; ampliar um logotipo em raster é pedir serrilhado
- [ ] Prometer paridade CMYK para a gráfica**: GIMP e Inkscape não têm suporte nativo a CMYK [11][13][17]. Se o seu fluxo principal é impressão profissional certificada, essa é a lacuna honesta — mantenha o aluguel para esse fluxo específico ou contorne com plugins e ferramentas auxiliares, e deixe isso combinado com a gráfica antes de prometer a troca para o time
- [ ] Depender de IA generativa**: o Generative Fill do Photoshop não tem equivalente maduro nas quatro ferramentas [11][13]. Se a sua rotina depende de preenchimento generativo de imagens, nenhuma das peças desta bancada substitui esse fluxo hoje — planeje o contorno (remover o elemento manualmente com carimbo e clonagem) antes de migrar
- [ ] Subestimar o ecossistema**: o Penpot tem base de usuários menor e menos plugins de terceiros que o Figma, e o Canva vende templates prontos que não têm equivalente direto [6][7]. Times que vivem de marketplace de plugins ou de templates prontos vão sentir a troca — o contorno é construir a sua própria biblioteca de componentes no Penpot, e isso também é trabalho de bancada

### ⑦ Armadilhas

- _(a completar)_

## Passo 6 — Vídeo e Nuvem: Editando e Guardando Seus Arquivos Sem Assinatura

> **Estágio:** Bancada  ·  **Origem:** Cap. 6 — Vídeo e Nuvem: Editando e Guardando Seus Arquivos Sem Assinatura

### ① Objetivo do passo

Cobrir edição de vídeo e armazenamento em nuvem self-hosted, sinalizando com precisão os casos em que 'open source' é rótulo incorreto.

### ② Pré-requisito

Passo 5 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Montando a Bancada de Vídeo**

```console
$ uname -a
Linux oficina 6.8.0-45-generic #45-Ubuntu SMP x86_64 GNU/Linux
$ free -h
               total        used        free
Mem:           15GiB       3,2GiB       11GiB
$ glxinfo | grep "OpenGL version"
OpenGL version string: 4.6 (Core Profile) Mesa 24.0.5
```

**A Estante Central: Nextcloud Self-Hosted**

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

**A Prateleira Externa: Backup com a Regra 3-2-1**

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

**Vídeo Não É Só Cortar: O Fluxo de Produção Completo**

```console
$ ffprobe -v error -show_entries format=duration,bit_rate -of default=noprint_wrappers=1 projeto-final.mp4
duration=300.500000
bit_rate=8250000
$ ls -lh projeto-final.mp4
-rw-r--r-- 1 artesao artesao 313M ago 20 07:00 projeto-final.mp4
```

### ⑤ Verificação / Gate

```bash
docker compose up -d
```

### ⑥ Feito quando…

- [ ] A jornada prática deste capítulo é a primeira semana do Artesão Digital migrando vídeo
- [ ] O cenário: você terminou de editar um vídeo curto para o canal da sua área — algo de cinco minutos
- [ ] Erro comum:** você confia na sincronização como se ela fosse backup
- [ ] Edita o vídeo direto da pasta sincronizada do Nextcloud em dois dispositivos
- [ ] O diagnóstico é sempre o mesmo: sincronizar replica
- [ ] São funções diferentes
- [ ] Prática correta:** a pasta sincronizada recebe apenas o material de trabalho corrente

### ⑦ Armadilhas

- _(a completar)_

## Passo 7 — Análise de Dados e Gestão de Projetos: BI e Kanban Sem Licença por Usuário

> **Estágio:** Bancada  ·  **Origem:** Cap. 7 — Análise de Dados e Gestão de Projetos: BI e Kanban Sem Licença por Usuário

### ① Objetivo do passo

Cobrir ferramentas de BI self-hosted e de gestão de projetos, incluindo o alerta de risco de longevidade de projetos com manutenção incerta.

### ② Pré-requisito

Passo 6 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Subindo o Metabase**

```yaml
# docker-compose.yml — Metabase (referência mínima de produção)
version: "3.9"

services:
  metabase:
    image: metabase/metabase:latest
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      MB_DB_TYPE: postgres
      MB_DB_DBNAME: metabase
      MB_DB_PORT: 5432
      MB_DB_USER: metabase
      MB_DB_PASS: troque-esta-senha
      MB_DB_HOST: db
    volumes:
      - metabase-data:/metabase.db
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: metabase
      POSTGRES_USER: metabase
      POSTGRES_PASSWORD: troque-esta-senha
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  metabase-data:
  db-data:
```

**A Bancada de Gestão: OpenProject**

```yaml
# docker-compose.yml — OpenProject (Community Edition)
version: "3.9"

services:
  openproject:
    image: openproject/openproject:16
    restart: unless-stopped
    ports:
      - "8080:80"
    environment:
      OPENPROJECT_HOST: projetos.suaoficina.com
      OPENPROJECT_SECRET_KEY_BASE: troque-esta-chave
    volumes:
      - op-pgdata:/var/lib/postgresql/14/main
      - op-assets:/var/db/openproject
    command: docker/production/install

volumes:
  op-pgdata:
  op-assets:
```

**O Caminho do Superset: Quando o Analytics Precisa de Profundidade**

```console
$ docker compose -f docker-compose.yml up -d
[+] Running 4/4
 ✔ Container superset_db         Started
 ✔ Container superset_cache      Started
 ✔ Container superset_worker     Started
 ✔ Container superset_app        Started
$ docker compose exec superset_app superset fab create-admin \
    --username artesao --firstname Artesao --lastname Digital \
    --email artesao@oficina.com --password troque-esta-senha
$ docker compose exec superset_app superset init
```

**O Ciclo de Vida de um Relatório: Do Banco ao E-mail Agendado**

```console
$ curl -s -X POST http://localhost:3000/api/pulse \
  -H "X-Metabase-Session: SESS_ID" \
  -H "Content-Type: application/json" \
  -d '{"name":"Relatorio semanal de vendas","channel_specs":{"email":{"recipients":["gestor@oficina.com"]}},"cards":[{"id":1,"include_csv":true}],"schedule_type":"weekly","schedule_day":"mon","schedule_hour":8}'
{"id":42,"name":"Relatorio semanal de vendas","schedule_type":"weekly"}
```

### ⑤ Verificação / Gate

```bash
docker compose up -d
```

### ⑥ Feito quando…

- [ ] A jornada prática deste capítulo é a primeira semana do Artesão Digital medindo
- [ ] O cenário: você tem vendas acontecendo — o produto digital que o livro deu condições de criar —
- [ ] Os dados estão espalhados entre uma planilha
- [ ] Erro comum:** você escolhe o BI pelo nome — "Tableau é o que as empresas usam" — ou pelo preço zero
- [ ] O primeiro erro paga mensalidade por assento para sempre
- [ ] O segundo pendura na parede uma peça cuja manutenção morreu
- [ ] É exatamente o que acontece com o Redash: quem montou a stack em 2019

### ⑦ Armadilhas

- _(a completar)_

## Passo 8 — Comunicação em Equipe e a Infraestrutura Que Sustenta Tudo

> **Estágio:** Bancada  ·  **Origem:** Cap. 8 — Comunicação em Equipe e a Infraestrutura Que Sustenta Tudo

### ① Objetivo do passo

Encerrar a jornada mostrando a peça que sustenta todas as anteriores — a infraestrutura self-hosted —, e entregar ao leitor um balanço final de quando a troca vale o esforço.

### ② Pré-requisito

Passo 7 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**A Bancada Que Hospeda Tudo: Mattermost + Docker**

```yaml
# docker-compose.yml — Mattermost (time pequeno)
version: "3.9"

services:
  mm-postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: mattermost
      POSTGRES_USER: mmuser
      POSTGRES_PASSWORD: troque-esta-senha
    volumes:
      - pgdata:/var/lib/postgresql/data

  mattermost:
    image: mattermost/mattermost-team-edition:latest
    restart: unless-stopped
    ports:
      - "8065:8065"
    environment:
      MM_SQLSETTINGS_DRIVERNAME: postgres
      MM_SQLSETTINGS_DATASOURCE: postgres://mmuser:troque-esta-senha@mm-postgres:5432/mattermost?sslmode=disable
      MM_SERVICESETTINGS_SITEURL: http://chat.suaoficina.com
    volumes:
      - mmdata:/mattermost/data
    depends_on:
      - mm-postgres

volumes:
  pgdata:
  mmdata:
```

**O Deploy na Camada PaaS: Dokku**

```console
$ dokku apps:create oficina-chat
Creating oficina-chat... done

$ dokku postgres:create chat-db
       Waiting for container to be ready... done
$ dokku postgres:link chat-db oficina-chat

$ dokku domains:add oficina-chat chat.suaoficina.com
-----> Added chat.suaoficina.com to oficina-chat

$ git push dokku main
-----> Building oficina-chat from buildpacks...
-----> Deploying oficina-chat to dokku
=====> Application deployed:
       http://chat.suaoficina.com
```

**O Armário com Painel: Coolify para Quem Quer Ver Tudo**

```console
$ sudo curl -fsSL https://coolify.io/install.sh | bash
[INFO] Installing Docker Engine...
[INFO] Installing Coolify v4.x...
[INFO] Coolify is ready: http://192.168.0.10:8000
$ curl -sI http://192.168.0.10:8000 | head -1
HTTP/1.1 200 OK
```

**A Segurança da Oficina: Atualização e Acesso**

```console
$ sudo apt update && sudo apt upgrade -y
$ cd /srv/oficina && docker compose pull
$ docker compose up -d
$ curl -sI https://chat.suaoficina.com | head -1
HTTP/1.1 200 OK
```

### ⑤ Verificação / Gate

```bash
docker compose up -d
```

### ⑥ Feito quando…

- [ ] A assinatura cobra por usuário? Some o custo anual de todo o time
- [ ] A alternativa open source tem manutenção ativa? Olhe o repositório e o changelog — a lição do Redash do capítulo 7
- [ ] A equipe depende de integrações prontas ou recursos exclusivos da loja? Video nativo, conectores, marketplace
- [ ] Alguém assume o plantão de atualizações, backup e segurança? Sem dono, não há troca
- [ ] A soma VPS + manutenção + risco fica abaixo da assinatura? Só então a peça é sua

### ⑦ Armadilhas

- _(a completar)_

# Checklist Mestre

**Passo 1 — Anotações e Produtividade: Saindo do Aluguel do Notion e do Evernote**

- [ ] Colaboração em tempo real polida** é onde toda a categoria perde para o Notion. AppFlowy até cobre parte disso, mas Logseq, Trilium Notes e Standard Notes são desenhados como local-first e não escalam para edição multiusuário simultânea — no caso do Trilium, essa limitação nem é um roadmap futuro, é uma decisão de design definitiva do mantenedor [26]. Não force esse uso: equipes que dependem de colaboração ao vivo devem manter a ferramenta paga para esse fluxo específico, mesmo adotando alternativas abertas para o resto [5]
- [ ] Apps mobile maduros** são o segundo limite real. O comparativo entre AppFlowy e Notion aponta especificamente o aplicativo mobile como sensivelmente menos polido que o do concorrente pago [19], e o Trilium Notes simplesmente não tem app mobile oficial [26]. Se sua equipe trabalha primariamente em celular, teste esse fluxo específico antes de migrar — não assuma que a experiência desktop se repete lá
- [ ] OCR e busca em anexos de nível Evernote** ainda não têm equivalente maduro nesta lista. O Joplin oferece um plugin de OCR desde a versão 2.14, mas com desempenho fraco em imagens complexas, e sem a busca full-text robusta em anexos que o Evernote entrega nativamente [10][9]. Quem depende de digitalizar recibos, cartões de visita ou documentos escaneados como parte do fluxo de trabalho principal ainda sente essa lacuna

**Passo 2 — E-mail Marketing: Enviando Campanhas Sem Depender do Mailchimp**

- [ ] Publique os três registros DNS (SPF, DKIM, DMARC) do seu domínio de envio e confirme a propagação com `dig` ou `nslookup`
- [ ] Suba o Listmonk com Docker Compose, rode o instalador e envie uma campanha de teste para uma lista pequena (menos de 20 contatos)
- [ ] Rode o script `validar_spf` deste capítulo contra o registro SPF real do seu domínio
- [ ] Monte o checklist de auditoria de licença (formato JSON deste capítulo) para duas ferramentas "open source" que você usa ou pretende usar

**Passo 3 — CRM: Vendendo e Atendendo Sem Pagar Salesforce**

- [ ] Migrar contatos e negócios de uma planilha ou de outro CRM sem mapear os campos personalizados antes — o resultado é um funil com metade dos negócios "sem estágio definido"
- [ ] Subestimar o tempo de configuração de automação de e-mail transacional: o EspoCRM já inclui campanhas de e-mail na base gratuita [5], mas a configuração de SMTP e autenticação de domínio (o mesmo tema do Capítulo 2) continua sendo seu trabalho
- [ ] Escolher a ferramenta pela nota de benchmark de código sem checar a nota de maturidade de mercado: o Twenty tem ótimo código [4], mas ainda carece de recursos que uma equipe de vendas grande considera básicos [11]

**Passo 4 — Automação de Fluxos: Trocando o Zapier pelo n8n**

- [ ] Suba o `docker-compose.yml` desta seção em uma VPS de teste (2 GB RAM é suficiente para começar)
- [ ] Importe o fluxo JSON do webhook e ative-o
- [ ] Dispare o webhook com `curl` usando um payload diferente do exemplo e confirme a resposta
- [ ] Crie a credencial do nó `HTTP Request` pelo painel de credenciais do n8n — nunca em texto livre no nó
- [ ] Configure o script de backup via `cron` e confirme que o arquivo `.sql.gz` é gerado no dia seguinte
- [ ] Escreva, em uma frase, quem na sua equipe (ou você mesmo) fica de guarda se esse fluxo falhar às 3h da manhã

**Passo 5 — Design Gráfico e Edição de Imagem: Sem Canva, Sem Photoshop, Sem Illustrator**

- [ ] Trocar a ferramenta pelo fluxo errado**: usar o GIMP para desenhar um logotipo que vai ser impresso em vários tamanhos. Logotipo é vetor — a peça certa é o Inkscape, que exporta SVG e escala sem perda [14]. O GIMP é raster; ampliar um logotipo em raster é pedir serrilhado
- [ ] Prometer paridade CMYK para a gráfica**: GIMP e Inkscape não têm suporte nativo a CMYK [11][13][17]. Se o seu fluxo principal é impressão profissional certificada, essa é a lacuna honesta — mantenha o aluguel para esse fluxo específico ou contorne com plugins e ferramentas auxiliares, e deixe isso combinado com a gráfica antes de prometer a troca para o time
- [ ] Depender de IA generativa**: o Generative Fill do Photoshop não tem equivalente maduro nas quatro ferramentas [11][13]. Se a sua rotina depende de preenchimento generativo de imagens, nenhuma das peças desta bancada substitui esse fluxo hoje — planeje o contorno (remover o elemento manualmente com carimbo e clonagem) antes de migrar
- [ ] Subestimar o ecossistema**: o Penpot tem base de usuários menor e menos plugins de terceiros que o Figma, e o Canva vende templates prontos que não têm equivalente direto [6][7]. Times que vivem de marketplace de plugins ou de templates prontos vão sentir a troca — o contorno é construir a sua própria biblioteca de componentes no Penpot, e isso também é trabalho de bancada

**Passo 6 — Vídeo e Nuvem: Editando e Guardando Seus Arquivos Sem Assinatura**

- [ ] A jornada prática deste capítulo é a primeira semana do Artesão Digital migrando vídeo
- [ ] O cenário: você terminou de editar um vídeo curto para o canal da sua área — algo de cinco minutos
- [ ] Erro comum:** você confia na sincronização como se ela fosse backup
- [ ] Edita o vídeo direto da pasta sincronizada do Nextcloud em dois dispositivos
- [ ] O diagnóstico é sempre o mesmo: sincronizar replica
- [ ] São funções diferentes
- [ ] Prática correta:** a pasta sincronizada recebe apenas o material de trabalho corrente

**Passo 7 — Análise de Dados e Gestão de Projetos: BI e Kanban Sem Licença por Usuário**

- [ ] A jornada prática deste capítulo é a primeira semana do Artesão Digital medindo
- [ ] O cenário: você tem vendas acontecendo — o produto digital que o livro deu condições de criar —
- [ ] Os dados estão espalhados entre uma planilha
- [ ] Erro comum:** você escolhe o BI pelo nome — "Tableau é o que as empresas usam" — ou pelo preço zero
- [ ] O primeiro erro paga mensalidade por assento para sempre
- [ ] O segundo pendura na parede uma peça cuja manutenção morreu
- [ ] É exatamente o que acontece com o Redash: quem montou a stack em 2019

**Passo 8 — Comunicação em Equipe e a Infraestrutura Que Sustenta Tudo**

- [ ] A assinatura cobra por usuário? Some o custo anual de todo o time
- [ ] A alternativa open source tem manutenção ativa? Olhe o repositório e o changelog — a lição do Redash do capítulo 7
- [ ] A equipe depende de integrações prontas ou recursos exclusivos da loja? Video nativo, conectores, marketplace
- [ ] Alguém assume o plantão de atualizações, backup e segurança? Sem dono, não há troca
- [ ] A soma VPS + manutenção + risco fica abaixo da assinatura? Só então a peça é sua
