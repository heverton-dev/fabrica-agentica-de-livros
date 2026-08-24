# Relatório: Arquitetura de IA — Do Zero ao PhD

**Data:** 21/08/2026  
**Slug:** `livros/arquitetura-de-ia`  
**Status:** ✅ CONCLUÍDO

## Resumo

Livro técnico com projeto progressivo (Assistente de IA Completo) que evolui a cada capítulo. O leitor constrói um sistema real desde o primeiro capítulo.

## O que foi criado

| Item | Status | Detalhe |
|------|--------|---------|
| Livro | ✅ | 8 capítulos, 200.5k chars, 141 páginas PDF |
| Capa | ✅ | PNG 726KB via gerar-capa.py |
| PDF | ✅ | 2.63MB via Pandoc+Typst |
| Playbook | ✅ | 8 passos, 0 violações R-PBK |
| Coleção | ✅ | 2 membros (livro + playbook) |
| Campanhas | ❌ | Pulada (a pedido) |
| Máquina de vendas | ❌ | Pulada (a pedido) |

## Sumário do Livro

| Parte | Capítulo | Título | Projeto |
|-------|----------|--------|---------|
| I — Fundamentos | 1 | O Primeiro Contato com IA | Chat básico + API |
| | 2 | Persistência e API | FastAPI + PostgreSQL |
| | 3 | RAG | ChromaDB + embeddings |
| | 4 | Fine-Tuning | LoRA + QLoRA |
| II — Produção | 5 | Evals e Testing | Framework de avaliação |
| | 6 | Segurança | JWT + Rate Limiting |
| | 7 | Deploy | Docker + Prometheus + Grafana |
| | 8 | Arquitetura Avançada | Cache + Multi-tenant |

## Playbook (8 passos)

| # | Título | Estágio |
|---|--------|---------|
| 1 | Configurar Ambiente e Primeiro Chat | Fundamentos |
| 2 | Adicionar API REST e Persistência | Fundamentos |
| 3 | Implementar RAG com ChromaDB | Conhecimento |
| 4 | Fine-Tuning com LoRA | Conhecimento |
| 5 | Sistema de Evals e Testing | Qualidade |
| 6 | Autenticação e Rate Limiting | Segurança |
| 7 | Deploy e Monitoramento | Produção |
| 8 | Arquitetura Avançada | Produção |

## Arquivos

```
output/livros/arquitetura-de-ia/
├── arquitetura-de-ia-do-zero-ao-phd.pdf  (2.63MB, 141 páginas)
├── arquitetura-de-ia-do-zero-ao-phd.md   (200.5k chars)
├── capitulos/cap_1-8.md
├── imagens/capa.png
├── pesquisa/
├── sumario_macro.json
└── config_obra.json

output/arquitetura-de-ia/playbooks/pbk-1-arquitetura-ia-phd/
├── passos/passo_01-08.json (8 passos CONFORME)
└── config_obra.json

output/arquitetura-de-ia/colecoes/arquitetura-de-ia.json
```
