# Engenharia Agêntica — Versão Iniciante

## A jornada em 16 dias

Esta versão reescreve o livro **Engenharia Agêntica** em linguagem simples,
um dia por vez, usando o **projeto real `ecossistema-aidd`** como exemplo
contínuo do começo ao fim. Cada dia tem:

- **Meta do dia** — o que você será capaz de fazer ao final.
- **A ideia em uma frase** — o resumo sem tecnicismo.
- **A explicação simples** — conceito em linguagem de gente.
- **O exemplo real** — o que acontece de verdade no `ecossistema-aidd`.
- **Mão na massa** — exercício prático na sua máquina.
- **Checklist do dia** — confira antes de fechar.
- **Para saber mais** — leitura opcional.

Não precisa de experiência prévia com agentes. Só um editor de texto
(ou este próprio projeto aberto) e paciência.

---

## Mapa da jornada

| Dia | Capítulo original | Tema | Exemplo real |
|---|---|---|---|
| 1 | 1 | O agente não é o modelo | As 5 peças da cabine no repositório |
| 2 | 2 | Probabilismo e determinismo | Gates e scripts como juízes |
| 3 | 3 | O arquivo que todo agente lê | O `AGENTS.md` do ecossistema |
| 4 | 4 | Skills, MCPs e tools | As 6 ferramentas e as skills de `componentes/` |
| 5 | 5 | Turnos agênticos e custo | Pipeline de 8 fases do Generator |
| 6 | 6 | Cache hit | ESTADO em JSON, não em conversa |
| 7 | 7 | Economia severa de tokens | `context_slicer.py` e respostas secas |
| 8 | 8 | Otimização de contexto | Fatias AST e Cognitive Ledger |
| 9 | 9 | Scripts e gates na esteira | Os 12 Quality Gates de `gates/` |
| 10 | 10 | Hooks | Audit via `pre-commit` no `audit` |
| 11 | 11 | Agents e subagentes | Frentes isoladas (ORCA ADE / worktrees) |
| 12 | 12 | Orquestração | `ecossistema.py orchestrate` e Flight Plan |
| 13 | 13 | Roteamento inteligente de LLM | Multi-harness por frente no plano |
| 14 | 14 | Configurações que nunca te contam | `.env`, harnesses, bamainda |
| 15 | 15 | Segredos universais | As 8 Leis Invioláveis do AGENTS.md |
| 16 | 16 | Arquitetura da esteira agêntica | O ecossistema AIDD completo |

---

## Como usar

1. Leia um dia por vez. Não pule dias — cada um constrói a base do seguinte.
2. Faça o "Mão na massa": o aprendizado está em mexer, não em só ler.
3. Quando o dia citar `ecossistema-aidd`, abra a pasta desse projeto
   e localize o arquivo ou script mencionado. Ler o código de verdade é parte
   do treino.
4. Conclua o checklist antes de ir para o próximo dia.