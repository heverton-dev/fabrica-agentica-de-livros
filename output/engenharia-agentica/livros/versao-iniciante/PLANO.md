# Engenharia Agêntica — Versão Iniciante

## A jornada em 16 dias

Esta versão reescreve o livro **Engenharia Agêntica** em linguagem simples,
um capítulo por dia, usando o **projeto real `proj_fabrica-de-livros`** como
exemplo contínuo do começo ao fim. Cada dia tem:

- **Meta do dia** — o que você será capaz de fazer ao final.
- **A ideia em uma frase** — o resumo sem tecnicismo.
- **A explicação simples** — conceito em linguagem de gente.
- **O exemplo real** — o que acontece de verdade no `proj_fabrica-de-livros`.
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
| 2 | 2 | Probabilismo e determinismo | Scripts e gates como juízes |
| 3 | 3 | O arquivo que todo agente lê | O `AGENTS.md` da própria fábrica |
| 4 | 4 | Skills, MCPs e tools | As skills e agents de `.claude/` |
| 5 | 5 | Turnos agênticos e custo | Lotes de capítulos em paralelo |
| 6 | 6 | Cache hit | A ordem estável do contexto |
| 7 | 7 | Economia severa de tokens | Skills `lean-ctx`, `headroom`, `caveman` |
| 8 | 8 | Otimização de contexto | Compressão, seleção e isolamento |
| 9 | 9 | Scripts e gates na esteira | `auditar-obra.py` e validadores |
| 10 | 10 | Hooks | O hook `pre-commit` e `settings.json` |
| 11 | 11 | Agents e subagentes | Delegação com contexto isolado |
| 12 | 12 | Orquestração | Worktrees, paralelismo e Orca ADE |
| 13 | 13 | Roteamento inteligente de LLM | Modelo certo por tarefa |
| 14 | 14 | Configurações que nunca te contam | Chaves silenciosas e auditoria |
| 15 | 15 | Segredos universais | Princípios que resistem ao tempo |
| 16 | 16 | Arquitetura da esteira agêntica | A fábrica de livros completa |

---

## Como usar

1. Leia um dia por vez. Não pule dias — cada um constrói a base do seguinte.
2. Faça o "Mão na massa": o aprendizado está em mexer, não em só ler.
3. Quando o dia citar `proj_fabrica-de-livros`, abra a pasta desse projeto
   e localize o arquivo ou script mencionado. Ler o código de verdade é parte
   do treino.
4. Conclua o checklist antes de ir para o próximo dia.