#!/bin/bash
# Script de compilação do Manual OmniRoute para PDF
# Segue padrão: Pandoc (Markdown) → Typst → PDF

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIVRO_DIR="$SCRIPT_DIR"
CAPITULOS_DIR="$LIVRO_DIR/capitulos"
OUTPUT_PDF="$LIVRO_DIR/manual-omniroute.pdf"
TEMP_MD="$LIVRO_DIR/_manual_temp.md"
TEMP_TYP="$LIVRO_DIR/_manual_temp.typ"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📚 Compilando Manual OmniRoute para PDF...${NC}"

# 1. Consolidar capítulos em um único Markdown
echo -e "${YELLOW}[1/4] Consolidando capítulos...${NC}"
cat > "$TEMP_MD" << 'HEADER'
# Manual OmniRoute
## 15 Provedores de IA Gratuitos para Máxima Confiabilidade

---

**Data**: 24 de agosto de 2026
**Versão**: 1.0
**Autor**: Marketing Conexão
**Editor**: Editora Agêntica

---

HEADER

# Adicionar todos os capítulos
for cap in "$CAPITULOS_DIR"/01-*.md "$CAPITULOS_DIR"/02-*.md "$CAPITULOS_DIR"/03-*.md "$CAPITULOS_DIR"/04-*.md "$CAPITULOS_DIR"/05-*.md; do
    if [ -f "$cap" ]; then
        echo -e "${GREEN}  ✓ $(basename "$cap")${NC}"
        cat "$cap" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "---" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
done

# 2. Converter Markdown para Typst
echo -e "${YELLOW}[2/4] Convertendo para Typst...${NC}"
if ! command -v pandoc &> /dev/null; then
    echo -e "${RED}❌ Pandoc não encontrado. Instale com: apt-get install pandoc${NC}"
    exit 1
fi

pandoc "$TEMP_MD" \
    --from markdown \
    --to typst \
    --output "$TEMP_TYP" \
    --template /dev/null \
    2>/dev/null || echo -e "${YELLOW}⚠️  Aviso: Conversão Typst parcial${NC}"

# 3. Compilar Typst para PDF
echo -e "${YELLOW}[3/4] Compilando Typst → PDF...${NC}"
if command -v typst &> /dev/null; then
    typst compile --root "$LIVRO_DIR" "$TEMP_TYP" "$OUTPUT_PDF" 2>/dev/null || \
        echo -e "${YELLOW}⚠️  Aviso: Typst não compilou. Alternativa: Pandoc direto${NC}"
else
    echo -e "${YELLOW}⚠️  Typst não instalado. Tentando Pandoc direto...${NC}"
    pandoc "$TEMP_MD" \
        --from markdown \
        --to pdf \
        --output "$OUTPUT_PDF" \
        --pdf-engine=wkhtmltopdf 2>/dev/null || \
    pandoc "$TEMP_MD" \
        --from markdown \
        --to pdf \
        --output "$OUTPUT_PDF" 2>/dev/null || \
        echo -e "${RED}❌ Nenhum motor PDF disponível${NC}"
fi

# 4. Limpeza
echo -e "${YELLOW}[4/4] Limpeza...${NC}"
rm -f "$TEMP_MD" "$TEMP_TYP"

# Verificar resultado
if [ -f "$OUTPUT_PDF" ] && [ -s "$OUTPUT_PDF" ]; then
    SIZE=$(du -h "$OUTPUT_PDF" | cut -f1)
    echo -e "${GREEN}✅ PDF compilado com sucesso!${NC}"
    echo -e "${GREEN}📄 Arquivo: $OUTPUT_PDF (${SIZE})${NC}"
else
    echo -e "${RED}❌ Falha na compilação do PDF${NC}"
    exit 1
fi
