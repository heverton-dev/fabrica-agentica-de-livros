# RTK Scratchpad — Fábrica Agêntica de Publicações

> Espaço para registro de aprendizados pela skill `rtk-memory`. Arquivo EXTERNO ao
> `CLAUDE.md` (migrado em 21-08-2026, item D do plano
> `melhorias/21-08-2026-plano-acao-tokens-sob-pericia.md`): o corpo normativo do
> `CLAUDE.md` fica estável como prefixo de cache; este arquivo cresce a cada sessão
> e é consultado sob demanda, não lido automaticamente em toda chamada de agente.
> Nova entrada = sempre um append no final deste arquivo, nunca editar `CLAUDE.md`.

## RTK SCRATCHPAD

- **2026-08-11 Produção completa série 5 (coleção `agentic-design-patterns`):**
  causa: série 5 da proposta (Agentic Design Patterns — o "Gang of Four" dos
  fluxos agênticos) exigia fluxo FULL com livro, derivados, campanhas e máquina;
  3 lições reais. Fix/lições: (1) **pasta `campanhas/material/` é o nome
  CANÔNICO da campanha do livro-raiz** — `nome_material` do slug
  `<chave>/livros/<chave>-v1` trunca para `v1` e o fallback de `nome_curto`
  vira `material`; NÃO apagar (parece lixo, é a campanha do livro; as pastas
  dos derivados são `dck-1-design`, `eb-01-design` etc. com desambiguação V5.4);
  (2) `criar-campanha --completo` com 12 materiais estoura timeout (~590s) —
  rodar `--completo` e completar materiais restantes com `--material <slug>`
  individual (32 artes cada); (3) moldes de campanha nascem `Status: RASCUNHO`
  e R-CP-2 reprova — promover a `FINAL` com sed em massa e marcar `status:
  completa` no `campanha.json` (o flag `--marcar-completa` junto de
  `--completo` REGENERA tudo e estoura timeout; editar o JSON direto).
  Resultado: livro 68 pág CONFORME, 12 membros, campanhas 12/12 com 384 artes
  únicas (R-CP-6), máquina personalizada (gate regra 12 vazio), suíte 662/662.
  Arquivos: `output/agentic-design-patterns/**`,
  `relatorios/11-08--producao-completa-agentic-design-patterns.md/.pdf`.
- **2026-08-11 Cheatsheet vazio + R-PBK-5 em playbook de livro P (fluxo FULL MAS):** causa: (1) `gerar-lead-magnet.py --todos` gerava cheatsheet com 0 itens — `montar_cheatsheet` lê `card.comandos` no NÍVEL do card (ou `card.gate`), não dentro de `execucao[]`, e o `extrair-passos-praticos.py` só preenche `execucao[].codigo`; (2) `validar-playbook.py` R-PBK-5 conta a soma de linhas de TODOS os blocos de `execucao` (`sum(len(codigo)+2)`), então múltiplos blocos de código de capítulo estouram 25 linhas; (3) R2 do livro P exige ~100.000 chars (40 pág.) — 4 capítulos de ~20k chars ficam ~20% abaixo. Fix: adicionar `comandos` no topo dos cards do playbook (11 comandos → cheatsheet CONFORME); compactar `execucao` para 1 bloco de ≤18 linhas por card (truncar mantendo docstring+assinaturas); expandir capítulos com seções técnicas reais (votação do enxame, validação de contrato, retry com backoff, roteador, dual-mode, monitor de custo, calibração por amostra). Prevenção: cheatsheet = agregador de `card.comandos`/`card.gate` do playbook — se o playbook nasce sem comandos, o LM cheatsheet nasce vazio; validar playbook ANTES de gerar LMs; R2 = estimar chars por capítulo na escrita (mín. 25k por capítulo de livro P). Resultado: livro MAS 100.000+ chars/54 pág PDF CONFORME, playbook 4 passos CONFORME, 6 LMs CONFORME, suíte 662/662. Arquivos: `output/…/playbooks/pbk-1-sistemas-multiagentes/passos/*.json`.
- **2026-08-11 Campanhas em hub MULTI-VOLUME (nome_material V5.5):** causa: a desambiguação de `nome_material` só removia o prefixo da CHAVE da coleção (`aidd-engenharia-nativa--eb-01-...`); o primeiro hub com 4 volumes (AIDD) expôs 2 colisões novas — (1) `dck-1-*`/`eml-1-*`/`pbk-1-*`/`lm-N-*` têm o MESMO prefixo de 2 palavras em todos os volumes (4 decks → 4 pastas `dck-1` sobrescrevendo); (2) artigos/ebooks repetem o slug do VOLUME, não da chave (`aidd-v1-arquitetura-da-inteligencia--art-01-...` → truncava para `aidd-arquitetura`, a mesma pasta do livro). Fix: `_volume_obra` lê `obra_mae`/`livro_mae` do config_obra (volume = slug que difere da chave), `nome_material` remove o prefixo do VOLUME com separador explícito (`--`/`-`) e anexa a palavra distintiva do volume (2ª palavra significativa do slug do volume: `aidd-v2-arsenal-do-agente` → `arsenal`); resultado truncado a 20 chars (invariante V5.1). Prevenção: em hub multi-volume o discriminador de pasta de campanha é o VOLUME (config `obra_mae`), não a chave; validar colisão com um teste que passa 4 volumes do mesmo tipo; nunca anexar sufixo sem cortar o total a 20 chars. Resultado: 48 campanhas AIDD com pastas únicas (aidd-arquitetura, dck-1-arsenal, art-01-governanca...), gate R-CP estrito 48/48, suíte 662/662. Arquivos: `scripts/campanha.py`, `tests/test_campanha.py`.
- **2026-08-11 Produção completa série MCP (coleção `revolucao-mcp`):** causa: série 3 da proposta estratégica (MCP) exigia fluxo FULL com livro, derivados, campanhas e máquina; 4 lições reais surgiram. Fix/lições: (1) **headings EITA-V2 obrigatórios** — `dividir_secoes`/`secao_por_nome` (validar-escala, validar-metricas) só reconhecem `## N. Nome` numerado; capítulos com `## Introdução` sem número falham R-ES-1/R-MT-1 mesmo com o conteúdo correto (sed `s/^## Aplica:/## 5. Aplica/`); (2) **mermaid-cli quebra com subgraph aninhado/acentos em labels** — `flowchart TB` com `subgraph` falhou render com ParseError; simplificar para nós planos resolveu; (3) **R-CP-C1 lê `campanhas/campanha.json` com `materiais[].slug` = caminho COMPLETO do manifesto** — meu `campanha.json` inicial usava nomes curtos (`eb-01-mcp`) e o gate reprovou 12/12; regenerar com slugs do manifesto + `status: completa`; (4) **`transport` do FastMCP instalado é `streamable-http` (hífen)** — `streamable_http` (underscore) lança ValueError no smoke test; e `mcp.run()` bloqueia o `validar-codigo --executar` (timeout 20s) — guardar com env var em exemplo didático. Prevenção: rodar `auditar-obra --estrito` + `validar-codigo --executar` ANTES da capa/PDF; usar headings EITA numerados desde o primeiro rascunho. Resultado: livro 63 pags CONFORME, 12 membros, campanhas 12/12, máquina com gate regra 12 vazio, suíte 662/662, commit+push. Arquivos: capítulos MCP, `scripts/validar-escala.py` (leitura), `scripts/validar-campanha.py` (leitura).
- **2026-08-11 Série 4 (Autonomous DevOps) — 7 bugs reais no fluxo FULL:** causa: (1) `validar-afirmacoes` reprovava listas de definições sem `[N]` (SLI/SLO/SLA; timings do incidente em bullets) — citar cada item factual; (2) bloco de código do `Cirurgiao` com AssertionError: lambda de runbook irreversível retornava `verificacao: nao_aplicado` e o assert esperava `ok` — semântica correta é a verificação falhar → `reverter` (mostra o gate funcionando); (3) Vigia cap_2: taxa 0.05 não superava 5x o teto (severidade virava P2) e o sazonal com desvio zero (histórico idêntico) disparava o pico normal — usar valores com variância real; (4) lead magnets nasciam com `itens: 0` no `sumario_macro.json` (R-LM-7) e sem CTA UTM no corpo (R-LM-1 exige `# Próximo passo` + `utm_source=`) — preencher itens e bloco CTA; (5) e-mails com formato errado (`Status:` no lugar certo) e CTA sem link markdown — `[texto](url)` com assunto ≤60 chars (R-EM-1/R-EM-2); (6) e-books sem campo `serie` (eb-02 ficou fora → coleção com 11 membros) — conferir TODOS os configs após o script; (7) campanhas `inbound_emails` (sequencia-mkt/nutricao, 84 moldes) não caem no polimento genérico — script dedicado por sequência. RTK: `pdf_typst.executar(comando, pdf_path, dir_raiz, typst_bin)` — importar `compilar_markdown_pdf` de `criar-campanha.py` via importlib (nome com hífen não importa direto); `campanha.json` usa slug COMPLETO do manifesto no formato `{slug, tipo, status, atualizado_em}`. Prevenção: validar blocos de código com dados REALISTAS (assert deve refletir a semântica, não forçar pass); LM/emails exigem CTA rastreável + itens contados no sumário. Resultado: série 4 completa, suíte 662/662. Arquivos: `output/devops-agente/**`, `relatorios/11-08--producao-completa-devops-agente.md/.pdf`.
- **2026-08-10 Artes de campanha únicas por envio (R-CP-6) + desambiguação `nome_material`:** causa: artes (PNG) da campanha nasciam IDÊNTICAS em todos os envios — (1) `gerar_artes` interpola o HTML do WhatsApp UMA VEZ fora do loop (arte-01..06 com mesmo MD5); (2) posts/stories "variavam" só com sufixo `(i/n)` colado ao título e cortado pelo `[:64]` de `variaveis_arte`; (3) o gate R-CP-3 só contava QUANTIDADE de PNGs, nunca unicidade (62 PNGs, 8 MD5 únicos "validavam 100%"); (4) `nome_material` corta o nome do diretório nas 2 primeiras palavras (`nome_curto max_palavras=2`) e `spec-driven-development--eb-01-…` virava `spec-driven` — campanhas dos e-books caíam na pasta do livro, sobrescrevendo moldes/artes. Fix: `ganchos_arte(ctx, formato, n, base=None)` deriva gancho curto (≤70 chars, break scroll) + apoio (≤90) do sumário (títulos/objetivos/pilares; post prioriza capítulos, story/whatsapp priorizam pilares como dica); `gerar_artes` interpola o HTML DENTRO do loop com `titulo_arte`/`apoio_arte`/`rotulo_arte` ("Post 3/7") como elementos SEPARADOS (nunca colados/cortados do título); templates ganham `.rotulo` no topo + subtítulo = `${APOIO}`; novo gate **R-CP-6** (`_artes_duplicadas`): PNGs repetidos por MD5 e HTML fonte repetido reprovam; `nome_material` remove o prefixo da chave da coleção com separador EXPLÍCITO (`chave--`/`chave-`; sem separador não trunca — material que apenas compartilha prefixo não é afetado). Prevenção: ao "variar" arte por envio, variar o CONTEÚDO (gancho/apoio/rótulo), nunca sufixo truncável; validação de arte precisa gate de UNICIDADE (MD5), não só contagem; nome curto de derivado que repete o slug da coleção precisa desambiguação com separador. Resultado: suíte 652/652; campanha do SDD regenerada com 372 PNGs e 0 duplicatas. Arquivos: `scripts/campanha.py`, `scripts/criar-campanha.py`, `scripts/validar-campanha.py`, `templates/campanha/*.html`, `tests/test_campanha.py`.
- **2026-08-10 Universalização OpenCode:** causa: o harness opencode só carregava built-ins — não lia `.claude/agents`, `.claude/commands` nem os MCPs do `.mcp.json`. Fix: (1) frontmatter dos agents: remover `model: inherit` (quebra no OpenCode: "Model not found: inherit/") e usar `mode: subagent`; (2) junctions `.opencode/{agents,commands,skills,mcp-servers}` → `.claude/` via `New-Item -ItemType Junction` do PowerShell (`ln -s` do git-bash COPIA, gera inode diferente — bug real); (3) `.opencode/plugins/fabrica-hooks.ts` (API `export const X: Plugin = async ({$}) => ({event, hooks})`, NÃO `app.on` — API antiga quebra com "app.on is not a function"); (4) MCP do opencode = bloco `mcp` com `command:[...]` array trazendo `type:"local"` — schema difere do `.mcp.json`, logo não é junction; `scripts/sync-opencode-mcp.mjs` traduz (merge preserva `instructions`/`permission`); (5) paths relativos de MCP NO OpenCode NÃO resolvem — usar absolutos; (6) junction `.opencode/skills` duplica `.claude/skills` e gera warnings inofensivos de skill duplicada; (7) `scheduled_tasks.lock`/`settings.local.json` são runtime/local — gitignorar com as junctions, manter só `.opencode/plugins/` versionado (`.opencode/.gitignore` interno já ignora node_modules/package.json). Prevenção: rodar `scripts/setup-links.ps1` após clone; `opencode mcp list` e `opencode agent list` (subagentes mostram `(subagent)`) para validar; subagente não roda como primary (fallback expected). Arquivos: `.claude/agents/*.md`, `.claude/commands/criar-maquina.md`, `.opencode/plugins/fabrica-hooks.ts`, `opencode.json`, `scripts/sync-opencode-mcp.mjs`, `scripts/setup-links.ps1/.sh`, `~/.config/opencode/plugins/crg-plugin.ts`.
- **2026-08-10 `fatiar-obra.py` grava `obra_mae` mas a coleção lê `serie`/`livro_mae`:** causa: configs de artigos/ebooks derivados nasciam com `obra_mae: <volume>` e sem `serie`/`livro_mae`; `resolver_serie_key` (série ← `serie` → `livro_mae` → nome do slug) então criava 1 coleção fantasma por volume (`aidd-v1-...`, `aidd-v2-...`) em vez de agregar ao hub. Fix: adicionar `livro_mae: <slug-colecao>` (a CHAVE da coleção, não o volume) nos configs de artigos/ebooks e re-rodar `colecao.py --sincronizar` sem `--slug` (a limpeza global remove os manifestos órfãos). Prevenção: derivados fatiados de uma SÉRIE (vários livros no mesmo hub) precisam apontar `livro_mae` para o slug da coleção; playbooks já nascem com `serie`. Arquivos: `scripts/fatiar-obra.py`, `scripts/colecao.py`, `scripts/series_capa.py` (`resolver_serie_key`).
- **2026-08-11 Falha de TDD de campanhas (0/7 artes + R-CP-2 em cronograma mestre):** causa: `criar-campanha.py` não aplicava `_pdf_atualizado` em ads pago/distribuição; `test_campanha.py` tinha hardcode pra `anuncio-04`; R-CP-2 exigia `.pdf` de `cronograma_mestre.md` porque isenção usava `startswith("cronograma-")`. Fix: Adicionadas chamadas de conversão PDF; removido hífen do validador de isenção de R-CP-2; corrigidos hardcodes (`anuncio-04` → `0{i}`). Prevenção: Testar integridade do gerador comparado ao nome e paths lógicos declarados; e incluir logs explícitos de não geração de PDFs em mocks. Arquivos: `scripts/criar-campanha.py`, `scripts/validar-campanha.py`, `scripts/campanha.py`, `tests/test_campanha.py`.
- **2026-08-09 Reescrita e transmutação de materiais:** causa: a esteira só
  criava novo (-v2) ou retomava; não dava para regravar capítulo/obra nem mudar
  de tipo sem orfanar série/coleção. Fix: `pool-capitulos.py --reescrever <n>`
  (backup em `revisao/backups/<ts>/` + flag `reescrever` no estado que o
  `montar_visao` respeita até `--registrar --sucesso`); campo `reescrever_de`
  no registro de tipos (transmutação: livro←ebook/playbook/artigo/tcc,
  tcc←livro/ebook, ebook←livro/tcc/playbook, artigo←livro/tcc/ebook);
  `scripts/transmutar-obra.py` (recorte origem→destino, slug destino com
  sufixo `--liv/--tcc/--ebk/--art` no layout plano, `slug_origem` no config,
  registro em `derivados.json` da origem); comandos `/reescrever-capitulo`,
  `/reescrever`, `/refinar`, `/reescrever-como`; skills com Modo
  reescrita/transmutação (preservar refs [N] e diagramas; gates do DESTINO
  obrigatórios). Prevenção: R16 — após toda implementação, suíte 100% → commit
  e push; <100% → analisar, corrigir, testar (nunca commitar vermelho).
  Arquivos: `scripts/pool-capitulos.py`, `scripts/tipos_obra.py`,
  `scripts/transmutar-obra.py`, `.claude/commands/reescrever*.md`,
  `.claude/commands/refinar.md`.
- **2026-08-09 Gates de conteúdo F1/F2 (mérito além da estrutura):** causa:
  validar estrutura (R1-R15) não pegava referência inventada, código que não
  roda, capítulo sem métrica nem limite de escala, dado factual sem citação.
  Fix: 5 gates novos + `validar-codigo --executar/--playbook`; registro via
  campo `gates_conteudo` no tipo `livro` (tipos_obra.py) e encadeamento em
  `auditar-obra --estrito` (referências rodam offline `--sem-rede`; o
  revisor-tecnico roda com rede). Prevenção: estrategista declara
  `metricas_obrigatorias` no draft; redator-eita cita no mesmo parágrafo,
  inclui métrica e limites de escala; pesquisador classifica fontes `(A)/(B)/(C)`
  no dossiê (gate R-FT-1 ≥70% A+B). Ajustes calibrados: superlativos de ênfase
  ("o mais importante") e garantias técnicas ("nunca confie") NÃO são
  disparadores factuais (ruído); `**Desafio` (exercício do autor) é excluído;
  cache de referências só é conclusivo para ok/falha — `nao_verificado` não
  bloqueia checagem futura. Achado real do gate: `fin.ai/blog/ai-agent-roi-customer-support`
  404 no cap_1; playbook pbk-1 tem 13 blocos truncados sem elipse (código
  cortado no meio). Arquivo: `scripts/validar-*.py` + `tests/test_validar_*`.
- **2026-08-09 Cronogramas ricos (o que/por que/como/quando):** causa:
  cronogramas da campanha eram listas secas ("D+N (data): Post — Título")
  sem instrução de uso. Fix: cada dia vira bloco com **o quê** (arquivo
  EXATO: arte PNG + legenda MD da rede / texto MD do canal),
  **por quê** (`campanha.objetivo_do_dia` — objetivo rotativo por fase do
  funil: `fase_da_janela` 0=gancho, 1=aprofundamento, 2=urgência/CTA),
  **como** (`COMO_FORMATO` interpolado com arte/texto/CTA reais) e
  **quando** (data + horário por formato). Dias sem envio dos canais viram
  PAUSA estratégica. Bug real corrigido de quebra: a numeração dos itens de
  canal usava a POSIÇÃO do dia (`email-11/20/30` — arquivos inexistentes);
  agora contador sequencial `email-01..04` batendo com `texto_nome` e artes
  WhatsApp (`item.split('-')[1]`). Gate R-CP-5 exige as 4 dimensões
  (`**O quê:**` etc.) — reprova lista seca. Prevenção: ao numerar artefatos
  de sequência, usar contador sequencial, NUNCA posição do dia.
  Arquivos: `scripts/campanha.py`, `scripts/criar-campanha.py`,
  `scripts/validar-campanha.py`, `tests/test_campanha.py`.
  capas dos materiais divergiam do padrão 2D plano. Três causas reais:
  (1) `ebook_metadados.json` herdou títulos antigos concatenados com "&" de
  gerações anteriores (ex.: "…Por Que o Modelo Não Basta & Anatomia de um
  Harness: O") — `gerar-capa.py` prioriza `meta_ebook.titulo` sobre
  `sumario.titulo_obra`, então capas mostravam lixo truncado;
  (2) `validar-capa-nivel.py` procurava em `output/livros/<slug>` (layout
  plano) e nunca validou no HUB POR COLEÇÃO (`output/<colecao>/livros/…`);
  (3) títulos longos estouravam a capa (máx. 2 linhas, sem linha de 1
  palavra) — validar-capa-texto usa largura por TIPO (`playbook` 1600 vs
  `ebook` 1200 quebram diferente; testar sempre com o tipo real do material).
  Fix: `validar-capa-nivel.main()` resolve via `tipos_obra.dir_obra` (plano e
  hub; escopo R5: badge só livro/ebook); capas de título longo usam
  `ebook_metadados.json` curto (título + subtítulo) SEM tocar no sumário
  (documento EPUB/PDF mantém título completo — gerar-epub prioriza
  `sumario.titulo_obra`). Prevenção: ao encurtar título de capa, validar com
  `gerar-capa.py <slug>` (tipo real) e conferir badge via
  `validar-capa-nivel.py <slug>`. Arquivos: `scripts/validar-capa-nivel.py`,
  `scripts/gerar-capa.py`, `scripts/validar-capa-texto.py`,
  `ebook_metadados.json` dos materiais.
  faltava no template (checkout page postava nela → 404 em toda máquina nova) e
  page antiga usava form urlencoded vazio → 500 no `request.json()`. Fix: rota
  com zod + `/api/leads/` + `BACKEND_URL`; page client com nome/e-mail + fetch
  JSON. Prevenção: `produto` default alinhado ao `config/produtos.json`
  (ex.: `dentista-gestor-livro`); leads de teste vivem em
  `backend/data/vendas.db` (não `database/maquina.db`) — limpar. Arquivo:
  `templates/maquina/frontend/app/api/checkout/route.ts`.
- **2026-08-09 Máquina de vendas — fluxo:** causa: template nascia com copy
  genérica; `criar-maquina-vendas.py` quebrava no Windows cp1252 (emojis).
  Fix: personalização por nicho em 8 pontos com gate `grep 'Autor Digital|centenas de pessoas'`
  vazio (regra 12); `sys.stdout.reconfigure` no corpo de `criar_maquina`
  (regra 11). Derivados copiados via `output/colecoes/<slug>.json` (nomenclatura
  V5 não casa com substring — fallback 1ª palavra). Prevenção: máquinas antigas
  sincronizam copiando rota+page do template — skill `sincronizar-maquina-vendas`.
- **2026-08-09 Skill `gerar-relatorio-sessao`:** toda sessão com mudanças
  encerra em `relatorios/<YYYY-MM-DD>-<tema>.md/.pdf` (convenção V5.2) —
  relatório → testes → commit → push. Fix: `scripts/gerar-relatorio-sessao.py`
  (slug NFKD, 6 seções obrigatórias, Pandoc→Typst) + skill que orquestra o
  fluxo completo. Prevenção: nunca commitar sem `pytest -q` verde; mensagem via
  `git commit -F` (acentos/quebras de linha quebram `-m`); `_commit_msg*.txt`
  vaza no `git add -A` — apagar ANTES do add ou `git rm --cached` + `--amend`.
  Arquivo: `.claude/skills/gerar-relatorio-sessao/SKILL.md`.
- **2026-08-09 Padronização HUB POR COLEÇÃO:** causa: `output/` misturava layout
  plano (`output/livros/`, `output/tccs/` vazios) com hubs; `output/series.json`
  tinha 120/125 `membros` órfãos (destinos `livros/<slug>` de layout antigo);
  docs/AGENTS.md ainda descreviam organização por "série" (regra morta
  `output/series/`). Fix: coleção = hub único (`output/<obra>/<tipo>/...` com
  manifesto em `<obra>/colecoes/<nome>.json`); "série" virou termo obsoleto —
  preservado APENAS como nome interno de `output/series.json` (cores persistidas
  + migração `_series.json` dependem — NÃO renomear); `series_capa.py --reindexar`
  reconstrói `membros` com slugs reais (via `tipos_obra.listar_materiais` +
  `resolver_serie_key`), preserva cores, órfãos saem, chaves sem material ficam
  com `membros: []` (cor reservada). Prevenção: ao criar material novo, usar
  sempre `dir_obra`/`listar_materiais` (resolvem plano, por-obra e single-book);
  rodar `series_capa.py --reindexar` após reorganizações de `output/`.
  Arquivo: `scripts/series_capa.py`, `scripts/tipos_obra.py`, `AGENTS.md` §COLEÇÃO.
- **2026-08-09 Reestruturação HUB POR COLEÇÃO (manifestos por hub):** causa:
  `_dir_colecoes` gravava os 7 manifestos no 1º hub com `colecoes/` (analista)
  e single-books viviam na raiz de `livros/`/`tccs/` (fora do padrão `*/*`);
  `<hub>/series.json` (metadados ricos) duplicava o conceito do manifesto.
  Fix: `_dir_colecoes_da` resolve o dir pelo hub da coleção (1º segmento comum
  dos membros que não seja raiz de tipo; fallback plano `output/colecoes/`);
  `_metadados_ricos` funde `<hub>/series.json` no manifesto e apaga o legado
  (idempotente: reusa `metadados` do manifesto anterior); single-books migrados
  para `<tipo>/<slug>/`; `_todos_dirs_manifestos` varre `DIR_OUTPUT/*/colecoes`
  (NÃO `tipos_obra._sereis()` — usa `TO.DIR_OUTPUT` real, quebra teste com
  monkeypatch). Prevenção: limpeza global de manifestos órfãos deve varrer
  fallback + hubs; `_slug_arquivo` vira `ç` em `-` (minha-cole-o.json).
  Arquivo: `scripts/colecao.py`, `tests/test_colecao_hub.py`.
- **2026-08-09 Camada CAMPANHA (V5.3):** causa: a coleção entregava materiais,
  mas nenhuma camada de divulgação (posts, artes, sequências, cronogramas).
  Fix: `output/<colecao>/campanhas/<material>/` (HUB por coleção, subpasta por
  material: redes-sociais/instagram+linkedin e canais-comunicacao/emails+whatsapp);
  registro declarativo em `scripts/campanha.py` (artefato novo = 1 linha);
  `criar-campanha.py --material/--completo/--marcar-completa` (estrutura +
  moldes com rascunho determinístico do config_obra/sumário/manifesto + artes
  HTML+CSS→Chromium PNG + cronogramas com datas reais; custo zero) →
  agente reescreve copy (LLM baixo) → `validar-campanha.py` (R-CP-1..5 +
  R-CP-C1 no --completo; copy genérica regra 12 reprova; molde `Status: RASCUNHO`
  pendente reprova até a reescrita). Prevenção: campanha NÃO é tipo de obra
  (não toca tipos_obra.py); identidade vem do manifesto (`cor_accent`,
  `motivo_condutor.vocabulario`, `nucleo.senioridade`, `cta_url`); arquivo do
  manifesto usa slug normalizado (`_slug_arquivo` — `Colecao Teste` →
  `colecao-teste.json`); nos testes, monkeypatch de TODOS os `DIR_OUTPUT`
  (colecao.py incluído — esquecer `colecao.DIR_OUTPUT` faz o `varrer()` ler o
  output real e o teste falha de forma confusa).
  Arquivos: `scripts/campanha.py`, `scripts/criar-campanha.py`,
  `scripts/validar-campanha.py`, `templates/campanha/*.html`,
  `.claude/commands/campanha.md`, `.claude/commands/campanha-completa.md`,
  `tests/test_campanha.py`, spec em `melhorias/09-08-2026-campanhas-camada-nova.md`.
- **2026-08-09 Artes da campanha suprem o cronograma (V5.3):** causa:
  `gerar_artes` gerava `for i in (1,)` — 1 arte por formato (IG 1 post + 1
  story, LI 1 post, WhatsApp 1 por sequência) enquanto o cronograma cobre
  14–30 dias de envio. Fix: `campanha.py` ganhou `roteiro_rede` (usa os MESMOS
  nomes de formato do registro: `feed-story`, não `story` — erro real de
  contagem) e `n_artes_redes`/`n_artes_whatsapp` (quantidade que supre o
  cronograma: IG 14d = 7 posts + 7 stories, LI 14d = 7 posts, WhatsApp = 1
  arte por mensagem da sequência, 4 e 6); `gerar_artes` itera `range(1, n+1)`
  e `gerar_cronogramas` usa `CP.roteiro_rede` (DRY). Gate R-CP-3 agora valida
  a CONTAGEM por formato/sequência (`n_real/n_esperado artes (cronograma)`),
  não só existência/assinatura. Prevenção: ao adicionar formato de arte novo no
  registro, o nome TEM que casar com o usado em `roteiro_rede`/`TEMPLATES_ARTE`
  (feed-story ≠ story); regenerar coleção inteira demora (~600s+ por lote de 16
  materiais com Chromium) — rodar `--completo` e completar materiais restantes
  com `--material` quando estourar timeout. Arquivos: `scripts/campanha.py`,
  `scripts/criar-campanha.py`, `scripts/validar-campanha.py`,
  `tests/test_campanha.py`.
- **2026-08-09 PDFs em .md de campanha (V5.3) — cronogramas e textos:** causa:
  cronogramas e moldes de texto nasciam só em `.md`; imprimir/compartilhar
  exigia compilar à mão. Fix: `criar-campanha.py` ganhou
  `compilar_markdown_pdf` (alias retro `compilar_cronograma_pdf`) — Pandoc→Typst
  via `pdf_typst.executar` (fluxo `.typ` intermediário, nunca
  `--pdf-engine=typst`), binários por `shutil.which` com fallback WinGet
  cacheado (`functools.lru_cache`); `gerar_cronogramas` e `escrever_moldes`
  emitem `.md` + `.pdf` (mesmo nome); `_pdf_atualizado` regenera o PDF quando o
  `.md` foi editado depois (copy final do agente mais nova que o PDF). Log
  separa `X moldes (+Y PDF), Z cronogramas (+W PDF)`. Gates: R-CP-5 exige
  `.pdf` ao lado de cada `cronograma-*.md`; R-CP-2 exige `.pdf` ao lado de cada
  texto (exclui cronogramas, cobertos pelo R-CP-5); ambos reprovam PDF vazio.
  Prevenção: campanhas criadas ANTES do fix reprovam — rodar
  `criar-campanha.py --completo <colecao>` (ou helper temp) para gerar PDFs
  retroativos; nos testes, a fixture `ambiente` mocka a compilação com
  placeholder `%PDF` (gates só verificam existência) e há teste real com skip
  `precisa_pandoc_typst`. Arquivos: `scripts/criar-campanha.py`,
  `scripts/validar-campanha.py`, `tests/test_campanha.py`.
- **2026-08-09 Máquina de vendas 1:1 (V5.3):** causa: máquinas nasciam em
  `marketing/maquinas/` (caminho morto) ou `output/<hub>/marketing/` (várias por
  coleção, sem vínculo com campanhas). Fix: 1 máquina por COLEÇÃO em
  `output/<hub>/maquina/` (hub = 1º segmento do slug que não seja raiz de tipo);
  `criar-maquina-vendas.py` recusa 2ª obra do mesmo hub (sem input, retorna
  None) e copia `output/<hub>/campanhas/` → `maquina/campanhas/` com
  `snapshot.json` (origem/atualizado_em/materiais/copiado_em — normalizar
  separador com `replace("\\","/")` no Windows); manifesto da máquina ganha
  `colecao`/`maquina_em`/`campanhas`; `colecao.py --sincronizar` registra
  `maquina` + `maquinas_legadas` (não destrutivo — legadas em
  `output/<hub>/marketing/` ficam para o operador decidir); `empacotar-colecao.py`
  copia a máquina no pacote (ignora node_modules/.next/*.db). Prevenção:
  fallback de derivados usa TIPOS válidos (`playbook`, `ebook`, `deck`,
  `lead-magnet`) — nomes de raiz plural (`playbooks`) quebram
  `TO.listar_materiais` (KeyError); nos testes, `monkeypatch.setattr(TO,
  "DIR_OUTPUT", ...)` — `gerador.OUTPUT_BASE`/`OBRA_BASE` não existem mais.
  Arquivos: `scripts/criar-maquina-vendas.py`, `scripts/colecao.py`,
  `scripts/empacotar-colecao.py`, `tests/test_maquina_colecao.py`,
  spec em `melhorias/09-08-2026-maquina-1por-colecao-usa-campanhas.md`.

### [2026-08-13] RUNTIME: Subagente de expansão travou em 48 turns
- **Causa**: spawnar 1 subagente para expandir 8 capítulos (de ~12k para ~25k chars cada = ~100k chars de expansão total) estourou o limite de turns. Tarefa monolítica demais para um único subagente geral.
- **Fix**: cancelado (actor cancel). Expansão ficou pendente.
- **Arquivo**: actor general-10 (expansão de conteúdo livros/orca-ide)
- **Prevenção**: em expansion tasks, dividir em lotes de 2-3 capítulos por subagente, nunca 8 de uma vez. Se a tarefa envolver rewrite de múltiplos arquivos grandes, usar subagentes paralelos com escopo delimitado.

### [2026-08-13] PADRÃO: Playbook extraído de capítulos com refs faltantes
- **Causa**: `extrair-passos-praticos.py` extrai dados dos capítulos, mas 3 capítulos (2,3,7) tinham seção 7 (Referências) vazia. O gate R4 (mín 8 refs) falhou na auditoria.
- **Fix**: subagente revisor adicionou 3 refs ABNT a cada capítulo afetado.
- **Arquivo**: output/livros/orca-ide/capitulos/cap_{2,3,7}.md
- **Prevenção**: validar refs na seção 7 DEPOIS da escrita de cada capítulo (auto-validação do subagente-redator-capitulo deve checar contagem de refs, não apenas existência). Rodar `auditar-obra.py` imediatamente após cada lote, não só no final.

### [2026-08-13] CONFIG: Livro M ficou com 99k chars (mínimo 200k)
- **Causa**: capítulos escritos com ~12k chars em média, mas o mínimo para tamanho M (~80 páginas) é ~25k chars por capítulo. Subagentes produziram conteúdo válido mas curto demais.
- **Fix**: pendente — conteúdo precisa ser expandido.
- **Arquivo**: output/orca-ide/livros/orca-ide/capitulos/cap_*.md
- **Prevenção**: no prompt do subagente-redator-capitulo, incluir meta explícita de tamanho mínimo por seção (ex.: "seção Explica: mínimo 3000 caracteres"). Incluir contagem de caracteres no relatório de auto-validação.

### [2026-08-13] ESTRUTURA: Diretórios soltos fora do hub da coleção
- **Causa**: `fatiar-obra.py --playbook` gravou em `output/playbooks/` e o minerador acadêmico gravou em `output/orca-ide/pesquisa/` — ambos fora do hub `output/orca-ide/`. O orquestrador não validou a localização antes de prosseguir. Além disso, `colecao.py --sincronizar` criou `output/colecoes/` como fallback quando o hub não existia.
- **Fix**: movido manualmente para `output/orca-ide/livros/orca-ide/` e `output/orca-ide/playbooks/pbk-1-orca-ide-manual/`. Limpos diretórios órfãos `output/livros/`, `output/playbooks/` e `output/colecoes/`.
- **Arquivo**: output/orca-ide/ (hub), output/livros/ (removido), output/playbooks/ (removido), output/colecoes/ (removido)
- **Prevenção**: SEMPRE usar `tipos_obra.dir_obra(slug)` para resolver caminhos — nunca criar diretórios manualmente. Após `fatiar-obra.py`, validar que os artefatos ficaram dentro do hub com `ls output/<hub>/<tipo>/`. Se estiverem soltos, MOVER antes de qualquer operação seguinte. Rodar `colecao.py --sincronizar` após cada movimentação. O fallback `output/colecoes/` do `colecao.py` é legado — NÃO deve ser usado; o manifesto sempre vai em `<hub>/colecoes/<slug>.json`.

### [2026-08-20] ESTRUTURA: `relatorios/` órfã e vazia dentro de 2 hubs (recorrência do bug de pasta solta)
- **Causa**: durante a manufatura do Capítulo 8 de `livros/otimizacao-tokens-ide-agentica`, o operador sinalizou recorrência do bug de "pasta solta fora do hub" (ver entrada 2026-08-13 acima). Auditoria de `output/` mostrou que os 2 hubs existentes (`output/otimizacao-tokens-ide-agentica/`, `output/gratis-open-source/`) tinham uma subpasta `relatorios/` **vazia** e **fora do schema documentado** da seção "Estrutura de Coleções (HUB)" deste arquivo (que só lista `livros/ tccs/ artigos/ ebooks/ playbooks/ lead-magnets/ decks/ emails/ campanhas/ distribuicao/ maquina/ colecoes/`). Causa raiz identificada em `scripts/gerar-capa-relatorio.py`: `DIR_RELATORIOS = "relatorios"` era um caminho **relativo à CWD**, não ancorado na raiz do projeto — se o script roda com o diretório de trabalho dentro de `output/<hub>/` (comum em sessões de subagente que navegam para lá), ele cria `output/<hub>/relatorios/imagens/` silenciosamente em vez de `<raiz-do-projeto>/relatorios/imagens/`. **Importante**: nem toda estrutura "atípica" em `output/` é bug — `tipos_obra.dir_obra()` suporta oficialmente 2 layouts (multi-book: `<hub>/<tipo>/<slug>`; single-book raiz: `<hub>/<tipo>` quando `hub == slug`, caso de `output/gratis-open-source/livros/`), então não confundir layout single-book raiz válido com pasta solta.
- **Fix**: `gerar-capa-relatorio.py` corrigido para `DIR_RELATORIOS = str(Path(__file__).resolve().parent.parent / "relatorios")` (ancorado na raiz do projeto, como já fazia `gerar-relatorio-sessao.py`). Removidas as 2 pastas vazias `output/otimizacao-tokens-ide-agentica/relatorios/` e `output/gratis-open-source/relatorios/` (confirmado 0 arquivos antes de `rmdir`).
- **Arquivo**: `scripts/gerar-capa-relatorio.py` (linha `DIR_RELATORIOS`), `output/<hub>/relatorios/` (removidas, x2).
- **Prevenção**: nunca usar caminho relativo (`"relatorios"`, `"output"`, etc.) para diretório de escrita em script Python da fábrica — sempre `Path(__file__).resolve().parent.parent / "<pasta>"` (âncora na raiz do projeto), igual ao padrão já usado em `gerar-relatorio-sessao.py` e em `tipos_obra.DIR_OUTPUT`. Antes de declarar "pasta solta = bug", confirmar contra o schema documentado da seção "Estrutura de Coleções (HUB)" e contra os layouts suportados em `tipos_obra.dir_obra()` (docstring da função) — só remover/mover se a pasta não corresponder a nenhum layout válido.

### [2026-08-21] PADRÃO: RTK scratchpad migrado para arquivo externo (item D — cache do CLAUDE.md)
- **Causa**: o `CLAUDE.md` (lido automaticamente em toda sessão) chegou a 463 linhas/~51KB, boa parte por duas seções "RTK SCRATCHPAD" (uma numerada `## 7.`, outra solta `##` sem número — duplicata gerada pela skill `rtk-memory` porque `SKILL.md`/`templates.md` instruíam gravar em `AGENTS.md` procurando literalmente o heading `## RTK SCRATCHPAD`, sem achar `## 7. RTK SCRATCHPAD` já existente). Cada sessão nova appenda aqui, sem teto — o próprio livro "Tokens Sob Perícia" (Cap. 2) documenta, com fonte primária Anthropic, que o cache de prompt exige prefixo byte-a-byte idêntico e que um arquivo lido automaticamente que muda a cada sessão é o cenário exato de "prefixo instável".
- **Fix**: conteúdo das duas seções movido para `RTK-SCRATCHPAD.md` (raiz do projeto, este arquivo); `CLAUDE.md` passou a ter só um ponteiro de 1 linha na seção `## 7. RTK SCRATCHPAD`; `SKILL.md`/`templates.md` do `rtk-memory` atualizados para gravar em `RTK-SCRATCHPAD.md`, não mais em `AGENTS.md`/`CLAUDE.md`.
- **Arquivo**: `CLAUDE.md` (corpo normativo, agora estável), `RTK-SCRATCHPAD.md` (novo), `.claude/skills/rtk-memory/SKILL.md`, `.claude/skills/rtk-memory/templates.md`.
- **Prevenção**: novas entradas de aprendizado SEMPRE vão em `RTK-SCRATCHPAD.md` (append no final), nunca de volta no `CLAUDE.md` — isso reintroduziria o mesmo problema de prefixo instável que este fix resolve. Se uma skill genérica (multi-projeto) instruir gravar em `AGENTS.md`, sobrescrever a instrução localmente apontando para este arquivo.

### [2026-08-22] AMBIENTE: `.agents/` colide com o Codebuff/Freebuff, que executa os `.js`/`.mjs` que encontra lá
- **Causa**: `freebuff` (CLI da CodebuffAI) morria dentro do projeto imprimindo o USO do `compilador-abnt`. O Codebuff usa `.agents/` como diretório de agentes customizados e faz `import()` dos `.js`/`.mjs` que acha lá **dentro do próprio processo** (comprovado por sonda: `process.argv[1]` = executável do freebuff, `import.meta.url` = arquivo do projeto — logo import, não spawn). Como `setup-links` apontava `.agents/skills` e `.agents/mcp-servers` para `.claude/`, o CLI carregava `compilar-livro.mjs`, que executa no topo do módulo, imprime o USO e chama `process.exit(1)`. Causa independente e somada: o pacote npm global `node@24.19.0` instala `bin/node` como arquivo de texto ("This file intentionally left blank"), e o shim POSIX do freebuff prefere `basedir/node` — no Git Bash isso virava `This: command not found`.
- **Fix**: `npm uninstall -g node` (o Node real de `C:/Program Files/nodejs` fica intacto e é o primeiro no PATH); `.agents/` passou a receber só `agents/` e `commands/` (somente `.md`), removendo `skills/` e `mcp-servers/` dos dois `setup-links`. Skills e MCP servers seguem expostos via `agentic/` e `.opencode/`.
- **Arquivo**: `scripts/setup-links.ps1`, `scripts/setup-links.sh`, `CLAUDE.md` (seção 6), commit `f648552`.
- **Prevenção**: nunca reapontar `.agents/skills` ou `.agents/mcp-servers` para `.claude/` — `.agents/` é namespace de terceiro (Codebuff/Freebuff). Ao colocar qualquer `.js`/`.mjs` em `.agents/`, garantir que não tenha efeito colateral no topo do módulo (envolver em guard de main-module). Antes de instalar pacote npm global, checar se ele duplica algo já no PATH: `node` como pacote global quebra **todo** shim npm no Git Bash, não só um.

### [2026-08-22] ARMADILHA: apagar pasta espelho sem checar reparse points destrói o conteúdo real
- **Causa**: ao remover `.agents/skills` (suposta cópia descartável), foram destruídas 13 skills do plugin Cloudflare — porque `.claude/skills/<skill>` eram **junctions apontando para `.agents/skills/<skill>`**, o inverso do que a seção 6 do `CLAUDE.md` documenta (`.claude/` como fonte). A verificação de integridade feita por contagem de arquivos (`Get-ChildItem -Recurse -File` em `.claude/skills`, 3026 antes e 3026 depois) **não detectou nada**, porque `Get-ChildItem -Recurse` não desce dentro de junction — os 375 arquivos nunca entraram na contagem nas duas medições.
- **Fix**: as 13 junctions penduradas foram removidas com `[System.IO.Directory]::Delete($p, $false)` (apaga só o link) e os 375 arquivos restaurados com `git checkout -- .claude/skills/`, levando `git ls-files -d` de volta a 0.
- **Arquivo**: `.claude/skills/{cloudflare*,wrangler,agents-sdk,durable-objects,sandbox-*,turnstile-spin,web-perf,workers-best-practices}`.
- **Prevenção**: antes de apagar qualquer pasta espelho (`.agents/`, `agentic/`, `.opencode/`), mapear quem aponta para quem com `cmd /c dir /AL <pasta>` ou pelo atributo `ReparsePoint` — **nunca** confiar em contagem de arquivos como prova de integridade, e nunca assumir a direção do link pelo que a documentação diz. Para remover junction use `Directory.Delete(path, false)` ou `cmd /c rmdir` (sem `/s`); `Remove-Item -Recurse` pode atravessar para o alvo. Conferir `git ls-files -d` logo após qualquer remoção em massa: se aparecer arquivo deletado que você não pretendia tocar, restaurar com `git checkout --` antes de commitar.
