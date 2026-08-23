# RELATÓRIO DE SESSÃO — Correcao do Freebuff: shim node quebrado e colisao de namespace em .agents/

> **Data:** 2026-08-22
> **Projeto:** Fábrica Agêntica de Publicações

---

## 1. Contexto

O comando freebuff falhava dentro do projeto, imprimindo o USO do compilador-abnt e saindo. A investigacao revelou duas causas independentes e sem relacao entre si: um pacote npm global corrompido e uma colisao de namespace entre a pasta .agents/ do projeto e o diretorio de agentes do Codebuff/Freebuff.

---

## 2. Bugs Descobertos e Corrigidos

### O pacote npm global node@24.19.0 instala bin/node como arquivo de texto de 34 bytes (This file intentionally left blank); o shim POSIX do freebuff prefere basedir/node e o Git Bash tentava interpretar o texto como script, gerando This: command not found

- **Causa:** O pacote npm global node@24.19.0 instala bin/node como arquivo de texto de 34 bytes (This file intentionally left blank); o shim POSIX do freebuff prefere basedir/node e o Git Bash tentava interpretar o texto como script, gerando This: command not found
- **Fix:** Removido o pacote global redundante com npm uninstall -g node; o Node real v24.19.0 em C:/Program Files/nodejs permanece intacto e continua primeiro no PATH
- **Arquivo:** `AppData/Roaming/npm/node_modules/node/bin/node`

### setup-links apontava .agents/skills e .agents/mcp-servers para .claude/; o Codebuff/Freebuff varre .agents/ e faz import() dos .js/.mjs dentro do proprio processo, entao compilar-livro.mjs executava no import, imprimia o USO e chamava process.exit(1), derrubando o CLI

- **Causa:** setup-links apontava .agents/skills e .agents/mcp-servers para .claude/; o Codebuff/Freebuff varre .agents/ e faz import() dos .js/.mjs dentro do proprio processo, entao compilar-livro.mjs executava no import, imprimia o USO e chamava process.exit(1), derrubando o CLI
- **Fix:** Removidas as duas junctions do setup-links; .agents/ passa a receber apenas agents/ e commands/ (somente .md). Skills e MCP servers seguem expostos via agentic/ e .opencode/
- **Arquivo:** `scripts/setup-links.ps1, scripts/setup-links.sh, CLAUDE.md`

### Incidente durante a correcao: a remocao de .agents/skills destruiu o conteudo real de 13 skills do plugin Cloudflare, porque .claude/skills/<skill> eram junctions apontando para .agents/skills/<skill> (o inverso do documentado). A verificacao de integridade por contagem nao detectou porque Get-ChildItem -Recurse nao desce em junction

- **Causa:** Incidente durante a correcao: a remocao de .agents/skills destruiu o conteudo real de 13 skills do plugin Cloudflare, porque .claude/skills/<skill> eram junctions apontando para .agents/skills/<skill> (o inverso do documentado). A verificacao de integridade por contagem nao detectou porque Get-ChildItem -Recurse nao desce em junction
- **Fix:** As 13 junctions penduradas foram removidas com Directory.Delete(path,false) e os 375 arquivos restaurados do git com git checkout -- .claude/skills/; git ls-files -d voltou a zero
- **Arquivo:** `.claude/skills/ (13 skills: cloudflare*, wrangler, agents-sdk, durable-objects, sandbox-*, turnstile-spin, web-perf, workers-best-practices)`

### A edicao de CLAUDE.md pela ferramenta Edit rompeu o hardlink com os 5 arquivos espelho, que ficaram com o conteudo antigo

- **Causa:** A edicao de CLAUDE.md pela ferramenta Edit rompeu o hardlink com os 5 arquivos espelho, que ficaram com o conteudo antigo
- **Fix:** Hardlinks refeitos rodando scripts/setup-links.ps1; conferido com stat -c %h (voltou a 7) e inode identico nos 6 arquivos
- **Arquivo:** `CLAUDE.md, AGENTS.md, .windsurfrules, .clinerules, .github/copilot-instructions.md, .cursor/rules/fabrica-agentica.mdc`

---

## 3. Arquivos Alterados

- `CLAUDE.md`
- `AGENTS.md`
- `.windsurfrules`
- `.clinerules`
- `.github/copilot-instructions.md`
- `.cursor/rules/fabrica-agentica.mdc`
- `.windsurf/rules/fabrica-agentica.md`
- `scripts/setup-links.ps1`
- `scripts/setup-links.sh`

---

## 4. Validações

- 833 testes passando (pytest -q, 2min04) - rodado antes do commit e de novo pelo hook pre-commit
- freebuff e npx freebuff abrem a TUI do Freebuff dentro do projeto, sem cair no compilador-abnt
- 13 skills restauradas: 375 arquivos, git ls-files -d = 0
- hardlinks de CLAUDE.md restaurados: links=7, inode identico nos 6 espelhos
- varredura de reparse points em .claude/ = 0 junctions penduradas

---

## 5. Commits

- `f648552 fix(portabilidade): nao expor skills/ e mcp-servers/ em .agents/`

---

## 6. Resumo de Entregas

- freebuff volta a funcionar dentro do projeto
- colisao .agents/ documentada na secao 6 do CLAUDE.md e comentada nos dois setup-links
- skills do plugin Cloudflare restauradas e agora como pastas reais em .claude/skills/ (fonte de verdade, conforme secao 6)
- tres memorias de projeto gravadas: privacidade do Freebuff, quebra de hardlink pelo Edit e links materializados na copia de backup

---

## 7. Adendo — Reconstrucao das junctions do projeto

O relatorio original registrava, como pendencia em aberto, que nesta copia em
`D:\Backup_C_...` **todas** as pastas espelho estavam materializadas como
diretorios reais duplicados, ja divergindo da fonte (`compilar-livro.mjs` com
17.677 bytes no espelho contra 18.130 em `.claude/`). O operador pediu a
reconstrucao, feita na mesma sessao.

**Verificacoes antes de apagar** (aplicando a licao do incidente da secao 2):

- git nao rastreia nada nos espelhos: `agentic/` = 0 e `.agents/` = 0 arquivos
  versionados; `.opencode/` = 1, apenas `plugins/fabrica-hooks.ts`, que nao e
  junction e nao foi tocado. `.gitignore` cobre as 10 pastas.
- nenhum arquivo exclusivo dos espelhos: as 10 arvores comparadas com `comm -23`
  contra a fonte deram **0** arquivos que existiriam so na copia.
- nenhum reparse point aninhado nos 10 espelhos — `Remove-Item -Recurse` nao
  teria como atravessar para um alvo.

**Execucao:** as 10 pastas reais foram removidas e `scripts/setup-links.ps1`
recriou as junctions. A fonte permaneceu intacta (3401 / 7 / 19 / 375 arquivos
em `.claude/{skills,agents,commands,mcp-servers}`, identico ao baseline medido
antes da remocao).

**Junctions ativas:** `agentic/{skills,agents,commands,mcp-servers}`,
`.opencode/{skills,agents,commands,mcp-servers}` e `.agents/{agents,commands}`.
`.agents/` **nao** recebeu `skills/` nem `mcp-servers/` — e exatamente a correcao
do commit `f648552`, preservada.

**Validacoes do adendo:**

- propagacao provada por inode: `compilar-livro.mjs` tem inode `844424931101077`
  e 18.130 bytes lido via `.claude/`, via `agentic/` e via `.opencode/` — mesmo
  arquivo, sem duplicacao nem divergencia
- espelhos agora servem a fonte atualizada (3401 arquivos em skills, nao os
  3026 obsoletos)
- `git ls-files -d` = 0 e `git status` limpo
- freebuff continua abrindo a TUI dentro do projeto (sem regressao)
- 833 testes passando

---

*Relatório gerado em 2026-08-22 — Fábrica Agêntica de Publicações*
