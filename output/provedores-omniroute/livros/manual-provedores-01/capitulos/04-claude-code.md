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
