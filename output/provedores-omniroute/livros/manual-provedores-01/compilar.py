#!/usr/bin/env python3
"""
Compilador PDF do Manual OmniRoute — Padrão Fábrica Agêntica
Converte: Markdown → Consolidado → PDF

Uso:
    python compilar.py
    ou
    python compilar.py --output caminho/do/pdf.pdf
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import Optional
import json

# Cores para terminal
class Cores:
    AMARELO = '\033[1;33m'
    VERDE = '\033[0;32m'
    VERMELHO = '\033[0;31m'
    RESET = '\033[0m'
    INFO = '\033[0;36m'

def log_info(msg: str):
    print(f"{Cores.AMARELO}ℹ️  {msg}{Cores.RESET}")

def log_sucesso(msg: str):
    print(f"{Cores.VERDE}✅ {msg}{Cores.RESET}")

def log_erro(msg: str):
    print(f"{Cores.VERMELHO}❌ {msg}{Cores.RESET}")

def log_passo(num: int, total: int, msg: str):
    print(f"{Cores.AMARELO}[{num}/{total}] {msg}...{Cores.RESET}")

def consolidar_capitulos(dir_livro: Path, temp_md: Path) -> bool:
    """Consolida todos os capítulos em um único Markdown."""
    log_passo(1, 4, "Consolidando capítulos")

    capitulos_dir = dir_livro / "capitulos"
    if not capitulos_dir.exists():
        log_erro(f"Diretório {capitulos_dir} não encontrado")
        return False

    with open(temp_md, "w", encoding="utf-8") as f:
        # Cabeçalho
        f.write("# Manual OmniRoute\n\n")
        f.write("## 15 Provedores de IA Gratuitos para Máxima Confiabilidade\n\n")
        f.write("---\n\n")
        f.write("**Data**: 24 de agosto de 2026\n")
        f.write("**Versão**: 1.0\n")
        f.write("**Autor**: Marketing Conexão\n")
        f.write("**Editor**: Editora Agêntica\n\n")
        f.write("---\n\n")

        # Capítulos
        caps = sorted(capitulos_dir.glob("*.md"))
        for cap_file in caps:
            try:
                with open(cap_file, "r", encoding="utf-8") as cap:
                    content = cap.read()
                    f.write(content)
                    f.write("\n\n---\n\n")
                log_info(f"✓ {cap_file.name}")
            except Exception as e:
                log_erro(f"Erro ao ler {cap_file.name}: {e}")
                return False

    log_sucesso("Capítulos consolidados")
    return True

def verificar_pandoc() -> bool:
    """Verifica se Pandoc está instalado."""
    try:
        subprocess.run(["pandoc", "--version"],
                      capture_output=True,
                      check=True,
                      timeout=5)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def verificar_typst() -> bool:
    """Verifica se Typst está instalado."""
    try:
        subprocess.run(["typst", "--version"],
                      capture_output=True,
                      check=True,
                      timeout=5)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def compilar_via_pandoc(temp_md: Path, output_pdf: Path) -> bool:
    """Compila Markdown → PDF via Pandoc."""
    log_passo(2, 4, "Convertendo Markdown → PDF (Pandoc)")

    if not verificar_pandoc():
        log_erro("Pandoc não encontrado. Instale com: https://pandoc.org/installing.html")
        return False

    # Tenta com diferentes engines
    engines = ["wkhtmltopdf", "weasyprint", None]  # None = default pdflatex

    for engine in engines:
        try:
            cmd = [
                "pandoc",
                str(temp_md),
                "--from", "markdown",
                "--to", "pdf",
                "--output", str(output_pdf),
                "-V", "geometry:margin=1in",
                "-V", "mainfont=Calibri",
                "-N",  # Number sections
                "--toc",  # Table of contents
                "--toc-depth=2",
                "--standalone",
            ]

            if engine:
                cmd.extend(["--pdf-engine", engine])

            log_info(f"Tentando com engine: {engine or 'default (pdflatex)'}")
            result = subprocess.run(cmd,
                                  capture_output=True,
                                  text=True,
                                  timeout=60)

            if result.returncode == 0 and output_pdf.exists() and output_pdf.stat().st_size > 0:
                log_sucesso(f"PDF compilado com {engine or 'pdflatex'}")
                return True

        except subprocess.TimeoutExpired:
            log_info(f"Timeout com {engine or 'default'}")
            continue
        except Exception as e:
            log_info(f"Erro com {engine or 'default'}: {e}")
            continue

    return False

def compilar_via_typst(temp_md: Path, temp_typ: Path, output_pdf: Path, dir_livro: Path) -> bool:
    """Compila via Typst (método preferido da Fábrica)."""
    log_passo(2, 4, "Convertendo Markdown → Typst → PDF")

    if not verificar_pandoc():
        log_erro("Pandoc necessário para converter para Typst")
        return False

    # Converter MD para Typst
    log_info("Markdown → Typst...")
    try:
        result = subprocess.run([
            "pandoc",
            str(temp_md),
            "--from", "markdown",
            "--to", "typst",
            "--output", str(temp_typ),
        ], capture_output=True, text=True, timeout=30)

        if result.returncode != 0 or not temp_typ.exists():
            log_info("Fallback: Typst não disponível")
            return False

    except Exception as e:
        log_info(f"Erro na conversão Typst: {e}")
        return False

    # Compilar Typst para PDF
    if not verificar_typst():
        log_info("Typst não encontrado. Use: cargo install typst-cli")
        return False

    log_info("Typst → PDF...")
    try:
        result = subprocess.run([
            "typst",
            "compile",
            "--root", str(dir_livro),
            str(temp_typ),
            str(output_pdf)
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0 and output_pdf.exists() and output_pdf.stat().st_size > 0:
            log_sucesso("PDF compilado via Typst")
            # Limpar .typ temporário
            temp_typ.unlink(missing_ok=True)
            return True

    except Exception as e:
        log_info(f"Erro na compilação Typst: {e}")

    return False

def main():
    # Setup
    dir_livro = Path(__file__).parent
    temp_md = dir_livro / "_manual_temp.md"
    temp_typ = dir_livro / "_manual_temp.typ"
    output_pdf = dir_livro / "manual-omniroute.pdf"

    # Parse args
    if len(sys.argv) > 2 and sys.argv[1] == "--output":
        output_pdf = Path(sys.argv[2])

    print(f"\n{Cores.AMARELO}{'='*60}")
    print(f"📚 Compilador Manual OmniRoute — Fábrica Agêntica")
    print(f"{'='*60}{Cores.RESET}\n")

    try:
        # 1. Consolidar
        if not consolidar_capitulos(dir_livro, temp_md):
            raise Exception("Falha ao consolidar capítulos")

        # 2. Compilar
        sucesso = False
        if verificar_typst():
            sucesso = compilar_via_typst(temp_md, temp_typ, output_pdf, dir_livro)

        if not sucesso:
            sucesso = compilar_via_pandoc(temp_md, output_pdf)

        if not sucesso:
            raise Exception("Nenhum motor de compilação disponível")

        # 3. Verificar resultado
        log_passo(3, 4, "Verificando resultado")
        if not output_pdf.exists() or output_pdf.stat().st_size == 0:
            raise Exception("Arquivo PDF vazio ou não criado")

        size_mb = output_pdf.stat().st_size / (1024*1024)
        log_sucesso(f"PDF compilado: {output_pdf.name} ({size_mb:.1f} MB)")

        # 4. Limpeza
        log_passo(4, 4, "Limpeza")
        temp_md.unlink(missing_ok=True)
        temp_typ.unlink(missing_ok=True)

        print(f"\n{Cores.VERDE}{'='*60}")
        print(f"✅ Compilação concluída com sucesso!")
        print(f"📄 Arquivo: {output_pdf}")
        print(f"{'='*60}{Cores.RESET}\n")

        return 0

    except Exception as e:
        log_erro(str(e))

        # Limpeza em caso de erro
        temp_md.unlink(missing_ok=True)
        temp_typ.unlink(missing_ok=True)

        print(f"\n{Cores.VERMELHO}{'='*60}")
        print(f"❌ Compilação falhou")
        print(f"{'='*60}{Cores.RESET}\n")

        return 1

if __name__ == "__main__":
    sys.exit(main())
