# Relatório de Produção Completa — 2026-08-25

## Resumo Executivo
- **Obra:** Economia Extrema de Tokens (livro, tamanho M)
- **Coleção:** economia-extrema-de-tokens
- **Status Geral:** ⚠️ CONCLUÍDO COM RESSALVAS
- **Escopo desta execução:** apenas FLUXO 1 (Materiais) — Campanha e Máquina de
  vendas **excluídos por escolha explícita do operador** (`/produzir-obra-completa
  livros/economia-extrema-de-tokens (SEM MÁQUINA E SEM CAMPANHA)`), conforme R17 da
  fábrica (campanha/máquina são sempre opcionais).

---

## FLUXO 1 — MATERIAIS

| Item | Status | Caminho | Observação |
|------|--------|---------|------------|
| Livro (PDF) | ✅ | `output/economia-extrema-de-tokens/livros/livro_final.pdf` | 107 páginas, 204.509 caracteres de corpo, veredito **CONFORME** |
| Playbook | ⚠️ | `output/economia-extrema-de-tokens/playbooks/pbk-1-economia-extrema-tokens/` | PDF compila (31 páginas) mas conteúdo NÃO CONFORME (21 violações estruturais) |
| Artigos / E-books / Lead Magnets / Deck / E-mails | — | — | não contratados no esboço |
| Coleção | ✅ | `output/economia-extrema-de-tokens/colecoes/economia-extrema-de-tokens.json` | 2 membros |

**Relatório detalhado:** `fluxo1-materiais-2026-08-25.md`

---

## FLUXO 2 — CAMPANHAS

**Status:** ⏭️ PULADO — exclusão explícita do operador nesta execução (R17: campanha é
sempre opcional). Pode ser disparado a qualquer momento com
`/campanha-completa economia-extrema-de-tokens`.

---

## FLUXO 3 — MÁQUINA DE VENDAS

**Status:** ⏭️ PULADO — exclusão explícita do operador nesta execução (R17: máquina é
sempre opcional). Pode ser disparado a qualquer momento com
`/criar-maquina economia-extrema-de-tokens`.

---

## DISTRIBUIÇÃO

| Item | Caminho |
|------|---------|
| Pacote | `output/economia-extrema-de-tokens/livros/distribuicao/` |
| Conteúdo | `livro_final.pdf`, `playbooks/pbk-1-economia-extrema-tokens.pdf`, `README.md`, `LICENSE` |

---

## Achados e Correções de Infraestrutura (fora do escopo original)

Durante a produção, o operador sinalizou que os artefatos estavam sendo gravados em
raízes planas (`output/livros/...`, `output/playbooks/...`, `output/colecoes/...`) em
vez do padrão HUB POR COLEÇÃO (V5). Investigação e correção completas:

1. **Migração física em tempo real** — todo o conteúdo (config, dossiê, capítulos,
   playbook, manifesto) foi movido para `output/economia-extrema-de-tokens/` sem
   interromper os 4 subagentes de redação que já estavam escrevendo nos capítulos
   1-4 (aguardou conclusão do lote antes de mover a pasta do livro).
2. **Causa raiz corrigida na fonte:** `.claude/commands/esbocar.md` instruía
   literalmente `output/<prefixo>/<slug>/` (raiz plana) no Passo 0/2. Reescrito para
   `output/<slug>/<prefixo>/` (hub primeiro) — futuras obras via `/esbocar` não
   repetirão o erro.
3. **Bug de compilação Typst por `$` solto** encontrado ao compilar o PDF final
   (sinopse com "$100/mês" abria modo matemático no Typst). Corrigido na função
   compartilhada `_variaveis`/`variaveis_pandoc*` de `scripts/metadados_livro.py`
   (usada por livro, TCC, artigo, playbook, lead-magnet e deck). Suíte completa
   revalidada: **833/833 testes passando**. Commit `a1802c4` (main), já pushado.
4. **`derivados.json` com caminho obsoleto** do playbook após a migração —
   corrigido manualmente.

## Expansão de Conteúdo (Gate R2)

A primeira rodada de manufatura produziu 137.029 caracteres (8 capítulos), abaixo do
mínimo de 200.000 exigido para tamanho M (~80 páginas). Todos os 8 capítulos foram
expandidos (RAG no dossiê, sem inventar dados) para 203.962-204.509 caracteres finais.
A expansão introduziu 21 violações novas do gate `validar-afirmacoes.py`/
`validar-escala.py` (exemplos numéricos ilustrativos sem marcador de cena
reconhecido) — todas corrigidas via `subagente-revisor-tecnico` reformulando a
abertura dos parágrafos afetados (nunca inventando citação `[N]`).

## Validações Executadas

Ver detalhamento completo em `fluxo1-materiais-2026-08-25.md`. Resumo:
`auditar-obra.py --estrito` → **CONFORME**; `pytest -q` → **833/833**;
`validar-artefatos.py --estrito` → livro e playbook abrem.

## Pendências

| # | Pendência | Fluxo | Prioridade |
|---|-----------|-------|------------|
| 1 | Playbook não conforme ao padrão editorial (cenas narrativas vs. extrator de bullets) | Materiais | Média |
| 2 | `colecao.py --sincronizar` recria manifesto plano órfão intermitentemente | Infraestrutura | Baixa |
| 3 | Campanha e Máquina de vendas não geradas (exclusão intencional) | Campanha/Máquina | — (disparar sob demanda) |

## Arquivos Gerados

| Arquivo | Descrição |
|---------|-----------|
| `relatorios/fluxo1-materiais-2026-08-25.md` | Relatório detalhado do Fluxo 1 |
| `relatorios/relatorio-completo-2026-08-25.md` | Este relatório consolidado |
