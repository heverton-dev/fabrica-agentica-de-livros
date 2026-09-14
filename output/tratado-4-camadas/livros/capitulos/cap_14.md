# Capítulo 14: A Matriz de 3 Tiers de Modelos: Otimização de Custo e Performance

## 1. Introdução

Você já entendeu que usar o modelo mais caro para tarefas simples é como usar uma bazuca para matar um mosquito [1].

Mas como escolher exatamente qual modelo utilizar na prática? Quais são as opções disponíveis no mercado atual e como elas se comparam em velocidade, capacidade e custo? [1] [2]

Para evitar que você fique perdido no labirinto de centenas de nomes de modelos lançados a cada mês, a Fábrica Agêntica consolidou a **Matriz Universal de 3 Tiers de Modelos** [1].

Neste capítulo, você aprenderá as características de cada Tier, quando acionar cada um e como configurar o seu ambiente para alternar entre eles com precisão cirúrgica [1].

## 2. Explica

### 2.1 A Estrutura dos 3 Tiers Cognitivos

A matriz divide todos os modelos do mercado em três patamares operacionais [1] [3]:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   A MATRIZ DE 3 TIERS COGNITIVOS                       │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 1: RÁPIDO & ECONÔMICO (Operários Mecânicos)                       │
│ - Modelos: Gemini 2.0 Flash, Claude 3.5 Haiku, GPT-4o Mini            │
│ - Custo: ~US$ 0.10 a US$ 0.80 por Milhão de Tokens                     │
│ - Uso: Filtros, regex, JSON formatting, renomeações, triagem           │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 2: DESENVOLVIMENTO EQUILIBRADO (O Engenheiro Pleno)               │
│ - Modelos: Claude 3.7 Sonnet (Standard), DeepSeek-V3, Codex, GPT-4o    │
│ - Custo: ~US$ 2.50 a US$ 3.00 por Milhão de Tokens                     │
│ - Uso: Codificação diária, criação de endpoints, testes unitários      │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 3: RACIOCÍNIO PESADO (O Arquiteto Chefe)                          │
│ - Modelos: Claude 3.7 Sonnet Thinking, OpenAI o3-mini, Gemini Thinking │
│ - Custo: ~US$ 3.00 a US$ 15.00 por Milhão de Tokens                    │
│ - Uso: Arquitetura de sistemas, segurança, concorrência e matemática   │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.2 As Regras de Transição entre Tiers

Como o Engenheiro Agêntico opera essa matriz no dia a dia? [1]
1. **Regra do Default Econômico**: Toda tarefa começa, por padrão, no **Tier 1** ou **Tier 2** [1].
2. **Escalação Condicional**: Se o Tier 2 tentar resolver um problema complexo e falhar por duas vezes consecutivas, o sistema escala automaticamente a tarefa para o **Tier 3** [1] [4].
3. **Desescalada Imediata**: Assim que o Tier 3 resolve o nó arquitetural e define o plano, a implementação dos arquivos volta imediatamente para o **Tier 2** ou **Tier 1** [1].

## 3. Ilustra

Veja o fluxo de escalação inteligente da matriz de Tiers:

```mermaid
%% legenda: A Matriz de 3 Tiers em Ação
flowchart TD
    A["Nova Tarefa de Software"] --> B["Tier 1: Extração e Triagem Mecânica"]
    B --> C["Tier 2: Implementação do Código e Testes"]
    C --> D{"Testes Passaram no Tier 2?"}
    D -->|Sim| E["Tarefa Concluída com Baixo Custo!"]
    D -->|Não (Bug Complexo)| F["Escalação: Tier 3 (Raciocínio Profundo)"]
    F -->|Plano de Correção Resolvido| C
```

## 4. Técnica

### Configuração Declarativa da Matriz de Tiers (`.router/tiers.json`)

Salve o arquivo abaixo na pasta `.router/tiers.json` do seu projeto para formalizar os modelos ativos [1] [3]:

```json
{
  "tiers_matrix": {
    "tier_1_fast": {
      "primary": "gemini-2.0-flash",
      "fallback": "claude-3-5-haiku",
      "max_tokens_budget": 1000,
      "temperature": 0.1
    },
    "tier_2_standard": {
      "primary": "claude-3-7-sonnet",
      "fallback": "deepseek-chat",
      "max_tokens_budget": 4000,
      "temperature": 0.2
    },
    "tier_3_reasoning": {
      "primary": "claude-3-7-sonnet-thinking",
      "fallback": "o3-mini",
      "thinking_budget": 8000,
      "temperature": 1.0
    }
  }
}
```

## 5. Aplica

### Estudo de Caso: Construindo um Sistema de Gestão com Custo Mínimo

Uma fábrica de software precisava refatorar um sistema legado de 100 módulos [1]:
- **Estratégia Monolítica (Sem Tiers)**: Enviou todos os módulos para o modelo de raciocínio pesado. Custo estimado: R$ 3.800,00 [1].
- **Estratégia dos 3 Tiers da Camada 3**:
  - O **Tier 1** leu os 100 módulos e gerou o catálogo de dependências em JSON por R$ 4,50 [1].
  - O **Tier 3** analisou apenas os 5 módulos centrais de banco de dados e desenhou o novo schema por R$ 22,00 [1].
  - O **Tier 2** reescreveu os 95 módulos restantes seguindo o schema aprovado por R$ 180,00 [1].
- **O Resultado**: O projeto foi entregue com qualidade máxima por R$ 206,50 — uma economia líquida superior a 94% [1].

### Exercício
- [ ] Crie o arquivo `.router/tiers.json` com os 3 tiers e insira os modelos que você possui configurados
- [ ] Classifique 5 tarefas reais entre Tier 1, Tier 2 e Tier 3 e justifique cada escolha
- [ ] Simule a Regra de Escalação: force uma falha dupla no Tier 2 e observe a escalação automática para o Tier 3
- [ ] Estime o custo de um projeto seu usando a estratégia monolítica vs a estratégia dos 3 Tiers

## 6. Fixa

### Exercício Prático 1: O Exercício da Escalação
Se um agente está tentando conectar um banco de dados e recebe um erro de senha incorreta, essa tarefa exige escalação para o Tier 3 de raciocínio pesado? Justifique sua resposta.

### Exercício Prático 2: Configurando seus Provedores
Abra o arquivo `.router/tiers.json` e insira as chaves dos modelos que você possui configurados na sua máquina.

## 7. Conclusão

**Os 3 pontos que você dominou neste capítulo:**
1. A Matriz de 3 Tiers divide os modelos em Rápido & Econômico (Tier 1), Desenvolvimento Equilibrado (Tier 2) e Raciocínio Pesado (Tier 3), cada um com custo e uso específicos.
2. As Regras de Transição — Default Econômico, Escalação Condicional e Desescalada Imediata — garantem que cada tarefa use o modelo proporcional à sua complexidade.
3. A configuração declarativa em `.router/tiers.json` formaliza os modelos ativos e seus fallbacks, permitindo alternância cirúrgica.

**Desafio final:** Configure a sua Matriz de Tiers e rode um projeto real com a estratégia dos 3 Tiers. Compare o custo com a abordagem monolítica; se a economia não for superior a 90%, revise a classificação das tarefas.

**No próximo capítulo**, você vai dominar a Camada 4 — a Central de Comando que integra as três camadas anteriores em um painel único de soberania.

## 8. Referências Bibliográficas

[1] PROJETO ARSENAL. *A Matriz de 3 Tiers de Modelos e Otimização de Pareto*. São Paulo: Fábrica Agêntica, 2026.

[2] ANTHROPIC. *Model Comparison, Latency and Pricing Matrix*. São Francisco: Anthropic Developer Guides, 2024.

[3] DEEPSEEK AI. *DeepSeek-V3 and DeepSeek-R1 Architecture Report*. Pequim: DeepSeek, 2025.

[4] GOOGLE. *Gemini 2.0 Flash and Thinking Models Overview*. Mountain View: Google DeepMind, 2024.

[5] OPENAI. *OpenAI o1 and o3 Series System Card*. São Francisco: OpenAI, 2024.
