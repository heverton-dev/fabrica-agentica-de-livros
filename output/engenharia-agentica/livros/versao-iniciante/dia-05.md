# Dia 5 — Turnos agênticos: anatomia de um loop e por que ele custa dinheiro

## Meta do dia

Decompor o custo de um agente em **turnos**, medir o custo real de uma
sessão, identificar as três fontes de vazamento mais comuns e aprender a
reduzir o número de turnos — a alavanca mais rentável que existe.

## A ideia em uma frase

O custo de um agente é o custo do **prefixo reenviado a cada turno** — e o
prefixo é justamente o que ninguém olha.

---

## A explicação simples

Um **turno agêntico** é uma iteração completa do ciclo:

1. o modelo recebe o estado atual;
2. decide uma ação — responder ou chamar uma ferramenta;
3. o harness executa;
4. o resultado volta para o modelo.

Cada iteração é uma **chamada nova de inferência**. Não existe memória: o que
o modelo "sabe" é exatamente o que o harness acabou de enviar.

Agora o ponto que muda tudo. Numa sessão de 20 turnos, no turno 20, o harness
envia: a instrução persistente, a definição de todas as ferramentas, o
histórico completo dos 19 turnos anteriores e o resultado da última ação.

> **O custo de entrada cresce de forma aproximadamente quadrática com o
> número de turnos.**

Não porque o modelo ficou mais caro — porque o prefixo cresce a cada passo e
é **reenviado integralmente** a cada turno.

A fórmula (não se assuste, é só para enxergar o problema):

```
Custo de entrada ≈ n·P + Σ (n − i + 1)·c_i
```

- `P` = prefixo estável (instrução + ferramentas), pago em **todos** os n turnos.
- `c_i` = conteúdo acrescentado no turno `i` (resultado de ferramenta,
  histórico), que **continua sendo pago** em todos os turnos seguintes.

Dois termos, **duas alavancas distintas**. O livro separa: Dia 6 trata do
cache do prefixo `P`; Dia 8 trata do controle do conteúdo incremental `c_i`.

### A consequência mais contraintuitiva

**Reduzir o número de turnos vale mais do que reduzir o tamanho do prompt.**

- Cortar o prefixo `P` pela metade só afeta o primeiro termo.
- Eliminar uma fração dos turnos afeta o **somatório inteiro** — o termo que
  domina o custo.

É por isso que um harness com boas verificações — que impede o agente de
tentar, errar, tentar, errar — é uma ferramenta de economia **antes** de ser
uma ferramenta de qualidade.

## As três fontes de vazamento (em ordem de impacto)

### 1. Resultado de ferramenta sem teto

Um comando que despeja 5.000 linhas de log no contexto **não custa uma vez**:
custa em todos os turnos seguintes, porque a partir dali faz parte do prefixo.
Uma única leitura descuidada no meio da sessão pode **dobrar** o custo da
segunda metade.

### 2. Turno de retrabalho

Agente que não sabe o contrato de qualidade erra, você corrige, ele erra de
outra forma. Cada ciclo adiciona conteúdo incremental que fica no histórico.
O desperdício não é o erro em si — é o **erro persistido no prefixo**.

### 3. Capacidade não usada carregada sempre

Cinquenta definições de ferramentas, das quais três são usadas na tarefa,
custam em todo turno. É o item mais fácil de corrigir e o mais ignorado.

## O efeito de segunda ordem: menos é mais

Contexto grande **degrada a atenção**. Modelos performam melhor com o
*conjunto certo* de tokens do que com o conjunto máximo.

A economia não é só financeira — é de **qualidade**. O agente que recebe menos
ruído decide melhor. Isso inverte a intuição de "mais informação é sempre
melhor" e explica por que harnesses maduros são enxutos.

## Turno ≠ sessão

- **Sessão** é a unidade de trabalho humano ("corrigir o bug 1042").
- **Turno** é a unidade de inferência.

Você otimiza por sessão (resultado por dólar) e diagnostica por turno (onde o
token foi queimado). Confundir leva a metas erradas: reduzir o custo por turno
sem olhar o número de turnos é economizar combustível **acelerando mais**.

---

## O exemplo real: os turnos da fábrica

O `proj_fabrica-de-livros` é, no fundo, uma máquina de transformar tokens em
capítulos. E ele aplica o Dia 5 no desenho do fluxo:

### Onde os turnos nascem

Abra o `AGENTS.md` na seção 5 (Fluxo Operacional). Repare na **Fase 2**:

> `pool-capitulos.py --plano --lote 4` → subagentes-redator em lotes
> (estratégia + redação + diagrama + CI + auto-validação). **Retentativa com
> backoff (máx. 3)**

Duas decisões econômicas aí:

1. **Lotes de 4, não um por um.** A esteira limita a fila para não explodir o
   consumo de uma vez (e para diagnosticar antes de replicar).
2. **Retentativa com backoff, máx. 3.** Isso é `limite_de_tentativas` — o
   contrato do Dia 5 aplicado à geração: tentar 3 vezes e parar para reportar o
   bloqueio, em vez de tentar 20 vezes variando a mesma abordagem.

### Onde os turnos são economizados (a parte que vale ouro)

A fábrica batizou suas skills de economia com os nomes exatos desta lição:

- `lean-ctx` — "grep antes de read: hierarquia de custo das operações de leitura".
  Menos conteúdo incremental: em vez de abrir o arquivo inteiro, busca antes o
  trecho. É a tática "corte de vazamento nº 1" do Dia 5 aplicada ao dia a dia.
- `headroom` — "se a saída do comando tiver mais de 7 linhas, comprima mantendo
  as **primeiras 3 e últimas 4**". A função `comprimir_saida` do Dia 5, em
  forma de política de equipe.
- `caveman` — "ultra-compressed communication mode". Instrução de estilo
  telegráfico — a tática nº 9 da tabela de redução de turnos.

Agora o mais importante. Repare na **economia do primeiro turno** no AGENTS.md:

> "grep antes de read em código/config. Limitar leitura por linha."

E na regra 8 (Fidelidade de Conteúdo):

> "arquivos em `output/**`, JSONs de estado e verificações de `auditar-obra.py`
> são isentos de compressão — leitura sempre integral."

Isso é **teto por tipo de dado**: o que é dado de trabalho da obra (conteúdo
de `output/`) nunca é cortado; o que é log intermediário sempre é. Um teto que
sabe a diferença entre carga e combustível — a mesma separação da tabela de
tetos do capítulo.

### Os turnos de confirmação, cortados na raiz

Quando a fábrica roda a suíte de testes, quem evita o "turno de confirmação"
é o **hook `pre-commit`** (R16): o teste roda *antes* do commit e *bloqueia* se
falhar. O agente não precisa reler para conferir que não quebrou nada — o
código garante. Contrato vira lei, e o retrabalho vira impossível, não apenas
indesejável.

---

## Mão na massa

### Tarefa 1 — compute o custo de uma sessão pela fórmula

Crie um script que resume turnos gravados um por linha (JSONL):

```python
#!/usr/bin/env python3
"""Resume o custo de uma sessao a partir dos registros por turno."""
import json
from pathlib import Path

PRECO_ENTRADA = 3.00 / 1_000_000      # por token
PRECO_SAIDA = 15.00 / 1_000_000
PRECO_CACHE = 0.30 / 1_000_000


def resumir(caminho):
    turnos = [json.loads(l) for l in Path(caminho).read_text(encoding="utf-8").splitlines() if l.strip()]
    entrada = sum(t["tokens_entrada"] for t in turnos)
    saida = sum(t["tokens_saida"] for t in turnos)
    cache = sum(t.get("tokens_cache_leitura", 0) for t in turnos)
    custo = entrada * PRECO_ENTRADA + saida * PRECO_SAIDA + cache * PRECO_CACHE
    return {
        "turnos": len(turnos),
        "tokens_entrada": entrada,
        "tokens_saida": saida,
        "tokens_cache": cache,
        "proporcao_cache": round(cache / entrada, 3) if entrada else 0.0,
        "custo_usd": round(custo, 4),
        "custo_por_turno": round(custo / len(turnos), 4) if turnos else 0.0,
    }


if __name__ == "__main__":
    import sys
    print(json.dumps(resumir(sys.argv[1]), ensure_ascii=False, indent=2))
```

Crie um `turnos.jsonl` com um exemplo (5 registros) e rode. O campo
`proporcao_cache` é o indicador que você quer empurrar para cima.

### Tarefa 2 — a compressão cabeça + cauda (o padrão da fábrica)

Implemente o mesmo padrão que o projeto usa em `headroom`:

```python
def comprimir_saida(texto, primeiras=3, ultimas=4, limite_linhas=200):
    """Mantem cabeca e cauda; resume o meio."""
    linhas = texto.splitlines()
    if len(linhas) <= limite_linhas:
        return texto
    cabeca = linhas[:primeiras]
    cauda = linhas[-ultimas:]
    omitidas = len(linhas) - primeiras - ultimas
    return "\n".join(cabeca + [f"... [{omitidas} linhas omitidas] ..."] + cauda)
```

Teste com um texto de 50 linhas e confirme que só o miolo some. Quando o
agente precisar do meio, ele pede um trecho específico — e aí sim paga por ele.

### Tarefa 3 — contrate o "pronto" antes da tarefa

Escreva o critério de pronto de uma tarefa sua antes de pedir ao agente:

```yaml
tarefa: corrigir-bug-1042
criterio_de_pronto:
  - "suite completa executa sem falha"
  - "teste novo cobre o caso relatado"
  - "nenhum arquivo fora de app/ foi alterado"
limite_de_tentativas: 3
ao_atingir_limite: "parar e reportar o bloqueio com a ultima falha"
```

`limite_de_tentativas` é a diferença entre um agente que converge e um que
gasta dez turnos variando a mesma tentativa.

### Tarefa 4 — projete o custo antes de gastar

Rode a projeção mental: **10 vs 20 vs 40 turnos**, mesmo prefixo. O crescimento
é visivelmente superlinear. Essa curva é o argumento mais eficaz para
convencer o time a investir em reduzir turnos em vez de micro-otimizar prompt.

### Tabela de diagnóstico: sintoma → causa → ação

| Sintoma medido | Causa provável | Ação |
|---|---|---|
| proporção de cache ≈ 0 | prefixo instável, sem cache | Dia 6: estabilizar a ordem das partes |
| entrada cresce rápido por turno | saída de ferramenta sem teto | compressão cabeça+cauda |
| muitos turnos em tarefa simples | critério de pronto ausente | declarar contrato antes da tarefa |
| custo/turno baixo, custo/sessão alto | muitos turnos | atacar causa raiz das repetições |
| erro recorrente do mesmo tipo | gate ausente | verificação em script (Dia 2) |

---

## As dez táticas para reduzir turnos (por impacto)

| # | Tática | Impacto típico |
|---|---|---|
| 1 | Critério de pronto escrito antes da tarefa | −30% a −50% |
| 2 | Teto em toda saída de ferramenta | −15% a −30% |
| 3 | Comando verboso → versão silenciosa (`-q`, `--oneline`) | −10% a −25% |
| 4 | Limite de tentativas com reporte obrigatório | −10% a −20% |
| 5 | Memória externa do que já foi lido | −10% a −20% |
| 6 | Verificação automática antes de perguntar ao humano | −5% a −15% |
| 7 | Roteamento por exigência cognitiva | −5% a −15% |
| 8 | Delegação de varredura pesada | −5% a −15% (e custo menor) |
| 9 | Instrução de estilo telegráfico na resposta | −5% a −10% |
| 10 | Reuso de resultado já obtido na sessão | −5% a −10% |

As três primeiras cobrem a maior parte do ganho — e **nenhuma exige trocar de
modelo ou de ferramenta**. A economia está na cabine, não no motor.

## Cinco erros de medição que enganam

1. **Medir só a média** — esconde a sessão de 200 turnos; acompanhe p95/máximo.
2. **Medir custo por token** — ignora retrabalho; meça por tarefa concluída.
3. **Medir só tarefas concluídas** — exclui as que falharam e consumiram.
4. **Medir sem separar por tipo de tarefa** — compara o incomparável.
5. **Medir uma vez** — decisão sobre ruído; janela mínima de duas semanas.

## Erros de julgamento deste dia

- Otimizar o turno mais caro quando o custo está distribuído em muitos turnos
  médios.
- Medir só entrada e ignorar que a saída verbosa de um turno volta como
  entrada do próximo.
- Interpretar custo alto como "modelo caro" e trocar de modelo quando o
  problema é o número de voltas.
- Cortar contexto para economizar e conseguir **aumentar** os turnos — economia
  paga com retrabalho é prejuízo disfarçado.

**Antipadrão observável:** a mesma consulta aparece repetida com variação
mínima no log. Não é o agente confuso: é o estado da tarefa que não está
escrito em lugar nenhum.

---

## Checklist do dia

- [ ] Explico por que o custo cresce com o quadrado dos turnos.
- [ ] Digo as 3 fontes de vazamento (teto, retrabalho, capacidade ociosa).
- [ ] Gravei/reconstruí o custo de uma sessão real (ou exemplo) com o script.
- [ ] Implementei a compressão cabeça + cauda.
- [ ] Escrevi um critério de pronto com limite de tentativas.
- [ ] Identifiquei onde a fábrica economiza turnos (lote, backoff, `-q`, hook).

## Para saber mais

- AGENTS.md seção 0 (Economia Severa de Tokens) — a política de teto e
  compressão da fábrica inteira.
- Skills `lean-ctx` e `headroom` da fábrica — as táticas do Dia 5 viraram
  procedimento.

No Dia 6, atacamos o termo dominante de frente: o cache de prefixo — o
desconto que existe, que é grande, e que se perde com uma única linha
instável no lugar errado.