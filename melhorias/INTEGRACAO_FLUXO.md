# Integração ao Fluxo: Fase 6

**Status:** ✅ Documentado | ⏳ Implementação em 2 partes

---

## Visão Geral

O fluxo atual (Fase F2: Redação em Paralelo) precisa de 2 pontos de integração:

```
FLUXO ATUAL:
pool-capitulos.py --lote 4
  → subagente-redator-capitulo × 4 (paralelo)
    → Saída: 4 capitulos brutos

FLUXO NOVO (com gates):
pool-capitulos.py --lote 4
  → subagente-redator-capitulo × 4 (paralelo)
    → Saída: 4 capítulos brutos
    → **GATE 1-4** (validação automática) ← NOVO
      → Se PASS: avança para F2.5
      → Se FAIL: marcar cap como BLOQUEADO + feedback ao redator
    → F2.5: revisor-tecnico (agora valida também Gate 5)
```

---

## Parte A: Integração ao Pool (Automática)

### 1. Modificar `pool-capitulos.py`

**Local:** `scripts/pool-capitulos.py` (linha ~XXX)

**Antes:**
```python
def pool_capitulos():
    # ... lógica de paralelização
    resultados = await run_parallel_redators(lote)
    
    # Salvar capítulos
    for cap in resultados:
        save_chapter(cap)
    
    return resultados
```

**Depois:**
```python
def pool_capitulos():
    # ... lógica de paralelização
    resultados = await run_parallel_redators(lote)
    
    # ✅ NOVO: Validar com Gates antes de salvar
    for cap in resultados:
        passed = validate_with_gates(cap)  # Roda Gate 1-4
        
        if passed:
            save_chapter(cap)
            mark_as("VALIDADO", cap)
        else:
            mark_as("BLOQUEADO", cap)
            add_feedback(cap)  # "Gate X falhou: motivo"
    
    return resultados

def validate_with_gates(chapter_content, chapter_num):
    """Rodar Gates 1-4 em um capítulo."""
    # Salvar temporariamente
    temp_file = f"/tmp/cap_{chapter_num}_validate.md"
    with open(temp_file, "w") as f:
        f.write(chapter_content)
    
    # Rodar gates
    gates = [
        "scripts/gate_1_eita_structure.py",
        "scripts/gate_2_code_completeness.py",
        "scripts/gate_3_didactic_accessibility.py",
        "scripts/gate_4_exercises_completeness.py"
    ]
    
    failures = []
    for gate_script in gates:
        result = subprocess.run(
            ["python", gate_script, temp_file],
            capture_output=True
        )
        if result.returncode != 0:
            failures.append(f"{gate_script}: {result.stderr}")
    
    # Limpar temp
    os.remove(temp_file)
    
    return len(failures) == 0, failures
```

### 2. Integração ao settings.json

**Local:** `.claude/settings.json`

**Adicionar hook:**
```json
{
  "hooks": {
    "post-edit": [
      {
        "matcher": "output/*/livros/*/capitulos/cap_*.md",
        "command": "python scripts/validate_all_gates.py"
      }
    ]
  }
}
```

Isso roda validação sempre que um capítulo é editado.

---

## Parte B: Integração ao Revisor (Checklist)

### 1. Atualizar CLAUDE.md do `revisor-tecnico`

**Local:** `.claude/agents/revisor-tecnico.md`

**Adicionar checklist:**
```markdown
## NOVO: Checklist Gate 5 (Qualidade)

Antes de liberar um capítulo, valide:

- [ ] Gate 5 rodou sem críticos?
- [ ] Código é copy-paste-able?
- [ ] Referências são confiáveis?
- [ ] PT-BR ortografia OK?

Se algum falhar → volta ao redator com feedback.
```

### 2. Adicionar Dashboard ao Relatório

**Local:** `relatorios/YYYYMMDD-tema.md`

Ao fim de cada sessão, gerar:

```markdown
## Validação de Qualidade (Gates)

| Livro | G1 | G2 | G3 | G4 | G5 | Score |
|---|---|---|---|---|---|---|
| TELA | 3/4 | 2/4 | 1/4 | 4/4 | 4/4 | 55% |
| HARNESS | 4/4 | 4/4 | 1/4 | 4/4 | 4/4 | 85% |
| ... |

**Total: XXX/160 gates (XX%)**
```

---

## Parte C: Checklist Redator

### Adicionar ao CLAUDE.md do `redator-capitulo`

```markdown
# NOVO: Antes de Submeter (Checklist 10/10)

1. **Gate 1 (EITA):** 7 seções presentes?
   - [ ] Introdução
   - [ ] Explica (>200 palavras)
   - [ ] Ilustra (com diagrama/metáfora)
   - [ ] Técnica (>2 exemplos)
   - [ ] Aplica (erro + solução)
   - [ ] Conclusão
   - [ ] Referências (>5)

2. **Gate 2 (Código):** Copy-paste-able?
   - [ ] Python: sem syntax errors
   - [ ] JSON: válido
   - [ ] LangGraph: handlers definidos
   - [ ] Imports: completos

3. **Gate 3 (Didática):** Acessível?
   - [ ] TL;DR presente (1-3 linhas)
   - [ ] Jargão explicado
   - [ ] Parágrafos <400 palavras

4. **Gate 4 (Exercício):** Pronto pra praticar?
   - [ ] "Seu Turno" presente
   - [ ] Gabarito existe

5. **Gate 5 (Qualidade):** OK?
   - [ ] Rodar `python scripts/validate_all_gates.py`
   - [ ] Score >= 70%
```

---

## Fluxo Completo (Com Gates)

```
ANTES (sem qualidade):
INPUT → Pool-Capitulos → Redator (4 caps) → Auditar → Compilar → PDF

DEPOIS (com qualidade):
INPUT → Pool-Capitulos → Redator (4 caps)
                              ↓
                         [GATE 1-4] ← VALIDAÇÃO AUTOMÁTICA
                              ↓
                   ┌─────────┴────────┐
                   ↓                  ↓
               PASS (13/16)      FAIL (3/16)
                   ↓                  ↓
            Auditar (F2.5)    Feedback → Redator
                   ↓             ↓
            [GATE 5]         Retry
                   ↓             ↓
            Revisor-Técnico    (volta ao Pool)
                   ↓
            [100% Gates OK?]
                   ↓ SIM
            Compilar → PDF
```

---

## Comando de Teste (Pré-Integração)

Para testar o fluxo ANTES da integração completa:

```bash
# Teste de gate em um capítulo
python scripts/gate_1_eita_structure.py output/tela-camada-agente/livros/harness-segunda-camada/capitulos/cap_2.md

# Teste de todos os gates em todos os caps
python scripts/validate_all_gates.py

# Esperado: Score >= 70% = OK para avançar para Compilação
```

---

## Estimativa de Esforço

| Tarefa | Tempo | Prioridade |
|---|---|---|
| **A1:** Modificar pool-capitulos.py | 2-3h | 🔴 CRÍTICA |
| **A2:** Integrar hook settings.json | 0.5h | 🟡 MÉDIA |
| **B1:** Atualizar revisor-tecnico.md | 1h | 🟡 MÉDIA |
| **B2:** Dashboard relatório | 1-2h | 🟢 BAIXA |
| **C1:** Checklist redator | 0.5h | 🟢 BAIXA |
| **Testes E2E** | 2-3h | 🔴 CRÍTICA |

**Total:** 8-10 horas

---

## Checklist de Implementação (Fase 6)

- [ ] Modificar `pool-capitulos.py` (Parte A1)
- [ ] Integrar hook (Parte A2)
- [ ] Atualizar revisor-tecnico.md (Parte B1)
- [ ] Adicionar dashboard (Parte B2)
- [ ] Adicionar checklist redator (Parte C1)
- [ ] Testes E2E com 4-Camadas completo
- [ ] Validação de 100% dos caps
- [ ] Deploy em produção

---

## Após a Integração: Próximas Iterações

### Iteração 1 (Agora):
- ✅ 5 Gates implementados
- ✅ Validação automática
- ⏳ Integração ao fluxo

### Iteração 2 (Semana próxima):
- Gate 5 com LLM real (não heurística)
- Métricas de readability (Flesch-Kincaid PT-BR)
- Notificações automáticas

### Iteração 3 (2 semanas):
- Auto-fix de problemas simples (TL;DR missing, etc)
- Painel de progresso (web UI)
- Integração com git (auto-commit quando 100% gates pass)

---

## Referências

- Gates: `scripts/gate_*.py`
- Validador: `scripts/validate_all_gates.py`
- Plano: `melhorias/plano-qualidade-10-10.md`
- Status: `melhorias/STATUS.md`

---

**Próximo:** Implementar Parte A (pool-capitulos.py modification)
