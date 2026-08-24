#!/usr/bin/env python3
"""
GATE 2: Code Completeness Validator
Verifica se código em markdown é válido e executável
"""

import os
import sys
import json
import re

def console_utf8():
    """Force UTF-8 on Windows console."""
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

console_utf8()

def extract_code_blocks(markdown_text):
    """Extrair blocos de código do markdown."""
    blocos = []
    linhas = markdown_text.split("\n")
    dentro_bloco = False
    linguagem = None
    conteudo_bloco = []
    num_bloco = 0

    for i, linha in enumerate(linhas):
        # Detectar início de bloco
        if linha.startswith("```"):
            if not dentro_bloco:
                dentro_bloco = True
                linguagem = linha[3:].strip() or "text"
                conteudo_bloco = []
                num_bloco += 1
            else:
                dentro_bloco = False
                blocos.append({
                    "num": num_bloco,
                    "lang": linguagem,
                    "code": "\n".join(conteudo_bloco),
                    "linha": i - len(conteudo_bloco)
                })
        elif dentro_bloco:
            conteudo_bloco.append(linha)

    return blocos

def validate_python_syntax(code):
    """Validar sintaxe Python."""
    try:
        compile(code, "<code>", "exec")
        return True, "OK"
    except SyntaxError as e:
        return False, f"SyntaxError em linha {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Erro: {e}"

def validate_json_syntax(code):
    """Validar JSON."""
    try:
        json.loads(code)
        return True, "OK"
    except json.JSONDecodeError as e:
        return False, f"JSONDecodeError: {e.msg} em linha {e.lineno}"
    except Exception as e:
        return False, f"Erro: {e}"

def check_missing_imports(code):
    """Detectar imports faltantes."""
    # Padrão simples: procurar "import X" ou "from X import Y"
    import_statements = re.findall(r"^(?:import|from)\s+(\w+)", code, re.MULTILINE)
    used_modules = set(import_statements)

    # Procurar usos de módulos sem import
    common_modules = {
        "asyncio", "json", "os", "sys", "re", "time", "random",
        "anthropic", "langgraph", "langchain", "requests",
        "pytest", "unittest", "datetime", "logging"
    }

    missing = []
    for module in common_modules:
        # Se menciona módulo no código mas não importa
        if module in code and module not in used_modules:
            missing.append(module)

    return missing

def check_indentation(code):
    """Validar indentação (Python)."""
    linhas = code.split("\n")
    erros = []

    for i, linha in enumerate(linhas[1:], start=1):
        if not linha or linha[0] not in (" ", "\t"):
            continue

        # Se linha anterior termina com ":" e esta não tem indentação
        if i > 0 and linhas[i-1].rstrip().endswith(":"):
            if linha and linha[0] not in (" ", "\t"):
                erros.append(f"Linha {i}: esperava indentação após ':'")

    return erros

def check_langgraph_completeness(code):
    """Verificar se LangGraph tem handlers definidos."""
    has_state_graph = "StateGraph" in code
    has_handlers = bool(re.search(r"def \w+_node\(", code))

    if has_state_graph and not has_handlers:
        return False, "LangGraph usa StateGraph mas não define funções node (def *_node)"

    return True, "OK"

def validate_code_completeness(arquivo_md):
    """Validar completeness de todo código no arquivo."""
    try:
        with open(arquivo_md, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        return False, f"Erro ao ler: {e}"

    blocos = extract_code_blocks(conteudo)
    erros = []

    if not blocos:
        return True, "✅ Nenhum bloco de código"

    for bloco in blocos:
        lang = bloco["lang"]
        code = bloco["code"].strip()

        if not code:
            continue

        # Teste 1: Sintaxe Python
        if lang == "python":
            passed, msg = validate_python_syntax(code)
            if not passed:
                erros.append(f"Bloco {bloco['num']} (python, linha {bloco['linha']}): {msg}")

            # Teste 2: Imports faltando (SKIP — muitos falsos positivos)
            # missing = check_missing_imports(code)
            # if missing:
            #     erros.append(
            #         f"Bloco {bloco['num']} (python): "
            #         f"Imports faltando: {', '.join(missing)}"
            #     )

            # Teste 3: Indentação
            indent_erros = check_indentation(code)
            if indent_erros:
                erros.extend([
                    f"Bloco {bloco['num']} (python): {e}"
                    for e in indent_erros
                ])

        # Teste 4: Sintaxe JSON
        elif lang == "json":
            passed, msg = validate_json_syntax(code)
            if not passed:
                erros.append(f"Bloco {bloco['num']} (json): {msg}")

        # Teste 5: LangGraph completeness
        if "StateGraph" in code or "LangGraph" in code:
            passed, msg = check_langgraph_completeness(code)
            if not passed:
                erros.append(f"Bloco {bloco['num']} (langgraph): {msg}")

    if erros:
        return False, "\n".join(erros)

    return True, f"✅ Código OK ({len(blocos)} blocos validados)"

def main():
    if len(sys.argv) < 2:
        print("Usage: python gate_2_code_completeness.py <arquivo.md>")
        sys.exit(1)

    arquivo = sys.argv[1]

    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        sys.exit(1)

    print(f"\n💾 GATE 2: Code Completeness Validator")
    print(f"━" * 60)
    print(f"Validando: {arquivo}\n")

    passed, message = validate_code_completeness(arquivo)

    if message.startswith("✅"):
        print(message)
        print(f"\n✅ PASSED: Código válido\n")
        sys.exit(0)
    else:
        print(message)
        print(f"\n❌ FAILED: Código inválido\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
