# Gabarito — Capítulo 13: Roteamento inteligente de LLM

## Exercício 1 — Classificação por exigência cognitiva

| Tarefa | Exigência | Degrau | Verificação |
|---|---|---|---|
| Extrair campos de nota fiscal | transformação | pequeno | validador de esquema |
| Classificar ticket por categoria | transformação | pequeno | pertence ao enum |
| Escrever parecer de auditoria | síntese | médio | seções + citações |
| Depurar falha intermitente | raciocínio profundo | grande | teste que falhava passa |
| Decidir arquitetura de fila | raciocínio profundo | grande + humano | revisão humana |

Erro comum: classificar por tamanho de prompt. Uma extração longa continua sendo
transformação — o que importa é o tipo de operação mental exigida.

## Exercício 2 — Cascata com escalonamento

```python
DEGRAUS = ["pequeno", "medio", "grande"]
MAX_TENTATIVAS = 2


def executar_com_cascata(tarefa, executar_modelo, verificar):
    inicio = DEGRAUS.index(tarefa.get("modelo_inicial", "pequeno"))
    historico = []
    for tentativa in range(MAX_TENTATIVAS):
        modelo = DEGRAUS[min(inicio + tentativa, len(DEGRAUS) - 1)]
        saida = executar_modelo(modelo, tarefa)
        veredito = verificar(tarefa, saida)
        historico.append({"modelo": modelo, "aprovado": veredito["aprovado"]})
        if veredito["aprovado"]:
            return {"saida": saida, "modelo_final": modelo, "historico": historico}
    return {"saida": None, "historico": historico, "escalar_humano": True}
```

O `historico` é obrigatório para descobrir a taxa de acerto do primeiro degrau —
a métrica que decide a economia real.

## Exercício 3 — Custo por resultado aceito

```python
def custo_por_aceito(execucoes):
    aceitas = [e for e in execucoes if e["aprovado"]]
    gasto = sum(e["custo"] for e in execucoes)
    return {
        "taxa_aceitacao": round(len(aceitas) / len(execucoes), 3) if execucoes else 0.0,
        "custo_por_aceita": round(gasto / len(aceitas), 4) if aceitas else None,
    }
```

Custo por token mente; custo por resultado aceito não.

## Checklist de aceitação

- [ ] Matriz de roteamento versionada, com verificação por linha
- [ ] Cascata implementada com histórico e escalonamento humano
- [ ] Custo por resultado aceito medido contra o cenário anterior
- [ ] Conjunto de avaliação com critério de aprovação
- [ ] Nenhuma linha da matriz sem verificação declarada

## Registro de aprendizagem

Cascata sem gate é retry caro: você paga duas vezes e não aprende nada. A verificação
externa é o que transforma escalonamento em economia medida.
