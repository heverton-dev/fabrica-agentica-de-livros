# 📄 Como Gerar o PDF do Manual

Devido a limitações de dependências do sistema para PDF headless, o formato **recomendado é HTML** (que já está completamente formatado e pronto).

## ✅ Opção 1: HTML → PDF pelo Navegador (RECOMENDADO)

### Passo 1: Abrir o arquivo
```bash
open livro.html
# ou simplesmente double-click no arquivo
```

### Passo 2: Imprimir como PDF
- **Chrome/Chromium**: `Ctrl+P` → "Salvar como PDF"
- **Firefox**: `Ctrl+P` → "Imprimir em arquivo" → PDF
- **Safari**: `Cmd+P` → "PDF" → "Salvar como PDF"

### Resultado
- ✅ Capa colorida
- ✅ Sumário
- ✅ Diagramas Mermaid
- ✅ Tabelas formatadas
- ✅ Código com syntax highlight
- ✅ Páginas numeradas
- ✅ Espaçamento profissional

---

## ⚡ Opção 2: Converter Markdown direto (se tiver Pandoc + pdflatex/typst)

```bash
# Instalação necessária:
# - Pandoc (https://pandoc.org)
# - MikTeX ou TeX Live (pdflatex)
# - OU Typst (https://typst.app)

# Usar template da fábrica
pandoc livro.md \
  --template ../../../../templates/template.typ \
  --toc \
  --number-sections \
  -V title="Manual OmniRoute" \
  -V author="Marketing Conexão" \
  -V cor_acento="#2563eb" \
  -o manual-omniroute.pdf
```

---

## 📋 Alternativa: Markdown para PDF com Typst

Se tiver **Typst** instalado (recomendado para qualidade profissional):

```bash
# 1. Converter Markdown → Typst
pandoc livro.md \
  --from markdown \
  --to typst \
  --output _manual.typ \
  --template ../../../../templates/template.typ

# 2. Compilar Typst → PDF
typst compile --root . _manual.typ manual-omniroute.pdf

# 3. Limpar
rm _manual.typ
```

---

## ✨ Por que HTML é melhor agora

- ✅ Sem dependências (funciona em qualquer navegador)
- ✅ Renderização rápida
- ✅ Diagramas Mermaid já inclusos
- ✅ Responsivo (mobile-friendly)
- ✅ Suporta temas (claro/escuro)
- ✅ PDF pelo navegador = qualidade máxima

---

## 📦 Arquivos Disponíveis

| Arquivo | Formato | Usar Para |
|---------|---------|-----------|
| `livro.html` | Web + Print | **Recomendado** - abrir e imprimir como PDF |
| `livro.md` | Markdown | Editar conteúdo |
| `manual-omniroute.pdf` | PDF básico | Fallback (sem capa/diagramas) |
| `capitulos/*.md` | Markdown | Editar capítulos individuais |

