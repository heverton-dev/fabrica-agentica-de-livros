#!/usr/bin/env python3
"""
Gerador unico de capa (livro e e-book), padrao Editora Agentica.

Substitui scripts/gerar-capa-ebook-padrao.py (Playwright/HTML antigo, so
ebook), scripts/gerar-capa-ebooks.py (Pillow, dimensao 1:1,6 divergente),
scripts/testar_capa_marketing.py e scripts/gerar_capas_demais_ebooks.py
(CONFIGS_SERIE hardcoded — agora em output/series.json via series_capa.py).

Ver docs/superpowers/specs/2026-08-06-capas-padronizadas-design.md.

Uso (1 obra, resolvendo tudo a partir dos arquivos da propria obra):
    python scripts/gerar-capa.py livros/meu-livro
    python scripts/gerar-capa.py ebooks/meu-livro--eb-01-titulo

Uso (titulo/subtitulo/cor explicitos, sem depender de arquivos da obra):
    python scripts/gerar-capa.py livros/meu-livro --tipo livro \
        --titulo "MEU TITULO" --subtitulo "Meu subtitulo" --cor "#58a6ff"

Uso (migracao em lote — regenera todas as obras existentes):
    python scripts/gerar-capa.py --todos
"""
import argparse
import importlib
import json
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[ERRO] playwright nao instalado")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tipos_obra as TO  # noqa: E402
from series_capa import resolver_cor, resolver_serie_key  # noqa: E402

_validar_mod = importlib.import_module("validar-capa-texto")
validar_capa = _validar_mod.validar_capa

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

AUTOR_PADRAO = "Heverton Eduardo Peres"
QUALIFICACAO_PADRAO = "Especialista em Marketing e Desenvolvimento de Soluções"

# V5: dimensoes vem do registro declarativo (scripts/tipos_obra.py). Um tipo novo
# com capa propria nao exige tocar neste arquivo.
DIMENSOES = {t: TO.dimensoes_capa(t) for t in TO.tipos_validos()
             if TO.dimensoes_capa(t)}
TIPOS_COM_CAPA = tuple(sorted(DIMENSOES))
# Variante "social" (card 1080x1350) — hoje so o lead magnet declara
DIMENSOES_SOCIAL = {t: TO.dimensoes_capa(t, variante="social") for t in TO.tipos_validos()
                    if TO.dimensoes_capa(t, variante="social")}


CODIGO_DECORATIVO_PADRAO = """import omp
from pathlib import Path

async def deploy_pipeline(
    project: str,
    env: str = "production"
) -> DeployResult:
    agent = CodingAgent(model="gpt-4o")
    await agent.analyze(project)
    tests = await agent.run_tests()
    if tests.passed:
        return await agent.deploy(env)

const pipeline = new AIPipeline({
  model: "claude-opus",
  tools: ["bash", "editor", "browser"],
  maxIterations: 50
})

await pipeline.execute(`
  Construa um sistema completo
  de gestao de pedidos com
  testes unitarios e deploy
`)"""


def _ler_template():
    """Le o template HTML externo (capa-refinada.html)."""
    template_path = DIR_PROJETO / "templates" / "capa-refinada.html"
    if not template_path.exists():
        print(f"[ERRO] Template nao encontrado: {template_path}")
        sys.exit(1)
    return template_path.read_text(encoding="utf-8")


def _dividir_titulo(titulo):
    """Divide o titulo em 3 linhas para o template refinado.

    Linha 1: palavras ate a penultima (branco)
    Linha 2: ultima palavra (gradiente cor)
    Linha 3: vazio (sera preenchido pelo subtitulo ou badge)
    """
    palavras = titulo.strip().split()
    if len(palavras) <= 1:
        return titulo, "", ""
    if len(palavras) == 2:
        return palavras[0], palavras[1], ""
    # 3+ palavras: ante-penultima + penultima | ultima | vazio
    resto = " ".join(palavras[:-1])
    ultima = palavras[-1]
    return resto, ultima, ""


def _calcular_stats(dir_obra):
    """Calcula stats da obra a partir dos arquivos existentes."""
    sumario = _ler_json(dir_obra / "sumario_macro.json")
    config = _ler_json(dir_obra / "config_obra.json")

    # Contar capitulos
    capitulos = 0
    for parte in sumario.get("partes", []):
        capitulos += len(parte.get("capitulos", []))

    # Contar paginas (estimativa: 10k chars = 1 pagina)
    total_chars = 0
    capitulos_dir = dir_obra / "capitulos"
    if capitulos_dir.exists():
        for cap in capitulos_dir.glob("cap_*.md"):
            total_chars += len(cap.read_text(encoding="utf-8", errors="replace"))
    paginas = max(70, total_chars // 10000)

    return {
        "STAT1_NUMERO": str(capitulos) if capitulos else "16",
        "STAT1_LABEL": "CAPÍTULOS",
        "STAT2_NUMERO": f"{paginas}+",
        "STAT2_LABEL": "PÁGINAS",
        "STAT3_NUMERO": "∞",
        "STAT3_LABEL": "PROJETOS",
    }


def _ler_json(caminho):
    """Le um arquivo JSON de forma segura."""
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except (ValueError, json.JSONDecodeError):
            return {}
    return {}


def _gerar_html(titulo, subtitulo, cor_acento, autor, qualificacao, badge_texto,
                 ilustracao_relpath, largura, altura, categoria=None, stats=None,
                 edition_tag=None, codigo_decorativo=None):
    """Gera HTML usando o template refinado externo."""
    template = _ler_template()

    # Dividir titulo em 3 linhas
    linha1, linha2, linha3 = _dividir_titulo(titulo)

    # Stats padrao se nao fornecidos
    if stats is None:
        stats = {
            "STAT1_NUMERO": "16",
            "STAT1_LABEL": "CAPÍTULOS",
            "STAT2_NUMERO": "70+",
            "STAT2_LABEL": "PÁGINAS",
            "STAT3_NUMERO": "∞",
            "STAT3_LABEL": "PROJETOS",
        }

    # Ilustracao
    bloco_ilustracao = ""
    if ilustracao_relpath:
        bloco_ilustracao = f'<img src="{ilustracao_relpath}" alt="">'

    # Categoria padrao
    if categoria is None:
        categoria = "DESENVOLVIMENTO DE SOFTWARE"

    # Edition tag padrao
    if edition_tag is None:
        from datetime import datetime
        ano = datetime.now().year
        edition_tag = f"v1.0 · {ano}"

    # Codigo decorativo
    if codigo_decorativo is None:
        codigo_decorativo = CODIGO_DECORATIVO_PADRAO

    # Subtitulo com strong
    subtitulo_html = subtitulo if subtitulo else ""

    # Substituir variaveis
    html = template
    html = html.replace("{{LARGURA}}", str(largura))
    html = html.replace("{{ALTURA}}", str(altura))
    html = html.replace("{{COR}}", cor_acento)
    html = html.replace("{{TITULO_LINHA1}}", linha1)
    html = html.replace("{{TITULO_LINHA2}}", linha2)
    html = html.replace("{{TITULO_LINHA3}}", linha3)
    html = html.replace("{{SUBTITULO}}", subtitulo_html)
    html = html.replace("{{CATEGORIA}}", categoria)
    html = html.replace("{{BADGE_PRINCIPAL}}", badge_texto or "PARA INICIANTES")
    html = html.replace("{{BADGE_SECUNDARIO1}}", "16 capítulos")
    html = html.replace("{{BADGE_SECUNDARIO2}}", "projetos práticos")
    html = html.replace("{{STAT1_NUMERO}}", stats["STAT1_NUMERO"])
    html = html.replace("{{STAT1_LABEL}}", stats["STAT1_LABEL"])
    html = html.replace("{{STAT2_NUMERO}}", stats["STAT2_NUMERO"])
    html = html.replace("{{STAT2_LABEL}}", stats["STAT2_LABEL"])
    html = html.replace("{{STAT3_NUMERO}}", stats["STAT3_NUMERO"])
    html = html.replace("{{STAT3_LABEL}}", stats["STAT3_LABEL"])
    html = html.replace("{{AUTOR}}", autor)
    html = html.replace("{{QUALIFICACAO}}", qualificacao)
    html = html.replace("{{EDITION_TAG}}", edition_tag)
    html = html.replace("{{ILUSTRACAO}}", bloco_ilustracao)
    html = html.replace("{{CODIGO_DECORATIVO}}", codigo_decorativo)

    return html


def gerar_capa(titulo, subtitulo, dir_saida, tipo="livro", cor_acento="#58a6ff",
               autor=AUTOR_PADRAO, qualificacao=QUALIFICACAO_PADRAO,
               badge_texto=None, ilustracao_relpath=None, variante=None,
               nome_arquivo=None, categoria=None, stats=None, edition_tag=None):
    """Gera capa usando o template refinado (capa-refinada.html).

    Parametros adicionais (V5.3):
        categoria: label mono antes do titulo (ex: "DESENVOLVIMENTO DE SOFTWARE")
        stats: dict com STAT1_NUMERO, STAT1_LABEL, etc. (calculado automaticamente se None)
        edition_tag: tag de versao (ex: "v1.0 · 2026")
    """
    dir_saida = Path(dir_saida)
    dimensoes = (TO.dimensoes_capa(tipo, variante=variante)
                 or DIMENSOES.get(tipo) or DIMENSOES["livro"])
    largura, altura = dimensoes

    resultado = validar_capa(titulo, subtitulo, tipo)
    for campo in ("titulo", "subtitulo"):
        r = resultado[campo]
        if not r["ok"]:
            print(f"[AVISO] {campo} viola a regra de quebra de linha: {r['motivo']}")

    if ilustracao_relpath and not (dir_saida / ilustracao_relpath).exists():
        ilustracao_relpath = None

    # Calcular stats automaticamente se nao fornecidos
    if stats is None:
        stats = _calcular_stats(dir_saida)

    html = _gerar_html(titulo, subtitulo, cor_acento, autor, qualificacao,
                        badge_texto, ilustracao_relpath, largura, altura,
                        categoria=categoria, stats=stats, edition_tag=edition_tag)

    dir_saida.mkdir(parents=True, exist_ok=True)
    (dir_saida / "imagens").mkdir(exist_ok=True)
    sufixo_html = "_social" if variante == "social" else ""
    html_file = dir_saida / f"capa{sufixo_html}.html"
    html_file.write_text(html, encoding="utf-8")

    png_file = dir_saida / "imagens" / (
        nome_arquivo or ("card_social.png" if variante == "social" else "capa.png"))
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=_executavel_chromium())
        page = browser.new_page(viewport={"width": largura, "height": altura})
        page.goto(f"file:///{html_file.resolve().as_posix()}")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(png_file))
        browser.close()

    print(f"[OK] {png_file.relative_to(DIR_PROJETO)} ({png_file.stat().st_size // 1024} KB)")
    return png_file


def _executavel_chromium():
    """Caminho de um Chrome/Chromium do sistema, ou None (playwright baixa o seu).

    Fallback para maquinas onde o playwright nao tem browsers instalados
    (erro 'Executable doesn't exist at ... playwright install'): usar o Chrome
    do sistema evita baixar ~150MB e funciona em qualquer maquina com Chrome."""
    candidatos = [
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        str(Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/snap/bin/chromium",
    ]
    for caminho in candidatos:
        if Path(caminho).exists():
            return str(caminho)
    return None


def gerar_capa_da_obra(slug, tipo_forcado=None, variante=None):
    """Resolve titulo/subtitulo/cor/ilustracao a partir dos arquivos da propria obra.

    V5.3: usa template refinado (capa-refinada.html) com stats, categoria e edition_tag.
    Prioridade de metadados: para LIVROS, sumario tem prioridade sobre ebook_metadados.
    """
    dir_obra = TO.dir_obra(slug, DIR_OUTPUT)
    config_obra = _ler_json(dir_obra / "config_obra.json")
    sumario = _ler_json(dir_obra / "sumario_macro.json")
    meta_ebook = _ler_json(dir_obra / "ebook_metadados.json")

    # V5: o tipo sai do config; o prefixo do slug e o fallback (registro de tipos).
    tipo = (tipo_forcado or config_obra.get("tipo_obra")
            or TO.tipo_por_prefixo(slug) or "livro")
    if tipo not in DIMENSOES:
        print(f"[ERRO] tipo {tipo!r} nao declara capa propria no registro. "
              f"Tipos com capa: {', '.join(TIPOS_COM_CAPA)}")
        sys.exit(1)

    # V5.3: prioridade de metadados depende do tipo
    if tipo == "livro":
        # Para LIVROS: sumario tem prioridade (titulo da obra completa)
        titulo = (sumario.get("titulo_obra") or config_obra.get("titulo_obra")
                  or meta_ebook.get("titulo") or Path(slug).name).upper()
        subtitulo = (sumario.get("subtitulo") or config_obra.get("subtitulo")
                     or meta_ebook.get("subtitulo") or "")
    else:
        # Para EBOOKS/OUTROS: meta_ebook tem prioridade (titulo pode ser mais curto)
        titulo = (meta_ebook.get("titulo") or sumario.get("titulo_obra")
                  or config_obra.get("titulo_obra") or Path(slug).name).upper()
        subtitulo = (meta_ebook.get("subtitulo") or sumario.get("subtitulo")
                     or config_obra.get("subtitulo") or "")

    serie_key = resolver_serie_key(config_obra, slug)
    cor_acento = resolver_cor(serie_key, slug)

    ilustracao_relpath = "imagens/capa_ilustracao.png"

    nivel = (config_obra.get("senioridade_obra") or "").strip()
    # V5.3: fallback para senioridade do livro-mae (ebooks podem nao ter)
    if not nivel:
        livro_mae = TO.resolver_slug_mae(config_obra)
        if livro_mae:
            dir_mae = TO.dir_obra(livro_mae, DIR_OUTPUT)
            config_mae = _ler_json(dir_mae / "config_obra.json")
            nivel = (config_mae.get("senioridade_obra") or "iniciante").strip()
        else:
            nivel = "iniciante"
    if not nivel:
        print("[ERRO] config_obra.json sem 'senioridade_obra' — badge de nivel "
              "obrigatorio (REGRA 5/Capa, item h). Preencha (iniciante | "
              "intermediario | avancado) e rode de novo.")
        sys.exit(1)
    rotulos = {"iniciante": "PARA INICIANTES", "intermediario": "NÍVEL INTERMEDIÁRIO",
               "intermediário": "NÍVEL INTERMEDIÁRIO", "avancado": "NÍVEL AVANÇADO",
               "avançado": "NÍVEL AVANÇADO"}
    badge_texto = rotulos.get(nivel.lower(), f"NÍVEL: {nivel.upper()}")

    # V5.3: categoria derivada do motivo_condutor ou do tipo
    motivo = sumario.get("motivo_condutor", {})
    categoria = motivo.get("nome") or config_obra.get("tema", "").split(":")[0].strip()
    if not categoria:
        categoria = "DESENVOLVIMENTO DE SOFTWARE"

    # V5.3: edition_tag declarado na obra tem prioridade sobre o padrao "v1.0 · ano".
    # Sem isso, a capa contradizia o edition_tag do sumario_macro.json (edicoes
    # praticas/expandidas apareciam rotuladas como v1.0).
    edition_tag = (sumario.get("edition_tag") or config_obra.get("edition_tag")
                   or meta_ebook.get("edition_tag") or None)

    return gerar_capa(
        titulo=titulo,
        subtitulo=subtitulo,
        dir_saida=dir_obra,
        tipo=tipo,
        cor_acento=cor_acento,
        badge_texto=badge_texto,
        ilustracao_relpath=ilustracao_relpath,
        variante=variante,
        categoria=categoria,
        edition_tag=edition_tag,
    )


def main():
    ap = argparse.ArgumentParser(description="Gerador unico de capa (livro/ebook)")
    ap.add_argument("slug", nargs="?", help="ex.: livros/meu-livro ou ebooks/meu-livro--eb-01-titulo")
    ap.add_argument("--tipo", choices=list(TIPOS_COM_CAPA), default=None)
    ap.add_argument("--titulo")
    ap.add_argument("--subtitulo", default="")
    ap.add_argument("--cor")
    ap.add_argument("--badge")
    ap.add_argument("--social", action="store_true",
                     help="gera tambem o card social (imagens/card_social.png)")
    ap.add_argument("--todos", action="store_true",
                     help="regenera todas as obras dos tipos com capa (registro V5)")
    args = ap.parse_args()

    if args.todos:
        alvos = []
        for tipo in TIPOS_COM_CAPA:
            alvos += TO.listar_materiais(tipo, DIR_OUTPUT)
        falhas = []
        for slug in sorted(alvos):
            try:
                gerar_capa_da_obra(slug)
            except Exception as exc:  # noqa: BLE001 — nao travar o lote por 1 obra ruim
                print(f"[ERRO] {slug}: {exc}")
                falhas.append(slug)
        if falhas:
            print(f"\n[AVISO] {len(falhas)} obra(s) falharam: {falhas}")
        return 0

    if not args.slug:
        print("[ERRO] informe <slug> ou use --todos")
        return 1

    if args.titulo:
        config_obra = _ler_json(TO.dir_obra(args.slug, DIR_OUTPUT) / "config_obra.json")
        cor = args.cor or resolver_cor(resolver_serie_key(config_obra, args.slug), args.slug)
        gerar_capa(args.titulo, args.subtitulo, TO.dir_obra(args.slug, DIR_OUTPUT),
                   tipo=args.tipo or "livro", cor_acento=cor, badge_texto=args.badge)
    else:
        gerar_capa_da_obra(args.slug, tipo_forcado=args.tipo)

    if args.social:
        tipo_social = args.tipo or _ler_json(
            TO.dir_obra(args.slug, DIR_OUTPUT) / "config_obra.json").get("tipo_obra") \
            or TO.tipo_por_prefixo(args.slug)
        if TO.dimensoes_capa(tipo_social, variante="social"):
            gerar_capa_da_obra(args.slug, tipo_forcado=tipo_social, variante="social")
        else:
            print(f"[i] tipo {tipo_social!r} nao declara card social — nada a fazer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
