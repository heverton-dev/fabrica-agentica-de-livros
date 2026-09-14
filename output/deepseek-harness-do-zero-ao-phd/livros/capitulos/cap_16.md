# Capítulo 16: Deploy e Operacao: Levando a Oficina para Producao

## 1. Introdução

Você chegou ao último capítulo. Ao longo dos 15 capítulos anteriores, montou sua oficina de agentes do zero — instalou o harness, escolheu o modelo, configurou o engine, gerenciou plugins, orquestrou pipelines, construiu ferramentas customizadas, implementou RAG, fez fine-tuning, coordenou múltiplos agentes, e criou profiles otimizados [1].

Agora é hora de levar tudo isso para produção. Neste capítulo, você vai containerizar o harness com Docker, configurar monitoramento e observabilidade, implementar rate limiting e fallback entre modelos, e estabelecer uma rotina de manutenção contínua. É o momento em que a oficina pessoal se torna uma concessionária profissional [2].

## 2. Explica

### Docker e Containerização

A containerização é essencial para deploy em produção [3]:

- **Reprodutibilidade:** o mesmo container funciona em qualquer máquina
- **Isolamento:** o harness não interfere com outros serviços
- **Escalabilidade:** fácil de duplicar containers para múltiplos usuários
- **GPU Passthrough:** NVIDIA Container Toolkit permite acesso a GPU dentro do container

Um detalhe que separa um Dockerfile de laboratório de um Dockerfile de produção é o **multi-stage build**: uma etapa instala dependências de compilação (que pesam centenas de MB e não são necessárias em runtime), e uma segunda etapa copia só os artefatos finais para uma imagem base mínima. O resultado prático é uma imagem menor — menos superfície de ataque, menos tempo de pull no deploy, menos custo de storage no registry [3]. A alternativa (uma única etapa, com todo o toolchain de build dentro da imagem final) funciona no dia 1, mas em produção contínua isso significa reconstruir e repuxar uma imagem inchada a cada deploy.

### Monitoramento e Observabilidade

Em produção, você precisa saber o que está acontecendo com seu agente [4]. A prática consolidada de observabilidade em sistemas distribuídos organiza isso em quatro sinais — latência, tráfego, taxa de erro e saturação — e o harness em produção não é exceção:

- **Logs:** registro de todas as ações do agente para debug
- **Métricas:** latência, throughput, erro rate, uso de VRAM
- **Tracing:** rastreamento completo de cada requisição do início ao fim
- **Alertas:** notificações quando algo sai do esperado

A saturação de VRAM merece atenção especial num harness local: diferente de latência ou erro rate (que degradam gradualmente), esgotar VRAM tende a ser um evento binário — o processo simplesmente crasha ou passa a rejeitar requisições, sem aviso prévio gradual. É por isso que o incidente descrito na seção Aplica deste capítulo levou horas para ser percebido: sem um alerta específico de saturação de VRAM, o sintoma visível (erros 500 intermitentes) não apontava direto para a causa raiz.

### Rate Limiting e Fallback

Proteção contra abuso e garantia de disponibilidade [1]:

- **Rate limiting:** limitar requisições por usuário/tempo
- **Fallback de modelo:** se o modelo primário falhar, usar um secundário
- **Circuit breaker:** parar de tentar um serviço que está fora do ar

O circuit breaker (padrão consolidado em sistemas distribuídos, análogo ao disjuntor elétrico que dá nome à técnica) tem três estados: **fechado** (tráfego normal, falhas são apenas contadas), **aberto** (após N falhas consecutivas, o circuito para de tentar o serviço primário e desvia direto para o fallback, sem gastar tempo de timeout em cada tentativa) e **semiaberto** (depois de um intervalo de espera, deixa passar 1 requisição de teste para checar se o serviço primário voltou — se sim, fecha o circuito; se não, volta a abrir). Sem circuit breaker, um modelo primário instável degrada a experiência de TODOS os usuários, porque cada requisição paga o custo total do timeout antes de cair no fallback; com circuit breaker, esse custo é pago uma vez, não a cada requisição.

### Manutenção Contínua

Deploy não é um evento único — é o início de uma rotina. Três eixos de manutenção que um harness em produção exige, e que costumam ser esquecidos até virarem incidente:

1. **Atualização de modelo:** novas versões do modelo primário (ou do secundário de fallback) trazem melhorias, mas também podem mudar comportamento sutilmente — o mesmo prompt pode produzir uma resposta diferente. A prática recomendada é atualizar em um ambiente de staging primeiro, rodar a suíte de avaliação do time contra o novo modelo, e só promover para produção depois de comparar métricas de qualidade antes/depois — nunca atualizar o modelo de produção diretamente na primeira disponibilidade da versão nova.
2. **Atualização de dependências e imagem base:** a imagem Docker herda vulnerabilidades da imagem base e das dependências do sistema operacional; deixar de reconstruir a imagem por meses acumula CVEs conhecidas sem que o código do harness em si tenha mudado. Um rebuild periódico (mesmo sem mudança de código) mantém a superfície de vulnerabilidade sob controle.
3. **Rotação e limpeza de logs/sessões:** logs estruturados e sessões duráveis crescem indefinidamente se não houver retenção configurada — o script de backup mostrado nesta seção já inclui uma política de expurgo (30 dias), mas o mesmo raciocínio vale para os logs do Prometheus/Grafana e para o próprio audit log de produção: sem rotação, o disco enche, e "disco cheio" é uma das causas mais banais — e mais evitáveis — de queda de serviço em produção.

Nenhum desses três eixos é tecnicamente complexo isoladamente. O que os torna um risco real é justamente a previsibilidade da negligência: são tarefas de baixa urgência percebida no dia a dia, até o dia em que a ausência de uma delas causa o próprio incidente que uma rotina teria evitado.

## 3. Ilustra

### A Oficina em Produção

Levar a oficina para produção é como abrir uma concessionária. Na oficina pessoal, você podia fazer o que quisesse — deixar peças espalhadas, testar ferramentas novas, quebrar coisas sem consequência. Na concessionária, tudo precisa ser profissional: atendimento rápido, qualidade consistente, sem surpresas para o cliente [5].

O Docker é o prédio da concessionária — uma estrutura padronizada que pode ser replicada em qualquer cidade. O monitoramento são as câmeras e sensores que mostram se tudo está funcionando. O rate limiting é o controle de fluxo de clientes — não deixar mais gente entrar do que a concessionária aguenta atender. O fallback é o plano B — se a peça original não estiver disponível, usar uma equivalente.

```mermaid
%% legenda: Arquitetura de produção — Docker, monitoramento, rate limiting, fallback
flowchart TB
    subgraph Producao["Produção"]
        LB[Load Balancer]
        LB --> C1[Container 1]
        LB --> C2[Container 2]
        LB --> C3[Container N]
        
        C1 --> GPU[GPU (NVIDIA)]
        C2 --> GPU
        C3 --> GPU
        
        MON[Monitoramento] --> C1
        MON --> C2
        MON --> C3
        
        RL[Rate Limiter] --> LB
        
        FB[Fallback Model] -.->|se primário falhar| C1
    end
    
    USR[Usuários] --> RL
    
    style Producao fill:#7C3AED,color:#fff
    style USR fill:#10B981,color:#fff
```

## 4. Técnica

### Dockerfile para DeepSeek Harness

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

### Docker Compose com GPU

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

### Monitoramento com Prometheus

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

### Rate Limiting

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

### Circuit Breaker

```yaml
# dsh.config.yaml — circuit breaker
circuit_breaker:
  enabled: true
  failure_threshold: 5        # falhas consecutivas para abrir o circuito
  open_duration: 30s          # tempo em estado aberto antes de testar de novo
  half_open_max_calls: 1      # requisições de teste permitidas no semiaberto
  fallback_on_open: "secondary"
```

### Backup de Sessões

```bash
#!/usr/bin/env bash
# backup-sessions.sh — roda via cron diário
set -euo pipefail
DATA=$(date +%Y-%m-%d)
DESTINO="/backups/dsh-sessions-${DATA}.tar.gz"
tar -czf "$DESTINO" -C /root/.dsh sessions/
find /backups -name "dsh-sessions-*.tar.gz" -mtime +30 -delete  # retenção 30 dias
echo "[backup] OK: $DESTINO"
```

## 5. Aplica

### O Deploy que Caiu na Primeira Noite

Um desenvolvedor fez deploy do harness em produção sem healthcheck. Na primeira noite, o modelo crashed por falta de VRAM (outro serviço estava usando a GPU). O harness ficou retornando erros por 8 horas antes de alguém perceber [4]. O diagnóstico, quando finalmente aconteceu, levou minutos — mas chegar até ele levou horas, porque não havia alerta específico de saturação de VRAM, só o sintoma indireto (erros 500 esporádicos que pareciam intermitência de rede).

A correção não foi só adicionar o healthcheck que faltava — foi reconhecer que "o processo está rodando" e "o processo está funcionando" são verificações diferentes. Um healthcheck de liveness (o processo responde?) não pega esse tipo de falha, porque o processo continuava de pé, só que devolvendo erro em toda chamada de inferência. Foi preciso um healthcheck de readiness que de fato chamasse o modelo com um prompt mínimo e validasse a resposta, não só a porta TCP.

### A Prática Correta

Checklist de deploy em produção:

| Item | Status | Config |
|------|--------|--------|
| Dockerfile | ✅ | Multi-stage build |
| GPU passthrough | ✅ | NVIDIA Container Toolkit |
| Healthcheck | ✅ | `/health` a cada 30s |
| Rate limiting | ✅ | 60 req/min por usuário |
| Fallback | ✅ | Modelo secundário automático |
| Logs | ✅ | Structured JSON |
| Métricas | ✅ | Prometheus + Grafana |
| Alertas | ✅ | Erro rate > 5% |
| Backup | ✅ | Sessões diárias |
| SSL/TLS | ✅ | Let's Encrypt |

O fallback de modelo secundário resolve indisponibilidade do modelo primário, mas não escala como solução para todo tipo de degradação: se o modelo secundário é menor (no exemplo deste capítulo, 7B contra 14B), ele responde com menos qualidade — aceitável para manter o serviço no ar por minutos, não recomendado como estado permanente. Acima de alguns minutos no secundário, o alerta deveria escalar de "degradação tolerável" para "incidente" que exige intervenção humana, não só o circuit breaker sozinho decidindo por quanto tempo ficar nesse modo.

### Rollback: Canary e Blue-Green

A checklist de deploy desta seção cobre o estado estável — mas o momento de maior risco não é operar em regime, é o instante da troca de versão. Duas estratégias reduzem esse risco, e nenhuma delas depende do healthcheck sozinho para decidir se o deploy deu certo:

- **Canary:** a nova versão recebe uma fração pequena do tráfego real (por exemplo, redirecionando um subconjunto de sessões novas), enquanto a versão estável continua atendendo o resto. Métricas de erro e latência da fração canary são comparadas com a versão estável antes de expandir gradualmente — se a nova versão degradar, o dano fica contido a essa fração pequena.
- **Blue-green:** duas versões completas rodam em paralelo (blue = atual, green = nova); o load balancer aponta todo o tráfego para uma versão de cada vez, nunca para as duas ao mesmo tempo. A troca é instantânea, e o rollback também — basta apontar o load balancer de volta para a versão anterior, sem esperar um novo deploy.

Nenhuma das duas estratégias substitui o healthcheck de readiness discutido na seção Aplica — elas decidem QUANDO expor a nova versão a tráfego real; o healthcheck decide SE a nova versão está de fato pronta para receber esse tráfego. Um deploy canary de uma versão com o mesmo bug de saturação de VRAM do incidente descrito nesta seção teria limitado o impacto a uma fração dos usuários, mas não teria evitado o incidente por si só — só o healthcheck de readiness correto faz isso.

### Runbook: Respondendo a uma Saturação de VRAM

Para o tipo de incidente descrito nesta seção — modelo crashando por falta de VRAM — um runbook curto evita que a resposta dependa de alguém lembrar os passos certos sob pressão, de madrugada:

1. **Confirme o sintoma:** o healthcheck de readiness está falhando, ou só o de liveness? Se o processo responde na porta mas a inferência falha, é saturação de recurso (VRAM/RAM), não crash do processo — os dois exigem diagnóstico diferente.
2. **Verifique quem mais está usando a GPU:** `nvidia-smi` mostra todos os processos com VRAM alocada. Se outro serviço subiu depois do harness e não havia isolamento de GPU dedicado, esse é o suspeito principal.
3. **Force o fallback manualmente, se o circuit breaker ainda não abriu:** não espere o circuito abrir sozinho se o impacto para o usuário já está acontecendo — abrir manualmente corta o tempo de degradação.
4. **Depois de estabilizar, não feche o incidente sem adicionar o alerta que faltou:** o ponto central deste capítulo é que o sintoma (erro 500 esporádico) não apontava para a causa raiz (saturação de VRAM) sem um alerta específico — se esse alerta não existia antes do incidente, ele precisa existir depois, ou o mesmo incidente se repete.

Esse runbook não substitui o julgamento de quem está respondendo — mas garante que os primeiros minutos, que são os que mais determinam se o incidente dura pouco tempo ou o resto do turno, não dependam de reconstruir o raciocínio do zero.

## 6. Conclusão

Parabéns — você chegou ao fim do livro. Ao longo dos 16 capítulos, você construiu uma oficina completa de agentes de IA: desde a instalação básica até o deploy em produção, passando por plugins, ferramentas, pipelines, RAG, fine-tuning, multi-agente, e profiles.

O DeepSeek Harness não é apenas uma ferramenta — é uma plataforma que evolui com você. Cada capítulo deste livro é uma peça que você pode combinar, substituir, ou melhorar conforme sua necessidade cresce.

O ecossistema está apenas começando. O Cordis é novo, os plugins estão amadurecendo, e as possibilidades de personalização são virtualmente infinitas. Como Engenheiro de Agentes, você agora tem as habilidades para não apenas usar essa tecnologia — mas para moldá-la de acordo com suas necessidades.

### O Fio que Atravessou os 16 Capítulos

Se há um padrão que se repetiu, disfarçado, em quase todo capítulo deste livro, é este: cada camada de sofisticação que você adicionou existia para tornar visível um limite que, sem ela, ficaria invisível até dar errado. O sandbox do Capítulo 8 não existe para impedir que o agente funcione — existe para que um erro do agente tenha um raio de dano conhecido em vez de ilimitado. O circuit breaker e o rate limiting deste capítulo não existem para desacelerar o sistema — existem para que uma falha do modelo primário custe uma degradação previsível, não um colapso total. O runbook de incidente não existe para substituir julgamento — existe para que o julgamento, sob pressão, não precise reconstruir do zero um raciocínio que já foi feito com calma antes.

Essa é a diferença entre uma oficina pessoal e uma concessionária profissional que a metáfora deste capítulo tentou capturar: não é sofisticação por sofisticação — é a disposição de perguntar, antes que algo quebre, "o que acontece quando isso não funcionar?" e responder essa pergunta em configuração, não em pânico. Você vai continuar encontrando esse padrão fora deste livro, em qualquer sistema que opere em produção por tempo suficiente: escala não é sobre fazer mais rápido, é sobre saber, com antecedência, onde e como a coisa para de funcionar.

A oficina está pronta. O motor está calibrado. As ferramentas estão afiadas. É hora de produzir.

## 7. Referências Bibliográficas

[1] DEEPSEEK AI. *DeepSeek Harness developer preview*. Disponível em: https://deepseek.com/harness/en/. Acesso em: 23 ago. 2026.

[2] COMETAPI. *6 Methods to Deploy DeepSeek Harness Locally*. Disponível em: https://www.cometapi.com/how-to-install-and-deploy-deepseek-harness-locally/. Acesso em: 23 ago. 2026.

[3] ATLASCLOUD. *How to Install DeepSeek Harness in 10 Minutes*. Disponível em: https://www.atlascloud.ai/blog/tips/how-to-install-deepseek-harness. Acesso em: 23 ago. 2026.

[4] TOWARDS AI. *DeepSeek Harness vs Claude Code*. Disponível em: https://pub.towardsai.net/deepseek-harness-vs-claude-code-a-plugin-architecture-teardown-da3c916f3af1. Acesso em: 23 ago. 2026.

[5] HABR. *Inside DeepSeek Harness*. Disponível em: https://habr.com/en/articles/1070958/. Acesso em: 23 ago. 2026.

[6] FLOATBOAT.AI. *Cordis — The Plugin Kernel*. Disponível em: https://floatboat.ai/blog/cordis-plugin-framework. Acesso em: 23 ago. 2026.

[7] AGENTATLAS. *Cordis Explained*. Disponível em: https://agentatlas.org/blog/cordis-explained-how-deepseek-harness-plugin-framework-works/. Acesso em: 23 ago. 2026.

[8] MEDIUM (data-and-beyond). *Decoding DeepSeek Harness*. Disponível em: https://medium.com/data-and-beyond/decoding-deepseek-harness-the-open-source-runtime-behind-composable-ai-agents-c2299e992870. Acesso em: 23 ago. 2026.

[9] ATLASCLOUD. *DeepSeek Harness Plugins: The 7 Worth It*. Disponível em: https://www.atlascloud.ai/blog/tips/deepseek-harness-plugins. Acesso em: 23 ago. 2026.

[10] COMPOSIO. *Best plugins for DeepSeek Harness*. Disponível em: https://composio.dev/content/best-deepseek-harness-plugins. Acesso em: 23 ago. 2026.

[11] MINDSTUDIO. *What Is DeepSeek Harness?*. Disponível em: https://www.mindstudio.ai/blog/deepseek-harness-agentic-coding. Acesso em: 23 ago. 2026.

[12] DATACAMP. *DeepSeek Harness Tutorial*. Disponível em: https://www.datacamp.com/tutorial/deepseek-harness. Acesso em: 23 ago. 2026.

[13] SPRINGBRAND. *DeepSeek Harness (dsh): Everything Is a Plugin*. Disponível em: https://springbrand.ai/deepseek-harness. Acesso em: 23 ago. 2026.

[14] YOUTUBE. *Every Deepseek Harness Concept Explained*. Disponível em: https://www.youtube.com/watch?v=24UCnAs7MVg. Acesso em: 23 ago. 2026.

[15] YOUTUBE. *NEW Deepseek Agent Harness EXPLAINED*. Disponível em: https://www.youtube.com/watch?v=Hpw4fAHlHDw. Acesso em: 23 ago. 2026.

[16] EXPLOREX.AI. *DeepSeek Harness v0.1*. Disponível em: https://explainx.ai/blog/deepseek-harness-v0-1-plugin-first-agent-stack-august-2026. Acesso em: 23 ago. 2026.

[17] DEEPSEEKHARNESSAI. *Security Plugins for DeepSeek Harness*. Disponível em: https://deepseekharnessai.com/categories/security. Acesso em: 23 ago. 2026.

[18] MEDIUM (kaliarch). *DeepSeek Harness: When the Agent Loop Itself Becomes a Plugin*. Disponível em: https://medium.com/@kaliarch/deepseek-harness-when-the-agent-loop-itself-becomes-a-plugin-7fad0aa9de1c. Acesso em: 23 ago. 2026.

[19] 0XSLINE. *awesome-deepseek-harness*. GitHub. Disponível em: https://github.com/0xsline/awesome-deepseek-harness. Acesso em: 23 ago. 2026.

[20] LINKEDIN (Tony Ren). *DeepSeek Harness: Agent Operating System*. Disponível em: https://www.linkedin.com/posts/tonyren_i-spent-the-evening-in-the-deepseek-harness-activity-7493848102076882944-GGXB. Acesso em: 23 ago. 2026.
