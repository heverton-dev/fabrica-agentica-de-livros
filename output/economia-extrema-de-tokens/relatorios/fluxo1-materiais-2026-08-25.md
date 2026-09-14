# Relatório FLUXO 1 — Materiais — 2026-08-25

## Resumo Executivo
- **Status:** ⚠️ CONCLUÍDO COM RESSALVAS
- **Obra:** Economia Extrema de Tokens (livro, tamanho M, 8 capítulos)
- **Duração:** ~3h (esboço + manufatura em 2 lotes + expansão R2 + correção de gates + compilação)

## Itens Criados

| Item | Status | Caminho | Observação |
|------|--------|---------|------------|
| Livro (PDF) | ✅ | `output/economia-extrema-de-tokens/livros/livro_final.pdf` | 107 páginas, 2.599 KB, veredito **CONFORME** |
| Playbook | ⚠️ | `output/economia-extrema-de-tokens/playbooks/pbk-1-economia-extrema-tokens/` | 8 passos extraídos, PDF compila (31 páginas), mas `validar-playbook.py` reporta **NÃO CONFORME** (21 violações) |
| Artigos | — | — | não contratados (`gerar_artigos=false`) |
| E-books | — | — | não contratados (`gerar_ebooks=false`) |
| Lead Magnets | — | — | não contratados (`gerar_lead_magnets=false`) |
| Deck | — | — | não contratado (`gerar_deck=false`) |
| E-mails | — | — | não contratado (`gerar_emails=false`) |
| Coleção | ✅ | `output/economia-extrema-de-tokens/colecoes/economia-extrema-de-tokens.json` | 2 membros (livro + playbook) |
| Distribuição | ✅ | `output/economia-extrema-de-tokens/livros/distribuicao/` | livro_final.pdf + playbook + README + LICENSE |

## Achados de Infraestrutura (fora do escopo original, corrigidos durante a execução)

1. **Estrutura de diretórios "solta" (bug crítico, reportado pelo operador em tempo real):**
   O `/esbocar` criou a obra em `output/livros/economia-extrema-de-tokens/` (raiz plana),
   violando a regra HUB POR COLEÇÃO (V5). Migrado fisicamente para
   `output/economia-extrema-de-tokens/{livros,playbooks,colecoes,relatorios}/` sem
   interromper os subagentes de redação em andamento. Causa raiz identificada em
   `.claude/commands/esbocar.md` (Passo 0/2 instruía o layout plano) — **corrigida na
   skill** para não repetir em futuras obras.
2. **Bug de compilação Typst ($ solto):** a sinopse gerada por `metadados_livro.py`
   continha valores monetários (`$100/mês`) que o Typst interpretava como abertura de
   modo matemático, quebrando a compilação. `converter-md-pdf.ps1` já escapava isso no
   corpo do Markdown, mas o caminho Python principal (`compilar-para-pdf.py`) não
   escapava as variáveis `-V`. **Corrigido na função compartilhada** (`_escapar_typst`
   em `metadados_livro.py`), beneficiando todos os tipos de obra (livro/tcc/artigo/
   playbook/lead-magnet/deck). Suíte completa revalidada: 833/833 testes passando.
3. **`derivados.json` com caminho obsoleto:** após a migração de hub, o registro do
   playbook em `derivados.json` apontava para o caminho antigo, fazendo
   `empacotar-distribuicao.py` reportar o playbook como "ausente". Corrigido.
4. **`colecao.py --sincronizar` recria manifesto plano órfão:** comportamento
   observado (não corrigido — fora do escopo desta sessão): ao sincronizar, o script
   por vezes recria `output/colecoes/<nome>.json` mesmo quando o hub já existe.
   Removido manualmente a cada ocorrência nesta sessão; recomenda-se investigar
   `_dir_colecoes_da`/`_hub_da_colecao` em sessão futura.

## Validações Executadas

| Validação | Resultado |
|-----------|-----------|
| `auditar-obra.py --estrito` | ✅ CONFORME (R1-R15 + 6 gates de conteúdo) |
| `validar-codigo.py` | ✅ 100% dos blocos verificáveis |
| `renderizar-diagramas.py --validar` | ✅ 14/14 diagramas Mermaid válidos |
| `validar-referencias.py` | ✅ |
| `validar-metricas.py` | ✅ |
| `validar-escala.py` | ✅ (corrigido após expansão) |
| `validar-afirmacoes.py` | ✅ (corrigido após expansão — 21 violações → 0) |
| `validar-fontes.py` | ✅ |
| `validar-comandos-cli.py` | ✅ |
| `validar-capa-nivel.py` | ✅ badge "PARA INICIANTES" coerente |
| `validar-artefatos.py --estrito` | ✅ livro e playbook abrem |
| `validar-playbook.py --estrito` | ❌ NÃO CONFORME (21 violações — ver pendências) |
| `python -m pytest -q` (suíte completa) | ✅ 833/833 |

## Pendências

1. **Playbook fora do padrão editorial** (`R-PBK-1/2/3/5`): as cenas de contraste do
   livro são narrativas em 2ª pessoa (exigência do próprio contrato EITA do livro),
   enquanto `extrair-passos-praticos.py` busca listas de bullets sob a palavra
   "armadilha"/"cuidado". Resultado: 0-2 armadilhas extraídas por passo, seções
   "execução" acima do limite de 25 linhas, sem comando de verificação executável em
   3/8 passos. O PDF do playbook compila e abre, mas o conteúdo está incompleto para
   uso como playbook autônomo. Requer uma passada editorial dedicada (fora do escopo
   desta produção) ou ajuste do extrator para reconhecer cenas narrativas.
2. **`colecao.py` recria manifesto plano intermitente** — ver achado 4 acima.
