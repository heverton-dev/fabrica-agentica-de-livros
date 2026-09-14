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

    def carga_peca4(self) -> CargaPeça:
        """Peça 4: hook. Sinais: bypass frequente, falso-positivo acumulado."""
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
            if "bypass" in texto.lower() or "no-verify" in texto.lower():
                sinais.append(f"hook {hook.name} menciona bypass — investigar se bypass é documentado ou não")
            if "TODO" in texto and "fixar" not in texto.lower():
                sinais.append(f"hook {hook.name} tem TODO sem resolver — sinal de manutenção pendente")
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
                sinais.append(f"gate {gate.name} menciona falso-positivo — ajustar critério pode reduzir")
            if "TODO" in texto:
                sinais.append(f"gate {gate.name} tem TODO — sinal de manutenção pendente")
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
                sinais.append(f"CI {c.name} tem timeout configurado — pipeline pode ser lento")
            if "retry" in texto.lower():
                sinais.append(f"CI {c.name} tem retry — pode indicar flakiness")
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
