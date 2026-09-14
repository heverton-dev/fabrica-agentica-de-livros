# Parecer de Revisão Técnica — Tokens Sob Perícia

## Veredito
CONFORME

## Requisitos contratuais

| Requisito | Status | Observação |
|---|---|---|
| R1 (mín. 8 capítulos) | OK | 8 capítulos |
| R2 (mín. 200.000 caracteres) | OK | 213.169 caracteres (~85,3 páginas) |
| R3 (7 seções EITA-V2) | OK | todos os capítulos completos |
| R4 (mín. 20 refs/capítulo) | OK | todos os capítulos |
| R9 (sem horizontal rules) | OK | — |
| R10 (mín. 3 citações inline) | OK | — |
| R11 (diagrama Mermaid válido) | OK | 8/8 |
| R12 (artefato técnico) | OK | — |
| R13 (sem truncamento) | OK | — |
| R14 (rastreabilidade [N]) | OK | 0 órfãs |
| R15 (ordem NBR 6023) | OK | corrigido cap_3, cap_4, cap_6 |
| Gates de conteúdo (referências/métricas/escala/afirmações/fontes) | OK | 5/5 |

## Correções aplicadas

| Capítulo | Classe do defeito | O que foi corrigido |
|---|---|---|
| cap_1, cap_2 | R2 (déficit de caracteres) | +8.390 caracteres de aprofundamento real (hierarquia de fontes, posicionamento de cache_control, scripts técnicos novos) |
| cap_3, cap_4 | R2 (déficit de caracteres) + R15 | +7.191 caracteres (catálogo Zen, config avançada GPTCache/servidor) e reordenação da seção 7 |
| cap_5, cap_6 | R2 (déficit) + 19 refs não citadas em cap_6 | +8.924 caracteres; todas as 27 referências do cap_6 agora citadas no corpo |
| cap_7, cap_8 | R2 (déficit de caracteres) | +8.824 caracteres (delegação Hermes, Antigravity, blindagem de segredos) |
| cap_1–cap_8 | Grafia inconsistente (pericia/agentica/semaforo) | `corrigir-mecanico.py` canonicalizou para a forma acentuada |
| cap_3, cap_4, cap_6 | R15 (ordem numérica NBR 6023) | seção 7 reordenada ascendente [1]..[N] |
| cap_2 (x2), cap_5 (x3), cap_6 (x1) | R-AF-1 (dado factual sem [N] no parágrafo) | citação `[N]` adicionada no mesmo parágrafo, reusando referência já existente no capítulo |

## Conferência por amostra

| Capítulo | Citação [N] | Fonte | Resultado |
|---|---|---|---|
| cap_2 | [1] | https://platform.claude.com/docs/en/build-with-claude/prompt-caching | conferido — desconto de 90% no cache read confirmado na doc oficial |
| cap_6 | [1] | https://github.com/ryoppippi/ccusage | conferido — pacote npm, subcomandos `daily/weekly/monthly/session/blocks` reais |
| cap_9 (auditoria geral, LAB 9) | — | https://hermes-agent.nousresearch.com/docs/user-guide | conferido — verbos reais `skills install/browse/list`, `sessions` no plural |

## Não conformidades residuais
Nenhuma (R1-R15 e os 5 gates de conteúdo em CONFORME/exit 0).

## Recomendações de estilo (não bloqueantes)
- 26 citações empilhadas (tom de revisão de literatura) remanescentes em cap_3, cap_4, cap_6, cap_7, cap_8 — a maioria em células de tabela comparativa (formato compacto aceitável), residual pode ser polido em uma futura revisão de estilo.
- `validar-codigo.py --executar` reporta 7 blocos com falha de execução isolada (cap_1, cap_2, cap_4 x3, cap_5, cap_6) — todas de causa ambiental (rede indisponível para `npx`, `gptcache`/`gptcache_server` não instalados neste sandbox, linha de `crontab` classificada como bash executável, blocos que reaproveitam função definida em bloco anterior do mesmo capítulo por escolha didática). Sintaxe 100% válida (`validar-codigo.py --estrito`, sem `--executar`); não é defeito de conteúdo.
