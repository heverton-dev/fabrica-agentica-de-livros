# Dia 7 — Economia severa: as configurações reais que cortam sem cortar qualidade

## Meta do dia

Aprender as **alavancas de economia de tokens** com efeito medível — hierarquia
de leitura, teto em ferramentas, compressão de saída e limpeza de resultado
consumido — e o critério que separa economia de mesquinharia: **há tokens que
você deve gastar de propósito.**

## A ideia em uma frase

Economia severa não é cortar contexto — é **gastar o token caro só onde ele
compra decisão**.

---

## A explicação simples

Existem três alavancas, com ordens de grandeza diferentes:

| Alavanca | O que faz | Efeito |
|---|---|---|
| **NÃO buscar o que não precisa** | hierarquia de leitura | reduz entrada em ordens de magnitude |
| Comprimir o que já entrou | cabeça + cauda | reduz volume ×3 a ×10 |
| Reduzir verbosidade de saída | estilo + orçamento | corta o token **mais caro** do sistema |

A ordem importa. Comece pela alavanca mais rentável — e a mais contraintuitiva.

### A hierarquia de custo das operações de leitura

| Operação | Custo |
|---|---|
| Declarar o alvo que procura | zero |
| Buscar por padrão | algumas linhas |
| Ler um intervalo do arquivo | trecho |
| Ler o arquivo inteiro | caro |
| Ler vários arquivos | muito caro |
| Reprocessar tudo a cada turno | custo multiplicado |

Lê-se da precificação: **abrir um arquivo inteiro custa o tamanho do arquivo;
buscar por padrão custa algumas linhas; declarar onde está custa nada.** Um
agente disciplinado nunca abre um arquivo sem saber o que procura.

E tem um detalhe que o diagrama não mostra: o custo de uma leitura **não
termina nela**. Se o conteúdo entra no histórico e o prefixo é reenviado,
aquela leitura é paga em todos os turnos seguintes. A economia acontece na
**decisão de leitura** — antes de ela acontecer.

### Por que saída é mais cara que entrada

O token **gerado** custa tipicamente várias vezes o token lido. E o agente
gasta saída em três lugares: raciocínio intermediário, texto explicativo e
conteúdo real. A configuração econômica ataca os dois primeiros com
orçamento e protocolo de estilo — o conteúdo real é o único que recebe saída
generosa.

### A alavanca escondida: delegação

Um subagente com contexto próprio lê o material pesado e devolve apenas um
resumo. O pai **nunca vê** as 3.000 linhas lidas — vê 200 linhas de
conclusão. É compressão aplicada à arquitetura em vez de ao texto.

### Limite duro versus limite mole

- **Limite duro** (teto de linhas, máx. de tokens, nº de turnos): imposto pelo
  código do harness. Só nele você confia de verdade (lembra do Dia 2).
- **Limite mole** (instrução de estilo, "seja breve"): depende da obediência
  do modelo.

Duro se impõe; mole se pede. Configure os dois, mas acredite só no primeiro.

---

## O exemplo real: a seção 0 do AGENTS.md

O `proj_fabrica-de-livros` chama a seção 0 de "**Economia Severa de Tokens
(PRIORIDADE MÁXIMA)**". É o Dia 7 transformado em política de equipe. Algumas
regras, uma a uma:

### Regra 2 = a compressão que você já conhece

> "Headroom & RTK: logs/builds >7 linhas → comprimir (3 topo + 4 fim)."

É exatamente a função do Dia 5 (`primeiras=3, ultimas=4`) vingando como regra
de projeto. Mas repare no fim da regra 2 — a parte que evita o "corte
uniforme" que arruína tudo:

> "**EXCEÇÃO:** conteúdo em `output/**` e dados de obra NUNCA são comprimidos."

E a regra 8 é ainda mais explícita:

> "arquivos em `output/**`, JSONs de estado e verificações de
> `auditar-obra.py`/`validar-codigo.py`/`revisor-tecnico` são isentos de
> compressão — leitura sempre integral."

Isso é **teto por natureza de dado**, na prática: o conteúdo da obra é o
"contexto que muda uma decisão" (o schema do banco do Dia 7) — nunca cortado;
o log intermediário é "resultado de build bem-sucedido" — sempre cortado. É a
tabela de decisão do capítulo rodando em produção.

### Regra 3 = a hierarquia de leitura obrigatória

> "LeanCTX: grep antes de read em código/config. Limitar leitura por linha."

A Configuração 1 do capítulo (buscar antes de abrir, ler intervalo antes de
ler inteiro), virou regra número 3 da empresa.

### Regra 4 = delegação comprimida

> "Delegação Cavecrew: subagentes comprimidos para buscas/edições extensas
> (nunca para prosa)."

Subagente lê muito, devolve pouco — e há uma proibição de delegar o que é
caro de outra forma (prosa).

### Regra 6 = economia com respeito humano

> "Fallback Terminal: se sandbox bloquear, exibir comandos PowerShell no chat
> para o usuário rodar. / 7. Soberania do Usuário: nada é barrado sem
> confirmação explícita do operador."

Economia de tokens **não** vale para jogar o trabalho de volta — se o
sandbox falhar, o agente mostra o comando ao humano em vez de tentar 20
vezes. É o limite de tentativas do Dia 5 e a alavanca nº 4 da tabela.

### Regra 10 = a prevenção de retrabalho

> "Auto-commit/push: alterações devem ser commitadas e pushadas para manter
> grafo atualizado."

E a R16 (hook `pre-commit`): o teste roda antes do commit e **bloqueia** se
falhar. Retrabalho vira impossível por construção — o "tokem que compra
verificação" é gasto em script, não em perguntas ao modelo.

### A regra que resume o capítulo

> "9. Busca via Grafo: usar `.code-review-graph` antes de tools de
> leitura/busca."

É a hierarquia de leitura nos seus dois níveis superiores: **usar o índice do
projeto antes de abrir arquivo**. A leitura mais barata é a que não acontece.

---

## Mão na massa

### Configuração 1 — a hierarquia de leitura obrigatória

Cole na sua instrução persistente. É a regra com maior retorno por linha do
livro inteiro:

```markdown
### Ordem obrigatoria de leitura
1. Antes de abrir qualquer arquivo, declare o que procura.
2. Use busca por padrao para localizar a linha.
3. Leia apenas o intervalo necessario (offset + limite).
4. Abra o arquivo inteiro SOMENTE se ele tiver menos de 200 linhas.
5. Nunca leia dois arquivos grandes no mesmo turno.
```

### Configuração 2 — teto e compressão em toda ferramenta

Teto é **limite duro** — não depende de obediência:

```python
LIMITE_SAIDA_PADRAO = 200

def teto(texto, primeiras=3, ultimas=4, limite=LIMITE_SAIDA_PADRAO):
    linhas = texto.splitlines()
    if len(linhas) <= limite:
        return texto
    omitidas = len(linhas) - primeiras - ultimas
    return "\n".join(linhas[:primeiras] + [f"... [{omitidas} linhas omitidas] ..."] + linhas[-ultimas:])
```

Aplique a **saída de todo comando** — teste, busca, listagem de diretório,
diff, resposta de API. Mas atenção ao erro do capítulo: **teto apertado em
saída de teste que falhou é desastre** — ali o detalhe é o sinal. O erro exato
nunca é cortado.

### Configuração 3 — orçamento de saída por fase

Declare o perfil de gasto de cada fase. Isso impede o agente de escrever prosa
na fase de verificação:

```yaml
orcamento_por_fase:
  descoberta:
    tokens_saida_alvo: 800
    regra: "listar achados, sem explicar"
  geracao:
    tokens_saida_alvo: 6000
    regra: "conteudo real; nada de preambulo"
  verificacao:
    tokens_saida_alvo: 300
    regra: "apenas veredito e localizacao de falhas"
  relato:
    tokens_saida_alvo: 500
    regra: "telegrafico: caminho, numero, veredito"
teto_de_turnos_por_tarefa: 25
```

### Configuração 4 — protocolo de estilo (o limite mole)

```markdown
### Protocolo de resposta
- Sem saudacao, sem preambulo, sem reafirmar o pedido.
- Sem resumo do que acabou de ser feito, salvo pedido explicito.
- Listas em vez de paragrafos quando houver 3+ itens.
- Nunca repetir o conteudo de um arquivo ja mostrado: citar caminho e linha.
- Se a resposta passar de 400 palavras, ela precisa de subtitulos.
```

Isso é o `caveman` da fábrica, generalizado para qualquer projeto.

### Configuração 5 — limpeza de resultado já consumido

Técnica com ganho desproporcional em sessões longas: o resultado de ferramenta
que já foi usado **não deve ser pago nos turnos seguintes**:

```json
{
  "politica_resultado_ferramenta": {
    "apos_consumo": "substituir por resumo de 1 linha",
    "exemplo": "[resultado de run_tests: 34 passaram, 0 falharam]",
    "excecao": "se o agente declarar que precisara reusar, manter integral"
  }
}
```

### Configuração 6 — delegação comprimida

```yaml
subagente:
  papel: "investigador"
  entrada: "pergunta objetiva"
  saida_maxima_tokens: 250
  formato_saida: "lista de achados com caminho:linha"
  proibido: "colar trechos de codigo; apenas referenciar"
```

Sem o teto de retorno, o subagente devolve 4.000 tokens e anula o ganho.

### A tabela de decisão: onde economizar e onde NÃO

| Situação | Economizar? | Por quê |
|---|---|---|
| Ler arquivo para achar um símbolo | sim, sempre | busca responde em 1% do custo |
| Ler schema do banco antes de modelar | **não** | erro de modelo custa geração inteira |
| Verificar antes de gerar 10 páginas | **não** | previne retrabalho massivo |
| Explicar o que já foi feito | sim | não compra decisão |
| Reler o mesmo arquivo | sim (memorizar) | repetição pura |
| Instrução de critério de pronto | **não** | 200 tokens por 10 turnos poupados |
| Formatar saída de ferramenta usada | sim | resultado já consumido |

### O painel de quatro números por sessão

Economia sem medição é superstição. Quatro números, nada mais:

| Indicador | O que mede | Alarme |
|---|---|---|
| Tokens de **entrada** por turno | peso do contexto carregado | crescendo sem mudar de tarefa |
| Tokens de **saída** por turno | verbosidade do agente | muito acima da resposta útil |
| Chamadas de **ferramenta** por turno | dispersão de busca | muitas leituras, poucas decisões |
| **Turnos até a 1ª edição correta** | eficácia do contexto | alto com contexto pequeno = falta de sinal |

O quarto é o mais importante. Um agente que gasta pouco mas precisa de doze
turnos para acertar é **mais caro** do que um que gasta o dobro e acerta na
primeira vez — cada turno de retrabalho recarrega o contexto inteiro. A métrica
real não é tokens: é **tokens × turnos desperdiçados**.

### Teto duro com três camadas (o alarme programado)

- **Por turno:** limite de saída por resposta; ao atingir, resume em vez de
  continuar truncado.
- **Por tarefa:** limite acumulado; ao atingir, o sistema **grava o estado e
  devolve o controle** ao operador com resumo — nunca mata o processo no meio.
- **Por sessão:** limite de janela; encerra com relatório — nunca com parede
  silenciosa.

A regra de projeto: **o teto nunca produz perda de trabalho.**

### Os nove vazamentos silenciosos

1. Saída de ferramenta não comprimida (build de 4.000 linhas, 20 úteis).
2. Leitura integral de arquivo grande para editar três linhas.
3. Contexto reescrito a cada turno (derrota o cache do Dia 6).
4. Listagem recursiva de diretório inteiro.
5. Dois subagentes investigando a mesma pergunta (falta de contrato).
6. Verbosidade de estilo — explicações do que acabou de fazer.
7. Retentativa sem diagnóstico — rodar de novo o comando que falhou sem ler o
   erro.
8. Instrução duplicada lida três vezes (a tesoura de boilerplate).
9. Contexto de ferramenta consumido que nunca é descartado.

Isolado, cada um é irrelevante. Somados, explicam por que duas equipes com o
mesmo modelo têm custos com uma **ordem de grandeza** de diferença. A diferença
raramente está no modelo — está no número de torneiras abertas.

---

## Três regras que ficam com você

1. **Meça por origem.** Sem saber qual bloco consumiu mais, todo corte é
   palpite.
2. **Teto nunca trunca em silêncio.** Ao atingir o limite, resuma e sinalize.
3. **Economia que aumenta retrabalho não é economia.** Compare custo por
   entrega aceita, nunca custo por turno.

## Erros de julgamento deste dia

- Cortar em **todas** as saídas igual — truncar o log de erro destrói o sinal
  mais valioso da sessão.
- Otimizar o turno isolado e ignorar o custo da tarefa.
- Contar tokens sem **atribuição por origem** — sem saber de onde eles vêm,
  não há corte defensável.
- Tratar orçamento como assunto financeiro e não como **critério de
  engenharia**.
- Economizar no lugar errado: cortar o schema antes de modelar e deixar a
  prosa de 400 palavras intacta.

---

## Checklist do dia

- [ ] Explico as 3 alavancas em ordem de impacto (ler, comprimir, saída).
- [ ] Escrevi a hierarquia de leitura obrigatória na instrução persistente.
- [ ] Apliquei teto a todas as ferramentas — com a exceção do log de erro.
- [ ] Ativei a política de limpeza de resultado consumido.
- [ ] Declarei orçamento de saída por fase.
- [ ] Montei o painel de 4 números e anotei "turnos até a 1ª edição correta".
- [ ] Identifiquei as 3 torneiras abertas mais gordas do meu fluxo.

## Para saber mais

- `AGENTS.md` seção 0 (Economia Severa de Tokens) — as 12 regras: `headroom`
  (compressão 3+4), `lean-ctx` (hierarquia de leitura), `caveman` (estilo
  telegráfico), regra 8 (fidelidade de conteúdo — a exceção que salva o dado
  de obra).
- Skills `lean-ctx`, `headroom`, `caveman` da fábrica — as alavancas deste dia
  viraram procedimento executável.

No Dia 8, você generaliza tudo: as **quatro operações de contexto** —
escrever, selecionar, comprimir e isolar — e deixa de economizar caso a caso
para **projetar harnesses que já nascem econômicos**.