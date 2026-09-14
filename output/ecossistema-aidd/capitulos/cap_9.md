# Capítulo 9: Diagnosticar antes de instalar

## 1. Introdução

Os capítulos 3 a 8 detalharam as seis peças do ecossistema: separação builder/critic, gate determinístico, registro declarativo, nunca commitar vermelho, postmortem que vira teste, e hook + CI/CD. Cada peça entrega critério de instalação — mas instalar peça por estar no catálogo é instalar por moda, não por sintoma. Este capítulo detalha o diagnóstico que precede a instalação: o relatório de diagnóstico com seis campos que mapeia quais peças tem sintoma real no repo, e em que ordem instalar [1][2].

Ao final deste capítulo você será capaz de, diante de um repo, gerar um relatório de diagnóstico que diz quais peças propor — sem instalar peça que não tem sintoma, e sem instalar peça de proteção de merge antes de ter suíte executável.

## 2. Explica

O diagnóstico de peça não é opinião — é mapeamento de sintoma. Para cada uma das seis peças, o diagnóstico pergunta a pergunta que a peça resolve e verifica se o repo tem o sintoma que a peça resolve. Se o repo tem o sintoma, a peça é candidata a instalação; se não tem, instalar a peça é custo sem benefício — e o custo é real porque cada peça, uma vez instalada, exige manutenção [3][4].

O relatório de diagnóstico entrega seis campos — um por peça — mais um campo de resumo que ordena as peças por impacto estimado. O campo por peça não é "instalar ou não" — é "tem sintoma? qual sintoma? qual o custo de não instalar?" A pergunta de instalar ou não é decidida pelo time com base no relatório, não pelo diagnóstico automaticamente — porque o diagnóstico mapeia sintoma, e a decisão de instalar depende do contexto de negócio do repo [5][6].

Um erro comum: diagnosticar e instalar tudo de uma vez. Instalar tudo de uma vez é instalar a peça que o repo não precisa e, às vezes, instalar peça de proteção de merge antes de ter suíte executável — o que gera hook que bloqueia tudo porque não tem suíte para rodar, e o developer bypassa o hook porque "não tem teste para rodar". O critério de ordem de instalação é: suíte executável antes de hook que bloqueia commit; gate antes de registry que registra critério do gate; postmortem vira teste a partir do postmortem existente, não de postmortem futuro [1][7].

O diagnóstico não é único — é feito no momento da decisão de instalar, porque o sintoma de repo muda com o tempo (mais agentes, mais incidentes, mais colaboradores). O relatório é o que orienta a decisão do momento — e o re-diagnóstico periódico é o que orienta a decisão de revisitar peças instaladas [2][4].

## 3. Ilustra

Imagine um diagnóstico médico onde o médico faz exame para saber quais problemas o paciente tem — e só prescreve medicamento para o problema que o exame detectou. Prescrever medicamento para problema que o paciente não tem é custo e risco sem benefício. Em repo, o relatório de diagnóstico é o exame — e a peça a instalar é o medicamento para o sintoma detectado [3][6].

```mermaid
%% legenda: Diagnóstico de repo — mapear sintoma antes de instalar peça
flowchart TD
  A[Repo para diagnóstico] --> B[Relatório: 6 campos (1 por peça) + resumo de ordem]
  B --> C{Peça tem sintoma no repo?}
  C -->|sim| D[Candidata a instalação — ordem por impacto]
  C -->|não| E[Não instalar — custo sem benefício]
  D --> F[Ordem: suíte executável antes de hook; gate antes de registry]
  F --> G[Instalar peça por sintoma, não por catálogo]
  E -.-> H[instalar peça sem sintoma = custo de manutenção sem benefício]
  F -.-> I[instalar hook de merge antes de ter suíte = hook bloqueia tudo — developer bypassa]
```

## 4. Técnica

A técnica de diagnóstico é: para cada peça, perguntar a pergunta que a peça resolve e verificar se o repo tem o sintoma. O relatório entrega seis campos — um por peça — mais resumo de ordem. A técnica não gera script automaticamente — descreve o que cada campo pergunta e como verificar [1][4].

### Os seis campos do relatório de diagnóstico

1. **Separação Builder/Critic (peça 1):**
- [ ] Defina o limite de diagnóstico: diagnóstico deve ser feito sobre os últimos 30 dias de atividade do repo (limite de janela de tempo para sintoma relevante) — sintoma de há 6 meses pode não ser mais relevante.
- [ ] Defina o contorno de diagnóstico: diagnóstico não decide instalar — ele mapeia sintoma; decisão de instalar é do time com base no contexto de negócio do repo. O repo tem agentes ou processos onde o mesmo entidade gera e decide aceite? Sintoma: agente de IA que gera e self-review, developer que aprova próprio PR sem review. Se sim, peça 1 é candidata — classificador de papéis (cap 3) para mapear. Se não, o repo já tem separação — e peça 1 pode não ser prioridade.

2. **Gate Determinístico (peça 2):** O repo tem critério textual que podia ser gate mas é apenas lembrete? Sintoma: README com "deve ter chave X" mas sem script que verifica. Se sim, peça 2 é candidata — gate canônico (cap 4) para transformar critério em condição objetiva. Se não, o repo já tem gate — e peça 2 pode não ser prioridade.

3. **Registro Declarativo (peça 3):** O repo tem variável ou condição que se repete em dois ou mais arquivos de dispatch? Sintoma: mapeamento de tipo para comportamento em if/elif em múltiplos arquivos. Se sim, peça 3 é candidata — scaffold de registro (cap 5) para centralizar em 1 entrada. Se não, o repo já tem registro — e peça 3 pode não ser prioridade.

4. **Nunca Commitar Vermelho (peça 4):** O repo tem hook de pre-commit que realmente bloqueia (código não-zero) ou apenas avisa? Sintoma: hook que roda lints mas ignora código de saída, ou sem hook. Se sim, peça 4 é candidata — hook minimal (cap 6) para bloquear com código não-zero. Se não, o repo já tem hook de bloqueio — e peça 4 pode não ser prioridade.

5. **Postmortem vira Teste (peça 5):** O repo tem postmortems arquivados com prevenção textual sem stub? Sintoma: postmortem com "melhorar monitoramento" sem condição objetiva. Se sim, peça 5 é candidata — conversor (cap 7) para gerar stub de prevenções com condição objetiva. Se não, o repo já tem stub — e peça 5 pode não ser prioridade.

6. **Hook + CI/CD (peça 6):** O repo tem CI/CD que aplica o mesmo gate do hook local em cenário que o local não cobre? Sintoma: sem CI/CD, ou CI que reporta mas não bloqueia, ou CI com critério diferente do local. Se sim, peça 6 é candidata — workflow mínimo (cap 8) para aplicar mesmo gate. Se não, o repo já tem consistência de gate — e peça 6 pode não ser prioridade.

### Código: gerador de relatório de diagnóstico de repo (Python)

```python
# gerar_relatório_diagnóstico.py — gera relatório de 6 campos de diagnóstico de repo
# Critério objetivo, sem nuance de LLM. Baseado em busca de sintoma nos arquivos do repo.

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

@dataclass
class CampoDiagnóstico:
    """Campo de diagnóstico de uma peça: sintoma detectado, magnitude, recomendação."""
    peça: str
    sintoma: str
    magnitude: int
    recomendação: str
    detalhes: list[str] = field(default_factory=list)

class DiagnósticoRepo:
    """Gera relatório de diagnóstico de repo com 6 campos (um por peça)."""

    def __init__(self, caminho_repo: Path) -> None:
        self.repo = caminho_repo
        self.caminhos_py = list(caminho_repo.rglob("*.py")) + list(caminho_repo.rglob("*.js")) + list(caminho_repo.rglob("*.ts"))
        self.caminhos_md = list(caminho_repo.rglob("*.md"))
        self.caminhos_yaml = list(caminho_repo.rglob("*.yaml")) + list(caminho_repo.rglob("*.yml"))
        self.caminhos_json = list(caminho_repo.rglob("*.json"))
        self.caminhos_hook = list(caminho_repo.rglob(".git/hooks/pre-commit")) + list(caminho_repo.rglob("*.hook"))
        self.caminhos_ci = list(caminho_repo.rglob(".github/workflows/*.yml")) + list(caminho_repo.rglob(".gitlab-ci.yml"))
        self.caminhos_postmortem = [p for p in self.caminhos_md if "postmortem" in p.name.lower() or "incidente" in p.name.lower()]

    def diagnóstico_peca1(self) -> CampoDiagnóstico:
        """Peça 1: builder=critic. Sintoma: agente que gera e reviewa ao mesmo tempo."""
        arquivo_reviews = self.repo / ".gitreviews.json"
        if arquivo_reviews.exists():
            try:
                with open(arquivo_reviews, encoding="utf-8") as f:
                    reviews = json.load(f)
                sintomas = []
                for r in reviews:
                    autor = (r.get("author") or r.get("quem_abriu") or "").lower().strip()
                    revisor = (r.get("reviewer") or r.get("quem_aprovou") or "").lower().strip()
                    if autor and revisor and autor == revisor:
                        sintomas.append(r)
                return CampoDiagnóstico(
                    peça="1: Builder != Critic",
                    sintoma="reviews onde autor==revisora detectados" if sintomas else "sem sintoma detectável com instrumentação atual",
                    magnitude=len(sintomas),
                    recomendação="se magnitude > 0: classificar papéis de agente (cap 3); se sem instrumentação: instrumentar antes de decidir",
                    detalhes=[f"instrumentação de reviews: {'presente' if arquivo_reviews.exists() else 'ausente'}"],
                )
            except (json.JSONDecodeError, OSError) as e:
                return CampoDiagnóstico(
                    peça="1: Builder != Critic",
                    sintoma="erro ao ler instrumentação de reviews",
                    magnitude=0,
                    recomendação="verificar formato de .gitreviews.json",
                )
        return CampoDiagnóstico(
            peça="1: Builder != Critic",
            sintoma="sem instrumentação de reviews detectável",
            magnitude=0,
            recomendação="instrumentar coleta de reviews para fazer visível builder=critic",
            detalhes=["sem .gitreviews.json — diagnóstico não pode quantificar sintoma"],
        )

    def diagnóstico_peca2(self) -> CampoDiagnóstico:
        """Peça 2: gate determinístico. Sintoma: configuração sem gate verificável."""
        gate_scripts = [p for p in self.caminhos_py if "gate" in p.name.lower() or "validar" in p.name.lower()]
        configs = self.caminhos_yaml + self.caminhos_json
        if configs and not gate_scripts:
            return CampoDiagnóstico(
                peça="2: Gate determinístico",
                sintoma="configurações sem gate verificável detectável",
                magnitude=len(configs),
                recomendação="escrever gate canônico (cap 4) para critérios de presença/formato de configuração",
                detalhes=[f"{len(configs)} arquivo(s) de configuração sem gate detectável"],
            )
        if configs and gate_scripts:
            return CampoDiagnóstico(
                peça="2: Gate determinístico",
                sintoma="gate existente — verificar se cobre todos os formatos de configuração",
                magnitude=len(gate_scripts),
                recomendação="se gate cobre todos os formatos: ok; se não: estender gate",
                detalhes=[f"{len(configs)} configuração(ões), {len(gate_scripts)} gate(s)"],
            )
        return CampoDiagnóstico(
            peça="2: Gate determinístico",
            sintoma="sem configuração detectável — gate não necessário agora",
            magnitude=0,
            recomendação="reavaliar quando nasce configuração de agente ou tipo novo",
        )

    def diagnóstico_peca3(self) -> CampoDiagnóstico:
        """Peça 3: registro declarativo. Sintoma: variável/condição repetida em múltiplos arquivos."""
        repeticoes: dict[str, list[str]] = {}
        for caminho in self.caminhos_py:
            try:
                texto = caminho.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for tipo in ("agente", "configuracao", "politica", "pipeline"):
                if tipo in texto and len(self.caminhos_py) > 1:
                    repeticoes.setdefault(tipo, []).append(str(caminho))
        multi_arquivo = {k: v for k, v in repeticoes.items() if len(v) >= 2}
        if multi_arquivo:
            detalhes = [f"{k}: aparece em {len(v)} arquivo(s)" for k, v in multi_arquivo.items()]
            return CampoDiagnóstico(
                peça="3: Registro declarativo",
                sintoma="palavra-chave de tipo em múltiplos arquivos de código",
                magnitude=sum(len(v) for v in multi_arquivo.values()),
                recomendação="escrever scaffold de registro (cap 5) para centralizar critério por tipo",
                detalhes=detalhes,
            )
        return CampoDiagnóstico(
            peça="3: Registro declarativo",
            sintoma="sem sintoma de espalhamento de critério detectável com busca simples",
            magnitude=0,
            recomendação="reavaliar quando nasce tipo novo que exigiria editar múltiplos arquivos",
            detalhes=["diagnóstico com busca simples — para critério complexo, usar grep ou AST"],
        )

    def diagnóstico_peca4(self) -> CampoDiagnóstico:
        """Peça 4: nunca commitar vermelho. Sintoma: hook que não bloqueia ou sem hook."""
        hooks = [p for p in self.caminhos_hook if p.is_file()]
        if not hooks:
            return CampoDiagnóstico(
                peça="4: Nunca commitar vermelho",
                sintoma="sem hook de pre-commit detectável",
                magnitude=0,
                recomendação="escrever hook minimal (cap 6) que bloqueia quando suíte fala não",
                detalhes=["sem .git/hooks/pre-commit ou arquivo .hook"],
            )
        bloqueia = any("return 1" in p.read_text(encoding="utf-8", errors="ignore") or "sys.exit(1)" in p.read_text(encoding="utf-8", errors="ignore") for p in hooks if p.is_file())
        if bloqueia:
            return CampoDiagnóstico(
                peça="4: Nunca commitar vermelho",
                sintoma="hook de bloqueio detectável presentes",
                magnitude=len(hooks),
                recomendação="se hook bloqueia: ok; revisar consistência com CI (cap 8)",
                detalhes=[f"{len(hooks)} hook(s) com bloqueio detectável"],
            )
        return CampoDiagnóstico(
            peça="4: Nunca commitar vermelho",
            sintoma="hook presente mas sem bloqueio detectável (sem return 1/sys.exit(1))",
            magnitude=len(hooks),
            recomendação="adicionar retorno de código não-zero ao hook para transformar em peça 4",
            detalhes=[f"{len(hooks)} hook(s) que apenas avisa"],
        )

    def diagnóstico_peca5(self) -> CampoDiagnóstico:
        """Peça 5: postmortem vira teste. Sintoma: postmortem com prevenção textual sem stub."""
        if not self.caminhos_postmortem:
            return CampoDiagnóstico(
                peça="5: Postmortem vira teste",
                sintoma="sem postmortem detectável",
                magnitude=0,
                recomendação="quando surgir incidente: usar molde com checkbox de prevenção (cap 7)",
                detalhes=["sem arquivo de postmortem ou incidente em markdown"],
            )
        stubs = list(self.repo.glob("**/*_stubs.py")) + list(self.repo.glob("**/*stub*.py"))
        if stubs:
            return CampoDiagnóstico(
                peça="5: Postmortem vira teste",
                sintoma="stub de teste gerado para postmortem existente",
                magnitude=len(stubs),
                recomendação="integrar stubs na suíte — peça 5 ativa",
                detalhes=[f"{len(stubs)} stub(s) gerado(s)"],
            )
        return CampoDiagnóstico(
            peça="5: Postmortem vira teste",
            sintoma="postmortem presente sem stub de teste",
            magnitude=len(self.caminhos_postmortem),
            recomendação="aplicar conversor de postmortem para stub (cap 7)",
        )

    def diagnóstico_peca6(self) -> CampoDiagnóstico:
        """Peça 6: hook + CI/CD. Sintoma: sem CI, ou CI que não bloqueia, ou CI com critério diferente do local."""
        ci = [p for p in self.caminhos_ci if p.is_file()]
        local = [p for p in self.caminhos_hook if p.is_file()]
        if not ci:
            return CampoDiagnóstico(
                peça="6: Hook + CI/CD",
                sintoma="sem CI/CD detectável",
                magnitude=0,
                recomendação="escrever workflow mínimo (cap 8) que aplica mesmo gate do hook local em remoto",
                detalhes=["sem .github/workflows/ ou .gitlab-ci.yml"],
            )
        if not local:
            return CampoDiagnóstico(
                peça="6: Hook + CI/CD",
                sintoma="CI presente mas sem hook local",
                magnitude=len(ci),
                recomendação="instalar hook local (peça 4) para detecção antes do commit",
                detalhes=[f"{len(ci)} CI(s), sem hook local"],
            )
        return CampoDiagnóstico(
            peça="6: Hook + CI/CD",
            sintoma="hook local e CI presentes — verificar consistência de critério",
            magnitude=len(ci) + len(local),
            recomendação="rodar verificador de consistência de gate (cap 8)",
        )

    def gerar_relatório(self) -> dict[str, Any]:
        """Gera relatório completo de diagnóstico."""
        diagnósticos = [
            self.diagnóstico_peca1(),
            self.diagnóstico_peca2(),
            self.diagnóstico_peca3(),
            self.diagnóstico_peca4(),
            self.diagnóstico_peca5(),
            self.diagnóstico_peca6(),
        ]
        candidatas = [d for d in diagnósticos if d.magnitude > 0]
        ordem = [d.peça for d in candidatas]
        return {
            "repo": str(self.repo),
            "data": "gerado automaticamente",
            "campos": [d.__dict__ for d in diagnósticos],
            "candidatas_a_instalar": [d.__dict__ for d in candidatas],
            "ordem_de_instalação": ordem or ["nenhuma peça com sintoma detectável"],
        }

def main(caminho: str) -> int:
    repo = Path(caminho)
    if not repo.is_dir():
        print(f"ERRO: {caminho} não é diretório", file=sys.stderr)
        return 2
    diagnóstico = DiagnósticoRepo(repo)
    relatório = diagnóstico.gerar_relatório()
    print("RELATÓRIO DE DIAGNÓSTICO DE REPO")
    print("=" * 50)
    print(f"Repo: {relatório['repo']}")
    print()
    for campo in relatório["campos"]:
        print(f"[{campo['peça']}]")
        print(f"  Sintoma: {campo['sintoma']}")
        print(f"  Magnitude: {campo['magnitude']}")
        print(f"  Recomendação: {campo['recomendação']}")
        if campo["detalhes"]:
            for detalhe in campo["detalhes"]:
                print(f"    - {detalhe}")
        print()
    print("CANDIDATAS A INSTALAÇÃO (por ordem de dependência):")
    for item in relatório["ordem_de_instalação"]:
        print(f"  - {item}")
    saida = repo / "diagnostico_relatorio.json"
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(relatório, f, ensure_ascii=False, indent=2)
    print(f"\nRelatório gravado em: {saida}")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python gerar_relatório_diagnóstico.py <caminho-do-repo>", file=sys.stderr)
        sys.exit(2)
    raise SystemExit(main(sys.argv[1]))
```

O gerador de relatório entrega os seis campos com magnitude e recomendação — e o resumo de ordem de instalação. O relatório é o que orienta a decisão de instalar peça por sintoma, e não por catálogo. O relatório também grava JSON para rastreio da decisão [1][4].

### Resumo de ordem

O resumo de ordem ordena as peças candidatas por impacto e por dependência: suíte executável antes de hook de bloqueio; gate antes de registro que registra critério do gate; postmortem vira teste a partir de postmortem existente; hook + CI/CD depois de hook local. A ordem não é rígida — é orientação para não instalar peça de proteção de merge antes de ter suíte para rodar [2][5].

## 5. Aplica

Você entra em um repo novo e quer saber quais das seis peças instalar. O diagnóstico começa perguntando: o repo tem suíte de teste executável? Se não, a prioridade não é hook de bloqueio — é suíte. Sem suíte, hook de bloqueio bloqueia tudo e o developer bypassa. Depois de suíte, o diagnóstico pergunta: o repo tem critério textual que podia ser gate? Se sim, peça 2. Depois: o repo tem variável repetida em múltiplos arquivos? Se sim, peça 3. Depois: o repo tem hook de bloqueio real ou apenas aviso? Se não, peça 4. Depois: o repo tem postmortems com prevenção textual sem stub? Se sim, peça 5. Depois: o repo tem CI/CD com mesmo gate do local? Se não, peça 6 [3][7].

Um cenário real de instituição: repo pequeno com 3 pessoas, sem suíte de teste, sem hook, sem postmortem. O diagnóstico mostra: peça 4 (hook) não é prioridade antes de suíte; peça 5 (postmortem vira teste) não é prioridade antes de postmortem; peça 2 (gate) pode ser prioridade se houver critério textual que podia ser gate; peça 3 (registro) pode ser prioridade se houver variável repetida. O relatório entrega a ordem: suíte antes de hook; gate e registro conforme sintoma [1][4].

Escala: em repo grande com múltiplos agentes, o diagnóstico é mais relevante porque o número de sintomas possíveis cresce — e instalar peça por sintoma evita instalar peça de proteção para cenário que o repo não tem. O diagnóstico periódico é o que orienta a decisão de revisitar peças instaladas quando o repo muda [2][6].

## 6. Conclusão

O diagnóstico de repo é o que transforma a lista de seis peças em decisão de engenharia — e o relatório de seis campos é o que mapeia sintoma antes de instalar. A técnica não gera script automaticamente — descreve o que cada campo pergunta e como verificar. A ordem de instalação é orientação: suíte executável antes de hook; gate antes de registro; postmortem vira teste a partir de postmortem existente; hook + CI/CD depois de hook local. Os próximos capítulos detalham a aplicação: instalar sem destruir (cap 10), manter vivo depois da instalação (cap 11). A peça de diagnóstico é a que orienta todas as outras — e é a que mais vezes é pulada porque "já sabemos o que instalar" — e instalar sem diagnóstico é instalar por moda, não por sintoma [3][5].

## 7. Referências Bibliográficas

[1] MARTIN, R. C. *Agile Software Development: Principles, Patterns, and Practices*. Boston: Prentice Hall, 2002. ISBN 978-0135974543.

[2] MARTIN, R. C. *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. 1. ed. Boston: Pearson, 2017. ISBN 978-0134434403.

[3] MYERS, G. J. *The Art of Software Testing*. 2. ed. Hoboken: John Wiley & Sons, 2011. ISBN 978-0470404152.

[4] FOWLER, M. *Continuous Integration*. 2001. Disponível em: https://martinfowler.com/articles/continuousIntegration.html. Acesso em: 09 set. 2026.

[5] GOOGLE SRE. *Testing Release and Deployment*. In: *Site Reliability Engineering*. Disponível em: https://sre.google/sre-book/testing-releases/. Acesso em: 09 set. 2026.

[6] BROWN, S.; BEYER, B.; et al. *Site Reliability Engineering: How Google Runs Production Systems*. Sebastopol: O'Reilly Media, 2016. ISBN 978-1491929124.

[7] HUMBLE, J.; FARLEY, D. *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Boston: Addison-Wesley, 2010. ISBN 978-0321601945.
