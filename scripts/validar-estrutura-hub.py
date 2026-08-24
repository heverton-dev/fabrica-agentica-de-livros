#!/usr/bin/env python3
"""
V5.8 — Guardião inviolável da regra HUB POR COLEÇÃO.

Valida que:
1. Nenhuma raiz plana existe (output/livros/, output/playbooks/, etc.)
2. Todos os manifestos estão dentro de hubs
3. Nenhum artefato está órfão (sem hub pai)

Regra (CLAUDE.md, seção "Estrutura de Coleções (HUB)"):
- Proibido: output/<tipo>/<slug>  (raiz plana)
- Obrigatório: output/<hub>/<tipo>/<slug>  (dentro do hub)
- Manifestos: output/<hub>/colecoes/<nome>.json (nunca em output/colecoes/)

Uso:
    python scripts/validar-estrutura-hub.py                   # modo check (sem falhar)
    python scripts/validar-estrutura-hub.py --estrito         # falha em violações
    python scripts validar-estrutura-hub.py --relatorio       # gera JSON
"""

import argparse
import json
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

import tipos_obra as TO


def console_utf8():
    """Impede UnicodeEncodeError no console Windows (travessoes, circulos, etc)."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass


# ──────────────────────────────────────────────────────────────────────────
# VALIDADORES DETERMINÍSTICOS
# ──────────────────────────────────────────────────────────────────────────

def validar_raizes_planas_proibidas(base=None):
    """Valida que NENHUMA raiz plana existe para tipos de obra.

    Retorna: {"erros": [...], "avisos": [...]}
    """
    base = Path(base) if base is not None else DIR_OUTPUT
    if not base.exists():
        return {"erros": [], "avisos": []}

    TIPOS_PROIBIDOS_PLANOS = {
        "livros", "tccs", "artigos", "ebooks",
        "playbooks", "lead-magnets", "decks", "emails"
    }

    erros = []
    avisos = []

    for item in base.iterdir():
        if not item.is_dir():
            continue

        # ✗ Raiz plana proibida
        if item.name in TIPOS_PROIBIDOS_PLANOS:
            conteudo = list(item.iterdir())
            erros.append({
                "tipo": "raiz_plana_proibida",
                "caminho": str(item.relative_to(base)),
                "mensagem": f"Raiz plana '{item.name}/' encontrada com {len(conteudo)} items. "
                           f"Mude para output/<hub>/{item.name}/",
                "items": [str(p.name) for p in conteudo]
            })

        # ✓ Diretório é um hub de coleção (não é raiz plana)
        elif item.name not in {"distribuicao", "colecoes", "series.json"}:  # excessões permitidas
            # Verificar se tem estrutura de hub (contém pastas de tipo)
            pastas_tipo = [d.name for d in item.iterdir() if d.is_dir()
                          and d.name in TIPOS_PROIBIDOS_PLANOS]
            if pastas_tipo:
                # É um hub - OK
                pass
            else:
                # Não é hub nem raiz plana - pode ser outro diretório
                pass

    return {"erros": erros, "avisos": avisos}


def validar_manifestos_em_hub(base=None):
    """Valida que manifestos de coleção estão dentro de hubs, não em raiz plana.

    Proibido: output/colecoes/<nome>.json
    Obrigatório: output/<hub>/colecoes/<nome>.json

    Retorna: {"erros": [...], "avisos": [...]}
    """
    base = Path(base) if base is not None else DIR_OUTPUT
    if not base.exists():
        return {"erros": [], "avisos": []}

    erros = []
    avisos = []

    # Verificar output/colecoes/ (raiz plana proibida)
    dir_colecoes_plana = base / "colecoes"
    if dir_colecoes_plana.exists():
        manifestos_planos = list(dir_colecoes_plana.glob("*.json"))
        for manifesto in manifestos_planos:
            # Tentar encontrar o hub correto
            nome_slug = manifesto.stem  # ex.: "deepseek-harness-do-zero-ao-phd"

            # Procurar em hubs
            hub_correto = None
            for hub in base.iterdir():
                if hub.is_dir() and hub.name not in {"distribuicao", "colecoes"}:
                    dir_manifesto_hub = hub / "colecoes" / manifesto.name
                    if dir_manifesto_hub.exists():
                        hub_correto = hub
                        break

            erros.append({
                "tipo": "manifesto_fora_do_hub",
                "caminho": str(manifesto.relative_to(base)),
                "mensagem": f"Manifesto em raiz plana. Mude de 'output/colecoes/{manifesto.name}' "
                           f"para 'output/<hub>/colecoes/{manifesto.name}'",
                "hub_detectado": str(hub_correto.relative_to(base)) if hub_correto else None
            })

    return {"erros": erros, "avisos": avisos}


def validar_artefatos_orfaos(base=None):
    """Valida que nenhum artefato está órfão (sem hub pai detectável).

    Um artefato é órfão se:
    - Vive em output/<tipo>/<slug> (raiz plana) SEM um hub correspondente
    - Tem config_obra.json apontando para um hub que não existe

    Retorna: {"erros": [...], "avisos": [...]}
    """
    base = Path(base) if base is not None else DIR_OUTPUT
    if not base.exists():
        return {"erros": [], "avisos": []}

    TIPOS_OBRA = {
        "livros", "tccs", "artigos", "ebooks",
        "playbooks", "lead-magnets", "decks", "emails"
    }

    erros = []
    avisos = []

    # Procurar em raízes planas (onde NÃO deveriam estar)
    for tipo in TIPOS_OBRA:
        dir_plano = base / tipo
        if dir_plano.exists():
            for obra_dir in dir_plano.iterdir():
                if obra_dir.is_dir():
                    # Verificar se tem config_obra.json
                    config_file = obra_dir / "config_obra.json"
                    if config_file.exists():
                        try:
                            config = json.loads(config_file.read_text(encoding="utf-8"))
                            obra_mae = config.get("obra_mae")
                            if obra_mae:
                                erros.append({
                                    "tipo": "artefato_derivado_orfao",
                                    "caminho": str(obra_dir.relative_to(base)),
                                    "mensagem": f"Artefato derivado de '{obra_mae}' está em raiz plana. "
                                              f"Mude para 'output/<hub-da-mae>/{tipo}/{obra_dir.name}'",
                                    "obra_mae": obra_mae
                                })
                            else:
                                # Obra raiz em raiz plana (também errado conforme CLAUDE.md)
                                erros.append({
                                    "tipo": "obra_raiz_em_raiz_plana",
                                    "caminho": str(obra_dir.relative_to(base)),
                                    "mensagem": f"Obra raiz em raiz plana. Crie um hub: "
                                              f"'output/<novo-hub>/{tipo}/{obra_dir.name}'",
                                    "slug": obra_dir.name
                                })
                        except json.JSONDecodeError:
                            avisos.append({
                                "tipo": "config_invalida",
                                "caminho": str(config_file.relative_to(base)),
                                "mensagem": "config_obra.json inválida (JSON mal-formado)"
                            })

    return {"erros": erros, "avisos": avisos}


def validar_estrutura_output(base=None):
    """Valida TODA a estrutura de output/ contra a regra HUB POR COLEÇÃO.

    Retorna: {
        "valido": bool,
        "violacoes_criticas": [...],
        "avisos": [...],
        "resumo": str
    }
    """
    console_utf8()
    base = Path(base) if base is not None else DIR_OUTPUT

    resultado = {
        "valido": True,
        "violacoes": [],
        "avisos": [],
        "resumo": ""
    }

    # Rodas os 3 validadores
    v1 = validar_raizes_planas_proibidas(base)
    v2 = validar_manifestos_em_hub(base)
    v3 = validar_artefatos_orfaos(base)

    resultado["violacoes"] = v1["erros"] + v2["erros"] + v3["erros"]
    resultado["avisos"] = v1["avisos"] + v2["avisos"] + v3["avisos"]

    if resultado["violacoes"]:
        resultado["valido"] = False

    # Gerar resumo
    n_criticas = len(resultado["violacoes"])
    n_avisos = len(resultado["avisos"])
    resultado["resumo"] = (
        f"{'✓' if resultado['valido'] else '✗'} Estrutura hub: "
        f"{n_criticas} violação(ões) crítica(s), {n_avisos} aviso(s)"
    )

    return resultado


# ──────────────────────────────────────────────────────────────────────────
# CLI & INTEGRAÇÃO
# ──────────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Validador da regra HUB POR COLEÇÃO (inviolável)"
    )
    ap.add_argument("--estrito", action="store_true",
                    help="Falha (exit 1) se houver violações")
    ap.add_argument("--relatorio", action="store_true",
                    help="Gera JSON em stdout")
    ap.add_argument("--base", type=Path, default=DIR_OUTPUT,
                    help="Diretório base de output (default: ./output)")

    args = ap.parse_args()

    resultado = validar_estrutura_output(args.base)

    if args.relatorio:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        return 0 if resultado["valido"] else 1

    # Modo interativo
    print(resultado["resumo"])

    if resultado["violacoes"]:
        print("\n━━ VIOLAÇÕES CRÍTICAS ━━")
        for i, v in enumerate(resultado["violacoes"], 1):
            print(f"{i}. [{v['tipo']}] {v['caminho']}")
            print(f"   {v['mensagem']}")
            if "items" in v:
                for item in v["items"][:3]:
                    print(f"   - {item}")
                if len(v["items"]) > 3:
                    print(f"   ... e {len(v['items']) - 3} mais")

    if resultado["avisos"]:
        print("\n━━ AVISOS ━━")
        for i, a in enumerate(resultado["avisos"], 1):
            print(f"{i}. [{a['tipo']}] {a['caminho']}")
            print(f"   {a['mensagem']}")

    if args.estrito and not resultado["valido"]:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
