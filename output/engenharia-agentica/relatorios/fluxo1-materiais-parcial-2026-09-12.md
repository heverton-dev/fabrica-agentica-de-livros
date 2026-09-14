# Relatório FLUXO 1 — Materiais (PARCIAL) — 12 set. 2026

## Resumo Executivo
- **Status:** ⚠️ 16/16 capítulos escritos · auditoria pendente apenas de VOLUME (R2)
- **Coleção:** `engenharia-agentica`
- **Obra:** Engenharia Agêntica (livro, GG — 4 partes / 16 capítulos / 160 p)
- **Escopo autorizado:** SOMENTE FLUXO 1. FLUXO 2 (campanhas) e FLUXO 3 (máquina)
  **pulados por ordem explícita** do operador ("SEM MÁQUINA E SEM CAMPANHA", REGRA 17).

## Itens Criados

| Item | Status | Caminho | Observação |
|---|---|---|---|
| Config da obra | ✅ | `livros/config_obra.json` | válido por `parametros_obra.py --validar` |
| Dossiês de pesquisa | ✅ | `livros/pesquisa/` | 8 dossiês, 648 KB |
| Índice RAG | ✅ | `livros/pesquisa/indice_dossie.json` | 28 blocos |
| Sumário macro | ✅ | `livros/sumario_macro.json` | 4 partes, 16 capítulos, motivo condutor |
| Capítulos 1-16 | ✅ | `livros/capitulos/cap_01..16.md` | EITA-V2, gates 1-4 OK nos 16 |
| Gabaritos | ✅ | `solucoes/cap_5..16_gabarito.md` | exigidos pelo gate 4 |
| Playbook | ⏳ esqueleto | `playbooks/pbk-1-engenharia-agentica/` | extração depende dos capítulos |
| Coleção | ✅ | `colecoes/engenharia-agentica.json` | 2 membros |
| Livro final (PDF) | ⏳ pendente | — | Fase 3 não iniciada |

## Audit de conformidade (estado atual)

| Requisito | Status | Detalhe |
|---|---|---|
| R1 — 16 capítulos | ✅ | 16 |
| R2 — 400.000 caracteres (GG) | ❌ | **278.817** caracteres (~111,5 páginas) |
| R3 — 7 seções EITA-V2 | ✅ | nenhum capítulo incompleto |
| R4 — 20 referências ABNT/capítulo | ✅ | nenhum capítulo abaixo |
| R9 — sem `---` | ✅ | — |
| R10 — 3 citações inline `[N]` | ✅ | corrigido em cap 09 e cap 14 |
| R11 — 1 diagrama mermaid em Ilustra | ✅ | 16/16 válidos |
| R12 — artefato técnico na Técnica | ✅ | 85 blocos, 100% dos verificáveis OK |
| R13 — sem truncamento/pendência | ✅ | — |
| R14 — rastreabilidade `[N]` | ✅ | — |
| R15 — referências em ordem | ✅ | — |
| Gates de conteúdo F1/F2 | ✅ | referências, métricas, escala, afirmações, fontes, CLI — todos exit 0 |

**Veredito:** `NAO CONFORME` — reprova **somente** por R2 (volume).

## Alertas do revisor (não bloqueiam, mas devem ser tratados)

- 21 pares de parágrafos sobrepostos — quase todos pelo bloco "Os termos da casa"
  repetido nos capítulos (sim=1.0 entre cap 15 e cap 16). Variação de redação prevista.
- 7 termos com grafia inconsistente (`esta/está`, `AGENTS.md/agentsmd`, `historico/histórico`).
- 23 citações empilhadas (`[N][N]`) — tom de revisão de literatura em trechos pontuais.
- Motivo condutor ausente fora da seção Ilustra em cap 06, 07, 08, 09, 11, 14.

## Bug de harness corrigido (R16)

`scripts/pool-capitulos.py` quebrava em Windows/cp1252 (regra 11 do `AGENTS.md`):
1. `main()` sem `TO.console_utf8()` → `UnicodeEncodeError` ao imprimir `✅`;
2. `subprocess.run(..., text=True)` sem `encoding="utf-8"` → `UnicodeDecodeError`
   ao ler a saída dos gates.

Corrigido nos dois pontos; **suíte completa reexecutada: 833 passed**.

## Pendências

| # | Pendência | Prioridade |
|---|---|---|
| 1 | Expandir os 16 capítulos em ~121.183 caracteres para fechar R2 | alta |
| 2 | Reduzir sobreposição do bloco "termos da casa" e padronizar grafia | média |
| 3 | Desempilhar citações `[N][N]` | média |
| 4 | Reforçar motivo condutor fora da Ilustra em 6 capítulos | baixa |
| 5 | Fase 3 — compilação ABNT, capa, PDF (`compilar-para-pdf.py --paginas-exatas`) | média |
| 6 | Extração do playbook (`extrair-passos-praticos.py`) | baixa |
| 7 | `empacotar-distribuicao.py` + relatório consolidado + relatório de sessão | baixa |
| 8 | Commit + push do fix de `pool-capitulos.py` (aguarda autorização) | média |
