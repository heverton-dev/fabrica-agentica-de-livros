# instalar_peca_dryrun.py — simula instalação de peça em modo dry-run, sem gravar no repo
# Critério objetivo: relata impacto esperado sem alterar arquivos.

import os
import re
import sys
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ImpactoPeça:
    """Impacto esperado de instalação de uma peça: arquivos afetados, ações, risco."""
    peça: str
    ações: list[str] = field(default_factory=list)
    arquivos_afetados: list[str] = field(default_factory=list)
    risco: str = "baixo"
    nota: str = ""


class InstaladorDryRun:
    """Simula instalação de peças sem gravar no repo — reporta impacto esperado."""

    def __init__(self, caminho_repo: Path) -> None:
        self.repo = caminho_repo
        self.caminhos_py = list(caminho_repo.rglob("*.py")) + list(caminho_repo.rglob("*.js")) + list(caminho_repo.rglob("*.ts"))
        self.caminhos_md = list(caminho_repo.rglob("*.md"))
        self.caminhos_yaml = list(caminho_repo.rglob("*.yaml")) + list(caminho_repo.rglob("*.yml"))
        self.caminhos_hook = list(caminho_repo.rglob(".git/hooks/pre-commit")) + list(caminho_repo.rglob("*.hook"))
        self.caminhos_ci = list(caminho_repo.rglob(".github/workflows/*.yml")) + list(caminho_repo.rglob(".gitlab-ci.yml"))

    def dry_run_peca2(self) -> ImpactoPeça:
        """Dry-run de gate: relata quantos arquivos de configuração seriam verificados."""
        configs = self.caminhos_yaml + self.caminhos_json
        ações = ["escrever gate_canonico.py com critérios de presença/formato"] if configs else ["gate não necessário sem configuração"]
        return ImpactoPeça(
            peça="2: Gate determinístico",
            ações=ações,
            arquivos_afetados=[str(p) for p in configs] if configs else [],
            risco="baixo" if configs else "nenhum",
            nota=f"dry-run: {len(configs)} arquivo(s) de configuração seriam verificados pelo gate" if configs else "sem configuração para gate",
        )

    def dry_run_peca3(self) -> ImpactoPeça:
        """Dry-run de registro: relata quantos arquivos teriam que ser refatorados."""
        repeticoes: dict[str, list[str]] = {}
        for caminho in self.caminhos_py:
            try:
                texto = caminho.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for tipo in ("agente", "configuracao", "politica", "pipeline"):
                if tipo in texto and len(self.caminhos_py) > 1:
                    repeticoes.setdefault(tipo, []).append(str(caminho))
        multi = {k: v for k, v in repeticoes.items() if len(v) >= 2}
        ações = ["escrever scaffold de registro (registro_tipos.py) e refatorar consumidores para ler registro"]
        return ImpactoPeça(
            peça="3: Registro declarativo",
            ações=ações,
            arquivos_afetados=[str(p) for v in multi.values() for p in v],
            risco="médio" if multi else "baixo",
            nota=f"dry-run: {len(multi)} tipo(s) com critério em múltiplos arquivos — refatorar {sum(len(v) for v in multi.values())} arquivo(s)" if multi else "sem sintoma de espalhamento — registro não necessário agora",
        )

    def dry_run_peca4(self) -> ImpactoPeça:
        """Dry-run de hook: relata se hook existente bloqueia e quantos commits seriam afetados."""
        hooks = [p for p in self.caminhos_hook if p.is_file()]
        ações = []
        if hooks:
            bloqueia = any("return 1" in p.read_text(encoding="utf-8", errors="ignore") or "sys.exit(1)" in p.read_text(encoding="utf-8", errors="ignore") for p in hooks)
            if bloqueia:
                ações = ["hook de bloqueio já existente — revisar consistência com CI (cap 8)"]
                risco = "baixo"
                nota = "dry-run: hook bloqueia — não há ação de instalação, apenas revisão de consistência"
            else:
                ações = ["adicionar retorno de código não-zero ao hook existente para transformar em peça 4"]
                risco = "médio"
                nota = "dry-run: hook atual apenas avisa — adicionar bloqueio é mínimo (1 linha)"
        else:
            ações = ["escrever pre_commit_hook.py minimal que roda suíte e bloqueia com código não-zero"]
            risco = "médio"
            nota = "dry-run: sem hook — instalar hook minimal; verificar se suíte existe antes de instalar hook de bloqueio"
        return ImpactoPeça(
            peça="4: Nunca commitar vermelho",
            ações=ações,
            arquivos_afetados=[str(p) for p in hooks] if hooks else [],
            risco=risco,
            nota=nota,
        )

    def dry_run_peca5(self) -> ImpactoPeça:
        """Dry-run de postmortem vira teste: relata quantos stubs seriam gerados."""
        postmortems = [p for p in self.caminhos_md if "postmortem" in p.name.lower() or "incidente" in p.name.lower()]
        if not postmortems:
            return ImpactoPeça(
                peça="5: Postmortem vira teste",
                ações=["sem postmortem — não há ação de instalação agora"],
                arquivos_afetados=[],
                risco="nenhum",
                nota="dry-run: sem postmortem — peça 5 não ativa até surgir incidente documentado",
            )
        ações = ["rodar postmortem_para_stub.py em cada postmortem para gerar stub de prevenções com condição objetiva"]
        return ImpactoPeça(
            peça="5: Postmortem vira teste",
            ações=ações,
            arquivos_afetados=[str(p) for p in postmortems],
            risco="baixo",
            nota=f"dry-run: {len(postmortems)} postmortem(ês) — gerar stubs e integrar na suíte",
        )

    def dry_run_peca6(self) -> ImpactoPeça:
        """Dry-run de CI/CD: relata se CI existe e se é consistente com hook local."""
        ci = [p for p in self.caminhos_ci if p.is_file()]
        local = [p for p in self.caminhos_hook if p.is_file()]
        ações = []
        risco = "baixo"
        if not ci:
            ações = ["escrever .github/workflows/ci-gate.yml com as mesmas etapas do hook local (formatação, lint, suíte, gate)"]
            risco = "médio"
            nota = "dry-run: sem CI — instalar workflow mínimo que bloqueia merge quando gate decide não"
        elif not local:
            ações = ["instalar hook local (peça 4) para detecção antes do commit — CI é segunda linha"]
            risco = "médio"
            nota = "dry-run: CI presente sem hook local — hook local é primeira linha de defesa"
        else:
            ações = ["verificar consistência de gate local/remoto com consistencia_gate.py"]
            nota = "dry-run: hook local e CI presentes — verificar se critério é o mesmo"
        return ImpactoPeça(
            peça="6: Hook + CI/CD",
            ações=ações,
            arquivos_afetados=[str(p) for p in ci] + [str(p) for p in local],
            risco=risco,
            nota=nota,
        )

    def gerar_relatório_impacto(self) -> list[ImpactoPeça]:
        """Gera relatório de impacto de dry-run para todas as peças."""
        return [
            self.dry_run_peca2(),
            self.dry_run_peca3(),
            self.dry_run_peca4(),
            self.dry_run_peca5(),
            self.dry_run_peca6(),
        ]


def main(caminho: str) -> int:
    repo = Path(caminho)
    if not repo.is_dir():
        print(f"ERRO: {caminho} não é diretório", file=sys.stderr)
        return 2
    instalador = InstaladorDryRun(repo)
    impactos = instalador.gerar_relatório_impacto()
    print("DRY-RUN DE INSTALAÇÃO DE PEÇAS")
    print("=" * 50)
    print(f"Repo: {repo}")
    print("AVISO: dry-run não altera arquivos — apenas relata impacto esperado\n")
    for impacto in impactos:
        print(f"[{impacto.peça}]")
        print(f"  Risco: {impacto.risco}")
        print(f"  Ações: {len(impacto.acoes)}")
        for ação in impacto.acoes:
            print(f"    - {ação}")
        if impacto.arquivos_afetados:
            print(f"  Arquivos afetados: {len(impacto.arquivos_afetados)}")
            for a in impacto.arquivos_afetados[:5]:
                print(f"    - {a}")
            if len(impacto.arquivos_afetados) > 5:
                print(f"    ... +{len(impacto.arquivos_afetados) - 5} mais")
        print(f"  Nota: {impacto.nota}")
        print()
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python instalar_peca_dryrun.py <caminho-do-repo>", file=sys.stderr)
        sys.exit(2)
    raise SystemExit(main(sys.argv[1]))
