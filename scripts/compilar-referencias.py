#!/usr/bin/env python3
"""
No 7 - Auditor de Rastreabilidade (Fabrica Agentica de Livros).

Compila as "Fontes brutas" de todos os dossies de pesquisa de uma obra em uma
lista de referencias ABNT unica: deduplicada por URL normalizada e ordenada
alfabeticamente por autor/titulo. Ate aqui isso era instrucao em linguagem
natural para o `compilador-abnt` executar durante o merge (No 7) - e
normalizacao de string + set, zero julgamento editorial, entao vira script.

Uso:
    python scripts/compilar-referencias.py <slug>
    python scripts/compilar-referencias.py <slug> --json
    python scripts/compilar-referencias.py <slug> --saida caminho/saida.md

Le:   <dir_obra>/pesquisa/dossie*.md (secao "## Fontes brutas")
Grava (default): <dir_obra>/referencias_compiladas.md
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

RE_SECAO_FONTES = re.compile(r"##\s*Fontes brutas\b", re.IGNORECASE)
RE_PROXIMO_HEADING = re.compile(r"\n#{1,2}\s+\S")

RE_FONTE = re.compile(
    r"^-\s*(?P<autor>.+?)\.\s*\*(?P<titulo>.+?)\*\.\s*Dispon[ií]vel em:\s*"
    r"(?P<url>\S+?)\.?\s*Acesso em:\s*(?P<acesso>.+?)\.?\s*"
    r"(?:\((?P<classe>[ABC])\))?\s*$"
)


def normalizar_url(url):
    """Sem protocolo, sem barra final, minusculo - http/https e barra final
    nao duplicam a mesma fonte (mesma normalizacao usada em
    `.claude/mcp-servers/pdf-gen-server/compilar-livro.mjs`)."""
    url = (url or "").strip().rstrip("/")
    url = re.sub(r"^https?://", "", url, flags=re.IGNORECASE)
    return url.lower()


def parsear_linha(linha):
    """Extrai autor/titulo/url/acesso/classe de 1 linha de 'Fontes brutas'.

    Retorna None se a linha nao seguir o formato ABNT obrigatorio do
    pesquisador (nunca descarta silenciosamente - o chamador reporta as
    linhas nao parseadas para revisao humana/LLM)."""
    m = RE_FONTE.match(linha.strip())
    if not m:
        return None
    d = m.groupdict()
    return {
        "autor": d["autor"].strip(),
        "titulo": d["titulo"].strip(),
        "url": d["url"].strip().rstrip(".,;:"),
        "acesso": d["acesso"].strip(),
        "classe": d["classe"] or "",
    }


def extrair_secao_fontes(texto):
    """Isola o bloco 'Fontes brutas' de 1 dossie (da secao ate o proximo
    heading de nivel 1/2, ou EOF - a secao nasce sempre por ultimo no
    template, mas nao assume isso)."""
    m = RE_SECAO_FONTES.search(texto or "")
    if not m:
        return ""
    resto = texto[m.end():]
    prox = RE_PROXIMO_HEADING.search(resto)
    return resto[: prox.start()] if prox else resto


def coletar_fontes(dir_pesquisa):
    """Le todos os dossie*.md do diretorio; retorna (fontes, nao_parseadas)."""
    fontes, nao_parseadas = [], []
    if not dir_pesquisa.exists():
        return fontes, nao_parseadas
    for arq in sorted(dir_pesquisa.glob("dossie*.md")):
        texto = arq.read_text(encoding="utf-8", errors="replace")
        for linha in extrair_secao_fontes(texto).splitlines():
            linha = linha.strip()
            if not linha.startswith("-"):
                continue
            fonte = parsear_linha(linha)
            if fonte is None:
                nao_parseadas.append({"arquivo": arq.name, "linha": linha})
                continue
            fonte["arquivo_origem"] = arq.name
            fontes.append(fonte)
    return fontes, nao_parseadas


def deduplicar(fontes):
    """Dedup por URL normalizada, preservando a 1a ocorrencia. Se uma
    duplicata trouxer classe A/B/C e a fonte mantida ainda nao tiver
    classificacao, promove a classe (nunca perde classificacao por causa da
    ordem de leitura dos dossies)."""
    por_url = {}
    ordem = []
    for fonte in fontes:
        chave = normalizar_url(fonte["url"])
        if chave not in por_url:
            por_url[chave] = dict(fonte)
            ordem.append(chave)
        elif not por_url[chave]["classe"] and fonte["classe"]:
            por_url[chave]["classe"] = fonte["classe"]
    return [por_url[chave] for chave in ordem]


def ordenar_alfabetico(fontes):
    return sorted(fontes, key=lambda f: (f["autor"].upper(), f["titulo"].upper()))


def formatar_abnt(fonte):
    classe = f" ({fonte['classe']})" if fonte.get("classe") else ""
    return (
        f"- {fonte['autor']}. *{fonte['titulo']}*. Disponível em: "
        f"{fonte['url']}. Acesso em: {fonte['acesso']}.{classe}"
    )


def compilar(slug, base=None):
    """Retorna (fontes_unicas_ordenadas, nao_parseadas, total_bruto)."""
    dir_obra = TO.dir_obra(slug, base or DIR_OUTPUT)
    fontes, nao_parseadas = coletar_fontes(dir_obra / "pesquisa")
    unicas = ordenar_alfabetico(deduplicar(fontes))
    return unicas, nao_parseadas, len(fontes)


def main():
    console_utf8()
    ap = argparse.ArgumentParser(
        description="No 7 - compila as Fontes brutas dos dossies em 1 lista ABNT deduplicada"
    )
    ap.add_argument("slug")
    ap.add_argument("--json", action="store_true", help="Saida em JSON (nao grava .md)")
    ap.add_argument("--saida", help="Caminho do .md de saida (default: <dir_obra>/referencias_compiladas.md)")
    args = ap.parse_args()

    unicas, nao_parseadas, total_bruto = compilar(args.slug)
    duplicatas = total_bruto - len(unicas)

    if args.json:
        print(json.dumps({
            "total_bruto": total_bruto,
            "total_unico": len(unicas),
            "duplicatas_removidas": duplicatas,
            "nao_parseadas": nao_parseadas,
            "referencias": unicas,
        }, ensure_ascii=False, indent=2))
        return 0

    linhas_md = ["# Referências Bibliográficas", ""] + [formatar_abnt(f) for f in unicas]
    saida = Path(args.saida) if args.saida else TO.dir_obra(args.slug, DIR_OUTPUT, modo='escrita') / "referencias_compiladas.md"
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(linhas_md) + "\n", encoding="utf-8")

    print(
        f"[compilar-referencias] {total_bruto} fontes brutas -> {len(unicas)} unicas "
        f"({duplicatas} duplicatas removidas), {len(nao_parseadas)} nao parseadas"
    )
    for np in nao_parseadas[:10]:
        print(f"  [nao parseada] {np['arquivo']}: {np['linha'][:80]}")
    print(f"[compilar-referencias] gravado em {saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
