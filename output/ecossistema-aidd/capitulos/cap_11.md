# Capítulo 11: Manter vivo depois da instalação

## 1. Introdação

O capítulo anterior mostrou que instalar sem destruir é o ritual que transforma diagnóstico em mecanismo — e que dry-run, explicar, gravar por peça, esperar e regra de colisão são o que orientam o ritmo de instalação. Mas instalar é só o começo — manter as peças vivas depois da instalação é o que transforma mecanismo instalado em propriedade do repo ao longo do tempo. Este capítulo detalha os três sinais de que uma peça virou carga — e o critério de quando o kit pode pular uma peça sem perder coerência [1][2].

Ao final deste capítulo você será capaz de, diante de uma peça instalada, decidir se ela ainda vale a pena — ou se virou carga que exige manutenção sem benefício — e saber quando o kit pode pular peça sem perder a propriedade de coerência do repo.

## 2. Explica

Manter vivo não é manter tudo — é manter o que ainda entrega benefício, e revisar o que parou de entregar. O princípio de peça que virou carga é: custo de manutenção da peça excede benefício de propriedade que a peça entrega — e o critério de revisar é detectar quando o custo subiu ou o benefício desceu [3][4].

Três sinais de carga de peça:

1. **Bypass frequente:** peça que é bypassada frequentemente — porque o time não entende, porque o dry-run não cobrou o impacto real, ou porque a peça gera falso-positivo que o time aprende a ignorar. Bypass frequente é sinal de que a peça não está entregando benefício — o time a ignora, e a propriedade que a peça deveria entregar não está sendo entregue. Se a peça é bypassada por todos, revisar se a peça é necessária — ou se o problema é peça com falso-positivo que precisa de ajuste, não de remoção [5][6].

2. **Falso-positivo acumulado:** peça que gera falso-positivo que o time aprende a ignorar — e o falso-positivo acumulado gera "alerta falso" que murcha o critério de gate. Se o gate gera falso-positivo que o time ignora, o gate não está entregando proteção — está entregando ruído. O critério de ajuste é: reduzir falso-positivo antes de remover — porque falso-positivo é sintoma de gate com critério muito frouxo ou muito restritivo, não de peça desnecessária. Ajustar critério de gate é o que transforma ruído em proteção [1][7].

3. **Manutenção desproporcional:** peça que exige manutenção desproporcional ao benefício — porque critério mudou, porque arquivo de configuração cresceu, porque agente que a peça verifica mudou de comportamento. Se a manutenção da peça é desproporcional ao benefício, revisar se a peça ainda entrega propriedade — ou se a propriedade pode ser entregue por mecanismo mais leve. Reduzir complexidade de peça é o que transforma manutenção desproporcional em manutenção sustentável [2][4].

Critério de quando o kit pode pular peça: o kit pode pular peça quando a peça não tem sintoma (diagnóstico do capítulo 9 mostra sem sintoma) — e quando pular a peça não deixa buraco de coerência que outra peça não cobre. Se peça 4 (hook) é pulada porque repo é pequeno e sem suíte — mas repo tem CI/CD que aplica gate (peça 6) — o buraco de hook local pode ser coberto por gate remoto. Se peça é pulada e nenhuma outra cobre o buraco, pular é perda de propriedade — e o critério de pular é cobertura de buraco por outra peça [3][5].

## 3. Ilustra

Imagine um sistema de manutenção de peças de segurança de um prédio onde cada peça é revisada periodicamente — e revisada para ver se ainda entrega benefício. Peça que gera alerta falso constantemente é peça que o morador ignora — e o morador que ignora alerta falso não é protegido quando o alerta real chega. Em repo, o sinal de alerta falso acumulado é o que orienta o ajuste do gate — porque gate com falso-positivo não entrega proteção, entrega ruído [4][6].

```mermaid
%% legenda: Sinais de carga de peça — quando manter, quando revisar, quando pular
flowchart TD
  A[Peça instalada no repo] --> B{Revisar periodicamente: os 3 sinais de carga?}
  B --> C[Bypass frequente: time ignora peça]
  B --> D[Falso-positivo acumulado: alerta que morre de ouvir]
  B --> E[Manutenção desproporcional: custo > benefício]
  C --> F{Causa de bypass?}
  F -->|time não entende| G[Explicar melhor — educar, não remover]
  F -->|falso-positivo| H[Ajustar critério de gate — reduzir falso-positivo]
  F -->|peça não entrega benefício| I[Revisar se peça é necessária — remover se sem sintoma]
  D --> H
  E --> J{Custo de manutenção > benefício?}
  J -->|sim| K[Revisar se peça pode ser mais leve ou removida]
  J -->|não| L[Manter — benefício justifica custo]
  M[Peça sem sintoma (diagnóstico cap 9)] --> N[Pode pular sem perder coerência]
  N -.-> O[verificar cobertura de buraco por outra peça antes de pular]
  O -.-> P[se buraco não coberto: não pular — instalar ou manter]
```

## 4. Técnica

A técnica de manutenção é: revisar periodicamente cada peça instalada contra os três sinais de carga — e aplicar critério de ajuste, manutenção ou remoção. A técnica também entrega o critério de quando o kit pode pular peça — cobertura de buraco por outra peça [1][5].

### Revisão periódica de peça

Para cada peça instalada, revisar periodicamente:
- [ ] Defina o limite de revisão: revisar peça a cada 90 dias ou quando o repo muda (novo agente, novo incidente, novo colaborador) — revisão mensal é excessivo para repo estável; revisão anual é insuficiente para repo em crescimento.
- [ ] Defina o contorno de revisão: peça que virou carga não deve ser removida na revisão imediatamente — remover só após 2 revisões consecutivas com mesmo sinal de carga (bypass frequente em 2 períodos, ou falso-positivo acumulado em 2 períodos) — porque um período pode ser anomalia.

1. **Bypass frequente:** quantas vezes a peça foi bypassada no último período? Se bypass frequente, investigar causa: time não entende, falso-positivo, ou peça sem benefício. Se causa é não-entendimento, educar — não remover. Se causa é falso-positivo, ajustar critério. Se causa é sem benefício, revisar remoção.

2. **Falso-positivo acumulado:** quantos falso-positivo a peça gerou no último período? Se falso-positivo acumulado, ajustar critério de gate — reduzir falso-positivo antes de remover. Peça com falso-positivo não é peça desnecessária — é peça com critério que precisa de ajuste.

3. **Manutenção desproporcional:** quanto tempo a peça exige de manutenção no último período? Se manutenção desproporcional, revisar se a peça pode ser mais leve (simplificar critério, reduzir arquivos de configuração, migrar para mecanismo mais simples) ou removida.

### Código: revisor de carga de peça (Python)

```python
# revisor_carga_peca.py — detecta os 3 sinais de carga de uma peça instalada
# Critério objetivo: bypass frequente, falso-positivo acumulado, manutenção desproporcional.

import os
import re
import sys
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any
from collections import Counter

@dataclass
class CargaPeça:
    """Carga detectada de uma peça: sinais, magnitude, recomendação."""
    peça: str
    sinais: list[str] = field(default_factory=list)
    magnitude: dict[str, int] = field(default_factory=dict)
    recomendação: str = ""

class RevisorCarga:
    """Detecta sinais de carga de peças instaladas."""

    def __init__(self, caminho_repo: Path) -> None:
        self.repo = caminho_repo
        self.caminhos_py = list(caminho_repo.rglob("*.py")) + list(caminho_repo.rglob("*.js")) + list(caminho_repo.rglob("*.ts"))
        self.caminhos_md = list(caminho_repo.rglob("*.md"))
        self.caminhos_hook = list(caminho_repo.rglob(".git/hooks/pre-commit")) + list(caminho_repo.rglob("*.hook"))
        self.caminhos_ci = list(caminho_repo.rglob(".github/workflows/*.yml")) + list(caminho_repo.rglob(".gitlab-ci.yml"))
        self.caminhos_log = list(caminho_repo.rglob("*.log")) + list(caminho_repo.rglob("*.jsonl"))
        self.caminhos_postmortem = [p for p in self.caminhos_md if "postmortem" in p.name.lower() or "incidente" in p.name.lower()]

    def carga_peca4(self) -> CargaPeça:
        """Peça 4: hook. Sinais: bypass frequente (hook ignorado), falso-positivo acumulado."""
        hooks = [p for p in self.caminhos_hook if p.is_file()]
        sinais: list[str] = []
        magnitude: dict[str, int] = {}
        if not hooks:
            return CargaPeça(
                peça="4: Nunca commitar vermelho",
                sinais=["sem hook instalado — não há carga para revisar"],
                magnitude={},
                recomendação="instalar hook (peça 4) antes de revisar carga",
            )
        for hook in hooks:
            try:
                texto = hook.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            # detecta bypass por "bypass" ou "--no-verify" no hook
            if "bypass" in texto.lower() or "no-verify" in texto.lower():
                sinais.append(f"hook {hook.name} menciona bypass — investigar se bypass é documentado ou não");
            if "TODO" in texto and "fixar" not in texto.lower():
                sinais.append(f"hook {hook.name} tem TODO sem resolver — sinal de manutenção pendente")
        # magnitude de bypass: contar commits com "bypass" no log (se log existir)
        bypasses = 0
        for log in self.caminhos_log:
            try:
                texto = log.read_text(encoding="utf-8", errors="ignore")
                bypasses += len(re.findall(r"bypass|no-verify|skip-hook", texto, re.IGNORECASE))
            except OSError:
                continue
        magnitude["bypass"] = bypasses
        if bypasses > 5:
            sinais.append(f"bypass frequente detectado no log: {bypasses} ocorrências — hook pode não estar entregando benefício")
        if not sinais:
            sinais.append("sem sinal de carga detectável com busca simples — hook parece estar entregando benefício")
        return CargaPeça(
            peça="4: Nunca commitar vermelho",
            sinais=sinais,
            magnitude=magnitude,
            recomendação="se bypass frequente: investigar causa (suíte lenta? falso-positivo? hook não entendeu?) antes de remover; se falso-positivo: ajustar critério, não remover" if bypasses > 5 else "manter — sem sinal de carga",
        )

    def carga_peca2(self) -> CargaPeça:
        """Peça 2: gate. Sinais: falso-positivo acumulado, manutenção desproporcional."""
        gate_scripts = [p for p in self.caminhos_py if "gate" in p.name.lower() or "validar" in p.name.lower()]
        sinais: list[str] = []
        magnitude: dict[str, int] = {}
        if not gate_scripts:
            return CargaPeça(
                peça="2: Gate determinístico",
                sinais=["sem gate instalado — não há carga para revisar"],
                magnitude={},
                recomendação="instalar gate (peça 2) antes de revisar carga",
            )
        for gate in gate_scripts:
            try:
                texto = gate.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if "falso-positivo" in texto.lower() or "falso positivo" in texto.lower():
                sinais.append(f"gate {gate.name} menciona falso-positivo — ajustar critério pode reduzir");
            if "TODO" in texto:
                sinais.append(f"gate {gate.name} tem TODO — sinal de manutenção pendente")
        # falso-positivo: contar em log se gate reportou falha que depois foi revertida
        falsos_positivos = 0
        for log in self.caminhos_log:
            try:
                texto = log.read_text(encoding="utf-8", errors="ignore")
                falsos_positivos += len(re.findall(r"falha.*revertida|revert.*falha|falso-positivo", texto, re.IGNORECASE))
            except OSError:
                continue
        magnitude["falso-positivo"] = falsos_positivos
        if falsos_positivos > 5:
            sinais.append(f"falso-positivo acumulado no log: {falsos_positivos} ocorrências — gate pode ter critério muito restritivo ou muito frouxo")
        if not sinais:
            sinais.append("sem sinal de carga detectável — gate parece estar entregando benefício")
        return CargaPeça(
            peça="2: Gate determinístico",
            sinais=sinais,
            magnitude=magnitude,
            recomendação="se falso-positivo acumulado: ajustar critério de gate (reduzir restrição ou refinar condição) antes de remover; gate com falso-positivo não é gate desnecessário — é gate com critério que precisa de ajuste",
        )

    def carga_peca6(self) -> CargaPeça:
        """Peça 6: CI/CD. Sinais: manutenção desproporcional (pipeline lento, falhas recorrentes)."""
        ci = [p for p in self.caminhos_ci if p.is_file()]
        sinais: list[str] = []
        magnitude: dict[str, int] = {}
        if not ci:
            return CargaPeça(
                peça="6: Hook + CI/CD",
                sinais=["sem CI instalado — não há carga para revisar"],
                magnitude={},
                recomendação="instalar CI (peça 6) antes de revisar carga",
            )
        for c in ci:
            try:
                texto = c.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if "timeout" in texto.lower():
                sinais.append(f"CI {c.name} tem timeout configurado — pipeline pode ser lento");
            if "retry" in texto.lower():
                sinais.append(f"CI {c.name} tem retry — pode indicar flakiness");
        magnitude["timeout"] = len([c for c in ci if "timeout" in c.read_text(encoding="utf-8", errors="ignore").lower()])
        if not sinais:
            sinais.append("sem sinal de carga detectável — CI parece estar entregando benefício")
        return CargaPeça(
            peça="6: Hook + CI/CD",
            sinais=sinais,
            magnitude=magnitude,
            recomendação="se pipeline lento ou flaky: investigar etapas que causam lentidão antes de remover CI; CI é segunda linha de defesa — remover só se substituído por outro mecanismo",
        )

    def revisar(self) -> list[CargaPeça]:
        """Revisa carga de todas as peças instaladas."""
        return [
            self.carga_peca4(),
            self.carga_peca2(),
            self.carga_peca6(),
        ]

def main(caminho: str) -> int:
    repo = Path(caminho)
    if not repo.is_dir():
        print(f"ERRO: {caminho} não é diretório", file=sys.stderr)
        return 2
    revisor = RevisorCarga(repo)
    cargas = revisor.revisar()
    print("REVISÃO DE CARGA DE PEÇAS INSTALADAS")
    print("=" * 50)
    print(f"Repo: {repo}")
    print("AVISO: revisão é informativa — decisão de manter/ajustar/remover é do time\n")
    for carga in cargas:
        print(f"[{carga.peça}]")
        print(f"  Sinais ({len(carga.sinais)}):")
        for sinal in carga.sinais:
            print(f"    - {sinal}")
        print(f"  Magnitude: {carga.magnitude}")
        print(f"  Recomendação: {carga.recomendação}")
        print()
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python revisor_carga_peca.py <caminho-do-repo>", file=sys.stderr)
        sys.exit(2)
    raise SystemExit(main(sys.argv[1]))
```

O revisor de carga entrega os três sinais por peça instalada — e o que orienta a decisão de manter, ajustar ou remover. O revisor é informativo — a decisão é do time com base no contexto de negócio. O revisor periódico é o que transforma instalação em propriedade sustentável [1][4].

### Critério de quando o kit pode pular peça

O kit pode pular peça quando: (1) diagnóstico (cap 9) mostra peça sem sintoma; (2) pular a peça não deixa buraco de coerência que outra peça não cobre. Se peça é pulada e buraco não é coberto, pular é perda de propriedade — e o critério de pular é cobertura de buraco por outra peça. A cobertura de buraco é o que transforma "pular peça" em "pular peça sem perder coerência" — e é o que evita pular peça que o repo ainda precisa [2][7].

Um exemplo de cobertura de buraco: repo pequeno com 3 pessoas, sem suíte de teste (peça 4 — hook — não instalada porque sem suíte). O buraco de hook local pode ser coberto por CI/CD (peça 6) que aplica gate remoto — se repo tem CI/CD. Se repo não tem CI/CD, pular peça 4 deixa buraco de proteção de merge — e peça 4 deve ser instalada quando suíte for instalada. O critério de pular é cobertura de buraco — e a cobertura é decidida pelo diagnóstico e pelo contexto do repo [3][6].

## 5. Aplica

Você instalou gate (peça 2), registro (peça 3), hook (peça 4) no repo. Após três meses, revisão periódica mostra: hook foi bypassado 15 vezes nos últimos 30 dias — e o diagnóstico mostra que o bypass foi porque suíte era lenta e o developer não queria esperar. Causa de bypass não é sem benefício — é suíte lenta. A técnica de manutenção orienta: melhorar performance de suíte antes de remover hook — porque hook é proteção de merge, e remover hook sem resolver causa de bypass é perder proteção [1][4].

Limite de escala do repo: revisão periódica de peça é relevante quando o repo tem mais de 5 colaboradores ou mais de 2 incidentes por trimestre — abaixo disso, a revisão pode ser anual (contorno: repo pequeno estável não precisa de revisão mensal de peça). Contorno de remoção de peça: remover peça só quando a peça não entrega benefício em 2 revisões consecutivas — remover na primeira revisão com sinal de carga é prematuro porque um período pode ser anomalia.

Outro exemplo: gate gerou falso-positivo 20 vezes nos últimos 30 dias — e o time aprendeu a ignorar gate. Falso-positivo acumulado é sinal de que gate com critério muito restritivo ou muito frouxo. A técnica de manutenção orienta: ajustar critério de gate antes de remover — porque gate com falso-positivo não é gate desnecessário, é gate com critério que precisa de ajuste. Reduzir falso-positivo é o que transforma ruído em proteção [5][7].

## 6. Conclusão

Manter vivo depois da instalação é o que transforma mecanismo instalado em propriedade do repo ao longo do tempo — e os três sinais de carga de peça (bypass frequente, falso-positivo acumulado, manutenção desproporcional) são o que orientam a decisão de ajustar, manter ou remover. O critério de quando o kit pode pular peça é cobertura de buraco por outra peça — e é o que evita pular peça que o repo ainda precisa. O próximo livro não é este — é o livro que o leitor escreve depois de aplicar as seis peças ao seu repo. A peça de manutenção é a que transforma instalação em propriedade sustentável — e é a que mais vezes é pulada porque "já instalou, já tá bom" — e é a que cura o repo quando feita com critério [2][3].

## 7. Referências Bibliográficas

[1] MARTIN, R. C. *Agile Software Development: Principles, Patterns, and Practices*. Boston: Prentice Hall, 2002. ISBN 978-0135974543.

[2] MARTIN, R. C. *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. 1. ed. Boston: Pearson, 2017. ISBN 978-0134434403.

[3] MYERS, G. J. *The Art of Software Testing*. 2. ed. Hoboken: John Wiley & Sons, 2011. ISBN 978-0470404152.

[4] FOWLER, M. *Continuous Integration*. 2001. Disponível em: https://martinfowler.com/articles/continuousIntegration.html. Acesso em: 09 set. 2026.

[5] GOOGLE SRE. *Testing Release and Deployment*. In: *Site Reliability Engineering*. Disponível em: https://sre.google/sre-book/testing-releases/. Acesso em: 09 set. 2026.

[6] BROWN, S.; BEYER, B.; et al. *Site Reliability Engineering: How Google Runs Production Systems*. Sebastopol: O'Reilly Media, 2016. ISBN 978-1491929124.

[7] HUMBLE, J.; FARLEY, D. *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Boston: Addison-Wesley, 2010. ISBN 978-0321601945.
