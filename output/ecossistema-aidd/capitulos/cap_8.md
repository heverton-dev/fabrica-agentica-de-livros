# Capítulo 8: Peça 6: Hook + CI/CD

## 1. Introdução

O capítulo anterior mostrou que a peça 5 transforma postmortem em memória mecânica — e que o repo avisa quando o mesmo problema tenta voltar. Mas a peça 5 previne recorrência a partir de incidente que já aconteceu; há um tipo de risco que ela não cobre: mudança que entra no repo sem passar pelo mecanismo local, porque o developer bypassou o hook ou o hook não existia. Este capítulo entra na peça 6: hook + CI/CD — dois pontos de aplicação do mesmo gate, local antes do commit e remoto antes do merge, complementando, não duplicando [1][2].

Ao final deste capítulo você será capaz de, diante de um repo com gate local (peça 4) e sem CI/CD, escrever o workflow mínimo que aplica o mesmo gate no ambiente remoto — e saber quando o CI/CD é redundante em relação ao hook local.

## 2. Explica

A peça 6 é a extensão da peça 4 para o ambiente remoto: o mesmo gate que bloqueia o commit local também é aplicado no pipeline de CI — mas os dois pontos têm função complementar, não idêntica. O hook local detecta vermelho antes do commit, no contexto do developer — e o CI remoto detecta vermelho que o hook local não capturou (porque o developer bypassou, porque o hook não roda em todas as condições, porque o ambiente do CI difere do local) [3][4].

A distinção entre complementar e duplicar é central. Dois pontos de aplicação do mesmo gate são complementares quando cada um cobre um cenário que o outro não cobre. São duplicados quando ambos cobrem exatamente o mesmo cenário — e nesse caso, um dos dois é custo sem benefício. O critério de peça 6 é: hook local para detecção antes do commit (contexto do developer); CI/CD para detecção remota (contexto do merge e de ambientes diferentes) — e o gate em ambos deve ser o mesmo critério, para que o comportamento seja consistente [5][6].

Um erro comum: CI/CD que roda testes mas não bloqueia merge (apenas reporta). O CI que reporta mas não bloqueia é, no limite, o mesmo que o hook de conforto do capítulo 6 — reporta, não impede. O critério de peça 6 é que o CI/CJ bloqueie merge quando o gate decide não — não avise, não permita o merge com vermelho no pipeline [1][7].

Um outro erro: CI/CD que roda critérios diferentes do hook local. Se o hook local verifica formato e lint, e o CI verifica apenas suíte de teste, o desenvolvedor pode bypassar o hook local (lints leves) e o CI detecta só no merge — com atraso e com custo de investigação. O critério de consistência de gate é: o mesmo critério, nos dois pontos — para que o developer saiba que o que não passa localmente não passará remotamente [2][4].

Métrica deste capítulo: número de etapas do pipeline definidas no exercício — porque as etapas são o que definem o que o CI/CD aplica, e definir é o que torna o pipeline auditável.

## 3. Ilustra

Imagine um portão de segurança de uma entrada física onde o sensor local detecta mochila na entrada — e o sensor remoto no checkpoint de saída detecta mochila que passou pelo local (porque o local falhou ou foi bypassado). Os dois sensores são complementares: o local para a maioria dos casos; o remoto captura o que o local perdeu. Em repo, o hook local é o sensor local — e o CI/CD é o sensor remoto — e o mesmo critério de detecção aplica em ambos [3][6].

```mermaid
%% legenda: Hook local + CI/CD remoto — dois pontos de aplicação do mesmo gate
flowchart TD
  A[Developer modifica código] --> B[Hook local (pre-commit) roda gate]
  B --> C{Commit local permitido?}
  C -->|sim (verde)| D[Commit local — código entra no repo local]
  C -->|não (vermelho)| E[Bloqueio local — developer corrige]
  D --> F[Push para remoto]
  F --> G[CI/CD remoto roda mesmo gate]
  G --> H{O gate remoto decide verde?}
  H -->|sim| I[Merge permitido — gate consistente local e remoto]
  H -->|não| J[Bloqueio remoto — merge bloqueado — mesmo critério do local]
  I -.-> K[gate complementar: local detecta antes do commit;\nremoto detecta se local falhou ou bypassado]
  G -.-> K
  E -.-> L[hook de conforto (cap 6): avisa mas não bloqueia — peça 4 não cumprida]
  J -.-> M[CI que reporta mas não bloqueia — peça 6 não cumprida]
```

## 4. Técnica

A técnica da peça 6 é: definir o pipeline mínimo com as etapas que aplicam o mesmo gate do hook local — e garantir que o pipeline bloqueia merge quando o gate decide não. O pipeline mínimo não é pipeline grande — é pipeline com as etapas que cobrem o cenário que o hook local não cobre [1][5].

### Exemplo mínimo de workflow CI (GitHub Actions)

```yaml
# .github/workflows/ci-gate.yml — pipeline mínimo de gate remoto
# Aplica o mesmo critério do hook local (peça 4) em ambiente remoto.
# Bloqueia merge quando o gate decide não — não reporta apenas.

name: CI Gate — mesma verificação do pre-commit local

on:
  pull_request:
    branches: [main]
    paths-ignore:
      - "**.md"
      - ".github/**"

# Cancelar execuções redundantes se novo commit entrar no PR
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout do code
        uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install .[dev] 2>/dev/null || pip install pytest ruff
        # Se o repo tiver setup.py/pyproject.toml com dependências de dev, usar .
        # Caso contrário, instalar pytest e ruff manualmente como fallback mínimo.

      - name: Formatação (ruff format — mesmo critério do hook local)
        run: ruff format --check .
        # Falha se houver formatação pendente — mesmo critério do pre-commit.

      - name: Lint (ruff check — mesmo critério do hook local)
        run: ruff check .
        # Falha se houver lint — mesmo critério do pre-commit.

      - name: Suíte de teste (pytest — mesmo critério do hook local)
        run: pytest -q --no-header -p no:cacheprovider
        # Falha se algum teste falhar — mesmo critério do pre-commit.
        # Código de saída determinístico: 0 = verde, não-zero = vermelho.

      - name: Gate de configuração (lê registro — peça 3 + peça 2)
        run: python gate_lendo_registro.py config.yaml
        # Falha se configuração não passar no gate — mesmo critério do pre-commit.
        # Adicionar aqui outros arquivos de configuração que o repo usa.
```

O padrão que o workflow mínimo entrega: as mesmas etapas do hook local — formatação, lint, suíte de teste, gate de configuração — aplicadas no ambiente remoto. O critério é o mesmo — e o pipeline falha com código de saída não-zero quando qualquer etapa falha, bloqueando merge automaticamente [2][7].

### Por que não duplicar

O critério de não duplicação é: cada etapa do pipeline cobre um cenário que o hook local não cobre. Hook local cobre: commit local, contexto do developer. Pipeline remoto cobre: merge, ambiente diferente, push de developer que bypassou o hook local, agente remoto que não tem hook local. Se o pipeline remoto rodasse exatamente o que o hook local já roda — e o hook local já bloqueia — o pipeline seria redundante em relação ao hook. Mas o pipeline não é redundante porque cobre o cenário do merge e do ambiente remoto — cenários que o hook local não cobre [3][4].

Um exemplo de duplicação a evitar: hook local roda "pytest -q" e pipeline roda "pytest -q" e mais nada — e o hook local já bloqueia commit vermelha. Nesse caso, o pipeline está duplicando o hook local sem cobrir novo cenário. O pipeline em essa situação deve cobrir ao menos a etapa de merge (verificar que o commit que vai ser mergeado passou pelo hook local) ou ambiente diferente (rodar em ubuntu quando o developer usa Windows, para detectar problema de ambiente) [5][6].

### Código: verificador de consistência de gate local/remoto

```python
# consistencia_gate.py — verifica se o gate local e remoto aplicam o mesmo critério
# Critério objetivo: compara os comandos dos arquivos de hook local e do workflow CI.
# Não decide por opinião — reporta diferenças de comandos para investigação.

import os
import re
import sys
from pathlib import Path

def extrair_comandos_hook_local(caminho_hook: Path) -> list[str]:
    """Extrai comandos de hook local (bash ou Python) por leitura de texto.
    Simplificação: busca linhas que parecem comandos (começam com comando conhecido).
    Para análise precisa, adaptar para parser de shell ou AST do hook.
    """
    if not caminho_hook.exists():
        return []
    comandos: list[str] = []
    try:
        texto = caminho_hook.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        # Comandos conhecidos do hook de exemplo
        if any(linha.startswith(cmd) for cmd in ("pytest", "ruff", "python", "node", "npm", "yarn")):
            comandos.append(linha)
    return comandos

def extrair_comandos_ci(caminho_workflow: Path) -> list[str]:
    """Extrai comandos de workflow CI (yaml) por leitura de texto.
    Simplificação: busca linhas 'run:' e captura comando na linha seguinte.
    Para análise precisa, adaptar para parser de YAML.
    """
    if not caminho_workflow.exists():
        return []
    comandos: list[str] = []
    try:
        texto = caminho_workflow.read_text(encoding="utf-8")
    except OSError:
        return []
    linhas = texto.splitlines()
    for i, linha in enumerate(linhas):
        if linha.strip() == "run:" and i + 1 < len(linhas):
            proxima = linhas[i + 1].strip()
            if proxima and not proxima.startswith("#"):
                comandos.append(proxima)
    return comandos

def comparar_comandos(comandos_local: list[str], comandos_ci: list[str]) -> list[str]:
    """Compara comandos do hook local e do CI — reporta diferenças.
    Simplificação: match por substring do comando base (primeiro token).
    """
    def base(cmd: str) -> str:
        primeiro = cmd.split()[0] if cmd.split() else ""
        return primeiro
    bases_local = {base(c) for c in comandos_local}
    bases_ci = {base(c) for c in comandos_ci}
    diferenças: list[str] = []
    sobrando_no_ci = bases_ci - bases_local
    sobrando_no_local = bases_local - bases_ci
    if sobrando_no_ci:
        diferenças.append(f"CI tem comando que local não tem: {', '.join(sorted(sobrando_no_ci))}")
    if sobrando_no_local:
        diferenças.append(f"Local tem comando que CI não tem: {', '.join(sorted(sobrando_no_local))}")
    return diferenças

def main(hook: str, workflow: str) -> int:
    hp = Path(hook)
    wp = Path(workflow)
    comandos_local = extrair_comandos_hook_local(hp)
    comandos_ci = extrair_comandos_ci(wp)
    print(f"Hook local: {hp} ({len(comandos_local)} comando(s))")
    for c in comandos_local:
        print(f"  - {c}")
    print(f"CI workflow: {wp} ({len(comandos_ci)} comando(s))")
    for c in comandos_ci:
        print(f"  - {c}")
    diferenças = comparar_comandos(comandos_local, comandos_ci)
    if diferenças:
        print("\nAVISO: diferenças de critério entre hook local e CI — investigar consistência do gate:")
        for d in diferenças:
            print(f"  - {d}")
        return 1
    print("\nOK: hook local e CI aplicam os mesmos comandos base — consistência de gate verificada.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python consistencia_gate.py <caminho-do-hook-local> <caminho-do-workflow-ci>", file=sys.stderr)
        sys.exit(2)
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
```

A propriedade que o verificador de consistência entrega: o repo sabe se o gate local e remoto aplicam o mesmo critério — e, se não, investiga a diferença antes que ela gere comportamento surpresa no merge. O verificador não decide se a diferença é legítima — reporta para investigação humana [1][7].

## 5. Aplica

Você entra em um repo com hook local de peça 4 (bloqueia commit vermelha) e sem CI/CD. O diagnóstico de peça 6 pergunta: o que o CI/CD deve cobrir que o hook local não cobre? Cenários: merge de developer que bypassou o hook local (push forçado ou clone sem hook); ambiente diferente (developer Windows, CI Ubuntu — detectar diferença de formatação); agente remoto que não tem hook local (agente de IA que empurra sem passar pelo pre-commit) [2][5].

Um cenário real de instituição: repo com hook local e pipeline remoto que roda pytest mas não lint e não formatação — e o hook local roda pytest, lint e formatação. O verificador de consistência mostra que o CI está rodando menos que o local — e o time adiciona lint e formatação ao CI para consistência. O trabalho é mínimo — adicionar duas etapas — mas é o que garante que o gate remoto é o mesmo que o local [3][6].

Escala: em repo com múltiplos agentes e múltiplos desarrolladores, o CI/CD é a segunda linha de defesa que captura o que o hook local não capturou — e o critério de consistência de gate é o que garante que o merge remoto não introduce vermelho que o local deixou passar. Sem consistência de gate, o developer descobre no merge que algo que passou localmente falhou remotamente — e o custo de investigação é pago por todos que esperam o merge [1][7].

### Exercício

- [ ] Liste os arquivos de hook local do seu repo (ou framework equivalente de hook).
- [ ] Defina o limite de pipeline: pipeline de gate deve ter no mínimo 3 etapas (formatação/lint, suíte de teste, gate de configuração) e no máximo 10 etapas para manter tempo de execução abaixo de 10 minutos (limite prático para não tornar merge lento).
- [ ] Defina o contorno de pipeline: pipeline não deve rodar critérios que já são verificados pelo hook local com resultado idêntico (evitar duplicação); critérios que o local não cobre (ambiente diferente, merge de developer que bypassou) são o que justificam o pipeline remoto.
- [ ] Liste os arquivos de workflow CI/CD do seu repo (ou CI equivalente).
- [ ] Para cada um, liste os comandos/etapas que rodam (grep por comandos).
- [ ] Rode o verificador de consistência de gate para detectar diferenças entre hook local e CI.
- [ ] Para cada diferença, decida se é legítima (cenário que o local não cobre) ou redundante (mesmo comando nos dois, ou CI com menos que o local).
- [ ] Para as missing no CI, adicione ao workflow mínimo — para cobrir cenário que o local não cobre.
- [ ] Comite o relatório de consistência de gate — porque o relatório é o que justifica quais etapas o CI cobre e quais o local cobre.

## 6. Conclusão

A peça 6 é hook + CI/CD — dois pontos de aplicação do mesmo gate, local antes do commit e remoto antes do merge, complementando, não duplicando. A peça não propõe CI/CD para tudo — propõe CI/CD que aplica o mesmo critério do hook local em cenários que o local não cobre (merge, ambiente diferente, bypass). O workflow mínimo deste capítulo entrega as etapas do gate remoto — e o verificador de consistência mostra se o local e remoto aplicam o mesmo critério. Os próximos capítulos detalham a aplicação do kit no repo: diagnóstico antes de instalar (cap 9), instalar sem destruir (cap 10), manter vivo depois da instalação (cap 11). A peça 6 é a linha de defesa remota — e a consistência com o local é o que garante que o merge não introduz vermelho que o local deixou passar [2][4].

## 7. Referências Bibliográficas

[1] MARTIN, R. C. *Agile Software Development: Principles, Patterns, and Practices*. Boston: Prentice Hall, 2002. ISBN 978-0135974543.

[2] MARTIN, R. C. *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. 1. ed. Boston: Pearson, 2017. ISBN 978-0134434403.

[3] FOWLER, M. *Continuous Integration*. 2001. Disponível em: https://martinfowler.com/articles/continuousIntegration.html. Acesso em: 09 set. 2026.

[4] GOOGLE SRE. *Testing Release and Deployment*. In: *Site Reliability Engineering*. Disponível em: https://sre.google/sre-book/testing-releases/. Acesso em: 09 set. 2026.

[5] HUMBLE, J.; FARLEY, D. *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Boston: Addison-Wesley, 2010. ISBN 978-0321601945.

[6] BROWN, S.; BEYER, B.; et al. *Site Reliability Engineering: How Google Runs Production Systems*. Sebastopol: O'Reilly Media, 2016. ISBN 978-1491929124.

[7] CHACON, S.; STRAUB, B. *Pro Git*. 2. ed. Apress, 2014. Disponível em: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks. Acesso em: 09 set. 2026.
