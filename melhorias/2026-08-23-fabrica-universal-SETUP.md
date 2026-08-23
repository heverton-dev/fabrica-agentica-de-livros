# SETUP: Publicar fabrica-universal no GitHub

**Status:** Repositório pronto localmente em `../fabrica-universal/`

---

## Passo 1: Criar Repositório no GitHub

### Via GitHub Web

1. Ir para https://github.com/new
2. **Repository name:** `fabrica-universal`
3. **Description:** `Infrastructure reusável: governança, padrões, economia de tokens, portabilidade multi-IDE`
4. **Visibility:** Public
5. **Initialize with:** Nada (vamos fazer push do local)
6. Clicar **Create repository**

### Via GitHub CLI (faster)

```bash
gh repo create fabrica-universal \
  --public \
  --description "Infrastructure reutilizável: governança, padrões, economia, portabilidade multi-IDE" \
  --source=. \
  --remote=origin \
  --push
```

---

## Passo 2: Configurar Remote & Push

```bash
cd ../fabrica-universal

# 1. Adicionar remote (substituir seu-usuario)
git remote add origin https://github.com/seu-usuario/fabrica-universal.git

# 2. Verificar
git remote -v

# 3. Push do branch main
git branch -M main
git push -u origin main

# 4. Verificar
git log --oneline
```

---

## Passo 3: Criar GitHub Actions (CI/CD)

### Criar arquivo `.github/workflows/validate.yml`

```yaml
name: Validate Submodule

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Python syntax
        run: python -m py_compile scripts/*.py
      
      - name: CLAUDE.md frontmatter
        run: grep "alwaysApply: true" .claude/CLAUDE.md
      
      - name: Checklist
        run: |
          test -f CLAUDE.md || exit 1
          test -d .claude/skills/caveman || exit 1
          test -f scripts/pdf_typst.py || exit 1
          echo "✅ Validação passou"
```

Push:
```bash
git add .github/
git commit -m "ci: adicionar validacao de submodule"
git push origin main
```

---

## Passo 4: Criar GitHub Release (v1.0.0)

```bash
cd ../fabrica-universal

# Tag
git tag -a v1.0.0 -m "Initial release: universal infrastructure"

# Push tag
git push origin v1.0.0

# Via GitHub UI:
# 1. Ir para Releases
# 2. Clicar "Create a new release"
# 3. Tag: v1.0.0
# 4. Title: "Fábrica Universal v1.0.0"
# 5. Description:
```

**Description para Release:**

```
# Fábrica Universal v1.0.0 — Infraestrutura Reutilizável

## O que é

Componentes universais (40% da Fábrica Agêntica) — **Use como submodule em qualquer projeto**.

Setup: 5 minutos | Domínios: SaaS, Pesquisa, Consultoria, Publicações, etc.

## O Que Vem Nesta Release

- ✅ **CLAUDE.md** com governança R1–R17
- ✅ **RTK.md** — Guia de token economy
- ✅ **5 Skills de economia:** caveman, headroom, lean-ctx, rtk-memory, pre-flight-check
- ✅ **Setup scripts:** setup-links.ps1/.sh (portabilidade multi-IDE)
- ✅ **Padrões reutilizáveis:** templates de skill, script, comando, MCP
- ✅ **Documentation:** README, QUICKSTART, TROUBLESHOOTING

## Como Usar

```bash
# Novo projeto
git init meu-projeto
cd meu-projeto
git submodule add https://github.com/seu-usuario/fabrica-universal.git fabrica-universal
cp -r fabrica-universal/.claude .
./scripts/setup-links.ps1
```

## Próximos Passos

1. Adicionar esta release como submodule em seus projetos
2. Customizar CLAUDE.md para seu domínio
3. Criar skills/comandos/gates específicos de seu escopo
4. Executar `python fabrica-universal/scripts/validate.py`

## Feedback

Issues: [github.com/seu-usuario/fabrica-universal/issues](https://github.com/seu-usuario/fabrica-universal/issues)
```

---

## Passo 5: Adicionar Tópicos (GitHub Tags)

1. Ir para Settings > Topics
2. Adicionar:
   - `infrastructure`
   - `claude-code`
   - `governance`
   - `token-economy`
   - `multi-ide`
   - `reusable`
   - `submodule`

---

## Passo 6: Atualizar em proj_fabrica-de-livros

Agora que `fabrica-universal` está no GitHub, vamos adicionar como submodule em `proj_fabrica-de-livros`:

```bash
cd ../proj_fabrica-de-livros

# Adicionar submodule
git submodule add https://github.com/seu-usuario/fabrica-universal.git fabrica-universal

# Commit
git add .gitmodules fabrica-universal
git commit -m "chore: integrar fabrica-universal como submodule"

# Push
git push origin main
```

---

## Checklist Final

```
GITHUB
[ ] Repositório criado (público, MIT license)
[ ] Remote adicionado e verificado (git remote -v)
[ ] Branch main pushado (git push -u origin main)
[ ] v1.0.0 tag criado e pushed
[ ] Release criada no GitHub
[ ] CI/CD workflow adicionado
[ ] Tópicos adicionados

PROJ_FABRICA-DE-LIVROS
[ ] Submodule adicionado (git submodule add)
[ ] Commit feito
[ ] Push para remote

DOCUMENTAÇÃO
[ ] README.md verifica-se corretamente
[ ] QUICKSTART.md testado
[ ] TROUBLESHOOTING.md presente
```

---

## Comandos Rápidos (Copy-Paste)

```bash
# 1. Configurar remote
cd ../fabrica-universal
git remote add origin https://github.com/SEU_USUARIO/fabrica-universal.git
git branch -M main
git push -u origin main

# 2. Criar tag
git tag -a v1.0.0 -m "Initial release: universal infrastructure"
git push origin v1.0.0

# 3. Adicionar em proj_fabrica
cd ../proj_fabrica-de-livros
git submodule add https://github.com/SEU_USUARIO/fabrica-universal.git fabrica-universal
git add .gitmodules fabrica-universal
git commit -m "chore: integrar fabrica-universal como submodule"
git push origin main
```

---

**Próximo:** Depois que fizer push, enviar as URLs:
- `https://github.com/seu-usuario/fabrica-universal` (repositório)
- `https://github.com/seu-usuario/fabrica-universal/releases/tag/v1.0.0` (release)
