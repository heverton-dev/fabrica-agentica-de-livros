#!/usr/bin/env python3
"""
GATE 4: Exercises Completeness Validator
Verifica se capítulo tem exercícios e gabaritos
"""

import os
import sys
import re

def console_utf8():
    """Force UTF-8 on Windows console."""
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

console_utf8()

def has_exercise(markdown_text):
    """Detectar se tem seção 'Seu Turno', 'Exercício', 'Prática'."""
    keywords = ["seu turno", "exercício", "exercicio", "prática", "pratica", "desafio"]
    normalized = markdown_text.lower()

    for keyword in keywords:
        if keyword in normalized:
            return True
    return False

def has_gabarito(num_capitulo):
    """Verificar se arquivo de gabarito existe."""
    gabarito_paths = [
        f"solucoes/cap_{num_capitulo}_gabarito.md",
        f"output/solucoes/cap_{num_capitulo}_gabarito.md",
    ]

    for path in gabarito_paths:
        if os.path.exists(path):
            return True, path

    return False, None

def has_checklist(markdown_text):
    """Detectar se tem checklist de implementação."""
    return "[ ]" in markdown_text or "- [ ]" in markdown_text

def extract_cap_number(filepath):
    """Extrair número do capítulo do caminho."""
    match = re.search(r"cap_(\d+)", filepath)
    if match:
        return int(match.group(1))
    return None

def validate_exercises(arquivo_md):
    """Validar completeness de exercícios."""
    try:
        with open(arquivo_md, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        return False, f"Erro ao ler: {e}"

    num_cap = extract_cap_number(arquivo_md)
    erros = []
    warnings = []

    # Teste 1: Tem exercício?
    if not has_exercise(conteudo):
        erros.append("❌ Falta seção 'Seu Turno', 'Exercício' ou 'Prática'")
    else:
        # Teste 2: Se tem exercício, tem gabarito?
        has_gab, path = has_gabarito(num_cap)
        if not has_gab:
            erros.append(
                f"❌ CRÍTICO: Exercício presente mas gabarito falta "
                f"(esperado: solucoes/cap_{num_cap}_gabarito.md)"
            )
        else:
            warnings.append(f"✅ Gabarito encontrado: {path}")

    # Teste 3: Tem checklist?
    if not has_checklist(conteudo):
        warnings.append("⚠️  Falta checklist [ ] de implementação")

    # Compilar resultado
    if erros:
        return False, "\n".join(erros + warnings)

    if warnings:
        return True, "\n".join(warnings)

    return True, "✅ Exercícios OK (com gabarito)"

def main():
    if len(sys.argv) < 2:
        print("Usage: python gate_4_exercises_completeness.py <arquivo.md>")
        sys.exit(1)

    arquivo = sys.argv[1]

    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        sys.exit(1)

    print(f"\n📝 GATE 4: Exercises Completeness Validator")
    print(f"━" * 60)
    print(f"Validando: {arquivo}\n")

    passed, message = validate_exercises(arquivo)

    print(message)

    if passed:
        print(f"\n✅ PASSED: Exercícios válidos\n")
        sys.exit(0)
    else:
        print(f"\n❌ FAILED: Exercícios inválidos\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
