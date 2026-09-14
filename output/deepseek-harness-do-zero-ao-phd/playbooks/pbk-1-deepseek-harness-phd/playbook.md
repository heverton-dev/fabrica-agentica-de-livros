---
title: "Playbook — DeepSeek Harness: Do zero ao PhD"
subtitle: "Guia de bancada · 16 passos práticos"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Objetivo do Material

Apresentar o DeepSeek Harness como o framework que democratiza agentes de IA autonomos.

# Como usar este playbook

Você é o **Engenheiro de Agentes**. Cada passo é um card independente com sete partes: objetivo, pré-requisito, entregas, execução, gate de verificação, critério de conclusão e armadilhas.

Este documento **não repete a teoria** do livro. Quando precisar do porquê, siga a referência cruzada do card para o capítulo correspondente.

# Mapa dos Estágios

| # | Estágio | Passos |
|---|---|---|
| 1 | Kit de pecas | 1, 2, 3, 4 |
| 2 | Montagem | 5, 6, 7, 8 |
| 3 | Estacao de trabalho | 9, 10, 11, 12 |
| 4 | Calibracao | 13, 14, 15, 16 |

# Passos Práticos

## Passo 1 — O Que e o DeepSeek Harness: O Agente que e Plugin

> **Estágio:** Kit de pecas  ·  **Origem:** Cap. 1 — O Que e o DeepSeek Harness: O Agente que e Plugin

### ① Objetivo do passo

Entender a arquitetura plugin-first do DeepSeek Harness.

### ② Pré-requisito

Nenhum — este é o ponto de partida

### ③ Entregas

- _(a completar)_

### ④ Execução

**Estrutura de um Plugin Cordis**

```json
{
  "name": "meu-plugin",
  "version": "0.1.0",
  "description": "Plugin personalizado para o DeepSeek Harness",
  "main": "index.js",
  "cordis": {
    "provides": ["tool", "service"],
    "requires": ["model"],
    "lifecycle": {
      "ready": "onReady",
      "dispose": "onDispose"
    }
  }
}
```

**Registro de um Plugin**

```javascript
// index.js do plugin
export default function meuPlugin(ctx) {
  // Registra um serviço no contexto compartilhado
  ctx.service('minha-ferramenta', {
    execute(params) {
      // Lógica da ferramenta
      return { resultado: `Processado: ${params.input}` };
    }
  });

  // Escuta eventos de sessão
  ctx.on('session:turn', (event) => {
    console.log(`Novo turno iniciado: ${event.id}`);
  });

  // Registra efeito reversível
  ctx.effect(() => {
    // Setup
    console.log('Plugin instalado');
    return () => {
      // Teardown (quando o plugin for removido)
      console.log('Plugin removido');
    };
  });
}
```

**Modos de Execução na Prática**

```bash
# Modo Standard (padrão) — toolset completo
dsh --mode standard

# Modo Code — modelo gera código para orquestrar tools
dsh --mode code

# Modo Minimal — apenas shell + editor
dsh --mode minimal

# Modo Creator — usa profile personalizado
dsh --mode creator --profile meu-profile
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Você escolhe o modo Minimal porque "é mais leve"
- [ ] Três horas depois
- [ ] Você precisava do Standard o tempo todo
- [ ] O erro não foi escolher o modo errado — foi não entender o que cada modo oferece antes de começar
- [ ] O modo Minimal é excelente para benchmarks
- [ ] Se vai medir algo isolado
- [ ] Se vai repetir o mesmo workflow muitas vezes

### ⑦ Armadilhas

- _(a completar)_

## Passo 2 — Instalacao Local: Do Zero ao Primeiro dsh

> **Estágio:** Kit de pecas  ·  **Origem:** Cap. 2 — Instalacao Local: Do Zero ao Primeiro dsh

### ① Objetivo do passo

Instalar e executar o primeiro agente.

### ② Pré-requisito

Passo 1 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Instalação Completa — Rota npm**

```bash
# Passo 1: Verificar se o Node.js está instalado e na versão correta
node --version
# Saída esperada: v22.x.x ou superior

# Passo 2: Instalar o DeepSeek Harness globalmente
npm install -g deepseek-harness

# Passo 3: Verificar a instalação
dsh --version
# Saída esperada: deepseek-harness v0.1.x

# Passo 4: Verificar os modos disponíveis
dsh --help
```

**Instalação Completa — Rota Source**

```bash
# Passo 1: Clonar o repositório
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness

# Passo 2: Instalar dependências (pnpm recomendado)
pnpm install

# Passo 3: Compilar o projeto
pnpm build

# Passo 4: Linkar o binário globalmente (para usar 'dsh' de qualquer pasta)
pnpm link --global

# Passo 5: Verificar
dsh --version
```

**Configuração da API Key**

```bash
# Opção A: DeepSeek API (cloud)
dsh config set-api-key deepseek <SUA_API_KEY_AQUI>

# Verificar se a chave foi salva
dsh config show
```

**Primeira Execução**

```bash
# Iniciar o DeepSeek Harness no modo Standard
dsh --mode standard

# Você verá algo como:
# 🚀 DeepSeek Harness v0.1.0
# Mode: Standard | Model: deepseek-v4 (via ollama)
# Type your message or /help for commands
#
# dsh>
```

### ⑤ Verificação / Gate

```bash
node --version
```

### ⑥ Feito quando…

- [ ] Node.js desatualizado**: sempre use v22+. Versões anteriores causam erros de módulos ESM
- [ ] Permissões no Linux/macOS**: se o `npm install -g` pedir sudo, use `nvm` para gerenciar Node.js sem sudo
- [ ] Firewall bloqueando Ollama**: se o Ollama não responde, verifique se a porta 11434 não está bloqueada

### ⑦ Armadilhas

- _(a completar)_

## Passo 3 — Modelos DeepSeek: Escolhendo o Motor da Sua Oficina

> **Estágio:** Kit de pecas  ·  **Origem:** Cap. 3 — Modelos DeepSeek: Escolhendo o Motor da Sua Oficina

### ① Objetivo do passo

Compreender a familia de modelos e hardware necessario.

### ② Pré-requisito

Passo 2 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Instalando e Testando Modelos com Ollama**

```bash
# Instalar modelos de diferentes tamanhos
ollama pull deepseek-v4:7b      # ~4.7GB download
ollama pull deepseek-r1:14b     # ~9GB download
ollama pull deepseek-r1:32b     # ~19GB download

# Listar modelos instalados
ollama list
# NAME                    ID            SIZE      MODIFIED
# deepseek-v4:7b          a1b2c3d4      4.7 GB    2 minutes ago
# deepseek-r1:14b         e5f6g7h8      9.0 GB    5 minutes ago
# deepseek-r1:32b         i9j0k1l2      19.0 GB   10 minutes ago

# Testar cada modelo
ollama run deepseek-v4:7b "Explique o que é um plugin em 3 frases"
ollama run deepseek-r1:14b "Resolva: qual é a derivada de x^3 + 2x?"
ollama run deepseek-r1:32b "Escreva uma função Python que valida CPF"
```

**Monitorando VRAM em Tempo Real**

```bash
# NVIDIA (Linux)
watch -n 1 nvidia-smi

# macOS (Apple Silicon)
sudo powermetrics --samplers gpu_power -n 1 -i 1000

# Windows
nvidia-smi -l 1
```

**Conectando o Modelo ao DeepSeek Harness**

```bash
# Verificar que o Ollama está rodando
curl http://localhost:11434/api/tags

# Configurar o DeepSeek Harness para usar Ollama
dsh config set-model ollama deepseek-v4:7b

# Iniciar o harness com o modelo local
dsh --mode standard

# Testar no harness
dsh> Escreva uma função Python que calcula Fibonacci
```

**Exportando Modelo Quantizado do HuggingFace**

```bash
# Baixar modelo GGUF do HuggingFace (exemplo: 7B)
huggingface-cli download deepseek-ai/DeepSeek-V4-7B-GGUF \
  --include "deepseek-v4-7b-q4_k_m.gguf" \
  --local-dir ./models/

# Testar com llama.cpp
./llama-cli -m ./models/deepseek-v4-7b-q4_k_m.gguf \
  -p "Explique plugins em IA" -n 200
```

### ⑤ Verificação / Gate

```bash
curl http://localhost:11434/api/tags
```

### ⑥ Feito quando…

- [ ] O modelo carregou parcialmente
- [ ] Cada resposta levava 45 segundos em vez de 2
- [ ] Ele gastou três horas tentando otimizar parâmetros do Ollama antes de perceber que simplesmente não tinha VRAM suficiente para aquele modelo [4]
- [ ] A solução: ele trocou para o DeepSeek-R1-14B em quantização Q4_K_M
- [ ] O modelo cabia inteiro na GPU

### ⑦ Armadilhas

- _(a completar)_

## Passo 4 — Ollama, vLLM e llama.cpp: Os Tres Motores de Inferencia Local

> **Estágio:** Kit de pecas  ·  **Origem:** Cap. 4 — Ollama, vLLM e llama.cpp: Os Tres Motores de Inferencia Local

### ① Objetivo do passo

Configurar e comparar engines de inferencia local.

### ② Pré-requisito

Passo 3 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Configurando Ollama**

```bash
# Instalar Ollama (Linux/macOS)
curl -fsSL https://ollama.com/install.sh | sh

# Instalar Windows: baixe de https://ollama.com/download

# Puxar um modelo
ollama pull deepseek-v4:7b

# Iniciar o servidor (API na porta 11434)
ollama serve

# Testar a API
curl http://localhost:11434/api/generate -d '{
  "model": "deepseek-v4:7b",
  "prompt": "Olá, funciona?",
  "stream": false
}'
```

**Configurando vLLM**

```bash
# Instalar vLLM via pip
pip install vllm

# Iniciar o servidor com modelo DeepSeek
vllm serve deepseek-ai/DeepSeek-V4-7B-AWQ \
  --host 0.0.0.0 \
  --port 8000 \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.9

# Testar a API (compatível com OpenAI)
curl http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "deepseek-ai/DeepSeek-V4-7B-AWQ",
  "messages": [{"role": "user", "content": "Olá"}]
}'
```

**Configurando llama.cpp**

```bash
# Compilar o llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make -j$(nproc)

# Baixar modelo GGUF
wget https://huggingface.co/deepseek-ai/DeepSeek-V4-7B-GGUF/resolve/main/deepseek-v4-7b-q4_k_m.gguf

# Rodar o servidor HTTP
./llama-server -m deepseek-v4-7b-q4_k_m.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  -ngl 99 \
  -c 4096

# Testar
curl http://localhost:8080/health
```

**Conectando ao DeepSeek Harness**

```bash
# Para Ollama (porta 11434)
dsh config set-model ollama deepseek-v4:7b
dsh config set-endpoint http://localhost:11434

# Para vLLM (porta 8000)
dsh config set-model vllm deepseek-ai/DeepSeek-V4-7B-AWQ
dsh config set-endpoint http://localhost:8000

# Para llama.cpp (porta 8080)
dsh config set-model llamacpp deepseek-v4-7b-q4_k_m
dsh config set-endpoint http://localhost:8080

# Verificar configuração
dsh config show

# Iniciar
dsh --mode standard
```

### ⑤ Verificação / Gate

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### ⑥ Feito quando…

- [ ] Para 5 desenvolvedores funcionava bem
- [ ] Quando o time cresceu para 20
- [ ] O Ollama não foi projetado para múltiplas requisições simultâneas — ele processa uma por vez [3]
- [ ] A solução: migraram para vLLM com a mesma GPU
- [ ] O throughput subiu de 5 para 45 requisições simultâneas
- [ ] O custo da GPU foi o mesmo — a diferença foi apenas o engine [4]
- [ ] Se o time cresceu

### ⑦ Armadilhas

- _(a completar)_

## Passo 5 — Sistema de Plugins: O Coracao do Harness

> **Estágio:** Montagem  ·  **Origem:** Cap. 5 — Sistema de Plugins: O Coracao do Harness

### ① Objetivo do passo

Dominar o ciclo de vida dos plugins Cordis.

### ② Pré-requisito

Passo 4 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Criando um Plugin do Zero**

```bash
# Criar estrutura do plugin
mkdir my-word-count-plugin
cd my-word-count-plugin
npm init -y
```

**Instalando e Testando**

```bash
# Instalar localmente
dsh plugins install ./my-word-count-plugin

# Verificar que está instalado
dsh plugins list
# NAME                    VERSION  PROVIDES    REQUIRES
# my-word-count-plugin    0.1.0    tool        filesystem

# Testar no harness
dsh> Use a ferramenta word-count no arquivo README.md
# Resultado: { words: 1247, lines: 89, chars: 7832 }
```

**Resolvendo Conflitos**

```bash
dsh plugins check-conflicts
# ⚠️ Conflito: serviço 'shell' registrado por:
#   - @deepseek/shell-tool (v1.2.0)
#   - my-custom-shell (v0.1.0)
# Resolução: my-custom-shell tem prioridade (mais recente)
```

### ⑤ Verificação / Gate

```bash
npm init -y
```

### ⑥ Feito quando…

- [ ] Sempre implemente o lifecycle completo:** `ready` e `dispose` não são opcionais
- [ ] Use `ctx.effect()` para side effects:** cada `addEventListener`, `setInterval`, ou modificação de estado global deve ter um cleanup associado
- [ ] Declare dependências explicitamente:** o campo `requires` no `package.json` permite que o Cordis resolva conflitos antes de carregar
- [ ] Teste a remoção:** antes de publicar, instale e remova seu plugin 3 vezes seguidas. Se o harness ficar instável, há um leak [3]

### ⑦ Armadilhas

- _(a completar)_

## Passo 6 — Tool Pipeline: Como o Agente Executa Acoes

> **Estágio:** Montagem  ·  **Origem:** Cap. 6 — Tool Pipeline: Como o Agente Executa Acoes

### ① Objetivo do passo

Entender o fluxo de ferramentas de ponta a ponta.

### ② Pré-requisito

Passo 5 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Configurando Policy Rules**

```yaml
# dsh.config.yaml
tools:
  policy:
    # Bloquear comandos perigosos
    blocked:
      - "git push --force"
      - "rm -rf /"
      - "sudo *"
    
    # Permitir apenas em modo read
    read-only:
      - "filesystem:read"
      - "web:search"
    
    # Exigir aprovação humana
    require-approval:
      - "shell:execute"
      - "filesystem:write"
```

**Configurando Filesystem Guards**

```yaml
# dsh.config.yaml
sandbox:
  filesystem:
    # Permitir leitura em qualquer lugar
    read:
      - "/home/user/**"
      - "/tmp/**"
    
    # Permitir escrita apenas no projeto
    write:
      - "/home/user/projeto/**"
      - "/tmp/output/**"
    
    # Bloquear绝对amente
    deny:
      - "/etc/**"
      - "/root/**"
      - "/home/user/.ssh/**"
```

**Hooks de Auditoria**

```javascript
// plugin de auditoria
export default function auditPlugin(ctx) {
  ctx.on('tool:pre-execute', (event) => {
    console.log(`[AUDIT] ${event.tool} executada por ${event.session}`);
  });

  ctx.on('tool:post-execute', (event) => {
    console.log(`[AUDIT] ${event.tool} retornou ${event.result.length} chars`);
  });
}
```

**Monitorando o Pipeline em Tempo Real**

```bash
# Habilitar verbose mode
dsh --mode standard --verbose

# Output:
# [TOOL] policy: shell:execute -> permitido
# [TOOL] pre-execute: sandbox isolado ativado
# [TOOL] execute: ls -la /home/user/projeto
# [TOOL] post-execute: resultado comprimido de 2048 para 512 chars
# [TOOL] observation: resultado entregue ao modelo
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Nunca rode agentes com acesso total ao filesystem
- [ ] Sempre teste em um diretório temporário primeiro
- [ ] Mantenha backups antes de qualquer operação de agente
- [ ] Use approval mode para qualquer coisa que você não pode desfazer

### ⑦ Armadilhas

- _(a completar)_

## Passo 7 — Sessoes e Estado: Memoria do Agente

> **Estágio:** Montagem  ·  **Origem:** Cap. 7 — Sessoes e Estado: Memoria do Agente

### ① Objetivo do passo

Configurar sessoes duraveis e manipular historico.

### ② Pré-requisito

Passo 6 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Criando e Gerenciando Sessões**

```bash
# Criar nova sessão
dsh session create --name "refatoracao-api"

# Listar sessões existentes
dsh session list
# NAME                CREATED            STATUS
# refatoracao-api     2026-08-23 14:30   active
# debug-cache         2026-08-22 09:15   paused

# Retomar sessão anterior
dsh session resume refatoracao-api

# Bifurcar sessão
dsh session fork refatoracao-api --point turn:15 --name "experimento- alternativo"
```

**Visualizando Eventos**

```bash
# Listar eventos da sessão atual
dsh session events --last 10
# EVENT       TIMESTAMP           DETAILS
# turn:start  2026-08-23 14:32:01  turn_id: abc123
# user:msg    2026-08-23 14:32:01  "Refatore a função X"
# tool:call   2026-08-23 14:32:05  filesystem:read src/x.js
# tool:result 2026-08-23 14:32:06  2048 chars lidos
# tool:call   2026-08-23 14:32:10  filesystem:write src/x.js
# tool:result 2026-08-23 14:32:11  arquivo atualizado
# turn:end    2026-08-23 14:32:15  3 tools executadas

# Buscar eventos por ferramenta
dsh session search --tool "shell:execute"
# Encontra todos os momentos em que o agente executou comandos no shell
```

**Configurando Persistência**

```yaml
# dsh.config.yaml
session:
  storage:
    # Armazenar sessões em disco
    type: file
    path: ~/.dsh/sessions/
    
    # Comprimir sessões antigas (>7 dias)
    compress: true
    
    # Limitar tamanho por sessão
    max-size: "100MB"
    
    # Auto-save a cada N eventos
    auto-save: 10
```

**Exportando e Importando Sessões**

```bash
# Exportar sessão para compartilhar
dsh session export refatoracao-api --format json --output sessao.json

# Importar sessão de outro computador
dsh session import sessao.json --name "continuacao"
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Nomeie suas sessões descritivamente** — "refatoracao-api" é melhor que "sessao1"
- [ ] Faça fork antes de experimentar** — preserve o caminho original
- [ ] Exporte sessões importantes** — backup é segurança
- [ ] Limpe sessões antigas regularmente** — disco não é infinito

### ⑦ Armadilhas

- _(a completar)_

## Passo 8 — Sandbox e Seguranca: Isolando o Agente

> **Estágio:** Montagem  ·  **Origem:** Cap. 8 — Sandbox e Seguranca: Isolando o Agente

### ① Objetivo do passo

Configurar sandboxes e guardrails de seguranca.

### ② Pré-requisito

Passo 7 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Configurando Git Worktrees**

```bash
# Configurar o harness para usar worktrees
dsh config set sandbox.worktree.enabled true
dsh config set sandbox.worktree.path ~/.dsh/worktrees/

# Criar sessão com worktree isolado
dsh session create --name "feature-nova" --worktree

# Verificar que o worktree foi criado
git worktree list
# /home/user/projeto          abc1234 [main]
# /home/user/.dsh/worktrees/feature-nova  def5678 [feature-nova]
```

**Configurando Filesystem Guards**

```yaml
# dsh.config.yaml
sandbox:
  filesystem:
    # Diretório do projeto — leitura e escrita
    allow:
      - path: "./src/**"
        permissions: ["read", "write"]
      - path: "./tests/**"
        permissions: ["read", "write"]
      - path: "./docs/**"
        permissions: ["read", "write"]
    
    # Diretórios sensíveis — apenas leitura
    read-only:
      - path: "./.env.example"
      - path: "./config/*.json"
    
    # Diretórios bloqueados
    deny:
      - path: "./.git/**"
      - path: "./node_modules/**"
      - path: "~/.ssh/**"
      - path: "~/.aws/**"
```

**Configurando Security Plugins**

```bash
# Instalar plugins de segurança
dsh plugins install @deepseek/approvals
dsh plugins install @deepseek/audit

# Configurar aprovações
dsh config set security.approvals.enabled true
dsh config set security.approvals.require-for:
  - "shell:execute"
  - "filesystem:delete"
  - "git:push"
  - "git:reset"
```

**Rodando com Segurança**

```bash
# Iniciar com sandbox habilitado
dsh --mode standard --sandbox

# Output:
# 🔒 Sandbox ativo
# 📁 Filesystem: ./src/** (r/w), ./tests/** (r/w)
# 🚫 Bloqueado: ~/.ssh/**, ~/.aws/**
# ✅ Approvals: shell:execute, filesystem:delete
# 
# dsh> Modifique a função X
# [APPROVAL] shell:execute: "ls -la src/"
# Aprovar? (s/n): s
# [APPROVAL] filesystem:write: "src/x.js"
# Aprovar? (s/n): s
```

### ⑤ Verificação / Gate

```bash
git worktree list
```

### ⑥ Feito quando…

- [ ] NUNCA rode agentes com acesso total ao sistema
- [ ] Sempre bloqueie diretórios sensíveis (.ssh, .aws, .env)
- [ ] Habilite approvals para ações destrutivas
- [ ] Audite regularmente os logs de ação
- [ ] Use worktrees para isolar sessões de trabalho

### ⑦ Armadilhas

- _(a completar)_

## Passo 9 — Criando seu Primeiro Plugin personalizado

> **Estágio:** Estacao de trabalho  ·  **Origem:** Cap. 9 — Criando seu Primeiro Plugin personalizado

### ① Objetivo do passo

Desenvolver um plugin do zero para o harness.

### ② Pré-requisito

Passo 8 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Criando o Plugin: Contador de Repositórios**

```bash
# Criar estrutura
mkdir repo-stats-plugin
cd repo-stats-plugin
npm init -y
```

**Testando o Plugin**

```bash
# Instalar localmente
dsh plugins install ./repo-stats-plugin

# Testar no harness
dsh> Use a ferramenta repo-stats no diretório /home/user/projetos
# Resultado:
# {
#   "totalRepos": 5,
#   "repos": [
#     { "name": "projeto-a", "commits": 234, "branches": 3 },
#     { "name": "projeto-b", "commits": 89, "branches": 1 }
#   ],
#   "scanDirectory": "/home/user/projetos"
# }
```

**Escrevendo Testes**

```javascript
// test/index.test.js
import { describe, it, expect } from 'vitest';
import repoStatsPlugin from '../index.js';

describe('repo-stats plugin', () => {
  it('deve retornar stats de repositórios', async () => {
    const mockCtx = {
      service: (name, impl) => {
        if (name === 'repo-stats') return impl;
      },
      effect: () => {}
    };
    
    // Mock dos serviços
    mockCtx.service('filesystem', { exists: () => Promise.resolve(true) });
    mockCtx.service('shell', { execute: (cmd) => '/path/to/repo/.git' });
    
    const plugin = repoStatsPlugin(mockCtx);
    const result = await plugin.execute({ directory: '/path/to' });
    
    expect(result.totalRepos).toBe(1);
  });
});
```

### ⑤ Verificação / Gate

```bash
npm init -y
```

### ⑥ Feito quando…

- [ ] Responsabilidade única:** cada plugin faz UMA coisa bem feita
- [ ] Performance:** plugins não devem adicionar latência perceptível
- [ ] Graceful degradation:** se um serviço dependência não estiver disponível, o plugin deve funcionar parcialmente, não quebrar
- [ ] Testes:** todo plugin deve ter testes unitários antes de ser publicado

### ⑦ Armadilhas

- _(a completar)_

## Passo 10 — Ferramentas Customizadas: Construindo Pecas Novas

> **Estágio:** Estacao de trabalho  ·  **Origem:** Cap. 10 — Ferramentas Customizadas: Construindo Pecas Novas

### ① Objetivo do passo

Criar ferramentas personalizadas para o agente.

### ② Pré-requisito

Passo 9 concluído

### ③ Entregas

- `${params.registry}/${params.tag}`

### ④ Execução

**Criando uma Tool de Deploy**

```javascript
// tools/deploy-docker.js
export default {
  name: "deploy-docker",
  description: "Faz build e deploy de uma aplicação Docker",
  parameters: {
    type: "object",
    properties: {
      dockerfile: {
        type: "string",
        description: "Caminho para o Dockerfile"
      },
      tag: {
        type: "string",
        description: "Tag da imagem Docker"
      },
      registry: {
        type: "string",
        description: "Registry de destino",
        default: "docker.io"
      }
    },
    required: ["dockerfile", "tag"]
  },
  async execute(params, ctx) {
    const shell = ctx.service('shell');
    
    try {
      // Build da imagem
      const buildResult = shell.execute(
        `docker build -t ${params.tag} -f ${params.dockerfile} .`
      );
      
      // Push para o registry
      const pushResult = shell.execute(
        `docker push ${params.registry}/${params.tag}`
      );
      
      return {
        success: true,
        image: `${params.registry}/${params.tag}`,
        buildOutput: buildResult,
        pushOutput: pushResult
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
};
```

**Composição de Tools**

```javascript
// Tool que busca e analisa um repositório
export default {
  name: "analisar-repo",
  description: "Busca um repositório e retorna análise de qualidade",
  parameters: {
    type: "object",
    properties: {
      repo: { type: "string" },
      branch: { type: "string", default: "main" }
    },
    required: ["repo"]
  },
  async execute(params, ctx) {
    const shell = ctx.service('shell');
    
    // Step 1: Clonar o repositório
    shell.execute(`git clone ${params.repo} /tmp/analysis`);
    
    // Step 2: Analisar complexidade
    constLOC = shell.execute('find /tmp/analysis -name "*.js" | xargs wc -l');
    const issues = shell.execute('cd /tmp/analysis && npm audit --json');
    
    // Step 3: Limpar
    shell.execute('rm -rf /tmp/analysis');
    
    return {
      linesOfCode: loc,
      securityIssues: JSON.parse(issues)
    };
  }
};
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Sempre defina timeout** — tools não devem rodar indefinidamente
- [ ] Trate todos os erros** — rede, arquivo, permissão
- [ ] Retorne resultados estruturados** — o modelo precisa processar o output
- [ ] Limpe recursos** — arquivos temporários, conexões, processos
- [ ] Teste cenários de falha** — API fora do ar, disco cheio, permissão negada

### ⑦ Armadilhas

- _(a completar)_

## Passo 11 — Pipelines de Ferramentas: Orquestrando Acoes Complexas

> **Estágio:** Estacao de trabalho  ·  **Origem:** Cap. 11 — Pipelines de Ferramentas: Orquestrando Acoes Complexas

### ① Objetivo do passo

Construir pipelines de multiplas ferramentas.

### ② Pré-requisito

Passo 10 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Configurando um Pipeline Chain**

```yaml
# pipelines/deploy.yaml
name: deploy-completo
description: Pipeline de deploy: lint → test → build → push → deploy
steps:
  - name: lint
    tool: shell:execute
    params:
      command: "npm run lint"
    on-success: next
    on-fail: stop
    
  - name: test
    tool: shell:execute
    params:
      command: "npm test"
    on-success: next
    on-fail: rollback
    
  - name: build
    tool: shell:execute
    params:
      command: "npm run build"
    on-success: next
    on-fail: rollback
    
  - name: push
    tool: git:push
    params:
      branch: "main"
    on-success: next
    on-fail: rollback
```

**Configurando Fan-out Paralelo**

```yaml
# pipelines/analise-multiplas.yaml
name: analise-multiplas-fontes
description: Analisa múltiplas fontes em paralelo
parallel:
  - name: analise-codigo
    tool: analisar-codigo
    params:
      directory: "./src"
      
  - name: analise-testes
    tool: analisar-testes
    params:
      directory: "./tests"
      
  - name: analise-documentacao
    tool: analisar-docs
    params:
      directory: "./docs"
      
consolidate:
  tool: consolidar-relatorio
  params:
    inputs:
      - "{{steps.analise-codigo.result}}"
      - "{{steps.analise-testes.result}}"
      - "{{steps.analise-documentacao.result}}"
```

**Hooks de Auditoria**

```javascript
// hook de auditoria para pipelines
export default function pipelineAuditHook(ctx) {
  ctx.on('pipeline:start', (event) => {
    console.log(`[PIPELINE] ${event.name} iniciado`);
  });

  ctx.on('pipeline:step:complete', (event) => {
    console.log(`[PIPELINE] ${event.step} completado em ${event.duration}ms`);
  });

  ctx.on('pipeline:step:fail', (event) => {
    console.log(`[PIPELINE] ${event.step} falhou: ${event.error}`);
  });
}
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Limite retries a 3-5** — mais que isso é desperdício
- [ ] Use backoff exponencial** — 1s → 2s → 4s é melhor que 3x 5s
- [ ] Defina timeout por step** — nenhum step deve rodar mais que 60s
- [ ] Logs em cada step** — para debug quando algo falha
- [ ] Rollback automático** — se o deploy falhar, desfazer mudanças

### ⑦ Armadilhas

- _(a completar)_

## Passo 12 — RAG Local: Memoria de Longo Prazo para Agentes

> **Estágio:** Estacao de trabalho  ·  **Origem:** Cap. 12 — RAG Local: Memoria de Longo Prazo para Agentes

### ① Objetivo do passo

Construir pipeline RAG completo e self-hosted.

### ② Pré-requisito

Passo 11 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Setup com ChromaDB (Local)**

```python
# rag_setup.py
import chromadb
from sentence_transformers import SentenceTransformer

# Inicializar modelo de embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Criar cliente ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("documentos")

# Função para indexar documentos
def indexar_documento(texto, metadata):
    # Dividir em chunks de 500 caracteres
    chunks = [texto[i:i+500] for i in range(0, len(texto), 500)]
    
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(
            ids=[f"{metadata['id']}_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{**metadata, "chunk_index": i}]
        )

# Função para buscar
def buscar(query, n_results=3):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results['documents'][0]
```

**Setup com Qdrant (Produção)**

```bash
# Instalar Qdrant via Docker
docker run -p 6333:6333 -v qdrant_data:/qdrant/storage qdrant/qdrant

# Python
pip install qdrant-client
```

**Integrando com DeepSeek Harness**

```javascript
// Plugin de RAG para o harness
export default function ragPlugin(ctx) {
  ctx.service('rag-search', {
    async execute({ query, collection }) {
      // Buscar chunks relevantes
      const results = await fetch('http://localhost:8000/rag/search', {
        method: 'POST',
        body: JSON.stringify({ query, collection, top_k: 3 })
      });
      
      const chunks = await results.json();
      
      // Formatar para o modelo
      return {
        context: chunks.map(c => c.document).join('\n\n'),
        sources: chunks.map(c => c.metadata.source)
      };
    }
  });
}
```

### ⑤ Verificação / Gate

```bash
docker run -p 6333:6333 -v qdrant_data:/qdrant/storage qdrant/qdrant
```

### ⑥ Feito quando…

- [ ] O embedding model não conseguia capturar o significado de chunks tão grandes — os resultados da busca eram irrelevantes 60% das vezes [3]
- [ ] A causa: chunks grandes diluem o significado
- [ ] Um documento sobre "configuração de Docker" misturado com "introdução ao Linux" no mesmo chunk confunde o embedding model

### ⑦ Armadilhas

- _(a completar)_

## Passo 13 — Fine-Tuning Local: Personalizando o Modelo

> **Estágio:** Calibracao  ·  **Origem:** Cap. 13 — Fine-Tuning Local: Personalizando o Modelo

### ① Objetivo do passo

Realizar fine-tuning com LoRA/QLoRA.

### ② Pré-requisito

Passo 12 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Setup com Unsloth**

```bash
# Instalar Unsloth
pip install unsloth

# Script de fine-tuning
python << 'EOF'
from unsloth import FastLanguageModel
import torch

# Carregar modelo base com QLoRA
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/DeepSeek-V4-7B",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

# Adicionar adaptadores LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
)

# Treinar
from trl import SFTTrainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    max_seq_length=2048,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        num_train_epochs=3,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        output_dir="outputs",
    ),
)
trainer.train()

# Salvar adaptador
model.save_pretrained("deepseek-finetuned")
EOF
```

**Exportando para GGUF**

```bash
# Converter adaptador para GGUF
python scripts/convert_lora_to_gguf.py \
  --base-model deepseek-ai/DeepSeek-V4-7B \
  --lora-model ./deepseek-finetuned \
  --output deepseek-finetuned-Q4_K_M.gguf

# Carregar no Ollama
ollama create deepseek-custom -f Modelfile
```

### ⑤ Verificação / Gate

```bash
pip install unsloth
```

### ⑥ Feito quando…

- [ ] O resultado: o modelo ficou excelente para Python
- [ ] O fine-tuning causou catastrophic forgetting [1]
- [ ] A causa: dataset pequeno
- [ ] O modelo "esqueceu" conceitos gerais porque só viu um tipo de dado durante o treino

### ⑦ Armadilhas

- _(a completar)_

## Passo 14 — Multi-Agente: Coordenando uma Equipe de Agentes

> **Estágio:** Calibracao  ·  **Origem:** Cap. 14 — Multi-Agente: Coordenando uma Equipe de Agentes

### ① Objetivo do passo

Configurar multiplos agentes em paralelo.

### ② Pré-requisito

Passo 13 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Configurando Multi-Agent com Worktrees**

```bash
# Script de setup multi-agente
#!/bin/bash
REPO="/home/user/projeto"
AGENTS=("frontend" "backend" "tests")

for agent in "${AGENTS[@]}"; do
  # Criar worktree
  git -C "$REPO" worktree add "../${agent}" "feature/${agent}"
  
  # Criar sessão isolada
  dsh session create --name "agent-${agent}" --worktree "../${agent}"
  
  # Configurar agente com foco específico
  dsh config set agent.focus "${agent}" --session "agent-${agent}"
done

echo "✅ ${#AGENTS[@]} agentes configurados"
```

**Orquestração com Pipeline**

```yaml
# pipelines/multi-agente.yaml
name: desenvolvimento-completo
orchestrator: standard
agents:
  - name: frontend
    focus: "React, TypeScript, UI components"
    worktree: "feature/frontend"
    tools: ["filesystem", "shell"]
    
  - name: backend
    focus: "Python, FastAPI, database"
    worktree: "feature/backend"
    tools: ["filesystem", "shell", "database"]
    
  - name: tests
    focus: "pytest, integration tests"
    worktree: "feature/tests"
    tools: ["filesystem", "shell"]

dispatch:
  parallel: true
  wait: all
  aggregate: merge
```

### ⑤ Verificação / Gate

```bash
git -C "$REPO" worktree add "../${agent}" "feature/${agent}"
```

### ⑥ Feito quando…

- [ ] Isolamento total:** cada agente em seu próprio worktree
- [ ] Divisão clara de responsabilidades:** agentes diferentes modificam arquivos diferentes
- [ ] Merge com revisão:** sempre revisar conflitos antes de consolidar
- [ ] Testes finais:** rodar suite de testes completa depois do merge

### ⑦ Armadilhas

- _(a completar)_

## Passo 15 — Profiles e Configuracao Avancada: Afinando a Oficina

> **Estágio:** Calibracao  ·  **Origem:** Cap. 15 — Profiles e Configuracao Avancada: Afinando a Oficina

### ① Objetivo do passo

Criar profiles personalizados e otimizar o harness.

### ② Pré-requisito

Passo 14 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Criando Profiles**

```bash
# Criar profile de coding
mkdir -p ~/.dsh/profiles
cat > ~/.dsh/profiles/coding.yaml << 'EOF'
name: coding
description: "Profile para desenvolvimento de software"
config:
  model: "deepseek-v4:14b"
  mode: "standard"
  tools:
    - "filesystem"
    - "shell"
    - "web-search"
  sandbox:
    worktree: true
    filesystem:
      write: ["./src/**", "./tests/**"]
      deny: ["./.git/**", "./.env"]
  session:
    auto-save: 5
    max-turns: 100
EOF

# Criar profile de research
cat > ~/.dsh/profiles/research.yaml << 'EOF'
name: research
description: "Profile para pesquisa e análise"
config:
  model: "deepseek-r1:32b"
  mode: "standard"
  tools:
    - "filesystem"
    - "web-search"
  sandbox:
    worktree: false
    filesystem:
      read: ["./docs/**", "./research/**"]
      write: ["./output/**"]
  session:
    auto-save: 10
    max-turns: 200
EOF
```

**Usando Profiles**

```bash
# Iniciar com profile específico
dsh --profile coding
dsh --profile research

# Listar profiles disponíveis
dsh profiles list

# Verificar configuração ativa
dsh config show
```

**Otimização de Performance**

```yaml
# ~/.dsh/config.yaml — otimizações
performance:
  # Cache de respostas
  cache:
    enabled: true
    max-size: "1GB"
    ttl: "24h"
  
  # Limites de contexto
  context:
    max-tokens: 8192
    compress-threshold: 0.8  # Comprimir quando 80% cheio
  
  # RTK (memória de longo prazo)
  rtk:
    enabled: true
    storage: "~/.dsh/rtk/"
    max-entries: 1000
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Um profile por caso de uso** — não tente fazer um profile "serve para tudo"
- [ ] Teste cada profile** antes de usar em produção
- [ ] Documente** o que cada profile faz
- [ ] Versione** seus profiles no Git

### ⑦ Armadilhas

- _(a completar)_

## Passo 16 — Deploy e Operacao: Levando a Oficina para Producao

> **Estágio:** Calibracao  ·  **Origem:** Cap. 16 — Deploy e Operacao: Levando a Oficina para Producao

### ① Objetivo do passo

Colocar o harness em producao com Docker e monitoramento.

### ② Pré-requisito

Passo 15 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Dockerfile para DeepSeek Harness**

```dockerfile
# Dockerfile
FROM node:22-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar DeepSeek Harness
RUN npm install -g deepseek-harness

# Criar diretório de trabalho
WORKDIR /app

# Copiar configuração
COPY .dsh/ .dsh/

# Expor portas
EXPOSE 11434 8000

# Iniciar
CMD ["dsh", "--mode", "standard", "--host", "0.0.0.0"]
```

**Docker Compose com GPU**

```yaml
# docker-compose.yaml
version: '3.8'
services:
  harness:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./config:/app/.dsh
      - ./sessions:/root/.dsh/sessions
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - DSH_MODEL=deepseek-v4:14b
      - DSH_MODE=standard
      - NVIDIA_VISIBLE_DEVICES=all
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Monitoramento com Prometheus**

```yaml
# prometheus.yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'deepseek-harness'
    static_configs:
      - targets: ['harness:8080']
    metrics_path: '/metrics'
```

**Rate Limiting**

```yaml
# dsh.config.yaml — produção
rate_limiting:
  enabled: true
  requests_per_minute: 60
  tokens_per_hour: 100000
  per_user: true

fallback:
  primary: "deepseek-v4:14b"
  secondary: "deepseek-v4:7b"
  on_error: "switch"
  max_retries: 3
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Na primeira noite
- [ ] O harness ficou retornando erros por 8 horas antes de alguém perceber [3]

### ⑦ Armadilhas

- _(a completar)_

# Checklist Mestre

**Passo 1 — O Que e o DeepSeek Harness: O Agente que e Plugin**

- [ ] Você escolhe o modo Minimal porque "é mais leve"
- [ ] Três horas depois
- [ ] Você precisava do Standard o tempo todo
- [ ] O erro não foi escolher o modo errado — foi não entender o que cada modo oferece antes de começar
- [ ] O modo Minimal é excelente para benchmarks
- [ ] Se vai medir algo isolado
- [ ] Se vai repetir o mesmo workflow muitas vezes

**Passo 2 — Instalacao Local: Do Zero ao Primeiro dsh**

- [ ] Node.js desatualizado**: sempre use v22+. Versões anteriores causam erros de módulos ESM
- [ ] Permissões no Linux/macOS**: se o `npm install -g` pedir sudo, use `nvm` para gerenciar Node.js sem sudo
- [ ] Firewall bloqueando Ollama**: se o Ollama não responde, verifique se a porta 11434 não está bloqueada

**Passo 3 — Modelos DeepSeek: Escolhendo o Motor da Sua Oficina**

- [ ] O modelo carregou parcialmente
- [ ] Cada resposta levava 45 segundos em vez de 2
- [ ] Ele gastou três horas tentando otimizar parâmetros do Ollama antes de perceber que simplesmente não tinha VRAM suficiente para aquele modelo [4]
- [ ] A solução: ele trocou para o DeepSeek-R1-14B em quantização Q4_K_M
- [ ] O modelo cabia inteiro na GPU

**Passo 4 — Ollama, vLLM e llama.cpp: Os Tres Motores de Inferencia Local**

- [ ] Para 5 desenvolvedores funcionava bem
- [ ] Quando o time cresceu para 20
- [ ] O Ollama não foi projetado para múltiplas requisições simultâneas — ele processa uma por vez [3]
- [ ] A solução: migraram para vLLM com a mesma GPU
- [ ] O throughput subiu de 5 para 45 requisições simultâneas
- [ ] O custo da GPU foi o mesmo — a diferença foi apenas o engine [4]
- [ ] Se o time cresceu

**Passo 5 — Sistema de Plugins: O Coracao do Harness**

- [ ] Sempre implemente o lifecycle completo:** `ready` e `dispose` não são opcionais
- [ ] Use `ctx.effect()` para side effects:** cada `addEventListener`, `setInterval`, ou modificação de estado global deve ter um cleanup associado
- [ ] Declare dependências explicitamente:** o campo `requires` no `package.json` permite que o Cordis resolva conflitos antes de carregar
- [ ] Teste a remoção:** antes de publicar, instale e remova seu plugin 3 vezes seguidas. Se o harness ficar instável, há um leak [3]

**Passo 6 — Tool Pipeline: Como o Agente Executa Acoes**

- [ ] Nunca rode agentes com acesso total ao filesystem
- [ ] Sempre teste em um diretório temporário primeiro
- [ ] Mantenha backups antes de qualquer operação de agente
- [ ] Use approval mode para qualquer coisa que você não pode desfazer

**Passo 7 — Sessoes e Estado: Memoria do Agente**

- [ ] Nomeie suas sessões descritivamente** — "refatoracao-api" é melhor que "sessao1"
- [ ] Faça fork antes de experimentar** — preserve o caminho original
- [ ] Exporte sessões importantes** — backup é segurança
- [ ] Limpe sessões antigas regularmente** — disco não é infinito

**Passo 8 — Sandbox e Seguranca: Isolando o Agente**

- [ ] NUNCA rode agentes com acesso total ao sistema
- [ ] Sempre bloqueie diretórios sensíveis (.ssh, .aws, .env)
- [ ] Habilite approvals para ações destrutivas
- [ ] Audite regularmente os logs de ação
- [ ] Use worktrees para isolar sessões de trabalho

**Passo 9 — Criando seu Primeiro Plugin personalizado**

- [ ] Responsabilidade única:** cada plugin faz UMA coisa bem feita
- [ ] Performance:** plugins não devem adicionar latência perceptível
- [ ] Graceful degradation:** se um serviço dependência não estiver disponível, o plugin deve funcionar parcialmente, não quebrar
- [ ] Testes:** todo plugin deve ter testes unitários antes de ser publicado

**Passo 10 — Ferramentas Customizadas: Construindo Pecas Novas**

- [ ] Sempre defina timeout** — tools não devem rodar indefinidamente
- [ ] Trate todos os erros** — rede, arquivo, permissão
- [ ] Retorne resultados estruturados** — o modelo precisa processar o output
- [ ] Limpe recursos** — arquivos temporários, conexões, processos
- [ ] Teste cenários de falha** — API fora do ar, disco cheio, permissão negada

**Passo 11 — Pipelines de Ferramentas: Orquestrando Acoes Complexas**

- [ ] Limite retries a 3-5** — mais que isso é desperdício
- [ ] Use backoff exponencial** — 1s → 2s → 4s é melhor que 3x 5s
- [ ] Defina timeout por step** — nenhum step deve rodar mais que 60s
- [ ] Logs em cada step** — para debug quando algo falha
- [ ] Rollback automático** — se o deploy falhar, desfazer mudanças

**Passo 12 — RAG Local: Memoria de Longo Prazo para Agentes**

- [ ] O embedding model não conseguia capturar o significado de chunks tão grandes — os resultados da busca eram irrelevantes 60% das vezes [3]
- [ ] A causa: chunks grandes diluem o significado
- [ ] Um documento sobre "configuração de Docker" misturado com "introdução ao Linux" no mesmo chunk confunde o embedding model

**Passo 13 — Fine-Tuning Local: Personalizando o Modelo**

- [ ] O resultado: o modelo ficou excelente para Python
- [ ] O fine-tuning causou catastrophic forgetting [1]
- [ ] A causa: dataset pequeno
- [ ] O modelo "esqueceu" conceitos gerais porque só viu um tipo de dado durante o treino

**Passo 14 — Multi-Agente: Coordenando uma Equipe de Agentes**

- [ ] Isolamento total:** cada agente em seu próprio worktree
- [ ] Divisão clara de responsabilidades:** agentes diferentes modificam arquivos diferentes
- [ ] Merge com revisão:** sempre revisar conflitos antes de consolidar
- [ ] Testes finais:** rodar suite de testes completa depois do merge

**Passo 15 — Profiles e Configuracao Avancada: Afinando a Oficina**

- [ ] Um profile por caso de uso** — não tente fazer um profile "serve para tudo"
- [ ] Teste cada profile** antes de usar em produção
- [ ] Documente** o que cada profile faz
- [ ] Versione** seus profiles no Git

**Passo 16 — Deploy e Operacao: Levando a Oficina para Producao**

- [ ] Na primeira noite
- [ ] O harness ficou retornando erros por 8 horas antes de alguém perceber [3]
