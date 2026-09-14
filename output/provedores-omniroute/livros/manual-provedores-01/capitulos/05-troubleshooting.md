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
