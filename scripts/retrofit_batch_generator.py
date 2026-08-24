#!/usr/bin/env python3
"""
Retrofit Batch Generator
Gera exercícios e gabaritos para todos os capítulos
"""

import os
import json
from pathlib import Path

def console_utf8():
    import sys
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

console_utf8()

# Template de exercício por livro
TEMPLATES = {
    "tela-camada-agente": {
        "titulo": "Seu Turno: Configure a Camada TELA",
        "instrucoes": """Neste exercício, você vai criar um CLAUDE.md mínimo para seu projeto.

**Contexto:** Você tem um projeto de IA que precisa de configuração clara.

**Tarefa:** Crie um arquivo `CLAUDE.md` com:
1. Seção de convenções de código (linguagem, indentação, etc.)
2. Seção de permissões (o que o agente NÃO pode fazer)
3. Seção de skills (skills reutilizáveis para este projeto)

**Restrições:**
- Máximo 1 página
- Deve ser específico do seu projeto (não genérico)

Gabarito: `solucoes/cap_X_gabarito.md`"""
    },
    "harness-segunda-camada": {
        "titulo": "Seu Turno: Configure um HARNESS Mínimo",
        "instrucoes": """Neste exercício, você vai configurar hooks e permissões básicas.

**Contexto:** Seu agente executa muitos comandos e precisa de proteção.

**Tarefa:** Crie um arquivo `settings.json` com:
1. Hook `post-edit` que valida código
2. Permissões `deny` para comandos perigosos
3. Permissões `allow` específicas

**Restrições:**
- Sem usar `*` genérico
- Todos os comandos devem existir

Gabarito: `solucoes/cap_X_gabarito.md`"""
    },
    "llm-terceira-camada": {
        "titulo": "Seu Turno: Entenda Prompt Engineering vs Context Engineering",
        "instrucoes": """Neste exercício, você vai comparar 2 abordagens de otimização.

**Contexto:** Você precisa melhorar a qualidade de respostas do agente.

**Tarefa:** Escreva 1 página comparando:
1. Prompt Engineering (reescrever instruções)
2. Context Engineering (preparar melhor o contexto)

Para cada abordagem: quando usar? qual custo? qual resultado?

Gabarito: `solucoes/cap_X_gabarito.md`"""
    },
    "tools-quarta-camada": {
        "titulo": "Seu Turno: Projete uma Tool para seu Caso de Uso",
        "instrucoes": """Neste exercício, você vai desenhar uma tool.

**Contexto:** Seu agente precisa de uma capacidade nova que não existe.

**Tarefa:** Descreva uma tool com:
1. Nome, objetivo, inputs, outputs
2. Onde vive (API, local command, MCP server?)
3. Como agente a chama

**Restrições:**
- Deve ser real (não ficção)
- Máximo 1 página

Gabarito: `solucoes/cap_X_gabarito.md`"""
    }
}

TLDR_TEMPLATE = """
### TL;DR (Resumo)

{conteudo}
"""

def generate_exercise_section(livro, cap_num):
    """Gerar seção 'Seu Turno'."""
    template = TEMPLATES.get(livro, TEMPLATES["harness-segunda-camada"])

    section = f"""
### Seu Turno: {template['titulo'].split(':')[1].strip()}

{template['instrucoes']}

"""
    return section

def generate_gabarito_file(livro, cap_num, titulo):
    """Gerar arquivo de gabarito."""
    livro_nomes = {
        "tela-camada-agente": "TELA",
        "harness-segunda-camada": "HARNESS",
        "llm-terceira-camada": "LLM",
        "tools-quarta-camada": "TOOLS"
    }

    livro_nome = livro_nomes.get(livro, "DESCONHECIDO")

    gabarito = f"""# Gabarito: Cap {cap_num} — {livro_nome}

## Solução Esperada

(Aqui vai a solução completa do exercício)

## Explicação

(Aqui vai a explicação linha-por-linha ou conceitual)

## Variações Aceitas

(Aqui vão outras respostas válidas)

## Erros Comuns

(Aqui vão os erros típicos e como evitá-los)

## Checklist de Validação

- [ ] Requisito 1 atendido
- [ ] Requisito 2 atendido
- [ ] Requisito 3 atendido

---

**Próximo passo:** Avançar para Cap {cap_num + 1}
"""

    return gabarito

def scan_chapters():
    """Escanear capítulos e gerar stats."""
    base_path = Path("output/tela-camada-agente/livros")
    livros = [d for d in base_path.iterdir() if d.is_dir()]

    stats = {}

    for livro_path in sorted(livros):
        livro = livro_path.name
        caps_path = livro_path / "capitulos"

        if not caps_path.exists():
            continue

        caps = sorted([f for f in caps_path.glob("cap_*.md")])
        stats[livro] = {
            "total": len(caps),
            "caps": [f.stem for f in caps]
        }

    return stats

def main():
    print("\n🔧 Retrofit Batch Generator")
    print("━" * 60)

    stats = scan_chapters()

    print(f"\nCapítulos encontrados:")
    for livro, info in stats.items():
        print(f"  📚 {livro}: {info['total']} capítulos")

    # Criar diretório solucoes se não existir
    os.makedirs("solucoes", exist_ok=True)

    # Gerar gabaritos para todos os caps (template)
    total_gabaritos = 0
    for livro, info in stats.items():
        for cap_num in range(1, info['total'] + 1):
            gabarito_file = f"solucoes/cap_{cap_num}_gabarito.md"

            # Não sobrescrever se já existe
            if os.path.exists(gabarito_file):
                print(f"  ✓ Gabarito {gabarito_file} já existe")
                continue

            titulo = f"Capítulo {cap_num} ({livro})"
            gabarito = generate_gabarito_file(livro, cap_num, titulo)

            with open(gabarito_file, "w", encoding="utf-8") as f:
                f.write(gabarito)

            print(f"  ✅ Gerado: {gabarito_file}")
            total_gabaritos += 1

    print(f"\n✅ {total_gabaritos} gabaritos gerados")
    print("\n📝 Próximos passos:")
    print("  1. Editar manualmente os gabaritos em solucoes/")
    print("  2. Adicionar exercícios aos capítulos (usar templates)")
    print("  3. Rodar gates para validar")

if __name__ == "__main__":
    main()
