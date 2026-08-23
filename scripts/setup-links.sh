#!/usr/bin/env bash
# Recria os links de portabilidade multi-IDE da Fabrica Agentica de Livros (macOS/Linux).
# Idempotente. Aqui symlink real de arquivo e de pasta funciona sem privilegio elevado,
# entao usamos symlink em todos os casos (equivalente ao hardlink+junction do Windows).
#
# Uso: bash scripts/setup-links.sh
set -euo pipefail

raiz="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$raiz"

link() {
  local alvo="$1" link="$2"
  if [ ! -e "$alvo" ]; then
    echo "AVISO: alvo nao encontrado, pulando: $alvo"
    return
  fi
  mkdir -p "$(dirname "$link")"
  if [ -L "$link" ]; then
    echo "OK (ja e symlink): $link"
    return
  fi
  if [ -e "$link" ]; then
    echo "AVISO: ja existe e NAO e symlink, pulando (apague manualmente se quiser recriar): $link"
    return
  fi
  ln -s "$(realpath --relative-to="$(dirname "$link")" "$alvo")" "$link"
  echo "Criado symlink: $link -> $alvo"
}

echo "== Arquivos de instrucao (symlink para CLAUDE.md) =="
link "CLAUDE.md" "AGENTS.md"
link "CLAUDE.md" ".cursor/rules/fabrica-agentica.mdc"
link "CLAUDE.md" ".windsurfrules"
link "CLAUDE.md" ".windsurf/rules/fabrica-agentica.md"
link "CLAUDE.md" ".clinerules"
link "CLAUDE.md" ".github/copilot-instructions.md"

echo
echo "== MCP (symlink para .mcp.json, schema compativel) =="
link ".mcp.json" ".cursor/mcp.json"

echo
echo "== Pastas neutras (symlink para .claude/...) =="
link ".claude/skills" "agentic/skills"
link ".claude/agents" "agentic/agents"
link ".claude/commands" "agentic/commands"
link ".claude/mcp-servers" "agentic/mcp-servers"

echo
echo "== Pastas .agents/ (symlink para .claude/..., harnesses alternativos) =="
# NAO expor skills/ e mcp-servers/ aqui: .agents/ e o diretorio de agentes do
# Codebuff/Freebuff, que importa e executa os .js/.mjs que encontra dentro dele.
# compilar-livro.mjs roda no import, imprime o USO e chama process.exit(1),
# matando o CLI. Apenas agents/ e commands/ (somente .md) sao seguros aqui.
# Skills e MCP servers seguem disponiveis via agentic/ e .opencode/.
link ".claude/agents" ".agents/agents"
link ".claude/commands" ".agents/commands"

echo
echo "== Pastas .opencode/ (symlink para .claude/..., OpenCode) =="
link ".claude/skills" ".opencode/skills"
link ".claude/agents" ".opencode/agents"
link ".claude/commands" ".opencode/commands"
link ".claude/mcp-servers" ".opencode/mcp-servers"
link ".claude/settings.json" ".opencode/settings.json"

echo
echo "== MCP traduzido para VS Code e OpenCode (schemas diferentes, gerados por script) =="
node "$raiz/scripts/sincronizar-mcp-vscode.mjs"
node "$raiz/scripts/sincronizar-mcp-opencode.mjs"

echo
echo "== Hook pre-commit (R16 - copia, .git/hooks nao aceita link) =="
cp "$raiz/scripts/hooks/pre-commit" "$raiz/.git/hooks/pre-commit"
chmod +x "$raiz/.git/hooks/pre-commit"
echo "Copiado: scripts/hooks/pre-commit -> .git/hooks/pre-commit"

echo
echo "Concluido."
