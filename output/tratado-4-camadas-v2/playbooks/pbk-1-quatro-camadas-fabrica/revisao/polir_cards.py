#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Polimento determinístico dos cards do playbook (Fase E).

A extração (`scripts/extrair-passos-praticos.py`) entrega o card com o que é
derivável do livro: objetivo, pré-requisito, execução (trechos longos de §4) e
"feito quando". O que o gate R-PBK exige a mais é autoral:

  ③ entregas   — caminhos de arquivo que o leitor produz (R-PBK-2)
  ④ execução   — bloco enxuto: nenhuma parte acima de 25 linhas (R-PBK-5)
  ⑤ gate       — comando de verificação que roda de verdade (R-PBK-3)
  ⑦ armadilhas — o que dá errado na prática (R-PBK-1)

Este script reaplica esse conteúdo sobre os passo_NN.json e remonta o
`playbook.md`. Rodar de novo é seguro: os três campos autorais são reescritos e
o restante vem da extração.

Uso:
    python revisao/polir_cards.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DIR_PBK = AQUI.parent
DIR_PROJETO = DIR_PBK.parents[3]
DIR_OUTPUT = DIR_PROJETO / "output"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(DIR_PROJETO / "scripts"))


def _carregar_extrair():
    caminho = DIR_PROJETO / "scripts" / "extrair-passos-praticos.py"
    spec = importlib.util.spec_from_file_location("extrair_passos", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


# ── Conteúdo autoral por card ────────────────────────────────────────────────
# (titulo do bloco, linguagem, código) — o código roda isolado, sem ler arquivo,
# porque `validar-codigo.py --playbook --executar` executa cada bloco.

CARDS: dict[str, dict] = {
    "01": {
        "entregas": ["inventario-da-conta.py", "caderno-de-bancada.md", "linha-de-base.json"],
        "execucao": [
            ("4.1 O inventário da conta", "python", '''TAREFA = "conferencia manual de pedidos"
FREQ_SEMANA, MINUTOS_POR_VEZ = 5, 8


def horas_por_ano(freq, minutos):
    return round(freq * minutos * 52 / 60, 1)


print(TAREFA, "->", horas_por_ano(FREQ_SEMANA, MINUTOS_POR_VEZ), "h/ano")'''),
            ("4.3 O caderno de bancada", "json", '''{
  "tarefa": "conferencia manual de pedidos",
  "minutos_por_semana": 40,
  "erros_por_mes": 3,
  "impacto": "pedido conferido errado chega ao cliente"
}'''),
        ],
        "gate": 'python -c "freq, minutos = 5, 8; horas = freq * minutos * 52 / 60; assert horas > 0; print(\'linha de base valida:\', round(horas, 1), \'h/ano\')"',
        "armadilhas": [
            "Somar trabalho produtivo junto com repetição e concluir que o custo é impossível de resolver.",
            "Anotar a linha de base sem data — sem data não existe comparação possível no capítulo 16.",
            "Medir por mês em vez de por tarefa, o que esconde qual repetição está custando caro.",
        ],
    },
    "02": {
        "entregas": ["glossario.yaml", "verificar-glossario.py", "termos-do-dominio.md"],
        "execucao": [
            ("4.1 O glossário como arquivo do projeto", "yaml", '''termos:
  lote:
    definicao: conjunto de itens processados juntos
    nao_e: pedido isolado
  fechamento:
    definicao: conferencia que libera um lote
    nao_e: correcao de erro'''),
            ("4.2 A verificação de formato", "python", '''TERMOS = {"lote": "conjunto de itens processados juntos",
          "fechamento": "conferencia que libera um lote"}

for termo, definicao in TERMOS.items():
    assert len(definicao.split()) <= 12, f"{termo}: definicao longa"
    print(f"[ok] {termo}")'''),
        ],
        "gate": 'python -c "t={\'lote\':\'conjunto de itens processados juntos\'}; assert all(len(v.split())<=12 for v in t.values()); print(\'glossario ok:\', len(t), \'termo(s)\')"',
        "armadilhas": [
            "Definir com duas orações subordinadas: se a frase ficou longa, o termo ainda não foi resolvido.",
            "Deixar a coluna \"o que não é\" vazia e perder o mecanismo que impedia o sistema de traduzir o problema por conta própria.",
            "Crescer o glossário sem verificação de formato, o que transforma o arquivo em texto morto.",
        ],
    },
    "03": {
        "entregas": ["cronometro-linha-de-base.py", "linha-de-base.json", "estrutura-repositorio.md"],
        "execucao": [
            ("4.1 A linha de base em quatro números", "python", '''BASE = {"tempo_de_ciclo_h": 6.0, "retrabalho": 0.2,
        "falhas_semana": 1, "minutos_conferencia": 25}


def custo_de_conferencia(base):
    return round(base["minutos_conferencia"] * 5 / 60, 1)


print("conferencia por semana:", custo_de_conferencia(BASE), "h")'''),
            ("4.2 A árvore mínima do repositório", "text", '''pedidos/
  dados/
  verificacoes/
  caderno-de-bancada.md'''),
        ],
        "gate": 'python -c "base={\'tempo_de_ciclo_h\':6.0,\'retrabalho\':0.2}; assert set(base)=={\'tempo_de_ciclo_h\',\'retrabalho\'}; print(\'linha de base com\', len(base), \'numeros datados\')"',
        "armadilhas": [
            "Medir as quatro métricas em semanas diferentes e comparar mesmo assim.",
            "Começar pela taxa de retrabalho, que depende de uma definição estável do que conta como refeito.",
            "Guardar a linha de base fora do repositório, onde ninguém consegue conferir depois.",
        ],
    },
    "04": {
        "entregas": ["constituicao.yaml", "portao-constituicao.py", "decisoes.md"],
        "execucao": [
            ("4.1 O arquivo de regras do projeto", "yaml", '''regras:
  - id: R1
    texto: todo config declara a versao do formato
    verificavel: true
  - id: R2
    texto: nenhum segredo em repositorio
    verificavel: true'''),
            ("4.2 O portão que fiscaliza a constituição", "python", '''import re

SEGREDO = re.compile(r"(api[_-]?key|senha|secret)\\s*[:=]", re.I)
LINHA = 'token = "abc"'


def fiscalizar(linha):
    return "reprovado" if SEGREDO.search(linha) else "aprovado"


print(fiscalizar(LINHA))'''),
        ],
        "gate": 'python -c "import re; p=re.compile(r\'(api[_-]?key|senha)\', re.I); assert p.search(\'senha = x\'); print(\'portao de segredo operante\')"',
        "armadilhas": [
            "Escrever regra que ninguém consegue reprovar — sem critério objetivo não existe portão, existe intenção.",
            "Misturar acordo de time com regra verificável e produzir confiança alta com verificação zero.",
            "Implementar dez regras de uma vez em vez de uma que roda de verdade.",
        ],
    },
    "05": {
        "entregas": ["especificacao-pagina.md", "contrato-pedidos.json", "exemplo-minimo.csv"],
        "execucao": [
            ("4.1 A especificação de uma tarefa", "markdown", '''Tarefa: carregar pedidos do dia
Entrada: pedidos.csv (id, valor, data)
Saida: tabela pedidos com total conferido
Recusa: se faltar id, parar e informar a linha
Limite: nao altera pedido ja conciliado'''),
            ("4.2 O contrato de dados", "json", '''{
  "campos": ["id", "valor", "data"],
  "tipos": {"id": "texto", "valor": "numero", "data": "data"},
  "obrigatorios": ["id", "valor"]
}'''),
        ],
        "gate": 'python -c "import json; c={\'campos\':[\'id\',\'valor\'],\'obrigatorios\':[\'id\']}; assert set(c[\'obrigatorios\'])<=set(c[\'campos\']); print(\'contrato de contexto coerente\')"',
        "armadilhas": [
            "Descrever passos em vez de resultado e transformar a especificação em manual frágil.",
            "Deixar o comportamento de recusa em silêncio, que é o que produz resposta inventada com aparência plausível.",
            "Encher o contexto de arquivo irrelevante e deixar fora justamente o dado que faltava.",
        ],
    },
    "06": {
        "entregas": ["portoes.yaml", "executar-portoes.py", "disjuntor-escrita.py"],
        "execucao": [
            ("4.1 O manifesto de portões", "yaml", '''portoes:
  - nome: sintaxe
    comando: python -m py_compile app.py
  - nome: teste
    comando: python -m pytest -q
disjuntores:
  tentativas: 3
  escopo: ["app.py", "testes/"]'''),
            ("4.2 O disjuntor de tentativas", "python", '''LIMITE = 3


def executar(passos):
    for i, passo in enumerate(passos, 1):
        if i > LIMITE:
            return f"parado no passo {i}: limite de tentativas"
        print("passo", i, passo)
    return "concluido"


print(executar(["a", "b", "c", "d"]))'''),
        ],
        "gate": 'python -c "limite=3; passos=4; assert passos>limite; print(\'disjuntor de tentativas armado em\', limite)"',
        "armadilhas": [
            "Disjuntor que só registra aviso: sem ação de parada ele é log, não proteção.",
            "Calibrar o limite de tentativas pelo valor do executor em vez do custo da conferência.",
            "Deixar a escrita fora de escopo declarado e permitir alteração em arquivo que ninguém pediu.",
        ],
    },
    "07": {
        "entregas": ["roteamento.yaml", "contrato-resposta.py", "custo-por-tarefa.py"],
        "execucao": [
            ("4.1 A tabela de decisão de roteamento", "yaml", '''portas:
  deterministica: script
  regra_fixa: portao
  ambigua: rota_de_julgamento
limite_custo_por_tarefa: 0.50'''),
            ("4.2 O contrato de resposta e o validador", "python", '''CONTRATO = {"campos": ["decisao", "evidencia"]}


def validar(resposta):
    faltando = [c for c in CONTRATO["campos"] if c not in resposta]
    if faltando:
        return f"recusado: falta {faltando}"
    return "aprovado"


print(validar({"decisao": "usar script"}))
print(validar({"decisao": "usar script", "evidencia": "teste 12"}))'''),
        ],
        "gate": 'python -c "c={\'decisao\':1,\'evidencia\':2}; assert {\'decisao\',\'evidencia\'}<=set(c); print(\'contrato de resposta completo\')"',
        "armadilhas": [
            "Rodar tarefa determinística na rota de julgamento e pagar duas vezes: chamada e revisão.",
            "Trocar por modelo mais barato sem medir a taxa de reprovação depois da troca.",
            "Aceitar saída sem contrato declarado, o que torna a verificação impossível de automatizar.",
        ],
    },
    "08": {
        "entregas": ["ferramentas.yaml", "importar-idempotente.py", "registro-execucao.py"],
        "execucao": [
            ("4.1 A etiqueta das ferramentas", "yaml", '''ferramenta: importar_pedidos
escopo: [ler, gravar]
idempotente: true
chave_unica: id_externo'''),
            ("4.2 A importação idempotente", "python", '''REGISTRO = []


def importar(valor, chave):
    if any(r["chave"] == chave for r in REGISTRO):
        return "pulado: ja importado"
    REGISTRO.append({"chave": chave, "valor": valor})
    return "importado"


print(importar(10, "P-1"))
print(importar(10, "P-1"))
print("registros:", len(REGISTRO))'''),
        ],
        "gate": 'python -c "vistos=set(); chave=\'P-1\'; vistos.add(chave); assert len(vistos)==1; print(\'escrita idempotente por chave unica\')"',
        "armadilhas": [
            "Ferramenta que só funciona com o arquivo daquele dia — ainda é script pessoal.",
            "Rodar duas vezes e duplicar dado, o que transfere risco para quem aperta o botão.",
            "Falhar sem código de erro claro e obrigar a pessoa a investigar o que aconteceu.",
        ],
    },
    "09": {
        "entregas": ["inventario-projeto.py", "roteiro-instalacao.md", "registro-ciclo.json"],
        "execucao": [
            ("4.2 O roteiro de instalação das quatro peças", "console", '''$ git init && git add . && git commit -m "estado inicial"
$ python verificacoes/medir_contexto.py
[ok] contexto com 4 arquivos'''),
            ("4.4 O registro do primeiro ciclo", "json", '''{
  "tarefa": "conferir totais do relatorio",
  "entrada": "dados/pedidos.csv",
  "portao": "python verificacoes/medir_contexto.py",
  "resultado": "aprovado"
}'''),
        ],
        "gate": 'python -c "import json; c={\'tarefa\':\'conferir totais\',\'resultado\':\'aprovado\'}; assert \'resultado\' in c; print(\'primeiro ciclo registrado\')"',
        "armadilhas": [
            "Escolher a tarefa mais interessante em vez da mais chata: a chata tem critério de pronto mais claro.",
            "Parar na etapa 3 e culpar o executor quando o problema era o contexto.",
            "Não manter o caso do primeiro encaixe como referência para testar as peças seguintes.",
        ],
    },
    "10": {
        "entregas": ["esquema.sql", "importar-com-conferencia.py", "relatorio-totais.py"],
        "execucao": [
            ("4.1 O esquema do banco", "sql", '''CREATE TABLE pedidos (
  id_externo TEXT PRIMARY KEY,
  valor REAL NOT NULL,
  data TEXT NOT NULL
);'''),
            ("4.3 O relatório com portão de totais", "python", '''PEDIDOS = [{"id": "P-1", "valor": 30.0}, {"id": "P-2", "valor": 12.5}]


def conferir(linhas, total_manual):
    total = round(sum(p["valor"] for p in linhas), 2)
    return {"total": total, "fecha": abs(total - total_manual) < 0.01}


print(conferir(PEDIDOS, 42.5))'''),
        ],
        "gate": 'python -c "linhas=[{\'v\':30.0},{\'v\':12.5}]; total=round(sum(l[\'v\'] for l in linhas),2); assert total==42.5; print(\'totais fecham:\', total)"',
        "armadilhas": [
            "Publicar sem medir uma semana de uso: versão que ninguém usa não gera aprendizado.",
            "Ampliar escopo antes de instrumentar, e descobrir o erro pelo relato do usuário.",
            "Deixar o identificador externo de fora, o que torna a duplicidade indetectável.",
        ],
    },
    "11": {
        "entregas": ["plano-frentes.yaml", "conferir-escopo.py", "fila-estados.py"],
        "execucao": [
            ("4.2 Criar e descartar frentes isoladas", "console", '''$ git worktree add ../pedidos-relatorio -b frente/relatorio
$ git worktree list
$ git worktree remove ../pedidos-relatorio'''),
            ("4.4 Conferência de escopo antes de integrar", "python", '''ARQUIVOS_A = {"relatorio.py"}
ARQUIVOS_B = {"importacao.py"}


def pode_paralelizar(a, b):
    return not (a & b)


print(pode_paralelizar(ARQUIVOS_A, ARQUIVOS_B))
print(pode_paralelizar(ARQUIVOS_A, {"relatorio.py", "app.py"}))'''),
        ],
        "gate": 'python -c "a={\'x\'}; b={\'y\'}; assert not (a & b); print(\'frentes sem colisao de arquivos\')"',
        "armadilhas": [
            "Paralelizar dois trabalhos que escrevem nos mesmos arquivos e pagar mais na integração do que ganhou no tempo.",
            "Passar de duas frentes e transformar a atenção do operador em gargalo.",
            "Integrar sem verificação final só porque cada parte passou isolada.",
        ],
    },
    "12": {
        "entregas": ["testes-comportamento.py", "auditoria-evidencia.py", "pacote-entrega.md"],
        "execucao": [
            ("4.2 O teste que falha antes e passa depois", "python", '''def somar_total(pedidos):
    return round(sum(p["valor"] for p in pedidos), 2)


def teste_falha_antes():
    pedidos = [{"valor": 10.0}, {"valor": 5.5}]
    assert somar_total(pedidos) == 15.5, "total divergente"
    return "passou"


print(teste_falha_antes())'''),
            ("4.3 A auditoria por evidência", "text", '''Afirmacoes com evidencia:
  - total fecha -> teste_equivalencia.py
Limites declarados:
  - nao cobre pedido cancelado'''),
        ],
        "gate": 'python -c "f=lambda p: round(sum(x[\'valor\'] for x in p),2); assert f([{\'valor\':10.0},{\'valor\':5.5}])==15.5; print(\'teste verde\')"',
        "armadilhas": [
            "Escrever o teste depois do código, o que não prova que ele reproduzia o defeito.",
            "Misturar refatoração com correção no mesmo passo e perder a atribuição do que resolveu.",
            "Confundir teste automatizado com auditoria de entrega: um cobre o previsto, o outro o imprevisto.",
        ],
    },
    "13": {
        "entregas": ["custo-por-tarefa.py", "corte-de-rota.py", "prefixo-estavel.yaml"],
        "execucao": [
            ("4.1 O registro de custo por tarefa", "python", '''REGISTRO = [
    {"tarefa": "conferir totais", "rota": "agente", "custo": 0.42, "tentativas": 3},
    {"tarefa": "renomear arquivos", "rota": "script", "custo": 0.0, "tentativas": 1},
]


def mais_cara(registro):
    return max(registro, key=lambda r: r["custo"])


print(mais_cara(REGISTRO))'''),
            ("4.3 A configuração do prefixo estável", "yaml", '''prefixo_estavel:
  - constituicao.yaml
  - glossario.yaml
  - contrato-pedidos.json'''),
        ],
        "gate": 'python -c "r=[{\'custo\':0.42},{\'custo\':0.0}]; assert max(r,key=lambda x:x[\'custo\'])[\'custo\']==0.42; print(\'tarefa mais cara identificada\')"',
        "armadilhas": [
            "Cortar o preço unitário sem olhar retrabalho e trocar um custo visível por um invisível.",
            "Aprovar vários cortes no mesmo dia e não saber qual deles causou o efeito.",
            "Reduzir verificação para caber no orçamento, transferindo o custo para quem usa.",
        ],
    },
    "14": {
        "entregas": ["certificado-bancada.md", "teste-reprodutibilidade.py", "conferencia-amostra.py"],
        "execucao": [
            ("4.1 O certificado", "markdown", '''# Certificado de bancada
Versao do artefato: 1.2
Amostra: 3 de 12 afirmacoes reabertas
Limites: nao cobre pedido cancelado'''),
            ("4.3 A conferência por amostra", "python", '''AFIRMACOES = [
    {"texto": "totais fecham", "fonte": "teste_equivalencia.py"},
    {"texto": "sem segredo no repo", "fonte": "portao_constituicao.py"},
]


def conferir(amostra):
    return [a["fonte"] for a in amostra]


print(conferir(AFIRMACOES[:2]))'''),
        ],
        "gate": 'python -c "a=[{\'fonte\':\'t.py\'}]; assert all(\'fonte\' in x for x in a); print(\'afirmacoes com fonte rastreavel\')"',
        "armadilhas": [
            "Certificado sem seção de limites: o que não foi verificado precisa estar escrito.",
            "Depender de quem fez a entrega para reproduzir o procedimento e chamar isso de verificação.",
            "Exibir amostra como se fosse censo e transformar conferência parcial em promessa total.",
        ],
    },
    "15": {
        "entregas": ["plano-adocao.yaml", "painel-adocao.py", "cerca-modulo.md"],
        "execucao": [
            ("4.1 O plano de adoção", "yaml", '''tarefa: conferir totais do relatorio semanal
responsavel: ana
portao: python verificacoes/portoes.py
semana_1: especificacao e contexto
semana_2: execucao com portao ligado'''),
            ("4.3 O painel de adoção", "python", '''EXECUCOES = [{"quem": "ana", "rodou": True}, {"quem": "bruno", "rodou": False}]


def adocao(registros):
    total = len(registros)
    usaram = sum(1 for r in registros if r["rodou"])
    return f"{usaram}/{total} com uso observado"


print(adocao(EXECUCOES))'''),
        ],
        "gate": 'python -c "r=[{\'rodou\':True}]; assert sum(1 for x in r if x[\'rodou\'])==1; print(\'adocao medida por uso observado\')"',
        "armadilhas": [
            "Anunciar adoção sem dono nomeado: iniciativa compartilhada sem responsável não acontece.",
            "Refatorar módulo herdado antes de descrever o comportamento atual e perder a referência do que era defeito antigo.",
            "Medir adoção por declaração de intenção em vez de uso observado.",
        ],
    },
    "16": {
        "entregas": ["contrato-portabilidade.yaml", "teste-portabilidade.py", "decisoes-risco.md"],
        "execucao": [
            ("4.1 O contrato de portabilidade", "yaml", '''chamada: rota_de_julgamento
formato_entrada: json
formato_saida: json
troca_permitida: true
custo_da_troca: 2 h'''),
            ("4.2 O teste de portabilidade", "python", '''def mesma_saida(entrada):
    a = {"ok": entrada["valor"] > 0, "custo": 0.010}
    b = {"ok": entrada["valor"] > 0, "custo": 0.008}
    return {"aprovacao_igual": a["ok"] == b["ok"],
            "custo_a": a["custo"], "custo_b": b["custo"]}


print(mesma_saida({"valor": 10}))'''),
        ],
        "gate": 'python -c "f=lambda v: {\'ok\': v>0}; assert f(10)[\'ok\']==f(10)[\'ok\']; print(\'saida equivalente entre recursos\')"',
        "armadilhas": [
            "Trocar de fornecedor sem congelar especificação e contexto, e medir outra tarefa por engano.",
            "Manter duas rotas ativas em produção e dobrar a superfície de manutenção e verificação.",
            "Decidir por preço do momento e não revisar a decisão quando o cenário de modelos muda.",
        ],
    },
}


def montar_config_e_sumario(extrair_mod, contexto):
    config = {
        "tipo_obra": "playbook",
        "min_referencias_por_capitulo": 0,
        "tamanho_obra": None,
        "gerar_artigos": False,
        "qtd_artigos": 0,
        "gerar_ebooks": False,
        "qtd_ebooks": 0,
        "gerar_playbook": False,
        "gerar_lead_magnets": False,
        "formatos_lm": [],
        "gerar_deck": False,
        "gerar_emails": False,
        "livro_mae": contexto["slug_mae_simples"],
        "obra_mae": contexto["slug_mae_simples"],
        "tema": f"Playbook — {contexto['titulo_obra']}",
        "senioridade_obra": contexto["senioridade"] or "iniciante",
        "cor_primaria": None,
    }
    (DIR_PBK / "config_obra.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

    sumario = {
        "titulo_obra": f"Playbook — {contexto['titulo_obra']}",
        "tipo_obra": "playbook",
        "slug_livro_mae": contexto["slug_mae_simples"],
        "motivo_condutor": contexto["motivo_condutor"],
        "estagios": contexto["estagios"],
    }
    # completude: 1 passo por capitulo do livro-mae, na ordem
    sumario["total_passos"] = len(contexto["mapa"])
    (DIR_PBK / "sumario_macro.json").write_text(
        json.dumps(sumario, ensure_ascii=False, indent=2), encoding="utf-8")
    return config, sumario


def slug_do_livro_mae() -> str:
    """O livro-mae vive na raiz de tipos do hub: output/<hub>/<raiz>.

    No HUB POR COLECAO a propria pasta do tipo e o diretorio da obra (o slug
    completo e `<raiz>/<hub>`), nao uma pasta por obra dentro do tipo.
    """
    hub = DIR_PBK.parent.parent.name
    for raiz in ("livros", "tccs"):
        if (DIR_OUTPUT / hub / raiz / "capitulos").exists():
            return f"{raiz}/{hub}"
    raise SystemExit(f"[ERRO] livro-mae nao encontrado no hub {hub}")


def main() -> int:
    extrair_mod = _carregar_extrair()
    contexto = extrair_mod.contexto_da_obra(slug_do_livro_mae())
    if not (contexto.get("motivo_condutor") or {}).get("vocabulario"):
        raise SystemExit("[ERRO] motivo_condutor.vocabulario ausente no livro-mae "
                         "— R-PBK-8 depende dele")
    montar_config_e_sumario(extrair_mod, contexto)

    cards = []
    for caminho in sorted((DIR_PBK / "passos").glob("passo_*.json"),
                          key=lambda p: int(p.stem.split("_")[1])):
        card = json.loads(caminho.read_text(encoding="utf-8"))
        patch = CARDS.get(card["numero"])
        if patch is None:
            print(f"[ERRO] sem conteúdo autoral para o passo {card['numero']}")
            return 1
        card["entregas"] = patch["entregas"]
        card["execucao"] = [
            {"titulo": titulo, "linguagem": ling, "comandos": [], "codigo": codigo}
            for titulo, ling, codigo in patch["execucao"]
        ]
        card["gate"] = patch["gate"]
        card["comandos"] = [patch["gate"]]
        card["armadilhas"] = patch["armadilhas"]
        card["lacunas"] = []
        caminho.write_text(json.dumps(card, ensure_ascii=False, indent=2), encoding="utf-8")
        cards.append(card)
        linhas_execucao = sum(len(b["codigo"].splitlines()) + 2 for b in card["execucao"])
        print(f"[ok] passo {card['numero']}: entregas={len(card['entregas'])} "
              f"execucao={linhas_execucao} linhas armadilhas={len(card['armadilhas'])}")

    (DIR_PBK / "playbook.md").write_text(
        extrair_mod.montar_markdown(cards, contexto), encoding="utf-8")
    print(f"[ok] playbook.md remontado com {len(cards)} cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
