# Capítulo 6: Peça 4: Nunca commitar vermelho

## 1. Introdução

O capítulo anterior mostrou que a peça 3 centraliza critério em registro — e que tipo novo de configuração de agente = 1 entrada no dicionário, sem editar múltiplos arquivos de dispatch. Mas centralizar critério não garante que ele seja aplicado antes do commit — pode existir registro e gate, e o developer ainda mergear com suíte vermelha porque "o hook é opcional" ou "vai passar depois". Este capítulo entra na peça 4: nunca commitar vermelho — o hook de pre-commit que bloqueia quando a suíte de teste fala não, sem depender de promessa de "vamos revisar depois" [1][2].

Ao final deste capítulo você será capaz de, diante de um pre-commit existente, revisá-lo para ver se ele realmente bloqueia o commit vermelho — e escrever o marcador de bloco que faz o hook falhar de forma determinística quando o critério não é atendido.

## 2. Explica

" Nunca commitar vermelho" é a frase que o time repete — e a que mais falha em repo sem mecanismo. O problema não é a intenção — é que "nunca" expressa uma promessa textual, não um mecanismo que impede. Promessa de "não commitar vermelho" sem hook que bloqueia quando a suíte fala não é peça 4 — é peça do capítulo 1: promessa que depende da vontade humana [3][4].

A peça 4 transforma a promessa em mecanismo: hook de pre-commit que roda a suíte de teste (ou o critério relevante) e bloqueia o commit quando o resultado não é verde — não avisa, não pede confirmação, não deixa passar com "lembrete". Bloqueia. O bloqueio é o que transforma "lembrete" em "lei do repo" [5][6].

Dois detalhes de implementação que distinguem peça 4 de hook amadora. Primeiro: marcador de bloco — o hook deve ter critério objetivo de falha, e falhar de forma determinística (código de saída não-zero, mensagem de motivo rastreável). Segundo: regra append — quando um developer revisar um pre-commit existente para adicionar uma verificação nova, a regra é adicionar ao final, não substituir o corpo. Substituir o corpo apaga a verificação anterior — e o developer que não conhece o hook a priori não percebe que perdeu a proteção [1][7].

Um erro comum: hook que roda "teste" mas não roda a suíte completa — roda apenas lints leves, ou roda em modo skip por padrão. O hook que não roda a suíte completa não é peça 4 — é hook de conforto. O critério de peça 4 é: hook que, quando a suíte fala não, impede o commit. Se o hook permite commit com suíte vermelha porque "o desenvolvedor sabe o que faz", o hook não está cumprindo a peça 4 [2][4].

Métrica deste capítulo: número de linhas do hook analisado no exercício — porque revisar o hook é o que detecta se o "nunca commitar vermelho" é mecanismo ou promessa.

## 3. Ilustra

Imagine um portão de segurança de uma entrada onde o aviso diz "não entre com mochila". O aviso existe — é texto. Mas o portão não impede; a pessoa que tem mochila passa porque o portão não bloqueia. Substituir o aviso por um sensor que detecta mochila e bloqueia a passagem muda a propriedade do portão: ninguém mais precisa ser lembrado. Em repo, o hook que bloqueia é o sensor — e a suíte de teste é o critério que o sensor verifica [5][6].

```mermaid
%% legenda: Hook de pre-commit que bloqueia — sensor que aplica o critério antes do commit
flowchart TD
  A[Developer faz commit] --> B[Pre-commit hook é disparado]
  B --> C{Hook roda suíte/teste?}
  C -->|não| D[Hook não é peça 4\né hook de conforto — promessa]
  C -->|sim| E{Suíte verde?}
  E -->|sim| F[Comit é permitido\nsuíte verde — sem vermelho no repo]
  E -->|não| G[Hook bloqueia commit\nmensagem de motivo rastreável — sem avisar]
  G --> H[Developer corrige ou investiga\nsem merge de vermelho]
  D -.-> I[repo com promessa de "nunca vermelho"\nmás sem mecanismo — capítulo 1]
```

## 4. Técnica

A técnica da peça 4 é: escrever hook de pre-commit que roda o critério relevante (suíte de teste, gate, lint) e bloqueia com código de saída não-zero quando o critério não é atendido — e revisar hook existente para verificar se ele realmente bloqueia, não apenas avisa.

### Código: hook de pre-commit minimal (Python)

```python
#!/usr/bin/env python3
# pre_commit_hook.py — hook de pre-commit que roda suíte de teste e bloqueia se vermelha
# Instalar em .git/hooks/pre-commit (executável + shebang correto).
# Critério objetivo: código de saída 0 = verde, código não-zero = bloqueia commit.

import os
import subprocess
import sys
from pathlib import Path

# ── Configuração do repo (declarar aqui ou ler de registro — peça 3) ─────

SUITE_CMD = ["pytest", "-q", "--no-header", "-p", "no:cacheprovider"]
# Adaptar ao comando real de suíte do repo. Se repo não usa pytest, substituir.
# O comando deve retornar:
#   código 0  -> suíte passou (verde)
#   código não-zero -> suíte falhou (vermelha)
# O hook não decide "passou com verdades" — ele reporta o código de saída do comando.

# ── Hook de pre-commit ────────────────────────────────────────────────────

def rodar_suíte() -> tuple[int, str]:
    """Roda a suíte de teste e retorna (código de saída, stdout+stderr truncado).
    Código de saída 0 = verde, não-zero = vermelha.
    """
    try:
        result = subprocess.run(
            SUITE_CMD,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutos — ajustar ao tempo real da suíte
        )
        saida = (result.stdout + result.stderr).strip()
        # Truncar para não gerar commit message enorme se a suíte tiver saída grande
        if len(saida) > 4000:
            saida = saida[:2000] + "\n... [truncado por limite do hook] ..." + saida[-2000:]
        return (result.returncode, saida)
    except subprocess.TimeoutExpired:
        return (124, "SUÍTE TIMEOUT — bloqueando commit (ajustar timeout ou dividir suíte)")
    except FileNotFoundError:
        return (127, f"comando '{SUITE_CMD[0]}' não encontrado — instalar suíte ou ajustar SUITE_CMD")

def main() -> int:
    repo = Path(os.environ.get("GIT_PREFIX", ".")).resolve()
    print(f"[# pre-commit] rodando suíte em {repo}")
    codigo, saida = rodar_suíte()
    if codigo == 0:
        print("[# pre-commit] suíte verde — commit permitido")
        return 0
    else:
        print(f"[# pre-commit] SUÍTE VERMELHA (código {codigo}) — commit BLOQUEADO")
        if saida:
            print("--- saída da suíte ---")
            print(saida)
            print("--- fim da saída ---")
        print("""
[# pre-commit] Motivo do bloqueio: suíte de teste não passou.
[# pre-commit] Para desbloquear:
[# pre-commit]   1. Corrija o teste que falhou (ou o código que ele detectou)
[# pre-commit]   2. Ou, se o falha é conhecidamente flaky, investigue e documente o flaky
[# pre-commit]      antes de bypassar — nunca bypassar sem diagnóstico rastreável.
[# pre-commit] Nunca commitar vermelho. (Peça 4)
""")
        return 1  # código não-zero -> git bloqueia o commit

if __name__ == "__main__":
    raise SystemExit(main())
```

O padrão que o hook minimal entrega: roda a suíte, reporta código de saída, bloqueia quando não-zero, mensagem de motivo rastreável. O hook não decide "o que está errado" — ele reporta a saída da suíte e bloqueia. O diagnosis do que corrigir é função da suíte, não do hook [3][5].

### Marcador de bloco

O marcador de bloco é o critério objetivo de falha — o que faz o hook retornar código não-zero. No hook minimal acima, o marcador é o código de saída da suíte. Em hook que verificam múltiplos critérios (lints, format, gate), o marcador é: qualquer critério falha = bloqueia. O marcador não é "lembrete" — é falha determinística [6][7].

```python
# marcador_bloqueio.py — exemplo de critérios de bloqueio acumulativos
# Cada critério é uma condição objetiva; se qualquer uma falha, o hook bloqueia.

import os
import re
import subprocess
import sys
from pathlib import Path

class CritérioBloqueio:
    """Critério de bloqueio com nome, comando/condição, e mensagem de falha."""
    def __init__(self, nome: str, comando: list[str] | None = None, condicao=None) -> None:
        self.nome = nome
        self.comando = comando
        self.condicao = condicao

    def verificar(self) -> tuple[bool, str]:
        """Retorna (passou, mensagem). True = não bloqueia; False = bloqueia."""
        if self.condicao is not None:
            try:
                resultado = self.condicao()
                if isinstance(resultado, tuple):
                    passou, msg = resultado
                else:
                    passou, msg = bool(resultado), ""
                if passou:
                    return (True, f"{self.nome}: OK")
                return (False, f"{self.nome}: {msg}")
            except Exception as e:
                return (False, f"{self.nome}: erro ao verificar — {e}")
        if self.comando:
            try:
                result = subprocess.run(
                    self.comando,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.returncode == 0:
                    return (True, f"{self.nome}: OK")
                msg = (result.stdout + result.stderr).strip()
                if len(msg) > 1500:
                    msg = msg[:750] + " ... [truncado] ... " + msg[-750:]
                return (False, f"{self.nome}: falhou (código {result.returncode}) — {msg}")
            except subprocess.TimeoutExpired:
                return (False, f"{self.nome}: timeout")
            except FileNotFoundError:
                return (False, f"{self.nome}: comando não encontrado")
        return (False, f"{self.nome}: sem implementação")

# ── Exemplo de critérios de bloqueio ─────────────────────────────────────

CRITÉRIOS_BLOQUEIO = [
    CritérioBloqueio(
        nome="suíte de teste",
        comando=["pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
    ),
    CritérioBloqueio(
        nome="formatação",
        comando=["ruff", "format", "--check", "."],
    ),
    CritérioBloqueio(
        nome="lint",
        comando=["ruff", "check", "."],
    ),
    CritérioBloqueio(
        nome="arquivos não commitados com 'TODO' sem issue",
        condicao=lambda: (
            False,
            "arquivo com TODO sem referência de issue — use TODO(#1234) ou issue.track"
        ) if any(
            "TODO" in line and not re.search(r"TODO\s*\(#\d+\)", line)
            for line in Path(".").read_text(encoding="utf-8", errors="ignore").splitlines()
        ) else (True, "OK"),
    ),
]

def main() -> int:
    falhas = []
    for criterio in CRITÉRIOS_BLOQUEIO:
        passou, msg = criterio.verificar()
        if passou:
            print(f"[OK] {msg}")
        else:
            print(f"[FALHA] {msg}")
            falhas.append(msg)
    if falhas:
        print(f"\n[# pre-commit] {len(falhas)} critério/io(rio)s de bloqueio falharam — commit BLOQUEADO")
        for f in falhas:
            print(f"  - {f}")
        return 1
    print("\n[# pre-commit] todos os critérios passaram — commit permitido")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

A propriedade que o marcador de bloco entrega: o hook não decide por opinião — decide por critério acumulativo de condições objetivas. Se ruff falha, se pytest falha, se TODO sem issue aparece — bloqueia. O developer não precisa "concordar" com o bloqueio; o hook aplica critério objetivo [1][4].

### Regra append ao revisar pre-commit existente

Quando um developer revisar um pre-commit existente para adicionar uma verificação nova, a regra é: adicionar ao final da lista de critérios, não substituir o corpo do hook. Substituir o corpo apaga as verificações anteriores — e o developer que não conhece o hook a priori não percebe que perdeu a proteção.

```bash
# Exemplo de revisão correta de pre-commit existente:
# ANTES (hook com pytest e ruff):
#   CRITÉRIOS_BLOQUEIO = [CritérioBloqueio("suíte", ["pytest"...]), CritérioBloqueio("format", ["ruff"...])]
# DEPOIS (adicionar gate de configuração — append, não substituir):
#   CRITÉRIOS_BLOQUEIO = [
#       CritérioBloqueio("suíte", ["pytest"...])=,
#       CritérioBloqueio("format", ["ruff"...])==,
#       CritérioBloqueio("config-valida", ["python", "gate_lendo_registro.py", "config.yaml"]),
#   ]
```

A regra append é inegociável porque o pre-commit é peça de proteção do repo — não script de conforto que pode ser reescrito sem consequência. Reescrever o corpo sem manter as verificações anteriores é apagar proteção sem registrar que apagou — e o próximo developer não sabe que perdeu [2][7].

## 5. Aplica

Você entra em um repo onde o README diz "nunca commitar vermelho" e o .git/hooks/pre-commit existe — mas o hook roda apenas ruff format --check, não roda pytest. O developer que comete e mergea com suíte vermelha não é bloqueado — porque o hook que existe é hook de conforto, não peça 4. Revisar o hook é o diagnóstico: quantas linhas ele tem, quais critérios ele verifica, e ele bloqueia quando a suíte fala não? [3][5].

Um cenário real de instituição: repo com hook existente que roda pytest mas sem bloqueio (código de saída ignorado). O diagnóstico mostra que o hook roda a suíte — mas ignora o código de saída, deixa o commit passar. A correção é fazer o hook retornar o código de saída da suíte — o que transforma o hook de conforto em peça 4. O trabalho é mínimo — uma linha — mas é a linha que transforma promessa em mecanismo [6][7].

Escala: em repo com múltiplos desenvolvedores e múltiplos agentes, o hook de pre-commit é a primeira linha de defesa contra vermelho no repo local — e o CI/CD (peça 6) é a segunda linha de defesa remota. Sem a primeira linha local, a segunda linha remota recebe vermelho no pipeline — e o pipeline fica vermelho, o que gera custo de investigação para todos. Com a primeira linha local, o vermelho é detectado antes do commit — e o developer corrige no contexto, sem poluir o pipeline [1][4].

### Exercício

- [ ] Liste os arquivos de hook de pre-commit do seu repo (.git/hooks/pre-commit, ou framework de hook equivalente).
- [ ] Defina o limite de hook: hook de bloqueio deve rodar em até 2 minutos no máquina do developer (limite prático para não tornar commit inviável) — se a suíte ultrapassa 2 minutos, dividir em suíte de commit rápida + suíte completa no CI (peça 6).
- [ ] Defina o contorno de hook: hook de bloqueio não deve bloquear commit de rascunho ou feature branch isolada — bloqueia na tentativa de push/merge para branch principal (main/develop).
- [ ] Para cada hook, conte quantas linhas ele tem e quais critérios ele verifica (grep por comandos, condições).
- [ ] Para cada critério, decida se ele realmente bloqueia (código de saída não-zero quando falha) ou apenas avisa.
- [ ] Para os critérios que apenas avisa, descreva em uma linha como transformar em bloqueio (código de saída, mensagem de motivo).
- [ ] Para o hook existente, revise se ele segue a regra append — se uma nova verificação for adicionada, onde ela vai ser adicionada (final da lista, não substituição do corpo).
- [ ] Comite o relatório de revisão do hook — porque o diagnóstico do hook é o que justifica instalar ou corrigir a peça 4.

## 6. Conclusão

A peça 4 é nunca commitar vermelho — o hook de pre-commit que bloqueia quando a suíte de teste fala não, sem depender de promessa de "vamos revisar depois". A peça não propõe hook para tudo — propõe hook que aplica critério de bloqueio determinístico ( código de saída não-zero, mensagem de motivo rastreável) e segue a regra append quando revisado. O diagnóstico de peça 4 é revisar o hook existente para detectar se ele realmente bloqueia — e o exercício entrega o mapeamento de critérios de bloqueio do repo. Os próximos capítulos detalham as outras peças: postmortem que vira teste (cap 7); hook + CI/CD (cap 8). A peça 4 é a linha de defesa local — sem ela, vermelho chega ao pipeline remoto e gera custo de investigação para todos [2][3].

## 7. Referências Bibliográficas

[1] MARTIN, R. C. *Agile Software Development: Principles, Patterns, and Practices*. Boston: Prentice Hall, 2002. ISBN 978-0135974543.

[2] MARTIN, R. C. *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. 1. ed. Boston: Pearson, 2017. ISBN 978-0134434403.

[3] CHACON, S.; STRAUB, B. *Pro Git*. 2. ed. Apress, 2014. Disponível em: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks. Acesso em: 09 set. 2026.

[4] MYERS, G. J. *The Art of Software Testing*. 2. ed. Hoboken: John Wiley & Sons, 2011. ISBN 978-0470404152.

[5] FOWLER, M. *Continuous Integration*. 2001. Disponível em: https://martinfowler.com/articles/continuousIntegration.html. Acesso em: 09 set. 2026.

[6] GOOGLE SRE. *Testing Release and Deployment*. In: *Site Reliability Engineering*. Disponível em: https://sre.google/sre-book/testing-releases/. Acesso em: 09 set. 2026.

[7] HUMBLE, J.; FARLEY, D. *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Boston: Addison-Wesley, 2010. ISBN 978-0321601945.
