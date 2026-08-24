#!/usr/bin/env python3
"""
GATE 5: Quality Metrics Validator
Heurísticas para copy-paste-ability, refs, ortografia
"""

import os
import sys
import re

def console_utf8():
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

console_utf8()

def extract_code_blocks(markdown_text):
    """Extrair blocos de código."""
    blocos = []
    lines = markdown_text.split("\n")
    in_block = False
    lang = None
    code = []

    for line in lines:
        if line.startswith("```"):
            if not in_block:
                in_block = True
                lang = line[3:].strip() or "text"
                code = []
            else:
                blocos.append({"lang": lang, "code": "\n".join(code)})
                in_block = False
        elif in_block:
            code.append(line)

    return blocos

def check_copy_paste_ability(code_blocks):
    """Verificar se código é copy-paste-able."""
    warnings = []

    for i, block in enumerate(code_blocks):
        if block["lang"] not in ["python", "json"]:
            continue

        code = block["code"]

        # Teste 1: Verificar se tem prompt/instrução (não deve ter)
        if code.startswith(">>>") or code.startswith("#"):
            warnings.append(f"Bloco {i}: Começa com prompt (>>>), remover")

        # Teste 2: Verificar se referencia variável não-definida (heurística)
        common_issues = [
            ("initial_state", "Variável initial_state não definida"),
            ("think_node", "Função think_node não definida"),
            ("MyClass", "Classe MyClass não definida"),
            ("config", "Variável config não definida"),
        ]

        for var, msg in common_issues:
            if var in code and f"{var} =" not in code:
                if block["lang"] == "python":
                    warnings.append(f"Bloco {i}: {msg}")

        # Teste 3: Verificar se comentários explicam tudo
        comment_lines = [l for l in code.split("\n") if l.strip().startswith("#")]
        code_lines = [l for l in code.split("\n") if l.strip() and not l.strip().startswith("#")]

        if len(code_lines) > 10 and len(comment_lines) == 0:
            warnings.append(f"Bloco {i}: Sem comentários explicatórios (código >10 linhas)")

    return warnings if warnings else ["✅ Código copy-paste-able"]

def check_references(markdown_text):
    """Verificar referências."""
    ref_pattern = r"\[(\d+)\]\s+(.+?)(?=\n\[|$)"
    refs = re.findall(ref_pattern, markdown_text, re.MULTILINE | re.DOTALL)

    warnings = []

    for ref_num, ref_text in refs:
        # Verificar se URL parece válida
        if "http" in ref_text:
            url_match = re.search(r"https?://[\w.-]+\.\w+", ref_text)
            if url_match:
                url = url_match.group(0)
                # Heurística: URLs com muitas slashes ou sem domínio claro são suspeitas
                if url.count("/") > 5:
                    warnings.append(f"Ref [{ref_num}]: URL parece inválida ({url})")
                elif "example.com" in url or "blog" in url and "medium.com" not in url:
                    warnings.append(f"Ref [{ref_num}]: URL pode ser blog/site não-confiável")

    return warnings if warnings else ["✅ Referências OK"]

def check_pt_br_spelling_heuristic(markdown_text):
    """Verificar PT-BR ortografia (heurística simples)."""
    common_errors = {
        r"\baí\b": "ai (sem acento)",
        r"\bé\b": "e (sem acento) — se não for fim de verbo",
        r"\blínhas\b": "linhas (com til)",
        r"\bmais\b": "mas (ou mais?)",
        r"\bporquê\b": "porque (4 formas diferentes em PT-BR)",
    }

    warnings = []

    # Apenas avisos leves (não bloqueia)
    text_sample = markdown_text[:2000]  # Apenas primeiras 2000 chars
    if text_sample.count(" e ") > 20 and text_sample.count(" é ") < 3:
        warnings.append("⚠️  Pode haver uso excessivo de 'e' em vez de 'é'")

    return warnings

def validate_quality_metrics(arquivo_md):
    """Validar métricas de qualidade."""
    try:
        with open(arquivo_md, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        return False, f"Erro ao ler: {e}"

    all_warnings = []

    # Teste 1: Copy-paste-ability
    code_blocks = extract_code_blocks(conteudo)
    if code_blocks:
        copy_paste_warnings = check_copy_paste_ability(code_blocks)
        all_warnings.extend(copy_paste_warnings)

    # Teste 2: Referências
    ref_warnings = check_references(conteudo)
    all_warnings.extend(ref_warnings)

    # Teste 3: PT-BR ortografia
    spelling_warnings = check_pt_br_spelling_heuristic(conteudo)
    all_warnings.extend(spelling_warnings)

    # Compilar resultado
    msg = "\n".join(all_warnings)

    # Gate 5 nunca bloqueia (é aviso apenas)
    return True, msg

def main():
    if len(sys.argv) < 2:
        print("Usage: python gate_5_quality_metrics.py <arquivo.md>")
        sys.exit(0)  # Exit 0 mesmo com warnings

    arquivo = sys.argv[1]
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        sys.exit(0)

    print(f"\n⭐ GATE 5: Quality Metrics Validator")
    print(f"━" * 60)
    print(f"Validando: {arquivo}\n")

    passed, message = validate_quality_metrics(arquivo)

    print(message)
    print(f"\n✅ GATE 5 (Aviso somente — não bloqueia)\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
