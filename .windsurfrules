---
description: Regras, squad e fluxo da Fábrica Agêntica de Publicações — orquestrador para qualquer agente neste diretório.
alwaysApply: true
---

# FÁBRICA AGÊNTICA DE PUBLICAÇÕES — Orquestrador Central

> V5 (coleção): Livro, TCC, Artigo, E-book, Playbook, Lead Magnet, Deck, E-mails.
> Hardlink de `CLAUDE.md`, `.cursor/rules/fabrica-agentica.mdc`, `.windsurfrules`,
> `.clinerules`, `.github/copilot-instructions.md`. Edite apenas este arquivo.
> Junctions: `agentic/` aponta para `.claude/` (portabilidade multi-IDE);
> `.agents/` recebe só `agents/` e `commands/` (ver seção 6).
> Para recriar links após clone: `scripts/setup-links.ps1` (Win) ou `setup-links.sh` (Mac/Linux).

## 0. Economia Severa de Tokens (PRIORIDADE MÁXIMA)

1. **Caveman Ativo:** pensamento telegráfico (3-5 linhas), sem preâmbulos/saudações.
2. **Headroom & RTK:** logs/builds >7 linhas → comprimir (3 topo + 4 fim). EXCEÇÃO: conteúdo em `output/**` e dados de obra NUNCA são comprimidos.
3. **LeanCTX:** grep antes de read em código/config. Limitar leitura por linha.
4. **Delegação Cavecrew:** subagentes comprimidos para buscas/edições extensas (nunca para prosa).
5. **Pandoc+Typst ISENTO:** compilação PDF é liberada e obrigatória. Nenhuma regra de token economy interfere.
6. **Fallback Terminal:** se sandbox bloquear, exibir comandos PowerShell no chat para o usuário rodar.
7. **Soberania do Usuário:** nada é barrado sem confirmação explícita do operador.
8. **Fidelidade de Conteúdo (sobrepõe 2-4):** arquivos em `output/**`, JSONs de estado, e verificações de `auditar-obra.py`/`validar-codigo.py`/`revisor-tecnico` são isentos de compressão — leitura sempre integral.
9. **Busca via Grafo:** usar `.code-review-graph` antes de tools de leitura/busca.
10. **Auto-commit/push:** alterações devem ser commitadas e pushadas para manter grafo atualizado.
11. **UTF-8 no Windows:** todo script Python com `print`/emojis DEVE ter `console_utf8()` (padrão `scripts/tipos_obra.py`) ou `sys.stdout.reconfigure(encoding="utf-8")` — sem isso quebra em cp1252 (ex.: `criar-maquina-vendas.py`).
12. **Personalizar, não só gerar:** a máquina de vendas nasce com copy genérica ("Autor Digital", "centenas de pessoas") — o fluxo `/criar-maquina` exige personalização por nicho (configs + frontend + e-mails + campanhas + README) com gate `grep 'Autor Digital|centenas de pessoas'` (incluindo `campanhas/` do snapshot) retornando vazio.

## 1. Regras Globais

- **R1 (Idioma):** PT-BR estrito em toda comunicação e artefatos.
- **R2 (Silenciamento):** sem preâmbulos/saudações nos artefatos. Markdown limpo.
- **R3 (Autonomia):** após tema definido, fábrica roda 100% autônoma.
- **R4 (Auto-correção):** desvios são corrigidos internamente antes da compilação.
- **R5 (Capa 2D Plano):** Livro/E-book usam padrão 2D plano (detalhes em `docs/referencia-capa-design.md`). TCC/Artigo usam capa ABNT sóbria. Badge de nível OBRIGATÓRIO (validado por `validar-capa-nivel.py`).
- **R6 (Modelo Livre):** nenhum modelo LLM fixo. `model: inherit` em todos os agents.
- **R16 (Pós-implementação — nunca commitar vermelho):** APÓS TODA nova implementação: (1) rodar a suíte de testes necessária (`python -m pytest -q`, ou a suíte específica + a completa); (2) **100%** → commit + push; (3) **<100%** → analisar a falha, corrigir o código, re-testar até 100% (nunca commitar suíte vermelha; nunca contornar o teste para fazê-lo passar — corrigir a causa). Vale para qualquer agente/sessão da fábrica, incluindo reescrita de materiais.
- **R17 (CAMPANHA e MÁQUINA são OPCIONAIS — REGRA INTOCÁVEL):** a geração de CAMPANHA (V5.3) e de MÁQUINA de vendas NUNCA é obrigatória no fluxo. (1) Na entrevista inicial (`/esbocar`), o operador escolhe explicitamente se quer incluir a etapa CAMPANHA e/ou a etapa MÁQUINA no fluxo daquela coleção (persistido em `config_obra.json`: `gerar_campanha`, `gerar_maquina`); `/produzir-obra-completa` respeita essa escolha e PULA o fluxo correspondente quando `false`, sem tratar como falha. (2) Independente da escolha na entrevista, o operador pode disparar CAMPANHA ou MÁQUINA a qualquer momento para uma coleção JÁ EXISTENTE (`/campanha`, `/campanha-completa`, `/criar-maquina`). (3) Se já existir CAMPANHA ou MÁQUINA para aquela coleção, o sistema SEMPRE oferece ao operador a escolha entre: **Criar Nova** (versiona a existente — a existente é preservada, a nova criação passa a ser a atual) ou **Sobrescrever Existente** (substitui a existente no lugar). Nunca decidir isso silenciosamente — a escolha é sempre do operador.

### Tipos de Obra (V5) — registro declarativo em `scripts/tipos_obra.py`

| Tipo | Natureza | Custo LLM | Spec | Comando | Produtor |
|---|---|---|---|---|---|
| Livro | geração | alto | `SPEC.md` | `/criar-livro` | `redator-eita` |
| TCC | geração | alto | `SPEC_TCC.md` | `/criar-tcc` | `redator-academico` |
| Artigo | compressão | baixo | `SPEC_ARTIGO.md` | `/criar-artigo` | `redator-academico` |
| E-book | compressão | baixo | `SPEC_EBOOK.md` | `/criar-ebook` | `redator-ebook` |
| Playbook | extração | **zero** | `SPEC_PLAYBOOK.md` | `/criar-playbook` | `extrair-passos-praticos.py` |
| Lead Magnet | extração | **zero** | `SPEC_LEAD_MAGNET.md` | `/criar-lead-magnet` | `gerar-lead-magnet.py` |
| Deck | extração | **zero** | `SPEC_DECK.md` | `/criar-deck` | `gerar-deck.py` + `gerar-deck-html.py` |
| E-mails | extração | baixo | `SPEC_EMAILS.md` | `/criar-emails` | `gerar-sequencia-emails.py` |

**Motores de saída:** Pandoc→Typst é o padrão. Duas exceções onde o design vem
de CSS: **lead magnet** (`gerar-lead-magnet-pdf.py`) e **deck**
(`gerar-deck-html.py`), ambos HTML+CSS→Chromium.

O HTML é camada **intermediária** no lead magnet (entregável = PDF) e
**entregável** no deck (apresenta no navegador, offline). PPTX do deck existe via
`gerar-pptx.py`, mas fora do pacote.

**Nomenclatura curta (V5.1):** `output/<raiz>/<código-obra>/<pfx>-<seq>-<nome>/`.
Caminhos caíram de ~197 para ~150 chars (MAX_PATH do Windows = 260). Vale para os
tipos V5; artigo/e-book mantêm o nome V4 para não orfanar artefatos já compilados.
Regras em `scripts/nomes_curtos.py`.

**Adicionar um tipo novo = 1 entrada em `scripts/tipos_obra.py`.** Os 6 pontos de
dispatch (`parametros_obra`, `fatiar-obra`, `auditar-obra`, `gerar-capa`,
`metadados_livro`, `compilar-para-pdf`) consultam o registro — não se edita mais
6 arquivos por tipo. Matriz: `python scripts/tipos_obra.py --matriz`.

**Regra de derivação:** cascateie onde **comprime**, faça fan-out onde **expande**.
Compressão/extração são baratas; expansão (ex.: TCC → livro) custa geração.

### COLEÇÃO

Conjunto de todos os artefatos derivados de um mesmo **núcleo canônico**
(dossiê + `sumario_macro` + `motivo_condutor`), compartilhando identidade visual,
vocabulário condutor, badge de nível e CTA. Manifesto derivado em
`<obra>/colecoes/<nome>.json` — o hub da coleção (`scripts/colecao.py
--sincronizar`, comando `/colecao`). O fallback plano `output/colecoes/<nome>.json`
só existe quando nenhum hub foi criado (comportamento atual de `colecao.py`).

**Nenhum arquivo ou pasta gerado usa prefixo `_`** — em glob de shell, listagem
de nuvem e empacotamento ele é tratado como oculto. Caminhos legados são migrados
automaticamente (`nomes_curtos.migrar_prefixo_underscore`).

## 2. Squad

### Skills Editorial
`pesquisador` (F1) → `arquiteto` (F1) → `estrategista` (F2) → `redator-eita`/`redator-academico`/`redator-ebook` (F2) → `revisor-tecnico` (F2.5) → `compilador-abnt`/`compilador-tcc`/`compilador-artigo` (F3)

### Subagentes (`.claude/agents/`)
`subagente-pesquisador`, `subagente-redator-capitulo`, `subagente-redator-secao-tcc`, `subagente-redator-artigo`, `subagente-adaptador-ebook`, `subagente-revisor-tecnico`, `subagente-ilustrador`

### Scripts Determinísticos
`indexar-dossie.py` (RAG), `pool-capitulos.py` (lotes), `renderizar-diagramas.py`, `validar-codigo.py`, `auditar-obra.py`, `metadados_livro.py`, `parametros_obra.py`, `validar-abnt-tcc.py`, `fatiar-obra.py`, `gerar-epub.py`, `pdf_typst.py`, `series_capa.py`, `validar-capa-texto.py`, `validar-capa-nivel.py`

**V5:** `tipos_obra.py` (registro de tipos), `secoes_eita.py` (parser EITA canônico), `colecao.py`, `extrair-passos-praticos.py`, `validar-playbook.py`, `gerar-lead-magnet.py`, `validar-lead-magnet.py`, `gerar-deck.py`, `validar-deck.py`, `gerar-sequencia-emails.py`, `validar-emails.py`, `gerar-lead-magnet-pdf.py`, `gerar-pptx.py`, `gerar-deck-html.py`, `nomes_curtos.py`, `validar-artefatos.py`, `empacotar-colecao.py`

**V5.4 (pesquisa acadêmica — custo LLM zero):** `fontes_academicas.py` (registro declarativo das bases com API aberta: OpenAlex, Crossref, arXiv, Semantic Scholar, SciELO, PubMed — adicionar fonte = 1 entrada) e `minerar-fontes-academicas.py <tema> --slug <obra>` (mineração determinística via APIs, dedup por DOI, gera `pesquisa/mineracao_academica_<slug>.json/.md` já em ABNT classe (A), cache local + `--sem-rede`).

**Gates de conteúdo (F1/F2 — mérito, além da estrutura R1-R15):** `validar-referencias.py` (R-RF: URL/DOI reais, 4xx/DNS reprova, cache + `--sem-rede`), `validar-metricas.py` (R-MT: ≥1 métrica com valor+unidade+citação por capítulo; `metricas_obrigatorias` no sumário), `validar-escala.py` (R-ES: limites/contorno na seção Aplica), `validar-afirmacoes.py` (R-AF: dado factual sem `[N]` no parágrafo reprova), `validar-fontes.py` (R-FT: hierarquia A/B/C do dossiê ≥70% A+B), `validar-comandos-cli.py` (R-CLI: bloco de código/CLI marcado `<!-- cli-check: fonte=A|B|C; confere=false -->` reprova — opt-in via `config_obra.json:categoria_tecnica`, livros sobre ferramentas/CLIs/frameworks; sem marcação vira pendência, nunca reprova sozinho). `validar-codigo.py --executar` (smoke test real de python/js/bash) e `--playbook` (gate dos cards vira comando executado). Registrados em `tipos_obra.py` → campo `gates_conteudo` do tipo `livro`; `auditar-obra.py --estrito` os encadeia (referências offline).

### Token Economy Skills
`lean-ctx`, `headroom`, `caveman`, `rtk-memory`, `pre-flight-check`, `calcular-gastos-sessao`

### Fable Skills
`fable-method`, `fable-domain`, `fable-judge`, `fable-loop`, `self-learning`

## 3. MCPs

- `db_state` (SQLite) — estado da esteira
- `file_writer` — grava Markdown
- `mcp_deep_search` → `WebSearch`/`WebFetch` nativos
- `pdf_gen` (fallback CloudConvert) — método principal: Pandoc+Typst via `compilar-para-pdf.py`

## 4. Templates

`templates/template.typ` (Livro ABNT), `template_tcc.typ` (TCC NBR 14724), `template_artigo.typ` (Artigo NBR 6022), `template_eita.md` (molde EITA-V2), `template_playbook.typ` (cards de bancada), `template_lead_magnet.html` (A4 + CTA no rodapé), `template_deck.html` (16:9 navegável + PDF)

## 5. Fluxo Operacional

1. **Input:** operador define tema → `/esbocar <tema>`
2. **Fase 1:** pesquisador varre → `minerar-fontes-academicas.py "<tema>" --slug <obra>` (custo zero, APIs abertas) → `indexar-dossie.py --indexar` → arquiteto gera sumário macro
3. **Fase 2:** `pool-capitulos.py --plano --lote 4` → subagentes-redator em lotes (estratégia + redação + diagrama + CI + auto-validação). Retentativa com backoff (máx. 3)
4. **Fase 2.5:** `auditar-obra.py` (encadeia os gates de conteúdo F1/F2 via `gates_conteudo` no `--estrito`) + `validar-codigo.py --executar` + `renderizar-diagramas.py --validar` → `revisor-tecnico` corrige (inclui conferência por amostra: reabrir 1 fonte por capítulo e conferir o dado citado)
5. **Fase 3:** `compilador-abnt` merge + pré/pós-textuais + referências ABNT
6. **PDF:** `compilar-para-pdf.py <slug> --paginas-exatas` → Pandoc→`.typ`→Typst
7. **Fase 4 (V5) — Coleção:** `/criar-playbook` → `/criar-lead-magnet --todos` +
   `/criar-deck` + `/criar-emails` (paralelos) → `colecao.py --sincronizar` →
   `empacotar-colecao.py`. Playbook **antes** dos lead magnets/e-mails.
8. **Entrega:** `validar-artefatos.py --todos --estrito` (testa se cada arquivo
   ABRE) → `empacotar-colecao.py <coleção>`. O pacote leva **só o que está
   finalizado e abre**, com `LICENCA.txt` e `LEIA-ME.md` que declara o que ficou
   de fora e por quê.
9. **Máquina de vendas (V5.3):** `/criar-maquina <slug>` → gera em
   `output/<slug-colecao>/maquina/` (**1 máquina por COLEÇÃO**, regra 1:1; o hub
   é derivado do slug) com **snapshot das campanhas** em `maquina/campanhas/` +
   personalizar por nicho (configs, frontend, e-mails, campanhas, README) +
   testar `POST /api/checkout` (rota nasce no template — verificar que o lead
   chega em `/api/leads/`) + deploy. Legadas em `output/<hub>/marketing/` são
   sinalizadas como `maquinas_legadas` no manifesto da coleção.
   **Checklist mínimo de segurança antes de qualquer deploy em produção**
   (a máquina é o único artefato da fábrica que vira aplicação web exposta —
   os demais são documentos estáticos): (a) **rate limiting** em `/api/checkout`
   e `/api/leads/` (proteção contra spam/abuso do formulário); (b) **não logar
   payload de lead em claro** (nome/e-mail/telefone) em stdout/arquivo de log;
   (c) **HTTPS obrigatório** em produção (nunca servir o checkout em HTTP puro);
   (d) **autenticação no painel de leads/admin** (`/api/leads/` e telas
   administrativas não podem ficar públicas sem login); (e) **política de
   retenção documentada** para `backend/data/vendas.db` (por quanto tempo os
   dados de lead ficam armazenados, e como são expurgados). É responsabilidade
   do operador aplicar essas proteções no momento do deploy — a fábrica não as
   impõe automaticamente, só avisa. Checklist completo em
   `.claude/commands/criar-maquina.md`.
10. **Campanha (V5.3):** `/campanha <slug>` (1 material) ou `/campanha-completa
    [colecao]` (todos os membros do manifesto) → `criar-campanha.py` (estrutura +
    moldes de copy + artes HTML→Chromium + cronogramas; custo zero) → agente
    escreve a copy final nos moldes (LLM baixo) → `validar-campanha.py --estrito`
    (gates R-CP-1..5) → `--marcar-completa`. Vive em
    `output/<colecao>/campanhas/<material>/` + `campanha.json` (hub). Não é tipo
    de obra: camada própria (registro declarativo em `scripts/campanha.py`).

**Output (HUB POR COLEÇÃO):** cada coleção vive em `output/<slug-colecao>/` com
as raízes de tipos **dentro do hub** — `livros/`, `tccs/`, `artigos/`, `ebooks/`,
`playbooks/`, `lead-magnets/`, `decks/`, `emails/`, `distribuicao/` e
`colecoes/<nome>.json` (manifestos). Não existem raízes planas no topo
(`output/livros/` etc.) — ver "Estrutura de Coleções (HUB)" abaixo.
**Nota:** não usar `pandoc --pdf-engine=typst` com figuras (bug de path absoluto Windows). Gerar `.typ` na pasta do livro e chamar `typst compile --root`.

### Estrutura de Coleções (HUB)

O agrupamento padrão da pasta `output/` é o **HUB POR COLEÇÃO**: uma pasta por
coleção (núcleo canônico: dossiê + `sumario_macro` + `motivo_condutor`):
```
output/<slug-colecao>/
├── livros/  tccs/  artigos/  ebooks/  playbooks/  lead-magnets/  decks/  emails/
├── campanhas/<material-slug>/  # Campanhas (V5.3): redes-sociais + canais-comunicacao
├── distribuicao/            # PDFs compilados para distribuição
├── maquina/                 # 1 máquina de vendas por coleção (Next.js+FastAPI)
├── campanhas/               # artefatos de campanha (textos, artes, cronogramas)
└── colecoes/<nome>.json     # Manifestos sincronizados (colecao.py --sincronizar)
```
Suportado por `tipos_obra.py` (`_sereis`, `dir_obra`, `listar_materiais`,
`_obra_raiz`) e `colecao.py` (`_dir_colecoes` prioriza `<obra>/colecoes/`).

**Glossário de nomenclatura:** **coleção = hub** (unidade de organização da
pasta `output/`); **série = termo obsoleto**, preservado apenas como nome
interno de compatibilidade do registro de cores `output/series.json` (não
renomear: as cores persistidas e a migração de `_series.json` dependem do nome).

### Entrega de Sessão (V5.2) — `relatorios/`

Toda sessão de trabalho na fábrica deve encerrar com um **relatório em
`relatorios/`** (raiz do projeto), em **MD + PDF** (Pandoc→Typst):

```
relatorios/<YYYY-MM-DD>-<tema-da-sessao>.md
relatorios/<YYYY-MM-DD>-<tema-da-sessao>.pdf
```

Conteúdo mínimo: contexto, bugs descobertos/corrigidos (causa→fix), arquivos
alterados, validações (testes/verificações rodadas), commits feitos e resumo
de entregas. O relatório é commitado e pushado junto com o trabalho da sessão.

## 6. Portabilidade Multi-IDE

Fonte: `.claude/`. Junctions: `agentic/*`, `.opencode/{agents,commands,skills,mcp-servers,settings.json}` e `.agents/{agents,commands}` → `.claude/*`. **`.agents/` recebe apenas `agents/` e `commands/` (somente `.md`)** — nunca `skills/` nem `mcp-servers/`: `.agents/` é o diretório de agentes do Codebuff/Freebuff, que **importa e executa** os `.js`/`.mjs` encontrados ali dentro; `compilar-livro.mjs` roda no import, imprime o USO e chama `process.exit(1)`, derrubando o CLI. Skills e MCP servers continuam expostos via `agentic/` e `.opencode/`. Hardlinks: `AGENTS.md`→`CLAUDE.md`, `.cursor/rules/`→`CLAUDE.md`, `.cursor/mcp.json`→`.mcp.json`. Schemas MCP que diferem são GERADOS por script (não link): `.vscode/mcp.json` via `scripts/sincronizar-mcp-vscode.mjs`, `opencode.json` via `scripts/sincronizar-mcp-opencode.mjs` (preserva `instructions`/`permission`/chaves manuais por merge; sobrescreve só o bloco `mcp`). Hooks do OpenCode vivem em `.opencode/plugins/fabrica-hooks.ts` (versionado; espelha `.claude/settings.json` — junction de `settings.json` só serve o schema do plugin, que o OpenCode lê além do `settings.json`). Hook git `pre-commit` (mecaniza R16 — bloqueia commit se `pytest -q` falhar) fonte versionada em `scripts/hooks/pre-commit`, copiado para `.git/hooks/pre-commit` (não é link: `.git/hooks` não aceita hardlink/junction de forma confiável). Recriar após clone: `scripts/setup-links.ps1` (Win) ou `setup-links.sh` (Mac/Linux) — ambos recopiam o hook. Submodule `.claude/mcp-servers/code-review-graph` (fonte vendorizada de https://github.com/tirth8205/code-review-graph.git, só leitura/referência — o MCP server em si roda via `uvx code-review-graph serve` do PyPI, `.mcp.json` não aponta pro submodule); clonar com `git clone --recurse-submodules` ou rodar `git submodule update --init --recursive` depois.

## 7. RTK SCRATCHPAD

> Aprendizados de sessões anteriores: ver `RTK-SCRATCHPAD.md` (arquivo externo na
> raiz do projeto, migrado em 21-08-2026 — item D de
> `melhorias/21-08-2026-plano-acao-tokens-sob-pericia.md` — para manter este
> arquivo estável como prefixo de cache). Não lido automaticamente pelo agente;
> consultar sob demanda. Novas entradas: SEMPRE appendar em `RTK-SCRATCHPAD.md`,
> nunca aqui.

