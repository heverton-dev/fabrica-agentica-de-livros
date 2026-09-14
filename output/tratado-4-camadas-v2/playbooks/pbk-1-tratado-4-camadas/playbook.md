---
title: "Playbook — O Tratado das 4 Camadas da Fábrica Agêntica"
subtitle: "Guia de bancada · 12 passos práticos"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Objetivo do Material

Apresentar a crise do desenvolvimento amador com IA, a transição para o Engenheiro Agêntico e a promessa da arquitetura de 4 Camadas da Edição Expandida e Definitiva.

# Como usar este playbook

Você é o **Engenheiro de Sistemas Autônomos**. Cada passo é um card independente com sete partes: objetivo, pré-requisito, entregas, execução, gate de verificação, critério de conclusão e armadilhas.

Este documento **não repete a teoria** do livro. Quando precisar do porquê, siga a referência cruzada do card para o capítulo correspondente.

# Mapa dos Estágios

| # | Estágio | Passos |
|---|---|---|
| 1 | Sala de controle | 1, 2, 3, 4 |
| 2 | Painel operacional | 5, 6, 7, 8, 9 |
| 3 | Circuito de segurança | 10, 11, 12 |

# Passos Práticos

## Passo 1 — O Contexto Real de Origem: Do Projeto Arsenal ao Ecossistema AIDD

> **Estágio:** Sala de controle  ·  **Origem:** Cap. 1 — O Contexto Real de Origem: Do Projeto Arsenal ao Ecossistema AIDD

### ① Objetivo do passo

Situar historicamente a passagem do programador manual ao Engenheiro Agêntico, apresentar o Projeto Arsenal Open Source como campo de batalha real e o Ecossistema AIDD como plataforma resultante.

### ② Pré-requisito

Nenhum — este é o ponto de partida

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 Primeiro mandamento operacional: inventariar o ambiente**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventario do ambiente AIDD: verifica instrumentos antes de acionar agentes."""

import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

MIN_PYTHON = (3, 10)
ITENS_CANONICOS = ["AGENTS.md", "ecossistema.py", "gates"]


def checar_python() -> bool:
    ok = sys.version_info[:2] >= MIN_PYTHON
    marca = "OK" if ok else "FALHA"
    print(f"[{marca}] Python {sys.version.split()[0]} (minimo {MIN_PYTHON[0]}.{MIN_PYTHON[1]})")
    return ok


def checar_ferramenta(nome: str) -> bool:
    caminho = shutil.which(nome)
    if not caminho:
        print(f"[FALHA] ausente no PATH: {nome}")
        return False
    try:
        saida = subprocess.run([nome, "--version"], capture_output=True,
                               text=True, timeout=5)
        versao = (saida.stdout or nome).splitlines()[0].strip()[:40]
        print(f"[OK] {nome}: {versao}")
        return True
    except (OSError, subprocess.SubprocessError) as erro:
        print(f"[AVISO] {nome} presente em {caminho}, mas nao respondeu: {erro}")
        return True


def checar_banco_local() -> bool:
    try:
        conexao = sqlite3.connect(":memory:")
        modo = conexao.execute("PRAGMA journal_mode=WAL;").fetchone()[0]
        conexao.close()
        print(f"[OK] SQLite com journal {modo.upper()}")
        return True
    except sqlite3.Error as erro:
        print(f"[FALHA] motor SQLite indisponivel: {erro}")
        return False


def checar_governanca() -> bool:
    faltando = [item for item in ITENS_CANONICOS if not Path(item).exists()]
```

**4.2 A matriz de transposição vira arquivo**

```json
{
  "tema": "O Tratado das 4 Camadas da Fabrica Agentica",
  "tipo_obra": "livro",
  "tamanho_obra": "G",
  "senioridade_obra": "iniciante",
  "min_referencias_por_capitulo": 20,
  "estilo_tecnica": "operacional",
  "gerar_playbook": true,
  "gerar_lead_magnets": false,
  "gerar_deck": false,
  "gerar_emails": false,
  "gerar_campanha": false,
  "gerar_maquina": false,
  "modo_producao": "obra-unica"
}
```

**4.3 O contrato de interface da esteira**

```yaml
obra: livros/tratado-4-camadas-v2
fluxo:
  inventario: python scripts/parametros_obra.py livros/tratado-4-camadas-v2 --validar
  mineracao: python scripts/minerar-fontes-academicas.py "<tema>" --slug livros/tratado-4-camadas-v2
  indice: python scripts/indexar-dossie.py livros/tratado-4-camadas-v2 --indexar
  auditoria: python scripts/auditar-obra.py livros/tratado-4-camadas-v2 --estrito
  empacote: python scripts/empacotar-distribuicao.py livros/tratado-4-camadas-v2
```

**4.4 Uma sessão de operação real**

```console
$ python preflight_check.py
============================================================
INVENTARIO DE AMBIENTE — SALA DE CONTROLE AIDD
============================================================
[OK] Python 3.12.4 (minimo 3.10)
[OK] git: git version 2.45.2.windows.1
[FALHA] ausente no PATH: pandoc
[OK] typst: typst 0.11.1
[OK] SQLite com journal WAL
[OK] governanca canonica presente na raiz
------------------------------------------------------------
STATUS: REPROVADO — corrija os itens acima antes de acionar agentes.
$ winget install --id JohnMacFarlane.Pandoc --accept-package-agreements
$ python preflight_check.py
------------------------------------------------------------
STATUS: APROVADO — sala de controle pronta para operar.
```

### ⑤ Verificação / Gate

```bash
python preflight_check.py
```

### ⑥ Feito quando…

- [ ] Tratar a verificação de ambiente como burocracia opcional. Ela é o que separa um erro barato de descoberta (antes de gerar código) de um erro caro (depois de compilar)
- [ ] Deixar a configuração de intenção em branco "para decidir depois". Decisão não registrada é decisão tomada por padrão, e o padrão raramente é o que você queria
- [ ] Confundir volume de regras com qualidade de governança. A pesquisa sobre contexto é explícita: mais texto não significa mais aderência [12]
- [ ] Instalar os guardiões depois de já ter código em produção. Portão de qualidade retroativo é auditoria de dívida, não prevenção

### ⑦ Armadilhas

- Tratar a verificação de ambiente como burocracia opcional. Ela é o que separa um erro barato de descoberta (antes de gerar código) de um erro caro (depois de compilar)
- Deixar a configuração de intenção em branco "para decidir depois". Decisão não registrada é decisão tomada por padrão, e o padrão raramente é o que você queria
- Confundir volume de regras com qualidade de governança. A pesquisa sobre contexto é explícita: mais texto não significa mais aderência [12]
- Instalar os guardiões depois de já ter código em produção. Portão de qualidade retroativo é auditoria de dívida, não prevenção

## Passo 2 — O Dicionário do Iniciante: Glossário Descomplicado

> **Estágio:** Sala de controle  ·  **Origem:** Cap. 2 — O Dicionário do Iniciante: Glossário Descomplicado

### ① Objetivo do passo

Fixar o vocabulário mínimo para operar a fábrica: agentes, harnesses, contexto, MCP, gates, stubs, context engineering, worktrees e persistência.

### ② Pré-requisito

Passo 1 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 Dicionário como contrato executável**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Glossario executavel: vocabulario validado antes de virar documentacao."""

import json
import sys
from dataclasses import dataclass, asdict
from typing import Literal

PAINEIS = ("CONTEXTO", "HARNESS", "MOTOR", "FERRAMENTAS")


@dataclass(frozen=True)
class Termo:
    termo: str
    painel: str
    definicao: str
    impacto: str

    def valido(self) -> bool:
        return (len(self.termo) >= 2
                and self.painel in PAINEIS
                and len(self.definicao) >= 20
                and len(self.impacto) >= 20)


GLOSSARIO = [
    Termo("Agente", "MOTOR",
          "Modelo mais instrucoes, historico e capacidade de chamar ferramentas.",
          "Separa a culpa: erro de instrucao nao se corrige trocando modelo."),
    Termo("Harness", "HARNESS",
          "Aplicacao hospedeira que executa comandos e acessa disco em nome do agente.",
          "Todo risco operacional real nasce aqui, nao no modelo."),
    Termo("Janela de contexto", "CONTEXTO",
          "Limite de tokens mantidos na memoria de trabalho de uma requisicao.",
          "Contexto cheio degrada foco, eleva custo e aumenta latencia."),
    Termo("Portao de qualidade", "CONTEXTO",
          "Script deterministico com saida binaria: zero aprova, um bloqueia.",
          "Permite automatizar a decisao sem julgamento humano por entrega."),
    Termo("Stub", "FERRAMENTAS",
          "Casca de funcao que simula funcionamento com pass ou pendencia.",
          "Passa na revisao manual e falha silenciosamente em producao."),
    Termo("Servidor MCP", "F
```

**4.2 O esquema de saída que o pipeline consome**

```json
{
  "versao": "2026.1",
  "termos": [
    {
      "termo": "Harness",
      "painel": "HARNESS",
      "definicao": "Aplicacao hospedeira que executa comandos em nome do agente.",
      "impacto": "Todo risco operacional real nasce aqui, nao no modelo."
    }
  ]
}
```

**4.3 Sessão de consulta do dicionário**

```console
$ python glossario.py --termo harness
Termo    : Harness
Painel   : HARNESS
Definicao: Aplicacao hospedeira que executa comandos em nome do agente.
Impacto  : Todo risco operacional real nasce aqui, nao no modelo.

$ python glossario.py --painel CONTEXTO
[1] Janela de contexto  (degradacao de foco com contexto cheio)
[2] Portao de qualidade (saida binaria: zero aprova, um bloqueia)
[3] Context engineering (governanca do que entra na mesa de trabalho)
```

**4.5 Detector de vocabulário inflado**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detector de adjetivos nao verificaveis em documentacao tecnica."""

import re
import sys
from pathlib import Path
from typing import Dict, List

ADJETIVOS = ("robusto", "escalavel", "seguro", "otimizado", "performatico",
             "completo", "confiavel", "avancado")

# Metrica adjacente: numero com unidade proxima ao adjetivo
RE_METRICA = re.compile(
    r"\d+(?:[.,]\d+)?\s*(?:%|ms|s\b|min|GB|MB|tokens?|vezes|x\b|milhoes?)",
    re.IGNORECASE,
)


class Ocorrencia:
    def __init__(self, arquivo: Path, linha: int, termo: str, contexto: str):
        self.arquivo = arquivo
        self.linha = linha
        self.termo = termo
        self.contexto = contexto

    def verificavel(self) -> bool:
        return bool(RE_METRICA.search(self.contexto))

    def __str__(self) -> str:
        marca = "OK" if self.verificavel() else "HIPOTESE"
        return f"[{marca}] {self.arquivo}:{self.linha} termo {self.termo!r}"


def varrer(arquivo: Path) -> List[Ocorrencia]:
    achados: List[Ocorrencia] = []
    for numero, linha in enumerate(arquivo.read_text(encoding="utf-8").splitlines(), 1):
        baixo = linha.lower()
        for adjetivo in ADJETIVOS:
            if re.search(r"\b" + re.escape(adjetivo) + r"\b", baixo):
                achados.append(Ocorrencia(arquivo, numero, adjetivo, baixo))
    return achados


def resumir(ocorrencias: List[Ocorrencia]) -> Dict[str, int]:
    return {
        "total": len(ocorrencias),
        "verificaveis": sum(1 for o in ocorrencias if o.verificavel()),
        "hipoteses": sum(1 for o in
```

### ⑤ Verificação / Gate

```bash
python glossario.py --termo harness
```

### ⑥ Feito quando…

- [ ] Usar "modelo" e "agente" como sinônimos. Isso faz você procurar a culpa no lugar errado e gastar orçamento trocando o que não estava quebrado
- [ ] Tratar a janela de contexto como disco. Contexto guardado não é contexto disponível; a mesa de trabalho tem tamanho
- [ ] Chamar de "teste" o que é portão de qualidade. Um teste informa; um portão bloqueia. Sem bloqueio, o defeito continua no caminho
- [ ] Aceitar definição sem impacto declarado. Termo que não muda nenhuma decisão é ornamento
- [ ] Confiar em teste que nunca falhou. Verifique se o teste é capaz de falhar antes de considerar que ele protege algo [19]

### ⑦ Armadilhas

- Usar "modelo" e "agente" como sinônimos. Isso faz você procurar a culpa no lugar errado e gastar orçamento trocando o que não estava quebrado
- Tratar a janela de contexto como disco. Contexto guardado não é contexto disponível; a mesa de trabalho tem tamanho
- Chamar de "teste" o que é portão de qualidade. Um teste informa; um portão bloqueia. Sem bloqueio, o defeito continua no caminho
- Aceitar definição sem impacto declarado. Termo que não muda nenhuma decisão é ornamento
- Confiar em teste que nunca falhou. Verifique se o teste é capaz de falhar antes de considerar que ele protege algo [19]

## Passo 3 — A Crise do Desenvolvimento com IA: Os 4 Problemas Catastróficos

> **Estágio:** Sala de controle  ·  **Origem:** Cap. 3 — A Crise do Desenvolvimento com IA: Os 4 Problemas Catastróficos

### ① Objetivo do passo

Dissecar as quatro falhas estruturais que colapsam iniciativas amadoras de IA: amnésia de contexto, stubs/alucinação funcional, subagentes headless no vácuo e lock-in de harness.

### ② Pré-requisito

Passo 2 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 A valva 2 em detalhe: portão anti-stub por árvore sintática**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Portao anti-stub: inspecao estrutural do corpo das funcoes via AST."""

import ast
import sys
from pathlib import Path
from typing import List, Tuple

IGNORAR = {".venv", "venv", "__pycache__", ".git", "scratch", "node_modules"}


class DetectorDeStubs(ast.NodeVisitor):
    def __init__(self) -> None:
        self.falhas: List[Tuple[int, str, str]] = []

    def _corpo_util(self, node: ast.FunctionDef) -> list:
        corpo = list(node.body)
        if corpo and isinstance(corpo[0], ast.Expr) and isinstance(
                corpo[0].value, ast.Constant) and isinstance(corpo[0].value.value, str):
            corpo = corpo[1:]
        return corpo

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if any(isinstance(d, ast.Name) and d.id == "abstractmethod"
               for d in node.decorator_list):
            return
        corpo = self._corpo_util(node)
        if not corpo:
            self.falhas.append((node.lineno, node.name, "corpo vazio"))
        elif len(corpo) == 1:
            unico = corpo[0]
            if isinstance(unico, ast.Pass):
                self.falhas.append((node.lineno, node.name, "apenas 'pass'"))
            elif isinstance(unico, ast.Expr) and isinstance(unico.value, ast.Constant) \
                    and unico.value.value is Ellipsis:
                self.falhas.append((node.lineno, node.name, "apenas '...'"))
        self.generic_visit(node)


def verificar(caminho: Path) -> List[Tuple[int, str, str]]:
    try:
        arvore = ast.parse(caminho.read_text(encoding="utf
```

**4.2 A válvula 1 em detalhe: medindo o orçamento de contexto**

```json
{
  "orcamento_contexto": {
    "teto_por_turno": 8000,
    "teto_por_sessao": 80000,
    "prefixo_estavel": true,
    "cache_ttl": "5m",
    "politica_ao_exceder": "comprimir-saida-e-expurgar-historico"
  },
  "limites_de_agente": {
    "max_turnos_sem_checkpoint": 8,
    "max_repeticoes_de_erro": 2,
    "timeout_por_comando_s": 30
  }
}
```

**4.3 Sessão real: o laço de erro que drena orçamento**

```console
$ python agente.py --tarefa "corrigir migracao"
[14:02:11] tentativa 1/∞ -> FAIL (coluna 'cpf' nao existe)
[14:02:19] tentativa 2/∞ -> FAIL (coluna 'cpf' nao existe)
[14:02:27] tentativa 3/∞ -> FAIL (coluna 'cpf' nao existe)
[14:02:35] tentativa 4/∞ -> FAIL (coluna 'cpf' nao existe)
^C
$ python agente.py --tarefa "corrigir migracao" --max-repeticoes 2 --timeout 30
[14:05:02] tentativa 1/∞ -> FAIL (coluna 'cpf' nao existe)
[14:05:10] tentativa 2/∞ -> FAIL (coluna 'cpf' nao existe)
[14:05:10] TETO ATINGIDO -> execucao interrompida; diagnostico devolvido ao operador
```

**4.5 Verificando dependências fantasma antes do merge**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detector de dependencias fantasma: import declarado que nao existe no ambiente."""

import ast
import json
import sys
from importlib.util import find_spec
from pathlib import Path
from typing import Dict, List, Set

IGNORAR = {".venv", "venv", "__pycache__", ".git", "node_modules", "scratch"}

# Modulos da biblioteca padrao e locais nunca sao dependencias externas
INTERNOS = {"__future__", "os", "sys", "re", "json", "ast", "pathlib", "typing",
            "dataclasses", "subprocess", "shutil", "sqlite3", "hashlib", "zipfile",
            "importlib", "unicodedata", "collections", "itertools", "statistics"}


def modulos_importados(arquivo: Path) -> Set[str]:
    try:
        arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
    except SyntaxError:
        return set()
    nomes: Set[str] = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            nomes.update(alias.name.split(".")[0] for alias in no.names)
        elif isinstance(no, ast.ImportFrom) and no.module and no.level == 0:
            nomes.add(no.module.split(".")[0])
    return nomes


def resolve(nome: str) -> bool:
    if nome in INTERNOS:
        return True
    try:
        return find_spec(nome) is not None
    except (ImportError, ValueError, ModuleNotFoundError):
        return False


def varrer(raiz: Path) -> Dict[str, List[str]]:
    fantasma: Dict[str, List[str]] = {}
    for arquivo in raiz.rglob("*.py"):
        if IGNORAR.intersection(arquivo.parts):
            continue
        for nome in sorted(modulos_importad
```

### ⑤ Verificação / Gate

```bash
python agente.py --tarefa "corrigir migracao"
```

### ⑥ Feito quando…

- [ ] Tratar sintoma como causa. "O agente mudou de convenção" é sintoma; "o contexto saturou" é causa. Corrigir o sintoma gera retrabalho eterno
- [ ] Confiar em revisão manual como portão. Revisão humana é o filtro certo para intenção e o filtro errado para completude mecânica
- [ ] Rodar agentes paralelos sem isolamento físico. Sem diretório próprio, o paralelismo produz conflito, não velocidade
- [ ] Deixar execução autônoma sem teto de repetição e de turnos. O laço de erro é o modo de falha mais caro e mais fácil de prevenir
- [ ] Guardar a governança na ferramenta. Regra que só existe dentro de um aplicativo é regra que expira com o aplicativo

### ⑦ Armadilhas

- Tratar sintoma como causa. "O agente mudou de convenção" é sintoma; "o contexto saturou" é causa. Corrigir o sintoma gera retrabalho eterno
- Confiar em revisão manual como portão. Revisão humana é o filtro certo para intenção e o filtro errado para completude mecânica
- Rodar agentes paralelos sem isolamento físico. Sem diretório próprio, o paralelismo produz conflito, não velocidade
- Deixar execução autônoma sem teto de repetição e de turnos. O laço de erro é o modo de falha mais caro e mais fácil de prevenir
- Guardar a governança na ferramenta. Regra que só existe dentro de um aplicativo é regra que expira com o aplicativo

## Passo 4 — A Constituição Mestre: As 10 Leis Inegociáveis

> **Estágio:** Sala de controle  ·  **Origem:** Cap. 4 — A Constituição Mestre: As 10 Leis Inegociáveis

### ① Objetivo do passo

Apresentar e justificar as 10 Leis de Ouro da governança AIDD, mostrando como cada uma neutraliza um modo de falha concreto do desenvolvimento agêntico.

### ② Pré-requisito

Passo 3 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 A constituição como arquivo versionado**

```markdown
# Governança Canônica do Projeto

## Leis inegociáveis
1. Determinismo primeiro: resolve com script antes de chamar modelo.
2. Qualidade binária: exit 0 aprova; exit 1 bloqueia. Sem meio-termo.
3. Persistência estruturada: estado e decisões em arquivo auditável.
4. Economia severa: raciocínio telegráfico, saída densa, expurgo entre fases.
5. Supremacia agnóstica: nenhuma regra depende de harness ou fornecedor.
6. Desenvolvedor no controle: proibido agente headless invisível.
7. Zero stubs: proibido corpo vazio, retorno fictício ou pendência.
8. Anti-NIH: justificar por escrito antes de construir mecanismo genérico.
9. Honestidade de rótulo: não alegar mais do que o teste provou.
10. Comunicação direta: sem preâmbulo, sem saudação, sem repetição.
```

**4.2 Leis 2 e 9 em código: o fiscal da constituição**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fiscal da constituicao: leis 3 (persistencia) e 9 (honestidade de rotulo)."""

import re
import sys
from pathlib import Path
from typing import List, Tuple

# Lei 9 — vocabulario que afirma mais do que qualquer teste pode provar
TERMOS_INFLADOS = (
    r"\b100%\s+seguro\b",
    r"\btotalmente\s+blindado\b",
    r"\bsem\s+qualquer\s+bug\b",
    r"\babsolutamente\s+(?:perfeito|seguro)\b",
)

# Lei 3 — diretorios cuja ausencia indica estado nao auditavel
DIRETORIOS_PERSISTENTES = ("docs", "gates", "componentes")

EXEMPLO_INFLADO = "Este modulo e 100% seguro em qualquer cenario de carga."


def auditar_honestidade(docs: List[Path]) -> Tuple[bool, List[str]]:
    violacoes: List[str] = []
    padroes = [re.compile(p, re.IGNORECASE) for p in TERMOS_INFLADOS]
    for doc in docs:
        texto = doc.read_text(encoding="utf-8", errors="ignore")
        for padrao in padroes:
            achado = padrao.search(texto)
            if achado:
                violacoes.append(f"{doc}: afirmacao inflada -> {achado.group(0)!r}")
    return (not violacoes), violacoes


def auditar_persistencia(raiz: Path) -> Tuple[bool, List[str]]:
    faltando = [d for d in DIRETORIOS_PERSISTENTES if not (raiz / d).is_dir()]
    return (not faltando), [f"diretorio persistente ausente: {d}" for d in faltando]


def verificar_rotulo_isolado(texto: str) -> bool:
    """Lei 9 aplicada a um unico trecho — usado antes de publicar relatorio."""
    return not any(re.search(p, texto, re.IGNORECASE) for p in TERMOS_INFLADOS)


def main() -> int:
    raiz = Path("."
```

**4.3 Os dez fiscais declarados em configuração**

```yaml
constituicao:
  leis:
    - id: 1
      nome: Determinismo em primeiro lugar
      fiscal: revisao-humana-no-plano
    - id: 2
      nome: Qualidade binaria
      fiscal: gates/exit-code.sh
    - id: 3
      nome: Persistencia estruturada
      fiscal: gates/fiscal-constituicao.py
    - id: 4
      nome: Economia severa de tokens
      fiscal: gates/orcamento-contexto.py
    - id: 5
      nome: Supremacia agnostica
      fiscal: gates/checar-acoplamento.py
    - id: 6
      nome: Desenvolvedor no controle
      fiscal: gates/bloquear-headless.py
    - id: 7
      nome: Zero stubs
      fiscal: gates/anti-stub-ast.py
    - id: 8
      nome: Anti-NIH
      fiscal: revisao-humana-no-plano
    - id: 9
      nome: Honestidade de rotulo
      fiscal: gates/fiscal-constituicao.py
    - id: 10
      nome: Comunicacao direta
      fiscal: gates/ritmo-de-saida.py
```

**4.4 Sessão de fiscalização em operação**

```console
$ python gates/fiscal-constituicao.py
==============================================================
FISCAL DA CONSTITUICAO — LEIS 2, 3 E 9
==============================================================
[LEI 3] OK persistencia estruturada
[LEI 9] BLOQUEIO honestidade de rotulo (12 documento(s) auditado(s))
  -> docs/relatorio-carga.md: afirmacao inflada -> '100% seguro'
--------------------------------------------------------------
[REPROVADO] exit 1 — violacao constitucional detectada.

$ sed -i 's/100% seguro/resiliente a falha de nos, ver secao 4/' docs/relatorio-carga.md
$ python gates/fiscal-constituicao.py
--------------------------------------------------------------
[APROVADO] exit 0 — constituicao respeitada.
```

### ⑤ Verificação / Gate

```bash
python gates/fiscal-constituicao.py
```

### ⑥ Feito quando…

- [ ] Escrever leis sem fiscais. Lei sem fiscal é sugestão, e sugestão não sobrevive à pressão de prazo
- [ ] Confundir quantidade com cobertura. Vinte leis inúteis protegem menos do que sete leis fiscalizadas
- [ ] Desligar o fiscal para liberar a entrega. Isso inverte a relação: o fiscal existe justamente para o momento em que a pressão para ignorá-lo é maior
- [ ] Colocar fiscal caro no gancho rápido. O custo de espera produz evasão, e evasão produz portão desativado
- [ ] Tratar a constituição como imutável. Ela precisa evoluir, mas toda alteração é mudança de lei e merece justificativa registrada [3]

### ⑦ Armadilhas

- Escrever leis sem fiscais. Lei sem fiscal é sugestão, e sugestão não sobrevive à pressão de prazo
- Confundir quantidade com cobertura. Vinte leis inúteis protegem menos do que sete leis fiscalizadas
- Desligar o fiscal para liberar a entrega. Isso inverte a relação: o fiscal existe justamente para o momento em que a pressão para ignorá-lo é maior
- Colocar fiscal caro no gancho rápido. O custo de espera produz evasão, e evasão produz portão desativado
- Tratar a constituição como imutável. Ela precisa evoluir, mas toda alteração é mudança de lei e merece justificativa registrada [3]

## Passo 5 — Visão Geral das 4 Camadas: A Arquitetura Completa

> **Estágio:** Painel operacional  ·  **Origem:** Cap. 5 — Visão Geral das 4 Camadas: A Arquitetura Completa

### ① Objetivo do passo

Apresentar o mapa definitivo das quatro camadas soberanas, a separação estrita de responsabilidades e como cada camada isola um tipo de complexidade.

### ② Pré-requisito

Passo 4 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 Auditoria transversal das quatro camadas**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditoria transversal das 4 camadas: confirma artefatos minimos por camada."""

import shutil
import sqlite3
import sys
from pathlib import Path
from typing import List, Tuple


def camada_1_contexto(raiz: Path) -> Tuple[bool, List[str]]:
    esperado = [
        ("AGENTS.md", "constituicao viva na raiz"),
        ("componentes", "fonte unica de verdade"),
        ("docs", "memoria estruturada auditavel"),
    ]
    faltando = [f"{desc} ({caminho})" for caminho, desc in esperado
                if not (raiz / caminho).exists()]
    return (not faltando), faltando


def camada_2_harness(raiz: Path) -> Tuple[bool, List[str]]:
    faltando: List[str] = []
    if not (raiz / ".git").exists():
        faltando.append("repositorio git ausente (sem isolamento por worktree)")
    elif not shutil.which("git"):
        faltando.append("cli git ausente no PATH")
    gates = list((raiz / "gates").glob("*.py")) if (raiz / "gates").is_dir() else []
    if not gates:
        faltando.append("nenhum portao deterministico em gates/")
    return (not faltando), faltando


def camada_3_motor(raiz: Path) -> Tuple[bool, List[str]]:
    faltando: List[str] = []
    politicas = (raiz / "config" / "orcamento_contexto.json")
    if not politicas.exists():
        faltando.append("politica de orcamento de contexto ausente")
    return (not faltando), faltando


def camada_4_ferramentas(raiz: Path) -> Tuple[bool, List[str]]:
    faltando: List[str] = []
    try:
        conexao = sqlite3.connect(":memory:")
        modo = conexao.execute("PRAGMA journ
```

**4.2 O contrato entre camadas**

```yaml
camadas:
  1_contexto:
    entrada: pedido_em_linguagem_natural
    saida: pedido_enquadrado_nas_regras
    artefatos: [AGENTS.md, componentes/specs, docs/protocolos]
    lei_principal: 3
  2_harness:
    entrada: pedido_enquadrado_nas_regras
    saida: acao_autorizada_ou_bloqueada
    artefatos: [gates/, .git/hooks, settings.json]
    lei_principal: 2
  3_motor:
    entrada: acao_autorizada
    saida: decisao_em_formato_tipado
    artefatos: [config/orcamento_contexto.json, schemas/]
    lei_principal: 1
  4_ferramentas:
    entrada: decisao_em_formato_tipado
    saida: mudanca_reversivel_e_registrada
    artefatos: [mcp.json, scripts/, data/estado.db]
    lei_principal: 7
```

**4.3 Sessão de operação das quatro camadas**

```console
$ python esteira.py --tarefa "aplicar migracao v12"
[CAMADA 1] contexto carregado: 4.100 tokens (orçamento 8.000 por turno)
[CAMADA 2] inspecionando comando: psql -f migracao_v12.sql
[CAMADA 2] BLOQUEIO -> comando sem --single-transaction em base marcada como critica
[CAMADA 3] decisao revisada: reescrever comando em transacao unica
[CAMADA 2] inspecionando comando: psql --single-transaction -f migracao_v12.sql
[CAMADA 2] autorizado (timeout 60s)
[CAMADA 4] executando em worktree .worktrees/tarefa-12
[CAMADA 4] resultado registrado em data/estado.db (linha 8421)
[PORTAO] exit 0 -> entrega confirmada
```

### ⑤ Verificação / Gate

```bash
python esteira.py --tarefa "aplicar migracao v12"
```

### ⑥ Feito quando…

- [ ] Começar pelas ferramentas porque é a parte visível. A ordem correta de montagem é contexto, harness, motor e ferramentas — nessa sequência
- [ ] Tratar as camadas como hierarquia de importância. Nenhuma é mais importante; cada uma cobre um tipo de falha que as outras não cobrem
- [ ] Configurar governança apenas no ambiente de desenvolvimento. Se o servidor não tem o mesmo disjuntor, o sistema não tem disjuntor
- [ ] Fazer o retorno de falha voltar direto à execução. Repetir ação sem rever decisão é a assinatura do laço de erro que drena orçamento
- [ ] Ampliar ferramentas sem ampliar auditoria. Cada ferramenta nova é uma credencial a mais — trate-a como tal [9]

### ⑦ Armadilhas

- Começar pelas ferramentas porque é a parte visível. A ordem correta de montagem é contexto, harness, motor e ferramentas — nessa sequência
- Tratar as camadas como hierarquia de importância. Nenhuma é mais importante; cada uma cobre um tipo de falha que as outras não cobrem
- Configurar governança apenas no ambiente de desenvolvimento. Se o servidor não tem o mesmo disjuntor, o sistema não tem disjuntor
- Fazer o retorno de falha voltar direto à execução. Repetir ação sem rever decisão é a assinatura do laço de erro que drena orçamento
- Ampliar ferramentas sem ampliar auditoria. Cada ferramenta nova é uma credencial a mais — trate-a como tal [9]

## Passo 6 — Camada 1 — Contexto e Governança: Densidade, Localidade e Determinismo

> **Estágio:** Painel operacional  ·  **Origem:** Cap. 6 — Camada 1 — Contexto e Governança: Densidade, Localidade e Determinismo

### ① Objetivo do passo

Ensinar os três princípios universais de contexto — Densidade de Shannon, Localidade de Contexto e Determinismo Declarativo — e a Constituição Viva que os materializa no repositório.

### ② Pré-requisito

Passo 5 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 Medindo densidade de contexto com evidência**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analisador de densidade de contexto para documentos de governanca."""

import re
import sys
from pathlib import Path
from typing import Dict

TERMOS_PROLIXOS = (
    "por favor", "gostaria", "poderia", "talvez", "se possivel",
    "espero que", "bom dia", "boa tarde", "atenciosamente", "obrigado",
)

LIMITE_APROVACAO = 80.0


def analisar(texto: str) -> Dict[str, float]:
    palavras = re.findall(r"\b\w+\b", texto.lower())
    total = len(palavras)
    if total == 0:
        return {"palavras": 0.0, "prolixos": 0.0, "densidade": 0.0}

    baixo = texto.lower()
    prolixos = sum(
        len(re.findall(r"\b" + re.escape(t) + r"\b", baixo))
        for t in TERMOS_PROLIXOS
    )
    penalidade = (prolixos * 12) / total
    densidade = max(0.0, min(100.0, 100.0 - penalidade * 100))
    return {"palavras": float(total), "prolixos": float(prolixos),
            "densidade": round(densidade, 2)}


def medir_blocos(texto: str) -> int:
    """Conta blocos separados por linha em branco — proxy de fragmentacao util."""
    return len([b for b in re.split(r"\n\s*\n", texto) if b.strip()])


def main() -> int:
    alvo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("AGENTS.md")
    if not alvo.exists():
        print(f"[FALHA] documento nao encontrado: {alvo}")
        return 1

    texto = alvo.read_text(encoding="utf-8")
    metricas = analisar(texto)
    print("=" * 60)
    print(f"DENSIDADE DE CONTEXTO — {alvo.name}")
    print("=" * 60)
    print(f"  palavras          : {int(metricas['palavras'])}")
    print(f"  termos prolix
```

**4.2 Separando prefixo estável de contexto volátil**

```json
{
  "prefixo_estavel": {
    "ordem_fixa": true,
    "conteudo": [
      "AGENTS.md (constituicao)",
      "docs/protocolos/convencoes.md",
      "schemas/contratos.json"
    ],
    "politica_de_mudanca": "somente-por-revisao-com-justificativa"
  },
  "contexto_volatil": {
    "conteudo": [
      "diff do turno atual",
      "saida do ultimo comando",
      "lista de pendencias abertas"
    ],
    "politica_de_expurgo": "descartar-entre-fases",
    "teto_por_turno_tokens": 8000
  },
  "proibido_no_contexto": [
    "logs integrais sem filtro",
    "transcricao de conversa anterior",
    "saudacoes e preambulos",
    "arquivo inteiro quando o diff basta"
  ]
}
```

**4.3 Sessão real de diagnóstico de contexto**

```console
$ python gates/densidade-contexto.py AGENTS.md
============================================================
DENSIDADE DE CONTEXTO — AGENTS.md
============================================================
  palavras          : 1840
  termos prolixos   : 14
  blocos de conteudo: 62
  indice de densidade: 90.87 / 100
------------------------------------------------------------
[APROVADO] exit 0 (limite 80.0)

$ python gates/densidade-contexto.py docs/protocolos/tudo-junto.md
  palavras          : 9120
  termos prolixos   : 96
  blocos de conteudo: 51
  indice de densidade: 87.37 / 100
  AVISO: 9120 palavras na bancada — mova o detalhe para as gavetas de modulo
------------------------------------------------------------
[APROVADO] exit 0 (limite 80.0)
```

### ⑤ Verificação / Gate

```bash
python gates/densidade-contexto.py AGENTS.md
```

### ⑥ Feito quando…

- [ ] Confundir densidade com brevidade. Frase curta e vaga tem menos informação que parágrafo preciso
- [ ] Promover detalhe de módulo para a raiz. Isso dilui as leis que valem para todos no meio de regras que valem para poucos
- [ ] Reordenar a constituição a cada edição. Estabilidade de ordem é o que habilita a economia de prefixo
- [ ] Manter pedido enfático onde caberia portão binário. "Por favor, não faça X" não sobrevive a contexto saturado [3]
- [ ] Guardar credencial no contexto. Regra de segurança que depende de o agente lembrar de não vazar não é regra de segurança

### ⑦ Armadilhas

- Confundir densidade com brevidade. Frase curta e vaga tem menos informação que parágrafo preciso
- Promover detalhe de módulo para a raiz. Isso dilui as leis que valem para todos no meio de regras que valem para poucos
- Reordenar a constituição a cada edição. Estabilidade de ordem é o que habilita a economia de prefixo
- Manter pedido enfático onde caberia portão binário. "Por favor, não faça X" não sobrevive a contexto saturado [3]
- Guardar credencial no contexto. Regra de segurança que depende de o agente lembrar de não vazar não é regra de segurança

## Passo 7 — Camada 2 — Harness e Ciclo de Vida: Disjuntores, Worktrees e Quality Gates

> **Estágio:** Painel operacional  ·  **Origem:** Cap. 7 — Camada 2 — Harness e Ciclo de Vida: Disjuntores, Worktrees e Quality Gates

### ① Objetivo do passo

Blindar o ambiente de execução com os três princípios do harness: isolamento de execução, interceptação de ciclo de vida e agnosticismo operacional.

### ② Pré-requisito

Passo 6 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 Disjuntor de terminal com lista de bloqueio e teto de tempo**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Disjuntor de terminal: inspecao pre-comando, lista de bloqueio e teto de tempo."""

import re
import subprocess
import sys
from typing import List, Tuple

TIMEOUT_PADRAO_S = 30

# (padrao, motivo) — inspecionado sobre o comando normalizado
BLOQUEIOS: List[Tuple[str, str]] = [
    (r"rm\s+-(?:rf|fr)\s+[/~]", "remocao recursiva em raiz ou home"),
    (r"remove-item\s+.*-recurse.*-force", "remocao recursiva forcada"),
    (r"drop\s+database", "destruicao de banco de dados"),
    (r"git\s+push\s+.*--force", "envio forcado de branch"),
    (r"git\s+commit\s+.*--no-verify", "tentativa de pular portoes de qualidade"),
    (r"format\s+[a-z]:", "formatacao de unidade"),
    (r":\(\)\s*\{.*\};\s*:", "fork bomb"),
]

BLOCOS = [re.compile(p, re.IGNORECASE) for p, _ in BLOQUEIOS]


def inspecionar(comando: str) -> Tuple[bool, str]:
    for (padrao, motivo), compilado in zip(BLOQUEIOS, BLOCOS):
        if compilado.search(comando.strip()):
            return False, f"DISJUNTOR ABERTO: {motivo} (padrao {padrao!r})"
    return True, "comando liberado"


def executar(comando: str, timeout: int = TIMEOUT_PADRAO_S) -> int:
    liberado, motivo = inspecionar(comando)
    if not liberado:
        print(f"[BLOQUEIO] {motivo}")
        print(f"[BLOQUEIO] comando rejeitado: {comando!r}")
        return 1

    print(f"[EXECUTANDO] {comando!r} (timeout {timeout}s)")
    try:
        processo = subprocess.run(comando, shell=True, capture_output=True,
                                  text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
  
```

**4.2 Configuração de contenção do harness**

```json
{
  "harness": {
    "isolamento": {
      "modo": "worktree-por-tarefa",
      "diretorio_base": ".worktrees",
      "descartar_em_reprovacao": true
    },
    "execucao": {
      "timeout_padrao_s": 30,
      "timeout_maximo_s": 120,
      "teto_repeticao_erro": 2,
      "teto_turnos_sem_checkpoint": 8
    },
    "bloqueios": ["rm -rf /", "drop database", "git push --force", "git commit --no-verify"],
    "pre_commit": {
      "ordem": ["segredos", "sintaxe", "anti-stub", "dependencias", "testes", "honestidade"],
      "bloquear_em_falha": true,
      "tempo_maximo_s": 20
    }
  }
}
```

**4.3 Sessão de operação com isolamento**

```console
$ python orquestrador.py --tarefa migracao-v12
[ORCA] criando ambiente isolado .worktrees/tarefa-12 (branch agent/tarefa-12)
[OK] worktree criado a partir de main
$ python disjuntor.py "git commit -m 'ajuste' --no-verify"
[BLOQUEIO] DISJUNTOR ABERTO: tentativa de pular portoes de qualidade
[BLOQUEIO] comando rejeitado: "git commit -m 'ajuste' --no-verify"
$ python disjuntor.py "pytest -q tests/test_migracao.py"
[EXECUTANDO] 'pytest -q tests/test_migracao.py' (timeout 30s)
  .....................
  21 passed in 1.84s
[RETORNO] exit 0
$ python orquestrador.py --concluir tarefa-12
[PORTAO] 6/6 aprovados -> merge em main
[ORCA] worktree .worktrees/tarefa-12 removido; planta central intacta
```

**4.5 Teste negativo da contenção**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teste negativo da contencao: prova que o disjuntor barra o que deve barrar."""

import re
import sys
from typing import List, Tuple

BLOQUEIOS: List[Tuple[str, str]] = [
    (r"rm\s+-(?:rf|fr)\s+[/~]", "remocao recursiva em raiz ou home"),
    (r"drop\s+database", "destruicao de banco de dados"),
    (r"git\s+push\s+.*--force", "envio forcado de branch"),
    (r"git\s+commit\s+.*--no-verify", "pular portoes de qualidade"),
]

COMPILADOS = [re.compile(p, re.IGNORECASE) for p, _ in BLOQUEIOS]

# (comando, deve_ser_bloqueado)
CASOS: List[Tuple[str, bool]] = [
    ("rm -rf /var/lib/dados", True),
    ("mysql -e 'DROP DATABASE producao'", True),
    ("git push origin main --force", True),
    ("git commit -m 'fix' --no-verify", True),
    ("rm -rf ./build", False),
    ("git push origin feature/nova-tela", False),
    ("pytest -q tests/test_frete.py", False),
    ("psql --single-transaction -f migracao_v12.sql", False),
]


def bloqueado(comando: str) -> bool:
    return any(p.search(comando) for p in COMPILADOS)


def executar_suite() -> Tuple[int, List[str]]:
    falhas: List[str] = []
    for comando, esperado in CASOS:
        obtido = bloqueado(comando)
        if obtido != esperado:
            direcao = "nao barrou" if esperado else "barrou por engano"
            falhas.append(f"{direcao}: {comando!r}")
    return len(CASOS), falhas


def main() -> int:
    total, falhas = executar_suite()
    print("=" * 62)
    print(f"TESTE NEGATIVO DA CONTENCAO — {total} caso(s)")
    print("=" * 62)
    for falha in falhas:
        p
```

### ⑤ Verificação / Gate

```bash
python disjuntor.py "pytest -q tests/test_migracao.py"
```

### ⑥ Feito quando…

- [ ] Desencorajar em vez de impossibilitar. Se pular o portão é possível, alguém vai pular sob pressão — e será justamente no commit que quebra produção
- [ ] Confundir lista de bloqueio longa com segurança. Lista exaustiva não é revisada; lista curta é confiável
- [ ] Deixar diretórios de trabalho órfãos. Ambiente órfão é estado fantasma que confunde o próximo agente
- [ ] Testar a contenção apenas no caminho felizes. Portão precisa ser testado com entrada hostil, senão você não sabe se ele funciona
- [ ] Tratar teto de repetição como detalhe. É o controle que separa um erro barato de uma fatura inesperada [4]

### ⑦ Armadilhas

- Desencorajar em vez de impossibilitar. Se pular o portão é possível, alguém vai pular sob pressão — e será justamente no commit que quebra produção
- Confundir lista de bloqueio longa com segurança. Lista exaustiva não é revisada; lista curta é confiável
- Deixar diretórios de trabalho órfãos. Ambiente órfão é estado fantasma que confunde o próximo agente
- Testar a contenção apenas no caminho felizes. Portão precisa ser testado com entrada hostil, senão você não sabe se ele funciona
- Tratar teto de repetição como detalhe. É o controle que separa um erro barato de uma fatura inesperada [4]

## Passo 8 — Camada 3 — Motor Cognitivo: Roteamento, Contratos Tipados e Economia de Tokens

> **Estágio:** Painel operacional  ·  **Origem:** Cap. 8 — Camada 3 — Motor Cognitivo: Roteamento, Contratos Tipados e Economia de Tokens

### ① Objetivo do passo

Ensinar a lei do determinismo em primeiro lugar, o roteamento por tiers de capacidade, os contratos tipados de saída e a Tríade Caveman Ultra de economia.

### ② Pré-requisito

Passo 7 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 O roteador: decidir antes de gastar**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Roteador cognitivo: determinismo primeiro, capacidade sob demanda."""

import re
import sys
from dataclasses import dataclass
from typing import Callable, Optional

NIVEL_1 = "capacidade-leve"
NIVEL_2 = "capacidade-media"
NIVEL_3 = "raciocinio-profundo"

TETO_TOKENS_POR_NIVEL = {NIVEL_1: 800, NIVEL_2: 4000, NIVEL_3: 12000}


@dataclass(frozen=True)
class Decisao:
    nivel: str
    deterministico: bool
    motivo: str
    teto_tokens: int


def normalizar_slug(texto: str) -> Optional[str]:
    if not isinstance(texto, str) or not texto.strip():
        return None
    limpo = re.sub(r"[^a-zA-Z0-9\s-]", "", texto).strip().lower()
    return re.sub(r"[\s-]+", "-", limpo) or None


def contar_campos(dados: dict, obrigatorios: list) -> Optional[list]:
    if not isinstance(dados, dict):
        return None
    return [c for c in obrigatorios if c not in dados or dados[c] in (None, "")]


def decidir(tarefa: str) -> Decisao:
    t = tarefa.lower()
    if any(k in t for k in ("slug", "renomear", "normalizar", "formatar")):
        return Decisao(NIVEL_1, True, "transformacao textual com regra exata", 0)
    if any(k in t for k in ("validar contrato", "checar campos", "conferir esquema")):
        return Decisao(NIVEL_1, True, "validacao de esquema e deterministica", 0)
    if any(k in t for k in ("teste", "implementar", "refatorar", "corrigir")):
        return Decisao(NIVEL_2, False, "engenharia delimitada exige sintese", 4000)
    return Decisao(NIVEL_3, False, "problema aberto exige raciocinio profundo", 12000)


CHECAGENS: dic
```

**4.2 Contrato tipado de saída**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ResultadoDeAnalise",
  "type": "object",
  "required": ["tarefa", "nivel", "achados", "confianca"],
  "additionalProperties": false,
  "properties": {
    "tarefa": { "type": "string", "minLength": 4 },
    "nivel": { "type": "string", "enum": ["capacidade-leve", "capacidade-media", "raciocinio-profundo"] },
    "achados": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["arquivo", "linha", "severidade"],
        "additionalProperties": false,
        "properties": {
          "arquivo": { "type": "string" },
          "linha": { "type": "integer", "minimum": 1 },
          "severidade": { "type": "string", "enum": ["baixa", "media", "alta"] }
        }
      }
    },
    "confianca": { "type": "number", "minimum": 0, "maximum": 1 }
  }
}
```

**4.3 Sessão de operação do roteador**

```console
$ python roteador.py "normalizar slug do capitulo"
tarefa            : normalizar slug do capitulo
nivel             : capacidade-leve
deterministico    : True
motivo            : transformacao textual com regra exata
teto de tokens    : 0
resultado direto  : meu-capitulo-introducao

$ python roteador.py "implementar teste do modulo de frete"
tarefa            : implementar teste do modulo de frete
nivel             : capacidade-media
deterministico    : False
motivo            : engenharia delimitada exige sintese
teto de tokens    : 4000
[CONTRATO] saida validada: 4 campos obrigatorios presentes
[CONSUMO] 1.uss 842 tokens de entrada (prefixo estavel reaproveitado)
```

### ⑤ Verificação / Gate

```bash
python roteador.py "implementar teste do modulo de frete"
```

### ⑥ Feito quando…

- [ ] Usar modelo para cálculo. Cada verificação determinística convertida em script economiza duas vezes: custo e latência
- [ ] Padronizar no modelo mais caro. Você paga raciocínio profundo por triagem mecânica e ainda ganha variação indesejada em tarefa que deveria ser repetível
- [ ] Consumir texto livre no pipeline. Toda extração por expressão regular é dívida acumulada que quebra na primeira mudança de formatação
- [ ] Comprimir contexto sem medir a consequência. Economia e retrabalho sobem juntos quando você corta significado em vez de redundância [10]
- [ ] Confiar em benchmark público como prova de capacidade real. A evidência é contundente: em base de avaliação com dados não vistos, o mesmo modelo que resolve a casa dos 23% numa suíte cai para cerca de 17,8% em outra, e outro caiu de 23,1% para 14,9% [3]. Benchmark mede o que ele mede — e não mede o seu domínio [1]

### ⑦ Armadilhas

- Usar modelo para cálculo. Cada verificação determinística convertida em script economiza duas vezes: custo e latência
- Padronizar no modelo mais caro. Você paga raciocínio profundo por triagem mecânica e ainda ganha variação indesejada em tarefa que deveria ser repetível
- Consumir texto livre no pipeline. Toda extração por expressão regular é dívida acumulada que quebra na primeira mudança de formatação
- Comprimir contexto sem medir a consequência. Economia e retrabalho sobem juntos quando você corta significado em vez de redundância [10]
- Confiar em benchmark público como prova de capacidade real. A evidência é contundente: em base de avaliação com dados não vistos, o mesmo modelo que resolve a casa dos 23% numa suíte cai para cerca de 17,8% em outra, e outro caiu de 23,1% para 14,9% [3]. Benchmark mede o que ele mede — e não mede o seu domínio [1]

## Passo 9 — Camada 4 — Ferramentas, MCP e Persistência: A Usina Determinística

> **Estágio:** Painel operacional  ·  **Origem:** Cap. 9 — Camada 4 — Ferramentas, MCP e Persistência: A Usina Determinística

### ① Objetivo do passo

Construir o braço físico da fábrica: servidores MCP sob escopo mínimo, scripts determinísticos idempotentes e persistência de estado auditável.

### ② Pré-requisito

Passo 8 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 Ferramenta idempotente com escopo e validação de saída**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ferramenta idempotente de sincronizacao com escopo minimo e auditoria."""

import hashlib
import json
import sqlite3
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

ESQUEMA_REGISTRO = {"origem", "destino", "hash", "status"}
BANCO = Path("data/estado.db")


@dataclass(frozen=True)
class Resultado:
    origem: str
    destino: str
    hash: str
    status: str


def escopo_permitido(destino: Path, raizes: list) -> bool:
    """Escopo minimo: a ferramenta so escreve dentro das raizes autorizadas."""
    try:
        resolvido = destino.resolve()
    except OSError:
        return False
    return any(resolvido.is_relative_to(Path(r).resolve()) for r in raizes)


def calcular_hash(conteudo: bytes) -> str:
    return hashlib.sha256(conteudo).hexdigest()[:16]


def sincronizar(origem: Path, destino: Path, raizes: list) -> Optional[Resultado]:
    if not origem.is_file():
        return None
    if not escopo_permitido(destino, raizes):
        raise PermissionError(f"destino fora do escopo autorizado: {destino}")

    dados = origem.read_bytes()
    digest = calcular_hash(dados)

    # Idempotencia: se o hash atual ja e o desejado, nada a fazer.
    if destino.exists() and calcular_hash(destino.read_bytes()) == digest:
        return Resultado(str(origem), str(destino), digest, "inalterado")

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(dados)
    return Resultado(str(origem), str(destino), digest, "sincronizado")


def validar_saida(regist
```

**4.2 Declaração de ferramentas com permissão mínima**

```json
{
  "servidores": [
    {
      "nome": "estado-interno",
      "transporte": "stdio",
      "escopo": {
        "leitura": ["data/", "config/"],
        "escrita": ["data/estado.db"],
        "proibido": ["..", "/etc", "variaveis-de-ambiente-sensiveis"]
      },
      "validacao_de_saida": "esquema-registro.json",
      "exige_autorizacao": false
    },
    {
      "nome": "publicacao",
      "transporte": "stdio",
      "escopo": {
        "leitura": ["dist/"],
        "escrita": ["dist/"],
        "proibido": ["producao", "secrets", ".."]
      },
      "validacao_de_saida": "esquema-publicacao.json",
      "exige_autorizacao": true,
      "motivo_autorizacao": "efeito irreversivel em ambiente publico"
    }
  ]
}
```

**4.3 Sessão real de operação**

```console
$ python ferramenta.py README.md dist/README.md
{
  "origem": "README.md",
  "destino": "dist/README.md",
  "hash": "9f2c41ab77de0310",
  "status": "sincronizado"
}

$ python ferramenta.py README.md dist/README.md
{
  "origem": "README.md",
  "destino": "dist/README.md",
  "hash": "9f2c41ab77de0310",
  "status": "inalterado"
}

$ python ferramenta.py README.md producao/README.md
[BLOQUEIO] destino fora do escopo autorizado: producao/README.md

$ sqlite3 data/estado.db "SELECT id, status, registrado_em FROM acoes ORDER BY id DESC LIMIT 2;"
2|inalterado|2026-09-12 14:22:07
1|sincronizado|2026-09-12 14:21:51
```

### ⑤ Verificação / Gate

```bash
python ferramenta.py README.md dist/README.md
```

### ⑥ Feito quando…

- [ ] Confiar em ferramenta pela descrição. A descrição é texto; o comportamento é código, e os dois podem divergir sem aviso [3]
- [ ] Consumir saída sem validar esquema. Campo inesperado quebra pipeline silenciosamente, e o sintoma aparece longe da causa
- [ ] Conceder escopo de escrita amplo "por conveniência". Conveniência de hoje é incidente de amanhã
- [ ] Escrever ferramenta não idempotente e recuperar falha manualmente. Toda recuperação manual é uma oportunidade de erro sob pressão
- [ ] Tratar o banco de estado como banco de aplicação. Ele guarda decisão e telemetria, com retenção declarada — não dados de negócio [14]

### ⑦ Armadilhas

- Confiar em ferramenta pela descrição. A descrição é texto; o comportamento é código, e os dois podem divergir sem aviso [3]
- Consumir saída sem validar esquema. Campo inesperado quebra pipeline silenciosamente, e o sintoma aparece longe da causa
- Conceder escopo de escrita amplo "por conveniência". Conveniência de hoje é incidente de amanhã
- Escrever ferramenta não idempotente e recuperar falha manualmente. Toda recuperação manual é uma oportunidade de erro sob pressão
- Tratar o banco de estado como banco de aplicação. Ele guarda decisão e telemetria, com retenção declarada — não dados de negócio [14]

## Passo 10 — Implementação e Réplica das 4 Camadas: O Manual de Montagem

> **Estágio:** Circuito de segurança  ·  **Origem:** Cap. 10 — Implementação e Réplica das 4 Camadas: O Manual de Montagem

### ① Objetivo do passo

Fornecer o blueprint executável de montagem da fábrica: estrutura canônica de diretórios, sincronização agnóstica de componentes e blindagem de projetos legados.

### ② Pré-requisito

Passo 9 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 Provisionador idempotente da estrutura canônica**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provisionador idempotente da estrutura canonica das 4 camadas."""

import json
import sys
from pathlib import Path
from typing import List, Tuple

PASTAS = [
    "componentes/specs",
    "componentes/ferramentas",
    "componentes/ganchos",
    "docs/protocolos",
    "docs/decisoes",
    "gates",
    "schemas",
]

# (caminho, conteudo, politica) — 'preservar' nunca sobrescreve; 'gerar' sempre reescreve
ARQUIVOS: List[Tuple[str, str, str]] = [
    (
        "AGENTS.md",
        "# Governanca Canonica\n\n"
        "## Leis inegociaveis\n"
        "1. Determinismo primeiro: script antes de modelo.\n"
        "2. Qualidade binaria: exit 0 aprova, exit 1 bloqueia.\n"
        "3. Persistencia estruturada: decisao sempre em disco.\n"
        "4. Economia severa: prefixo estavel, saida densa, expurgo entre fases.\n"
        "5. Supremacia agnostica: nenhuma regra depende de ambiente.\n"
        "6. Desenvolvedor no controle: proibido agente headless invisivel.\n"
        "7. Zero stubs: proibido corpo vazio ou retorno ficticio.\n"
        "8. Anti-NIH: justificar antes de construir mecanismo generico.\n"
        "9. Honestidade de rotulo: nao alegar mais do que o teste provou.\n"
        "10. Comunicacao direta: sem preambulo nem repeticao.\n",
        "preservar",
    ),
    ("CLAUDE.md", "@AGENTS.md\nSiga as diretivas canonicas da raiz.\n", "gerar"),
    ("GEMINI.md", "# Governanca centralizada\nConsulte AGENTS.md na raiz.\n", "gerar"),
    (".cursorrules", "Consulte AGENTS.md na raiz.\n", "gerar"),
    (".windsurfrules", "Consult
```

**4.2 Plano de blindagem de legado**

```yaml
blindagem_de_legado:
  principio: risco-decrescente
  etapas:
    - ordem: 1
      acao: inventariar
      altera_codigo: false
      entregavel: relatorio de ausencias por camada
    - ordem: 2
      acao: instalar disjuntor de comando
      altera_codigo: false
      entregavel: gates/disjuntor.py
    - ordem: 3
      acao: instalar portao anti-stub
      altera_codigo: false
      entregavel: gates/anti-stub-ast.py
    - ordem: 4
      acao: declarar constituicao
      altera_codigo: false
      entregavel: AGENTS.md
    - ordem: 5
      acao: medir consumo por tarefa
      altera_codigo: false
      entregavel: relatorio de consumo
    - ordem: 6
      acao: isolar trabalho novo em worktree
      altera_codigo: false
      entregavel: politica de execucao
  proibido: [reescrever-modulo-existente, migrar-banco, renomear-pacotes]
```

**4.3 Sessão de montagem**

```console
$ python provisionar.py
==============================================================
PROVISIONADOR IDEMPOTENTE — 4 CAMADAS
==============================================================
[PASTAS] criadas nesta execucao: 7
   + componentes/specs
   + componentes/ferramentas
   + gates
   + schemas
[ARQUIVOS] gravados: 4 | preservados: 0
--------------------------------------------------------------
[OK] exit 0 — estrutura canonica pronta e reexecutavel.

$ python provisionar.py
[PASTAS] criadas nesta execucao: 0
[ARQUIVOS] gravados: 0 | preservados: 1
--------------------------------------------------------------
[OK] exit 0 — estrutura canonica pronta e reexecutavel.

$ python auditar-4-camadas.py
[CAMADA 1 CONTEXTO E GOVERNANCA] OK
[CAMADA 2 HARNESS E CICLO DE VIDA] INCONFORME
   -> nenhum portao deterministico em gates/
[CAMADA 3 MOTOR COGNITIVO] INCONFORME
   -> politica de orcamento de contexto ausente
[CAMADA 4 FERRAMENTAS E PERSISTENCIA] OK
[REPROVADO] exit 1 — inconformidade em: 2 HARNESS, 3 MOTOR
```

**4.5 Auditoria de acoplamento entre camadas**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditor de acoplamento: reprova import que viola a ordem das camadas."""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Nivel 4 depende de 3, que depende de 2, que depende de 1 — e nunca o inverso.
CAMADAS: Dict[int, str] = {
    1: "contexto",
    2: "harness",
    3: "motor",
    4: "ferramentas",
}

# Diretorio -> nivel. Camadas de nivel baixo nao podem importar niveis acima.
DIRETORIOS: Dict[str, int] = {
    "contexto": 1,
    "harness": 2,
    "motor": 3,
    "ferramentas": 4,
}

IGNORAR = {".venv", "venv", "__pycache__", ".git", "tests"}


def nivel_do_arquivo(caminho: Path) -> int:
    for parte in caminho.parts:
        if parte in DIRETORIOS:
            return DIRETORIOS[parte]
    return 0


def modulos_importados(arquivo: Path) -> List[str]:
    try:
        arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
    except SyntaxError:
        return []
    nomes: List[str] = []
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            nomes.extend(alias.name for alias in no.names)
        elif isinstance(no, ast.ImportFrom) and no.module:
            nomes.append(no.module)
    return nomes


def nivel_do_import(nome: str) -> int:
    raiz = nome.split(".")[0]
    return DIRETORIOS.get(raiz, 0)


def auditar(raiz: Path) -> List[Tuple[str, str]]:
    violacoes: List[Tuple[str, str]] = []
    for arquivo in raiz.rglob("*.py"):
        if IGNORAR.intersection(arquivo.parts):
            continue
        origem = nivel_do_arquivo(arquivo)
        if
```

### ⑤ Verificação / Gate

```bash
python auditar-4-camadas.py
```

### ⑥ Feito quando…

- [ ] Reescrever em vez de governar. Reescrever troca dívida conhecida por risco desconhecido e consome o cronograma inteiro
- [ ] Começar a montagem pela camada mais visível. A ordem correta é freio, declaração, medição e isolamento — risco decrescente
- [ ] Sobrescrever arquivo que contém decisão humana. Política de sobrescrita mal definida destrói trabalho sem aviso
- [ ] Considerar a montagem pronta porque os arquivos existem. O critério é a auditoria transversal com capacidade operacional, não a presença de pasta
- [ ] Editar configuração de ambiente à mão. Divergência local vira bug silencioso na próxima sincronização [7]

### ⑦ Armadilhas

- Reescrever em vez de governar. Reescrever troca dívida conhecida por risco desconhecido e consome o cronograma inteiro
- Começar a montagem pela camada mais visível. A ordem correta é freio, declaração, medição e isolamento — risco decrescente
- Sobrescrever arquivo que contém decisão humana. Política de sobrescrita mal definida destrói trabalho sem aviso
- Considerar a montagem pronta porque os arquivos existem. O critério é a auditoria transversal com capacidade operacional, não a presença de pasta
- Editar configuração de ambiente à mão. Divergência local vira bug silencioso na próxima sincronização [7]

## Passo 11 — Orquestração Cross-Harness: Subagentes, Worktrees e o Protocolo ORCA ADE

> **Estágio:** Circuito de segurança  ·  **Origem:** Cap. 11 — Orquestração Cross-Harness: Subagentes, Worktrees e o Protocolo ORCA ADE

### ① Objetivo do passo

Ensinar a orquestrar múltiplos agentes e harnesses com isolamento físico, funil deliberativo com checkpoints humanos e paralelismo seguro.

### ② Pré-requisito

Passo 10 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 Gerenciador de ambientes isolados por tarefa**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gerenciador de ambientes isolados (ORCA ADE) para tarefas agenticas."""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

BASE = Path(".worktrees")
BRANCH_BASE = "main"


def _git(args: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, timeout=30)


def listar() -> List[str]:
    resultado = _git(["worktree", "list", "--porcelain"])
    if resultado.returncode != 0:
        return []
    return [linha.split(" ", 1)[1]
            for linha in resultado.stdout.splitlines()
            if linha.startswith("worktree ")]


def criar(nome: str, base: str = BRANCH_BASE) -> Optional[Path]:
    destino = BASE / nome
    branch = f"agent/{nome}"
    if destino.exists():
        print(f"[AVISO] ambiente ja existe: {destino}")
        return destino
    BASE.mkdir(exist_ok=True)
    resultado = _git(["worktree", "add", "-b", branch, str(destino), base])
    if resultado.returncode != 0:
        print(f"[FALHA] nao foi possivel criar ambiente: {resultado.stderr.strip()}")
        return None
    print(f"[OK] ambiente isolado criado: {destino} (branch {branch})")
    return destino


def descartar(nome: str, remover_branch: bool = True) -> bool:
    destino = BASE / nome
    resultado = _git(["worktree", "remove", "--force", str(destino)])
    if resultado.returncode != 0:
        print(f"[FALHA] nao foi possivel remover {destino}: {resultado.stderr.strip()}")
        return False
    if base_existe(destino
```

**4.2 Plano de despacho em lotes com desfecho obrigatório**

```json
{
  "plano": "PLAN-0011-governanca-de-frete",
  "aprovado_por": "operador",
  "aprovado_em": "2026-09-11",
  "lote_maximo": 4,
  "politica_de_memoria": "resumir-e-expurgar-regiao-volatil-entre-lotes",
  "politica_de_falha": "backoff-15s-30s-60s-ate-3-tentativas",
  "tarefas": [
    { "id": "t1", "escopo": "extrair contrato de frete",  "estado": "pendente", "criterio": "esquema valida" },
    { "id": "t2", "escopo": "criar portao anti-duplicata", "estado": "pendente", "criterio": "exit 1 em duplicata" },
    { "id": "t3", "escopo": "migrar consumidores",         "estado": "pendente", "criterio": "testes passam" },
    { "id": "t4", "escopo": "remover modulo antigo",       "estado": "pendente", "criterio": "nenhuma referencia restante" }
  ]
}
```

**4.3 Sessão de orquestração**

```console
$ python orca.py criar t1-contrato-frete
[OK] ambiente isolado criado: .worktrees/t1-contrato-frete (branch agent/t1-contrato-frete)
$ python orca.py criar t2-portao-duplicata
[OK] ambiente isolado criado: .worktrees/t2-portao-duplicata (branch agent/t2-portao-duplicata)

$ cd .worktrees/t2-portao-duplicata && python gates/anti-duplicata.py
[REPROVADO] exit 1 — dois modulos exportam calculo_frete

$ python orca.py descartar t2-portao-duplicata
[OK] ambiente descartado: .worktrees/t2-portao-duplicata
[REGISTRO] t2 = falhou (backoff 15s; tentativa 1 de 3)

$ cd .worktrees/t1-contrato-frete && python gates/validar-esquema.py
[APROVADO] exit 0 — contrato de frete valida
$ cd - && python orca.py listar
[".worktrees/t1-contrato-frete"]
[REGISTRO] t1 = sucesso (merge em main autorizado)
```

**4.5 Resumo de lote e expurgo de contexto**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resumo de lote concluido: o unico artefato que sobrevive ao expurgo."""

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

LIMITE_CARACTERES = 1200


@dataclass
class ResumoDeLote:
    lote: int
    tarefas_concluidas: List[str]
    tarefas_reprovadas: List[str]
    arquivos_tocados: List[str]
    decisoes: List[str]
    pendencias: List[str]

    def texto(self) -> str:
        linhas = [f"Lote {self.lote} concluido"]
        linhas.append("Concluidas: " + (", ".join(self.tarefas_concluidas) or "nenhuma"))
        linhas.append("Reprovadas: " + (", ".join(self.tarefas_reprovadas) or "nenhuma"))
        linhas.append("Arquivos: " + (", ".join(self.arquivos_tocados) or "nenhum"))
        for decisao in self.decisoes:
            linhas.append(f"Decisao: {decisao}")
        for pendencia in self.pendencias:
            linhas.append(f"Pendencia: {pendencia}")
        return "\n".join(linhas)


LIMITES_SUGERIDOS = {
    "max_tarefas_por_resumo": 8,
    "max_decisoes": 5,
    "max_pendencias": 5,
    "max_tokens_no_proximo_lote": 4000,
}


def validar(resumo: ResumoDeLote) -> List[str]:
    problemas: List[str] = []
    if len(resumo.tarefas_concluidas) > LIMITES_SUGERIDOS["max_tarefas_por_resumo"]:
        problemas.append("resumo com tarefas demais: consolide antes de gerar o artefato")
    if len(resumo.decisoes) > LIMITES_SUGERIDOS["max_decisoes"]:
        problemas.append("decisoes demais para o artefato: mova o detalhe para a documentacao")
    if len(resumo.
```

### ⑤ Verificação / Gate

```bash
python orca.py criar t1-contrato-frete
```

### ⑥ Feito quando…

- [ ] Paralelizar antes de planejar. Sem fronteiras declaradas, tarefas "independentes" disputam recursos e o ganho desaparece em reconciliação
- [ ] Usar o diretório de trabalho compartilhado. Sem isolamento físico, a última escrita vence e a intenção se perde [1]
- [ ] Deixar agente rodando sem observação e sem teto. Horizonte longo sem supervisão é onde o desvio de comportamento se instala [7]
- [ ] Não registrar falha. Tarefa que falha e desaparece da contagem distorce a percepção de progresso e esconde o gargalo real
- [ ] Carregar o histórico de todos os lotes adiante. Isso reproduz a saturação de contexto que o protocolo deveria evitar [14]

### ⑦ Armadilhas

- Paralelizar antes de planejar. Sem fronteiras declaradas, tarefas "independentes" disputam recursos e o ganho desaparece em reconciliação
- Usar o diretório de trabalho compartilhado. Sem isolamento físico, a última escrita vence e a intenção se perde [1]
- Deixar agente rodando sem observação e sem teto. Horizonte longo sem supervisão é onde o desvio de comportamento se instala [7]
- Não registrar falha. Tarefa que falha e desaparece da contagem distorce a percepção de progresso e esconde o gargalo real
- Carregar o histórico de todos os lotes adiante. Isso reproduz a saturação de contexto que o protocolo deveria evitar [14]

## Passo 12 — Super-Auditoria e Entrega Soberana: O Certificado de Confiabilidade

> **Estágio:** Circuito de segurança  ·  **Origem:** Cap. 12 — Super-Auditoria e Entrega Soberana: O Certificado de Confiabilidade

### ① Objetivo do passo

Fechar o ciclo com a auditoria final determinística, o pacote de entrega verificável e a evolução contínua da fábrica sem dívida técnica silenciosa.

### ② Pré-requisito

Passo 11 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 Auditor do pacote de entrega**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditor do pacote de entrega: prova que cada item existe e abre."""

import json
import sys
import zipfile
from pathlib import Path
from typing import Dict, List

LEITORES = {
    ".md": lambda p: p.read_text(encoding="utf-8"),
    ".json": lambda p: json.loads(p.read_text(encoding="utf-8")),
    ".txt": lambda p: p.read_text(encoding="utf-8"),
    ".html": lambda p: p.read_text(encoding="utf-8"),
    ".csv": lambda p: p.read_text(encoding="utf-8"),
}


def abre(caminho: Path) -> Dict[str, str]:
    """Confirma que o arquivo existe e que o conteudo e legivel no formato."""
    if not caminho.exists():
        return {"item": caminho.name, "status": "ausente", "detalhe": "nao encontrado"}
    if caminho.stat().st_size == 0:
        return {"item": caminho.name, "status": "vazio", "detalhe": "zero bytes"}

    extensao = caminho.suffix.lower()
    if extensao == ".pdf":
        cabecalho = caminho.open("rb").read(5)
        ok = cabecalho == b"%PDF-"
        return {"item": caminho.name, "status": "ok" if ok else "corrompido",
                "detalhe": "cabecalho PDF valido" if ok else "cabecalho invalido"}
    if extensao in (".epub", ".zip"):
        try:
            with zipfile.ZipFile(caminho) as pacote:
                nomes = pacote.namelist()
            return {"item": caminho.name, "status": "ok" if nomes else "vazio",
                    "detalhe": f"{len(nomes)} entrada(s)"}
        except zipfile.BadZipFile:
            return {"item": caminho.name, "status": "corrompido", "detalhe": "zip invalido"}

    leitor =
```

**4.2 Manifesto de entrega com omissões declaradas**

```json
{
  "obra": "O Tratado das 4 Camadas da Fabrica Agentica",
  "edicao": "v3.0 — Edicao Expandida e Definitiva",
  "gerado_em": "2026-09-12",
  "entregues": [
    { "item": "livro_final.pdf", "formato": "pdf", "verificacao": "cabecalho PDF valido" },
    { "item": "livro_final.md", "formato": "markdown", "verificacao": "abre em utf-8" },
    { "item": "playbook.pdf", "formato": "pdf", "verificacao": "cabecalho PDF valido" }
  ],
  "nao_entregues": [
    { "item": "campanhas/", "motivo": "nao solicitado pelo operador na fase 0" },
    { "item": "maquina/", "motivo": "nao solicitado pelo operador na fase 0" }
  ],
  "garantias_medidas": [
    { "afirmacao": "auditoria de requisitos contratuais", "comando": "auditar-obra --estrito", "resultado": "exit 0" },
    { "afirmacao": "sintaxe de todos os blocos de codigo", "comando": "validar-codigo", "resultado": "100% aprovados" }
  ]
}
```

**4.3 Sessão de encerramento**

```console
$ python auditar-obra.py --estrito
[FALHA] R4  Minimo 20 referencias ABNT por capitulo
        -> capitulos abaixo: 7
[REPROVADO] exit 1 — 1 requisito nao conforme.
Relatorio: revisao/relatorio_auditoria.json

$ python auditar-obra.py --estrito
[OK] R3 7 secoes EITA-V2 por capitulo
[OK] R4 Minimo 20 referencias ABNT por capitulo
[OK] R13 Sem truncamento nem pendencias
[OK] R14 Rastreabilidade [N] texto <-> referencias
[CONFORME] exit 0 — nenhum requisito pendente.

$ python auditar-pacote.py distribuicao
[           OK] livro_final.pdf — cabecalho PDF valido
[           OK] livro_final.md — conteudo legivel
[           OK] playbook.pdf — cabecalho PDF valido
--------------------------------------------------------------
[APROVADO] exit 0 — pacote integro e verificavel.
```

**4.5 Gerador do certificado de confiabilidade**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gerador do certificado de confiabilidade a partir de verificacoes executadas."""

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

APROVADO = "aprovado"
REPROVADO = "reprovado"
NAO_VERIFICADO = "nao-verificavel"


@dataclass(frozen=True)
class Verificacao:
    afirmacao: str
    comando: str
    exit_code: Optional[int]

    def status(self) -> str:
        if self.exit_code is None:
            return NAO_VERIFICADO
        return APROVADO if self.exit_code == 0 else REPROVADO

    def linha(self) -> str:
        marca = self.status().upper()
        codigo = "-" if self.exit_code is None else str(self.exit_code)
        return f"[{marca:>15}] {self.afirmacao} (comando: {self.comando}, exit {codigo})"


def semaforo(verificacoes: List[Verificacao]) -> str:
    """Veredito binario: uma reprovacao bloqueia; nao verificavel vira ressalva."""
    if any(v.status() == REPROVADO for v in verificacoes):
        return "NAO CONFORME"
    if any(v.status() == NAO_VERIFICADO for v in verificacoes):
        return "CONFORME COM RESSALVA"
    return "CONFORME"


def validar_certificado(verificacoes: List[Verificacao]) -> List[str]:
    problemas: List[str] = []
    if not verificacoes:
        problemas.append("certificado vazio: nenhuma verificacao executada")
    for v in verificacoes:
        if not v.comando.strip():
            problemas.append(f"afirmacao sem comando de medicao: {v.afirmacao!r}")
        if len(v.afirmacao.split()) < 4:
            proble
```

### ⑤ Verificação / Gate

```bash
python auditar-obra.py --estrito
```

### ⑥ Feito quando…

- [ ] Aceitar veredito com ressalvas em requisito bloqueante. Ressalva em requisito é requisito não cumprido com nome diferente
- [ ] Confiar em benchmark público como certificado. A evidência é clara: em conjuntos com casos não publicados, a resolução dos mesmos modelos recua para a casa dos 17% [3]
- [ ] Escrever a verdade sem medi-la. Toda afirmação de cobertura precisa do comando que a produziu; sem isso, ela é hipótese
- [ ] Entregar pacote sem declarar omissões. O que fica de fora em silêncio é indistinguível de esquecimento
- [ ] Não inspecionar o que a leitura não vê. Sobreposição, terminologia e truncamento são invisíveis a olho nu e triviais para o auditor [15]

### ⑦ Armadilhas

- Aceitar veredito com ressalvas em requisito bloqueante. Ressalva em requisito é requisito não cumprido com nome diferente
- Confiar em benchmark público como certificado. A evidência é clara: em conjuntos com casos não publicados, a resolução dos mesmos modelos recua para a casa dos 17% [3]
- Escrever a verdade sem medi-la. Toda afirmação de cobertura precisa do comando que a produziu; sem isso, ela é hipótese
- Entregar pacote sem declarar omissões. O que fica de fora em silêncio é indistinguível de esquecimento
- Não inspecionar o que a leitura não vê. Sobreposição, terminologia e truncamento são invisíveis a olho nu e triviais para o auditor [15]

# Checklist Mestre

**Passo 1 — O Contexto Real de Origem: Do Projeto Arsenal ao Ecossistema AIDD**

- [ ] Tratar a verificação de ambiente como burocracia opcional. Ela é o que separa um erro barato de descoberta (antes de gerar código) de um erro caro (depois de compilar)
- [ ] Deixar a configuração de intenção em branco "para decidir depois". Decisão não registrada é decisão tomada por padrão, e o padrão raramente é o que você queria
- [ ] Confundir volume de regras com qualidade de governança. A pesquisa sobre contexto é explícita: mais texto não significa mais aderência [12]
- [ ] Instalar os guardiões depois de já ter código em produção. Portão de qualidade retroativo é auditoria de dívida, não prevenção

**Passo 2 — O Dicionário do Iniciante: Glossário Descomplicado**

- [ ] Usar "modelo" e "agente" como sinônimos. Isso faz você procurar a culpa no lugar errado e gastar orçamento trocando o que não estava quebrado
- [ ] Tratar a janela de contexto como disco. Contexto guardado não é contexto disponível; a mesa de trabalho tem tamanho
- [ ] Chamar de "teste" o que é portão de qualidade. Um teste informa; um portão bloqueia. Sem bloqueio, o defeito continua no caminho
- [ ] Aceitar definição sem impacto declarado. Termo que não muda nenhuma decisão é ornamento
- [ ] Confiar em teste que nunca falhou. Verifique se o teste é capaz de falhar antes de considerar que ele protege algo [19]

**Passo 3 — A Crise do Desenvolvimento com IA: Os 4 Problemas Catastróficos**

- [ ] Tratar sintoma como causa. "O agente mudou de convenção" é sintoma; "o contexto saturou" é causa. Corrigir o sintoma gera retrabalho eterno
- [ ] Confiar em revisão manual como portão. Revisão humana é o filtro certo para intenção e o filtro errado para completude mecânica
- [ ] Rodar agentes paralelos sem isolamento físico. Sem diretório próprio, o paralelismo produz conflito, não velocidade
- [ ] Deixar execução autônoma sem teto de repetição e de turnos. O laço de erro é o modo de falha mais caro e mais fácil de prevenir
- [ ] Guardar a governança na ferramenta. Regra que só existe dentro de um aplicativo é regra que expira com o aplicativo

**Passo 4 — A Constituição Mestre: As 10 Leis Inegociáveis**

- [ ] Escrever leis sem fiscais. Lei sem fiscal é sugestão, e sugestão não sobrevive à pressão de prazo
- [ ] Confundir quantidade com cobertura. Vinte leis inúteis protegem menos do que sete leis fiscalizadas
- [ ] Desligar o fiscal para liberar a entrega. Isso inverte a relação: o fiscal existe justamente para o momento em que a pressão para ignorá-lo é maior
- [ ] Colocar fiscal caro no gancho rápido. O custo de espera produz evasão, e evasão produz portão desativado
- [ ] Tratar a constituição como imutável. Ela precisa evoluir, mas toda alteração é mudança de lei e merece justificativa registrada [3]

**Passo 5 — Visão Geral das 4 Camadas: A Arquitetura Completa**

- [ ] Começar pelas ferramentas porque é a parte visível. A ordem correta de montagem é contexto, harness, motor e ferramentas — nessa sequência
- [ ] Tratar as camadas como hierarquia de importância. Nenhuma é mais importante; cada uma cobre um tipo de falha que as outras não cobrem
- [ ] Configurar governança apenas no ambiente de desenvolvimento. Se o servidor não tem o mesmo disjuntor, o sistema não tem disjuntor
- [ ] Fazer o retorno de falha voltar direto à execução. Repetir ação sem rever decisão é a assinatura do laço de erro que drena orçamento
- [ ] Ampliar ferramentas sem ampliar auditoria. Cada ferramenta nova é uma credencial a mais — trate-a como tal [9]

**Passo 6 — Camada 1 — Contexto e Governança: Densidade, Localidade e Determinismo**

- [ ] Confundir densidade com brevidade. Frase curta e vaga tem menos informação que parágrafo preciso
- [ ] Promover detalhe de módulo para a raiz. Isso dilui as leis que valem para todos no meio de regras que valem para poucos
- [ ] Reordenar a constituição a cada edição. Estabilidade de ordem é o que habilita a economia de prefixo
- [ ] Manter pedido enfático onde caberia portão binário. "Por favor, não faça X" não sobrevive a contexto saturado [3]
- [ ] Guardar credencial no contexto. Regra de segurança que depende de o agente lembrar de não vazar não é regra de segurança

**Passo 7 — Camada 2 — Harness e Ciclo de Vida: Disjuntores, Worktrees e Quality Gates**

- [ ] Desencorajar em vez de impossibilitar. Se pular o portão é possível, alguém vai pular sob pressão — e será justamente no commit que quebra produção
- [ ] Confundir lista de bloqueio longa com segurança. Lista exaustiva não é revisada; lista curta é confiável
- [ ] Deixar diretórios de trabalho órfãos. Ambiente órfão é estado fantasma que confunde o próximo agente
- [ ] Testar a contenção apenas no caminho felizes. Portão precisa ser testado com entrada hostil, senão você não sabe se ele funciona
- [ ] Tratar teto de repetição como detalhe. É o controle que separa um erro barato de uma fatura inesperada [4]

**Passo 8 — Camada 3 — Motor Cognitivo: Roteamento, Contratos Tipados e Economia de Tokens**

- [ ] Usar modelo para cálculo. Cada verificação determinística convertida em script economiza duas vezes: custo e latência
- [ ] Padronizar no modelo mais caro. Você paga raciocínio profundo por triagem mecânica e ainda ganha variação indesejada em tarefa que deveria ser repetível
- [ ] Consumir texto livre no pipeline. Toda extração por expressão regular é dívida acumulada que quebra na primeira mudança de formatação
- [ ] Comprimir contexto sem medir a consequência. Economia e retrabalho sobem juntos quando você corta significado em vez de redundância [10]
- [ ] Confiar em benchmark público como prova de capacidade real. A evidência é contundente: em base de avaliação com dados não vistos, o mesmo modelo que resolve a casa dos 23% numa suíte cai para cerca de 17,8% em outra, e outro caiu de 23,1% para 14,9% [3]. Benchmark mede o que ele mede — e não mede o seu domínio [1]

**Passo 9 — Camada 4 — Ferramentas, MCP e Persistência: A Usina Determinística**

- [ ] Confiar em ferramenta pela descrição. A descrição é texto; o comportamento é código, e os dois podem divergir sem aviso [3]
- [ ] Consumir saída sem validar esquema. Campo inesperado quebra pipeline silenciosamente, e o sintoma aparece longe da causa
- [ ] Conceder escopo de escrita amplo "por conveniência". Conveniência de hoje é incidente de amanhã
- [ ] Escrever ferramenta não idempotente e recuperar falha manualmente. Toda recuperação manual é uma oportunidade de erro sob pressão
- [ ] Tratar o banco de estado como banco de aplicação. Ele guarda decisão e telemetria, com retenção declarada — não dados de negócio [14]

**Passo 10 — Implementação e Réplica das 4 Camadas: O Manual de Montagem**

- [ ] Reescrever em vez de governar. Reescrever troca dívida conhecida por risco desconhecido e consome o cronograma inteiro
- [ ] Começar a montagem pela camada mais visível. A ordem correta é freio, declaração, medição e isolamento — risco decrescente
- [ ] Sobrescrever arquivo que contém decisão humana. Política de sobrescrita mal definida destrói trabalho sem aviso
- [ ] Considerar a montagem pronta porque os arquivos existem. O critério é a auditoria transversal com capacidade operacional, não a presença de pasta
- [ ] Editar configuração de ambiente à mão. Divergência local vira bug silencioso na próxima sincronização [7]

**Passo 11 — Orquestração Cross-Harness: Subagentes, Worktrees e o Protocolo ORCA ADE**

- [ ] Paralelizar antes de planejar. Sem fronteiras declaradas, tarefas "independentes" disputam recursos e o ganho desaparece em reconciliação
- [ ] Usar o diretório de trabalho compartilhado. Sem isolamento físico, a última escrita vence e a intenção se perde [1]
- [ ] Deixar agente rodando sem observação e sem teto. Horizonte longo sem supervisão é onde o desvio de comportamento se instala [7]
- [ ] Não registrar falha. Tarefa que falha e desaparece da contagem distorce a percepção de progresso e esconde o gargalo real
- [ ] Carregar o histórico de todos os lotes adiante. Isso reproduz a saturação de contexto que o protocolo deveria evitar [14]

**Passo 12 — Super-Auditoria e Entrega Soberana: O Certificado de Confiabilidade**

- [ ] Aceitar veredito com ressalvas em requisito bloqueante. Ressalva em requisito é requisito não cumprido com nome diferente
- [ ] Confiar em benchmark público como certificado. A evidência é clara: em conjuntos com casos não publicados, a resolução dos mesmos modelos recua para a casa dos 17% [3]
- [ ] Escrever a verdade sem medi-la. Toda afirmação de cobertura precisa do comando que a produziu; sem isso, ela é hipótese
- [ ] Entregar pacote sem declarar omissões. O que fica de fora em silêncio é indistinguível de esquecimento
- [ ] Não inspecionar o que a leitura não vê. Sobreposição, terminologia e truncamento são invisíveis a olho nu e triviais para o auditor [15]
