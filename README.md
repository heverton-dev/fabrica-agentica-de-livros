# Fábrica Agêntica de Publicações

Orquestrador central para produção de coleções completas de publicações técnicas
com automação agêntica: **Livro, TCC, Artigo, E-book, Playbook, Lead Magnet,
Deck e E-mails** derivados de um mesmo núcleo canônico (dossiê + sumário macro +
motivo condutor), compartilhando identidade visual e vocabulário condutor.

## Tipos de obra

| Tipo | Natureza | Comando |
|---|---|---|
| Livro | geração (alto custo) | `/criar-livro` |
| TCC | geração (alto custo) | `/criar-tcc` |
| Artigo | compressão (baixo custo) | `/criar-artigo` |
| E-book | compressão (baixo custo) | `/criar-ebook` |
| Playbook | extração (custo zero) | `/criar-playbook` |
| Lead Magnet | extração (custo zero) | `/criar-lead-magnet` |
| Deck | extração (custo zero) | `/criar-deck` |
| E-mails | extração (baixo custo) | `/criar-emails` |

## Fluxo operacional

1. **Entrada:** `/esbocar <tema>` define o tema da coleção.
2. **Fase 1 — Pesquisa:** mineração de fontes acadêmicas (OpenAlex, Crossref,
   arXiv, Semantic Scholar, SciELO, PubMed) com custo LLM zero; indexação do
   dossiê via RAG e sumário macro produzido pelo arquiteto.
3. **Fase 2 — Manufatura:** capítulos/seções produzidos em lotes por subagentes
   (estratégia + redação + diagrama + CI + auto-validação), com revisor técnico
   em peer review.
4. **Fase 3 — Compilação:** merge dos capítulos aprovados, pré/pós-textuais e
   referências no padrão ABNT.
5. **PDF:** Pandoc → Typst (padrão); HTML+CSS → Chromium para lead magnet e deck.
6. **Fase 4 — Coleção:** playbook, lead magnets, deck e e-mails em paralelo;
   sincronização do manifesto e empacotamento.
7. **Extras opcionais:** máquina de vendas (1 por coleção, `/criar-maquina`) e
   campanhas de marketing (`/campanha`), conforme escolha do operador na
   entrevista inicial.

## Estrutura de saída (hub por coleção)

```
output/<slug-colecao>/
├── livros/  tccs/  artigos/  ebooks/  playbooks/  lead-magnets/  decks/  emails/
├── campanhas/
├── distribuicao/
├── maquina/
└── colecoes/<nome>.json
```

## Regras principais

- **R1:** comunicação e artefatos sempre em PT-BR.
- **R2:** markdown limpo, sem preâmbulos.
- **R3:** após o tema definido, a fábrica roda de forma autônoma.
- **R5:** livros/e-books usam capa 2D plana com badge de nível; TCC/artigo usam
  capa ABNT sóbria.
- **R16:** nunca commitar com a suíte de testes vermelha (bloqueado por hook
  `pre-commit`).
- **R17:** campanha e máquina de vendas são opcionais e nunca obrigatórias.

## Documentação

O orquestrador completo (squad, scripts, MCPs, templates, portabilidade
multi-IDE e RTK) está no `AGENTS.md` na raiz do projeto.