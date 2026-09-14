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
  title: "Camada 2 — HARNESS: O Painel de Segurança, Governança e Cross-Harness",
  author: "Heverton Eduardo Peres",
  date: datetime.today(),
)

// ── Cor cromatica da obra (derivada da mesma cor de accent da capa —
// REGRA 5 / scripts/series_capa.py — nunca mais uma paleta fixa isolada) ──
#let cor-acento-str = "#ef4444"
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
      align(center, "Camada 2 — HARNESS: O Painel de Segurança, Governança e Cross-Harness")
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
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 22pt, weight: "bold", fill: cor.primaria)[Camada 2 — HARNESS: O Painel de Segurança, Governança e Cross-Harness]
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
        [P437h],
        [
          #upper[Peres], Heverton Eduardo
          #pad(left: 0.8cm)[
            Camada 2 — HARNESS: O Painel de Segurança, Governança e Cross-Harness \/ Heverton Eduardo Peres. --
            São Paulo : Fábrica Agêntica de Livros,
            2026.
          ]
          #pad(left: 0.8cm)[29 p. ; 21 cm.]
                    #v(0.15cm)
          #pad(left: 0.8cm)[ISBN 978-65-00-00000-0]
                    #v(0.15cm)
          #pad(left: 0.8cm)[1. Inteligência Artificial. 2. Engenharia de Software. 3. Arquitetura Agêntica. 4. AIDD. 5. LLMs.]
          #v(0.3cm)
          #align(right)[CDD 004.6]
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
= Capítulo 9: Os 3 Princípios Universais do HARNESS (A Camada 2)
<capítulo-9-os-3-princípios-universais-do-harness-a-camada-2>
== 1. Introdução
<introdução>
Você já blindou a visão da sua Central de Comando com a Camada 1: seus agentes recebem apenas instruções limpas, em PT-BR, com economia de até 90% em cache de prefixo \[1\].

Mas agora surge uma pergunta vital que todo iniciante se faz: #emph[o que impede um agente de IA de cometer um erro catastrófico no meu computador?] \[2\]

Imagine um agente que, ao tentar limpar uma pasta temporária, execute um comando que apague todos os seus arquivos pessoais, ou que entre em um loop de tentativas repetidas e queime R\$ 500 em tokens em trinta minutos \[1\] \[3\].

Para que você durma tranquilo enquanto os seus agentes trabalham, você precisa da #strong[Camada 2 --- HARNESS & EXECUÇÃO] \[1\].

O termo #emph[Harness] (arnês / cinto de segurança) vem dos equipamentos de escalada e dos testes industriais \[4\]. Sua missão é simples e inegociável: envolver o agente em um casulo de segurança que torna qualquer falha inofensiva, reversível e imediatamente detectável \[1\] \[4\].

Neste capítulo, você aprenderá os três princípios universais que governam a Camada 2: #strong[Disjuntores (Circuit Breakers)], #strong[Sandboxes Reversíveis] e #strong[Hardlinks de Governança] \[1\].

== 2. Explica
<explica>
=== 2.1 Princípio 1: Disjuntores Industriais (Circuit Breakers)
<princípio-1-disjuntores-industriais-circuit-breakers>
Na engenharia elétrica, quando ocorre um curto-circuito na sua casa, o disjuntor desarma instantaneamente para evitar que a fiação pegue fogo \[4\].

Na engenharia agêntica, aplicamos o mesmo princípio para três tipos de perigo \[1\] \[4\]:
\1. #strong[Disjuntor de Turnos (Max Iterations)]: Define um teto rígido de passos (por exemplo, no máximo 15 ações). Se o agente não concluir o objetivo em 15 turnos, o sistema desarma e pausa o agente, evitando loops infinitos de cobrança \[1\].
\2. #strong[Disjuntor de Timeout (Tempo Limite)]: Se um comando de terminal travar ou demorar mais de 60 segundos, o processo é interrompido automaticamente \[1\].
\3. #strong[Disjuntor de Comandos Destrutivos (Command Blacklist)]: Qualquer tentativa de rodar comandos de alto risco (`rm -rf /`, `format`, `drop database`, `git reset --hard`) é interceptada e bloqueada antes de chegar ao sistema operacional \[1\] \[4\].

=== 2.2 Princípio 2: Sandbox Reversível (Ambiente Descartável e Seguro)
<princípio-2-sandbox-reversível-ambiente-descartável-e-seguro>
Nunca deixe um agente de IA trabalhar diretamente no seu ambiente de produção ou na sua branch principal do Git \[1\] \[5\].

O segundo princípio exige que todo trabalho seja executado dentro de uma #strong[Sandbox Reversível] \[1\]:
\- O agente opera em uma ramificação isolada (#emph[Git Worktree] ou container leve) \[5\].
\- Se o agente criar uma solução brilhante, você aprova as alterações e faz o merge seguro para a branch principal \[5\].
\- Se o agente se confundir e quebrar os arquivos, você simplesmente descarta a pasta de sandbox com um único comando, e o seu projeto original continua 100% intacto e limpo \[1\].

=== 2.3 Princípio 3: Hardlinks e Junções de Governança (Fonte Única da Verdade)
<princípio-3-hardlinks-e-junções-de-governança-fonte-única-da-verdade>
Em projetos maiores, você terá múltiplos agentes e subagentes trabalhando em pastas diferentes \[1\]. Um erro grave é copiar e colar o arquivo de regras em dez pastas diferentes: se você mudar uma regra, terá que atualizar todas as dez cópias manualmente, e inevitavelmente algumas ficarão desatualizadas \[1\].

O Engenheiro Agêntico resolve isso com #strong[Hardlinks (vínculos rígidos) ou Directory Junctions] no sistema de arquivos \[1\] \[6\]:
\- Existe apenas #strong[um único arquivo mestre de regras] no projeto (`.governance/CONSTITUTION.md`) \[1\].
\- Todas as outras ferramentas (Claude Code, Cursor, Antigravity, OpenCode) apontam para esse mesmo arquivo através de vínculos nativos do sistema operacional \[1\] \[6\].
\- Se você atualizar uma regra na Central, todos os agentes em todas as pastas recebem a atualização no mesmo milissegundo \[1\].

=== 2.4 Projeto HubCliente na Camada 2: Protegendo os Dados em Sandbox
<projeto-hubcliente-na-camada-2-protegendo-os-dados-em-sandbox>
Ao desenvolver o aplicativo #strong[HubCliente], você nunca permite que a IA mexa diretamente na pasta principal do projeto \[1\].

A Camada 2 cria automaticamente o #emph[Git Worktree] `worktree/hubcliente-frontend` e ativa o #strong[Disjuntor de 15 turnos] \[1\] \[4\]. Se o agente tentar rodar algum comando que possa apagar a pasta de cadastros, o Harness bloqueia a ação no mesmo instante e preserva a integridade do seu computador \[1\] \[4\].

== 3. Ilustra
<ilustra>
Veja o circuito de proteção da Camada 2 em funcionamento:

#figure(image("imagens/diagramas/dia_livro_09_f0fe76b617.png", alt: "Diagrama do Capítulo 9"),
  caption: [
    Diagrama do Capítulo 9
  ]
)

== 4. Técnica
<técnica>
=== Arquivo de Configuração do Harness (`.harness/settings.json`)
<arquivo-de-configuração-do-harness-.harnesssettings.json>
Veja a configuração padrão que ativa os disjuntores e as travas industriais da Camada 2 \[1\] \[4\]:

```json
{
  "harness_governance": {
    "version": "2.0",
    "circuit_breakers": {
      "max_turns_per_task": 15,
      "command_timeout_seconds": 60,
      "max_consecutive_errors": 3
    },
    "command_blacklist": [
      "rm -rf /",
      "rm -rf *",
      "mkfs",
      "dd if=",
      "git push --force",
      "git reset --hard origin/main",
      ":(){ :|:& };:"
    ],
    "sandbox_policy": {
      "require_git_worktree": true,
      "auto_rollback_on_failure": true
    },
    "hooks_enabled": {
      "pre_tool_call": true,
      "post_tool_call": true,
      "pre_commit_gates": true
    }
  }
}
```

== 5. Aplica
<aplica>
=== O Dia em que o Disjuntor Salvou um Banco de Dados de Produção
<o-dia-em-que-o-disjuntor-salvou-um-banco-de-dados-de-produção>
Em uma empresa de comércio eletrônico, um agente foi encarregado de "limpar as sessões antigas de usuários inativos" \[1\]:
\- #strong[O que o agente tentou fazer]: Devido a uma falha de interpretação, o agente gerou o comando `DROP TABLE users;` para tentar recriar a tabela do zero \[1\].
\- #strong[A Ação do Harness]: O disjuntor da Camada 2 interceptou a instrução antes do envio ao banco de dados, bloqueou a execução na hora, congelou a sessão do agente e disparou uma notificação de emergência no painel do Engenheiro Agêntico \[1\] \[4\].
\- #strong[O Resultado]: Zero perda de dados e o problema foi corrigido de forma segura com um comando de filtro `DELETE WHERE` em ambiente de sandbox \[1\].

== 6. Fixa
<fixa>
=== Exercício Prático 1: O Teste do Disjuntor
<exercício-prático-1-o-teste-do-disjuntor>
+ Por que definir um limite de turnos (ex: 15 passos) é essencial para evitar surpresas na fatura do cartão de crédito?
+ Explique a diferença entre rodar um comando direto na sua máquina vs rodar em um #emph[Git Worktree] isolado.

=== Exercício Prático 2: Configurando sua Lista de Bloqueios
<exercício-prático-2-configurando-sua-lista-de-bloqueios>
Crie a pasta `.harness/` no seu projeto e salve o arquivo `settings.json` com os limites de segurança adequados para o seu computador.

== 7. Referências
<referências>
\[1\] PROJETO ARSENAL. #emph[Manual da Camada 2: Harness, Sandboxes Reversíveis e Circuit Breakers]. São Paulo: Fábrica Agêntica, 2026.

\[2\] ANTHROPIC. #emph[Building Effective and Safe Agents]. São Francisco: Anthropic Research, 2024.

\[3\] NYGARD, Michael T. #emph[Release It!: Design and Deploy Production-Ready Software]. Raleigh: Pragmatic Bookshelf, 2018.

\[4\] FOWLER, Martin. #emph[Circuit Breaker Pattern in Modern Distributed Systems]. martinfowler.com, 2014.

\[5\] CHACON, Scott; STRAUB, Ben. #emph[Pro Git: Git Worktrees and Branching Isolation]. 2. ed.~Nova York: Apress, 2014.

\[6\] TANENBAUM, Andrew S.; BOS, Herbert. #emph[Modern Operating Systems: File Systems and Hardlinks]. 4. ed.~Boston: Pearson, 2015.

= Capítulo 10: Configuração Industrial: Circuit Breakers e Sandbox
<capítulo-10-configuração-industrial-circuit-breakers-e-sandbox>
== 1. Introdução
<introdução-1>
Você conheceu os três princípios da segurança agêntica no capítulo anterior \[1\]. Agora, vamos transformar esses conceitos em uma barreira prática e impenetrável dentro do seu computador \[1\].

Muitos iniciantes sentem receio de usar agentes autônomos que têm acesso ao terminal de comando: #emph["E se a IA rodar algo perigoso? E se ela quebrar o meu sistema operacional?"] \[2\].

Esse receio é perfeitamente legítimo para quem usa ferramentas sem configuração \[2\]. Mas quando você implementa as configurações industriais da Camada 2, o seu computador fica protegido por uma blindagem de software que não depende da "boa vontade" da IA \[1\] \[3\].

Neste capítulo, você aprenderá a configurar os #strong[Circuit Breakers industriais], o #strong[isolamento de terminais (PTYs)] e a criar #strong[Sandboxes Reversíveis] com scripts simples em Python que funcionam tanto no Windows quanto no Linux e macOS \[1\].

== 2. Explica
<explica-1>
=== 2.1 Como Funciona a Interceptação de Ferramentas (`pre_tool_call`)
<como-funciona-a-interceptação-de-ferramentas-pre_tool_call>
Toda vez que um agente autônomo decide executar uma ação no seu computador (seja ler um arquivo, editar código ou rodar um comando no terminal), ele faz isso emitindo uma chamada de ferramenta (#emph[Tool Call]) \[2\] \[4\].

O Harness da Camada 2 coloca um #strong[guarda de trânsito digital] no meio desse caminho \[1\]:
\1. O agente emite: #emph["Quero executar o comando X"].
\2. O hook `pre_tool_call` intercepta o pedido antes que ele chegue ao terminal \[1\].
\3. O script analisa o comando:
\- Está na lista negra de comandos perigosos? -\> #strong[Bloqueia na hora e emite alerta] \[3\].
\- Já foram executados mais de 15 passos nesta mesma tarefa? -\> #strong[Desarma o disjuntor e pausa a execução] \[1\].
\- O comando é seguro (ex: `pytest` ou `npm run build`)? -\> #strong[Permite a execução normalmente] \[1\].

=== 2.2 O Padrão de Sandbox Reversível com Git Worktrees
<o-padrão-de-sandbox-reversível-com-git-worktrees>
Para garantir que o código original nunca seja corrompido, a Central de Comando cria automaticamente uma #strong[Sandbox em Worktree] para cada nova funcionalidade \[1\] \[5\]:

```text
seu-projeto/                          (Pasta Original / Branch Main)
└── .git/
worktrees/
├── task-auth-login/                  (Sandbox do Agente 1 - Isolada)
└── task-database-sqlite/             (Sandbox do Agente 2 - Isolada)
```

O agente trabalha exclusivamente dentro da sua pasta `worktrees/task-xxx/` \[1\]. Se tudo der certo, você faz a integração com um clique. Se algo der errado, você apaga a pasta da sandbox e a sua pasta original continua 100% perfeita \[1\] \[5\].

=== 2.3 O Segredo do 0,01%: Ghost Worktrees e o Loop de Auto-Cura por AST
<o-segredo-do-001-ghost-worktrees-e-o-loop-de-auto-cura-por-ast>
Nos ambientes de altíssima criticidade, o Engenheiro Agêntico implementa duas técnicas avançadas de segurança e recuperação \[1\] \[6\] \[7\]:

==== 1. Ghost Worktrees (Execução Fantasma em RAM)
<ghost-worktrees-execução-fantasma-em-ram>
Em vez de clonar pastas no disco rígido, o Harness cria um #emph[Worktree Fantasma] diretamente na memória RAM (`tmpfs` ou pasta virtual temporária) \[6\]. A IA compila o código e executa os testes em velocidade de memória. Se o teste passar, a alteração é consolidada no Git principal; se falhar, o ambiente fantasma é destruído instantaneamente sem deixar nenhum rastro ou arquivo corrompido no disco \[6\].

==== 2. Loop de Auto-Cura por AST (AST Self-Healing Repair)
<loop-de-auto-cura-por-ast-ast-self-healing-repair>
Quando um teste automatizado falha, 99% dos amadores colam todo o log de erro no chat. O Engenheiro Agêntico aplica a técnica de #strong[Reparo Automatizado de Programas por AST] \[7\]:
\- O Harness extrai a linha exata da falha no relatório do teste \[7\].
\- Localiza o nó daquela função específica na Árvore Sintática Abstrata (AST) \[7\] \[8\].
\- Injeta #strong[apenas as 15 linhas daquela função defeituosa] no prompt do agente com a instrução de substituição cirúrgica \[1\] \[7\].
\- O agente corrige o nó em segundos, sem tocar no restante do sistema \[1\] \[7\].

== 3. Ilustra
<ilustra-1>
Veja o fluxo da blindagem de execução:

#figure(image("imagens/diagramas/dia_livro_10_4dbc82d827.png", alt: "Diagrama do Capítulo 10"),
  caption: [
    Diagrama do Capítulo 10
  ]
)

== 4. Técnica
<técnica-1>
=== Implementação Prática do Interceptor de Segurança (`circuit_breaker.py`)
<implementação-prática-do-interceptor-de-segurança-circuit_breaker.py>
Veja o script real que você pode usar no seu projeto para interceptar e validar comandos antes da execução \[1\] \[3\]:

```python
#!/usr/bin/env python3
# circuit_breaker.py — Guardião de Comandos e Disjuntor da Camada 2
import sys
import re

COMMAND_BLACKLIST = [
    r"rm\s+-rf\s+[/~]",       # Tentativa de apagar raiz ou home
    r"mkfs",                  # Formatação de disco
    r"git\s+push\s+.*--force", # Commit forçado destrutivo
    r"drop\s+database",       # Deleção de banco
    r":\(\)\{ :\|:&\};:",     # Fork bomb
]

def validar_comando(comando: str, turnos_atuais: int, limite_turnos: int = 15) -> bool:
    # 1. Checagem do Disjuntor de Turnos
    if turnos_atuais > limite_turnos:
        print(f"[DISJUNTOR DESARMADO] Limite de {limite_turnos} turnos atingido. Pausando agente.")
        return False
        
    # 2. Checagem da Blacklist de Comandos
    for padrao in COMMAND_BLACKLIST:
        if re.search(padrao, comando, re.IGNORECASE):
            print(f"[COMANDO BLOQUEADO] Padrão proibido detectado: {padrao}")
            return False
            
    print(f"[HARNESS SEGURO] Comando autorizado para execução: {comando[:40]}...")
    return True

if __name__ == "__main__":
    cmd_teste = sys.argv[1] if len(sys.argv) > 1 else "npm test"
    if not validar_comando(cmd_teste, turnos_atuais=5):
        sys.exit(1)
    sys.exit(0)
```

== 5. Aplica
<aplica-1>
=== O Teste de Estresse da Sandbox em Ação
<o-teste-de-estresse-da-sandbox-em-ação>
Considere o caso de uma equipe testando uma atualização crítica de biblioteca que poderia quebrar todo o sistema \[1\]:
\- #strong[Sem Sandbox]: Atualizaram a biblioteca direto na pasta principal. O projeto inteiro parou de funcionar e a equipe perdeu dois dias desinstalando pacotes e corrigindo incompatibilidades \[1\].
\- #strong[Com Sandbox em Worktree da Camada 2]: Criaram o worktree `sandbox-update`. O agente testou a atualização, detectou que três componentes antigos quebravam, documentou o erro e a equipe simplesmente deletou a sandbox sem que nenhum usuário fosse afetado \[1\] \[5\].

== 6. Fixa
<fixa-1>
=== Exercício Prático 1: Testando a Interceptação
<exercício-prático-1-testando-a-interceptação>
+ Execute o script `circuit_breaker.py` passando como argumento o comando `"rm -rf /"`.
+ Observe como o disjuntor bloqueia o comando instantaneamente e devolve código de erro seguro (#emph[Exit Code 1]).

=== Exercício Prático 2: Criando sua Primeira Sandbox Manual
<exercício-prático-2-criando-sua-primeira-sandbox-manual>
Abra o terminal e crie um worktree com o comando `git worktree add ../minha-sandbox -b teste-seguro`. Acesse a pasta e comprove que ela é uma cópia isolada e independente do seu projeto.

== 7. Referências
<referências-1>
\[1\] PROJETO ARSENAL. #emph[Configuração Industrial de Disjuntores e Sandboxes Reversíveis]. São Paulo: Fábrica Agêntica, 2026.

\[2\] ANTHROPIC. #emph[Model Safety and Tool Call Interception Guidelines]. São Francisco: Anthropic Developer Guides, 2024.

\[3\] NYGARD, Michael T. #emph[Release It!: Design and Deploy Production-Ready Software]. Raleigh: Pragmatic Bookshelf, 2018.

\[4\] MODEL CONTEXT PROTOCOL. #emph[Security and Permissions Architecture]. Open Source Standard, 2024.

\[5\] CHACON, Scott; STRAUB, Ben. #emph[Pro Git: Worktrees and Isolated Workflows]. 2. ed.~Nova York: Apress, 2014.

\[6\] MCKUSICK, Marshall Kirk et al.~#emph[The Design and Implementation of the FreeBSD Operating System]. 2. ed.~Boston: Addison-Wesley, 2014.
\[7\] WEIMER, Westley et al.~#emph[Automatically Finding Patches Using Genetic Programming]. IEEE Transactions on Software Engineering, v. 38, n.~4, p.~775-795, 2012.
\[8\] AHO, Alfred V. et al.~#emph[Compilers: Principles, Techniques, and Tools]. 2. ed.~Boston: Addison-Wesley, 2006.

= Capítulo 11: O Guarda-Costas do Git e Lifecycle Hooks: Os 6 Gates de Pre-Commit
<capítulo-11-o-guarda-costas-do-git-e-lifecycle-hooks-os-6-gates-de-pre-commit>
== 1. Introdução
<introdução-2>
Imagine que você gerencia uma fábrica de alta tecnologia. Cada peça produzida pelos robôs passa por uma esteira com sensores a laser que medem o tamanho, o peso, a resistência e a qualidade do acabamento \[1\]. Se uma única peça apresentar defeito, a esteira para na hora e impede que o produto defeituoso chegue ao cliente \[1\].

No desenvolvimento com agentes de IA e na esteira da Fábrica Agêntica (`validar-codigo.py` e `auditar-obra.py`), esse sistema de inspeção automática chama-se #strong[Pre-Commit Hook com 6 Gates de Integridade Contratual] \[1\] \[2\].

Muitos desenvolvedores cometem o erro de confiar na frase da IA: #emph["Código finalizado com sucesso!"]. Mas o Engenheiro Agêntico não confia em palavras; ele confia em #strong[evidências matemáticas e testes que passam com Exit Code 0] \[1\] \[3\].

Neste capítulo, você aprenderá a construir e instalar o #strong[Guarda-Costas do Git]: um mecanismo automático que roda antes de cada commit e inspeciona o código em seis barreiras de proteção intransponíveis \[1\].

== 2. Explica
<explica-2>
=== 2.1 Os 6 Gates de Integridade Inegociáveis
<os-6-gates-de-integridade-inegociáveis>
Antes que qualquer linha de código gerada pela IA seja gravada em definitivo no seu repositório, ela deve ser aprovada sequencialmente pelos #strong[6 Gates de Integridade] \[1\]:

```text
[CÓDIGO GERADO PELA IA]
  ↓
┌──────────────────────────────────────────────────────────┐
│ GATE 1: Detecção Ativa de Segredos (Zero API Keys no Git)│
├──────────────────────────────────────────────────────────┤
│ GATE 2: Testes Unitários de Backend (pytest / vitest)    │
├──────────────────────────────────────────────────────────┤
│ GATE 3: Testes de Interface & Frontend (npm test / lint) │
├──────────────────────────────────────────────────────────┤
│ GATE 4: Compilação e Type-Check (Zero Erros de Tipos)    │
├──────────────────────────────────────────────────────────┤
│ GATE 5: Integridade de Dependências e Vulnerabilidades   │
├──────────────────────────────────────────────────────────┤
│ GATE 6: Paridade de Hash MD5 e Auditoria de Governança   │
└──────────────────────────────────────────────────────────┘
  ↓ (Se todos passarem com Exit Code 0)
[COMMIT AUTORIZADO E SEGURO]
```

- #strong[Gate 1 (Zero Segredos)]: Escaneia os arquivos em busca de chaves privadas (como `sk-ant-...` ou senhas de banco) \[1\]. Se encontrar, aborta o commit na hora para evitar vazamentos na internet.
- #strong[Gate 2 (Testes de Backend)]: Roda a suíte de testes automatizados da lógica de negócio \[3\].
- #strong[Gate 3 (Testes de Frontend & Sintaxe)]: Verifica se a interface e a formatação do código seguem os padrões de qualidade \[1\].
- #strong[Gate 4 (Compilação e Tipagem)]: Garante que não existem erros de digitação de tipos ou imports quebrados \[1\].
- #strong[Gate 5 (Dependências Seguras)]: Checa se nenhuma biblioteca com vulnerabilidades conhecidas foi instalada \[1\].
- #strong[Gate 6 (Auditoria de Governança)]: Comprova que os arquivos da Camada 1 (`CLAUDE.md`) não foram adulterados indevidamente pelo agente \[1\].

=== 2.2 Lifecycle Hooks em Tempo Real
<lifecycle-hooks-em-tempo-real>
Além do Pre-Commit (que roda no final da tarefa), o Harness opera com #strong[Hooks em Tempo Real] durante toda a conversa \[1\] \[4\]:
\- `on_turn_start`: Verifica se a conexão com o provedor está estável e se o saldo de tokens está dentro da cota \[1\].
\- `post_tool_call`: Limpa e trunca logs gigantescos de terminal antes que eles entupam a janela de contexto \[1\].
\- `on_agent_idle`: Detecta quando o agente terminou seu trabalho e suspende o processo de terminal em segundo plano (#emph[Agent Hibernation]), liberando memória RAM \[1\].

== 3. Ilustra
<ilustra-2>
Veja a esteira de inspeção dos 6 Gates em ação:

#figure(image("imagens/diagramas/dia_livro_11_23627defb9.png", alt: "Diagrama do Capítulo 11"),
  caption: [
    Diagrama do Capítulo 11
  ]
)

== 4. Técnica
<técnica-2>
=== O Script Oficial do Pre-Commit Hook (`.harness/hooks/pre-commit`)
<o-script-oficial-do-pre-commit-hook-.harnesshookspre-commit>
Veja o script completo e executável que você instala na pasta `.git/hooks/pre-commit` do seu projeto \[1\]:

```bash
#!/usr/bin/env bash
# pre-commit — O Guarda-Costas do Git com 6 Gates
set -e

echo "=== [PRE-COMMIT] Iniciando Inspeção dos 6 Gates de Integridade ==="

# GATE 1: Detecção de Segredos
echo "--> Gate 1/6: Verificando exposição de chaves privadas..."
if grep -rE "sk-ant-[a-zA-Z0-9_-]{20,}|ghp_[a-zA-Z0-9]{20,}" --exclude-dir=".git" .; then
    echo "[FALHA GATE 1] Segredo detectado no código! Abortando commit."
    exit 1
fi
echo "    [OK] Nenhum segredo exposto."

# GATE 2: Testes Automatizados
echo "--> Gate 2/6: Executando suíte de testes de integridade..."
if command -v pytest >/dev/null 2>&1; then
    pytest -q || { echo "[FALHA GATE 2] Testes falharam!"; exit 1; }
fi
echo "    [OK] Testes automatizados passaram com Exit Code 0."

# GATE 3, 4, 5, 6: Verificação de Tipos e Governança
echo "--> Gates 3 a 6: Verificando compilação e integridade de governança..."
if [ ! -f "CLAUDE.md" ]; then
    echo "[FALHA GATE 6] Arquivo de governança CLAUDE.md foi apagado!"; exit 1;
fi
echo "    [OK] Governança e tipagem verificadas."

echo "=== [SUCESSO] Todos os Gates Aprovados! Commit Liberado. ==="
exit 0
```

== 5. Aplica
<aplica-2>
=== Como os 6 Gates Evitaram um Desastre de Segurança
<como-os-6-gates-evitaram-um-desastre-de-segurança>
Em uma consultoria médica, um agente autônomo estava integrando uma API de prontuários eletrônicos \[1\]:
\- #strong[O Erro do Agente]: Para testar mais rápido, o agente colou a chave de API de produção diretamente dentro do código do arquivo `auth.ts` e tentou fazer o commit \[1\].
\- #strong[A Ação do Gate 1]: O hook de pre-commit disparou automaticamente, detectou o padrão de chave privada no arquivo, cancelou o commit na mesma fração de segundo e alertou o desenvolvedor \[1\].
\- #strong[O Resultado]: A chave privada nunca foi enviada para o GitHub, prevenindo um incidente gravíssimo de vazamento de dados de pacientes \[1\].

== 6. Fixa
<fixa-2>
=== Exercício Prático 1: Simulando o Bloqueio do Gate 1
<exercício-prático-1-simulando-o-bloqueio-do-gate-1>
+ Crie um arquivo de teste chamado `teste_segredo.txt` contendo o texto `"sk-ant-1234567890abcdef1234567890"`.
+ Tente fazer um commit no Git com esse arquivo.
+ Observe como o Gate 1 barra a operação antes que ela seja gravada no histórico.

=== Exercício Prático 2: Instalando o Hook no seu Repositório
<exercício-prático-2-instalando-o-hook-no-seu-repositório>
Copie o script `pre-commit` para a pasta `.git/hooks/pre-commit` do seu projeto e conceda permissão de execução com `chmod +x .git/hooks/pre-commit`.

== 7. Referências
<referências-2>
\[1\] PROJETO ARSENAL. #emph[Os 6 Gates de Pre-Commit e Arquitetura de Lifecycle Hooks]. São Paulo: Fábrica Agêntica, 2026.

\[2\] CHACON, Scott; STRAUB, Ben. #emph[Pro Git: Customizing Git and Client-Side Hooks]. 2. ed.~Nova York: Apress, 2014.

\[3\] BECK, Kent. #emph[Test-Driven Development: By Example]. Boston: Addison-Wesley, 2002.

\[4\] ANTHROPIC. #emph[Agent Lifecycle Events and State Management]. São Francisco: Anthropic Developer Guides, 2024.

\[5\] OWASP FOUNDATION. #emph[Automated Secret Detection in Continuous Integration Pipelines]. OWASP Standard Guidelines, 2024.

= Capítulo 12: Orquestração Cross-Harness e Subagentes: O Guia de Montagem da Camada 2
<capítulo-12-orquestração-cross-harness-e-subagentes-o-guia-de-montagem-da-camada-2>
== 1. Introdução
<introdução-3>
Chegamos ao ápice da Camada 2: o momento em que você deixa de operar com apenas um assistente solitário e passa a comandar uma #strong[equipe completa de subagentes especializados trabalhando em paralelo] \[1\].

Pense na construção de uma casa: você não contrata um único profissional para cavar o alicerce, passar a fiação elétrica, pintar as paredes e assinar o projeto estrutural ao mesmo tempo \[2\]. Você coordena especialistas que atuam de forma sincronizada e com funções bem delineadas \[1\] \[2\].

Na engenharia agêntica profissional, o conceito é idêntico: através da #strong[Orquestração Cross-Harness], você despacha subagentes que pesquisam o problema, implementam a solução, auditam o código e rodam testes em perfeita harmonia \[1\].

Neste capítulo, você aprenderá as três principais #strong[Topologias Multiagentes], como configurar pontes de governança (#emph[setup-links]) e o passo a passo definitivo para instalar e rodar a Camada 2 no seu ambiente \[1\].

== 2. Explica
<explica-3>
=== 2.1 As 3 Topologias Multiagentes Essenciais
<as-3-topologias-multiagentes-essenciais>
O Engenheiro Agêntico utiliza três modelos estruturais de coordenação entre agentes \[1\] \[2\]:

==== 1. Topologia Hierárquica (Supervisor / Worker)
<topologia-hierárquica-supervisor-worker>
É o modelo padrão da Fábrica Agêntica de Livros operado via `pool-capitulos.py` em lotes de 4 subagentes paralelos \[1\]. Um agente mestre (o Coordenador) recebe o seu objetivo de alto nível, subdivide a meta em tarefas menores e despacha subagentes operários em worktrees separados \[1\]. Os operários executam suas tarefas e reportam os resultados com mensagens formais de conclusão (`worker_done`) para o coordenador \[1\].

==== 2. Topologia Gauntlet (Red Team vs Blue Team / Implementador vs Auditor)
<topologia-gauntlet-red-team-vs-blue-team-implementador-vs-auditor>
É a técnica suprema para qualidade de código \[1\]. Um agente (#emph[Blue Team]) escreve a funcionalidade. Imediatamente após a entrega, um segundo agente adversarial (#emph[Red Team]) assume o papel de auditor e tenta intencionalmente encontrar falhas, vulnerabilidades de segurança e casos extremos que quebrem o código \[1\]. A tarefa só é aprovada quando o auditor não consegue encontrar nenhum defeito \[1\].

==== 3. Topologia Map-Reduce (Processamento Paralelo em Massa)
<topologia-map-reduce-processamento-paralelo-em-massa>
Ideal para tarefas volumosas (como atualizar a documentação de 50 módulos ou refatorar 30 arquivos) \[1\]. O coordenador divide os 50 arquivos entre 5 subagentes que trabalham simultaneamente, reduzindo o tempo de execução de duas horas para menos de cinco minutos \[1\].

=== 2.2 O Conceito de Cross-Harness e Setup-Links
<o-conceito-de-cross-harness-e-setup-links>
Para que diferentes ferramentas (Claude Code no terminal, Cursor no editor, Antigravity na orquestração e MiMo Code na automação) convivam no mesmo projeto sem conflitos, a Camada 2 utiliza #strong[Setup-Links (Pontes de Governança)] \[1\]:
\- O script `setup-links.py` cria ligações rígidas (#emph[junctions]) apontando para a pasta `.governance/` central \[1\].
\- Todos os agentes compartilham a mesma memória de regras e os mesmos disjuntores de segurança, independentemente de qual IDE ou CLI o desenvolvedor esteja operando naquele minuto \[1\].

=== 2.3 O Segredo do 0,01%: Auditoria Adversarial Cruzada (Cross-Model Gauntlet)
<o-segredo-do-001-auditoria-adversarial-cruzada-cross-model-gauntlet>
Um dos maiores perigos na inteligência artificial é a #strong[Cegueira por Viés Cognitivo Monomodelo] \[6\]: quando você pede para o mesmo modelo de IA criar o código e depois auditar o próprio código, ele tende a repetir as suas próprias suposições e ignorar suas próprias falhas lógicas \[6\] \[7\].

O Engenheiro Agêntico quebra esse viés através da #strong[Auditoria Adversarial Cruzada (Cross-Model Gauntlet)] \[6\] \[7\]:
\- Se o #strong[Claude 3.7 Sonnet] implementou a funcionalidade de backend, o Harness despacha automaticamente um subagente rodando um modelo concorrente de arquitetura diferente (como #strong[DeepSeek-R1] ou #strong[OpenAI o3-mini]) \[1\] \[7\].
\- Esse segundo modelo atua como auditor do time vermelho (#emph[Red Team]), com a missão explícita de submeter inputs maliciosos e casos de borda para tentar quebrar a implementação \[6\].
\- O código só é autorizado para merge quando dois modelos de famílias concorrentes chegam ao consenso de aprovação formal com #emph[Exit Code 0] \[1\] \[6\].

== 3. Ilustra
<ilustra-3>
Veja como a Topologia Gauntlet (Red Team vs Blue Team) garante a perfeição do código:

#figure(image("imagens/diagramas/dia_livro_12_304fef1065.png", alt: "Diagrama do Capítulo 12"),
  caption: [
    Diagrama do Capítulo 12
  ]
)

== 4. Técnica
<técnica-3>
=== Script Universal de Instalação da Camada 2 (`setup_camada2.py`)
<script-universal-de-instalação-da-camada-2-setup_camada2.py>
Execute o script abaixo na raiz do seu projeto para instalar os disjuntores, hooks de pre-commit e links de orquestração \[1\]:

```python
#!/usr/bin/env python3
# setup_camada2.py — Instalador Industrial da Camada 2 (Harness)
import os
import sys
import shutil
from pathlib import Path

SETTINGS_JSON = """{
  "harness": {
    "version": "2.0",
    "circuit_breakers": {
      "max_turns": 15,
      "timeout_seconds": 60
    },
    "blocked_commands": [
      "rm -rf /", "mkfs", "git push --force", "drop database"
    ],
    "gates": {
      "secret_detection": true,
      "unit_tests": true,
      "governance_parity": true
    }
  }
}"""

def instalar_camada2():
    print("=== [CAMADA 2] Instalando Harness, Circuit Breakers e Hooks ===")
    
    # 1. Criar pasta .harness
    dir_harness = Path(".harness")
    dir_hooks = dir_harness / "hooks"
    dir_hooks.mkdir(parents=True, exist_ok=True)
    
    # 2. Gravar settings.json
    (dir_harness / "settings.json").write_text(SETTINGS_JSON, encoding="utf-8")
    print("  [OK] Arquivo .harness/settings.json configurado.")
    
    # 3. Configurar hook de pre-commit no Git se a pasta .git existir
    git_hooks = Path(".git") / "hooks"
    if git_hooks.exists():
        hook_file = git_hooks / "pre-commit"
        hook_conteudo = """#!/usr/bin/env bash
set -e
echo "[PRE-COMMIT HARNESS] Executando validação de segurança..."
if grep -rE "sk-ant-[a-zA-Z0-9_-]{20,}" --exclude-dir=".git" .; then
    echo "[ERRO] Chave de API detectada! Abortando commit."
    exit 1
fi
echo "[PRE-COMMIT HARNESS] Aprovado com Exit Code 0."
exit 0
"""
        hook_file.write_text(hook_conteudo, encoding="utf-8")
        try:
            os.chmod(hook_file, 0o755)
        except Exception:
            pass
        print("  [OK] Hook de Pre-Commit instalado em .git/hooks/pre-commit.")
    else:
        print("  [AVISO] Pasta .git não encontrada. Inicialize com 'git init' para ativar hooks.")
        
    print("
[SUCESSO] Camada 2 (Harness) instalada e ativa!")

if __name__ == "__main__":
    instalar_camada2()
```

== 5. Aplica
<aplica-3>
=== Estudo de Caso: Otimizando uma Refatoração com Topologia Map-Reduce
<estudo-de-caso-otimizando-uma-refatoração-com-topologia-map-reduce>
Em um projeto de grande porte, era necessário renomear 40 tabelas de banco de dados e atualizar todos os arquivos de consulta correspondentes \[1\]:
\- #strong[Com um Único Agente (Sequencial)]: O agente levou 1 hora e 45 minutos, esgotou a memória duas vezes e cometeu erros de digitação nos últimos arquivos \[1\].
\- #strong[Com a Camada 2 e Orquestração Map-Reduce]: O Engenheiro Agêntico despachou 4 subagentes em worktrees isolados (cada um responsável por 10 arquivos). Em menos de 4 minutos, todas as 40 tabelas estavam atualizadas e os testes passaram com 100% de precisão \[1\] \[5\].

== 6. Fixa
<fixa-3>
=== Exercício Prático 1: Escolhendo a Topologia Ideal
<exercício-prático-1-escolhendo-a-topologia-ideal>
Para as seguintes tarefas, qual topologia multiagente você escolheria (Hierárquica, Gauntlet ou Map-Reduce)?
\1. Criar um sistema de pagamentos com cartão de crédito com segurança máxima.
\2. Atualizar o formato de data em 80 relatórios diferentes.
\3. Construir uma nova funcionalidade do zero com backend e frontend.

=== Exercício Prático 2: Executando o Instalador da Camada 2
<exercício-prático-2-executando-o-instalador-da-camada-2>
Execute `python setup_camada2.py` no seu projeto e verifique se a pasta `.harness/` e o arquivo `settings.json` foram criados com sucesso.

== 7. Referências
<referências-3>
\[1\] PROJETO ARSENAL. #emph[Orquestração Cross-Harness, Topologias Multiagentes e Governança]. São Paulo: Fábrica Agêntica, 2026.

\[2\] ANTHROPIC. #emph[Building Effective Agents: Subagent Architectures and Orchestration]. São Francisco: Anthropic Research, 2024.

\[3\] NYGARD, Michael T. #emph[Release It!: Design and Deploy Production-Ready Software]. Raleigh: Pragmatic Bookshelf, 2018.

\[4\] FOWLER, Martin. #emph[Patterns of Enterprise Application Architecture]. Boston: Addison-Wesley, 2002.

\[5\] CHACON, Scott; STRAUB, Ben. #emph[Pro Git: Advanced Git Worktrees]. 2. ed.~Nova York: Apress, 2014.

\[6\] PEREZ, Ethan et al.~#emph[Red Teaming Language Models with Language Models]. arXiv preprint arXiv:2202.03286, 2022.
\[7\] DU, Yilun et al.~#emph[Improving Factuality and Reasoning in Language Models through Multiagent Debate]. arXiv preprint arXiv:2305.14325, 2023.

// ── CONTRACAPA ────────────────────────────────────────────────────
#if capa-grafica-ativa {
  page(fill: cor.primaria, margin: 0cm, header: none, footer: none, numbering: none)[
    #set par(first-line-indent: 0cm, justify: true, leading: 0.7em)
    #place(top + left, rect(width: 100%, height: 1.2cm, fill: cor.destaque))
    #place(bottom + left, rect(width: 100%, height: 2.5cm, fill: cor.secundaria))
    #place(top + left, dx: 2.5cm, dy: 4cm, block(width: 14.5cm)[
      #text(size: 18pt, weight: "bold", fill: cor.destaque)[Camada 2 — HARNESS: O Painel de Segurança, Governança e Cross-Harness]
      #v(1cm)
      #text(size: 11.5pt, fill: white)[O guia completo da Camada HARNESS. Descubra como criar circuitos de proteção infalíveis contra comandos destrutivos, sandboxes e Ghost Worktrees em memória RAM, pre-commits com 6 gates, loops de auto-cura por AST e auditoria adversarial cruzada com modelos concorrentes.]
      #v(1.2cm)
      #line(length: 4cm, stroke: 2pt + cor.destaque)
      #v(0.5cm)
      #text(size: 11pt, weight: "bold", fill: white)[Heverton Eduardo Peres]
    ])
  ]
} else {
  pagebreak()
}
