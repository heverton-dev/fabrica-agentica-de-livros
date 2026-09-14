# Dia 9 — Scripts e gates: o determinismo que sustenta a esteira

## Meta do dia

Entender o **gate** — o único componente do harness que nunca mente — e
aprender a escrever gates que reprovam de verdade, encadeá-los na ordem
certa e transformar "confie em mim" em veredito de código.

## A ideia em uma frase

O gate é o único componente que nunca mente — por isso **ele decide, e o
modelo apenas executa**.

---

## A explicação simples

### O que é um gate

Um **gate** é um programa determinístico que recebe um artefato, avalia um
contrato e devolve um veredito com **código de saída**. Três propriedades o
definem:

1. **Binário** — passa ou não passa. Sem "quase", sem "mais ou menos".
2. **Reprodutível** — mesma entrada, mesmo veredito, mil vezes.
3. **Localizado** — informa onde falhou, não apenas que falhou.

A terceira é a que vale ouro. "Documento inválido" obriga a investigar;
"`cap_07.md` seção 4: zero blocos de código" entrega a correção pronta — e a
mensagem localizada vira **instrução precisa** para o próximo turno do agente.
O gate transforma tentativa e erro em execução dirigida.

### As três famílias de gate

| Família | Verifica | Custo | Força |
|---|---|---|---|
| **Forma** | estrutura sintática: JSON parseável, seção presente, arquivo existe | milissegundos | elimina a classe de erro mais estúpida e mais frequente |
| **Contrato** | regras de negócio declaradas: mínimo de referências, formato de citação | pouco | é onde vive a maior parte do valor — política vira código |
| **Mérito** | se o artefato funciona: código executa, teste passa | mais (executa de verdade) | o mais convincente — toca o mundo |

**A ordem não é opcional: forma → contrato → mérito.** A razão é a mesma do
Dia 2: verificação barata primeiro. Rodar um teste de integração em um
documento que falha na checagem de estrutura é queimar orçamento em artefato
já condenado.

### A LEI do capítulo

> **Nunca commite (ou promova) com o gate vermelho.**

Um gate que às vezes é ignorado é **pior do que gate nenhum** — destrói a
associação entre veredito e verdade. A regra prática: transformar o gate em
**bloqueio mecânico** — hook de commit, proteção de branch, etapa obrigatória
no pipeline.

### Os dois erros simétricos

- **Usar o modelo como gate.** "Confira se está tudo certo" é verificação
  probabilística com custo alto e resultado variável. Modelo gera e sugere;
  **código julga.** (Você já sabia disso desde o Dia 2.)
- **Gate sem manutenção.** Vira ruído (reprova tudo → todos ignoram) ou vira
  decoração (nunca reprova → todos se acham protegidos).

### A ideia que dá nome ao capítulo

**Scripts são o substrato dos gates.** Todo gate é um script — e um script
bem escrito tem uma qualidade que o prompt não tem: **é testável**. Você pode
escrever um teste para o gate. Isso cria a hierarquia de confiança: o gate
confia no artefato, o teste confia no gate. É a única forma conhecida de
construir confiança em um sistema cujo componente central é probabilístico.

---

## O exemplo real: os gates da fábrica

O `proj_fabrica-de-livros` é, no fundo, uma **esteira de gates**. Abra o
`AGENTS.md`, seção 2, e veja a lista de "Scripts Determinísticos":

### As três famílias, em produção

- **Forma:** `validar-capa-nivel.py` (o badge de nível existe?), `secoes_eita.py`
  (parser do EITA canônico), `fatiar-obra.py`, `validar-code`.
- **Contrato:** `validar-referencias.py` (R-RF: URL/DOI reais, 4xx/DNS
  reprova), `validar-metricas.py` (R-MT: ≥1 métrica com valor+unidade+citação
  por capítulo), `validar-escala.py` (R-ES), `validar-afirmacoes.py` (R-AF:
  dado factual sem `[N]` reprova), `validar-fontes.py` (R-FT:
  hierarquia A/B/C ≥70% A+B).
- **Mérito:** `validar-codigo.py --executar` (fumaça real de python/js/bash),
  `renderizar-diagramas.py --validar` (o Mermaid compila de verdade).

### O encadeador é o `auditar-obra.py`

O `AGENTS.md` conta o segredo do encadeamento:

> "`auditar-obra.py --estrito` os encadeia (referências offline)."
> "gates_conteudo no tipo `livro` — registrados em `tipos_obra.py`"

O registro declarativo em `tipos_obra.py` (campo `gates_conteudo`) é o
**encadeador** do capítulo: adicionar um gate novo = uma entrada no registro,
sem reescrever a cadeia inteira. A ordem econômica (barato primeiro) e o
carregamento dos gates são decisão de dados, não de código espalhado.

### A resposta à falha com motivo localizado

O gate da Fase 2.5 (`revisor-tecnico`) recebe a saída dos gates e a usa para
**corrigir em paralelo** o lote defeituoso. A mensagem localizada do gate vira
o prompt do revisor — exatamente o efeito colateral louvado no capítulo.
Sem localização (arquivo, seção, regra), o revisor teria que adivinhar; com
ela, corrige em um turno.

### O gate de escopo, força de lei

A fábrica faz da disciplina de escopo uma regra: na entrevista inicial, o
operador escolhe se quer CAMPANHA/MÁQUINA no fluxo (R17), e o fluxo *respeita*
essa escolha "sem tratar como falha". E a Regra 12 exige personalizar a
máquina de vendas com um **gate literal**: `grep 'Autor Digital|centenas de
pessoas'` retornando **vazio** — copy genérica reprova, e com motivo claro.

### A R16 é a lei do gate em ação

> "APÓS TODA nova implementação: rodar a suíte → 100% → commit + push; <100%
> → corrigir a causa, re-testar até 100% (nunca commitar suíte vermelha;
> nunca contornar o teste)."

Frase normativa do capítulo, transformada em regra da empresa. E no Dia 10
você verá como ela virou **mecânica** (o pre-commit).

---

## Mão na massa

### Tarefa 1 — um gate de cada família

**Forma** (estrutura mínima):

```python
import re
from pathlib import Path

SECOES = ["Introducao", "Explica", "Ilustra", "Tecnica", "Aplica", "Conclusao", "Referencias"]

def verificar(caminho):
    texto = Path(caminho).read_text(encoding="utf-8", errors="replace")
    erros = []
    for nome in SECOES:
        if not re.search(rf"^##\s*\d*\.?\s*{nome}", texto, re.MULTILINE | re.IGNORECASE):
            erros.append(f"{caminho}: secao ausente -> {nome}")
    return erros

print("\n".join(verificar("cap_09.md")))
```

**Contrato** (regras do domínio): o padrão padrão — citações citadas precisam
existir nas referências:

```python
import re

MIN_REFERENCIAS = 20

def verificar(caminho):
    texto = Path(caminho).read_text(encoding="utf-8", errors="replace")
    secoes = re.split(r"^##\s*\d*\.?\s*", texto, flags=re.MULTILINE)
    corpo = "\n".join(secoes[:-1])
    refs = secoes[-1] if secoes else ""
    citadas = {m for m in re.findall(r"\[(\d{1,3})\]", corpo)}
    listadas = {m for m in re.findall(r"^\[(\d{1,3})\]", refs, re.MULTILINE)}
    orfas = sorted(citadas - listadas, key=int)
    erros = []
    if orfas:
        erros.append(f"{caminho}: citacoes sem referencia -> {', '.join(orfas)}")
    if len(listadas) < MIN_REFERENCIAS:
        erros.append(f"{caminho}: {len(listadas)} referencias (minimo {MIN_REFERENCIAS})")
    return erros
```

**Mérito** (executa de verdade): rode cada bloco de código do documento por
`py_compile` — o fumaça mínimo — e reprove o que não compila.

### Tarefa 2 — o encadeador que para no primeiro erro

```bash
#!/usr/bin/env bash
set -euo pipefail

ARTEFATO="${1:?uso: auditar.sh <arquivo>}"

python scripts/gate_forma.py "$ARTEFATO"
python scripts/gate_contrato.py "$ARTEFATO"
python scripts/gate_merito.py "$ARTEFATO"

echo "[OK] $ARTEFATO aprovado nos tres niveis"
```

O `set -euo pipefail` é a peça que torna o encadeamento confiável: qualquer
falha interrompe, erro dentro de pipe não passa silencioso.

### Tarefa 3 — o gate que deixa rastro

Registre o veredito de cada etapa — **inclusive os gates não executados**:

```json
{
  "artefato": "cap_09.md",
  "gates": [
    { "nome": "forma", "resultado": "aprovado", "duracao_ms": 12 },
    { "nome": "contrato", "resultado": "reprovado",
      "motivos": ["citacoes sem referencia -> 19, 21"] },
    { "nome": "merito", "resultado": "nao executado" }
  ],
  "veredito": "reprovado"
}
```

Registrar "não executado" mostra que a esteira parou na ordem correta.

### Tarefa 4 — a calibração dupla

Um gate testado só de um lado é um gate pela metade:

1. **Injete um erro de propósito** → confirme que o gate reprova.
2. **Injete uma mudança legítima** → confirme que ele deixa passar.

Essas duas linhas, no dia da criação, evitam o ciclo clássico: gate rigoroso →
reprova caso legítimo → é desligado na primeira semana.

### Tarefa 5 — o gate em vinte minutos

A receita em cinco passos:

1. **Nomeie o critério em uma frase afirmativa.** "Nenhum capítulo tem menos de
   três citações." Se não tem a frase, o critério está vago.
2. **Converta em comando.** Uma expressão que devolva zero ou não zero. Juízo
   subjetivo não é gate — é revisão.
3. **Decida o momento de disparo.** O gate no momento errado é ruído.
4. **Defina a resposta à falha.** Bloquear, avisar ou registrar — escolha de
   risco, não de estética.
5. **Registre o resultado.** Sem rastro, o gate vira folclore.

### Indicadores de calibração (o gate está funcionando?)

| Indicador | Saudável | Problema |
|---|---|---|
| Reprovações por semana | 5% a 40% | 0% = gate fraco ou desativado |
| Reprovação revertida por humano | < 10% | contrato mal escrito |
| Tempo do gate de forma | < 100 ms | lento demais para rodar sempre |
| Motivos com localização | 100% | motivo genérico não orienta |
| Gates novos por trimestre | 1 a 3 | zero = esteira estagnada |

---

## Três regras que ficam com você

1. **Todo gate é testado nos dois sentidos.** Com erro injetado, reprova; com
   mudança legítima, passa.
2. **Mensagem de falha aponta o local.** Diagnóstico na saída reduz um turno de
   investigação.
3. **Gate sem dono é gate morto.** Cada critério tem quem responde por ele.

## Erros de julgamento deste dia

- Tratar o veredito do gate como opinião e silenciar o que incomoda.
- Escrever gate para critério subjetivo — produz discussão em vez de decisão.
- Deixar a mensagem vaga ("estrutura inválida") — obriga o operador a fazer o
  trabalho que a máquina deveria ter feito.
- Acumular gates sem remover os que não correspondem mais ao risco.
- Rodar mérito antes de forma — queima execução em artefato já condenado.

**Antipadrão observável:** um gate sempre ignorado pelo time **já foi
desativado na prática**. Gate sem custo de desobediência é decoração.

---

## Checklist do dia

- [ ] Explico as 3 famílias de gate e a ordem (forma → contrato → mérito).
- [ ] Escrevi um gate com veredito binário e motivo localizado.
- [ ] Montei o encadeamento que para no primeiro erro (`set -euo pipefail`).
- [ ] Registro de auditoria gravando também os não executados.
- [ ] Fiz a calibração dupla (erro injetado reprova; mudança legítima passa).
- [ ] Sei onde a fábrica encadeia seus gates (`auditar-obra.py --estrito`).

## Para saber mais

- `AGENTS.md` seção 2 (Scripts Determinísticos) e a Fase 2.5 — a lista de
  gates da fábrica e como `auditar-obra.py --estrito` os encadeia.
- `scripts/tipos_obra.py` — o campo `gates_conteudo`: adicionar um gate novo é
  uma entrada declarativa, não mais edição de cadeia.
- R16 no `AGENTS.md` — "nunca commitar suíte vermelha".

No Dia 10, você conecta esse determinismo ao ciclo de vida do agente: **os
hooks** — a única parte do harness que decide antes do dano acontecer.