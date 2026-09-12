#!/usr/bin/env python3
"""
V5 / Fase B — Extrator DETERMINISTICO dos passos praticos do livro-mae (PLAYBOOK).

Le cada `output/<slug-mae>/capitulos/cap_NN.md`, particiona pelo framework EITA-V2
e transforma as secoes §4 *Tecnica* e §5 *Aplica* em um CARD estruturado por
capitulo. Nenhuma chamada de LLM: o playbook sai de `re.split` + agregacao.

Regra de ouro (R-PBK-0): teoria NAO entra. As secoes §1 Introducao, §2 Explica,
§3 Ilustra e §7 Referencias viram apenas referencia cruzada "-> Cap. N".

Saida:
    output/playbooks/<slug-mae>--pbk/passos/passo_NN.json   (1 card por capitulo)
    output/playbooks/<slug-mae>--pbk/playbook.md            (com --montar, padrao)
    output/playbooks/<slug-mae>--pbk/revisao/relatorio_extracao.json

Uso:
    python scripts/extrair-passos-praticos.py livros/<slug>
    python scripts/extrair-passos-praticos.py livros/<slug> --relatorio
    python scripts/extrair-passos-praticos.py livros/<slug> --sem-montar
    python scripts/extrair-passos-praticos.py livros/<slug> --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

import tipos_obra as TO
from secoes_eita import (blocos_de_codigo, caminhos_de_arquivo, comandos_executaveis,
                         dividir_secoes, itens_binarios, itens_de_lista, normalizar,
                         primeiro_paragrafo, secao_por_nome, subsecao, subtitulos,
                         titulo_do_capitulo)

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

MAX_ENTREGAS = 6
MAX_ARMADILHAS = 5
MAX_FEITO_QUANDO = 7
MIN_FEITO_QUANDO = 3
MAX_BLOCOS_EXECUCAO = 4

# Prioridade para eleger o comando de verificacao (parte ⑤ do card)
PRIORIDADE_GATE = ("validar", "auditar", "pytest", "test", "lint", "check", "verific")


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def _nome_hub(slug, dir_mae):
    """Nome simples da obra para derivar o slug do playbook.

    `slug` pode vir em duas ordens: legado `<tipo>/<nome>` (ex.: "livros/x",
    onde Path(slug).name == "x" já é o nome certo) ou hub V5 `<hub>/<tipo>`
    (ex.: "engenharia-agentica/livros", onde Path(slug).name == "livros" —
    o nome da pasta de TIPO, não da obra). Distingue os dois casos pelo pai
    do diretório resolvido: se ele é uma raiz de tipo conhecida (livros,
    tccs, ...), o nome da obra é o avô (o hub); senão, layout legado.
    """
    raizes_tipo = {TO.raiz_output(t) for t in TO.tipos_validos()}
    if dir_mae.name in raizes_tipo:
        return dir_mae.parent.name
    return Path(slug).name


def contexto_da_obra(slug):
    """Mapa capitulo -> {titulo, objetivo, estagio} + metadados herdados do livro-mae."""
    dir_mae = TO.dir_obra(slug, DIR_OUTPUT)
    nome_simples = _nome_hub(slug, dir_mae)
    sumario = _ler_json(dir_mae / "sumario_macro.json")
    config = _ler_json(dir_mae / "config_obra.json")
    motivo = sumario.get("motivo_condutor") or {}
    vocab = motivo.get("vocabulario") or []

    mapa, estagios = {}, []
    for i, parte in enumerate(sumario.get("partes", [])):
        # Nome do estagio: vocabulario do motivo condutor (R-PBK-8), com fallback
        # para o titulo da Parte quando a obra for V3 (sem motivo_condutor).
        termo = vocab[i] if i < len(vocab) else None
        nome_estagio = (termo or parte.get("titulo_parte") or f"Estágio {i + 1}").strip()
        caps = [str(c.get("capitulo")) for c in parte.get("capitulos", [])]
        estagios.append({
            "indice": i + 1,
            "nome": nome_estagio.capitalize() if termo else nome_estagio,
            "titulo_parte": parte.get("titulo_parte", ""),
            "capitulos": caps,
        })
        for c in parte.get("capitulos", []):
            mapa[str(c.get("capitulo")).zfill(2)] = {
                "titulo": c.get("titulo", ""),
                "objetivo": c.get("objetivo", ""),
                "estagio": estagios[-1]["nome"],
                "estagio_indice": i + 1,
            }

    return {
        "slug_mae": slug,
        "slug_mae_simples": nome_simples,
        "titulo_obra": sumario.get("titulo_obra", nome_simples),
        "introducao": sumario.get("introducao", ""),
        "motivo_condutor": motivo,
        "persona": motivo.get("persona_leitor", "Praticante"),
        "vocabulario": vocab,
        "senioridade": config.get("senioridade_obra", ""),
        "serie": config.get("serie"),
        "mapa": mapa,
        "estagios": estagios,
    }


def _gate(comandos):
    for prioritario in PRIORIDADE_GATE:
        for cmd in comandos:
            if prioritario in normalizar(cmd):
                return cmd
    return comandos[0] if comandos else ""


def _execucao(tecnica):
    """Blocos de execucao: subtitulo ### + comandos/codigo daquele trecho."""
    marcas = subtitulos(tecnica)
    blocos = []
    if marcas:
        partes = re.split(r"^#{3,4}[ \t]+.+?[ \t]*$", tecnica, flags=re.MULTILINE)[1:]
        for (_nivel, titulo), corpo in zip(marcas, partes):
            codigos = blocos_de_codigo(corpo)
            if not codigos:
                continue
            blocos.append({
                "titulo": titulo,
                "linguagem": codigos[0]["linguagem"],
                "comandos": comandos_executaveis(corpo, limite=6),
                "codigo": codigos[0]["codigo"][:1600],
            })
    if not blocos:
        for codigo in blocos_de_codigo(tecnica)[:MAX_BLOCOS_EXECUCAO]:
            blocos.append({
                "titulo": "Execução",
                "linguagem": codigo["linguagem"],
                "comandos": comandos_executaveis("```\n" + codigo["codigo"] + "\n```", limite=6),
                "codigo": codigo["codigo"][:1600],
            })
    return blocos[:MAX_BLOCOS_EXECUCAO]


def extrair_card(caminho, contexto, anterior=None):
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    # Numero canonico com 2 digitos, independente do nome do arquivo no disco
    # (a fabrica grava tanto cap_1.md quanto cap_01.md).
    numero = re.search(r"cap_(\d+)", caminho.stem).group(1).zfill(2)
    secoes = dividir_secoes(texto)

    tecnica = secao_por_nome(secoes, "tecnica")
    aplica = secao_por_nome(secoes, "aplica")
    meta = contexto["mapa"].get(numero, {})

    entregas = caminhos_de_arquivo(tecnica, limite=MAX_ENTREGAS)
    execucao = _execucao(tecnica)
    comandos = comandos_executaveis(tecnica, limite=12)

    exercicio = subsecao(aplica, "exercicio", "exercício", "pratique", "mao na massa")
    # `itens_binarios` quebra prosa imperativa quando o exercicio nao foi escrito
    # em lista — o EITA nao obriga a lista, e sem isso o card sairia vazio.
    feito = itens_binarios(exercicio, limite=MAX_FEITO_QUANDO)
    if len(feito) < MIN_FEITO_QUANDO:
        feito = itens_binarios(exercicio or aplica, limite=MAX_FEITO_QUANDO) or feito

    trecho_armadilhas = subsecao(aplica, "armadilha", "erro comum", "cuidado", "pitfall")
    armadilhas = itens_de_lista(trecho_armadilhas, limite=MAX_ARMADILHAS)

    objetivo = (meta.get("objetivo") or "").strip()
    if not objetivo:
        objetivo = primeiro_paragrafo(secao_por_nome(secoes, "introducao"), max_chars=280)

    lacunas = []
    if not tecnica:
        lacunas.append("sem_secao_tecnica")
    if not aplica:
        lacunas.append("sem_secao_aplica")
    if not entregas:
        lacunas.append("sem_entregas")
    if not execucao:
        lacunas.append("sem_execucao")
    if not comandos:
        lacunas.append("sem_gate")
    if len(feito) < MIN_FEITO_QUANDO:
        lacunas.append("feito_quando_insuficiente")
    if not armadilhas:
        lacunas.append("sem_armadilhas")
    if not objetivo:
        lacunas.append("sem_objetivo")

    return {
        "numero": numero,
        "capitulo_fonte": numero,
        "titulo": meta.get("titulo") or titulo_do_capitulo(texto, f"Passo {numero}"),
        "estagio": meta.get("estagio", ""),
        "estagio_indice": meta.get("estagio_indice", 0),
        "objetivo": objetivo,                                        # ①
        "pre_requisito": (f"Passo {anterior} concluído" if anterior else
                          "Nenhum — este é o ponto de partida"),     # ②
        "entregas": entregas,                                        # ③
        "execucao": execucao,                                        # ④
        "gate": _gate(comandos),                                     # ⑤
        "comandos": comandos,
        "feito_quando": feito,                                       # ⑥
        "armadilhas": armadilhas,                                    # ⑦
        "referencia_cruzada": f"Cap. {int(numero)} — {meta.get('titulo', '')}".strip(" —"),
        "lacunas": lacunas,
    }


# ── Montagem do playbook.md ───────────────────────────────────────────────────

def _bloco_card(card):
    L = [f"## Passo {int(card['numero'])} — {card['titulo']}", ""]
    if card["estagio"]:
        L.append(f"> **Estágio:** {card['estagio']}  ·  **Origem:** {card['referencia_cruzada']}")
        L.append("")
    L += ["### ① Objetivo do passo", "", card["objetivo"] or "_(a completar)_", "",
          "### ② Pré-requisito", "", card["pre_requisito"], "",
          "### ③ Entregas", ""]
    L += ([f"- `{e}`" for e in card["entregas"]] or ["- _(a completar)_"])
    L += ["", "### ④ Execução", ""]
    if card["execucao"]:
        for bloco in card["execucao"]:
            L.append(f"**{bloco['titulo']}**")
            L.append("")
            L.append(f"```{bloco['linguagem']}")
            L.append(bloco["codigo"])
            L.append("```")
            L.append("")
    else:
        L += ["_(a completar)_", ""]
    L += ["### ⑤ Verificação / Gate", ""]
    L += ([f"```bash\n{card['gate']}\n```"] if card["gate"] else ["_(a completar)_"])
    L += ["", "### ⑥ Feito quando…", ""]
    L += ([f"- [ ] {i}" for i in card["feito_quando"]] or ["- [ ] _(a completar)_"])
    L += ["", "### ⑦ Armadilhas", ""]
    L += ([f"- {a}" for a in card["armadilhas"]] or ["- _(a completar)_"])
    L.append("")
    return "\n".join(L)


def montar_markdown(cards, contexto, objetivo_material=""):
    titulo = f"Playbook — {contexto['titulo_obra']}"
    L = ["---", f'title: "{titulo}"',
         f'subtitle: "Guia de bancada · {len(cards)} passos práticos"',
         'author: "Heverton Eduardo Peres"', "lang: pt-BR", "---", "",
         "# Objetivo do Material", ""]
    L.append(objetivo_material or contexto["introducao"] or
             f"Executar, do início ao fim, os passos práticos de "
             f"{contexto['titulo_obra']} sem reler a teoria.")
    L += ["", "# Como usar este playbook", "",
          f"Você é o **{contexto['persona']}**. Cada passo é um card independente com "
          "sete partes: objetivo, pré-requisito, entregas, execução, gate de verificação, "
          "critério de conclusão e armadilhas.", "",
          "Este documento **não repete a teoria** do livro. Quando precisar do porquê, "
          "siga a referência cruzada do card para o capítulo correspondente.", ""]

    if contexto["estagios"]:
        L += ["# Mapa dos Estágios", "", "| # | Estágio | Passos |", "|---|---|---|"]
        for e in contexto["estagios"]:
            caps = ", ".join(str(int(c)) for c in e["capitulos"]) or "—"
            L.append(f"| {e['indice']} | {e['nome']} | {caps} |")
        L.append("")

    L += ["# Passos Práticos", ""]
    for card in cards:
        L.append(_bloco_card(card))

    L += ["# Checklist Mestre", ""]
    for card in cards:
        L.append(f"**Passo {int(card['numero'])} — {card['titulo']}**")
        L.append("")
        for item in (card["feito_quando"] or ["_(a completar)_"]):
            L.append(f"- [ ] {item}")
        L.append("")
    return "\n".join(L)


# ── Orquestracao ──────────────────────────────────────────────────────────────

def extrair(slug, montar=True):
    dir_mae = TO.dir_obra(slug, DIR_OUTPUT)
    dir_caps = dir_mae / "capitulos"
    if not dir_caps.exists():
        print(f"[ERRO] Capitulos nao encontrados: {dir_caps}")
        return None

    # Ordenacao NUMERICA (mesmo criterio de auditar-obra.py): os capitulos reais
    # sao gravados como cap_1.md..cap_20.md, e sorted() lexicografico colocaria
    # cap_10 antes de cap_2, quebrando a ordem dos passos (R-PBK-7).
    arquivos = sorted((c for c in dir_caps.glob("cap_*.md") if not c.stem.startswith("_")),
                      key=lambda p: int(re.search(r"cap_(\d+)", p.stem).group(1)))
    if not arquivos:
        print(f"[ERRO] Nenhum cap_*.md em {dir_caps}")
        return None

    contexto = contexto_da_obra(slug)
    slug_pbk = TO.slug_curto("playbook", contexto["slug_mae_simples"],
                             nome=contexto["titulo_obra"], base=DIR_OUTPUT)
    dir_pbk = TO.dir_obra(slug_pbk, DIR_OUTPUT)
    for sub in ("passos", "revisao", "imagens"):
        (dir_pbk / sub).mkdir(parents=True, exist_ok=True)

    cards, anterior = [], None
    for caminho in arquivos:
        card = extrair_card(caminho, contexto, anterior=anterior)
        (dir_pbk / "passos" / f"passo_{card['numero']}.json").write_text(
            json.dumps(card, ensure_ascii=False, indent=2), encoding="utf-8")
        cards.append(card)
        anterior = int(card["numero"])

    relatorio = {
        "slug_mae": slug,
        "slug_playbook": slug_pbk,
        "total_passos": len(cards),
        "passos_com_lacuna": [
            {"passo": c["numero"], "titulo": c["titulo"], "lacunas": c["lacunas"]}
            for c in cards if c["lacunas"]
        ],
        "lacunas_criticas": sorted({
            l for c in cards for l in c["lacunas"]
            if l in ("sem_secao_tecnica", "sem_secao_aplica", "sem_execucao")
        }),
        "cobertura": {
            "com_entregas": sum(1 for c in cards if c["entregas"]),
            "com_gate": sum(1 for c in cards if c["gate"]),
            "com_feito_quando": sum(1 for c in cards if len(c["feito_quando"]) >= MIN_FEITO_QUANDO),
            "com_armadilhas": sum(1 for c in cards if c["armadilhas"]),
        },
    }
    (dir_pbk / "revisao" / "relatorio_extracao.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")

    if montar:
        (dir_pbk / "playbook.md").write_text(
            montar_markdown(cards, contexto), encoding="utf-8")

    return {"cards": cards, "contexto": contexto, "relatorio": relatorio, "dir": dir_pbk}


def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(
        description="Extrai os passos praticos (§4 Tecnica + §5 Aplica) do livro-mae")
    ap.add_argument("slug", help="ex.: livros/meu-livro")
    ap.add_argument("--sem-montar", action="store_true",
                    help="so grava os passo_NN.json, nao monta playbook.md")
    ap.add_argument("--relatorio", action="store_true",
                    help="imprime as lacunas por passo (lista de trabalho do polimento)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    res = extrair(args.slug, montar=not args.sem_montar)
    if res is None:
        return 1

    rel, total = res["relatorio"], res["relatorio"]["total_passos"]
    if args.json:
        print(json.dumps(rel, ensure_ascii=False, indent=2))
        return 1 if rel["lacunas_criticas"] else 0

    try:
        onde = res["dir"].relative_to(DIR_PROJETO)
    except ValueError:      # output/ fora da arvore do projeto
        onde = res["dir"]
    print(f"[OK] {total} passo(s) extraido(s) em {onde}")
    c = rel["cobertura"]
    print(f"     entregas {c['com_entregas']}/{total} · gate {c['com_gate']}/{total} · "
          f"feito-quando {c['com_feito_quando']}/{total} · armadilhas {c['com_armadilhas']}/{total}")

    if args.relatorio or rel["lacunas_criticas"]:
        if rel["passos_com_lacuna"]:
            print("\nLacunas (lista de trabalho do polimento por LLM):")
            for p in rel["passos_com_lacuna"]:
                print(f"  passo {p['passo']} — {', '.join(p['lacunas'])}")
        else:
            print("\nNenhuma lacuna: extracao 100% deterministica.")

    if rel["lacunas_criticas"]:
        print(f"\n[AVISO] Lacunas criticas: {', '.join(rel['lacunas_criticas'])}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
