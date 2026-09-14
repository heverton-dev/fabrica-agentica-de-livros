#set document(
  title: "Manual OmniRoute",
  author: "Marketing Conexão",
)

#set page(
  paper: "a4",
  margin: (top: 0mm, bottom: 0mm, left: 0mm, right: 0mm),
)

#set text(font: "Times New Roman", size: 12pt, lang: "pt")

// Capa
#page(margin: 0mm)[
  #set align(center + horizon)
  
  #box(
    width: 210mm,
    height: 297mm,
    fill: gradient.linear(
      ..color.map.cividis
    ),
    {
      set text(fill: white, weight: "bold")
      
      v(80mm)
      
      text(size: 48pt)[Manual OmniRoute]
      
      v(20mm)
      
      text(size: 24pt)[
        15 Provedores de IA Gratuitos\
        para Máxima Confiabilidade
      ]
      
      v(40mm)
      
      text(size: 14pt)[
        Agregue Google Vertex AI, Claude, GPT-4\
        e mais em um único hub
      ]
      
      v(60mm)
      
      text(size: 12pt, fill: rgba(white, 0.9))[
        Editora Agêntica\
        Agosto 2026 — Versão 1.0
      ]
    }
  )
]

// Folha de rosto
#pagebreak()

#set page(margin: (top: 3cm, bottom: 2cm, left: 3cm, right: 2cm))
#set align(center + horizon)

#text(size: 24pt, weight: "bold")[Manual OmniRoute]

#v(1cm)

#text(size: 16pt)[
  15 Provedores de IA Gratuitos para\
  Máxima Confiabilidade
]

#v(2cm)

#text(size: 14pt)[
  Marketing Conexão
]

#v(3cm)

#align(bottom)[
  #grid(
    columns: 1,
    gutter: 0.5cm,
    [*Versão* 1.0],
    [*Data* 24 de agosto de 2026],
    [*Editora* Editora Agêntica],
    [*Local* São Paulo],
  )
]

// Conteúdo
#pagebreak()

#set align(left)
#counter(page).update(1)

#outline(depth: 2, indent: auto)

