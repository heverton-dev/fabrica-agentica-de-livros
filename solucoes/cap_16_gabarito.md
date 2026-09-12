# Gabarito — Capítulo 16: Arquitetura para desenvolvimento com IA

## Exercício final 1 — Esteira em um único arquivo

```yaml
esteira:
  nome: "relatorio-tecnico"
  entrada: { formato: "json", schema: "schemas/entrada.json" }
  saida:
    formato: "markdown"
    criterio_de_pronto: ["todas as secoes preenchidas", "toda metrica com fonte"]
  camadas:
    contrato: { arquivo: "contratos/relatorio.yaml" }
    contexto: { operacoes: ["escrever", "selecionar", "isolar", "comprimir"] }
    geracao: { roteamento: { extracao: "pequeno", sintese: "medio", raciocinio: "grande" } }
    verificacao: { gates: ["forma", "contrato", "merito"], bloqueio_mecanico: "pre-commit" }
    governanca: { custo_maximo_por_tarefa_usd: 1.20, retencao_historico_dias: 30 }
```

Critério: se um engenheiro novo não entende a esteira lendo só este arquivo, o
contrato está incompleto.

## Exercício final 2 — Painel de métricas

```python
METRICAS = {
    "custo_por_resultado_aceito_usd": {"meta": 0.35, "tipo": "menor_melhor"},
    "turnos_por_tarefa": {"meta": 18, "tipo": "menor_melhor"},
    "taxa_aceitacao_primeiro_degrau": {"meta": 0.70, "tipo": "maior_melhor"},
    "artefatos_sem_atribuicao": {"meta": 0.0, "tipo": "menor_melhor"},
}
```

Regra: métrica ausente é métrica reprovada. Painel com três métricas ativas é o
mínimo aceitável.

## Exercício final 3 — Governança em arquivo

```json
{
  "governanca": {
    "custo": { "orcamento_mensal_usd": 900, "alerta_em": 0.8 },
    "seguranca": { "rede": false, "acoes_irreversiveis": "somente_humano" },
    "retencao": { "historico_dias": 30, "auditoria_dias": 180 },
    "responsabilidade": { "dono_da_configuracao": "time-plataforma", "revisao": "trimestral" }
  }
}
```

Se algum dos quatro blocos estiver ausente, a esteira não é auditável.

## Checklist de aceitação

- [ ] Esteira declarada em um arquivo legível
- [ ] Contrato com schema e critério de pronto
- [ ] Painel com três métricas ou mais
- [ ] Gates em cascata com bloqueio mecânico
- [ ] Governança com dono e data de revisão
- [ ] Atribuição de artefato funcionando

## Registro de aprendizagem

Custo por peça publicada sem correção é a métrica que revela retrabalho escondido:
economia aparente costuma ser trabalho refeito que ninguém contabilizou.
