#!/bin/bash
# Wrapper: Validar um capítulo com todos os Gates
# Uso: bash scripts/validar_capitulo.sh <caminho_cap.md>

CAPITULO="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$CAPITULO" ]; then
    echo "❌ Uso: validar_capitulo.sh <caminho_cap.md>"
    exit 1
fi

if [ ! -f "$CAPITULO" ]; then
    echo "❌ Arquivo não encontrado: $CAPITULO"
    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 VALIDANDO CAPÍTULO COM GATES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Arquivo: $CAPITULO"
echo ""

PASSED=0
FAILED=0

# Gate 1
echo "🔍 Gate 1: EITA Structure..."
if python "$SCRIPT_DIR/gate_1_eita_structure.py" "$CAPITULO" > /dev/null 2>&1; then
    echo "  ✅ PASS"
    ((PASSED++))
else
    echo "  ❌ FAIL"
    ((FAILED++))
fi

# Gate 2
echo "🔍 Gate 2: Code Completeness..."
if python "$SCRIPT_DIR/gate_2_code_completeness.py" "$CAPITULO" > /dev/null 2>&1; then
    echo "  ✅ PASS"
    ((PASSED++))
else
    echo "  ❌ FAIL"
    ((FAILED++))
fi

# Gate 3 (Aviso, não bloqueia)
echo "🔍 Gate 3: Didactic Accessibility..."
if python "$SCRIPT_DIR/gate_3_didactic_accessibility.py" "$CAPITULO" > /dev/null 2>&1; then
    echo "  ✅ PASS"
    ((PASSED++))
else
    echo "  ⚠️  AVISO (não bloqueia)"
fi

# Gate 4
echo "🔍 Gate 4: Exercises Completeness..."
if python "$SCRIPT_DIR/gate_4_exercises_completeness.py" "$CAPITULO" > /dev/null 2>&1; then
    echo "  ✅ PASS"
    ((PASSED++))
else
    echo "  ❌ FAIL"
    ((FAILED++))
fi

# Gate 5
echo "🔍 Gate 5: Quality Metrics..."
if python "$SCRIPT_DIR/gate_5_quality_metrics.py" "$CAPITULO" > /dev/null 2>&1; then
    echo "  ✅ PASS"
    ((PASSED++))
else
    echo "  ⚠️  AVISO (não bloqueia)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TOTAL=$((PASSED + FAILED))
echo "📊 RESULTADO: $PASSED/$TOTAL gates passaram"

if [ $FAILED -eq 0 ]; then
    echo "✅ CAPÍTULO PRONTO ✅"
    exit 0
else
    echo "❌ BLOQUEADO: $FAILED gates falharam"
    exit 1
fi
