# Capítulo 2: Instalacao Local: Do Zero ao Primeiro dsh

## 1. Introdução

No Capítulo 1, você entendeu que o DeepSeek Harness é um framework plugin-first sustentado pelo Cordis. Agora é hora de tirar a poeira da bancada e montar sua primeira estação de trabalho. Neste capítulo, você vai instalar o Node.js, configurar o DeepSeek Harness no seu computador, adicionar uma API key (seja da DeepSeek ou de um provedor local), e executar seu primeiro agente no terminal.

A instalação parece simples à primeira vista — e para a maioria dos usuários, realmente é. Mas há detalhes que fazem diferença entre uma instalação que funciona por 5 minutos e uma que funciona por 5 meses. Neste capítulo, você vai cobrir não apenas o "como", mas o "porquê" de cada passo, para que quando algo der errado (e vai dar), você saiba exatamente onde procurar [1].

Ao final, você terá um `dsh` funcionando no modo Standard, pronto para receber plugins e ferramentas. É o primeiro passo concreto na construção da sua oficina de agentes.

## 2. Explica

### Pré-Requisitos: O Kit Básico

Antes de qualquer instalação, você precisa de três ferramentas fundamentais [2]:

1. **Node.js v22 ou superior** — o DeepSeek Harness é escrito em JavaScript/TypeScript e roda sobre Node.js. A versão 22 é a mínima recomendada por trazer melhorias significativas de performance e suporte a ESM nativo. Versões anteriores (v16, v18) podem causar erros crypticos com módulos ESM — é a causa mais comum de falhas na instalação [3].

2. **npm ou pnpm** — gerenciadores de pacotes Node.js. O pnpm é recomendado por ser mais rápido e eficiente em disco (usa hardlinks em vez de copiar pacotes), mas o npm funciona perfeitamente. A diferença prática é que o pnpm instala dependências ~2x mais rápido em projetos grandes.

3. **Git** — para clonar o repositório (se você instalar via source) e para o sistema de worktrees que veremos no Capítulo 8. Git é essencial não apenas para instalação, mas para o funcionamento do harness em produção.

**GPU é opcional mas recomendada.** Se você vai rodar modelos localmente (Ollama, vLLM), uma GPU NVIDIA com pelo menos 8GB de VRAM faz diferença enorme na velocidade. Mas para começar, você pode usar o modo cloud com uma API key da DeepSeek sem nenhuma GPU [4].

O Git merece uma nota especial: ele não é apenas o meio de baixar o código-fonte na Rota 2. A partir do Capítulo 8, você vai usar `git worktree` para isolar sessões do agente — cada sessão roda numa cópia de trabalho separada do repositório, sem risco de um agente pisar no trabalho de outro. Isso significa que, mesmo que você escolha a Rota 1 (npm) para instalar o harness em si, ainda vai precisar de um Git funcional e atualizado no sistema para os projetos que o agente vai gerenciar depois.

### Instalação por Sistema Operacional

Embora o Node.js seja multiplataforma, cada sistema operacional tem uma particularidade que vale conhecer antes de instalar [2]:

- **Linux:** a rota mais direta é via gerenciador de versões (`nvm`), porque distribuições diferentes empacotam versões de Node.js diferentes nos seus repositórios oficiais — e frequentemente desatualizadas. Instalar via `apt`/`dnf` direto do repositório da distro é a causa mais comum de acabar com Node.js abaixo da v22 sem perceber.
- **macOS:** o Homebrew (`brew install node@22`) é a rota mais previsível. Em Apple Silicon (M1/M2/M3), vale confirmar que o binário instalado é nativo ARM64 e não uma versão x86_64 rodando sob emulação Rosetta — isso afeta diretamente a performance de qualquer modelo local via Ollama/Metal.
- **Windows:** o instalador oficial do Node.js já cuida do PATH automaticamente, mas o `dsh` depende de um shim PowerShell para funcionar em qualquer terminal — é aqui que a política de execução do PowerShell (coberta mais adiante) costuma travar quem nunca precisou ajustá-la antes.

### Por que Node.js v22+?

O DeepSeek Harness usa recursos modernos do ECMAScript modules (ESM) que não estão disponíveis em versões anteriores do Node.js. Especificamente [3]:

- **`import.meta.resolve`** — para resolução de módulos relativos
- **`node:test`** — para testes integrados no runtime
- **Performance de streams** — melhorias significativas em I/O
- **Suporte a WebCrypto** — para operações criptográficas nativas

Se você tentar instalar com Node.js v16 ou v18, provavelmente verá erros como `ERR_MODULE_NOT_FOUND` ou `SyntaxError: Cannot use import statement outside a module`. A solução é sempre atualizar o Node.js [5].

### Duas Rotas de Instalação

O DeepSeek Harness oferece duas formas de instalação, cada uma com seu caso de uso [1]:

**Rota 1 — Via npm (recomendada para iniciantes):**
```bash
npm install -g deepseek-harness
```
Instalação global via npm. Mais simples, atualizações automáticas via `npm update`. Ideal para quem quer começar rápido. O binário `dsh` fica disponível em qualquer diretório do sistema.

**Rota 2 — Via source (recomendada para desenvolvedores):**
```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm build
```
Clona o repositório e compila localmente. Permite modificar o código fonte, contribuir com plugins, e ter controle total sobre versões. Essa rota é essential para os capítulos avançados (9-12) onde você vai criar plugins personalizados [6].

A diferença prática é que a Rota 1 te dá um binário pronto, enquanto a Rota 2 te dá o código fonte. Para o que vamos fazer neste livro, ambas funcionam — mas a Rota 2 é mais flexível para os capítulos avançados.

Vale entender o que `pnpm build` de fato faz na Rota 2: o repositório do DeepSeek Harness é organizado como um workspace com múltiplos pacotes internos — o núcleo do Cordis, os plugins nativos (filesystem, shell, web search), e o CLI que expõe o binário `dsh`. O comando de build compila cada pacote na ordem correta de dependência (o Cordis primeiro, já que os plugins dependem dele) e só então gera o executável final. Entender essa estrutura de workspace importa porque, quando você criar seu primeiro plugin personalizado nos capítulos 9-12, ele vai viver como mais um pacote dentro dessa mesma estrutura — não como um projeto isolado.

### Configuração da API Key

O DeepSeek Harness precisa de uma chave de API para se comunicar com modelos de linguagem. Você tem duas opções [7]:

| Critério | Cloud (API Key) | Local (Ollama) |
|----------|-----------------|-----------------|
| Tempo até a primeira resposta | Minutos (criar conta + gerar key) | Depende do tempo de download do modelo |
| Requisito de hardware | Nenhum | GPU recomendada (CPU funciona, mas mais lento) |
| Privacidade dos dados | Trafegam para a infraestrutura da DeepSeek | Nunca saem do computador |
| Previsibilidade de custo | Depende da tabela de preços vigente na plataforma | Fixo (custo de energia/hardware já possuído) |
| Melhor para | Começar rápido, prototipar, hardware modesto | Dados sensíveis, uso intensivo, aprendizado do stack local |

Nenhuma opção é estritamente "melhor" — a escolha depende do que você está otimizando no momento. Para os primeiros capítulos deste livro, qualquer uma funciona; a diferença começa a importar a partir do Capítulo 3, quando entramos em detalhes de hardware e quantização.

**Opção A — API Key da DeepSeek (cloud):**
Acesse platform.deepseek.com, crie uma conta, e gere uma API key. É a rota mais rápida para começar — não exige GPU nem download de modelo, e o primeiro turno de conversa já funciona no minuto seguinte à criação da chave. Antes de comprometer orçamento, consulte a tabela de preços vigente diretamente na plataforma: provedores de LLM revisam valores de tokens de entrada/saída com frequência, e qualquer número impresso num livro sobre esse tema fica desatualizado rápido demais para ser confiável [1].

Guarde a chave como variável de ambiente, nunca em texto plano dentro de um arquivo versionado — a prática recomendada é `export DEEPSEEK_API_KEY=<chave>` no shell (ou `$env:DEEPSEEK_API_KEY` no PowerShell) e deixar o `dsh` ler a variável, em vez de colar a chave direto num comando que fica salvo no histórico do terminal. Se você trabalha em mais de um projeto, crie uma key por projeto na plataforma — isso limita o raio de dano se uma delas for exposta acidentalmente (por exemplo, num commit para um repositório público).

**Opção B — Modelo local via Ollama (self-hosted):**
Se você preferir rodar tudo localmente, pode conectar o harness a um modelo Ollama rodando na porta 11434. Não precisa de API key — o modelo roda entirely no seu computador. Isso tem vantagens de privacidade (seus dados nunca saem do computador) e custo (zero, depois de baixar o modelo) [8]. A contrapartida é que a qualidade e a velocidade da resposta dependem inteiramente do seu hardware — sem GPU adequada, um modelo local pode ser perceptivelmente mais lento do que a mesma pergunta respondida pela API cloud.

### Instalação em Redes Corporativas

Se você está numa rede corporativa, duas armadilhas aparecem antes mesmo do Node.js entrar em cena [2]:

**Proxy/firewall bloqueando o npm.** Ambientes corporativos costumam forçar todo tráfego HTTP por um proxy. Se `npm install -g deepseek-harness` travar sem erro claro (ou falhar com timeout), configure o proxy do npm explicitamente antes de tentar de novo:

```bash
npm config set proxy http://usuario:senha@proxy.empresa.com:porta
npm config set https-proxy http://usuario:senha@proxy.empresa.com:porta

# Verificar a configuração
npm config get proxy
npm config get https-proxy
```

**Política de execução do PowerShell (Windows).** Por padrão, o Windows bloqueia a execução de scripts `.ps1` — e o instalador global do npm no Windows depende de um shim em PowerShell para expor o binário `dsh`. Se o comando `dsh` for reconhecido pelo `npm` mas recusado pelo terminal com um erro sobre política de execução, ajuste a política para o usuário atual (não é necessário privilégio de administrador):

```powershell
Get-ExecutionPolicy
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Monorepo vs instalação standalone.** Se o DeepSeek Harness vai rodar dentro de um monorepo já existente (por exemplo, um workspace pnpm com múltiplos pacotes), prefira instalar como dependência de desenvolvimento do workspace (`pnpm add -D deepseek-harness -w`) em vez de global — assim a versão do harness fica travada no `pnpm-lock.yaml` do projeto, e cada desenvolvedor do time usa exatamente a mesma versão, sem depender do que cada máquina tem instalado globalmente.

### Gerenciamento de Versões

Uma prática importante é gerenciar versões do DeepSeek Harness. Como o framework está em v0.1 (developer preview), atualizações frequentes trazem mudanças breaking [9]:

```bash
# Verificar versão atual
dsh --version

# Atualizar para a versão mais recente
npm update -g deepseek-harness

# Reverter para uma versão específica (se algo quebrou)
npm install -g deepseek-harness@0.1.0

# Verificar changelog
dsh changelog
```

Em time, a prática recomendada é travar a versão exata no `package.json` do projeto (`"deepseek-harness": "0.1.3"`, sem `^` ou `~` na frente) em vez de deixar o npm resolver automaticamente para a última minor/patch disponível. Numa developer preview, uma atualização de patch pode alterar o comportamento de um plugin sem aviso — travar a versão garante que todo o time (e o pipeline de CI, se houver um) roda exatamente a mesma build, e que a decisão de atualizar é deliberada, não acidental.

## 3. Ilustra

### Montando a Primeira Estação de Trabalho

Pense na instalação como montar a primeira estação de trabalho na sua oficina. O Node.js é a bancada — a superfície onde tudo se apoia. Sem uma bancada estável, nenhuma ferramenta funciona direito. O Git é a caixa de ferramentas — permite clonar, versionar, e manipular código. A API key é a tomada de energia — sem ela, nenhuma peça funciona [10].

Quando você executa `npm install -g deepseek-harness`, está como se estivesse colocando a furadeira central na bancada. Ela é a peça principal — sem ela, você não consegue fazer nada. Mas ela precisa de energia (a API key) e de material para trabalhar (os plugins que vamos instalar nos próximos capítulos).

O momento em que você digita `dsh` pela primeira vez e vê o prompt do agente respondendo é como ligar a furadeira e ouzir o motor girando pela primeira vez. A oficina ganhou vida. Mas atenção — assim como uma furadeira ligada sem material para furar gira no vazio, um agente sem contexto é apenas um prompt esperando por uma tarefa.

Agora imagine que você monta uma segunda bancada na mesma oficina — outro projeto, outra pasta, mas ainda a mesma tomada de energia (o Ollama rodando na porta 11434). As duas bancadas podem compartilhar a mesma tomada sem problema, porque o Ollama atende requisições de qualquer cliente que fale a API OpenAI-compatível — não importa se a pergunta vem do harness do projeto A ou do projeto B. O problema só aparece se você tentar ligar duas fontes de energia diferentes na mesma tomada: dois processos tentando abrir a porta 11434 ao mesmo tempo (por exemplo, um `ollama serve` manual rodando junto com o serviço que já inicia sozinho no boot do sistema). Nesse caso, o segundo processo simplesmente não consegue ocupar a porta, e o erro que aparece — algo como "address already in use" — não tem nada a ver com o DeepSeek Harness em si, mas com duas bancadas competindo pela mesma tomada.

```mermaid
%% legenda: Fluxo de instalação do DeepSeek Harness — do zero ao primeiro agente
flowchart LR
    A[Instalar Node.js v22+] --> B[Escolher rota de instalação]
    B -->|npm| C[npm install -g deepseek-harness]
    B -->|source| D[git clone + pnpm install]
    C --> E[Configurar API key]
    D --> E
    E -->|Cloud| F[DeepSeek API key]
    E -->|Local| G[Ollama rodando]
    F --> H[dsh --mode standard]
    G --> H
    H --> I[Primeiro agente funcionando]
    
    style H fill:#7C3AED,color:#fff
    style I fill:#10B981,color:#fff
```

### O Primeiro Debug

Todo desenvolvedor lembra do primeiro erro que encontrou. Para o DeepSeek Harness, o erro mais comum é `ERR_MODULE_NOT_FOUND` — e ele quase sempre significa que o Node.js está desatualizado [3]. É como tentar ligar uma furadeira de 220V numa tomada de 110V: a peça é a mesma, mas a energia não é compatível.

Outro erro comum é `EACCES` no Linux/macOS quando você tenta instalar globalmente sem permissões. A solução não é usar `sudo` (que pode causar outros problemas), mas sim instalar o Node.js via `nvm` (Node Version Manager), que permite gerenciar versões sem sudo [5].

## 4. Técnica

### Instalação Completa — Rota npm

Vamos executar a instalação passo a passo. Abra o terminal e siga cada comando:

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

# Passo 5: Listar plugins nativos
dsh plugins list-builtin
```

### Instalação Completa — Rota Source

Para quem quer mais controle:

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

# Passo 6: Rodar testes para garantir que tudo funciona
pnpm test
```

### Configuração da API Key

```bash
# Opção A: DeepSeek API (cloud) — use a variável de ambiente, nunca a chave em texto puro
dsh config set-api-key deepseek "$DEEPSEEK_API_KEY"

# Verificar se a chave foi salva
dsh config show

# Testar a conexão
dsh test-connection
```

Para a Opção B (local com Ollama), primeiro instale o Ollama:

```bash
# Instalar Ollama (Linux/macOS)
curl -fsSL https://ollama.com/install.sh | sh

# Instalar Windows: baixe de https://ollama.com/download

# Instalar um modelo DeepSeek (7B para começar)
ollama pull deepseek-v4:7b

# Verificar que o modelo está rodando
ollama list

# Testar o modelo diretamente
ollama run deepseek-v4:7b "Olá, funciona?"

# O DeepSeek Harness detecta automaticamente o Ollama na porta 11434
# Não precisa de API key — basta iniciar o dsh
dsh --mode standard
```

### Gerenciando o Espaço em Disco dos Modelos

Modelos locais ocupam espaço real em disco — um 7B em GGUF já fica na faixa de alguns gigabytes, e é fácil acumular várias variantes (7B, 14B, diferentes níveis de quantização) sem perceber quanto espaço elas somam:

```bash
# Listar modelos instalados com tamanho
ollama list

# Ver o espaço total ocupado pelos modelos do Ollama
du -sh ~/.ollama/models        # Linux/macOS
Get-ChildItem -Recurse "$env:USERPROFILE\.ollama\models" | Measure-Object -Property Length -Sum   # PowerShell

# Remover um modelo que não está mais em uso
ollama rm deepseek-v4:7b

# Remover TODOS os modelos não usados nos últimos 30 dias (script simples)
ollama list | tail -n +2 | awk '{print $1}' | while read -r modelo; do
  echo "Considerar remover: $modelo"
done
```

Uma prática saudável é manter no máximo dois ou três modelos baixados por vez — o que você está usando ativamente, mais um candidato que está testando. Acumular variantes "só para o caso de precisar" é a forma mais comum de um disco encher silenciosamente ao longo de alguns meses de uso do harness.

### Primeira Execução

```bash
# Iniciar o DeepSeek Harness no modo Standard
dsh --mode standard

# Você verá algo como:
# 🚀 DeepSeek Harness v0.1.0
# Mode: Standard | Model: deepseek-v4 (via ollama)
# Type your message or /help for commands
#
# dsh>

# Testar com uma mensagem simples
dsh> Olá! Quem é você?
# O agente responde com uma saudação e explica que é o DeepSeek Harness

# Testar uma tool básica
dsh> Liste os arquivos no diretório atual
# O agente usa a tool filesystem:readdir e lista os arquivos
```

Parabéns — sua primeira estação de trabalho está operacional. O agente está rodando no modo Standard com todas as ferramentas disponíveis [1].

### Testando um Plugin Nativo Isoladamente

Antes de confiar a instalação para o dia a dia, vale testar um plugin nativo isoladamente — isso confirma que o Cordis está resolvendo dependências corretamente, não só que o binário `dsh` inicia:

```bash
# Testar o plugin de shell isoladamente
dsh plugins test @deepseek/shell-tool

# Saída esperada em uma instalação saudável:
# ✅ @deepseek/shell-tool: carregado
# ✅ Dependências resolvidas: nenhuma
# ✅ Efeitos registrados: 1 (comando shell)
# ✅ Teste de execução: OK (echo "test" retornou "test")

# Se o teste falhar, o Cordis reporta exatamente qual etapa quebrou:
# ❌ @deepseek/shell-tool: falha na etapa "ready"
#    Causa: permissão negada ao registrar o efeito de shell
```

Se esse teste isolado passa mas o `dsh --mode standard` completo falha, o problema não está no plugin em si — está em outro lugar da cadeia (conflito entre plugins, configuração de sandbox, ou modelo inacessível). Isolar dessa forma economiza tempo de debug porque elimina uma variável por vez, em vez de tentar diagnosticar o sistema inteiro de uma só vez.

### Verificação Pós-Instalação

```bash
# Script de verificação completa
echo "=== Verificação Pós-Instalação ==="

# 1. Node.js
node --version | grep -q "v22" && echo "✅ Node.js v22+" || echo "❌ Node.js desatualizado"

# 2. DeepSeek Harness
dsh --version && echo "✅ dsh instalado" || echo "❌ dsh não encontrado"

# 3. Plugins nativos
dsh plugins list-builtin | wc -l | xargs -I {} echo "✅ {} plugins nativos carregados"

# 4. Conexão com modelo
dsh test-connection && echo "✅ Conexão OK" || echo "❌ Falha na conexão"

# 5. Git disponível (necessário para worktrees a partir do Capítulo 8)
git --version > /dev/null 2>&1 && echo "✅ Git disponível" || echo "❌ Git não encontrado"

# 6. Binário no PATH correto (evita conflito entre instalação global antiga e nova)
which dsh 2>/dev/null || where.exe dsh 2>/dev/null

echo "=== Verificação completa ==="
```

Rodar esse script inteiro depois de qualquer instalação nova, atualização de versão, ou troca entre Rota 1 e Rota 2, é mais rápido do que descobrir um problema no meio de uma sessão de trabalho — e vira hábito depois das primeiras vezes.

### Diagnosticando o PATH e o Ambiente

Grande parte dos problemas de "instalei mas não funciona" se resolve verificando o ambiente antes de reinstalar qualquer coisa:

```bash
# Onde o sistema está encontrando o binário 'dsh'?
which dsh          # Linux/macOS
where.exe dsh       # Windows (cmd/PowerShell)

# O PATH inclui o diretório global do npm?
npm config get prefix
echo $PATH | tr ':' '\n' | grep -i npm     # Linux/macOS
$env:Path -split ';' | Select-String npm   # PowerShell

# O Node.js consegue resolver o pacote instalado?
node -e "console.log(require.resolve('deepseek-harness/package.json'))"

# Diagnóstico geral de saúde do ambiente npm
npm doctor
```

Se `which dsh` (ou `where.exe dsh`) não retornar nada, o binário existe mas não está no PATH — normalmente porque o diretório global do npm (`npm config get prefix`) não foi adicionado à variável de ambiente do sistema. Adicionar esse diretório ao PATH resolve o `dsh: command not found` sem precisar reinstalar nada.

### Debugando um `ERR_MODULE_NOT_FOUND` Passo a Passo

Esse é o erro mais comum na instalação, e vale entender o fluxo de diagnóstico completo, não só a causa mais provável [3]:

1. **Reproduza o erro isoladamente.** Rode `dsh --version` puro, sem nenhum outro comando encadeado, para confirmar que o erro acontece na inicialização do próprio binário, e não em algum plugin carregado depois.
2. **Confirme a versão do Node.js que está de fato em uso.** `node --version` pode mostrar v22 enquanto o `dsh` executa sob uma versão diferente, se você usa `nvm` e trocou de shell — rode `nvm current` para conferir qual versão está ativa nessa sessão de terminal específica.
3. **Verifique se o erro aponta para um módulo interno do harness ou para uma dependência.** A mensagem completa de `ERR_MODULE_NOT_FOUND` cita o caminho do módulo que falhou ao resolver — se for algo dentro de `node_modules/deepseek-harness`, o problema é a versão do Node; se for uma dependência externa, pode ser uma instalação corrompida (`npm cache clean --force` seguido de reinstalação resolve a maioria desses casos).
4. **Se nada disso resolver, isole com uma instalação limpa.** Desinstale (`npm uninstall -g deepseek-harness`), confirme que `which dsh` não retorna nada, e reinstale do zero — isso elimina a possibilidade de um estado parcialmente corrompido de uma instalação anterior interrompida.

## 5. Aplica

### O Erro de Pular os Pré-Requisitos

Um desenvolvedor decidiu instalar o DeepSeek Harness sem verificar a versão do Node.js. Seu computador tinha o Node 16 (uma versão antiga). A instalação pareceu funcionar — o npm não reportou erros — mas ao executar `dsh`, ele recebeu erros crypticos sobre módulos ESM não encontrados [3].

Ele gastou duas horas debugando antes de descobrir que o problema era a versão do Node. A correção era simples: `nvm install 22`. Mas o tempo perdido poderia ter sido evitado com uma verificação de 30 segundos antes da instalação.

Outro caso comum: um desenvolvedor instalou o Ollama e o DeepSeek Harness no mesmo computador, mas o Ollama não estava rodando quando ele executou `dsh`. O harness tentou conectar na porta 11434, não encontrou nada, e retornou um erro genérico "Model not found". O desenvolvedor interpretou isso como "o modelo não está instalado" e começou a baixar o modelo novamente — gastando 20 minutos de download desnecessário [8].

Um terceiro caso, menos óbvio: um desenvolvedor já tinha um serviço próprio escutando na porta 11434 (um projeto anterior que também usava essa porta como padrão) quando instalou o Ollama. O Ollama subiu sem reclamar, mas o `dsh` continuava recebendo respostas de um servidor completamente diferente — nem erro, nem timeout, apenas respostas sem sentido para o contexto do agente. O diagnóstico levou mais tempo do que devia porque não havia mensagem de erro nenhuma para seguir; a causa só apareceu ao rodar `curl http://localhost:11434/api/tags` e notar que a lista de modelos retornada não correspondia a nada que ele tinha baixado via `ollama pull`.

### A Prática Correta

A instalação global via `npm install -g` funciona bem até você precisar manter duas versões do harness ativas ao mesmo tempo — por exemplo, testando uma branch experimental de um plugin próprio enquanto mantém a versão estável rodando em outro projeto. Acima desse cenário, a instalação global não escala: o pacote global do npm não suporta duas versões simultâneas no mesmo PATH, então a Rota 2 (source, clonada em pastas separadas por versão) passa a ser a única opção viável.

Sempre verifique os pré-requisitos antes de instalar:

```bash
# Script de verificação pré-instalação
echo "=== Verificação de Pré-Requisitos ==="

# Node.js
NODE_VERSION=$(node --version 2>/dev/null | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -ge 22 ]; then
  echo "✅ Node.js v${NODE_VERSION} (mínimo: v22)"
else
  echo "❌ Node.js v${NODE_VERSION} encontrado. Instale v22+: https://nodejs.org"
  echo "   Ou use: nvm install 22"
  exit 1
fi

# Git
git --version && echo "✅ Git instalado" || echo "❌ Git não encontrado"

# npm/pnpm
pnpm --version && echo "✅ pnpm disponível" || echo "⚠️  pnpm não encontrado (recomendado)"
npm --version && echo "✅ npm disponível" || echo "❌ npm não encontrado"

echo "✅ Todos os pré-requisitos verificados"
```

Armadilhas comuns na instalação:

| Erro | Causa | Solução |
|------|-------|---------|
| `ERR_MODULE_NOT_FOUND` | Node.js < v22 | `nvm install 22` |
| `EACCES` no Linux/macOS | Permissões npm | Usar `nvm` em vez de `sudo` |
| `dsh: command not found` | npm global bin não no PATH | Adicionar `$(npm config get prefix)/bin` ao PATH |
| Ollama não responde | Serviço não rodando | `ollama serve` |
| Modelo não encontrado | Modelo não baixado | `ollama pull deepseek-v4:7b` |
| Respostas sem sentido, sem erro | Porta 11434 ocupada por outro serviço | `curl http://localhost:11434/api/tags` para confirmar a origem antes de qualquer outra ação |
| `npm doctor` reporta falha em registry | Proxy corporativo não configurado | `npm config set proxy`/`https-proxy` |
| `dsh` roda mas ignora plugins customizados | Instalação global antiga conflitando com instalação source local | `which dsh` para confirmar qual binário está ativo |

## 6. Conclusão

Neste capítulo, você instalou o DeepSeek Harness pela primeira vez. Viu as duas rotas de instalação (npm e source), configurou uma API key (cloud ou local via Ollama), e executou seu primeiro agente no modo Standard. Sua estação de trabalho está montada e funcionando.

Mas uma estação de trabalho sem um bom motor é apenas uma mesa bonita. No próximo capítulo, você vai conhecer a família de modelos DeepSeek — do V4 ao R1, passando pelos variants distilled — e descobrir como escolher o modelo certo para o seu hardware e caso de uso. É aqui que você calibra o motor da sua oficina.

Antes de virar a página, vale reforçar o que realmente importa deste capítulo: a instalação em si é o passo menos interessante da jornada, mas é o único que, se malfeito, contamina todos os outros. Um Node.js na versão errada, uma API key salva em texto puro, ou uma porta 11434 disputada por dois processos — nenhum desses erros é sofisticado, mas todos eles produzem sintomas confusos que parecem muito mais graves do que realmente são. A checklist de verificação pós-instalação deste capítulo não é burocracia; é o que separa uma tarde perdida debugando o ambiente de uma tarde inteira efetivamente aprendendo o harness.

## 7. Referências Bibliográficas

[1] DEEPSEEK AI. *DeepSeek Harness developer preview: Everything is a plugin*. Disponível em: https://deepseek.com/harness/en/. Acesso em: 23 ago. 2026.

[2] MINDSTUDIO. *How to Install and Set Up DeepSeek Harness Locally*. Disponível em: https://www.mindstudio.ai/blog/how-to-set-up-deepseek-harness. Acesso em: 23 ago. 2026.

[3] DEEPSEEK AI. *deepseek-harness/docs/development.md*. GitHub. Disponível em: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/development.md. Acesso em: 23 ago. 2026.

[4] DEV.TO. *A Step-by-Step Guide to Install DeepSeek-R1 Locally*. Disponível em: https://dev.to/nodeshiftcloud/a-step-by-step-guide-to-install-deepseek-r1-locally-with-ollama-vllm-or-transformers-44a1. Acesso em: 23 ago. 2026.

[5] MEDIUM (techlatest). *How to Install DeepSeek Harness: A Step-by-Step Setup Guide*. Disponível em: https://medium.com/@techlatest.net/how-to-install-deepseek-harness-a-step-by-step-setup-guide-for-developers-9bedadfb584d. Acesso em: 23 ago. 2026.

[6] DATACAMP. *DeepSeek Harness Tutorial: Set Up the Open-Source Agent*. Disponível em: https://www.datacamp.com/tutorial/deepseek-harness. Acesso em: 23 ago. 2026.

[7] VERDENT.AI. *DeepSeek Harness Installation: How to Run dsh*. Disponível em: https://www.verdent.ai/guides/agents/install-deepseek-harness-dsh. Acesso em: 23 ago. 2026.

[8] ATLASCLOUD. *How to Install DeepSeek Harness in 10 Minutes*. Disponível em: https://www.atlascloud.ai/blog/tips/how-to-install-deepseek-harness. Acesso em: 23 ago. 2026.

[9] COMETAPI. *6 Methods to Deploy DeepSeek Harness Locally*. Disponível em: https://www.cometapi.com/how-to-install-and-deploy-deepseek-harness-locally/. Acesso em: 23 ago. 2026.

[10] TOWARDS AI. *DeepSeek Harness Explained: When the AI Model is Just a Plugin*. Disponível em: https://pub.towardsai.net/deepseek-harness-explained-when-the-ai-model-is-just-a-plugin-16b2496f3d01. Acesso em: 23 ago. 2026.

[11] CLOUDSWAY. *DeepSeek Harness Tutorial: Architecture and Quick Start*. Disponível em: https://www.cloudsway.ai/resources/deepseek-harness-tutorial-architecture-and-quick-start. Acesso em: 23 ago. 2026.

[12] LINKEDIN (Cole Medin). *DeepSeek Coding Agent Harness Offers Customizable Plugins*. Disponível em: https://www.linkedin.com/posts/cole-medin-727752184_deepseek-built-a-coding-agent-harness-last-activity-7495993045192998912-574a. Acesso em: 23 ago. 2026.

[13] XCLOUD. *DeepSeek Harness vs OpenClaw vs Hermes Agent*. Disponível em: https://xcloud.host/deepseek-harness-vs-openclaw-vs-hermes-agent. Acesso em: 23 ago. 2026.

[14] KIE.AI. *What Is DeepSeek Harness? V4 Agent Framework*. Disponível em: https://kie.ai/blog/what-is-deepseek-harness. Acesso em: 23 ago. 2026.

[15] YOUTUBE (DeepSeek Harness). *Everything You Need to Get Started*. Disponível em: https://www.youtube.com/watch?v=0sErTGzcJoc. Acesso em: 23 ago. 2026.

[16] YOUTUBE (DeepSeek Harness). *NEW Deepseek Agent Harness EXPLAINED (deep dive)*. Disponível em: https://www.youtube.com/watch?v=Hpw4fAHlHDw. Acesso em: 23 ago. 2026.

[17] YOUTUBE (DeepSeek Harness). *Every Deepseek Harness Concept Explained*. Disponível em: https://www.youtube.com/watch?v=24UCnAs7MVg. Acesso em: 23 ago. 2026.

[18] LINKEDIN (Richard Van Ngo Tran). *DeepSeek Harness v0.1 Released: Cordis Powered Plugin*. Disponível em: https://www.linkedin.com/posts/richard-van-ngo-tran-8095441a4_deepseek-harness-v01-is-now-available-in-activity-7493832260652228608-E39a. Acesso em: 23 ago. 2026.

[19] REDDIT (r/DeepSeek). *Can you help me find the Best AI Harness for the New Deepseek V4?*. Disponível em: https://www.reddit.com/r/DeepSeek/comments/1vjkstg/. Acesso em: 23 ago. 2026.

[20] SKYWORK. *DeepSeek V4 Local Deployment: A Comprehensive Guide*. Disponível em: https://skywork.ai/skypage/en/deepseek-local-deployment-guide/2047582806721294336. Acesso em: 23 ago. 2026.
