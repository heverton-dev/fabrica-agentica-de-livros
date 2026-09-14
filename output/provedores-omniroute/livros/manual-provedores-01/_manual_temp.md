# Manual OmniRoute

## 15 Provedores de IA Gratuitos para Maxima Confiabilidade

---

# Capítulo 1: OmniRoute — Seu Agregador de Modelos de IA

## 1. Introdução

Imagine que você trabalha com múltiplos modelos de inteligência artificial — Claude, GPT-4, Gemini — mas cada um exige uma conta separada, credenciais distintas e código de integração próprio. OmniRoute resolve esse caos: ele atua como **um hub único que conecta todos os seus provedores de IA**, fazendo load balancing automático, fallback inteligente e gerenciamento centralizado de credenciais.

Neste livro, você aprenderá a configurar OmniRoute, conectar seus 15+ provedores gratuitos e integrá-lo com suas ferramentas de desenvolvimento como Claude Code e Cursor.

## 2. Explica

OmniRoute é um **servidor proxy OpenAI-compatível** que funciona como intermediário entre suas aplicações e os provedores reais de IA. Quando você faz uma requisição via OmniRoute, ele:

1. **Recebe** a chamada (formato OpenAI standard)
2. **Roteia** para o provedor configurado (ou faz load balancing entre vários)
3. **Retorna** a resposta na mesma estrutura

A vantagem principal é a **abstração**: seu código não precisa saber qual provedor está sendo usado. Se Vertex AI atingir rate limit, OmniRoute tenta OpenCode automaticamente. Se um modelo não estiver disponível, ele procura um similar em outro provedor.

OmniRoute é **agnóstico a modelos**: suporta LLMs (texto), modelos de visão, embeddings, geração de imagens — qualquer coisa que seja OpenAI-compatível.

## 3. Ilustra

Pense em OmniRoute como um **porteiro inteligente de um prédio comercial com múltiplos elevadores**.

Você (sua aplicação) chega à recepção (OmniRoute) e pede "leve-me ao 10º andar" (faça uma chamada de chat). O porteiro verifica qual elevador está mais disponível naquele momento:
- Se o elevador do Vertex AI está congestionado (muitos usuários), ele manda você para o de OpenCode.
- Se o de Claude está em manutenção (API fora do ar), ele tenta o de Anthropic.
- Se todos estão cheios, ele avisa que o prédio está no limite.

Você não precisa saber qual elevador você usou — a experiência é uniforme. O porteiro (OmniRoute) cuida disso.

```mermaid
%% legenda: Fluxo de requisição através do OmniRoute
flowchart LR
  A[Sua App<br/>Claude Code] -->|POST /chat/completions| B[OmniRoute<br/>Proxy]
  B -->|Load Balance| C{Provedor<br/>Disponível?}
  C -->|Vertex AI<br/>OK| D["Vertex AI<br/>Gemini Pro"]
  C -->|OpenCode<br/>OK| E["OpenCode<br/>Llama 2"]
  C -->|Anthropic<br/>OK| F["Anthropic<br/>Claude 3"]
  D --> G[Resposta<br/>Unificada]
  E --> G
  F --> G
  G --> H[Sua App<br/>Recebe Resultado]
```

## 4. Técnica

### Arquitetura do OmniRoute

OmniRoute roda como um container Docker em `81.17.103.186:20127`. Seus componentes principais são:

| Componente | Função |
|---|---|
| **API Gateway** | Expõe endpoint OpenAI-compatível em `http://81.17.103.186:20127/v1` |
| **Provider Registry** | Armazena conexões e credenciais (Dashboard → Providers) |
| **Router Engine** | Decide qual provedor usar baseado em disponibilidade/prioridade |
| **Load Balancer** | Distribui carga entre provedores |
| **Cache Layer** | Armazena respostas idênticas para economizar créditos |
| **Logs & Analytics** | Registra todas as requisições |

### Setup Mínimo — 3 Passos

**Passo 1: Acessar o Dashboard**

```
URL: http://81.17.103.186:20127
Usuário: admin
Senha: omniroute_2026
```

**Passo 2: Gerar API Key**

No Dashboard, navegue até **Settings → API Keys** e clique **"Generate New Key"**. Você receberá uma chave tipo:
```
sk-omniroute-abc123def456...
```

**Passo 3: Usar em Sua App**

Via Python:
```python
import requests

endpoint = "http://81.17.103.186:20127/v1"
api_key = "sk-omniroute-abc123..."

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(
    f"{endpoint}/chat/completions",
    headers=headers,
    json={
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Olá!"}]
    }
)

print(response.json())
```

Via cURL:
```bash
curl http://81.17.103.186:20127/v1/chat/completions \
  -H "Authorization: Bearer sk-omniroute-abc123..." \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Olá!"}]}'
```

## 5. Aplica

### Cenário: Você está construindo um chatbot

**Situação:** Você cria um chatbot em Python que precisa de resposta instantânea do usuário. Escolhe GPT-4 pela qualidade, mas GPT-4 é caro — US$ 0,03 por 1K tokens. Se sua startup tem 1000 usuários ativos por dia, os custos explodem rapidamente.

**Erro plausível:** Você código-hardcoded `model="gpt-4"` e espera que as credenciais do OpenAI nunca falhem. Quando o OpenAI sofre uma indisponibilidade de 2 horas (rara, mas acontece), seu chatbot cai completamente.

**Diagnóstico:** Você está apostando tudo em um único provedor. Isso viola o princípio de **resiliência em produção**. Código robusto nunca depende 100% de uma fonte.

**Correção com OmniRoute:**

1. Configura 3 provedores: Vertex AI (300 créditos/mês), OpenCode (ilimitado), OpenAI (fallback premium).
2. Define prioridade: Vertex → OpenCode → OpenAI.
3. Código fica simples:

```python
# Uma única chamada, mas com 3 provedores por trás!
response = requests.post(
    "http://81.17.103.186:20127/v1/chat/completions",
    headers={"Authorization": "Bearer sk-omniroute-..."},
    json={"model": "gpt-4", "messages": [...]}
)
```

Se Vertex AI atingir 300 créditos, OmniRoute manda para OpenCode automaticamente. Seu chatbot continua funcionando sem mudança de código. **Resultado:** 99.99% uptime e custos 70% mais baixos.

### Armadilhas Comuns

1. **Não validar a API Key antes de deployar** — Teste sempre `curl ... /v1/models` antes de ir para produção.
2. **Deixar Status do provedor em OFF** — Verifique Dashboard → Providers e confirme que todos estão com toggle verde (ON).
3. **Esquecer de renovar créditos trial** — Créditos Anthropic ($5) expiram em 3 meses. Monitore em Billing.

## 6. Conclusão

OmniRoute é seu curador de modelos de IA — centraliza credenciais, faz balanceamento inteligente e elimina a fricção de múltiplos provedores. Os próximos capítulos te mostram como configurá-lo completamente, desde o dashboard até a integração com Claude Code.

**Seu desafio:** Acesse o dashboard em `http://81.17.103.186:20127` e verifique que consegue fazer login com admin/omniroute_2026. Ninguém segue adiante sem ter acesso comprovado ao OmniRoute.

## 7. Referências Bibliográficas

[1] OpenAI Platform Documentation. *OpenAI API Reference*. Disponível em: https://platform.openai.com/docs/api-reference. Acesso em: 24 ago. 2026.

[2] OmniRoute Official Repository. *OmniRoute — AI Model Aggregation*. Disponível em: https://github.com/omniroute/omniroute. Acesso em: 24 ago. 2026.

[3] Docker Documentation. *Docker Compose Overview*. Disponível em: https://docs.docker.com/compose/. Acesso em: 24 ago. 2026.


---

# Capítulo 2: Acessando e Navegando o Dashboard

## 1. Introdução

No Capítulo 1, você entendeu a **arquitetura** de OmniRoute. Agora vamos explorar o **painel de controle** — o lugar onde você configura provedores, monitora credenciais e ajusta prioridades. O dashboard é sua sala de máquinas: sem ele, nenhuma configuração é possível.

## 2. Explica

O Dashboard OmniRoute é uma **interface web centralizada** que expõe três funções principais:

1. **Provider Registry**: Gerenciar conexões com provedores (adicionar, remover, ativar/desativar)
2. **Model Inventory**: Ver quais modelos estão disponíveis após conectar os provedores
3. **Operations**: API Keys, logs, billing, rate limiting

Diferente de cada provedor ter seu próprio console (Google Cloud, OpenAI, Anthropic), aqui você tem tudo em um lugar. Isso reduz tempo de administração drasticamente — em vez de clicar em 5 consoles diferentes para ver status, você abre um dashboard.

## 3. Ilustra

Imagine o dashboard como um **painel de controle de um avião**, onde cada gauge representa um provedor:

- **Velocidade (modelo)**: Qual modelo está ativo agora? (gpt-4, gemini-pro, llama-70b)
- **Altitude (créditos)**: Quantos créditos sobraram? (300/300 Vertex, $5.00 Anthropic)
- **Combustível (rate limit)**: Quantas requisições por minuto você pode fazer?
- **Alarmes (status)**: Algum provedor está desconectado? (vermelho = OFF, verde = ON)

```mermaid
%% legenda: Componentes principais do Dashboard OmniRoute
flowchart TB
  A["Dashboard OmniRoute<br/>:20127"]
  A --> B["Menu Esquerdo"]
  A --> C["Painel Principal"]
  B --> B1["Dashboard Home"]
  B --> B2["Providers"]
  B --> B3["Models"]
  B --> B4["Settings"]
  B --> B5["Logs"]
  C --> C1["Status Overview"]
  C --> C2["Gráficos de Uso"]
  C --> C3["Alertas"]
```

## 4. Técnica

### Acessar o Dashboard — Passo a Passo

**URL:**
```
http://81.17.103.186:20127
```

**Credenciais padrão:**
- Usuário: `admin`
- Senha: `omniroute_2026`

**Procedimento:**

1. Abra seu navegador (Chrome, Firefox, Safari, Edge)
2. Digite a URL na barra de endereços
3. Você verá uma tela de login
4. Insira as credenciais
5. Clique em **LOGIN** ou pressione ENTER
6. Você será redirecionado para o Dashboard

### Estrutura do Menu

Após login, você verá o menu esquerdo com as seguintes opções:

| Seção | Para quê | Acesso |
|---|---|---|
| **Dashboard** | Ver visão geral, status dos provedores, gráficos de uso | Home do dashboard |
| **Providers** | Adicionar, remover, ativar/desativar provedores | Gerenciar conexões |
| **Models** | Ver modelos disponíveis, testar cada um | Descobrir capacidades |
| **Settings** | Gerar API Keys, configurar rate limits, preferências | Administração |
| **Logs** | Ver histórico de requisições, erros, latência | Debugging |

### Tela Principal — Dashboard Home

Após fazer login, você vê um painel com:

- **Status Overview**: Quantos provedores estão ON/OFF
- **Total Requests**: Número de requisições processadas no período
- **Models Available**: Contagem de modelos únicos conectados
- **Credits Remaining**: Barra de progresso dos créditos (por provedor)

### Testando Conexão — Health Check

Se tiver problema ao acessar:

```bash
# Verificar se o container está rodando
ssh root@81.17.103.186 "docker ps | grep omniroute"

# Resultado esperado:
# aaaa1111 omniroute:latest ... Up 5 hours 0.0.0.0:20127->8080/tcp
```

Se houver erro, aguarde 30 segundos (pode estar iniciando) ou reinicie:

```bash
ssh root@81.17.103.186 "docker restart omniroute"
```

## 5. Aplica

### Cenário: Seu time precisa de acesso ao OmniRoute

**Situação:** Você é DevOps em uma startup de 10 pessoas. Apenas você tem a senha do OmniRoute, mas agora a equipe de ML quer monitorar os créditos e o time de produto quer testar modelos diferentes. Você diz "não posso compartilhar a senha admin com todos".

**Erro plausível:** Você mantém tudo centralizado em uma única conta admin. Quando você sai de férias, ninguém consegue adicionar um novo provedor ou investigar um erro.

**Diagnóstico:** Falta de **separação de privilégios**. Produção robusto exige granularidade: alguns usuários só podem ler logs, outros podem adicionar provedores, apenas admin pode mudar rate limits.

**Correção:** 

Crie usuários adicionais via **Settings → Users**:
- Malte (ML team): Acesso apenas para ver Models e Logs (leitura)
- Clara (Product): Acesso para testar Models, sem poder mudar Provider
- Você (DevOps): Acesso total (admin)

Cada um acessa o mesmo dashboard em `http://81.17.103.186:20127` com suas credenciais próprias.

### Armadilhas Comuns

1. **Compartilhar a senha admin** — Crie usuários em vez disso; nunca espalhe credenciais.
2. **Deixar o navegador aberto no computador compartilhado** — Logout sempre quando terminar.
3. **Usar credenciais default em produção** — Após primeiro acesso, mude a senha em **Settings → Account**.

## 6. Conclusão

O dashboard é seu espaço seguro de administração. Você explorará suas abas (Providers, Models, Logs) nos próximos capítulos. Por enquanto, a lição é simples: **você deve conseguir fazer login sem erros**. Se não conseguir, investigue antes de prosseguir.

## 7. Referências Bibliográficas

[1] OWASP. *Authentication Cheat Sheet*. Disponível em: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html. Acesso em: 24 ago. 2026.

[2] Docker Logs Documentation. *Docker Logging Driver*. Disponível em: https://docs.docker.com/config/containers/logging/. Acesso em: 24 ago. 2026.


---

# Capítulo 3: 15 Provedores Gratuitos — Seleção, Setup e Comparação

## 1. Introdução

No Capítulo 2, você aprendeu a navegar o dashboard. Agora vem a decisão crucial: **qual provedor usar?** Você não precisa de apenas um. OmniRoute permite conectar múltiplos provedores e fazer load balancing entre eles. Este capítulo apresenta os 15 provedores com tier gratuito, compara custo-benefício de cada um, e mostra os 3 passos idênticos para configurar qualquer um.

## 2. Explica

Provedores de IA diferem em **três dimensões**:

1. **Modelo**: Qual inteligência? (GPT-4, Claude, Gemini, Llama)
2. **Custo**: Gratuito, trial, ou pago (limitado neste livro apenas a gratuitos)
3. **Velocidade**: Latência de resposta (importante para chatbots)

Cada provedor também tem **limites próprios**:
- **Rate limit**: Quantas requisições por minuto? (100/min vs 10,000/min)
- **Créditos**: Quanto você gasta por 1000 tokens? (Grátis, $5 trial, 300 créditos)
- **Timeout**: Quanto tempo a resposta leva? (1s vs 30s)

O segredo da arquitetura OmniRoute é justamente isso: **você não fica preso a um provedor**. Se Vertex AI atingir rate limit, ele tenta OpenCode. Se OpenCode falhar, tenta Claude. Resiliência automática.

## 3. Ilustra

Pense em provedores como **diferentes rotas para ir de casa ao trabalho**.

Você tem 5 rotas:
- **Rota 1 (Vertex AI)**: Rápida, eficiente, mas lotada às 9 da manhã
- **Rota 2 (OpenCode)**: Mais lenta, mas nunca fica lotada
- **Rota 3 (Claude)**: Premium, mais cara, mas super rápida
- **Rota 4 (OpenAI)**: Populosa, confiável, custo moderado
- **Rota 5 (Groq)**: Experimental, muito rápida em certos horários

OmniRoute é seu **GPS inteligente**: ele sabe qual rota usar a cada momento. 9 da manhã? Desvia de Vertex e manda para OpenCode. Seu cliente precisa de máxima qualidade? Rota Claude. Precisa testar um novo modelo? Tenta Groq. Você não precisa pensar — o GPS pensa por você.

```mermaid
%% legenda: Visão geral dos 15 provedores e suas características
flowchart TB
  A["15 Provedores Gratuitos"]
  A --> B["Alta Qualidade<br/>Vertex AI<br/>Anthropic<br/>OpenAI"]
  A --> C["Open Source<br/>Groq<br/>Together<br/>HuggingFace"]
  A --> D["Especialização<br/>Replicate Image<br/>Stability AI<br/>Jina Embeddings"]
  B --> B1["300 credits/mês<br/>$5 trial<br/>$5 trial"]
  C --> C1["∞ requests<br/>$5 trial<br/>∞ requests"]
  D --> D1["$1/mês<br/>$20 trial<br/>∞ requests"]
```

## 4. Técnica

### Tabela Resumida — Os 15 Provedores

| # | Provedor | Free Tier | Créditos | Setup Dificuldade | Melhor para | Link |
|---|----------|-----------|----------|------------------|------------|------|
| 1 | **Vertex AI** | ✅ | 300/mês | ⭐⭐⭐ | Uso contínuo, qualidade | console.cloud.google.com |
| 2 | OpenCode | ✅ | ∞ | ⭐⭐⭐⭐ | Teste rápido, backup | N/A |
| 3 | Anthropic (Claude) | ✅ | $5 trial | ⭐⭐⭐ | Qualidade premium | console.anthropic.com |
| 4 | OpenAI | ✅ | $5 trial | ⭐⭐⭐ | GPT-4, imagens | platform.openai.com |
| 5 | Groq | ✅ | ∞ | ⭐⭐⭐ | Velocidade extrema | console.groq.com |
| 6 | Replicate | ✅ | $1/mês | ⭐⭐⭐ | Image generation | replicate.com |
| 7 | Together AI | ✅ | $5 trial | ⭐⭐⭐ | Open-source models | together.ai |
| 8 | Aleph Alpha | ✅ | ∞ | ⭐⭐ | NLP avançado | aleph-alpha.com |
| 9 | Hugging Face | ✅ | ∞ | ⭐⭐⭐ | 1000+ modelos | huggingface.co |
| 10 | Mistral AI | ✅ | ∞ | ⭐⭐⭐ | Open-source qualidade | mistral.ai |
| 11 | Cohere | ✅ | $100 trial | ⭐⭐⭐ | NLG, summarization | dashboard.cohere.ai |
| 12 | Perplexity | ✅ | ∞ | ⭐⭐⭐ | Search + resposta | api.perplexity.ai |
| 13 | Stability AI | ✅ | $20 trial | ⭐⭐⭐ | Image gen profissional | stability.ai |
| 14 | Jina AI | ✅ | ∞ | ⭐⭐⭐ | Embeddings, search | jina.ai |
| 15 | Kiro | ✅ | 50/mês | ⭐⭐⭐ | Alternativa barata | kiro.com |

### Procedimento Idêntico para Qualquer Provedor — 5 Passos

Todos os provedores seguem o mesmo fluxo em OmniRoute:

**Passo 1: Criar conta no provedor**

Exemplo com Anthropic:
```
1. Visite: console.anthropic.com
2. Click "Sign Up"
3. Preencha email e senha
4. Verifique email (check spam!)
5. Login
```

**Passo 2: Gerar API Key**

Cada provedor tem um lugar diferente:
- Anthropic: Console → API Keys → Create Key
- OpenAI: Platform → API Keys → Create New Key
- Vertex AI: Google Cloud → APIs → Create Credentials → Service Account

Resultado: Uma string tipo `sk-ant-abc123...` ou `ghp_abcd1234...`.

**Passo 3: Adicionar no OmniRoute**

No Dashboard OmniRoute:
```
1. Menu esquerdo → Providers
2. Click "+ Add Provider"
3. Procure pelo provedor (digite "Anthropic")
4. Click para selecionar
5. Preencha:
   - Name: "Anthropic" (ou qualquer nome)
   - API Key: [colar a chave do passo 2]
   - Status: Toggle para ON (verde)
6. Click "SAVE"
```

**Passo 4: Testar Conexão**

```
1. Menu → Models
2. Procure por modelo do provedor (ex: "claude-3-opus")
3. Click "TEST" ao lado do modelo
4. Aguarde 5 segundos
5. Deve aparecer "✅ Success"
```

Se falhar com "❌", verifique:
- A API Key está correta (sem espaços, completa)
- O provedor tem créditos/trial ativo
- O status em Providers está ON

**Passo 5: Usar em Código**

```python
import requests

response = requests.post(
    "http://81.17.103.186:20127/v1/chat/completions",
    headers={
        "Authorization": "Bearer sk-omniroute-...",
        "Content-Type": "application/json"
    },
    json={
        "model": "claude-3-opus",  # Modelo do provedor que você conectou
        "messages": [{"role": "user", "content": "Olá!"}]
    }
)

print(response.json()["choices"][0]["message"]["content"])
```

### Top 3 Recomendados para Começar

#### 🥇 1º: Vertex AI

- **Créditos**: 300/mês (mais generoso)
- **Modelos**: Gemini, PaLM, Claude, Llama
- **Setup**: 1 click via Google (OAuth)
- **Por quê**: Múltiplos modelos em um só provedor

#### 🥈 2º: OpenCode Free

- **Créditos**: ∞ (ilimitado)
- **Modelos**: Llama, Mistral
- **Setup**: Instantâneo (nenhuma configuração!)
- **Por quê**: Backup perfeito quando outros falham

#### 🥉 3º: Anthropic (Claude)

- **Créditos**: $5 trial
- **Modelos**: Claude 3 Opus (melhor qualidade)
- **Setup**: 5 minutos
- **Por quê**: Melhor qualidade, ótimo custo-benefício

## 5. Aplica

### Cenário: Você quer máxima confiabilidade com mínimo custo

**Situação:** Sua startup construiu um assistente de IA em chatbot. Está crescendo, e você precisa de modelo com ótima qualidade AND disponibilidade 24/7. Um único provedor é arriscado.

**Erro plausível:** Você escolhe apenas Vertex AI (mais créditos) e espera que 300/mês sejam suficientes. Quando bate o limite, o chatbot retorna erro `429 Rate Limited Exceeded` e seus clientes ficam frustrados.

**Diagnóstico:** **Monocultura de provedor**. Em produção, um único ponto de falha é aceitável só se impossível ter alternativa. Aqui, é impossível não ter.

**Correção com 3 Provedores:**

1. **Vertex AI** (Primário): 300 créditos/mês, qualidade = 4/5
2. **OpenCode** (Backup infinito): ∞ requisições, qualidade = 3/5
3. **Claude** (Premium): $5 trial + pago depois, qualidade = 5/5

Configura todos os três em OmniRoute com **prioridade**:
```
Providers:
- Vertex AI (Priority: 1) → ON
- OpenCode (Priority: 2) → ON
- Claude (Priority: 3) → ON
```

Fluxo automático:
- Primeira requisição → tenta Vertex AI
- Se Vertex falhar/atingir limite → tenta OpenCode
- Se OpenCode falhar → tenta Claude
- Se todos falharem → erro ao cliente (mas raro)

**Resultado**: Confiabilidade 99.9% + custos otimizados.

### Armadilhas Comuns

1. **Confundir modelo com provedor** — Modelo é `gpt-4` (OpenAI), provedor é `openai`. Não misture nomes.
2. **Não monitorar créditos** — Defina alarmes: "Avise quando atingir 80% de uso de créditos".
3. **Credenciais na string de conexão visível** — Nunca faça `url="...?key=sk-..."` em logs públicos.

## 6. Conclusão

Você agora conhece os 15 provedores, como configurar qualquer um em 5 passos idênticos, e por que conectar múltiplos é melhor que depender de um. O próximo capítulo te mostra como integrar tudo isso com Claude Code — sua IDE favorita.

## 7. Referências Bibliográficas

[1] Anthropic. *Claude API Documentation*. Disponível em: https://docs.anthropic.com. Acesso em: 24 ago. 2026.

[2] OpenAI. *Models Overview*. Disponível em: https://platform.openai.com/docs/models. Acesso em: 24 ago. 2026.

[3] Google Cloud. *Vertex AI API Documentation*. Disponível em: https://cloud.google.com/docs/vertex-ai. Acesso em: 24 ago. 2026.

[4] Groq. *Getting Started with Groq API*. Disponível em: https://console.groq.com/docs. Acesso em: 24 ago. 2026.

[5] Hugging Face. *Inference API Guide*. Disponível em: https://huggingface.co/docs/inference-api. Acesso em: 24 ago. 2026.


---

# Capítulo 4: Integrando OmniRoute com Claude Code

## 1. Introdução

Você configurou os provedores em OmniRoute. Agora vem a parte prática: **usar OmniRoute como seu backend de IA em Claude Code e Cursor**. Este capítulo mostra como adicionar OmniRoute como provedor customizado na sua IDE, escolher modelos, e começar a codificar.

## 2. Explica

Claude Code (e Cursor) são editores que precisam de um backend de IA. Por padrão, eles se conectam diretamente aos provedores (OpenAI, Anthropic, etc.). Com OmniRoute, você **intercepta essa conexão**: em vez de conectar direto ao OpenAI, sua IDE se conecta a OmniRoute, que depois roteia para o provedor que você escolher.

Do ponto de vista do código, é transparente — você não muda nada no seu projeto. Apenas muda a configuração de onde buscar a IA.

## 3. Ilustra

Pense em Claude Code como um **telefone**. Por padrão, ele liga direto para o OpenAI (PABX central). Com OmniRoute, você instala um **operador de telefonia privada** que intercepta suas ligações e decide qual PABX usar:

- Você faz a chamada normalmente: "Conecte-me a um modelo"
- O operador (OmniRoute) intercepta e pergunta: "Vertex AI está disponível agora?"
- Se sim, roteia para Vertex. Se não, tenta OpenCode.
- Você recebe a resposta na forma esperada.

```mermaid
%% legenda: Fluxo de integração Claude Code → OmniRoute → Provedores
flowchart LR
  A["Claude Code<br/>IDE"] -->|Chama /chat/completions| B["OmniRoute<br/>Proxy OpenAI"]
  B --> C{Provedor<br/>Disponível?}
  C -->|Vertex OK| D["Vertex AI"]
  C -->|OpenCode OK| E["OpenCode"]
  B --> F["Resposta<br/>Unificada"]
  D --> F
  E --> F
  F --> A
```

## 4. Técnica

### Passo 1: Gerar API Key do OmniRoute

No Dashboard OmniRoute:
```
1. Vá em: Settings → API Keys
2. Clique: "+ Generate New Key"
3. Você receberá uma chave tipo: sk-omniroute-abc123def456
4. COPIE e guarde em lugar seguro
```

### Passo 2: Adicionar em Claude Code (Web)

Se você usa Claude Code online (`claude.ai/code`):

```
1. Abra: https://claude.ai/code
2. Clique em Settings (ícone de engrenagem, canto superior)
3. Vá em: "API Providers" ou "Custom API"
4. Clique: "+ Add Custom Provider"
5. Preencha:
   - Name: OmniRoute
   - Endpoint: http://81.17.103.186:20127/v1
   - API Key: sk-omniroute-abc123...
   - Type: OpenAI-compatible
6. Clique: "Save" ou "Add"
7. Feche settings
```

### Passo 3: Adicionar em Cursor (Desktop)

Se você usa Cursor IDE:

```
1. Abra Cursor
2. Pressione: Ctrl + , (settings)
3. Procure: "API Provider" ou "Models"
4. Escolha: "Custom API" ou "OpenAI-Compatible"
5. Preencha:
   - Endpoint: http://81.17.103.186:20127/v1
   - API Key: sk-omniroute-abc123...
6. Salve
7. Reinicie Cursor se necessário
```

### Passo 4: Selecionar Modelo

Após configurar, ao abrir o chat ou autocomplete, você verá um dropdown com modelos disponíveis:

```
Available models:
▼ gpt-4
  gpt-3.5-turbo
  claude-3-opus
  claude-3-sonnet
  gemini-pro
  llama-70b
  mistral-large
```

Selecione o modelo que deseja usar. Se escolher `gpt-4` mas só tiver OpenCode conectado, OmniRoute automaticamente rota para `llama-70b` (que é similar).

### Passo 5: Usar Normalmente

Agora quando você digitar um prompt no chat ou pedir autocomplete:

```
// Seu prompt:
"Escreva uma função em Python que valida CPF"

// Claude Code rota para OmniRoute
// OmniRoute escolhe o melhor provedor
// Você recebe a resposta em segundos
// Você continua codificando normalmente
```

### Teste com cURL

Para validar que tudo está funcionando, teste via terminal antes de usar na IDE:

```bash
curl http://81.17.103.186:20127/v1/chat/completions \
  -H "Authorization: Bearer sk-omniroute-abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Olá!"}]
  }'
```

Resposta esperada:
```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1724000000,
  "model": "gpt-4",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Olá! Como posso ajudá-lo?"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## 5. Aplica

### Cenário: Seu time inteiro precisa usar modelos diferentes

**Situação:** Seu time tem 5 desenvolvedores. Alice prefere Claude (melhor para reasoning), Bob quer GPT-4 (familiar com OpenAI), Clara quer testar Mistral (modelo novo). Todas precisam de acesso, mas você tem orçamento limitado ($50/mês).

**Erro plausível:** Você cria 3 contas pagas diferentes (Anthropic, OpenAI, Together) e distribui as credenciais. Custos saem do controle: $30 (Anthropic) + $50 (OpenAI) + $20 (Together) = $100/mês. Orçamento estouro!

**Diagnóstico:** Você está pagando por 3 provedores quando poderia otimizar com free tiers e load balancing.

**Correção com OmniRoute:**

1. Conecta: Vertex AI (300 créditos/mês ≈ $50), OpenCode (grátis, ∞), Mistral (grátis)
2. Configura prioridade: Vertex → OpenCode → Mistral
3. Distribui a **mesma** API Key de OmniRoute para todo o time
4. Cada dev escolhe seu modelo na IDE:
   - Alice: `claude-3-opus` (rota via Vertex AI)
   - Bob: `gpt-4` (rota via Vertex AI)
   - Clara: `mistral-large` (rota via Mistral)

**Resultado**: Custo total = ~$50/mês, todos felizes, zero fricção de credenciais.

### Armadilhas Comuns

1. **Compartilhar API Key em repositório (Git)** — Use variáveis de ambiente: `OMNIROUTE_API_KEY` em `.env`.
2. **Testar com endpoint errado** — Confirme: `http://81.17.103.186:20127/v1` (com `/v1` no final).
3. **Esquecer `/v1` no endpoint** — Sem isso, 404 Not Found.

## 6. Conclusão

Você agora tem OmniRoute integrado com sua IDE. A última seção deste livro cobre troubleshooting — o que fazer quando algo der errado. Mas primeiro, teste: abra seu Claude Code, mude para OmniRoute como provedor, e faça um prompt simples. Se receber resposta, está tudo funcionando.

## 7. Referências Bibliográficas

[1] OpenAI API Reference. *Authentication*. Disponível em: https://platform.openai.com/docs/api-reference/authentication. Acesso em: 24 ago. 2026.

[2] Cursor Documentation. *Provider Setup Guide*. Disponível em: https://docs.cursor.sh/settings/providers. Acesso em: 24 ago. 2026.


---

# Capítulo 5: Troubleshooting — Resolvendo Problemas Comuns

## 1. Introdução

Nem sempre tudo funciona na primeira tentativa. Este capítulo é seu **guia de diagnóstico** para os problemas mais comuns: conexão recusada, API Key inválida, modelo não encontrado, rate limits excedidos, créditos expirados. Cada problema tem causas raiz e soluções progressivas — comece pela mais simples.

## 2. Explica

Troubleshooting segue uma **metodologia de diagnóstico em camadas**:

1. **Camada de Rede**: Consegue alcançar OmniRoute? (ping, DNS)
2. **Camada de Autenticação**: API Key válida e ativa? (Bearer token)
3. **Camada de Provider**: O provedor está conectado em OmniRoute? (Status ON)
4. **Camada de Modelo**: O modelo existe e está disponível? (Models list)
5. **Camada de Limite**: Rate limit ou crédito não excedido? (Billing)

Trabalhar camada por camada evita perder tempo em causas erradas.

## 3. Ilustra

Troubleshooting é como **diagnosticar um carro que não liga**:

- **Camada 1**: Tem combustível? (Rede alcançável?)
- **Camada 2**: Chaves estão no carro? (Credenciais corretas?)
- **Camada 3**: Motor está ok? (Provedor ON?)
- **Camada 4**: Ignição funciona? (Modelo disponível?)
- **Camada 5**: Limite de velocidade OK? (Rate limit?)

Se você pular direto para "trocar motor" sem verificar se tem combustível, vai desperdiçar tempo.

```mermaid
%% legenda: Árvore de diagnóstico para problemas de conexão
flowchart TD
  A["Erro ao conectar OmniRoute"]
  A --> B{"Consegue acessar<br/>81.17.103.186:20127?"}
  B -->|Não| C["Problema de Rede"]
  B -->|Sim| D{"Dashboard<br/>carrega?"}
  D -->|Não| E["Firewall/VPS Down"]
  D -->|Sim| F{"API Key<br/>válida?"}
  F -->|Não| G["Gerar nova no Settings"]
  F -->|Sim| H{"Provedor<br/>Status=ON?"}
  H -->|Não| I["Ativar em Providers"]
  H -->|Sim| J["Teste Models → TEST"]
```

## 4. Técnica

### Problema 1: "Conexão Recusada" (Connection Refused)

**Erro comum:**
```
Connection refused to 81.17.103.186:20127
ou
Failed to connect: ECONNREFUSED 127.0.0.1:20127
```

**Causas possíveis:**
1. OmniRoute container não está rodando
2. Firewall bloqueando porta 20127
3. Endereço IP ou porta errados

**Solução progressiva:**

**Passo 1: Verificar se container está rodando**
```bash
ssh root@81.17.103.186 "docker ps | grep omniroute"
```

Resultado esperado:
```
aaaa1111 omniroute:latest ... Up 5 hours 0.0.0.0:20127->8080/tcp
```

Se não aparecer, o container caiu. Reinicie:
```bash
ssh root@81.17.103.186 "docker restart omniroute"
```

Aguarde 30 segundos e tente novamente.

**Passo 2: Verificar firewall**
```bash
# Se está em AWS/VPS:
ssh root@81.17.103.186 "ufw status | grep 20127"

# Resultado esperado: 20127 ALLOW
# Se não aparecer, abra a porta:
ssh root@81.17.103.186 "ufw allow 20127"
```

**Passo 3: Ping simples**
```bash
ping 81.17.103.186

# Resultado esperado: 4 packets transmitted, 4 received
# Se falhar (100% loss), problema de rede sua — check VPN/DNS
```

### Problema 2: "API Key Inválida" (Unauthorized 401)

**Erro comum:**
```json
{
  "error": {
    "message": "Invalid API Key",
    "type": "invalid_request_error",
    "code": 401
  }
}
```

**Causas possíveis:**
1. API Key tem espaços em branco extras
2. API Key não foi copiada completamente
3. API Key expirou ou foi revogada
4. Provedor desativado em OmniRoute (Status OFF)

**Solução progressiva:**

**Passo 1: Verificar API Key**
```bash
# Copie de novo em Dashboard → Settings → API Keys
# Compare no terminal (sem espaços):

echo "sk-omniroute-abc123def456"  # Sua chave copiada
# Deve ser idêntica, sem espaço no início ou final
```

**Passo 2: Testar com curl**
```bash
curl "http://81.17.103.186:20127/v1/models" \
  -H "Authorization: Bearer sk-omniroute-abc123def456"

# Resultado esperado: lista de modelos em JSON
# Se retorna 401, chave realmente inválida
```

**Passo 3: Regenerar chave**
Se suspeitar que a chave foi comprometida:
```
1. Dashboard → Settings → API Keys
2. Procure a chave antiga
3. Clique "Revoke"
4. Clique "+ Generate New Key"
5. Copie a nova chave
6. Atualize em Claude Code / seu código
```

**Passo 4: Verificar provedores**
Se tudo acima OK, mas ainda 401, verifique:
```
1. Dashboard → Providers
2. Confirme que todos os provedores têm Status = ON (verde)
3. Se algum estiver OFF, clique para ativar
```

### Problema 3: "Modelo Não Encontrado" (Model Not Found 404)

**Erro comum:**
```json
{
  "error": {
    "message": "Model not found: gpt-4",
    "type": "invalid_request_error"
  }
}
```

**Causas possíveis:**
1. Modelo não existe em nenhum provedor conectado
2. Provedor que tem o modelo está OFF
3. Nome do modelo errado

**Solução progressiva:**

**Passo 1: Listar modelos disponíveis**
```bash
curl "http://81.17.103.186:20127/v1/models" \
  -H "Authorization: Bearer sk-omniroute-abc123..."

# Resultado: JSON com lista completa de modelos disponíveis
```

**Passo 2: Verificar se modelo existe**

Procure seu modelo na lista. Exemplos:
- `gpt-4` (requer OpenAI ou Vertex conectado)
- `claude-3-opus` (requer Anthropic ou Vertex)
- `llama-70b` (requer OpenCode, Groq ou Together)

Se não aparecer, significa nenhum provedor tem esse modelo.

**Passo 3: Adicionar provedor que tem o modelo**

Se quer `gpt-4` mas não tem OpenAI:
```
1. Dashboard → Providers → + Add Provider
2. Procure "OpenAI"
3. Gere API Key em platform.openai.com
4. Cole em OmniRoute
5. Salve
6. Aguarde 30 segundos (sync de modelos)
7. Teste novamente
```

### Problema 4: "Rate Limit Excedido" (429 Too Many Requests)

**Erro comum:**
```json
{
  "error": {
    "message": "Rate limit exceeded",
    "type": "rate_limit_error",
    "code": 429
  }
}
```

**Causas:**
1. Você fez muitas requisições muito rápido
2. Um único provedor está recebendo toda carga
3. Limite diário do provedor foi atingido

**Solução progressiva:**

**Passo 1: Aguardar (solução imediata)**
```bash
# Espere 1-2 minutos e tente novamente
# Rate limits são temporários
sleep 60
curl ... # retry
```

**Passo 2: Conectar múltiplos provedores (solução estrutural)**

Se quer evitar rate limit, não dependa de um único provedor:
```
1. Dashboard → Providers
2. Adicione 2-3 provedores com free tier
3. OmniRoute distribui requisições automaticamente
4. Mesmo que um atinja limit, outros absorvem carga
```

**Passo 3: Implementar backoff exponencial no código**

```python
import time
import requests

def chat_with_retry(prompt, max_retries=3, backoff_factor=2):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "http://81.17.103.186:20127/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"model": "gpt-4", "messages": [{"role": "user", "content": prompt}]}
            )
            
            if response.status_code == 429:
                wait_time = backoff_factor ** attempt
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
    
    return None

# Uso
chat_with_retry("Escreva um poema")
```

### Problema 5: "Crédito Expirou" (Insufficient Balance)

**Erro comum:**
```
Free trial expired ou Credits exhausted
```

**Solução:**
1. Dashboard → Providers
2. Veja qual provedor está sem crédito
3. Escolha: (a) renovar trial daquele provedor, ou (b) usar outro provedor como primary

## 5. Aplica

### Cenário: Seu cliente relata erro vago "não funciona mais"

**Situação:** Você deployou OmniRoute 2 semanas atrás. Tudo funcionando. Hoje seu cliente relata: "Seu sistema de IA não está respondendo". Você checa o código — está certo. Chat não responde. Pânico?

**Erro plausível:** Você pula direto para "deve ser um bug no código" e passa horas debugando, quando a causa é muito simples.

**Diagnóstico com Troubleshooting:**

1. ✅ Consegue acessar `http://81.17.103.186:20127`? (SIM — rede OK)
2. ✅ Dashboard carrega? (SIM — OmniRoute roda)
3. ⚠️ API Key válida? (SIM — curl test OK)
4. ❌ Modelo disponível? (NÃO — lista vazia!)

**Causa raiz:** Todos os provedores estão OFF! Alguém deve ter desativado por acidente.

**Correção em 2 minutos:**
```
1. Dashboard → Providers
2. Vê que todos estão com Status = OFF
3. Clica em cada um para ativar (toggle verde)
4. Aguarda 30 segundos
5. Testa novamente
6. ✅ Funciona!
```

Se você tivesse pulado para "debug de código", seria mais 30 minutos perdidos.

## 6. Conclusão

Troubleshooting é 80% **diagnóstico metódico** e 20% **know-how técnico**. Trabalhe camada por camada, comece pelas causas mais simples, e você resolve 99% dos problemas em minutos. Se este capítulo não resolveu seu caso específico, você pode:

1. Consultar logs: Dashboard → Logs (vê requisições e erros)
2. Testar com curl: Elimina variáveis de código
3. Contactar suporte: OmniRoute Discord / comunidade

## 7. Referências Bibliográficas

[1] HTTP Status Codes. *RFC 7231 — HTTP Semantics and Content*. Disponível em: https://tools.ietf.org/html/rfc7231. Acesso em: 24 ago. 2026.

[2] Docker Documentation. *Troubleshooting Guide*. Disponível em: https://docs.docker.com/config/containers/logging/. Acesso em: 24 ago. 2026.

[3] OpenAI API. *Error Handling*. Disponível em: https://platform.openai.com/docs/guides/error-handling. Acesso em: 24 ago. 2026.


---

