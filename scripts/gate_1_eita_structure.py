#!/usr/bin/env python3
"""
GATE 1: EITA Structure Validator
Verifica se capítulo tem 7 seções obrigatórias (EITA pattern)
"""

import os
import re
import sys
import unicodedata
from pathlib import Path

def console_utf8():
    """Force UTF-8 on Windows console."""
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

console_utf8()

SECOES_OBRIGATORIAS = [
    "Introdução",
    "Explica",
    "Ilustra",
    "Técnica",
    "Aplica",
    "Conclusão",
    "Referências"
]

TAMANHO_MINIMO_EXPLICA = 200  # palavras

def extract_sections(markdown_text):
    """Extrair seções de um documento markdown."""
    secoes = {}
    linhas = markdown_text.split("\n")
    secao_atual = None
    conteudo_atual = []

    for linha in linhas:
        # Detectar header level 2 (## Seção)
        match = re.match(r"^## (\d+\. )?(.+)$", linha)
        if match:
            # Salvar seção anterior
            if secao_atual:
                secoes[secao_atual] = "\n".join(conteudo_atual)

            secao_atual = match.group(2).strip()
            conteudo_atual = []
        else:
            if secao_atual:
                conteudo_atual.append(linha)

    # Salvar última seção
    if secao_atual:
        secoes[secao_atual] = "\n".join(conteudo_atual)

    return secoes

def normalize_text(text):
    """Normalizar texto removendo acentos para comparação."""
    nfd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").lower()

def count_words(text):
    """Contar palavras em texto."""
    return len(text.split())

def has_diagram(text):
    """Verificar se tem diagrama ou metáfora (>150 palavras = ilustração substantiva)."""
    has_mermaid = "```mermaid" in text
    has_code = "```" in text
    has_metaphor = count_words(text) > 150  # Metáfora extensa é válida
    return has_mermaid or has_code or has_metaphor

def validate_eita_structure(arquivo_md):
    """Validar estrutura EITA de um capítulo."""
    try:
        with open(arquivo_md, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        return False, f"Erro ao ler arquivo: {e}"

    secoes = extract_sections(conteudo)
    erros = []

    # Teste 1: Seções obrigatórias presentes (case-insensitive, sem acentos)
    for secao_obrigada in SECOES_OBRIGATORIAS:
        encontrada = False
        normalized_obrigada = normalize_text(secao_obrigada)

        for secao_real in secoes.keys():
            if normalize_text(secao_real) == normalized_obrigada:
                encontrada = True
                break

        if not encontrada:
            erros.append(f"❌ Falta seção: '{secao_obrigada}'")

    # Teste 2: Tamanho mínimo de Explica
    for secao in secoes.keys():
        if "Explica" in secao:
            conteudo_explica = secoes[secao]
            palavras = count_words(conteudo_explica)
            if palavras < TAMANHO_MINIMO_EXPLICA:
                erros.append(
                    f"⚠️  Seção 'Explica' muito curta: {palavras} palavras "
                    f"(mínimo {TAMANHO_MINIMO_EXPLICA})"
                )

    # Teste 3: Diagrama em Ilustra
    for secao in secoes.keys():
        if "Ilustra" in secao:
            conteudo_ilustra = secoes[secao]
            if not has_diagram(conteudo_ilustra):
                erros.append("⚠️  Seção 'Ilustra' sem diagrama ou código")

    # Teste 4: Exemplos em Técnica
    for secao in secoes.keys():
        if "Técnica" in secao:
            conteudo_tecnica = secoes[secao]
            num_blocos = conteudo_tecnica.count("```")
            if num_blocos < 4:  # Mínimo 2 blocos (4 markers)
                erros.append(
                    f"⚠️  Seção 'Técnica' com <2 exemplos: "
                    f"encontrados {num_blocos // 2} blocos"
                )

    # Teste 5: Referências
    for secao in secoes.keys():
        if "Referência" in secao:
            conteudo_refs = secoes[secao]
            num_refs = conteudo_refs.count("[") + conteudo_refs.count("]")
            if num_refs < 10:  # Pelo menos 5 refs = 10 brackets
                erros.append(
                    f"⚠️  Seção 'Referências' com poucas citações: "
                    f"estimado <5 referências"
                )

    if erros:
        return False, "\n".join(erros)

    return True, "✅ EITA Structure: OK"

def main():
    if len(sys.argv) < 2:
        print("Usage: python gate_1_eita_structure.py <arquivo.md>")
        sys.exit(1)

    arquivo = sys.argv[1]

    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        sys.exit(1)

    print(f"\n📋 GATE 1: EITA Structure Validator")
    print(f"━" * 60)
    print(f"Validando: {arquivo}\n")

    passed, message = validate_eita_structure(arquivo)

    print(message)

    if passed:
        print(f"\n✅ PASSED: Estrutura EITA válida\n")
        sys.exit(0)
    else:
        print(f"\n❌ FAILED: Estrutura EITA inválida\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
