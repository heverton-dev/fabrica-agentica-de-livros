#!/usr/bin/env python3
"""
Validate All Gates
Roda todos os 5 gates em todos os capítulos e gera relatório
"""

import os
import subprocess
import json
from pathlib import Path
from collections import defaultdict

def console_utf8():
    import sys
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

console_utf8()

GATES = ["gate_1_eita_structure.py", "gate_2_code_completeness.py",
         "gate_3_didactic_accessibility.py", "gate_4_exercises_completeness.py",
         "gate_5_quality_metrics.py"]

def run_gate(gate_script, arquivo):
    """Rodar um gate em um arquivo."""
    try:
        result = subprocess.run(
            ["python", f"scripts/{gate_script}", arquivo],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except:
        return False

def scan_all_chapters():
    """Listar todos os capítulos."""
    base_path = Path("output/tela-camada-agente/livros")
    chapters = []

    for livro_path in sorted(base_path.iterdir()):
        if not livro_path.is_dir():
            continue
        caps_path = livro_path / "capitulos"
        if not caps_path.exists():
            continue

        for cap_file in sorted(caps_path.glob("cap_*.md")):
            chapters.append({
                "livro": livro_path.name,
                "arquivo": str(cap_file),
                "nome": cap_file.stem
            })

    return chapters

def validate_all():
    """Validar todos os capítulos com todos os gates."""
    chapters = scan_all_chapters()

    print("\n🔍 Validação Completa: Todos os Gates × Todos os Capítulos")
    print("━" * 80)

    # Matriz de resultados
    results = defaultdict(lambda: {})
    gate_scores = defaultdict(int)

    # Rodar cada gate em cada capítulo
    for chapter in chapters:
        print(f"\n📚 {chapter['livro']} / {chapter['nome']}")

        for gate in GATES:
            gate_name = gate.split("_")[1]  # ex: "eita", "code", etc
            passed = run_gate(gate, chapter["arquivo"])

            results[chapter["arquivo"]][gate_name] = "✅" if passed else "❌"
            if passed:
                gate_scores[gate_name] += 1

            print(f"  {gate_name:8} {'✅' if passed else '❌'}")

    # Relatório consolidado
    print("\n" + "━" * 80)
    print("\n📊 RELATÓRIO CONSOLIDADO")
    print("━" * 80)

    total_caps = len(chapters)

    for i, gate in enumerate(GATES, 1):
        gate_name = gate.split("_")[1]
        score = gate_scores[gate_name]
        pct = (score / total_caps * 100) if total_caps > 0 else 0

        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"\nGate {i}: {gate_name.upper():15} [{bar}] {score:2}/{total_caps} ({pct:5.1f}%)")

    # Score geral
    print("\n" + "━" * 80)
    print("\n🎯 SCORE GERAL")

    scores_by_livro = defaultdict(lambda: defaultdict(int))
    caps_by_livro = defaultdict(int)

    for chapter in chapters:
        livro = chapter["livro"]
        caps_by_livro[livro] += 1

        for gate_name, result in results[chapter["arquivo"]].items():
            if result == "✅":
                scores_by_livro[livro][gate_name] += 1

    for livro in sorted(scores_by_livro.keys()):
        total = caps_by_livro[livro]
        avg_score = sum(scores_by_livro[livro].values()) / (5 * total) if total > 0 else 0
        pct = avg_score * 100

        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"\n{livro:30} [{bar}] {pct:5.1f}%")

        for gate_name in ["eita", "code", "didactic", "exercises", "metrics"]:
            score = scores_by_livro[livro].get(gate_name, 0)
            print(f"  {gate_name:12} {score}/{total} caps")

    # Resumo
    print("\n" + "━" * 80)
    all_passed = sum(gate_scores.values())
    all_total = total_caps * len(GATES)
    final_pct = (all_passed / all_total * 100) if all_total > 0 else 0

    print(f"\n✅ TOTAL: {all_passed}/{all_total} gates passando ({final_pct:.1f}%)")
    print(f"\n📈 Score Estimado: {final_pct * 0.1:.1f}/10")

    # Próximos passos
    print("\n" + "━" * 80)
    print("\n📋 PRÓXIMOS PASSOS (Retrofit Priorizado):")

    for livro in sorted(scores_by_livro.keys()):
        total = caps_by_livro[livro]
        avg_score = sum(scores_by_livro[livro].values()) / (5 * total) if total > 0 else 0

        if avg_score < 0.5:
            print(f"  🔴 {livro}: Refazer (apenas {avg_score * 100:.0f}% gates passam)")
        elif avg_score < 0.8:
            print(f"  🟡 {livro}: Melhorar (faltam {(1 - avg_score) * 100:.0f}% gates)")
        else:
            print(f"  🟢 {livro}: OK (pronto para produção)")

    print("\n" + "━" * 80)

if __name__ == "__main__":
    validate_all()
