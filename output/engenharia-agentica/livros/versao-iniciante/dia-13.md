# Dia 13 — Roteamento de modelo: o cérebro certo para cada tarefa

## Meta do dia

Entender que **cada tarefa tem um modelo ideal** — e que escolher "o mais
forte para tudo" ou "o mais barato para tudo" é decidir por hábito, não por
critério. Aprender a classificar tarefas e montar uma **cascata de modelos**.

## A ideia em uma frase

Roteamento é a otimização que não exige abrir mão de nada — desde que você
meça **qualidade por tarefa**, e não por sensação.

---

## A explicação simples

### O que muda quando você roteia

Em vez de uma escolha única e global de modelo, o roteador decide **chamada a
chamada**: qual modelo para qual tarefa. A observação que sustenta tudo é
econômica: para a maior parte das consultas, um modelo **menor** entrega
resultado equivalente ao **maior**, por uma fração do custo. O trabalho do
roteador é identificar quais consultas são essas.

### A exigência cognitiva, não o tamanho do prompt

A dimensão que organiza a escolha é **quanto raciocínio a tarefa exige**. Três
perfis:

| Perfil | O que é | Exemplos | Modelo típico |
|---|---|---|---|
| Transformação | aplica regra conhecida à entrada | extrair campos, classificar, resumir em N palavras, traduzir | pequeno |
| Síntese | combina informações dispersas em algo novo | parecer, desenho de solução, revisão de documento | médio |
| Raciocínio profundo | passos interdependentes, decisões que mudam o caminho | depurar bug sutil, decidir arquitetura | grande |

**Transformação é onde mora o dinheiro economizado** — é previsível,
verificável, e quase sempre resolvida por modelo pequeno.

### Três estratégias, que se combinam

1. **Roteamento por regra** — metadados da tarefa decidem (tipo da operação,
   tamanho, fase). Determinística, gratuita, auditável. Uma linha de
   configuração vale mais que um condicional escondido.
2. **Roteamento por cascata** — tenta o barato; se a **verificação** falhar,
   escala. Sem gate, cascata é aposta; com gate, é economia com garantia. É a
   estratégia deste livro.
3. **Roteamento aprendido** — um classificador aprende qual modelo usar.
   Sofisticado, caro de manter; só compensa com volume alto.

### O erro de medir custo por token

A métrica que decide é **custo por resultado aceito**: quanto custa uma tarefa
que **passou na verificação**, já contando turnos e retrabalho. Um modelo barato
que falha e escala é mais caro que começar pelo caro — por isso a **taxa de
acerto do primeiro degrau** da cascata é o número mais importante.

### As duas armadilhas clássicas

- **Rotear por sensação**: "o modelo pequeno não serve para isso" — sem nunca
  ter testado com medição.
- **Rotear por preço unitário**: sempre o mais barato, ignorando que os turnos
  extras e o retrabalho custaram mais.

A mesma métrica resolve as duas: **custo por tarefa concluída com verificação
aprovada**.

### O que torna tudo seguro: o contrato

O harness não depende de um modelo específico porque o **contrato** (formato de
saída, esquema, critério de pronto) é verificado externamente. Trocar de
modelo vira um **parâmetro**, não uma reescrita. É o Capítulo 1 de novo: o que
garante o resultado é a cabine, não o piloto.

---

## O exemplo real: a fábrica já roteia por natureza

O `proj_fabrica-de-livros` não chama isso de roteamento, mas faz exatamente
isso — e está registrado em `scripts/tipos_obra.py`:

| Tipo | Natureza | Custo LLM |
|---|---|---|
| Livro | geração | alto |
| TCC | geração | alto |
| Artigo | compressão | baixo |
| E-book | compressão | baixo |
| Playbook | extração | zero |
| Lead Magnet | extração | zero |
| Deck | extração | zero |
| E-mails | extração | baixo |

A natureza (geração/compressão/extração) É a classificação por exigência. Cada
tipo tem seu produtor certo:

- **geração** (expansão!) → `redator-eita` / `redator-academico` — o modelo
  grande, porque está criando conteúdo novo a partir de dossiê;
- **compressão** (artigo/e-book) → reescrita sobre conteúdo já escrito, custo
  baixo;
- **extração** (playbook, deck, lead magnet) → **scripts determinísticos,
  custo zero** — nem modelo usa. É rotear para o degrau "sem LLM".

A regra de derivação do AGENTS.md reforça o critério:

> "Cascateie onde comprime, faça fan-out onde expande. Compressão/extração são
> baratas; expansão (ex.: TCC → livro) custa geração."

E o R6 (`model: inherit`) diz que nenhum agente fixa modelo no arquivo — a
escolha é parâmetro de configuração, exatamente o que este capítulo
prescreve. O **revisor-tecnico** é o gate: um degrau de verificação que roda
por script (`auditar-obra.py --estrito`) e não deixa resultado ruim passar de
fase só porque o gerador achou bom.

---

## Mão na massa

### Tarefa 1 — escreva a matriz de roteamento como configuração

Roteamento por regra precisa ser legível e versionado. Cada linha nomeia o
modelo **e a verificação** — uma tarefa sem verificação declarada não pode ir
para o modelo pequeno:

```yaml
roteamento:
  extracao-campos:
    modelo: pequeno
    verificacao: "schema json obrigatorio"
  resumo-curto:
    modelo: pequeno
    verificacao: "limite de palavras + 3 entidades citadas"
  parecer-tecnico:
    modelo: medio
    verificacao: "secoes obrigatorias + citacao de caminho:linha"
  escrita-longa:
    modelo: grande
    verificacao: "estrutura + consistencia entre secoes"
  depuracao-multi-passo:
    modelo: grande
    verificacao: "teste que falhava agora passa"
  decidir-arquitetura:
    modelo: grande
    verificacao: "revisao humana obrigatoria"
```

### Tarefa 2 — implemente a cascata com escalonamento

```python
DEGRAUS = ["pequeno", "medio", "grande"]
MAX_TENTATIVAS = 2


def executar_com_cascata(tarefa, executar_modelo, verificar):
    inicio = DEGRAUS.index(tarefa.get("modelo_inicial", "pequeno"))
    historico = []
    for tentativa in range(MAX_TENTATIVAS):
        degrau = min(inicio + tentativa, len(DEGRAUS) - 1)
        modelo = DEGRAUS[degrau]
        saida = executar_modelo(modelo, tarefa)
        veredito = verificar(tarefa, saida)
        historico.append({"modelo": modelo, "aprovado": veredito["aprovado"],
                          "motivo": veredito.get("motivo", "")})
        if veredito["aprovado"]:
            return {"saida": saida, "modelo_final": modelo, "historico": historico}
    return {"saida": None, "modelo_final": None, "historico": historico,
            "escalar_humano": True}
```

Dois detalhes de projeto: o `historico` é obrigatório (sem ele você não
descobre se o primeiro degrau acerta 90% ou 30% das vezes); e `escalar_humano`
é **resultado legítimo** — duas reprovações significam julgamento humano, não
capacidade a mais.

### Tarefa 3 — meça custo por resultado aceito

```python
PRECOS = {"pequeno": 0.6, "medio": 3.0, "grande": 15.0}  # por milhão de tokens de saída


def custo_por_aceito(execucoes):
    aceitas = [e for e in execucoes if e["aprovado"]]
    gasto_total = sum(e["custo"] for e in execucoes)
    return {
        "tarefas": len(execucoes),
        "aceitas": len(aceitas),
        "taxa_aceitacao": round(len(aceitas) / len(execucoes), 3) if execucoes else 0.0,
        "gasto_total": round(gasto_total, 4),
        "custo_por_aceita": round(gasto_total / len(aceitas), 4) if aceitas else None,
        "tentativas_medias": round(sum(e["tentativas"] for e in execucoes) / len(execucoes), 2),
    }
```

`custo_por_aceita` é a métrica de decisão. Compare "sempre o grande" com a
cascata: quando o primeiro degrau tem taxa alta de aceitação, a economia é
expressiva **sem perda de qualidade medida** — mas o número exato é da sua
tarefa, não deste livro.

### Tarefa 4 — monte um conjunto de avaliação

Roteador é código; código precisa de teste. Um conjunto pequeno e estável de
tarefas com resultado esperado, rodado a cada mudança de regra. Sem ele, você
não sabe se a economia veio de sabedoria ou de sorte.

### Tabela de decisão: qual degrau para qual tarefa

| Sinal da tarefa | Degrau | Verificação |
|---|---|---|
| Saída cabe em esquema fechado | pequeno | validador de esquema |
| Classificação com poucas categorias | pequeno | pertence ao enum |
| Resumo com limite objetivo | pequeno | limite + entidades citadas |
| Síntese com estrutura obrigatória | médio | seções e citações |
| Escrita longa e coerente | grande | consistência entre seções |
| Múltiplos passos com decisões encadeadas | grande | teste que exercita o caminho |
| Decisão irreversível | grande + humano | revisão humana |

### Três regras que constroem o dia

- **Determinístico antes de semântico.** Comece por regras auditáveis; um
  classificador só entra com evidência (e atrás de um piso mínimo de modelo).
- **Piso mínimo sempre.** Nenhuma economia justifica mandar tarefa de
  julgamento para um modelo abaixo do piso — ela passar nos gates de forma e
  falhar no mérito é a falha mais cara, porque não gera alarme.
- **Trade de cascata só com gate.** Sem verificação, "modelo pequeno primeiro"
  é retry caro, não economia.

---

## Três regras que ficam com você

1. **Roteie por natureza da tarefa, não por preferência.** Transformação vai
   para o pequeno; julgamento tem piso.
2. **Meça custo por resultado aceito.** A única métrica que enxerga retrabalho.
3. **Fallback deixa marca.** Artefato produzido em modo degradado carrega o
   registro da degradação — senão a revisão não sabe onde olhar.

## Erros de julgamento deste dia

- Roteador promovido sem conjunto de avaliação.
- Tarefa de julgamento roteada para baixo do piso (aprovação falsa).
- Identicador: mesma tarefa com qualidade visivelmente diferente entre
  execuções sem a entrada mudar = roteamento instável. Roteamento precisa ser
  auditável: mesmo caso, mesma escolha.
- Confiar em custo por token, que ignora turnos.
- Fallback silencioso, produzindo artefato degradado sem marca.

**Antipadrão observável:** a fase de entusiasmo em que o time manda quase tudo
para o modelo pequeno e descobre o custo nas revisões. O caminho certo é o
inverso: **roteamento conservador por padrão, expandido por evidência.**

---

## Checklist do dia

- [ ] As cinco tarefas mais frequentes classificadas por exigência cognitiva.
- [ ] Matriz de roteamento escrita com verificação por linha.
- [ ] Cascata de dois degraus implementada com histórico.
- [ ] Custo por resultado aceito medido contra o cenário anterior.
- [ ] Conjunto de avaliação criado para mudanças de regra.
- [ ] Piso mínimo definido para tarefas de julgamento.

## Para saber mais

- `scripts/tipos_obra.py` — a matriz natureza × custo LLM × produtor da fábrica.
- Regra de derivação (AGENTS.md): cascatear onde comprime, fan-out onde expande.
- `.claude/settings.json` e R6 (`model: inherit`) — modelo como parâmetro, não
  como lógica.

No Dia 14, a parte que ninguém documenta: **as configurações que existem, têm
efeito real — e não produzem nenhum aviso quando estão erradas.**