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
