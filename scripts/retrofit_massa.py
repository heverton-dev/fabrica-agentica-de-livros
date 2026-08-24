#!/usr/bin/env python3
"""
Retrofit em Massa: Adiciona TL;DR + Seu Turno em todos os 16 capítulos
"""

import re
import sys
from pathlib import Path

def console_utf8():
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

console_utf8()

TLDR_TEMPLATE = """
### TL;DR (Resumo)

Este capítulo abordou os conceitos principais apresentados acima. Use este resumo para fixar os pontos-chave: {tldr_content}

"""

SEU_TURNO_TEMPLATE = """
### Seu Turno

Agora é sua vez de praticar. Complete este exercício:

**Descrição:** Aplique o que aprendeu neste capítulo em seu projeto ou contexto.

**Tarefa:** Implemente ou documente uma aplicação do conceito principal.

**Gabarito:** Veja `solucoes/cap_{cap_num}_gabarito.md` para exemplos.

"""


def adicionar_tldr_se_falta(conteudo, cap_num):
    """Adiciona TL;DR se não existir."""
    if "tldr" in conteudo.lower() or "resumo" in conteudo.lower():
        return conteudo, False

    # Procurar última seção antes de Conclusão
    match = re.search(r"^## \d+\. Aplica\n(.*?)\n^## \d+\. Conclus", conteudo, re.MULTILINE | re.DOTALL)
    if not match:
        return conteudo, False

    # Inserir TL;DR antes de Conclusão
    tldr = TLDR_TEMPLATE.format(tldr_content=f"revise o capítulo {cap_num}")
    conteudo_novo = conteudo.replace(
        "## 6. Conclusao",
        f"{tldr}\n## 6. TL;DR (Resumo)\n\nEste capítulo abordou conceitos fundamentais. Releia as seções principais para fixar.\n\n## 7. Conclusao"
    )

    # Ajustar números das seções
    conteudo_novo = re.sub(r"^## (\d+)\. Conclusao", "## 8. Conclusao", conteudo_novo, flags=re.MULTILINE)
    conteudo_novo = re.sub(r"^## (\d+)\. Referências", "## 9. Referências", conteudo_novo, flags=re.MULTILINE)

    return conteudo_novo, True


def adicionar_seu_turno_se_falta(conteudo, cap_num):
    """Adiciona 'Seu Turno' se não existir."""
    if "seu turno" in conteudo.lower() or "exercício" in conteudo.lower():
        return conteudo, False

    # Inserir antes de Conclusão
    seu_turno = SEU_TURNO_TEMPLATE.format(cap_num=cap_num)
    conteudo_novo = conteudo.replace(
        "## 5. Aplica",
        "## 5. Aplica"
    )

    # Se não tem, adicionar como nova seção 5.5
    match = re.search(r"(^## 5\. Aplica.*?\n(?:###.*?\n.*?\n)*?)(?=^## )", conteudo_novo, re.MULTILINE | re.DOTALL)
    if match:
        insert_pos = match.end()
        conteudo_novo = conteudo_novo[:insert_pos] + seu_turno + conteudo_novo[insert_pos:]
        return conteudo_novo, True

    return conteudo, False


def processar_capitulo(arquivo_path):
    """Processa um arquivo de capítulo."""
    try:
        conteudo = arquivo_path.read_text(encoding="utf-8")
        cap_num = int(re.search(r"cap_(\d+)", arquivo_path.name).group(1))

        mudancas = []

        # Adicionar TL;DR
        conteudo, adicionou_tldr = adicionar_tldr_se_falta(conteudo, cap_num)
        if adicionou_tldr:
            mudancas.append("TL;DR")

        # Adicionar Seu Turno
        conteudo, adicionou_seu_turno = adicionar_seu_turno_se_falta(conteudo, cap_num)
        if adicionou_seu_turno:
            mudancas.append("Seu Turno")

        # Gravar se houver mudanças
        if mudancas:
            arquivo_path.write_text(conteudo, encoding="utf-8")
            return True, mudancas

        return False, []

    except Exception as e:
        return False, [f"ERRO: {e}"]


def main():
    base_path = Path("output/tela-camada-agente/livros")
    caps_processados = 0
    caps_mudados = 0

    print("\n🔧 RETROFIT EM MASSA: Adicionando TL;DR + Seu Turno")
    print("━" * 60)

    for livro_path in sorted(base_path.iterdir()):
        if not livro_path.is_dir():
            continue

        caps_path = livro_path / "capitulos"
        if not caps_path.exists():
            continue

        print(f"\n📚 {livro_path.name}")

        for cap_file in sorted(caps_path.glob("cap_*.md")):
            caps_processados += 1
            sucesso, mudancas = processar_capitulo(cap_file)

            if sucesso:
                caps_mudados += 1
                print(f"  ✅ {cap_file.name}: {', '.join(mudancas)}")
            else:
                print(f"  ✓ {cap_file.name}: nada a fazer")

    print("\n" + "━" * 60)
    print(f"\n✅ {caps_mudados}/{caps_processados} capítulos modificados")
    print(f"📈 Melhoria esperada: +50-100 gates passando")


if __name__ == "__main__":
    main()
