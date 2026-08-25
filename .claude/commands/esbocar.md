---
description: Fase 0 (V4) da Fábrica Agêntica de Publicações — elicitação interativa que decide tipo de obra (Livro/TCC), tamanho, mínimo de referências e se gera artigos/ebooks derivados. Único ponto de interação humana; depois disso a esteira roda 100% autônoma (REGRA 3).
---

Você é o Orquestrador Mestre. O operador disparou `/esbocar` com o tema em `$ARGUMENTS`.
Esta é a **Fase 0** — a única rodada de perguntas de toda a esteira.

## Passo 0 — Preparação
1. Slug em kebab-case a partir do tema. Se `output/<slug>/livros/` ou
   `output/<slug>/tccs/` já existir com conteúdo, use sufixo `-v2`.
2. **REGRA HUB POR COLEÇÃO (V5) — obrigatória, sem exceção:** a pasta raiz da obra
   é sempre `output/<slug>/<prefixo>/` (hub primeiro, tipo depois — ex.:
   `output/economia-extrema-de-tokens/livros/`), só criada no Passo 2 quando o tipo
   já é conhecido. **NUNCA** crie raízes planas no topo de `output/`
   (`output/livros/<slug>/`, `output/tccs/<slug>/`, `output/playbooks/<slug>/`
   etc.) — `dir_obra(..., modo='escrita')` rejeita esse layout e todo o resto da
   esteira (colecao.py, empacotar-distribuicao.py, validar-artefatos.py) espera
   o hub. Artigos, e-books e demais derivados de uma obra vivem **dentro do
   mesmo hub** (`output/<slug>/artigos/`, `output/<slug>/ebooks/`,
   `output/<slug>/playbooks/<material>/`, um nível abaixo do tipo, sem pasta
   intermediária) — nunca em raiz própria no topo — e referenciam a obra-mãe via
   `slug_livro_mae`/`obra_mae`.

## Passo 1 — Elicitação (2 rodadas de `AskUserQuestion`)

**Rodada 1 — sempre perguntar (até 4 perguntas por chamada):**

| Header | Pergunta | Opções |
|---|---|---|
| Tipo | Qual o tipo de obra a ser escrita? | Livro (Recommended) \| TCC |
| Senioridade | Qual o nível de senioridade principal do público-alvo? | Iniciante \| Intermediário (Recommended) \| Avançado \| Técnico |
| Refs | Mínimo de referências por capítulo? | 5 \| 8 \| 12 \| 16 \| 20 |
| Artigos | Deseja gerar artigos científicos a partir do tema? | Sim \| Não (Recommended) |

**Rodada 2 — só as perguntas aplicáveis às respostas da Rodada 1:**

| Header | Pergunta | Condição | Opções |
|---|---|---|---|
| Tamanho | Qual o tamanho do livro? | Tipo = Livro | P — 1 Parte, 4 capítulos, ~40 páginas \| M — 2 Partes, 8 capítulos, ~80 páginas (Recommended) \| G — 3 Partes, 12 capítulos, ~120 páginas \| GG — 4 Partes, 16 capítulos, ~160 páginas |
| Ebooks | Deseja gerar e-books a partir da obra? | Tipo = Livro | Sim \| Não (Recommended) |
| Qtd. Artigos | Quantos artigos científicos? | Artigos = Sim | 1 \| 2 \| 3 \| 4 \| 5 |
| Qtd. Ebooks | Quantos e-books? | Ebooks = Sim | 1-3 \| 4-6 \| 7-10 |
| Série | Esta obra faz parte de uma série/coleção? | sempre | Não, standalone (Recommended) \| Other (nome da série) |

**Rodada 3 (V5) — COLEÇÃO: derivados de extração (custo ~0 token):**

| Header | Pergunta | Condição | Opções |
|---|---|---|---|
| Derivados | Quais materiais de extração gerar? (múltipla) | Tipo = Livro | Playbook (Recommended) \| Lead magnets \| Slide deck \| Sequência de e-mails |
| Formatos LM | Quais formatos de lead magnet? (múltipla) | Lead magnets = Sim | Checklist (Recommended) \| Armadilhas \| Cheat sheet \| Mapa |
| CTA | URL de destino do CTA (rastreável) | Lead magnets, Deck ou E-mails = Sim | Other (URL) |

`multiSelect: true` nas duas primeiras. A pergunta **CTA é obrigatória** quando
qualquer um dos três tipos de conversão foi escolhido — sem `cta_url` os gates
R-LM-1 / R-DK-3 / R-EM-2 reprovam. Formatos válidos completos:
`checklist, armadilhas, cheatsheet, mapa, entregas, mini-guia`
(`python scripts/tipos_obra.py --formatos-lm`).

O `AskUserQuestion` aceita no máximo 4 opções por pergunta. Para o tier **XG — 5
Partes, 20 capítulos, ~200 páginas** (o maior da tabela, acima de GG), o operador
seleciona "Other" na pergunta Tamanho e digita `XG`.

Se "Qtd. Ebooks" vier como faixa, use o valor médio da faixa (2, 5 ou 8) como `qtd_ebooks`.
Se o operador selecionar "Other" em qualquer pergunta, use o valor livre fornecido,
respeitando os limites: refs 5-20, artigos 1-5, ebooks 1-10, tamanho P/M/G/GG/XG,
senioridade: iniciante/intermediario/avancado/tecnico,
série: qualquer texto livre (ou `null` se "Não, standalone").

## Passo 2 — Gravar `config_obra.json`

Com o `tipo_obra` já respondido no Passo 1, defina `prefixo = "livros"` (tipo_obra=livro)
ou `prefixo = "tccs"` (tipo_obra=tcc) e crie a pasta física em
`output/<slug>/<prefixo>/` (hub primeiro — REGRA HUB do Passo 0; NUNCA
`output/<prefixo>/<slug>/`). O identificador lógico usado em todas as chamadas
de script deste comando continua sendo `<prefixo>/<slug>` (ex.:
`livros/<slug>`) — é essa string que `dir_obra()` resolve para o caminho físico
correto no hub; não confundir identificador lógico com caminho de criação.

**Capa (Gap 3):** Antes de gravar o config, pergunte em até 4 perguntas, ainda na Rodada 1 ou 2:

| Header | Pergunta | Condição | Opções |
|---|---|---|---|
| Cor | Cor primária da capa (hex) | sempre | Other (#rrggbb) |
| Subtítulo | Subtítulo da obra | sempre | Other (texto livre) |
| Edição | Tag de edição (ex.: v1.0) | sempre | Other (ex.: v1.0) |

No config, os campos `cor_primaria`, `subtitulo`, `edition_tag` são **obrigatórios**
para `tipo_obra=livro` (Gap 3). Sem eles o `gerar-capa.py` usa fallback errado
(cor da série, subtítulo genérico) e a capa sai visualmente divergente do padrão.

Grave `output/<slug>/<prefixo>/config_obra.json` (raiz física da obra dentro do
hub, sem subpasta `esboco/`) no schema:
```json
{
  "tema": "$ARGUMENTS",
  "tipo_obra": "livro | tcc",
  "min_referencias_por_capitulo": 5,
  "tamanho_obra": "P | M | G | GG | XG | null",
  "senioridade_obra": "iniciante | intermediario | avancado | tecnico",
  "serie": "<nome-da-serie> | null",
  "cor_primaria": "#rrggbb",
  "subtitulo": "<subtitulo da obra>",
  "edition_tag": "v1.0",
  "estilo_tecnica": "codigo | hibrido | operacional",
  "gerar_artigos": true,
  "qtd_artigos": 3,
  "gerar_ebooks": true,
  "qtd_ebooks": 5,

  "gerar_playbook": true,
  "gerar_lead_magnets": true,
  "formatos_lm": ["checklist", "armadilhas"],
  "gerar_deck": false,
  "gerar_emails": false,
  "cta_url": "https://exemplo.com/obra",
  "cta_texto": "Quero a obra completa",

  "modo_producao": "obra-unica",
  "obra_raiz": null
}
```

> `modo_producao` aceita `obra-unica` (padrão) ou `cascata`. Em `cascata`,
> preencha `obra_raiz` com `livro` ou `tcc` — a raiz é gerada primeiro e os
> derivados de **compressão/extração** saem dela. Nunca cascateie uma
> **expansão** (TCC → livro): ali o custo é de geração, não de reescrita.
Valide com:
```bash
python scripts/parametros_obra.py <prefixo>/<slug> --validar
```
Se inválido, corrija os valores fora de faixa antes de prosseguir (nunca pergunte de novo — REGRA 3).

## Passo 3 — Gerar o esboço (sem pausa)

3. Invoque `subagente-pesquisador` com o tema. Dossiê em `output/<prefixo>/<slug>/pesquisa/`.
4. Indexe o dossiê: `python scripts/indexar-dossie.py <prefixo>/<slug> --indexar`.
5. Invoque `arquiteto` passando `tipo_obra` e `tamanho_obra` de `config_obra.json` — o
   sumário macro gerado deve respeitar os mínimos de `scripts/parametros_obra.py`
   (tabela `TAMANHOS` para livro; TCC usa 1 "parte" com as seções do framework ACAD
   como "capítulos" — ver `SPEC_TCC.md`).
6. **Validar título do sumário contra quebra de capa (Gap 4):** Após gerar o `sumario_macro.json`,
   rode `validar-capa-texto.py` com o `titulo_obra` e `subtitulo` do sumário:
   ```bash
   python scripts/validar-capa-texto.py --titulo "<titulo_obra>" --subtitulo "<subtitulo>" --tipo livro
   ```
   Se reprovado (>2 linhas ou linha com 1 palavra), encurte o título no `sumario_macro.json`
   (mantenha o título completo em `titulo_obra`; crie/corrija `titulo_capa` se necessário) e
   revalide. Máximo 3 tentativas. **Previne capa com 3 linhas que falha na compilação final.**
7. Se `gerar_artigos=true`: `python scripts/fatiar-obra.py <prefixo>/<slug> --artigos --qtd <qtd_artigos>`
   — particiona o sumário macro em `qtd_artigos` recortes temáticos (1-2 capítulos
   cada, sem sobreposição), cria cada `output/artigos/<slug>--art-NN-<titulo>/` e
   grava `output/<prefixo>/<slug>/derivados.json` (seção `artigos`).
8. Se `gerar_ebooks=true`: `python scripts/fatiar-obra.py <prefixo>/<slug> --ebooks --qtd <qtd_ebooks>`
   — mesmo princípio, cria cada `output/ebooks/<slug>--eb-NN-<titulo>/` e grava a
   seção `ebooks` do mesmo `derivados.json` (preserva a seção `artigos` já gravada).
9. Se `gerar_playbook=true`: `python scripts/fatiar-obra.py <prefixo>/<slug> --playbook`
   — cria o esqueleto em `output/playbooks/<slug>--pbk/`. A extração dos cards só
   roda depois que os capítulos existirem (`/criar-playbook`).
10. `python scripts/colecao.py --sincronizar --slug <prefixo>/<slug>` — registra a
    obra e seus derivados no manifesto `output/colecoes/<serie>.json`.

> Lead magnets, deck e e-mails **não** são fatiados aqui: dependem dos capítulos
> prontos. Ficam registrados no `config_obra.json` e são disparados na Fase 3
> por `/criar-lead-magnet`, `/criar-deck` e `/criar-emails`.

## Passo 4 — Relatório objetivo (REGRA 2, sem metatexto)

Exiba: slug completo (`<prefixo>/<slug>`), tipo de obra, tamanho (se livro),
quantidade de capítulos planejados, quantidade de artigos/ebooks planejados (se
solicitados), e a lista de comandos disponíveis para prosseguir:

```
/produzir-obra-completa <prefixo>/<slug>     — dispara tudo encadeado/paralelo
/criar-livro <prefixo>/<slug>                — só o livro/TCC
/criar-artigo <prefixo>/<slug>               — só os artigos (requer livro-mãe com dossiê+sumário)
/criar-ebook <prefixo>/<slug>                — só os ebooks (requer livro-mãe compilado)
/criar-playbook <prefixo>/<slug>             — só o playbook (extração, ~0 token)
/criar-lead-magnet <prefixo>/<slug> --todos  — família de lead magnets (~0 token)
/criar-deck <prefixo>/<slug>                 — slide deck 16:9 (~0 token)
/criar-emails <prefixo>/<slug>               — sequência de nutrição
/colecao --sincronizar                       — manifesto da coleção
```

Nenhuma pergunta adicional é feita a partir daqui — a esteira é 100% autônoma
(REGRA 3) até a entrega final de qualquer um dos comandos acima.
