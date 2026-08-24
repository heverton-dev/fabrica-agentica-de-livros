#!/usr/bin/env python3
"""
V5.4 — Registro declarativo de FONTES ACADÊMICAS com API aberta (Fase 1).

Antes desta versão as bases acadêmicas viviam SÓ como instrução textual na
skill pesquisador (prosa). Agora cada fonte é UMA entrada de dicionário aqui,
com URL de API, função de busca e parser próprios — o minerador
(`minerar-fontes-academicas.py`) consulta todas via `urllib` (stdlib, custo
LLM ZERO) e entrega um dossiê acadêmico já em ABNT com classe (A).

Filosofia RICA e BARATA:
  RICA   = cobertura ampla: cada fonte com API aberta retorna metadados
           estruturados (título, autores, DOI, resumo, ano, citações) — sem
           "adivinhar" base em busca web genérica.
  BARATA = custo LLM zero na mineração: é EXTRACÃO determinística (padrão dos
           produtores de custo zero: playbook/lead-magnet/deck). O LLM
           (pesquisador) só sintetiza o dossiê final a partir do JSON.

Fontes registradas (API aberta e gratuita, sem chave):
  - openalex          agregador ~250M obras (cobre Crossref/PubMed/Scopus/WoS)
  - crossref          registro de DOIs
  - arxiv             preprints (física/CS/matemática; Atom XML)
  - semantic_scholar  grafo de citações (rate limit sem chave)
  - scielo            produção científica PT-BR/América Latina
  - pubmed            medicina/ciências da vida (E-utilities; condicional ao tema)

Fontes SEM API pública (Google Scholar, ACM DL, IEEE Xplore, Springer Link)
seguem sendo buscadas MANUALMENTE pela skill pesquisador (WebSearch) e entram
no dossiê junto com o resultado do minerador.

Campos do descritor:
  nome             rotulo PT-BR
  classificacao    contrato com validar-fontes.py (A/B/C)
  max_padrao       limite default de resultados
  fetch            funcao que obtem as respostas brutas (levanta FonteIndisponivel)
  parser           funcao que converte as respostas em registros normalizados
  cobre            o que a fonte agrega (para o relatorio)
  quando_usar      orientacao de uso (ex.: pubmed so em temas de saude)

Registro normalizado (saida de todo parser):
  fonte, fonte_nome, classe, titulo, autores[display], ano, doi, url,
  resumo, citacoes, periodico

Uso como biblioteca:
    import fontes_academicas as FA
    FA.fontes_validas()
    FA.descritor("openalex")
    FA.buscar("openalex", "agentes de IA", max_resultados=10)
    FA.deduplicar(registros)
    FA.formato_abnt(registro)

Uso como CLI:
    python scripts/fontes_academicas.py --listar
    python scripts/fontes_academicas.py openalex --json
"""

import argparse
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

TIMEOUT_SEGUNDOS = 25
USER_AGENT = ("Mozilla/5.0 (compatible; FabricaAgentica/1.0; "
              "mineracao-academica; mailto:fabrica.agentica@local)")

MESES_PT = {1: "jan.", 2: "fev.", 3: "mar.", 4: "abr.", 5: "mai.", 6: "jun.",
            7: "jul.", 8: "ago.", 9: "set.", 10: "out.", 11: "nov.", 12: "dez."}

_RE_LATEX = re.compile(r"\\[a-zA-Z']")

_STOPWORDS_ARXIV = {
    "a", "an", "and", "as", "at", "com", "da", "das", "de", "do", "dos", "e",
    "em", "for", "from", "in", "na", "no", "of", "on", "o", "os", "para",
    "por", "que", "the", "to", "um", "uma", "with",
}


class FonteIndisponivel(Exception):
    """Fonte de busca indisponivel (rede, HTTP 4xx/5xx, parse) — nao bloqueia."""


# ── Registro declarativo ────────────────────────────────────────────────────
# Adicionar fonte nova = UMA entrada aqui + fetch + parser. Ordem = prioridade
# (agregadores primeiro) e dedup de titulo/DOI mantem o primeiro.

FONTES_ACADEMICAS = {
    "openalex": {
        "nome": "OpenAlex",
        "classificacao": "A",
        "max_padrao": 10,
        "fetch": "_fetch_openalex",
        "parser": "_parse_openalex",
        "cobre": "Crossref, PubMed, Scopus, Web of Science, IEEE (agregado)",
        "quando_usar": "sempre (agregador mais amplo, ~250M obras)",
    },
    "crossref": {
        "nome": "Crossref",
        "classificacao": "A",
        "max_padrao": 10,
        "fetch": "_fetch_crossref",
        "parser": "_parse_crossref",
        "cobre": "registro central de DOIs (todas as editoras associadas)",
        "quando_usar": "sempre (complementa DOI/citações do OpenAlex)",
    },
    "arxiv": {
        "nome": "arXiv",
        "classificacao": "A",
        "max_padrao": 10,
        "fetch": "_fetch_arxiv",
        "parser": "_parse_arxiv",
        "cobre": "preprints recentes de fisica, computacao e matematica",
        "quando_usar": "sempre (estado da arte em CS/IA)",
    },
    "semantic_scholar": {
        "nome": "Semantic Scholar",
        "classificacao": "A",
        "max_padrao": 10,
        "fetch": "_fetch_semantic_scholar",
        "parser": "_parse_semantic_scholar",
        "cobre": "grafo de citacoes e sintese de impacto",
        "quando_usar": "sempre (rate limit sem chave — falhas viram sem-rede)",
    },
    "scielo": {
        "nome": "SciELO",
        "classificacao": "A",
        "max_padrao": 10,
        "fetch": "_fetch_scielo",
        "parser": "_parse_scielo",
        "cobre": "producao cientifica em portugues/América Latina",
        "quando_usar": "obrigatorio quando o tema tiver literatura relevante em PT-BR",
    },
    "pubmed": {
        "nome": "PubMed",
        "classificacao": "A",
        "max_padrao": 8,
        "fetch": "_fetch_pubmed",
        "parser": "_parse_pubmed",
        "cobre": "medicina e ciencias da vida (E-utilities)",
        "quando_usar": "quando o tema tocar saude, biologia ou ciencias da vida",
    },
}


def fontes_validas():
    return tuple(FONTES_ACADEMICAS.keys())


def descritor(fonte):
    """Descritor da fonte; KeyError explicito se desconhecida."""
    d = FONTES_ACADEMICAS.get(fonte)
    if d is None:
        raise KeyError(
            f"fonte academica desconhecida: {fonte!r}. "
            f"Validas: {', '.join(fontes_validas())}")
    return d


# ── Helpers de rede ─────────────────────────────────────────────────────────

def _http_get(url, timeout=TIMEOUT_SEGUNDOS):
    """Retorna bytes da URL com retry em erros transitórios; levanta FonteIndisponivel em qualquer falha permanente."""
    max_tentativas = 3
    for tentativa in range(max_tentativas):
        req = urllib.request.Request(
            url, headers={"User-Agent": USER_AGENT, "Accept": "application/json,*/*"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            # Retry em erros transitórios (429, 502, 503)
            if tentativa < max_tentativas - 1 and exc.code in (429, 502, 503):
                espera = 0.5 * (2 ** tentativa) + random.uniform(0, 0.3)
                print(f"[Retry {tentativa+1}/{max_tentativas}] {url[:60]} em {espera:.2f}s")
                time.sleep(espera)
                continue
            # Erro permanente ou última tentativa
            raise FonteIndisponivel(f"{url[:80]} -> HTTP {exc.code}") from exc
        except urllib.error.URLError as exc:
            razao = getattr(exc, "reason", exc)
            raise FonteIndisponivel(f"{url[:80]} -> rede/DNS ({razao})") from exc
        except Exception as exc:  # noqa: BLE001 — timeout/parse contam como indisponivel
            raise FonteIndisponivel(f"{url[:80]} -> {exc}") from exc


def _http_get_json(url):
    return json.loads(_http_get(url).decode("utf-8"))


def _http_get_atom(url):
    try:
        return ET.fromstring(_http_get(url).decode("utf-8"))
    except ET.ParseError as exc:
        raise FonteIndisponivel(f"{url[:80]} -> XML invalido ({exc})") from exc


def _quote(texto):
    return urllib.parse.quote_plus(texto)


def _limpar_latex(texto):
    """Remove escapes LaTeX (\', \", \a) comuns em metadados de editoras."""
    if not texto:
        return texto
    return _RE_LATEX.sub("", texto)


def _primeiro(valor):
    """Primeiro elemento de lista, ou o proprio valor; None se vazio."""
    if isinstance(valor, list):
        return valor[0] if valor else None
    return valor or None


def _lista(valor):
    if valor is None:
        return []
    if isinstance(valor, list):
        return [v for v in valor if v]
    return [valor] if valor else []


def _ano_de(valor):
    """Extrai int do ano de valores variados (2024, '2024-01-23', '2024 jan')."""
    if isinstance(valor, int):
        return valor
    texto = str(valor or "")
    m = re.search(r"\b(1[89]\d{2}|20\d{2})\b", texto)
    return int(m.group(1)) if m else None


# ── Fetchers (obtem as respostas brutas; uma por fonte) ────────────────────

def _fetch_openalex(query, n):
    url = (f"https://api.openalex.org/works?search={_quote(query)}"
           f"&per-page={n}&mailto=fabrica.agentica@local")
    return [_http_get_json(url)]


def _fetch_crossref(query, n):
    url = (f"https://api.crossref.org/works?query={_quote(query)}&rows={n}"
           "&select=title,author,DOI,issued,container-title,abstract,URL"
           "&mailto=fabrica.agentica@local")
    return [_http_get_json(url)]


def _fetch_arxiv(query, n):
    # arXiv une termos soltos com OR por padrao (stopwords dominam o resultado).
    # Juntar com AND deixa cada termo obrigatorio; stopwords comuns sao removidas
    # para nao zerar o resultado em temas longos (arXiv e majoritariamente ingles).
    termos = "+AND+".join(
        f"all:{_quote(t)}" for t in query.split()
        if t.lower() not in _STOPWORDS_ARXIV)
    if not termos:
        termos = f"all:{_quote(query)}"
    url = (f"http://export.arxiv.org/api/query?search_query={termos}"
           f"&start=0&max_results={n}")
    return [_http_get_atom(url)]


def _fetch_semantic_scholar(query, n):
    url = ("https://api.semanticscholar.org/graph/v1/paper/search?"
           f"query={_quote(query)}&limit={n}"
           "&fields=title,authors,year,abstract,externalIds,url,citationCount,venue")
    return [_http_get_json(url)]


def _fetch_scielo(query, n):
    url = (f"https://search.scielo.org/api.php?q={_quote(query)}"
           f"&output=json&lang=pt&count={n}")
    return [_http_get_json(url)]


def _fetch_pubmed(query, n):
    """E-utilities em duas chamadas: esearch (IDs) -> esummary (metadados)."""
    base = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
            f"esearch.fcgi?db=pubmed&term={_quote(query)}&retmode=json"
            f"&retmax={n}&tool=FabricaAgentica&email=fabrica.agentica@local")
    esearch = _http_get_json(base)
    ids = (esearch.get("esearchresult") or {}).get("idlist") or []
    if not ids:
        return [esearch, {}]
    esummary = _http_get_json(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
        f"db=pubmed&id={','.join(ids)}&retmode=json")
    return [esearch, esummary]


FUNCOES_FETCH = {
    "_fetch_openalex": _fetch_openalex,
    "_fetch_crossref": _fetch_crossref,
    "_fetch_arxiv": _fetch_arxiv,
    "_fetch_semantic_scholar": _fetch_semantic_scholar,
    "_fetch_scielo": _fetch_scielo,
    "_fetch_pubmed": _fetch_pubmed,
}


# ── Parsers (respostas brutas -> registros normalizados) ───────────────────

def _registro(titulo, autores, ano=None, doi=None, url=None,
              resumo=None, citacoes=None, periodico=None):
    """Monta registro normalizado (remove ruido de LaTeX e vazios)."""
    titulo = _limpar_latex((titulo or "").strip())
    if not titulo:
        return None
    return {
        "titulo": titulo,
        "autores": [_limpar_latex(a).strip() for a in autores if _limpar_latex(a).strip()],
        "ano": _ano_de(ano),
        "doi": doi,
        "url": url,
        "resumo": resumo,
        "citacoes": citacoes,
        "periodico": periodico,
    }


def _abstract_openalex(inverted):
    """Reconstroi o resumo a partir do inverted index do OpenAlex."""
    if not inverted:
        return None
    tamanho = max(inverted.values(), default=[0])[0]
    palavras = [""] * (tamanho + 1)
    for palavra, posicoes in inverted.items():
        for pos in posicoes:
            if pos < len(palavras):
                palavras[pos] = palavra
    texto = " ".join(p for p in palavras if p)
    return texto.strip() or None


def _parse_openalex(dados):
    resultados = (dados[0] or {}).get("results") or []
    registros = []
    for w in resultados:
        autores = [(a.get("author") or {}).get("display_name")
                   for a in w.get("authorships") or []]
        doi = (w.get("doi") or "").replace("https://doi.org/", "").strip() or None
        fonte_url = (w.get("primary_location") or {}).get("landing_page_url")
        periodico = ((w.get("primary_location") or {}).get("source") or {})\
            .get("display_name")
        r = _registro(
            titulo=w.get("title"),
            autores=autores,
            ano=w.get("publication_year"),
            doi=doi,
            url=fonte_url or (f"https://doi.org/{doi}" if doi else None),
            resumo=_abstract_openalex(w.get("abstract_inverted_index")),
            citacoes=w.get("cited_by_count"),
            periodico=periodico,
        )
        if r:
            registros.append(r)
    return registros


def _parse_crossref(dados):
    itens = ((dados[0] or {}).get("message") or {}).get("items") or []
    registros = []
    for item in itens:
        autores = []
        for a in item.get("author") or []:
            familia = a.get("family")
            if familia:
                dado = re.sub(r",?\s*author\s*$", "", a.get("given", "").strip(),
                              flags=re.IGNORECASE)
                autores.append(f"{familia}, {dado}".strip(", "))
        doi = item.get("DOI")
        r = _registro(
            titulo=_primeiro(item.get("title")),
            autores=autores,
            ano=_ano_de((item.get("issued") or {}).get("date-parts")),
            doi=doi,
            url=item.get("URL") or (f"https://doi.org/{doi}" if doi else None),
            resumo=item.get("abstract"),
            citacoes=item.get("is-referenced-by-count"),
            periodico=_primeiro(item.get("container-title")),
        )
        if r:
            registros.append(r)
    return registros


def _parse_arxiv(dados):
    root = dados[0]
    atom = "{http://www.w3.org/2005/Atom}"
    arxiv_ns = "{http://arxiv.org/schemas/atom}"
    registros = []
    for entry in root.findall(f"{atom}entry"):
        titulo = (entry.findtext(f"{atom}title") or "").strip()
        autores = [a.findtext(f"{atom}name") for a in entry.findall(f"{atom}author")]
        publicado = entry.findtext(f"{atom}published") or ""
        doi_el = entry.find(f"{arxiv_ns}doi")
        doi = doi_el.text.strip() if doi_el is not None and doi_el.text else None
        r = _registro(
            titulo=titulo,
            autores=autores,
            ano=_ano_de(publicado),
            doi=doi,
            url=(entry.findtext(f"{atom}id") or "").strip(),
            resumo=(entry.findtext(f"{atom}summary") or "").strip(),
            periodico="arXiv",
        )
        if r:
            registros.append(r)
    return registros


def _parse_semantic_scholar(dados):
    papers = (dados[0] or {}).get("data") or []
    registros = []
    for p in papers:
        autores = [a.get("name") for a in p.get("authors") or [] if a.get("name")]
        doi = (p.get("externalIds") or {}).get("DOI")
        r = _registro(
            titulo=p.get("title"),
            autores=autores,
            ano=p.get("year"),
            doi=doi,
            url=p.get("url") or (f"https://doi.org/{doi}" if doi else None),
            resumo=p.get("abstract"),
            citacoes=p.get("citationCount"),
            periodico=p.get("venue"),
        )
        if r:
            registros.append(r)
    return registros


def _parse_scielo(dados):
    """Parser tolerante: o shape da resposta varia entre versoes da API."""
    obj = dados[0] or {}
    registros = []
    records = obj.get("records")
    if isinstance(records, dict):
        records = records.get("records") or []
    if not isinstance(records, list):
        records = []
    for r in records:
        autores = _lista(r.get("author")) or _lista(r.get("authors"))
        r_rec = _registro(
            titulo=_primeiro(r.get("title")) or _primeiro(r.get("titles")),
            autores=autores,
            ano=r.get("year") or r.get("publication_year"),
            doi=r.get("doi"),
            url=r.get("url") or r.get("uri"),
            periodico=(_primeiro(r.get("journal_title"))
                       or _primeiro(r.get("journal"))),
        )
        if r_rec:
            registros.append(r_rec)
    return registros


def _parse_pubmed(dados):
    esearch = dados[0] or {}
    esummary = dados[1] if len(dados) > 1 else {}
    ids = (esearch.get("esearchresult") or {}).get("idlist") or []
    resultado = esummary.get("result") or {}
    registros = []
    for pid in ids:
        info = resultado.get(pid) or {}
        autores = [a.get("name") for a in info.get("authors") or [] if a.get("name")]
        doi = None
        for aid in info.get("articleids") or []:
            if aid.get("idtype") == "doi":
                doi = aid.get("value")
                break
        r = _registro(
            titulo=info.get("title"),
            autores=autores,
            ano=_ano_de(info.get("pubdate") or info.get("pubyear")),
            doi=doi,
            url=f"https://pubmed.ncbi.nlm.nih.gov/{pid}/",
            periodico=info.get("fulljournalname"),
        )
        if r:
            registros.append(r)
    return registros


PARSERS = {
    "_parse_openalex": _parse_openalex,
    "_parse_crossref": _parse_crossref,
    "_parse_arxiv": _parse_arxiv,
    "_parse_semantic_scholar": _parse_semantic_scholar,
    "_parse_scielo": _parse_scielo,
    "_parse_pubmed": _parse_pubmed,
}


# ── API ─────────────────────────────────────────────────────────────────────

def buscar(fonte, query, max_resultados=None):
    """Consulta UMA fonte e devolve registros normalizados (fonte/classe anexados).

    Levanta FonteIndisponivel quando a fonte falha (rede/HTTP/parse) — o
    minerador trata como status 'erro', sem abortar as demais fontes.
    """
    d = descritor(fonte)
    n = max_resultados or d["max_padrao"]
    payloads = FUNCOES_FETCH[d["fetch"]](query, n)
    registros = PARSERS[d["parser"]](payloads)
    for r in registros:
        r["fonte"] = fonte
        r["fonte_nome"] = d["nome"]
        r["classe"] = d["classificacao"]
        if not r.get("url") and r.get("doi"):
            r["url"] = f"https://doi.org/{r['doi']}"
    return registros


def deduplicar(registros):
    """Deduplica por DOI; sem DOI, por titulo normalizado. Preserva ordem."""
    vistos, unicos = set(), []
    for r in registros:
        doi = (r.get("doi") or "").strip().lower()
        if doi:
            chave = "doi:" + doi
        else:
            titulo = re.sub(r"[^a-z0-9]", "", (r.get("titulo") or "").lower())
            chave = "titulo:" + titulo
        if not chave or chave in vistos:
            continue
        vistos.add(chave)
        unicos.append(r)
    return unicos


def _nome_abnt(display):
    """'Silverio Martinez-Fernandez' -> 'MARTINEZ-FERNANDEZ, Silverio'."""
    nome = _limpar_latex((display or "").strip())
    if not nome:
        return ""
    if "," in nome:
        familia, dados = [p.strip() for p in nome.split(",", 1)]
        return f"{familia.upper()}, {dados}"
    partes = nome.split()
    if len(partes) == 1:
        return partes[0].upper()
    return f"{partes[-1].upper()}, {' '.join(partes[:-1])}"


def data_hoje_abnt():
    agora = time.localtime()
    return f"{agora.tm_mday} {MESES_PT[agora.tm_mon]} {agora.tm_year}"


def formato_abnt(registro, data_acesso=None):
    """Uma linha ABNT com classe: '- AUTOR. *Titulo*. [In: ...] [ano]. Disponível em: URL. Acesso em: ... (A)'."""
    autores = registro.get("autores") or []
    if len(autores) > 3:
        autor = _nome_abnt(autores[0]) + " et al."
    elif len(autores) >= 2:
        autor = "; ".join(_nome_abnt(a) for a in autores)
    elif autores:
        autor = _nome_abnt(autores[0])
    else:
        autor = "AUTOR"
    linha = f"- {autor.rstrip('.')}. *{registro['titulo']}*."
    if registro.get("periodico"):
        linha += f" In: {registro['periodico']}."
    if registro.get("ano"):
        linha += f" {registro['ano']}."
    if registro.get("url"):
        data = data_acesso or data_hoje_abnt()
        linha += f" Disponível em: {registro['url']}."
        linha += f" Acesso em: {data}."
    linha += f" ({registro.get('classe', 'A')})"
    return linha


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Registro declarativo de fontes academicas com API aberta (V5.4)")
    ap.add_argument("fonte", nargs="?", help="fonte a inspecionar (ex.: openalex)")
    ap.add_argument("--listar", action="store_true", help="lista todas as fontes")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.listar or not args.fonte:
        if args.json:
            print(json.dumps(FONTES_ACADEMICAS, ensure_ascii=False, indent=2))
            return 0
        print(f"{'FONTE':<20} {'NOME':<18} {'CLASSE':<7} MAX  COBRE")
        print("-" * 100)
        for chave, d in FONTES_ACADEMICAS.items():
            print(f"{chave:<20} {d['nome']:<18} {d['classificacao']:<7} "
                  f"{d['max_padrao']:<4} {d['cobre']}")
        return 0

    try:
        d = descritor(args.fonte)
    except KeyError as exc:
        print(f"[ERRO] {exc}")
        return 1
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    for k, v in d.items():
        print(f"{k:<16}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
