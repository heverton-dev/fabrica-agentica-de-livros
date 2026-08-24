#!/usr/bin/env python3
"""
V5.1 — Pacote de distribuicao da COLECAO INTEIRA.

Diferenca para `empacotar-distribuicao.py` (V4, que empacota um livro e seus
artigos/e-books): aqui o pacote e da COLECAO — livro, TCC, artigos, e-books,
playbook, lead magnets, deck e sequencia de e-mails — e a regra de entrada e uma
so:

    **so entra o que esta FINALIZADO e ABRE.**

Cada candidato passa por `validar-artefatos.py` antes de ser copiado. Material
sem artefato compilado, PDF truncado ou caminho perto do MAX_PATH fica de fora e
e listado no relatorio — nunca entra "meio pronto" no pacote do cliente.

Nomes dentro do pacote seguem a convencao curta (`lm-1-armadilhas.pdf`), de modo
que o caminho final continue abrindo depois de zipado ou copiado.

Saida:
    output/distribuicao/<colecao>/
    ├── LEIA-ME.md          inventario do que esta no pacote
    ├── LICENCA.txt         direitos autorais (todos os direitos reservados)
    ├── livro/  tcc/  artigos/  ebooks/
    └── playbook/  lead-magnets/  deck/  emails/

Uso:
    python scripts/empacotar-colecao.py "<nome-da-colecao>"
    python scripts/empacotar-colecao.py --todas
    python scripts/empacotar-colecao.py "<colecao>" --incluir-parciais
"""

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tipos_obra as TO  # noqa: E402
from nomes_curtos import (codigo_obra, codigos_unicos,  # noqa: E402
                          migrar_prefixo_underscore, nome_curto)

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"
DIR_PACOTES = DIR_OUTPUT / "distribuicao"

AUTOR = "Heverton Eduardo Peres"
ANO = date.today().year

# Ordem de apresentacao no pacote e no LEIA-ME (do principal ao acessorio)
ORDEM = ("livro", "tcc", "artigo", "ebook", "playbook", "lead-magnet", "deck", "emails")

LICENCA = f"""LICENCA — TODOS OS DIREITOS RESERVADOS
Copyright (c) {ANO} {AUTOR}

Todos os direitos reservados.

Nenhuma parte desta colecao — incluindo, sem limitacao, o texto integral, os
capitulos, os cards de playbook, os lead magnets, os slides, as sequencias de
e-mail, as ilustracoes, as capas graficas, os diagramas e os arquivos PDF, EPUB,
HTML e PPTX — pode ser reproduzida, armazenada em sistema de recuperacao,
adaptada ou transmitida, sob qualquer forma ou por qualquer meio (eletronico,
mecanico, fotocopia, gravacao ou outro), sem autorizacao previa e por escrito do
autor.

E permitida a distribuicao deste pacote em sua forma INTEGRAL e INALTERADA para
fins de avaliacao e uso pessoal. Sao expressamente vedados, sem contrato de
licenciamento firmado com o autor:

  - uso comercial de qualquer parte da colecao;
  - revenda, sublicenciamento ou redistribuicao parcial;
  - republicacao, integral ou parcial, em qualquer meio;
  - uso do conteudo como material didatico de curso pago;
  - uso do conteudo para treinar modelos de aprendizado de maquina.

As marcas, nomes e identidade visual da Editora Agentica pertencem ao autor.

Para licenciamento e permissoes, contate o autor.
"""


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def _importar(nome_arquivo, nome_modulo):
    """Importa um script da fabrica REUSANDO a instancia ja carregada.

    Recarregar criaria um segundo modulo com estado proprio (DIR_OUTPUT etc.),
    e as duas copias divergiriam silenciosamente."""
    import importlib.util
    if nome_modulo in sys.modules:
        return sys.modules[nome_modulo]
    spec = importlib.util.spec_from_file_location(
        nome_modulo, DIR_PROJETO / "scripts" / nome_arquivo)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome_modulo] = mod
    spec.loader.exec_module(mod)
    return mod


def _importar_validador():
    return _importar("validar-artefatos.py", "validar_artefatos")


def _importar_colecao():
    return _importar("colecao.py", "colecao")


def _slug_arquivo(nome):
    import re
    return re.sub(r"[^a-z0-9]+", "-", (nome or "").lower()).strip("-") or "colecao"


def avaliar_membro(membro, validador, incluir_parciais=False):
    """Decide se o membro entra no pacote e devolve os arquivos aprovados."""
    slug = membro["slug"]
    arquivos = validador.artefatos_do_slug(slug)
    verificados = [validador.verificar_arquivo(a) for a in arquivos]

    # O criterio de entrada e ABRIR. Caminho longo na ORIGEM nao exclui: o pacote
    # copia com nome curto, entao empacotar e justamente o que resolve o problema.
    aprovados = [(a, v) for a, v in zip(arquivos, verificados) if v["abre"]]

    if not arquivos:
        motivo = "sem artefato compilado"
    elif not aprovados:
        motivo = "; ".join(f"{v['arquivo']}: {v['detalhe']}"
                           for v in verificados if not v["abre"])
    else:
        motivo = ""
    return {"entra": bool(aprovados), "motivo": motivo,
            "arquivos": [a for a, _v in aprovados],
            "verificados": verificados}


def montar_leia_me(colecao, manifesto, incluidos, excluidos, tem_maquina=False):
    nucleo = manifesto.get("nucleo", {})
    L = [f"# {nucleo.get('titulo') or colecao}", "",
         f"**Autor:** {AUTOR}  ·  **Coleção:** {colecao}  ·  "
         f"**Licença:** Todos os direitos reservados", ""]
    motivo = nucleo.get("motivo_condutor") or {}
    if motivo.get("descricao"):
        L += [motivo["descricao"], ""]

    L += ["## O que está neste pacote", "", "| Pasta | Material | Arquivo |", "|---|---|---|"]
    for tipo, membro, arquivos in incluidos:
        pasta = TO.raiz_output(tipo)
        rotulo = TO.campo(tipo, "rotulo", tipo)
        titulo = membro["titulo"][:58]
        for a in arquivos:
            L.append(f"| `{pasta}/` | {rotulo}: {titulo} | `{a.name}` |")
    L.append("")

    L += ["## Como usar", "",
          "- **PDF** — abre em qualquer leitor; é o formato de impressão e leitura.",
          "- **EPUB** — reflowable, para Kindle, Kobo, Apple Books e Google Play Livros.",
          "- **HTML** (deck) — abra no navegador e tecle `F` para tela cheia. "
          "Funciona offline; as setas navegam entre os slides.",
          "- **Markdown** (e-mails) — cada arquivo é um e-mail da sequência de "
          "nutrição, na ordem de envio.", ""]

    if excluidos:
        L += ["## Não incluído nesta versão", "",
              "Os materiais abaixo ainda não estão finalizados e por isso ficaram "
              "de fora — o pacote só carrega o que está pronto e abre:", ""]
        for tipo, membro, motivo_ex in excluidos:
            L.append(f"- **{TO.campo(tipo, 'rotulo', tipo)}**: "
                     f"{membro['titulo'][:52]} — {motivo_ex}")
        L.append("")

    if tem_maquina:
        L += ["## Máquina de vendas", "",
              "- **`maquina/`** — projeto full-stack (Next.js + FastAPI + SQLite) "
              "da coleção, com snapshot das campanhas em `maquina/campanhas/`. "
              "Personalize por nicho (config/, copy do frontend, e-mails) e "
              "deploye — consulte o README dentro da pasta.", ""]

    L += ["## Licença", "",
          f"© {ANO} {AUTOR}. Todos os direitos reservados. "
          "Consulte `LICENCA.txt` para os termos completos.", ""]
    return "\n".join(L)


def pasta_do_pacote(colecao):
    """Nome curto e UNICO da pasta do pacote entre todas as colecoes do disco."""
    todas = [p.stem for p in DIR_OUTPUT.glob("colecoes/*.json")]
    mod = _importar_colecao()
    nomes = [m["colecao"] for m in (mod.carregar(s) or {"colecao": s} for s in todas)]
    if colecao not in nomes:
        nomes.append(colecao)
    return codigos_unicos(nomes)[colecao]


def empacotar(colecao, incluir_parciais=False):
    colecao_mod = _importar_colecao()

    manifesto = colecao_mod.carregar(colecao)
    if manifesto is None:
        manifestos = colecao_mod.sincronizar()
        manifesto = next((m for m in manifestos if m["colecao"] == colecao), None)
    if manifesto is None:
        print(f"[ERRO] colecao nao encontrada: {colecao}")
        return None

    # PONTO 5: Validar estrutura HUB POR COLECAO antes de empacotar
    # (rejeita fallback plano na origem)
    nucleo = manifesto.get("nucleo", {})
    slug_nucleo = nucleo.get("slug", "")
    if slug_nucleo:
        try:
            TO.dir_obra(slug_nucleo, DIR_OUTPUT, modo='escrita')
        except ValueError as e:
            print(f"[ERRO] Estrutura HUB inválida — NÃO EMPACOTANDO")
            print(f"  {str(e)[:200]}")
            return None

    migrar_prefixo_underscore(DIR_PACOTES)        # _distribuicao -> distribuicao
    validador = _importar_validador()
    # Por obra: o pacote nasce em <obra>/distribuicao/ (a serie analista ja tem
    # esse dir). Sem obra resolvida (layout plano), cai em output/distribuicao/.
    nucleo = manifesto.get("nucleo", {})
    obra_raiz = TO._obra_raiz(Path(nucleo.get("slug", "")).name, DIR_OUTPUT)
    pacotes_root = DIR_PACOTES
    if obra_raiz is not None:
        pacotes_root = obra_raiz / "distribuicao"
        migrar_prefixo_underscore(pacotes_root)
    # Nome curto tambem na RAIZ do pacote: nao adianta encurtar o arquivo se a
    # pasta que o contem devolve os 40 caracteres ao caminho.
    destino = pacotes_root / pasta_do_pacote(colecao)
    if destino.exists():
        shutil.rmtree(destino)          # idempotente
    destino.mkdir(parents=True, exist_ok=True)

    membros = sorted(manifesto["membros"],
                     key=lambda m: (ORDEM.index(m["tipo"]) if m["tipo"] in ORDEM else 99,
                                    m["slug"]))
    incluidos, excluidos, total_kb = [], [], 0
    # Sequencia por TIPO, nao por arquivo: tres artigos viravam "art-1" tres vezes,
    # e o EPUB e o PDF do mesmo e-book viravam "ebk-1" e "ebk-2" como se fossem
    # obras diferentes. A extensao ja distingue o formato.
    sequencia = {}

    for membro in membros:
        tipo = membro["tipo"]
        sequencia[tipo] = sequencia.get(tipo, 0) + 1
        avaliacao = avaliar_membro(membro, validador, incluir_parciais)
        if not avaliacao["entra"]:
            excluidos.append((tipo, membro, avaliacao["motivo"]))
            print(f"  [--] {tipo:<12} {membro['titulo'][:40]:<42} {avaliacao['motivo']}")
            continue

        pasta = destino / TO.raiz_output(tipo)
        pasta.mkdir(parents=True, exist_ok=True)
        base = (Path(membro["slug"]).name if TO.usa_nomes_curtos(tipo)
                else f"{TO.prefixo_curto(tipo)}-{sequencia[tipo]}-"
                     f"{nome_curto(membro['titulo'])}")
        copiados = []
        for origem in avaliacao["arquivos"]:
            destino_arq = pasta / f"{base}{origem.suffix}"
            shutil.copy2(origem, destino_arq)
            copiados.append(destino_arq)
            total_kb += origem.stat().st_size // 1024

        # E-mails: a sequencia inteira, nao so o consolidado. A subpasta leva o
        # mesmo nome-base do consolidado para nao competir com ele.
        if tipo == "emails":
            origem_dir = TO.dir_obra(membro["slug"], DIR_OUTPUT) / "emails"
            if origem_dir.exists():
                sub = pasta / base
                sub.mkdir(parents=True, exist_ok=True)
                for eml in sorted(origem_dir.glob("email_*.md")):
                    shutil.copy2(eml, sub / eml.name)
                    total_kb += eml.stat().st_size // 1024

        incluidos.append((tipo, membro, copiados))
        print(f"  [OK] {tipo:<12} {membro['titulo'][:40]:<42} "
              f"{len(copiados)} arquivo(s)")

    # Máquina de vendas (regra 1:1 — 1 por coleção, output/<hub>/maquina): o
    # pacote carrega a máquina inteira com o snapshot de campanhas. Artefatos
    # de runtime (node_modules, build, bancos) ficam fora.
    tem_maquina = False
    hub = colecao_mod._hub_da_colecao(manifesto["membros"])
    if hub:
        dir_maquina = DIR_OUTPUT / hub / "maquina"
        if dir_maquina.is_dir() and (dir_maquina / "manifesto.json").is_file():
            destino_maquina = destino / "maquina"
            if destino_maquina.exists():
                shutil.rmtree(destino_maquina)
            shutil.copytree(
                dir_maquina, destino_maquina,
                ignore=shutil.ignore_patterns("node_modules", ".next", "*.db"))
            total_kb += sum(p.stat().st_size for p in destino_maquina.rglob("*")
                            if p.is_file()) // 1024
            tem_maquina = True
            print(f"  [OK] maquina      ... copiada com snapshot de campanhas")

    (destino / "LICENCA.txt").write_text(LICENCA, encoding="utf-8")
    (destino / "LEIA-ME.md").write_text(
        montar_leia_me(colecao, manifesto, incluidos, excluidos,
                       tem_maquina=tem_maquina),
        encoding="utf-8")

    return {
        "colecao": colecao,
        "pacote": str(destino.relative_to(DIR_OUTPUT)),
        "incluidos": len(incluidos),
        "excluidos": [{"tipo": t, "titulo": m["titulo"], "motivo": mo}
                      for t, m, mo in excluidos],
        "arquivos": sum(len(a) for _t, _m, a in incluidos),
        "kb": total_kb,
    }


def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(description="Empacota a colecao para distribuicao (V5.1)")
    ap.add_argument("colecao", nargs="?")
    ap.add_argument("--todas", action="store_true")
    ap.add_argument("--incluir-parciais", action="store_true",
                    help="aceita artefatos com caminho arriscado (nao recomendado)")
    ap.add_argument("--estrito", action="store_true",
                    help="exit 1 se algum membro da colecao ficar de fora")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.todas:
        alvos = [m["colecao"] for m in _importar_colecao().sincronizar()]
    elif args.colecao:
        alvos = [args.colecao]
    else:
        print("[ERRO] informe <colecao> ou use --todas")
        return 1

    metas = []
    for alvo in alvos:
        print(f"\nCOLECAO: {alvo}")
        meta = empacotar(alvo, incluir_parciais=args.incluir_parciais)
        if meta:
            metas.append(meta)
            print(f"  -> {meta['pacote']} · {meta['arquivos']} arquivo(s) · {meta['kb']} KB")

    if args.json:
        print(json.dumps(metas, ensure_ascii=False, indent=2))

    pendentes = sum(len(m["excluidos"]) for m in metas)
    if args.estrito and pendentes:
        print(f"\n[ERRO] {pendentes} material(is) fora do pacote")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
