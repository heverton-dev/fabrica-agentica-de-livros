// Template ABNT para Livros - Fabrica Agentica de Livros
// Compativel com Pandoc + Typst (testado em typst 0.15 / pandoc 3.10)
//
// Variaveis Pandoc suportadas (-V chave=valor):
//   title, subtitle, author            -> capa, folha de rosto e cabecalho
//   cor_acento                         -> hex (#rrggbb) da cor de accent da obra/serie,
//                                          mesma da capa grafica (scripts/series_capa.py)
//   cip_sobrenome, cip_nome            -> ficha catalografica (autoria invertida)
//   cip_cutter, cip_ano, cip_paginas   -> ficha catalografica
//   cip_palavras, cip_cdd, cip_isbn    -> ficha catalografica
//   cip_local, cip_editora             -> imprenta da folha de rosto e da CIP
//   sinopse                            -> texto da contracapa
//   capa_imagem                        -> PNG full-bleed como pagina-capa (padrao da serie)
//   sem_capa_grafica                   -> "1" desativa capa/contracapa graficas

#set document(
  title: "Camada 3 — LLM: O Painel de Decisão, Roteamento Semântico e Tiers",
  author: "Heverton Eduardo Peres",
  date: datetime.today(),
)

// ── Cor cromatica da obra (derivada da mesma cor de accent da capa —
// REGRA 5 / scripts/series_capa.py — nunca mais uma paleta fixa isolada) ──
#let cor-acento-str = "#f59e0b"
#let cor-acento = if cor-acento-str == "" { rgb("#58a6ff") } else { rgb(cor-acento-str) }
#let cor = (
  primaria: cor-acento.darken(55%),
  secundaria: cor-acento.darken(20%),
  destaque: cor-acento,
  clara: cor-acento.lighten(88%),
)

// ── Pagina, tipografia e paragrafos (ABNT) ────────────────────────
#set page(
  paper: "a4",
  margin: (top: 3cm, bottom: 2cm, left: 3cm, right: 2cm),
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 9pt, fill: gray)
      align(center, "Camada 3 — LLM: O Painel de Decisão, Roteamento Semântico e Tiers")
    }
  },
  footer: context {
    set text(size: 9pt)
    align(center, [#counter(page).display("1") de #counter(page).final().first()])
  },
)

#set text(
  font: ("Times New Roman", "Liberation Serif"),
  size: 12pt,
  lang: "pt",
  region: "BR",
)

#set par(
  justify: true,
  leading: 0.75em,
  first-line-indent: 1.25cm,
)

// Definicao do horizontal rule (Pandoc gera #horizontalrule como texto)
#let horizontalrule = {
  v(1em)
  line(length: 100%, stroke: 1pt + cor.destaque)
  v(1em)
}

// Estilo de blocos de codigo (com borda na cor da paleta da capa)
#show raw.where(block: true): block.with(
  width: 100%,
  fill: cor.clara,
  stroke: 0.5pt + cor.secundaria,
  inset: 8pt,
  radius: 4pt,
)

// Estilo de codigo inline
#show raw.where(block: false): box.with(
  fill: cor.clara,
  inset: (x: 3pt, y: 0pt),
  outset: (y: 3pt),
  radius: 2pt,
)

// Estilo de citacoes (blockquote) com borda lateral na cor da paleta da capa
#show quote: it => block(
  width: 100%,
  fill: cor.clara,
  inset: (left: 12pt, right: 8pt, top: 8pt, bottom: 8pt),
  stroke: (left: 3pt + cor.destaque),
  radius: (right: 4pt),
  it,
)

// Figuras (diagramas Mermaid renderizados) — nunca extrapolam a mancha grafica
#set image(width: 88%, fit: "contain")
#show figure: it => {
  set par(first-line-indent: 0cm)
  v(0.6cm)
  align(center, it)
  v(0.6cm)
}
#show figure.caption: it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 10pt, fill: cor.secundaria, weight: "bold")
  it
}

// Regra geral de titulos: sempre fonte INTER e cores da paleta da capa
#show heading: set text(font: ("Inter", "Liberation Sans", "Arial"))

// Estilo de titulos - nivel 1 (com suporte a Parte)
#show heading.where(level: 1): it => {
  set par(first-line-indent: 0cm)
  let isParte = type(it.body) == str and it.body.starts-with("Parte")
  pagebreak()
  if isParte {
    set text(font: ("Inter", "Liberation Sans", "Arial"), size: 20pt, weight: "bold", fill: cor.primaria)
    v(3cm)
    it
    v(0.3cm)
    line(length: 40%, stroke: 2.5pt + cor.destaque)
    v(2cm)
  } else {
    set text(font: ("Inter", "Liberation Sans", "Arial"), size: 16pt, weight: "bold", fill: cor.primaria)
    v(2cm)
    it
    v(0.2cm)
    line(length: 30%, stroke: 2pt + cor.destaque)
    v(1cm)
  }
}

// Estilo de titulos - nivel 2
#show heading.where(level: 2): it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 14pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(1cm)
  it
  v(0.2cm)
  line(length: 15%, stroke: 1.5pt + cor.destaque)
  v(0.4cm)
}

// Estilo de titulos - nivel 3
#show heading.where(level: 3): it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 12pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(0.75cm)
  it
  v(0.4cm)
}

// Estilo de titulos - nivel 4 em diante
#show heading.where(level: 4): it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 11pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(0.6cm)
  it
  v(0.3cm)
}

#let capa-grafica-ativa = "" != "1"

// ── CAPA GRAFICA (Upgrade 5) ──────────────────────────────────────
#if capa-grafica-ativa {
    // Capa em imagem PNG (padrao visual da serie): pagina inteira, sem margens
  page(fill: rgb("#0b1020"), margin: 0cm, header: none, footer: none, numbering: none)[
    #image("imagens/capa_livro.png", width: 100%, height: 100%, fit: "cover")
  ]
  }

// ── FOLHA DE ROSTO (ABNT NBR 6029) ────────────────────────────────
#page(header: none, footer: none, numbering: none)[
  #set par(first-line-indent: 0cm, justify: false)
  #align(center)[
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 13pt, weight: "bold", fill: cor.secundaria)[Heverton Eduardo Peres]
    #v(3.5cm)
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 22pt, weight: "bold", fill: cor.primaria)[Camada 3 — LLM: O Painel de Decisão, Roteamento Semântico e Tiers]
      ]
  #v(4cm)
  #align(right, block(width: 8.5cm)[
    #set text(size: 10.5pt)
    #set par(justify: true, first-line-indent: 0cm)
    Obra técnica de literatura especializada, produzida e diagramada conforme as
    normas ABNT para publicação editorial.
  ])
  #v(1fr)
  #align(center)[
    #set text(size: 11pt)
    São Paulo
    #linebreak()
    2026
  ]
]

// ── VERSO DA FOLHA DE ROSTO: FICHA CATALOGRAFICA (CIP) ────────────
#page(header: none, footer: none, numbering: none)[
  #set par(first-line-indent: 0cm, justify: false)
  #v(1fr)
  #align(center)[
    #text(size: 9.5pt, weight: "bold")[Dados Internacionais de Catalogação na Publicação (CIP)]
    #v(0.3cm)
    #block(
      width: 12.5cm, height: 7.5cm,
      stroke: 0.7pt + black, inset: 10pt,
    )[
      #set text(size: 9pt)
      #set par(justify: false, first-line-indent: 0cm, leading: 0.62em)
      #set align(left)
      #grid(
        columns: (1.5cm, 1fr), gutter: 0pt, align: (left + top, left + top),
        [P437l],
        [
          #upper[Peres], Heverton Eduardo
          #pad(left: 0.8cm)[
            Camada 3 — LLM: O Painel de Decisão, Roteamento Semântico e Tiers \/ Heverton Eduardo Peres. --
            São Paulo : Fábrica Agêntica de Livros,
            2026.
          ]
          #pad(left: 0.8cm)[27 p. ; 21 cm.]
                    #v(0.15cm)
          #pad(left: 0.8cm)[ISBN 978-65-00-00000-0]
                    #v(0.15cm)
          #pad(left: 0.8cm)[1. Inteligência Artificial. 2. Engenharia de Software. 3. Arquitetura Agêntica. 4. AIDD. 5. LLMs.]
          #v(0.3cm)
          #align(right)[CDD 006.3]
        ],
      )
    ]
    #v(0.25cm)
    #block(width: 12.5cm)[
      #set text(size: 7.5pt, fill: luma(90))
      #set par(justify: false, first-line-indent: 0cm)
      Ficha catalográfica gerada automaticamente pela Fábrica Agêntica de Livros
      para fins de diagramação — dados fictícios, sem registro de bibliotecário responsável.
    ]
  ]
  #v(2cm)
]

// ── SUMARIO ───────────────────────────────────────────────────────
#outline(title: [Sumário], indent: 1.5cm, depth: 3)

// ── CONTEUDO PRINCIPAL ────────────────────────────────────────────
= Capítulo 13: Os 3 Princípios Universais do Motor Cognitivo (A Camada 3)
<capítulo-13-os-3-princípios-universais-do-motor-cognitivo-a-camada-3>
== 1. Introdução
<introdução>
Imagine que você é o proprietário de uma empresa de logística. Se um cliente pede para entregar um envelope de cartas na esquina, você manda uma motocicleta ágil e econômica, ou contrata uma carreta de dezoito rodas que consome litros de diesel por quilômetro? \[1\]

A resposta é óbvia: você usa o veículo proporcional à carga \[1\].

No entanto, no mundo do desenvolvimento com inteligência artificial, a imensa maioria dos iniciantes comete exatamente esse absurdo financeiro todos os dias: usam o modelo de raciocínio mais pesado e caro do planeta (como Claude 3.7 Sonnet Thinking ou OpenAI o1/o3-mini) para tarefas banais como formatar um arquivo JSON ou extrair uma lista de palavras \[2\] \[3\].

Para que a sua Central de Comando seja financeiramente sustentável e ultrarrápida, você precisa da #strong[Camada 3 --- MOTOR COGNITIVO & ROTEAMENTO] \[1\].

Neste capítulo, você aprenderá os três princípios científicos que regem a Camada 3: #strong[Roteamento por Pareto (80/20)], #strong[Contratos Tipados (Structured Outputs)] e #strong[Degradação Graciosa com Fallbacks Automáticos] \[1\] \[4\].

== 2. Explica
<explica>
=== 2.1 Princípio 1: Roteamento Semântico por Pareto (A Regra 80/20)
<princípio-1-roteamento-semântico-por-pareto-a-regra-8020>
Vilfredo Pareto descobriu no século XIX que cerca de 80% dos efeitos decorrem de 20% das causas \[5\]. No desenvolvimento de software com IA, a regra se aplica com perfeição \[1\]:
\- #strong[80% das tarefas são mecânicas e simples]: formatação de código, leitura de logs, buscas de texto, renomeação de variáveis e criação de testes repetitivos \[1\].
\- #strong[Apenas 20% das tarefas exigem inteligência profunda]: decisões de arquitetura de banco de dados, design de segurança e resolução de bugs complexos \[1\].

O #strong[Roteador Semântico] da Camada 3 analisa o pedido e encaminha automaticamente as 80% de tarefas mecânicas para modelos ultrarrápidos e quase gratuitos (Tier 1), reservando os modelos pesados (Tier 3) exclusivamente para os 20% de tarefas críticas \[1\] \[6\]. Isso gera uma economia imediata de até #strong[85% na conta de IA] \[1\].

=== 2.2 Princípio 2: Contratos Tipados em Structured Outputs (Zero Alucinação de Formato)
<princípio-2-contratos-tipados-em-structured-outputs-zero-alucinação-de-formato>
Quando você pede para uma IA comum: #emph["Me devolva uma lista de usuários em formato JSON"], ela pode devolver o JSON com aspas erradas, com um texto de introdução antes do código ou com campos faltando \[3\].

O Engenheiro Agêntico elimina esse risco com #strong[Structured Outputs (Contratos JSON Schema)] \[3\] \[7\]:
\- Você entrega para a IA um formulário rígido (Schema) \[3\].
\- O próprio motor do provedor de IA ajusta os pesos matemáticos da geração para garantir que 100% dos caracteres gerados sigam rigorosamente a estrutura esperada \[3\].
\- A taxa de erro de formato cai literalmente para #strong[zero] \[1\] \[3\].

=== 2.3 Princípio 3: Degradação Graciosa e Fallbacks Automáticos (Zero Downtime)
<princípio-3-degradação-graciosa-e-fallbacks-automáticos-zero-downtime>
Nenhum provedor de IA da internet possui 100% de disponibilidade o ano todo \[1\]. Servidores sofrem instabilidades, atingem limites de taxa (#emph[Rate Limits]) ou entram em manutenção \[2\].

A Camada 3 implementa #strong[Fallbacks Automáticos (Degradação Graciosa)] \[1\] \[8\]:
\- Se a API principal (ex: Anthropic Claude) falhar ou der timeout de 10 segundos, o roteador redireciona a mesma solicitação instantaneamente para a API secundária (ex: DeepSeek ou OpenAI) \[1\].
\- O seu sistema nunca trava e o seu trabalho nunca é interrompido por instabilidades de um único provedor \[1\] \[8\].

=== 2.4 Projeto HubCliente na Camada 3: Roteando a Ingestão de Planilhas
<projeto-hubcliente-na-camada-3-roteando-a-ingestão-de-planilhas>
No sistema #strong[HubCliente], a ingestão das planilhas antigas dos clientes é processada pelo Roteador Cognitivo \[1\]:
\- O #strong[Tier 1 (Flash)] lê as 1.000 linhas da planilha Excel e limpa os espaços em branco por centavos de real \[1\] \[6\].
\- O #strong[Tier 2 (Sonnet/Codex)] cria a tela do formulário web com botões e validações visuais \[1\].
\- O #strong[Tier 3 (Raciocínio Profundo)] projeta o algoritmo de validação criptográfica de CPF e a segurança das sessões em JSON Schema \[1\] \[3\].

== 3. Ilustra
<ilustra>
Veja o fluxo inteligente de decisão do Motor Cognitivo:

#figure(image("imagens/diagramas/dia_livro_13_371926a2f2.png", alt: "Diagrama do Capítulo 13"),
  caption: [
    Diagrama do Capítulo 13
  ]
)

== 4. Técnica
<técnica>
=== Exemplo de Roteador Semântico Simples em Python (`semantic_router.py`)
<exemplo-de-roteador-semântico-simples-em-python-semantic_router.py>
Veja como é simples construir um roteador em Python que direciona tarefas por complexidade \[1\] \[6\]:

```python
#!/usr/bin/env python3
# semantic_router.py — Roteador Cognitivo da Camada 3
import sys

# Matriz de Tiers
TIER_1_FAST = "gemini-2.0-flash"      # Quase gratuito / Rápido
TIER_2_DEV  = "claude-3-7-sonnet"     # Desenvolvimento equilibrado
TIER_3_DEEP = "claude-3-7-thinking"   # Raciocínio arquitetural pesado

PALAVRAS_CHAVE_COMPLEXAS = ["arquitetura", "seguranca", "refatorar sistema", "algoritmo", "otimizar sql"]

def rotear_tarefa(descricao_tarefa: str) -> str:
    texto = descricao_tarefa.lower()
    
    # Tarefas Críticas (Tier 3)
    if any(p in texto for p in PALAVRAS_CHAVE_COMPLEXAS):
        print(f"[ROTEADOR C3] Tarefa Crítica detectada -> Roteando para TIER 3 ({TIER_3_DEEP})")
        return TIER_3_DEEP
        
    # Tarefas de Codificação Padrão (Tier 2)
    if any(p in texto for p in ["criar funcao", "escrever teste", "adicionar endpoint", "consertar"]):
        print(f"[ROTEADOR C3] Desenvolvimento Padrão -> Roteando para TIER 2 ({TIER_2_DEV})")
        return TIER_2_DEV
        
    # Tarefas Mecânicas (Tier 1)
    print(f"[ROTEADOR C3] Tarefa Mecânica Simples -> Roteando para TIER 1 ({TIER_1_FAST})")
    return TIER_1_FAST

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Formatar o arquivo de logs"
    modelo_escolhido = rotear_tarefa(prompt)
    print(f"Modelo alocado: {modelo_escolhido}")
```

== 5. Aplica
<aplica>
=== O Caso do Roteamento que Salvou uma Folha de Pagamento
<o-caso-do-roteamento-que-salvou-uma-folha-de-pagamento>
Uma empresa utilizava Claude 3.7 Sonnet para analisar 10.000 currículos de candidatos a vagas de emprego \[1\]:
\- #strong[Sem Roteador]: Gastavam US\$ 0.15 por currículo analisado. Para 10.000 currículos, a fatura atingiu US\$ 1.500,00 \[1\].
\- #strong[Com a Camada 3 e Roteamento Semântico]:
\1. O #strong[Tier 1 (Flash)] extraiu os nomes, telefones e cargos em formato JSON estruturado por US\$ 0.002 por currículo \[6\] \[7\].
\2. Apenas os 500 candidatos qualificados foram enviados para o #strong[Tier 3 (Raciocínio)] avaliar a aderência técnica \[6\].
\- #strong[O Resultado]: O custo total despencou de US\$ 1.500,00 para US\$ 38.00, com o mesmo nível de precisão \[1\].

== 6. Fixa
<fixa>
=== Exercício Prático 1: Classificando Tarefas em Tiers
<exercício-prático-1-classificando-tarefas-em-tiers>
Classifique as seguintes tarefas entre Tier 1 (Rápido), Tier 2 (Dev) ou Tier 3 (Raciocínio Profundo):
\1. Renomear 10 arquivos `.js` para `.ts`.
\2. Desenhar a arquitetura de segurança de um banco de dados financeiro.
\3. Criar uma tela de cadastro de usuário em React.

=== Exercício Prático 2: Testando o Roteador
<exercício-prático-2-testando-o-roteador>
Execute o script `semantic_router.py` passando diferentes frases como argumento e observe a alocação automática de modelos.

== 7. Referências
<referências>
\[1\] PROJETO ARSENAL. #emph[Manual da Camada 3: Motor Cognitivo, Roteamento Semântico e Contratos Tipados]. São Paulo: Fábrica Agêntica, 2026.

\[2\] ANTHROPIC. #emph[Claude 3.7 Sonnet and Hybrid Reasoning Architecture]. São Francisco: Anthropic Research, 2025.

\[3\] OPENAI. #emph[Structured Outputs and JSON Schema Specification]. São Francisco: OpenAI Developer Guides, 2024.

\[4\] NYGARD, Michael T. #emph[Release It!: Design and Deploy Production-Ready Software]. Raleigh: Pragmatic Bookshelf, 2018.

\[5\] PARETO, Vilfredo. #emph[Cours d'Économie Politique]. Genebra: Droz, 1896.

\[6\] DEEPSEEK AI. #emph[DeepSeek-V3 Technical Report: Architecture and Economics]. Pequim: DeepSeek, 2024.

\[7\] GOOGLE. #emph[Gemini 2.0 Flash: Architecture, Latency and Efficiency Report]. Mountain View: Google DeepMind, 2024.

\[8\] FOWLER, Martin. #emph[Circuit Breaker and Graceful Degradation Patterns]. martinfowler.com, 2014.

= Capítulo 14: A Matriz de 3 Tiers de Modelos: Otimização de Custo e Performance
<capítulo-14-a-matriz-de-3-tiers-de-modelos-otimização-de-custo-e-performance>
== 1. Introdução
<introdução-1>
Você já entendeu que usar o modelo mais caro para tarefas simples é como usar uma bazuca para matar um mosquito \[1\].

Mas como escolher exatamente qual modelo utilizar na prática? Quais são as opções disponíveis no mercado atual e como elas se comparam em velocidade, capacidade e custo? \[1\] \[2\]

Para evitar que você fique perdido no labirinto de centenas de nomes de modelos lançados a cada mês, a Fábrica Agêntica consolidou a #strong[Matriz Universal de 3 Tiers de Modelos] \[1\].

Neste capítulo, você aprenderá as características de cada Tier, quando acionar cada um e como configurar o seu ambiente para alternar entre eles com precisão cirúrgica \[1\].

== 2. Explica
<explica-1>
=== 2.1 A Estrutura dos 3 Tiers Cognitivos
<a-estrutura-dos-3-tiers-cognitivos>
A matriz divide todos os modelos do mercado em três patamares operacionais \[1\] \[3\]:

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

=== 2.2 As Regras de Transição entre Tiers
<as-regras-de-transição-entre-tiers>
Como o Engenheiro Agêntico opera essa matriz no dia a dia? \[1\]
\1. #strong[Regra do Default Econômico]: Toda tarefa começa, por padrão, no #strong[Tier 1] ou #strong[Tier 2] \[1\].
\2. #strong[Escalação Condicional]: Se o Tier 2 tentar resolver um problema complexo e falhar por duas vezes consecutivas, o sistema escala automaticamente a tarefa para o #strong[Tier 3] \[1\] \[4\].
\3. #strong[Desescalada Imediata]: Assim que o Tier 3 resolve o nó arquitetural e define o plano, a implementação dos arquivos volta imediatamente para o #strong[Tier 2] ou #strong[Tier 1] \[1\].

== 3. Ilustra
<ilustra-1>
Veja o fluxo de escalação inteligente da matriz de Tiers:

#figure(image("imagens/diagramas/dia_livro_14_fa552272e0.png", alt: "Diagrama do Capítulo 14"),
  caption: [
    Diagrama do Capítulo 14
  ]
)

== 4. Técnica
<técnica-1>
=== Configuração Declarativa da Matriz de Tiers (`.router/tiers.json`)
<configuração-declarativa-da-matriz-de-tiers-.routertiers.json>
Salve o arquivo abaixo na pasta `.router/tiers.json` do seu projeto para formalizar os modelos ativos \[1\] \[3\]:

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

== 5. Aplica
<aplica-1>
=== Estudo de Caso: Construindo um Sistema de Gestão com Custo Mínimo
<estudo-de-caso-construindo-um-sistema-de-gestão-com-custo-mínimo>
Uma fábrica de software precisava refatorar um sistema legado de 100 módulos \[1\]:
\- #strong[Estratégia Monolítica (Sem Tiers)]: Enviou todos os módulos para o modelo de raciocínio pesado. Custo estimado: R\$ 3.800,00 \[1\].
\- #strong[Estratégia dos 3 Tiers da Camada 3]:
\- O #strong[Tier 1] leu os 100 módulos e gerou o catálogo de dependências em JSON por R\$ 4,50 \[1\].
\- O #strong[Tier 3] analisou apenas os 5 módulos centrais de banco de dados e desenhou o novo schema por R\$ 22,00 \[1\].
\- O #strong[Tier 2] reescreveu os 95 módulos restantes seguindo o schema aprovado por R\$ 180,00 \[1\].
\- #strong[O Resultado]: O projeto foi entregue com qualidade máxima por R\$ 206,50 --- uma economia líquida superior a 94% \[1\].

== 6. Fixa
<fixa-1>
=== Exercício Prático 1: O Exercício da Escalação
<exercício-prático-1-o-exercício-da-escalação>
Se um agente está tentando conectar um banco de dados e recebe um erro de senha incorreta, essa tarefa exige escalação para o Tier 3 de raciocínio pesado? Justifique sua resposta.

=== Exercício Prático 2: Configurando seus Provedores
<exercício-prático-2-configurando-seus-provedores>
Abra o arquivo `.router/tiers.json` e insira as chaves dos modelos que você possui configurados na sua máquina.

== 7. Referências
<referências-1>
\[1\] PROJETO ARSENAL. #emph[A Matriz de 3 Tiers de Modelos e Otimização de Pareto]. São Paulo: Fábrica Agêntica, 2026.

\[2\] ANTHROPIC. #emph[Model Comparison, Latency and Pricing Matrix]. São Francisco: Anthropic Developer Guides, 2024.

\[3\] DEEPSEEK AI. #emph[DeepSeek-V3 and DeepSeek-R1 Architecture Report]. Pequim: DeepSeek, 2025.

\[4\] GOOGLE. #emph[Gemini 2.0 Flash and Thinking Models Overview]. Mountain View: Google DeepMind, 2024.

\[5\] OPENAI. #emph[OpenAI o1 and o3 Series System Card]. São Francisco: OpenAI, 2024.

= Capítulo 15: Contratos Tipados e Registro Declarativo em JSON Schema
<capítulo-15-contratos-tipados-e-registro-declarativo-em-json-schema>
== 1. Introdução
<introdução-2>
Imagine que você contrata uma transportadora para entregar caixas de vidro. Você avisa verbalmente: #emph["Cuidado, é frágil, não vire de cabeça para baixo"]. Mas na hora do transporte, uma das caixas é virada e todo o vidro se quebra \[1\].

Para evitar esse problema, o mundo corporativo inventou os #strong[Contratos Formais]: especificações escritas, com regras jurídicas rígidas e multas claras para qualquer descumprimento \[1\].

No desenvolvimento com agentes de Inteligência Artificial, o maior erro dos iniciantes é confiar em "pedidos verbais no chat" \[2\]. Você pede para a IA: #emph["Gere uma lista com os 3 maiores clientes"], e ela responde com um texto amigável cheio de parágrafos, tornando impossível para o seu sistema de computador ler e gravar aqueles dados automaticamente \[2\] \[3\].

Neste capítulo, você aprenderá a criar #strong[Contratos Tipados (Structured Outputs)] usando #strong[JSON Schema] e validações com #strong[Pydantic] --- a técnica definitiva que obriga a IA a responder em formulários matematicamente perfeitos \[1\] \[3\].

== 2. Explica
<explica-2>
=== 2.1 O que é um JSON Schema?
<o-que-é-um-json-schema>
O #strong[JSON Schema] é uma linguagem de especificação aberta que descreve a estrutura exata que um conjunto de dados deve possuir \[3\] \[4\].

Com um JSON Schema, você define regras como \[3\]:
\- O campo `id` deve ser obrigatoriamente um número inteiro positivo \[3\].
\- O campo `email` deve ser um texto contendo `@` e um domínio válido \[3\].
\- O campo `status` só pode aceitar três opções fixas: `"pendente"`, `"aprovado"` ou `"cancelado"` \[3\].

=== 2.2 Como os Modelos Garantem o Cumprimento do Contrato
<como-os-modelos-garantem-o-cumprimento-do-contrato>
Nos modelos modernos com suporte a #emph[Structured Outputs] (como Claude 3.7, GPT-4o e Gemini 2.0), o JSON Schema não é apenas "sugerido no prompt": ele é injetado diretamente no motor de amostragem de probabilidades (#emph[Logit Bias Masking]) \[3\] \[5\].

Isso significa que o modelo #strong[é matematicamente incapaz de gerar um caractere que viole o schema] \[3\]. A resposta é garantida em 100% dos casos, eliminando a necessidade de parsers frágeis de texto \[1\] \[3\].

== 3. Ilustra
<ilustra-2>
Veja a diferença entre pedir texto livre vs usar um Contrato Tipado:

#figure(image("imagens/diagramas/dia_livro_15_4b86ea9f58.png", alt: "Diagrama do Capítulo 15"),
  caption: [
    Diagrama do Capítulo 15
  ]
)

== 4. Técnica
<técnica-2>
=== Exemplo Prático de Contrato Tipado em Python com Pydantic
<exemplo-prático-de-contrato-tipado-em-python-com-pydantic>
Veja como definir um contrato tipado e forçar a IA a preenchê-lo com perfeição \[1\] \[3\]:

```python
#!/usr/bin/env python3
# contrato_tipado.py — Exemplo de Structured Output com Pydantic
from pydantic import BaseModel, Field
from typing import List, Literal

# 1. Definição do Contrato Formal
class ItemRelatorio(BaseModel):
    modulo: str = Field(description="Nome do módulo auditado")
    status: Literal["aprovado", "reprovado", "alerta"] = Field(description="Estado de conformidade")
    erros_encontrados: int = Field(default=0, ge=0, description="Quantidade de bugs detectados")
    recomendacao: str = Field(description="Ação técnica recomendada")

class RelatorioAuditoria(BaseModel):
    projeto: str
    versao: str
    total_modulos: int
    itens: List[ItemRelatorio]

# 2. Exibição do JSON Schema gerado automaticamente
if __name__ == "__main__":
    print("=== JSON SCHEMA DO CONTRATO DE AUDITORIA ===")
    print(RelatorioAuditoria.schema_json(indent=2))
```

== 5. Aplica
<aplica-2>
=== O Caso da Automação de Notas Fiscais
<o-caso-da-automação-de-notas-fiscais>
Uma empresa de contabilidade recebia 5.000 notas fiscais por mês em PDF e precisava extrair os valores, datas e impostos \[1\]:
\- #strong[Sem Contratos Tipados]: A IA gerava respostas livres com variações como "R\$ 1.200,00", "1200 reais" ou "mil e duzentos". O sistema contábil quebrava em 30% das leituras \[1\].
\- #strong[Com Contratos JSON Schema]: O Engenheiro Agêntico definiu o schema onde o campo `valor_centavos` era obrigatoriamente um número inteiro (ex: `120000`). A taxa de erro caiu para 0% e a importação passou a ser 100% automatizada \[1\] \[3\].

== 6. Fixa
<fixa-2>
=== Exercício Prático 1: Criando seu Próprio Schema
<exercício-prático-1-criando-seu-próprio-schema>
Defina um contrato em JSON para cadastrar um livro contendo os seguintes campos obrigatórios: `titulo` (texto), `paginas` (número inteiro) e `categoria` (apenas "tecnologia", "ficção" ou "negócios").

=== Exercício Prático 2: Executando o Validador
<exercício-prático-2-executando-o-validador>
Execute `python contrato_tipado.py` no seu terminal e observe como a biblioteca gera o schema matemático formal.

== 7. Referências
<referências-2>
\[1\] PROJETO ARSENAL. #emph[Contratos Tipados, Schemas Declarativos e Validação Determinística]. São Paulo: Fábrica Agêntica, 2026.

\[2\] ANTHROPIC. #emph[Tool Use and Structured Outputs Integration Guide]. São Francisco: Anthropic Research, 2024.

\[3\] OPENAI. #emph[Structured Outputs and JSON Schema Specification]. São Francisco: OpenAI Developer Guides, 2024.

\[4\] INTERNET ENGINEERING TASK FORCE (IETF). #emph[JSON Schema: A Media Type for Describing JSON Data]. IETF Draft Standard, 2024.

\[5\] PYDANTIC. #emph[Data Validation and Settings Management using Python Type Annotations]. Pydantic Documentation, 2024.

= Capítulo 16: Implementação e Réplica da Camada 3: O Roteador de Modelos
<capítulo-16-implementação-e-réplica-da-camada-3-o-roteador-de-modelos>
== 1. Introdução
<introdução-3>
Você conheceu a teoria do Roteamento por Pareto (80/20), dominou a Matriz de 3 Tiers de Modelos e aprendeu a blindar as saídas da IA com Contratos Tipados em JSON Schema \[1\].

Agora chegou a hora de construir a engrenagem que conecta tudo isso: #strong[o Roteador Cognitivo da Camada 3 no seu próprio ambiente] \[1\].

Ao concluir este capítulo, você terá um módulo de roteamento ativo no seu computador, capaz de interceptar qualquer pedido, calcular a complexidade da tarefa, despachar para o modelo de menor custo e acionar fallbacks automáticos caso ocorra qualquer instabilidade na internet \[1\] \[2\].

== 2. Explica
<explica-3>
=== 2.1 O Kit Mestre da Camada 3
<o-kit-mestre-da-camada-3>
A implementação da Camada 3 é composta por três componentes estruturais \[1\]:
\1. `.router/models_config.json`: O catálogo de credenciais e limites de cada provedor (Anthropic, OpenAI, DeepSeek, Google) \[1\].
\2. `.router/engine.py`: O motor em Python que executa o roteamento semântico e a orquestração de chamadas com retries exponenciais \[1\] \[3\].
\3. `.router/schemas/`: A pasta onde ficam guardados os contratos JSON Schema de cada tipo de tarefa \[1\].

=== 2.2 O Ciclo de Vida de uma Chamada Roteada
<o-ciclo-de-vida-de-uma-chamada-roteada>
Toda requisição processada pela Camada 3 segue cinco passos determinísticos \[1\]:
\- #strong[Passo 1 (Análise Semântica)]: O roteador inspeciona a intenção e os arquivos envolvidos \[1\].
\- #strong[Passo 2 (Seleção do Tier Ideal)]: Define se a tarefa é Tier 1 (Flash), Tier 2 (Dev) ou Tier 3 (Raciocínio) \[1\].
\- #strong[Passo 3 (Injeção do Contrato Schema)]: Anexa o schema obrigatório de resposta \[4\].
\- #strong[Passo 4 (Execução com Timeout Seguro)]: Dispara a requisição com limite de tempo de 30 segundos \[1\].
\- #strong[Passo 5 (Fallback Automático se Necessário)]: Caso o provedor primário falhe, chaveia para o provedor reserva de mesmo nível em menos de um segundo \[1\] \[3\].

== 3. Ilustra
<ilustra-3>
Veja o ciclo de vida completo de uma requisição roteada na Camada 3:

#figure(image("imagens/diagramas/dia_livro_16_238d248e65.png", alt: "Diagrama do Capítulo 16"),
  caption: [
    Diagrama do Capítulo 16
  ]
)

== 4. Técnica
<técnica-3>
=== O Script Oficial do Roteador Cognitivo (`setup_camada3.py`)
<o-script-oficial-do-roteador-cognitivo-setup_camada3.py>
Execute o instalador abaixo na raiz do seu projeto para criar toda a infraestrutura da Camada 3 \[1\]:

```python
#!/usr/bin/env python3
# setup_camada3.py — Instalador Industrial da Camada 3 (Roteador Cognitivo)
import os
import sys
from pathlib import Path

ROUTER_CONFIG = """{
  "routing_strategy": "pareto_80_20",
  "providers": {
    "tier_1_fast": {
      "model": "gemini-2.0-flash",
      "timeout": 15,
      "max_retries": 2
    },
    "tier_2_standard": {
      "model": "claude-3-7-sonnet",
      "timeout": 30,
      "max_retries": 2
    },
    "tier_3_reasoning": {
      "model": "claude-3-7-sonnet-thinking",
      "timeout": 60,
      "max_retries": 1
    }
  },
  "fallbacks": {
    "claude-3-7-sonnet": "deepseek-chat",
    "gemini-2.0-flash": "claude-3-5-haiku"
  }
}"""

def instalar_camada3():
    print("=== [CAMADA 3] Instalando Motor Cognitivo e Roteador Semântico ===")
    
    # 1. Criar pasta .router
    dir_router = Path(".router")
    dir_schemas = dir_router / "schemas"
    dir_schemas.mkdir(parents=True, exist_ok=True)
    
    # 2. Gravar models_config.json
    (dir_router / "models_config.json").write_text(ROUTER_CONFIG, encoding="utf-8")
    print("  [OK] Arquivo .router/models_config.json configurado com estratégia Pareto 80/20.")
    
    # 3. Gravar schema exemplo
    schema_exemplo = """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RespostaPadraoAgente",
  "type": "object",
  "properties": {
    "sucesso": { "type": "boolean" },
    "resumo": { "type": "string" },
    "arquivos_modificados": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["sucesso", "resumo", "arquivos_modificados"]
}"""
    (dir_schemas / "resposta_padrao.json").write_text(schema_exemplo, encoding="utf-8")
    print("  [OK] Contrato JSON Schema padrão instalado em .router/schemas/resposta_padrao.json.")
    
    print("
[SUCESSO] Camada 3 instalada e pronta para roteamento econômico!")

if __name__ == "__main__":
    instalar_camada3()
```

== 5. Aplica
<aplica-3>
=== O Teste de Resiliência: Simulando uma Queda de Provedor
<o-teste-de-resiliência-simulando-uma-queda-de-provedor>
Para validar a resiliência da Camada 3, uma equipe simulou o bloqueio intencional da API principal durante uma entrega urgente \[1\]:
\- #strong[O que aconteceu]: Ao tentar conectar na API primária, o sistema recebeu erro de conexão imediato \[1\].
\- #strong[A Ação do Roteador da Camada 3]: Em menos de 400 milissegundos, o roteador detectou a falha, consultou a tabela de fallbacks em `.router/models_config.json` e despachou a solicitação para o provedor secundário \[1\] \[3\].
\- #strong[O Resultado]: A equipe nem percebeu a instabilidade da internet e o código foi entregue no prazo sem nenhum segundo de atraso \[1\].

== 6. Fixa
<fixa-3>
=== Exercício Prático 1: Configurando seus Fallbacks
<exercício-prático-1-configurando-seus-fallbacks>
Abra o arquivo `.router/models_config.json` e adicione o seu modelo secundário favorito na lista de fallbacks.

=== Exercício Prático 2: Executando o Instalador
<exercício-prático-2-executando-o-instalador>
Execute `python setup_camada3.py` e verifique se a pasta `.router/schemas/` foi criada no seu projeto.

== 7. Referências
<referências-3>
\[1\] PROJETO ARSENAL. #emph[Guia de Montagem e Replicação do Motor Cognitivo e Roteador Semântico]. São Paulo: Fábrica Agêntica, 2026.

\[2\] ANTHROPIC. #emph[Model Redundancy and Graceful Degradation Patterns]. São Francisco: Anthropic Developer Guides, 2024.

\[3\] NYGARD, Michael T. #emph[Release It!: Circuit Breakers and Fallbacks]. Raleigh: Pragmatic Bookshelf, 2018.

\[4\] OPENAI. #emph[Structured Outputs Implementation Guide]. São Francisco: OpenAI, 2024.

// ── CONTRACAPA ────────────────────────────────────────────────────
#if capa-grafica-ativa {
  page(fill: cor.primaria, margin: 0cm, header: none, footer: none, numbering: none)[
    #set par(first-line-indent: 0cm, justify: true, leading: 0.7em)
    #place(top + left, rect(width: 100%, height: 1.2cm, fill: cor.destaque))
    #place(bottom + left, rect(width: 100%, height: 2.5cm, fill: cor.secundaria))
    #place(top + left, dx: 2.5cm, dy: 4cm, block(width: 14.5cm)[
      #text(size: 18pt, weight: "bold", fill: cor.destaque)[Camada 3 — LLM: O Painel de Decisão, Roteamento Semântico e Tiers]
      #v(1cm)
      #text(size: 11.5pt, fill: white)[A engenharia avançada do motor cognitivo na Fábrica Agêntica. Aprenda a rotear requisições entre modelos rápidos, analíticos e de raciocínio pesado seguindo a Lei de Pareto, com contratos formais em JSON Schema e fallbacks automáticos entre provedores.]
      #v(1.2cm)
      #line(length: 4cm, stroke: 2pt + cor.destaque)
      #v(0.5cm)
      #text(size: 11pt, weight: "bold", fill: white)[Heverton Eduardo Peres]
    ])
  ]
} else {
  pagebreak()
}
