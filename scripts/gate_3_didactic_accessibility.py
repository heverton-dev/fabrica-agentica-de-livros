#!/usr/bin/env python3
"""
GATE 3: Didactic Accessibility Validator
Heurísticas simples para validar acessibilidade didática
"""

import os
import sys
import re

def console_utf8():
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

console_utf8()

def count_words(text):
    return len(text.split())

def find_section(markdown, section_name):
    """Procurar seção (case-insensitive)."""
    pattern = rf"^##.*{section_name}.*$"
    matches = re.findall(pattern, markdown, re.IGNORECASE | re.MULTILINE)
    return matches[0] if matches else None

def extract_section_content(markdown, section_name):
    """Extrair conteúdo de uma seção até a próxima ##."""
    pattern = rf"^##.*{section_name}.*$\n(.*?)(?=^##|$)"
    match = re.search(pattern, markdown, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""

def check_tldr(markdown):
    """Verificar se tem TL;DR ou Resumo."""
    tldr_keywords = ["tldr", "resumo", "resumo em uma frase"]
    normalized = markdown.lower()
    found = any(kw in normalized for kw in tldr_keywords)

    if found:
        # Verificar se tem conteúdo (>20 palavras)
        tldr_section = re.search(r"(?:tldr|resumo)[:\s]+(.*?)(?:\n\n|\n##)", normalized, re.IGNORECASE)
        if tldr_section:
            content = tldr_section.group(1)
            if count_words(content) >= 10:
                return True, "TL;DR presente"

    return False, "TL;DR/Resumo falta (recomendado: 1-3 linhas)"

def check_jargao_explained(markdown):
    """Detectar jargão técnico não explicado."""
    jargoes = [
        "self-attention", "token", "context window", "feedforward", "feedback",
        "LLM", "harness", "hook", "checkpoint", "sandbox", "retry",
        "prompt engineering", "context engineering", "langgraph"
    ]

    warnings = []

    for jargao in jargoes:
        if jargao.lower() in markdown.lower():
            # Procurar definição (padrão: "X é", "X —", "X: ", "X significa")
            pattern = rf"{jargao}\s+(?:é|—|:|significa|representa)"
            if not re.search(pattern, markdown, re.IGNORECASE):
                warnings.append(f"⚠️  '{jargao}' não explicado na 1ª menção")

    return len(warnings) <= 2, warnings  # 3+ avisos = problema sério

def check_paragraph_length(markdown):
    """Verificar se tem parágrafos muito longos (>400 palavras)."""
    text_only = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)  # Remove code blocks
    text_only = re.sub(r"#.*?\n", "", text_only)  # Remove headers

    paragrafos = text_only.split("\n\n")
    long_paragrafos = []

    for i, p in enumerate(paragrafos):
        if count_words(p) > 400 and p.strip() and "|" not in p:  # Ignore tabelas
            long_paragrafos.append(f"Parágrafo {i}: {count_words(p)} palavras")

    if long_paragrafos:
        return False, f"Parágrafos muito longos: {', '.join(long_paragrafos[:3])}"

    return True, "Parágrafos legíveis (<400 palavras)"

def check_structure_consistency(markdown):
    """Verificar se seções EITA estão em ordem correta."""
    sections = ["Introdução", "Explica", "Ilustra", "Técnica", "Aplica", "Conclusão"]
    found_sections = []

    for section in sections:
        if find_section(markdown, section):
            found_sections.append(section)

    # Verificar ordem
    expected_order = [s for s in sections if s in found_sections]
    is_correct_order = found_sections == expected_order

    return is_correct_order, f"Ordem: {' → '.join(found_sections[:4])}"

def validate_didactic_accessibility(arquivo_md):
    """Validar acessibilidade didática."""
    try:
        with open(arquivo_md, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        return False, f"Erro ao ler: {e}"

    erros = []
    warnings = []

    # Teste 1: TL;DR presente
    has_tldr, msg = check_tldr(conteudo)
    if not has_tldr:
        warnings.append(msg)

    # Teste 2: Jargão explicado
    jargao_ok, jargao_warnings = check_jargao_explained(conteudo)
    if not jargao_ok:
        warnings.extend(jargao_warnings[:3])

    # Teste 3: Parágrafos legíveis
    para_ok, msg = check_paragraph_length(conteudo)
    if not para_ok:
        warnings.append(msg)

    # Teste 4: Ordem EITA
    order_ok, msg = check_structure_consistency(conteudo)
    warnings.append(msg)  # Informativo

    # Compilar resultado
    if warnings and len(warnings) > 3:
        msg = "\n".join(warnings)
        return False, msg

    if warnings:
        return True, "\n".join(["✅ Acessibilidade OK"] + warnings)

    return True, "✅ Acessibilidade OK"

def main():
    if len(sys.argv) < 2:
        print("Usage: python gate_3_didactic_accessibility.py <arquivo.md>")
        sys.exit(1)

    arquivo = sys.argv[1]
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        sys.exit(1)

    print(f"\n📖 GATE 3: Didactic Accessibility Validator")
    print(f"━" * 60)
    print(f"Validando: {arquivo}\n")

    passed, message = validate_didactic_accessibility(arquivo)

    print(message)

    if passed:
        print(f"\n✅ PASSED: Acessibilidade didática OK\n")
        sys.exit(0)
    else:
        print(f"\n⚠️  AVISO: Melhorar acessibilidade\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
