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
//   sem_folha_rosto                    -> "1" pula a folha de rosto (capa -> CIP direto, LIVRO)

#set document(
  title: "$title$",
  author: "$author$",
  date: datetime.today(),
)

// ── Cor cromatica da obra (derivada da mesma cor de accent da capa —
// REGRA 5 / scripts/series_capa.py — nunca mais uma paleta fixa isolada) ──
#let cor-acento-str = "$cor_acento$"
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
      align(center, "$title$")
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

#let capa-grafica-ativa = "$sem_capa_grafica$" != "1"

// Regra editorial (V5.5): LIVRO pode pular a folha de rosto e ir da capa
// direto para a ficha CIP (sem_folha_rosto=1, opt-in via config_obra.json).
#let folha-rosto-ativa = "$sem_folha_rosto$" != "1"

// ── CAPA GRAFICA (Upgrade 5) ──────────────────────────────────────
#if capa-grafica-ativa {
  $if(capa_imagem)$
  // Capa em imagem PNG (padrao visual da serie): pagina inteira, sem margens
  page(fill: rgb("#0b1020"), margin: 0cm, header: none, footer: none, numbering: none)[
    #image("$capa_imagem$", width: 100%, height: 100%, fit: "cover")
  ]
  $else$
  page(fill: cor.primaria, margin: 0cm, header: none, footer: none, numbering: none)[
    #set par(first-line-indent: 0cm, justify: false, leading: 0.55em)
    #place(top + right, dx: -2.2cm, rect(width: 0.35cm, height: 100%, fill: cor.secundaria))
    #place(top + left, rect(width: 100%, height: 1.2cm, fill: cor.destaque))
    #place(bottom + left, rect(width: 100%, height: 4.5cm, fill: cor.secundaria))
    #place(bottom + left, dy: -4.5cm, rect(width: 100%, height: 0.15cm, fill: cor.destaque))

    #place(top + left, dx: 2.5cm, dy: 6.5cm, block(width: 14.5cm)[
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 34pt, weight: "bold", fill: white)[$title$]
      $if(subtitle)$
      #v(0.8cm)
      #line(length: 5cm, stroke: 3pt + cor.destaque)
      #v(0.6cm)
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 15pt, fill: cor.destaque)[$subtitle$]
      $endif$
    ])

    #place(bottom + left, dx: 2.5cm, dy: -1.6cm, block(width: 15cm)[
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 15pt, weight: "bold", fill: white)[$author$]
      #v(0.2cm)
      #text(size: 10pt, fill: cor.clara)[#datetime.today().display("[year]")]
    ])
  ]
  $endif$
}

// ── FOLHA DE ROSTO (ABNT NBR 6029) ────────────────────────────────
#if folha-rosto-ativa {
  page(header: none, footer: none, numbering: none)[
    #set par(first-line-indent: 0cm, justify: false)
    #align(center)[
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 13pt, weight: "bold", fill: cor.secundaria)[$author$]
      #v(3.5cm)
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 22pt, weight: "bold", fill: cor.primaria)[$title$]
      $if(subtitle)$
      #v(0.5cm)
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 14pt, fill: cor.secundaria)[$subtitle$]
      $endif$
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
      $if(cip_local)$$cip_local$$else$Brasil$endif$
      #linebreak()
      $if(cip_ano)$$cip_ano$$else$#datetime.today().display("[year]")$endif$
    ]
  ]
}

// ── VERSO DA FOLHA DE ROSTO: FICHA CATALOGRAFICA (CIP) ────────────
$if(cip_palavras)$
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
        [$if(cip_cutter)$$cip_cutter$$endif$],
        [
          $if(cip_sobrenome)$#upper[$cip_sobrenome$], $cip_nome$$else$$author$$endif$
          #pad(left: 0.8cm)[
            $title$$if(subtitle)$ : $subtitle$$endif$ \/ $author$. --
            $if(cip_local)$$cip_local$$else$Brasil$endif$ : $if(cip_editora)$$cip_editora$$else$Edição do Autor$endif$,
            $if(cip_ano)$$cip_ano$$else$#datetime.today().display("[year]")$endif$.
          ]
          #pad(left: 0.8cm)[$if(cip_paginas)$$cip_paginas$ p. ; 21 cm.$else$; 21 cm.$endif$]
          $if(cip_isbn)$
          #v(0.15cm)
          #pad(left: 0.8cm)[ISBN $cip_isbn$]
          $endif$
          #v(0.15cm)
          #pad(left: 0.8cm)[$cip_palavras$]
          #v(0.3cm)
          #align(right)[$if(cip_cdd)$CDD $cip_cdd$$endif$]
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
$endif$

// ── SUMARIO ───────────────────────────────────────────────────────
#outline(title: [Sumário], indent: 1.5cm, depth: 3)

// ── CONTEUDO PRINCIPAL ────────────────────────────────────────────
$body$

// ── CONTRACAPA ────────────────────────────────────────────────────
$if(sinopse)$
#if capa-grafica-ativa {
  page(fill: cor.primaria, margin: 0cm, header: none, footer: none, numbering: none)[
    #set par(first-line-indent: 0cm, justify: true, leading: 0.7em)
    #place(top + left, rect(width: 100%, height: 1.2cm, fill: cor.destaque))
    #place(bottom + left, rect(width: 100%, height: 2.5cm, fill: cor.secundaria))
    #place(top + left, dx: 2.5cm, dy: 4cm, block(width: 14.5cm)[
      #text(size: 18pt, weight: "bold", fill: cor.destaque)[$title$]
      #v(1cm)
      #text(size: 11.5pt, fill: white)[$sinopse$]
      #v(1.2cm)
      #line(length: 4cm, stroke: 2pt + cor.destaque)
      #v(0.5cm)
      #text(size: 11pt, weight: "bold", fill: white)[$author$]
    ])
  ]
} else {
  pagebreak()
}
$else$
#pagebreak()
$endif$
