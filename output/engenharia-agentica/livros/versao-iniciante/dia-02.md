# Dia 2 — Probabilismo e determinismo: onde cada um manda

## Meta do dia

Classificar qualquer tarefa de IA em **4 faixas de confiabilidade** e decidir,
para cada uma, quem deve decidir: o **modelo** (probabilístico) ou o **código**
(determinístico). No final, você constrói seu primeiro **gate** — uma
verificação automática que reprova artefato ruim antes que ele avance.

## A ideia em uma frase

Você não consegue fazer o modelo de IA ser 100% confiável — mas consegue
fazer a **verificação** ser 100% confiável. Não adianta tentar estourar a
loteria; você controla é o portão por onde o resultado passa.

---

## A explicação simples

No Dia 1 você aprendeu que o modelo é probabilístico. Agora vem a pergunta
incômoda: **você não consegue deixá-lo determinístico?**

Não adianta colocar temperatura zero, fixar uma semente ou repetir o prompt
idêntico. A saída ainda varia. Por quê? Porque gerar texto é *amostrar de uma
distribuição de probabilidades* — o modelo escolhe palavras segundo chances,
não segundo certezas. E a variação não vem só da "temperatura": mudanças na
ordem dos resultados de busca, no tamanho das saídas truncadas, na versão do
modelo... tudo isso muda o resultado.

Mas existe um detalhe que muda tudo: **a verificação sim, essa é
determinística.**

Quando um teste roda e falha, a resposta é binária, reprodutível e auditável:

- "O JSON é válido?" → sim ou não. A mesma entrada, o mesmo veredito, sempre.
- "Há alguma citação sem referência?" → sim ou não. Sempre igual.
- "O código compila?" → sim ou não. Sempre igual.

Nenhum desses testes usa IA. Nenhum "depende do humor". É nesse andar do
prédio que se constrói confiança.

**Regra de ouro do dia:**

> Deixe o modelo decidir o que é ambíguo; obrigue o código a garantir o que é
> crítico.

## As 4 faixas de confiabilidade

Toda tarefa com IA cai em uma de 4 faixas:

### Faixa 1 — Determinístico por construção (sem IA)

O modelo nem entra. Contar palavras, validar um JSON, checar se existe arquivo,
comparar listas. Custo quase zero, precisão total.

*Se o seu problema cabe aqui, mantenha-o aqui.*

### Faixa 2 — Determinístico por verificação (IA + script)

A produção é probabilística, mas o resultado é checável de forma objetiva:
um código que compila e passa nos testes, um documento que satisfaz um esquema.
O modelo faz o **trabalho pesado**; o script decide se **valeu a pena**.

*É a faixa mais lucrativa da engenharia agêntica.*

### Faixa 3 — Probabilístico com revisão humana

A saída é boa para acelerar, mas alguém lê antes de assinar: um parecer
técnico, a decisão da ordem de um livro, um e-mail para cliente importante.
O que você constrói aqui é **revisão eficiente**: diff pequeno, contexto claro,
critério explícito.

### Faixa 4 — Probabilístico e aceito como tal

Chuva de ideias, rascunho, títulos alternativos. Forçar controle aqui destrói
o valor. A única proteção é o **orçamento**: barato de gerar, barato de
descartar.

## Os dois erros clássicos (e o custo real)

**Erro A — Colocar na faixa 4 algo que é da faixa 2.**

Pedir ao modelo, em linguagem natural: *"confira se o schema está correto"*.
Isso é caro, lento e não confiável — quando um validador de esquema faz em
milissegundos, de graça e sem errar.

**Erro B — Colocar na faixa 1 algo que é intrinsecamente ambíguo.**

Tentar escrever uma regra determinística para *"este parágrafo está bem
escrito"* vira uma heurística frágil que rejeita texto bom e aprova texto ruim.

E existe uma **assimetria econômica** que você precisa decorar:

> Verificação é barata; geração é cara.

Um gate que reprova custa frações de centavo. Um capítulo reescrito custa
dólares e minutos. Por isso, na dúvida entre automatizar uma verificação ou
não: **automatize** — desde que ela seja objetiva.

## O efeito de segunda ordem (o mais importante)

Um harness com boas verificações **permite usar modelos mais baratos**.

Pense: se a saída está checada, o custo de errar cai. Então você pode trocar
capacidade bruta de modelo por economia. *Sem verificação, cada economia se
converte em risco.* O Dia 13 vai usar exatamente esse raciocínio para escolher
modelos — mas ele nasce aqui.

## O relatório de verificação

Um gate não serve só para reprovar. Serve para **explicar**.

Compare:

- "documento inválido" → não diz nada.
- "cap_07.md seção 4: 0 blocos de código" → diz exatamente o que corrigir.

Um bom gate devolve: **localização + grandeza + expectativa**. Com esses três,
a correção deixa de exigir investigação e vira execução. E o relatório serve
de comida para o próximo agente — e lembra que contexto é o recurso mais caro.

---

## O exemplo real: a fábrica é um monumento ao determinismo

O `proj_fabrica-de-livros` vive das faixas 1 e 2. O modelo escreve os
capítulos (faixa 2 — produção probabilística), mas dezenas de scripts
determinísticos decidem se o texto está aprovado.

Abra a pasta `scripts/` e liste os validadores:

```bash
ls scripts/ | grep -E "validar|auditar"
```

Você vai encontrar coisas como:

- `validar-codigo.py` — **executa** trechos de código dos capítulos (smoke test real). Se compila e roda, passa; senão, reprova com localização.
- `validar-referencias.py` — confere se cada URL/DOI citada existe de verdade na internet (reprova URL quebrada).
- `validar-metricas.py` — garante que cada capítulo tem pelo menos uma métrica com valor, unidade e citação.
- `auditar-obra.py` — engrena todos os gates na ordem certa, do mais barato ao mais caro.

Repare no padrão que atravessa todos: **nenhum usa LLM para decidir.** O modelo
escreve (faixa 2), o script julga (faixa 1). Exatamente o desenho deste dia.

Vejamos como o projeto enfileira as verificações na ordem certa (barato antes
de caro), no fluxo operacional do AGENTS.md:

| Fase | Gate determinístico | Faixa |
|---|---|---|
| Estrutura | `validar_capitulo.sh` (estrutura EITA) | 1 |
| Referências | `validar-referencias.py` (URL real) | 1 |
| Conteúdo | `validar-metricas.py`, `validar-afirmacoes.py` | 1 |
| Código | `validar-codigo.py --executar` (roda o código) | 1 |
| Revisão de mérito | humano (revisor técnico) | 3 |
| Capa/nível | `validar-capa-nivel.py` | 1 |

Note a última linha: até o **mérito** (parte subjetiva) tem um script
determinístico cobrindo o que é objetivo. E note a revisão humana da fase 2.5
— o `revisor-tecnico` — é faixa 3 com método, não revisão de palpite.

---

## Mão na massa

Vamos construir um **gate mínimo** — exatamente o que a fábrica usa para não
deixar passar configuração inválida.

### Passo 1: crie o gate em um arquivo `gate_config.py`

```python
#!/usr/bin/env python3
"""Gate minimo: valida o esquema de um JSON de configuracao."""
import json
import sys
from pathlib import Path

CAMPOS_OBRIGATORIOS = ("tema", "tipo_obra", "min_referencias_por_capitulo")


def validar(caminho):
    erros = []
    try:
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"JSON invalido em {caminho}:{exc.lineno}: {exc.msg}"]

    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in dados:
            erros.append(f"{caminho}: campo obrigatorio ausente -> {campo}")

    refs = dados.get("min_referencias_por_capitulo")
    if isinstance(refs, int) and not (1 <= refs <= 20):
        erros.append(f"{caminho}: min_referencias_por_capitulo fora de 1..20 -> {refs}")

    return erros


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: python gate_config.py <arquivo.json>")
        sys.exit(2)
    problemas = validar(sys.argv[1])
    for p in problemas:
        print(f"[REPROVADO] {p}")
    sys.exit(1 if problemas else 0)
```

### Passo 2: teste com um arquivo bom

Crie `config_bom.json`:

```json
{
  "tema": "logistica",
  "tipo_obra": "livro",
  "min_referencias_por_capitulo": 12
}
```

Rode:

```bash
python gate_config.py config_bom.json
echo "exit code: $?"
```

Saída esperada: nada além de `exit code: 0`. **Zero é a senha que destrava
a esteira.**

### Passo 3: teste com um arquivo ruim

Crie `config_ruim.json` — tire o campo `tipo_obra` e ponha
`min_referencias_por_capitulo: 99`:

```json
{
  "tema": "logistica",
  "min_referencias_por_capitulo": 99
}
```

Rode:

```bash
python gate_config.py config_ruim.json
echo "exit code: $?"
```

Agora deve imprimir dois `[REPROVADO]` com localização exata e devolver
`exit code: 1`. Esse número `1` é o que o shell entende como "barra!".

### Passo 4: veja um gate real da fábrica

Abra `scripts/validar-referencias.py`. Não precisa ler tudo — procure:

1. Como ele decide reprovar (o critério).
2. Onde ele imprime o **motivo com localização** (arquivo + o que está errado).
3. Qual o **código de saída** ele usa.

Compare com o que você acabou de escrever. A estrutura é a mesma: um critério,
um relatório claro, um exit code.

---

## Classificação rápida: a sequência que decide em 1 minuto

Para qualquer tarefa nova que aparecer, rode esta sequência mental:

| Passo | Pergunta | Se sim | Se não |
|---|---|---|---|
| 1 | Existe regra objetiva que resolve **sem modelo**? | Faixa 1: script puro | passo 2 |
| 2 | A saída é checável por script? | Faixa 2: gerar e verificar | passo 3 |
| 3 | O erro é caro e recorrente? | Faixa 3: revisão humana | Faixa 4: livre |
| 4 | Já existe gate cobrindo isso? | reuse o gate | crie o gate |
| 5 | Verificar custa menos que corrigir? | automatize | revisão amostral |

A 5ª pergunta separa rigor de teatro: verificação que custa mais que o erro
que previne é burocracia; verificação que custa uma fração do erro é
engenharia.

## Quando a verificação precisa de humano

Separe **consistência** de **consequência**:

| Situação | Quem verifica | Por quê |
|---|---|---|
| Formato, esquema, tamanho | só script | objetivo, sem interpretação |
| Conteúdo factual com fonte | script + amostragem humana | a fonte pode estar errada de forma consistente |
| Ação irreversível (publicar, apagar, pagar) | humano obrigatório | não há desfazer |
| Estilo e tom | amostragem humana | julgamento, sem regra objetiva |
| Cálculo com fórmula definida | só script | reproduzível por definição |

Herurística útil: *se o dano é reversível com um comando, automatize; se exige
pedido de desculpas, não.*

---

## Erros comuns neste dia

1. **Verificar com o mesmo modelo.** Pedir ao LLM que revise o próprio trabalho
   é camada extra de conforto, nunca um gate — ele compartilha dos mesmos
   pontos cegos.
2. **Gate que sempre passa.** Política permissiva demais dá sensação de
   segurança sem cobertura.
3. **Gate que ninguém entende.** Se reprova sem explicar o motivo, vira ruído
   e é desativado pelo time.
4. **Ordem invertida.** Rodar a verificação cara antes da barata queima
   orçamento em artefato que já estava condenado.
5. **Temperatura zero = determinismo.** A amostragem é só *uma* fonte de
   variação; busca mal ordenada e truncamento divergem mesmo com temperatura 0.
6. **Estabilidade não é acerto.** Um erro estável continua sendo erro.

## O antipadrão que denuncia a falha

Quando o mesmo comando do agente funciona na segunda tentativa sem que nada
tenha mudado no repositório, o determinismo não está no lugar. É o voo na
sorte: hoje voou bem, amanhã talvez não, e ninguém sabe dizer por quê.

---

## Checklist do dia

- [ ] Digo as 4 faixas de confiabilidade de memória.
- [ ] Sei por que a verificação é determinística mesmo com modelo probabilístico.
- [ ] Criei `gate_config.py` e vi os exit codes 0 e 1 na prática.
- [ ] Localizei 3 validadores reais em `scripts/`.
- [ ] Classifiquei 1 tarefa do meu trabalho em uma faixa.
- [ ] Sei a regra de ouro: *o que é crítico é garantido por código, não por pedido*.

## Para saber mais

- `docs/manual-completo-fabrica.md` — o fluxo operacional completo onde os
  gates aparecem em ordem.
- `AGENTS.md` do projeto — procure a Fase 2.5 e veja quantos validadores
  rodam antes da revisão.

No Dia 3, vamos escrever o arquivo que todo agente lê antes de começar — o
`AGENTS.md` — e ver o da própria fábrica como exemplo vivo.