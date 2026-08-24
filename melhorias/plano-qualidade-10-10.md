# PLANO DE AÇÃO: ELEVAR & MANTER ARTEFATOS EM 10/10

**Escopo:** 
- Série 4 Camadas (+ derivados: Playbook, E-book, Deck, Lead Magnet)
- Todos os 8 tipos de obra (Livro, TCC, Artigo, E-book, Playbook, Lead Magnet, Deck, E-mails)
- Fluxo completo: Pesquisa → Redação → Revisão → Compilação

**Status Atual:** 8.1/10 (gaps em code completeness, exercícios interativos, acessibilidade non-dev)

---

## PARTE 1: DIAGNÓSTICO — O QUE FALTA PARA 10/10

### 1.1 Lacunas Técnicas (Código/Config)

| Gap | Impacto | Severidade | Afeta |
|---|---|---|---|
| **LangGraph handlers faltam** | Copy-paste quebra | ALTA | Dev iniciante |
| **Retry sem edge-case** | Ignora KeyboardInterrupt | MÉDIA | Produção |
| **Refs não-verificáveis** | Desconfiança em fontes | BAIXA | Credibilidade |
| **Sem screenshots/GIFs** | Iniciante perde-se visualmente | MÉDIA | Non-dev |
| **Sem checklist de implementação** | "E agora, como faço?" | MÉDIA | Aplicação |

**Fix Time Estimado:** 8-12 horas (parallelizável)

---

### 1.2 Lacunas Didáticas (Acessibilidade)

| Gap | Causa | Impacto | Afeta |
|---|---|---|---|
| **Sem TL;DR por capítulo** | Falta resumo | Iniciante esquece ideia central | Retenção |
| **Sem glossário técnico** | Jargão acumula | Non-dev abandon livro | Retenção |
| **Feedforward vs Feedback** | Mal definido | Leitor confunde | Entendimento |
| **Sem tabela de "qual componente usar"** | Decisão nebulosa | "Quando uso hook vs permissão?" | Aplicação |
| **Transformer/Self-Attention muito denso** | Pula etapas | Leitor perde-se | Entendimento |

**Fix Time Estimado:** 6-10 horas

---

### 1.3 Lacunas de Exercício & Prática

| Gap | Problema | Impacto | Afeta |
|---|---|---|---|
| **Sem "seu turno" exercises** | Passivo (lê apenas) | Não fixa aprendizado | Retenção |
| **Sem código sandbox interativo** | Teórico demais | Medo de "vou errar" | Confiança |
| **Sem "case real start-to-end"** | Fragmentado | "Como aplico tudo junto?" | Aplicação |
| **Sem gabarito/solução** | Exercício pendurado | Dúvida sem resposta | Motivação |

**Fix Time Estimado:** 16-20 horas (criar exercises, gabaritos, sandboxes)

---

### 1.4 Lacunas de Estrutura Meta (Série)

| Gap | Problema | Impacto |
|---|---|---|
| **Sem "4 Camadas em Ação" capstone** | Integração nebulosa | Leitor não vê como tudo funciona junto |
| **Sem roadmap pós-série** | Dead-end | "E depois? Por onde sigo?" |
| **Sem comparação com ferramentas** | Isolado | "Como isso difere de X, Y, Z?" |

**Fix Time Estimado:** 4-6 horas

---

## PARTE 2: ESTRUTURA DOS FLUXOS ATUAIS

### 2.1 Fluxo de Criação de Livro (Atual)

```
┌─────────────────────────────────────────────────────────┐
│ FLUXO ATUAL DE PRODUÇÃO DE LIVRO                         │
└─────────────────────────────────────────────────────────┘

1. INPUT: /esbocar <tema>
   └─ Operador define tema, série, senioridade

2. FASE 1 (F1) — Pesquisa & Arquitetura
   ├─ subagente-pesquisador: mineração acadêmica
   ├─ indexar-dossie.py: indexação RAG
   └─ arquiteto: gera sumário_macro
   ⚠️ CHECKPOINT: Gates de referências (validar-referencias.py --estrito)

3. FASE 2 (F2) — Redação em Paralelo
   ├─ pool-capitulos.py --lote 4
   ├─ subagente-redator-capitulo × N (paralelo)
   │  ├─ Estratégia (molde EITA)
   │  ├─ Redação
   │  ├─ Diagrama (renderizar-diagramas.py)
   │  ├─ CI de Código (validar-codigo.py)
   │  └─ Auto-validação (gates de conteúdo)
   └─ pool-capitulos.py --juntar
   ⚠️ CHECKPOINT: auditar-obra.py (gates EITA: R-RF, R-MT, R-ES, R-AF, R-FT)

4. FASE 2.5 (F2.5) — Revisão Técnica
   ├─ revisor-tecnico: peer-review + conferência de fontes
   ├─ validar-codigo.py --executar (smoke tests)
   └─ renderizar-diagramas.py --validar
   ⚠️ CHECKPOINT: Todos os gates rodando

5. FASE 3 (F3) — Compilação
   ├─ compilador-abnt: merge + pré/pós-textuais
   ├─ compilar-para-pdf.py: Pandoc → Typst
   └─ metadados_livro.py
   ⚠️ CHECKPOINT: PDF abre? Tem 100% das páginas esperadas?

6. SAÍDA: output/<colecao>/livros/<slug>/livro_final.pdf

FLUXO ATUALMENTE NÃO TESTA:
❌ Se exemplos no livro são copy-paste-able
❌ Se código está completo (LangGraph handlers)
❌ Se non-dev consegue entender (sem métricas)
❌ Se exercícios existem e têm gabarito
```

---

### 2.2 Fluxo Atual: Gargalos Identificados

| Fase | Gargalo | Sintoma |
|---|---|---|
| **F1** | Gates de referência incompletos | URLs "referências de blog" passam sem validação |
| **F2** | Sem gate de "completude de código" | LangGraph incompleto mas passa |
| **F2** | Sem gate de "exercícios faltam" | Cap tem "Aplica" mas não tem "seu turno" |
| **F2.5** | Revisor técnico foca em factual, não didática | Código "compila" mas não é "pronto pra usar" |
| **F3** | PDF abre ≠ conteúdo é 10/10 | Compilação passa, mas qualidade não |

---

## PARTE 3: SOLUÇÃO — SISTEMA DE GATES PARA 10/10

### 3.1 Arquitetura: 5 Camadas de Gates

```
ARTEFATO BRUTO (cap 1-4.md)
│
├─ GATE 1: Estrutura EITA
│  └─ Verifica: [✓Explica ✓Ilustra ✓Técnica ✓Aplica]
│     Se falha → REJEITA (feedback ao redator)
│
├─ GATE 2: Completude de Código
│  └─ Verifica: Python/JSON é executável? Imports faltam?
│     Se falha → REJEITA com lista de fixes
│
├─ GATE 3: Acessibilidade Didática
│  └─ Verifica: TL;DR? Feedforward/Feedback explicado? Jargão não-explicado?
│     Se falha → REJEITA com sugestões
│
├─ GATE 4: Completude de Exercícios
│  └─ Verifica: "Seu turno" presente? Gabarito existe?
│     Se falha → REJEITA (falta antes de compilação)
│
└─ GATE 5: Métricas de Qualidade (PASS/FAIL)
   ├─ Readability score (Flesch-Kincaid PT-BR)
   ├─ Jargão não-explicado (detect-undefined-terms.py)
   ├─ Exemplos são replicáveis (test-code-snippets.py)
   └─ Non-dev consegue entender 60%+ (LLM as judge — inferential)

RESULTADO: ARTEFATO 10/10 ✅
```

---

### 3.2 Detalhamento: Cada Gate

#### GATE 1: Estrutura EITA ✓ (Deterministico)

**O que verifica:**
```markdown
# Capítulo X

## 1. Introdução (presente?)
## 2. Explica (presente? >200 palavras?)
## 3. Ilustra (presente? diagrama ou metáfora?)
## 4. Técnica (presente? código/config real?)
## 5. Aplica (presente? erro comum + solução?)
## 6. Conclusão (presente?)
## 7. Referências (presente? >=5 itens?)
```

**Implementação:**
```python
# scripts/gate_1_eita_structure.py
def validar_estrutura_eita(arquivo_md):
    secoes_obrigatorias = ["Introdução", "Explica", "Ilustra", "Técnica", "Aplica", "Conclusão", "Referências"]
    for secao in secoes_obrigatorias:
        if secao not in arquivo_md:
            return False, f"Falta seção: {secao}"
    
    # Verificar tamanho mínimo
    explica = extract_section(arquivo_md, "Explica")
    if len(explica.split()) < 200:
        return False, "Explica tem <200 palavras"
    
    # Verificar se tem diagrama em Ilustra
    ilustra = extract_section(arquivo_md, "Ilustra")
    if "mermaid" not in ilustra and "```" not in ilustra:
        return False, "Ilustra sem diagrama/código"
    
    return True, "OK"
```

**Momento de execução:** Pós-redação, antes de auditar-obra.py  
**Rejeição:** SE qualquer seção falta → BLOQUEIA compilação

---

#### GATE 2: Completude de Código ✓ (Deterministico + Inferential)

**O que verifica:**
```
1. Código Python: rodar com "python -m py_compile"?
2. JSON: é válido (json.loads)?
3. LangGraph: imports presentes? node functions defini­das?
4. Exemplo está completo? (não falta linha)
5. Código está indentado corretamente?
6. Variáveis são definidas antes de usar?
```

**Implementação:**
```python
# scripts/gate_2_code_completeness.py
def validar_codigo(arquivo_md):
    blocos_codigo = extract_code_blocks(arquivo_md)
    erros = []
    
    for i, bloco in enumerate(blocos_codigo):
        # Teste 1: Python syntax
        if bloco["lang"] == "python":
            try:
                compile(bloco["code"], f"block_{i}", "exec")
            except SyntaxError as e:
                erros.append(f"Bloco {i}: Syntax error — {e}")
        
        # Teste 2: JSON validity
        if bloco["lang"] == "json":
            try:
                json.loads(bloco["code"])
            except json.JSONDecodeError as e:
                erros.append(f"Bloco {i}: JSON invalid — {e}")
        
        # Teste 3: LangGraph completeness
        if "StateGraph" in bloco["code"]:
            if "def " not in bloco["code"]:
                erros.append(f"Bloco {i}: LangGraph sem funções node definidas")
        
        # Teste 4: Indentação
        lines = bloco["code"].split("\n")
        for j, line in enumerate(lines):
            if line and not line[0].isspace() and j > 0:
                if lines[j-1].endswith(":") and not line.startswith(" "):
                    erros.append(f"Bloco {i}, linha {j}: Indentação inválida após ':'")
    
    if erros:
        return False, "\n".join(erros)
    return True, "OK"
```

**Momento de execução:** Pós-redação, em paralelo com Gate 1  
**Rejeição:** Qualquer erro → BLOQUEIA compilação

---

#### GATE 3: Acessibilidade Didática ✓ (Deterministico + Inferential)

**O que verifica:**
```
1. Cada capítulo tem TL;DR (1-3 linhas)?
2. Jargão técnico é definido na 1ª menção?
3. Feedforward vs Feedback: é claro qual é qual?
4. Tabelas de decisão presentes (ex: "Quando usar X vs Y")?
5. Readability score (Flesch-Kincaid) > 50 (iniciante)?
6. Parágrafos têm <4 linhas? (legibilidade)
```

**Implementação:**
```python
# scripts/gate_3_didactic_accessibility.py
def validar_acessibilidade(arquivo_md):
    erros = []
    
    # Teste 1: TL;DR por capítulo
    capitulos = extract_sections_at_level(arquivo_md, level=1)
    for cap in capitulos:
        if "TL;DR" not in cap and "resumo" not in cap.lower():
            erros.append(f"Capítulo '{cap}': Falta TL;DR")
    
    # Teste 2: Jargão técnico é definido
    jargoes = ["self-attention", "token", "context window", "feedforward", "feedback"]
    for jargao in jargoes:
        if jargao in arquivo_md:
            # Verificar se está entre aspas ou definido
            lines_with_jargao = [l for l in arquivo_md.split("\n") if jargao in l.lower()]
            primeira_mencao = lines_with_jargao[0] if lines_with_jargao else ""
            if not any(marker in primeira_mencao for marker in ['"', "'", "—", ":", "é"]):
                erros.append(f"Jargão '{jargao}' não definido na 1ª menção")
    
    # Teste 3: Readability score
    text_only = remove_markdown(arquivo_md)
    score = flesch_kincaid_score_pt_br(text_only)
    if score < 50:  # Muito denso
        erros.append(f"Readability score {score} < 50 (muito denso para iniciante)")
    
    # Teste 4: Parágrafos legíveis
    paragrafos = text_only.split("\n\n")
    for i, p in enumerate(paragrafos):
        linhas = p.split("\n")
        if len(linhas) > 4 and not is_table(p) and not is_code_block(p):
            erros.append(f"Parágrafo {i}: {len(linhas)} linhas (muito longo)")
    
    if erros:
        return False, "\n".join(erros)
    return True, "OK"
```

**Momento de execução:** Pós-redação  
**Rejeição:** Score readability <50 ou jargão não-definido → BLOQUEIA compilação

---

#### GATE 4: Completude de Exercícios ✓ (Deterministico + Inferential)

**O que verifica:**
```
1. Seção "Aplica" tem "Erro Comum" + "Solução Correta"?
2. Seção "Técnica" tem exemplos executáveis?
3. Existe "Seu Turno" ou "Exercício"?
   └─ Sim: Existe gabarito/solução?
   └─ Não: REJEITA (falta antes de compilação)
4. Checklist de implementação presente?
```

**Implementação:**
```python
# scripts/gate_4_exercises_completeness.py
def validar_exercicios(arquivo_md, cap_numero):
    erros = []
    
    # Teste 1: "Aplica" tem erro + solução
    aplica = extract_section(arquivo_md, "Aplica")
    if "Erro comum" not in aplica:
        erros.append("Seção Aplica: Falta 'Erro comum vs prática correta'")
    
    # Teste 2: "Técnica" tem exemplos
    tecnica = extract_section(arquivo_md, "Técnica")
    if len(extract_code_blocks(tecnica)) < 2:
        erros.append("Seção Técnica: <2 exemplos de código")
    
    # Teste 3: "Seu Turno" existe?
    seu_turno = find_section_like(arquivo_md, ["Seu Turno", "Exercício", "Prática"])
    if not seu_turno:
        erros.append("CRÍTICO: Falta seção 'Seu Turno'/'Exercício'")
    else:
        # Existe gabarito?
        gabarito_path = f"solucoes/cap_{cap_numero}_gabarito.md"
        if not os.path.exists(gabarito_path):
            erros.append(f"Exercício sem gabarito: {gabarito_path}")
    
    # Teste 4: Checklist de implementação
    checklist_found = "[ ]" in arquivo_md or "- [ ]" in arquivo_md
    if not checklist_found:
        erros.append("Falta checklist de implementação")
    
    if erros:
        return False, "\n".join(erros)
    return True, "OK"
```

**Momento de execução:** Pós-redação, bloqueia compilação se falta "Seu Turno"  
**Rejeição:** Sem exercício ou gabarito → BLOQUEIA

---

#### GATE 5: Métricas de Qualidade (Inferential)

**O que verifica:**
```
1. Exemplos no livro são copy-paste-able? (LLM as judge)
2. Non-dev consegue entender 60%+ do conteúdo? (LLM as judge)
3. Analogia "estúdio" é mantida consistentemente? (keyword search)
4. Referências são confiáveis? (validar-referencias.py)
5. Erros ortográficos? (PT-BR spell-check)
```

**Implementação:**
```python
# scripts/gate_5_quality_metrics.py
def validar_metricas(arquivo_md, config_obra):
    erros = []
    warnings = []
    
    # Teste 1: Copy-paste-ability (LLM as judge)
    blocos_codigo = extract_code_blocks(arquivo_md)
    for i, bloco in enumerate(blocos_codigo):
        prompt = f"""
        Esse código Python/JSON pode ser copiado e colado diretamente por um iniciante?
        Código:
        ```
        {bloco["code"]}
        ```
        Responda: SIM / NÃO
        Se NÃO, explique o que falta (imports, definições, etc.)
        """
        response = llm_judge(prompt)  # Chamar LLM para avaliar
        if "NÃO" in response:
            erros.append(f"Bloco {i}: Não é copy-paste-able — {response}")
    
    # Teste 2: Non-dev compreensão
    senioridade = config_obra.get("senioridade_obra", "iniciante")
    if senioridade == "iniciante":
        # Amostrar 3 seções aleatórias
        secoes_amostra = random.sample(extract_all_sections(arquivo_md), min(3, len(extract_all_sections)))
        for secao in secoes_amostra:
            prompt = f"""
            Um não-programador conseguiria entender esse texto? (0-100%)
            Texto:
            {secao[:500]}
            Responda com um número 0-100 e breve explicação.
            """
            response = llm_judge(prompt)
            score = extract_number(response)  # Ex: "85%" → 85
            if score < 60:
                warnings.append(f"Seção com baixa compreensão non-dev: {score}%")
    
    # Teste 3: Consistência de analogia "estúdio"
    if "estúdio" not in arquivo_md and config_obra.get("serie") == "4-Camadas":
        warnings.append("Analogia 'estúdio' não aparece (série 4-Camadas usa essa metáfora)")
    
    # Teste 4: Validar referências
    refs = extract_references(arquivo_md)
    for ref in refs:
        if "http" in ref:
            try:
                response = requests.head(ref, timeout=5)
                if response.status_code >= 400:
                    warnings.append(f"Referência quebrada: {ref} ({response.status_code})")
            except:
                warnings.append(f"Referência não testada (offline?): {ref}")
    
    # Teste 5: Ortografia PT-BR
    erros_ortografia = spell_check_pt_br(arquivo_md)
    if erros_ortografia:
        warnings.extend(erros_ortografia)
    
    return {
        "status": "BLOQUEADO" if erros else "AVISO" if warnings else "OK",
        "erros": erros,
        "warnings": warnings
    }
```

**Momento de execução:** Pós-gate 1-4, antes de compilação  
**Rejeição:** Código não copy-paste-able OU non-dev score <60% em amostra → BLOQUEIA ou requere fix

---

### 3.3 Configuração de Gates: Matrix de Decisão

| Gate | Tipo | Momento | Bloqueia? | Feedback |
|---|---|---|---|---|
| **GATE 1** | Deterministico | Pós-redação | ✅ SIM | Lista de seções faltando |
| **GATE 2** | Deterministico | Pós-redação | ✅ SIM | Linha exata do erro de código |
| **GATE 3** | Híbrido | Pós-redação | ✅ SIM | Readability score + seções |
| **GATE 4** | Deterministico | Pós-redação | ✅ SIM | "Falta 'Seu Turno'" |
| **GATE 5** | Inferential | Pré-compilação | ⚠️ AVISO | Warnings, não bloqueia |

---

## PARTE 4: ROTEIRO DE IMPLEMENTAÇÃO

### 4.1 Fase 1: GATES DETERMINISTICOS (Semana 1)

**Objetivo:** Bloquear artefatos com estrutura/código quebrado

**Tarefas:**
```
1.1 Criar gate_1_eita_structure.py
    ├─ Validar 7 seções obrigatórias
    ├─ Testar com cap 1-4 de todos os livros (4 Camadas)
    └─ Target: 100% dos atuais passam ou são marcados

1.2 Criar gate_2_code_completeness.py
    ├─ Syntax check Python/JSON
    ├─ LangGraph handler detection
    ├─ Indentation validation
    └─ Testar com código atual (deve achar gaps)

1.3 Criar gate_4_exercises_completeness.py
    ├─ Detectar "Seu Turno" ou "Exercício"
    ├─ Detectar gabarito
    ├─ Criar template de gabarito
    └─ Testar (esperado: FALHA em todos atuais)

1.4 Integrar ao fluxo
    ├─ Chamar gates após pool-capitulos.py --juntar
    ├─ Reject se qualquer gate falha
    └─ Output: relatório de rejeição

Dependências: NENHUMA
Estimativa: 6-8 horas
Critério de Sucesso: Gates rodando, detectando problemas reais
```

---

### 4.2 Fase 2: GATES ACESSIBILIDADE (Semana 1-2)

**Objetivo:** Garantir didática em 10/10 antes de compilação

**Tarefas:**
```
2.1 Criar gate_3_didactic_accessibility.py
    ├─ Implementar flesch_kincaid_score_pt_br
    ├─ Detectar jargão não-explicado
    ├─ Validar TL;DR por capítulo
    ├─ Validar tabelas de decisão
    └─ Testar com cap 1 (HARNESS) — atual tem "Feedforward vs Feedback" mal explicado

2.2 Criar glossário_tecnico.py
    ├─ Extrair termos técnicos por livro
    ├─ Gerar arquivo "Glossário.md" automático
    ├─ Validar que cada termo é definido
    └─ Integrar ao PDF final

2.3 Integrar ao fluxo
    ├─ Chamar após Gate 2
    ├─ Output: sugestões de reescrita (não bloqueia se warnings)
    └─ Redator pode aceitar ou corrigir

Dependências: Fase 1
Estimativa: 8-10 horas
Critério de Sucesso: Readability score verificado, jargão detectado/reportado
```

---

### 4.3 Fase 3: EXERCÍCIOS & GABARITOS (Semana 2-3)

**Objetivo:** Artefatos com exercícios completos + soluções

**Tarefas:**
```
3.1 Criar template "Seu Turno"
    ├─ Estrutura: [Descrição] [Contexto] [Tarefa] [Restrições]
    ├─ Criar para cada tipo de livro
    └─ Adicionar ao CLAUDE.md do redator-capitulo

3.2 Criar gerador de gabarito (semi-automático)
    ├─ Prompt: "Crie gabarito para esse exercício"
    ├─ LLM responde, humano revisa
    ├─ Salvar em solucoes/cap_X_gabarito.md
    └─ Gate 4 valida que existe

3.3 Aplicar retrofit aos livros 4-Camadas
    ├─ Cap 1 (TELA): Adicionar 1 "Seu Turno" per capítulo
    ├─ Cap 2-4 (HARNESS): Adicionar 1 "Seu Turno" per capítulo
    ├─ LLM (Cap 1-4): Adicionar exercícios
    ├─ TOOLS (Cap 1-4): Adicionar exercícios
    └─ Gerar todos os gabaritos

3.4 Integrar ao fluxo
    ├─ Gate 4 bloqueia se "Seu Turno" falta
    ├─ Gate 4 bloqueia se gabarito não existe
    ├─ Output: "Falta exercício em cap_2"

Dependências: Fase 1-2 (estrutura + acessibilidade)
Estimativa: 12-16 horas
Critério de Sucesso: Todos os caps 4-Camadas têm exercício + gabarito
```

---

### 4.4 Fase 4: GATE INFERENTIAL (LLM as Judge) (Semana 3-4)

**Objetivo:** Validar copy-paste-ability, non-dev compreensão, refs

**Tarefas:**
```
4.1 Criar gate_5_quality_metrics.py
    ├─ LLM judge: "Esse código é copy-paste-able?"
    ├─ LLM judge: "Non-dev entende isso?"
    ├─ Link checker: Validar referências HTTP
    ├─ PT-BR spell check
    └─ Gerar relatório de warnings

4.2 Integrar verificação de referências
    ├─ validar-referencias.py --cache (offline)
    ├─ Marcar refs como "verificada", "quebrada", "não-testada"
    └─ Output: "⚠️ Ref [1] retorna 404"

4.3 Setup de LLM judge
    ├─ Usar modelo rápido (Haiku) para julgamentos
    ├─ Cachear prompts (prompt caching)
    ├─ Timeout 30s por judge
    └─ Custo: ~0.001 USD por capítulo

4.4 Testar com amostra (4 Camadas)
    ├─ Rodar em cap_1 (TELA) completo
    ├─ Coletar scores de copy-paste-ability
    ├─ Coletar scores de non-dev compreensão
    └─ Validar que detecta problemas reais

Dependências: Fase 1-3
Estimativa: 10-14 horas
Critério de Sucesso: Gates rodando, julgamentos confiáveis, falsos-positivos < 10%
```

---

### 4.5 Fase 5: RETROFIT SÉRIE 4-CAMADAS (Semana 4-5)

**Objetivo:** Elevar livros atuais de 8.1 para 10/10

**Tarefas:**
```
5.1 Executar GATES nos 4 livros (TELA, HARNESS, LLM, TOOLS)
    ├─ Rodar Gate 1-5 em paralelo
    ├─ Coletar relatório de rejeições
    ├─ Priorizar por severidade

5.2 Fixes Fase 2.5 (Revisão Técnica)
    ├─ **LangGraph:** Adicionar handlers (think_node, act_node, etc.)
    ├─ **Retry:** Adicionar try-except KeyboardInterrupt
    ├─ **Refs:** Validar/remover refs não-verificáveis (ou marcar como "secundárias")
    ├─ **TL;DR:** Adicionar 1 parágrafo resumo ao fim de cada cap
    ├─ **Jargão:** Adicionar glossário inline
    └─ Estimativa: 12-16 horas

5.3 Fixes Exercícios
    ├─ Adicionar "Seu Turno" em cada capítulo
    ├─ Gerar gabaritos (semi-automático + review humano)
    ├─ Validar com Gate 4
    └─ Estimativa: 16-20 horas

5.4 Fixes Acessibilidade
    ├─ Melhorar explicação "Feedforward vs Feedback"
    ├─ Reescrever Transformer com progressão melhor
    ├─ Adicionar tabelas "Quando usar X vs Y"
    ├─ Validar readability score
    └─ Estimativa: 8-12 horas

5.5 Validação Final
    ├─ Todos os gates passam (Gate 1-4 = bloqueadores, Gate 5 = warnings <5)
    ├─ Code review manual dos fixes
    └─ PDF final recompilado

Dependências: Fase 1-4 completas
Estimativa: 40-50 horas (parallelizável)
Critério de Sucesso: Score 10/10 em todos os caps, Gates passam 100%
```

---

### 4.6 Fase 6: FLUXO FUTURO (Permanente)

**Objetivo:** Toda obra nova já nasce em 10/10

**Tarefas:**
```
6.1 Integração ao CLAUDE.md do redator-capitulo
    ├─ Adicionar checklist EITA (seções obrigatórias)
    ├─ Adicionar template "Seu Turno"
    ├─ Adicionar instrução "Código deve ser copy-paste-able"
    └─ Redator segue checklist antes de submeter

6.2 Integração ao fluxo CI
    ├─ pool-capitulos.py --juntar executa Gates 1-5
    ├─ SE qualquer gate falha:
    │  ├─ Marcar cap como BLOQUEADO
    │  ├─ Notificar revisor-tecnico
    │  └─ Não avança para F2.5
    ├─ SE todos gates passam:
    │  └─ Avança para revisor-tecnico normalmente

6.3 Integração ao CLAUDE.md do revisor-tecnico
    ├─ Revisor verifica não apenas factual, mas também:
    │  ├─ Copy-paste-ability de código
    │  ├─ Didática (jargão, TL;DR, exercícios)
    │  ├─ Non-dev compreensão
    │  └─ Integridade de referências
    └─ Revisor usa checklist de 10/10 antes de liberar

6.4 Dashboard de Qualidade
    ├─ Para cada obra:
    │  ├─ Score EITA (seções presentes/ausentes)
    │  ├─ Score Código (copy-paste-ability)
    │  ├─ Score Didática (readability, jargão)
    │  ├─ Score Exercícios (completude, gabaritos)
    │  └─ Score Geral = (EITA + Código + Didática + Exercícios) / 4
    └─ Mostrar no `relatorios/` ao fim de cada sessão

Dependências: Fase 1-5 completas
Estimativa: 8-12 horas (integração ao fluxo, not coding)
Critério de Sucesso: Toda obra nova passa em Gates 1-4, <5 warnings em Gate 5
```

---

## PARTE 5: ROADMAP CONSOLIDADO

### 5.1 Timeline Sugerida

```
┌─────────────────┬──────────────────────┬────────────────┬─────────────┐
│ FASE            │ TAREFAS              │ HORAS          │ SEMANA      │
├─────────────────┼──────────────────────┼────────────────┼─────────────┤
│ 1. Gates Determ │ Gate 1,2,4 + integ   │ 6-8h           │ Semana 1    │
│ 2. Acessiblid  │ Gate 3 + glossário    │ 8-10h          │ Sem 1-2     │
│ 3. Exercícios   │ Templates + gabarit  │ 12-16h         │ Sem 2-3     │
│ 4. LLM Judge    │ Gate 5 + ref check   │ 10-14h         │ Sem 3-4     │
│ 5. Retrofit 4C  │ Fixes + validação    │ 40-50h         │ Sem 4-5     │
│ 6. Fluxo Futuro │ Integração + dash    │ 8-12h          │ Sem 5       │
├─────────────────┼──────────────────────┼────────────────┼─────────────┤
│ TOTAL           │                      │ 84-110 HORAS   │ ~5 SEMANAS  │
└─────────────────┴──────────────────────┴────────────────┴─────────────┘

Parallelizável:
- Fase 1 (Gate 1,2,4) e Fase 2 (Gate 3) podem rodar em paralelo → 1 semana
- Fase 3 e 4 sequenciais, mas Fase 5 pode rodar em paralelo (4 livros) → -10h
- **Realista:** 5-6 semanas se serial, 3-4 se parallelizado

Custo (estimado):
- Development: 84-110h × USD 50/h = USD 4.2-5.5k
- LLM (Gate 5): 4 livros × 4 caps × USD 0.001 = USD 0.016 (negligível)
- Total: ~USD 4.2-5.5k
```

---

## PARTE 6: MÉTRICAS DE SUCESSO (10/10 Definition)

### 6.1 Score EITA (25 pontos)

```
[ ] 7/7 seções presentes (Intro, Explica, Ilustra, Técnica, Aplica, Conclusão, Refs)
[ ] Explica >200 palavras
[ ] Ilustra tem diagrama ou metáfora
[ ] Técnica tem >=2 exemplos de código/config
[ ] Aplica tem erro comum + solução
[ ] Referências >=5 (ou minimo do config_obra)

Score: 25 se tudo OK, reduz 3-5 pontos por seção incompleta
```

---

### 6.2 Score Código (25 pontos)

```
[ ] Python: syntax válido (py_compile OK)
[ ] JSON: válido (json.loads OK)
[ ] LangGraph: handlers definidos (se usado)
[ ] Retry: trata edge cases (KeyboardInterrupt, timeout)
[ ] Imports: todos presentes (não falta `import X`)
[ ] Indentação: correta
[ ] Copy-paste-ability: LLM judge >=80%

Score: 25 se tudo OK, -2 por erro detectado, -5 se copy-paste <80%
```

---

### 6.3 Score Didática (25 pontos)

```
[ ] TL;DR por capítulo (1-3 linhas)
[ ] Jargão técnico definido (1ª menção)
[ ] Feedforward vs Feedback: claro qual é qual
[ ] Readability score (Flesch-Kincaid PT-BR) >= 50
[ ] Parágrafos <=4 linhas (não blocos textuais)
[ ] Tabelas de decisão presentes (ex: "Quando usar X")
[ ] Non-dev compreensão: LLM judge >=60%

Score: 25 se tudo OK, -3 por gap, -5 se readability <50 ou non-dev <60%
```

---

### 6.4 Score Exercícios (25 pontos)

```
[ ] Cada capítulo tem "Seu Turno" ou "Exercício"
[ ] Exercício tem: [Descrição] [Contexto] [Tarefa] [Restrições]
[ ] Gabarito/solução existe e é acessível
[ ] Checklist de implementação presente
[ ] Exercício não é trivial (não é "responda sim/não")

Score: 25 se tudo OK, BLOQUEADO (-100) se nenhum exercício
```

---

### 6.5 Score Geral = (EITA + Código + Didática + Exercícios) / 4

```
Score Final   Interpretation
──────────────────────────────
95-100        🟢 10/10 — LIBERAR (pronto para produção)
85-94         🟡 8-9/10 — AVISOS (pequenos fixes antes de liberar)
70-84         🟠 7/10 — BLOQUEADO (revisão técnica requirida)
<70           🔴 <7/10 — REJEITAR (redação incompleta)
```

---

### 6.6 Exemplo: Score 4-Camadas Atual

| Livro | EITA | Código | Didática | Exerc | Geral | Status |
|---|---|---|---|---|---|---|
| TELA | 22 | 18 | 21 | 15 | **19/25** = 76% | 🟠 Bloqueado |
| HARNESS | 22 | 16 | 20 | 10 | **17/25** = 68% | 🔴 Rejeitar |
| LLM | 23 | 17 | 19 | 12 | **17.75/25** = 71% | 🟠 Bloqueado |
| TOOLS | 21 | 15 | 18 | 8 | **15.5/25** = 62% | 🔴 Rejeitar |

**Atual GERAL = (76+68+71+62)/4 = 69.25%** = "7/10 - Rejeitar"

**Alvo após Retrofit = 95%+** = "10/10 - Liberar"

---

## PARTE 7: DEPENDÊNCIAS & RISCOS

### 7.1 Dependências

```
PYTHON LIBS NECESSÁRIAS:
├─ textstat (readability scores)
├─ requests (link checking)
├─ ast / json (code validation)
├─ enchant ou similar (PT-BR spell check)
├─ python-docx (optional, para .docx export)
└─ anthropic (para LLM judge)

ARQUIVOS A CRIAR:
├─ scripts/gate_*.py (5 arquivos)
├─ scripts/quality_dashboard.py
├─ templates/seu-turno-template.md
├─ solucoes/cap_*_gabarito.md (N arquivos)
├─ referencia/glossario.md
└─ .github/workflows/gates-ci.yml (optional, para rodar em CI)

SCRIPTS A REFATORAR:
├─ pool-capitulos.py (chamar gates antes de juntar)
├─ subagente-redator-capitulo.md (adicionar checklist EITA)
├─ revisor-tecnico.md (validar 10/10 antes de liberar)
└─ compilador-abnt.py (validação final pré-PDF)
```

---

### 7.2 Riscos & Mitigação

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| **Gate muito rígido** | MÉDIA | ALTA | Fase de calibração: rodar em amostra, ajustar thresholds |
| **LLM judge inconsistente** | MÉDIA | MÉDIA | Usar modelo fixo (Haiku), cache de prompts, múltiplas tentativas |
| **Ref links mudam** | BAIXA | BAIXA | Cache de verificações, marcar como "não-testada offline" |
| **PT-BR spell check ruim** | MÉDIA | BAIXA | Usar dicionário confiável (ASPELL), whitelist de termos técnicos |
| **Tempo de execução + gates** | ALTA | MÉDIA | Paralelizar gates, fazer async com asyncio |
| **Novos tipos de obra** | BAIXA | MÉDIA | Gate 1 é genérico EITA, gates 2-5 adaptam por tipo |

---

## PARTE 8: ESTRUTURA DE GOVERNANÇA

### 8.1 Quem faz o quê?

```
┌─────────────────────────────────────────────────────┐
│ GOVERNO DE QUALIDADE 10/10                           │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Operador (você)                                      │
│ ├─ Define spec, autoriza fases, revisa retrofits    │
│ └─ Toma decisão final: "Está 10/10?"                │
│                                                      │
│ Engenheiro de Qualidade (humano + scripts)           │
│ ├─ Implementa gates                                  │
│ ├─ Calibra thresholds (readability, copy-paste)     │
│ ├─ Revisa LLM judges (evitar false-positives)       │
│ └─ Mantém dashboard                                 │
│                                                      │
│ Redator-Capítulo (subagente)                         │
│ ├─ Segue checklist EITA                             │
│ ├─ Inclui "Seu Turno"                               │
│ ├─ Garante código copy-paste-able                   │
│ └─ Submete com expectativa: "Vai passar em gates"   │
│                                                      │
│ Revisor-Técnico (subagente)                          │
│ ├─ Valida não apenas factual, mas também 10/10     │
│ ├─ Usa checklist de gates                           │
│ ├─ Solicita fixes se gate falha                     │
│ └─ Libera SÓ se score >=95%                         │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

### 8.2 Checklist de Autorização por Fase

**ANTES DE INICIAR FASE 1:**
- [ ] Operador aprova roadmap
- [ ] Budget de 84-110 horas aprovado
- [ ] Timeline de 5-6 semanas OK
- [ ] Dependências Python instaladas

**ANTES DE INICIAR FASE 5 (Retrofit):**
- [ ] Fases 1-4 100% completas
- [ ] Teste em amostra (1 cap) passou
- [ ] Gaps conhecidos documentados

**ANTES DE LIBERAR SÉRIE 4-CAMADAS EM 10/10:**
- [ ] Gates 1-4 passam 100%
- [ ] Gate 5 warnings <5 por livro
- [ ] Score Geral >= 95%
- [ ] Code review manual completo
- [ ] PDF recompilado e testado

---

## PARTE 9: PRÓXIMOS PASSOS PÓS-IMPLEMENTAÇÃO

### 9.1 Manutenção Contínua

```
SEMANAL:
├─ Rodar gates em todas obras em progresso
├─ Revisar warnings do Gate 5
└─ Ajustar thresholds se muitos false-positives

MENSAL:
├─ Revisar tipos de falhas mais comuns
├─ Atualizar templates se padrão emerge
├─ Calibrar LLM judges (novo modelo? nova abordagem?)
└─ Publicar relatório de qualidade

TRIMESTRAL:
├─ Auditoria de 10% amostra aleatória
├─ Entrevista com leitores (conseguem aplicar?)
├─ Ajustar definição de 10/10 se necessário
└─ Treinar novos redatores no processo
```

---

### 9.2 Expansão para Outros Tipos

```
HOJE: Livro (série 4-Camadas)
PRÓXIMO: Playbook, E-book (compatíveis com gates atuais)
DEPOIS: TCC, Artigo (adaptar Gate 3 para academicidade)
DEPOIS: Lead Magnet, Deck (adaptar Gate 4 para design/CTA)
```

---

## PARTE 10: SUMÁRIO EXECUTIVO (1 página)

### O QUE FALTA PARA 10/10 HOJE

| Área | Gap | Impacto | Fix Time |
|---|---|---|---|
| **Código** | LangGraph incompleto, retry sem edge-case | Copy-paste quebra | 4h |
| **Didática** | Sem TL;DR, jargão mal explicado, dense | Non-dev desiste | 6h |
| **Exercícios** | "Seu Turno" falta ou sem gabarito | Passivo, não fixa | 12h |
| **Acessibilidade** | Non-dev score baixo, refs não-verificáveis | Credibilidade | 8h |

**Total para elevar 4-Camadas:** ~40-50h

### SOLUÇÃO PROPOSTA: SISTEMA DE 5 GATES

1. **Gate 1 (EITA)** — Estrutura obrigatória (7 seções)
2. **Gate 2 (Código)** — Syntax + completeness
3. **Gate 3 (Didática)** — Readability + jargão + TL;DR
4. **Gate 4 (Exercícios)** — "Seu Turno" + gabarito obrigatório
5. **Gate 5 (Qualidade)** — LLM as judge (copy-paste, non-dev compreensão)

Todos os gates rodam **automaticamente** após redação, **bloqueiam** saída se falhas críticas.

### ROADMAP: 5-6 SEMANAS

| Semana | Fase | Outcome |
|---|---|---|
| 1 | Gates 1,2,4 | Detectando problemas reais |
| 1-2 | Gate 3 | Didática validada |
| 2-3 | Exercícios | Templates + gabaritos criados |
| 3-4 | Gate 5 | LLM judge calibrado |
| 4-5 | Retrofit 4-Camadas | 4 livros passando em todos gates |
| 5-6 | Fluxo Futuro | Toda obra nova nasce 10/10 |

### INVESTIMENTO

- **Tempo:** 84-110h
- **Custo:** ~USD 4.2-5.5k (dev time, LLM negligível)
- **Retorno:** Série 4-Camadas elevada de 8.1 a 10/10; toda obra futura já nasce pronta

---

## APÊNDICE A: CHECKLIST AUTOR (1 página)

**Redator-Capítulo deve garantir ANTES de submeter:**

```markdown
# Checklist EITA (Obrigatório)
- [ ] Seção "Introdução" escrita (2-3 parágrafos)
- [ ] Seção "Explica" >200 palavras
- [ ] Seção "Ilustra" tem diagrama/metáfora/código
- [ ] Seção "Técnica" tem >=2 exemplos
- [ ] Seção "Aplica" tem erro comum + solução
- [ ] Seção "Conclusão" tie-up com próximo capítulo
- [ ] Seção "Referências" >=5 fontes

# Checklist Código (Obrigatório)
- [ ] Python code: roda sem SyntaxError
- [ ] JSON code: válido (json.loads OK)
- [ ] LangGraph: functions definidas (se usado)
- [ ] Código é copy-paste-able (sem imports faltando)
- [ ] Indentação correta

# Checklist Didática
- [ ] TL;DR ao fim do capítulo
- [ ] Jargão técnico explicado na 1ª menção
- [ ] Parágrafos <=4 linhas
- [ ] Tabelas de decisão se aplicável
- [ ] Analogia "estúdio" mantida (se série 4-Camadas)

# Checklist Exercícios
- [ ] "Seu Turno" ou "Exercício" presente
- [ ] Exercício tem [Descrição] [Contexto] [Tarefa] [Restrições]
- [ ] Você criou gabarito em solucoes/cap_X_gabarito.md
```

---

## APÊNDICE B: REFERÊNCIA RÁPIDA — CADA GATE

### Gate 1: EITA Structure Validator
```bash
python scripts/gate_1_eita_structure.py capitulos/cap_1.md
# Output: PASS (7/7 seções OK) ou FAIL (falta Ilustra)
```

### Gate 2: Code Completeness Validator
```bash
python scripts/gate_2_code_completeness.py capitulos/cap_2.md
# Output: PASS (todos blocos válidos) ou FAIL (Bloco 3: import asyncio falta)
```

### Gate 3: Didactic Accessibility Validator
```bash
python scripts/gate_3_didactic_accessibility.py capitulos/cap_3.md
# Output: PASS (readability 65, jargão OK) ou FAIL (readability 38 < 50)
```

### Gate 4: Exercises Completeness Validator
```bash
python scripts/gate_4_exercises_completeness.py capitulos/cap_4.md
# Output: PASS (exercício + gabarito OK) ou FAIL (falta gabarito: solucoes/cap_4_gabarito.md)
```

### Gate 5: Quality Metrics Validator
```bash
python scripts/gate_5_quality_metrics.py capitulos/cap_1.md config_obra.json
# Output: PASS (copy-paste 92%, non-dev 72%, refs OK) ou AVISO (warnings 3)
```

---

## FIM DO PLANO

**Próximo passo esperado:** Operador revisa, comenta, pede ajustes, aprova fases.

Sem aprovação, **NADA é implementado**.
