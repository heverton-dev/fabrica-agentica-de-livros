# Plano de Reescrita — Edição Prática v4.0

Escopo aprovado pelo operador: reescrever a obra **no mesmo slug**
(`livros/tratado-4-camadas-v2`), em **linguagem simples** (senioridade iniciante),
com um **fio condutor prático aplicável ao projeto real do leitor** e um
**caso-âncora completo de apoio** (Painel de Pedidos). Tamanho **GG**: 4 partes,
16 capítulos, ~400.000 caracteres.

Backup da versão anterior (G, 12 capítulos):
`revisao/backups/20260914-081254-obra/`

## O que muda em relação à v3.0 (base)

| Dimensão | v3.0 (base) | v4.0 (esta edição) |
|---|---|---|
| Arquitetura | 3 partes, 12 capítulos | 4 partes, 16 capítulos |
| Linguagem | iniciante, densa | iniciante, simples e direta |
| Fio condutor | sala de controle soberana | bancada do projeto vivo |
| Persona | Engenheiro Agêntico | Engenheiro de Bancada |
| Prática | exemplos por capítulo | um projeto real atravessa a obra inteira |
| Caso âncora | Projeto Arsenal / AIDD | Painel de Pedidos (conferência de pedidos) |
| Estilo técnica | operacional | híbrido (código curto ou artefato real) |
| Gates novos | — | `categoria_tecnica: true` (R-CLI opt-in) |

## Estrutura (16 capítulos)

- **Parte I — A Bancada Antes da Primeira Peça:** 1 A conta que ninguém quer
  pagar · 2 O dicionário de bancada · 3 O seu projeto na bancada · 4 A
  Constituição da bancada
- **Parte II — As Quatro Peças:** 5 Contexto · 6 Harness · 7 Motor · 8
  Ferramentas e persistência
- **Parte III — Montagem: O Projeto Real de Ponta a Ponta:** 9 Primeiro encaixe
  · 10 O caso âncora completo · 11 Trabalho em paralelo · 12 Os portões finais
- **Parte IV — Escala, Custo e Soberania:** 13 Economia · 14 Certificado de
  bancada · 15 Adoção no time · 16 Soberania

Cada capítulo carrega, no `sumario_macro.json`, quatro campos novos que amarram
o fio condutor prático: `ancora_visual`, `entrega_tecnica`,
`aplicacao_no_projeto` e `caso_ancora`.

## Progresso

| Capítulo | Estado | Caracteres | Refs |
|---|---|---|---|
| 1 A conta que ninguém quer pagar | concluído | ~28.400 | 29 |
| 2 O dicionário de bancada | concluído | ~24.600 | 23 |
| 3 a 16 | pendentes | — | — |

## Procedimento por capítulo (receita verificada nos capítulos 1 e 2)

1. Ler as especificações do capítulo no `sumario_macro.json` (objetivo, 3
   pilares, âncora visual, entrega técnica, aplicação no projeto, caso âncora) e
   a entrada correspondente em `metricas_obrigatorias`.
2. Remover o capítulo antigo (`rm capitulos/cap_N.md`) — o backup já existe.
3. Escrever o capítulo em EITA-V2 de 7 seções, 24.000 a 30.000 caracteres, com:
   - ponte nomeada para o capítulo anterior na Introdução;
   - Explica com subseções 2.x, no máximo 2 citações por parágrafo;
   - Ilustra com o vocabulário da bancada + 1 bloco `mermaid` com
     `%% legenda:` e no máximo 12 nós;
   - Técnica com sub-títulos `###`, artefatos reais (python/json/yaml/bash) e
     portões de saída binária;
   - Aplica com cena de contraste em 2ª pessoa (situação, erro, diagnóstico,
     correção), tabela de métricas, armadilhas e um parágrafo de limites de
     escala (R-ES exige termo de limite em contexto de advertência);
   - Conclusão com 3 pontos, **Desafio** e ponte para o próximo capítulo.
4. Citar com marcadores `[ref:<chave>]` (chaves em
   `revisao/pool-referencias.json`) e aplicar:
   `python revisao/ferramentas_citacao.py --aplicar capitulos/cap_N.md`
   - Mínimo de 20 referências por capítulo (R4). Se ficar abaixo, acrescentar
     citações reais em parágrafos já existentes e reaplicar; quando o capítulo
     já estiver numerado, anexar as novas entradas como [N+1], [N+2] no fim da
     seção 7 (a ordem ascendente é o que o gate R15 verifica).
   - Números inventados do caso âncora só podem aparecer em tabela, bloco de
     código ou rótulos do template (Métricas, Armadilhas, cena) — nunca em
     parágrafo corrido, para não reprovar no R-AF.
5. Rodar os gates do capítulo:
   ```bash
   python scripts/validar-codigo.py livros/tratado-4-camadas-v2 --capitulo N --estrito --executar
   python scripts/validar-metricas.py livros/tratado-4-camadas-v2 --capitulo N --estrito
   python scripts/validar-escala.py livros/tratado-4-camadas-v2 --capitulo N --estrito
   python scripts/validar-afirmacoes.py livros/tratado-4-camadas-v2 --capitulo N --estrito
   ```
   (a métrica declarada no sumário precisa aparecer no capítulo com citação [N]
   no mesmo parágrafo — R-MT-2/R-MT-3)
6. Marcar no pool: `python scripts/pool-capitulos.py livros/tratado-4-camadas-v2 --registrar N --sucesso`

## Fechamento (quando os 16 estiverem prontos)

```bash
python scripts/auditar-obra.py livros/tratado-4-camadas-v2 --estrito
python scripts/validar-codigo.py livros/tratado-4-camadas-v2 --estrito --executar
python scripts/validar-referencias.py livros/tratado-4-camadas-v2 --estrito
python scripts/validar-fontes.py livros/tratado-4-camadas-v2 --estrito
python scripts/renderizar-diagramas.py livros/tratado-4-camadas-v2 --capitulos --validar
python scripts/gerar-capa.py livros/tratado-4-camadas-v2 --tipo livro
python compilar-para-pdf.py livros/tratado-4-camadas-v2 --paginas-exatas
python scripts/extrair-passos-praticos.py livros/tratado-4-camadas-v2   # playbook
python scripts/colecao.py --sincronizar --slug livros/tratado-4-camadas-v2
python scripts/empacotar-distribuicao.py livros/tratado-4-camadas-v2
python -m pytest -q
```

Relatório de sessão em `relatorios/<data>-<tema>.md` (+ PDF) conforme a
convenção V5.2 do `AGENTS.md`.
