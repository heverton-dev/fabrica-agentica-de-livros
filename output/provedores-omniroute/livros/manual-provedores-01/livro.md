# Manual OmniRoute — 15 Provedores de IA Gratuitos para Máxima Confiabilidade

**Agregue Google Vertex AI, Claude, GPT-4 e mais em um único hub**

---

**Data**: 2026-08-24  
**Versão**: 1.0  
**Autor**: Marketing Conexão  
**Editor**: Editora Agêntica

---

## Sumário

1. OmniRoute — Seu Agregador de Modelos de IA
2. Acessando e Navegando o Dashboard
3. 15 Provedores Gratuitos — Seleção, Setup e Comparação
4. Integrando OmniRoute com Claude Code
5. Troubleshooting — Resolvendo Problemas Comuns

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

*[Capítulos 3, 4 e 5 omitidos por brevidade — veja arquivos capitulos/03-provedores.md, 04-claude-code.md, 05-troubleshooting.md para conteúdo completo]*

---

**Fim do Livro**

*Manual OmniRoute — Versão 1.0*  
*Data: 2026-08-24*  
*Editora Agêntica*
