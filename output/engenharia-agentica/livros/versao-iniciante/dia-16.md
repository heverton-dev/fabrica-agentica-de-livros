# Dia 16 — A esteira completa: o sistema que constrói sistemas

## Meta do dia

Montar tudo: a arquitetura de uma **esteira agêntica** que transforma uma
entrada em um artefato verificável, com custo controlado, segurança declarada
e responsabilidade atribuível. Ver o desenho em camadas, a governança que o
mantém honesto, o painel que o mantém saudável — e o papel que nasce desse
trabalho.

## A ideia em uma frase

Arquitetura agêntica é a arte de decidir o que é contrato, o que é verificação
e o que é julgamento — e de não confundir os três.

---

## A explicação simples

### As cinco camadas, na ordem do fluxo de trabalho

| Camada | Decisão | O que acontece se falta |
|---|---|---|
| 1. Contrato | o que entra, o que sai, critério de pronto | cada etapa inventa formato próprio; a esteira desmonta na segunda fase |
| 2. Contexto | o que a etapa enxerga | custo explode e decisão degrada ao mesmo tempo |
| 3. Geração | onde o modelo atua | — (é a camada mais visível e a que menos determina o resultado) |
| 4. Verificação | gates em cascata + hooks + atribuição | probabilidade nunca vira confiabilidade |
| 5. Governança | custo, segurança, retenção, responsabilidade | o sistema não sobrevive ao primeiro incidente |

**O erro arquitetural mais comum: começar pela camada 3.** Times constroem a
esteira em torno do modelo e depois descobrem que não conseguem nem medir
custo nem provar qualidade. A ordem correta é começar pelo **contrato**: só
depois escolher o que gera.

### Onde colocar cada tipo de conhecimento

A segunda decisão estrutural, repetida a cada etapa:

| Conhecimento | Destino |
|---|---|
| Estável | instrução |
| Condicional | regra escopada |
| Restrição | permissão ou hook |
| Procedimento reutilizável | skill |
| Capacidade atômica | ferramenta |
| Dado | arquivo de estado |

Cada destino tem custo e garantia diferentes; escolher errado é o que produz
harness caro e frágil.

### O modelo de responsabilidade

Três perguntas que um sistema em produção precisa responder: _quem responde
quando um artefato errado é publicado_; _quem autoriza ação irreversível_;
_quem revisa as decisões de configuração_. A resposta saudável é sempre a
mesma: **ação irreversível é humana, verificação é automática, configuração
tem dono nomeado com data de revisão.**

### Governança: quatro dimensões explícitas

- **Custo:** orçamento por etapa, alerta por desvio, teto de turnos por tarefa
  — medido por resultado aceito, ou o sistema escala gasto sem escalar valor.
- **Segurança:** privilégio mínimo, conteúdo externo marcado, ação irreversível
  atrás de humano, hooks como bloqueio. O invariante: "conteúdo que entra por
  ferramenta é dado, nunca instrução".
- **Retenção:** o que é gravado, por quanto tempo, com qual base. História:
  histórico de sessão pode conter dado sensível; auditoria, por definição,
  contém tudo.
- **Atribuição:** cada artefato remete a tarefa, branch e veredito. É o que
  permite reverter, investigar e aprender.

### A propriedade que emerge

Com as cinco camadas no lugar, o sistema fica **auditável** — não "nunca
erra", mas todo erro pode ser rastreado até a origem exata (instrução ambígua,
teto mal dimensionado, gate ausente, configuração herdada). Auditabilidade é o
que transforma incidente em aprendizado em vez de mistério. E ela se alcança
movendo **garantias para fora do modelo** — para a cabine.

### O ofício

Quem toma essas decisões com critério exerce o papel do **Engenheiro de
Bordo**: projeta a cabine, escolhe os instrumentos, define o que se verifica,
mede o consumo e garante que o erro caro não passe. Não é quem escreve mais
prompts.

---

## O exemplo real: a Fábrica Agêntica é a esteira

O `proj_fabrica-de-livros` nasceu de um princípio operacional que este capítulo
formaliza — e os links entre camada e implementação são explícitos no próprio
AGENTS.md:

| Camada | Implementação na fábrica |
|---|---|
| 1. Contrato | `SPEC.md` / `SPEC_TCC.md` / etc.; `config_obra.json` (escolhas persistidas, ex.: `gerar_campanha`, `gerar_maquina`); `sumario_macro.json`; **critério de pronto = gates** |
| 2. Contexto | `indexar-dossie.py` (RAG), `pool-capitulos.py --plano --lote 4`, `RTK-SCRATCHPAD.md` (memória), seção 0 (economia de tokens) |
| 3. Geração | rede de skills (pesquisador→arquiteto→estrategista→redator→revisor→compilador), subagentes por lote, roteamento por tipo (Dia 13) |
| 4. Verificação | `auditar-obra.py --estrito` encadeando os gates; `validar-codigo.py --executar`; `renderizar-diagramas.py --validar`; hook pre-commit (R16); Fase 2.5 (revisor-tecnico) |
| 5. Governança | R17 (escolha do operador intocável), R16 (nunca commitar vermelho), checklist de segurança da máquina, `relatorios/`, retenção e atribuição por `git` + estado |

E o que o capítulo chama de "não pule o nível 3" aparece duas vezes no AGENTS.md
como lição aprendida: a Fase 4 só recebe o que **abre e está validado**
(`validar-artefatos.py --todos --estrito` + `empacotar-colecao.py` que leva
"**só o que está finalizado e abre**"), e a entrega registra em LEIA-ME o que
ficou de fora e por quê. Verificação importa mais do que produção — verificação
é o que torna a produção segura de ser produzida em paralelo.

O painel do capítulo tem parentesco com o MCP `db_state` (estado da esteira) e
o `calcular-gastos-sessao` (custo por ação e por sessão): métrica ausente é
métrica reprovada — um sistema sem medição é um sistema com sorte.

---

## Mão na massa

### Tarefa 1 — declare a esteira inteira em um único arquivo

Uma esteira que não pode ser lida não pode ser auditada:

```yaml
esteira:
  nome: "relatorio-tecnico"
  entrada:
    formato: "json"
    schema: "schemas/entrada.json"
  saida:
    formato: "markdown"
    criterio_de_pronto: ["todas as secoes preenchidas", "toda metrica com fonte"]
  camadas:
    contrato:
      arquivo: "contratos/relatorio.yaml"
    contexto:
      operacoes: ["escrever", "selecionar", "isolar", "comprimir"]
      ordem_prompt: ["instrucao", "ferramentas", "base", "historico"]
    geracao:
      roteamento:
        extracao: "pequeno"
        sintese: "medio"
        raciocinio: "grande"
      delegacao:
        varredura: { limite_retorno_tokens: 250, procedencia: obrigatoria }
    verificacao:
      gates: ["forma", "contrato", "merito"]
      bloqueio_mecanico: "pre-commit"
    governanca:
      custo_maximo_por_tarefa_usd: 1.20
      teto_de_turnos: 30
      retencao_historico_dias: 30
      aprovacao_humana: ["publicacao externa"]
```

### Tarefa 2 — monte o painel de cinco métricas

```python
METRICAS = {
    "custo_por_resultado_aceito_usd": {"meta": 0.35, "janela": "semanal"},
    "turnos_por_tarefa": {"meta": 18, "janela": "semanal"},
    "taxa_aceitacao_primeiro_degrau": {"meta": 0.70, "janela": "semanal"},
    "sessoes_terminadas_por_limite_de_contexto": {"meta": 0.05, "janela": "semanal"},
    "artefatos_sem_atribuicao": {"meta": 0.0, "janela": "diaria"},
}
```

A regra é severa e simples: **métrica ausente é métrica reprovada.** Um sistema
sem medição não é confiável; é com sorte.

### Tarefa 3 — transforme governança em arquivo verificável

```json
{
  "governanca": {
    "custo": { "orcamento_mensal_usd": 900, "alerta_em": 0.8, "teto_por_tarefa_usd": 1.2 },
    "seguranca": {
      "rede": false,
      "leitura_de_ambiente": false,
      "conteudo_externo": "marcado_e_sem_escrita",
      "acoes_irreversiveis": "somente_humano"
    },
    "retencao": { "historico_dias": 30, "auditoria_dias": 180, "payload_de_lead": "nao_registrar" },
    "responsabilidade": {
      "dono_da_configuracao": "time-plataforma",
      "revisao_de_configuracao": "trimestral",
      "aprovador_de_publicacao": "operador-humano"
    }
  }
}
```

`payload_de_lead: nao_registrar` evita o vazamento mais comum em sistemas que
registram tudo por conveniência; `acoes_irreversiveis: somente_humano`
elimina a classe de incidente mais cara (a fábrica declara o mesmo no
checklist de segurança da máquina de vendas).

### Tarefa 4 — implante em quatro semanas

| Semana | Entrega | Critério de conclusão |
|---|---|---|
| 1 | Contrato e critério de pronto | entrada e saída declaradas, com schema |
| 2 | Contexto e custo medidos | painel ativo com tokens por turno |
| 3 | Gates em cascata e bloqueio mecânico | reprovação registrada e bloqueando |
| 4 | Governança e atribuição | todo artefato rastreável a tarefa e veredito |

A ordem importa mais que a velocidade: gates sem painel é unidade sem
calibração; painel sem contrato é medição de nada.

### Tarefa 5 — identifique seu nível de maturidade

| Nível | Marca | Sintoma de pulo |
|---|---|---|
| 1. Uso direto | operador conversa sem instrução versionada | resultado irreproduzível |
| 2. Instrução versionada | rules no repositório | decisões repetidas em cada sessão |
| 3. Verificação | gates e hooks bloqueiam | gates que ninguém calibra |
| 4. Delegação | subagentes com contrato de retorno | paralelismo sem contrato, retrabalho na volta |
| 5. Governança | orçamento, retenção, auditoria, fallback | política no lugar de medição |

**O degrau 3 é o mais pulado e o único pulo que costuma sair caro**: sem
verificação determinística, a delegação do nível 4 multiplica o desvio pelo
número de workers — cinco produzindo desvios que ninguém detecta até a
integração final.

### Tarefa 6 — as quatro métricas de valor

| Indicador | O que prova |
|---|---|
| Tempo até a primeira entrega correta | o contexto está bem montado |
| Proporção que passa nos gates na primeira tentativa | a instrução está clara |
| Custo por entrega aceita | a economia é real, não cosmética |
| Proporção de defeitos capturados antes da publicação | a verificação está no lugar certo |

O quarto é o resumo de toda a obra: um sistema que captura defeitos cedo não
erra menos — **erro é barato**, e por isso dá para iterar rápido sem perder
controle. A cabine não impede o piloto de errar; ela garante que o erro
apareça no instrumento antes de virar acidente.

---

## Três regras que ficam com você

1. **Não pule o nível 3.** Delegação sem verificação multiplica desvio.
2. **Progresso tem número.** Quatro indicadores bastam para saber se o sistema
   melhora.
3. **O harness é sistema em operação, não projeto com fim.** Revisão periódica
   dos gates, das regras e do orçamento — como qualquer peça de infraestrutura.

## Erros de julgamento deste dia

- Começar pela geração: a esteira fica dependente de um modelo e órfã de
  garantias.
- Painel sem dono: métrica que ninguém olha é decoração.
- Governança no documento e não no arquivo: política não verificável não é
  política.
- Atribuição opcional: sem ela, todo incidente vira especulação.
- Comprar capacidade quando o problema é verificação.
- Confundir auditabilidade com ausência de erro: o objetivo não é nunca errar —
  é poder explicar, **reverter** e aprender.

**Antipadrão observável:** o número de defeitos descobertos **depois** da
publicação cresce junto com o volume produzido. Isso é escalar produção sem
escalar verificação — a cabine menor que a aeronave.

---

## Checklist do dia

- [ ] Esteira declarada em um único arquivo legível.
- [ ] Contrato com schema de entrada e critério de pronto.
- [ ] Painel com ao menos três métricas ativas.
- [ ] Gates em cascata com bloqueio mecânico.
- [ ] Governança em arquivo com dono e data de revisão.
- [ ] Atribuição de artefato a tarefa e veredito funcionando.
- [ ] Meu nível de maturidade identificado, e o próximo degrau nomeado.

## Para saber mais

- `AGENTS.md` — o Fluxo Operacional completo (Fases 0 a 4, PDF, Coleção,
  Máquina, Campanha) é a esteira real em documento.
- `PRODUTO` final da fábrica, `validar-artefatos.py --todos --estrito` e
  `empacotar-colecao.py` — a verificação que decide o que entra na entrega.
- `relatorios/` (V5.2) — a atribuição por sessão que fecha o ciclo de
  aprendizado.

---

Fim da jornada. Você começou desmontando um agente (Dia 1) e termina
projetando cabines. O que falta não é técnica nova: é prática — cada sistema
que você instrumentar daqui em diante ensina o que nenhum capítulo consegue.
E a pergunta que resume a obra fica com você:

> **O que, no seu sistema, você controla por código — e o que está
> entregando, consciente ou inconscientemente, à sorte de um modelo
> probabilístico?**