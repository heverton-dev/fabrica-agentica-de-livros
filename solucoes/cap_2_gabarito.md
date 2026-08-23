# Gabarito: Cap 2 — Configure um HARNESS Mínimo

## Solução Esperada

Arquivo `settings.json` com estrutura:

```json
{
  "hooks": {
    "post-edit": [
      {
        "matcher": "*.py",
        "command": "python -m py_compile $FILE && echo '[OK] Sintaxe validada' || echo '[ERRO] Sintaxe inválida'"
      }
    ]
  },
  "permissions": {
    "allow": [
      "Read",
      "Edit",
      "Bash(python -m:*)",
      "Bash(ruff:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push:*)",
      "Bash(sudo:*)"
    ]
  }
}
```

## Explicação Linha-por-Linha

### Hook Post-Edit
```json
"post-edit": [
  {
    "matcher": "*.py",                                        // Só roda em arquivos Python
    "command": "python -m py_compile $FILE && echo '[OK]...'" // Validar sintaxe + feedback
  }
]
```

**Por quê:**
- `post-edit` → Roda DEPOIS de cada edição de arquivo
- `matcher: "*.py"` → Só valida Python, não .json, .md, etc.
- `python -m py_compile` → Comando real, valida syntaxe sem executar
- `&& echo '[OK]'` → Feedback visual ao agente de que tudo OK

### Permissões Allow
```json
"allow": [
  "Read",           // Ler arquivos
  "Edit",           // Editar arquivos
  "Bash(python -m:*)", // Rodar módulos Python (py_compile, pytest, etc.)
  "Bash(ruff:*)"    // Rodar linter Ruff
]
```

**Por quê:** Apenas ações necessárias para editar e validar código.

### Permissões Deny
```json
"deny": [
  "Bash(rm -rf:*)",    // Bloquear comando destruidor
  "Bash(git push:*)",  // Bloquear push acidental
  "Bash(sudo:*)"       // Bloquear privilégios elevados
]
```

**Por quê:** Proteção contra acidentes — esses comandos são alta-risco.

---

## Variações Aceitas

### Opção 1: Adicionar Hook de Lint (mais robusto)
```json
"post-edit": [
  {
    "matcher": "*.py",
    "command": "python -m py_compile $FILE && ruff check $FILE --select E,F"
  }
]
```
✅ **Correto** — adicionou validação de estilo (ruff) além de sintaxe.

### Opção 2: Separar Syntax e Lint em Dois Hooks
```json
"post-edit": [
  {
    "matcher": "*.py",
    "command": "python -m py_compile $FILE"
  },
  {
    "matcher": "src/**/*.py",
    "command": "ruff check $FILE"
  }
]
```
✅ **Correto** — mais granular, ruff só roda em `src/`.

### Opção 3: Adicionar Deny Mais Específico
```json
"deny": [
  "Bash(rm -rf /:*)",  // Só bloqueia raíz, permite "rm -rf projeto/"
  "Bash(git push origin main:*)"  // Só bloqueia push pra main
]
```
✅ **Correto** — mais granular, permite algumas remoções.

---

## Erros Comuns

### ❌ Erro 1: Matcher Genérico
```json
{
  "matcher": "*",  // ERRADO — roda em TUDO
  "command": "..."
}
```
**Problema:** Hook roda em `.md`, `.json`, `.txt` também. Ineficiente.

**Corrigir:** `"matcher": "*.py"`

---

### ❌ Erro 2: Permissão Muito Aberta
```json
"allow": ["Bash(*)"]  // ERRADO — acesso total ao terminal
```
**Problema:** Agente pode rodar `rm -rf`, `sudo`, etc.

**Corrigir:** Especificar exatamente o quê é permitido.

---

### ❌ Erro 3: Comando Que Não Existe
```json
{
  "command": "python-check $FILE"  // ERRADO — comando não existe
}
```
**Problema:** Hook falha silenciosamente (ou quebra agente).

**Corrigir:** Usar comandos reais como `python -m py_compile`, `ruff check`.

---

### ❌ Erro 4: Deny Sem Glob Pattern
```json
"deny": ["Bash(rm)"]  // INCOMPLETO — falta padrão
```
**Problema:** Sintaxe incorreta. Deve ser `Bash(rm:*)`.

**Corrigir:** `"deny": ["Bash(rm -rf:*)"]`

---

## Checklist de Validação

- [ ] Hook `post-edit` valida código Python após edição
- [ ] Matcher é específico (`*.py`, não `*`)
- [ ] Comando existe (`python -m py_compile` é real)
- [ ] Permissões `deny` bloqueiam `rm -rf`, `git push`, `sudo`
- [ ] Permissões `allow` são específicas (não `Bash(*)`)
- [ ] JSON é válido (sem erros de vírgula, aspas)

---

## Teste a Solução

1. **Salve** o `settings.json` no diretório do projeto
2. **Edite** um arquivo Python (ex: adicione um comentário)
3. **Verifique:** Hook deve rodar `py_compile` automaticamente
4. **Teste deny:** Tente digitar `!rm -rf .` — deve ser bloqueado

---

## Próximo Passo

Agora que tem um HARNESS mínimo, leia **Cap 3** para aprender a criar hooks mais poderosos (CI, linting automático, notificações).
