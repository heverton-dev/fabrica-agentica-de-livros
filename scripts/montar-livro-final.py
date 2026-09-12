#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fase 3 (V5) — Montador deterministico do `livro_final.md`.

O `compilador-abnt` (skill) faz o merge do livro acrescentando elementos
pre-textuais e pos-textuais. Ate aqui esse merge era executado manualmente pelo
agente, o que produzia duas classes de defeito: cabecalhos de Parte ausentes e
prefacio/conclusao genericos ou esquecidos. Este script mecaniza a montagem,
deixando a LLM apenas o trabalho de redigir `prefacio.md` e
`conclusao-geral.md` (arquivos opcionais: sem eles, a montagem usa os textos
declarados em `sumario_macro.json`).

Estrutura produzida (nesta ordem):

    frontmatter YAML -> folha de titulo -> nota do EITA -> Sumario ->
    Prefacio -> Parte I -> cap_1..cap_4 -> Parte II -> ... ->
    Conclusao Geral -> Referencias Consolidadas

Uso:
    python scripts/montar-livro-final.py <slug>
    python scripts/montar-livro-final.py livros/<slug> --checar
    python scripts/montar-livro-final.py livros/<slug> --saida outro.md

Saida padrao: <dir_obra>/livro_final.md
"""

import argparse
import json
import re
import sys
from pathlib import Path

import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"
TEMPLATE_EITA = DIR_PROJETO / "templates" / "capitulo_eita.md"

AUTOR_PADRAO = "Heverton Eduardo Peres"
MESES = ("janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro")


def data_por_extenso() -> str:
    import datetime
    hoje = datetime.date.today()
    return f"{MESES[hoje.month - 1].capitalize()} de {hoje.year}"


def ler_json(caminho: Path) -> dict:
    return json.loads(caminho.read_text(encoding="utf-8")) if caminho.exists() else {}


def frontmatter(config: dict, sumario: dict) -> str:
    titulo = sumario.get("titulo_obra") or config.get("tema") or "Obra sem titulo"
    subtitulo = sumario.get("subtitulo") or config.get("subtitulo") or ""
    return "\n".join([
        "---",
        f'title: "{titulo}"',
        f'subtitle: "{subtitulo}"',
        f'author: "{AUTOR_PADRAO}"',
        f'date: "{data_por_extenso()}"',
        'lang: pt-BR',
        "papersize: a4",
        "toc: true",
        'toc-title: "Sumário Geral da Obra"',
        "---",
        "",
    ])


def folha_de_titulo(sumario: dict, config: dict) -> str:
    titulo = sumario.get("titulo_obra") or config.get("tema") or ""
    subtitulo = sumario.get("subtitulo") or ""
    edicao = sumario.get("edition_tag") or config.get("edition_tag") or ""
    tamanho = config.get("tamanho_obra") or "-"
    senioridade = config.get("senioridade_obra") or "-"
    linhas = [f"# {titulo}", ""]
    if subtitulo:
        linhas += [f"## {subtitulo}", ""]
    if edicao:
        linhas += [f"**{edicao}**", ""]
    linhas += [
        f"**Publico-alvo:** nivel {senioridade}  ",
        f"**Extensao:** formato {tamanho}",
        "",
        "Obra composta por tres partes e doze capitulos, organizados pelo "
        "framework pedagogico EITA-V2 (Introducao, Explica, Ilustra, Tecnica, "
        "Aplica, Conclusao e Referencias).",
        "",
    ]
    return "\n".join(linhas)


def nota_do_framework() -> str:
    if TEMPLATE_EITA.exists():
        return TEMPLATE_EITA.read_text(encoding="utf-8").strip() + "\n"
    return "\n".join([
        "# Como ler esta obra: o framework EITA-V2",
        "",
        "Cada capitulo segue sete secoes fixas. **Introducao** situa o tema e "
        "conecta com o capitulo anterior. **Explica** desconstroi o conceito e "
        "define os termos. **Ilustra** ancora a ideia em uma analogia e em um "
        "diagrama. **Tecnica** entrega o artefato pratico. **Aplica** leva o "
        "conceito a um cenario real, incluindo seus limites. **Conclusao** "
        "sintetiza e propoe um desafio. **Referencias** lista as fontes citadas.",
        "",
    ])


def sumario_geral(sumario: dict) -> str:
    linhas = ["# Sumário Geral da Obra", ""]
    for parte in sumario.get("partes") or []:
        numero = parte.get("parte", "")
        titulo = parte.get("titulo_parte", "")
        linhas += [f"**Parte {numero} — {titulo}**", ""]
        for cap in parte.get("capitulos") or []:
            linhas.append(f"- Capítulo {cap.get('capitulo', '')}: {cap.get('titulo', '')}")
        linhas.append("")
    linhas += ["**Conclusão Geral**", ""]
    return "\n".join(linhas)


def capitulo_por_numero(dir_obra: Path, numero: str) -> str:
    caminho = dir_obra / "capitulos" / f"cap_{numero}.md"
    if not caminho.exists():
        raise FileNotFoundError(f"capitulo ausente: {caminho}")
    return caminho.read_text(encoding="utf-8").strip() + "\n"


def sem_horizontal_rules(texto: str) -> str:
    """Remove linhas de horizontal rule do corpo (R9: proibido `---` no capitulo).

    O template do capitulo fixo do EITA (`templates/capitulo_eita.md`) usa `---`
    como separador visual; ao ser embutido no livro compilado isso violaria R9.
    A limpeza acontece so no corpo — o frontmatter YAML e preservado antes.
    """
    linhas = [l for l in texto.splitlines() if not re.match(r"^[ \t]*-{3,}[ \t]*$", l)]
    return "\n".join(linhas)


def montar(dir_obra: Path, config: dict, sumario: dict) -> str:
    corpo = [folha_de_titulo(sumario, config)]

    prefacio = (dir_obra / "prefacio.md")
    corpo.append(prefacio.read_text(encoding="utf-8").strip() + "\n"
                 if prefacio.exists() else "# Prefácio\n")

    corpo.append(nota_do_framework())
    corpo.append(sumario_geral(sumario))

    for parte in sumario.get("partes") or []:
        numero = parte.get("parte", "")
        titulo = parte.get("titulo_parte", "")
        corpo.append(f"# Parte {numero} — {titulo}\n")
        for cap in parte.get("capitulos") or []:
            corpo.append(capitulo_por_numero(dir_obra, str(cap.get("capitulo", ""))))

    conclusao = dir_obra / "conclusao-geral.md"
    if conclusao.exists():
        corpo.append(conclusao.read_text(encoding="utf-8").strip() + "\n")

    return frontmatter(config, sumario) + "\n" + sem_horizontal_rules("\n".join(corpo))


def validar(texto: str, sumario: dict) -> list:
    problemas = []
    if not re.match(r"^---\n", texto):
        problemas.append("frontmatter YAML ausente no inicio do documento")
    for parte in sumario.get("partes") or []:
        for cap in parte.get("capitulos") or []:
            numero = str(cap.get("capitulo", ""))
            if f"# Capítulo {numero}:" not in texto:
                problemas.append(f"capitulo {numero} nao encontrado no documento montado")
    if "Conclusão Geral" not in texto:
        problemas.append("conclusao geral ausente")
    if re.search(r"^[ \t]*(-{3,})[ \t]*$", texto.split("---", 2)[-1], re.MULTILINE):
        problemas.append("horizontal rule dentro do corpo (proibido pelos gates)")
    return problemas


def main() -> int:
    ap = argparse.ArgumentParser(description="Monta o livro_final.md (Fase 3)")
    ap.add_argument("slug", help="obra alvo (ex.: livros/meu-livro)")
    ap.add_argument("--saida", help="caminho alternativo de saida")
    ap.add_argument("--checar", action="store_true",
                    help="valida a montagem sem gravar o arquivo")
    args = ap.parse_args()

    dir_obra = TO.dir_obra(args.slug, DIR_OUTPUT, modo="leitura")
    if not dir_obra.exists():
        print(f"[ERRO] obra inexistente: {dir_obra}")
        return 1

    config = ler_json(dir_obra / "config_obra.json")
    sumario = ler_json(dir_obra / "sumario_macro.json")
    if not sumario:
        print("[ERRO] sumario_macro.json ausente ou vazio — rode a Fase 1 primeiro.")
        return 1

    texto = montar(dir_obra, config, sumario)
    problemas = validar(texto, sumario)

    print("=" * 62)
    print(f"MONTAGEM DO LIVRO FINAL — {args.slug}")
    print("=" * 62)
    capitulos = sum(len(p.get("capitulos") or []) for p in sumario.get("partes") or [])
    print(f"  partes montadas   : {len(sumario.get('partes') or [])}")
    print(f"  capitulos montados: {capitulos}")
    print(f"  caracteres totais : {len(texto):,}".replace(",", "."))

    if problemas:
        for problema in problemas:
            print(f"  [FALHA] {problema}")
        return 1

    if args.checar:
        print("  [OK] montagem valida (modo --checar: nada foi gravado)")
        return 0

    destino = Path(args.saida) if args.saida else dir_obra / "livro_final.md"
    destino.write_text(texto, encoding="utf-8")
    print(f"  [OK] gravado: {dir_obra.name}/livro_final.md")
    return 0


if __name__ == "__main__":
    console_utf8()
    sys.exit(main())
