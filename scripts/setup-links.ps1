# Recria os links de portabilidade multi-IDE da Fabrica Agentica de Livros (Windows).
# Idempotente: pode ser rodado quantas vezes quiser. Usa HARDLINK para arquivos e
# JUNCTION para pastas porque symlink real de ARQUIVO exige privilegio de administrador
# neste SO; junction de pasta e hardlink de arquivo nao exigem elevacao.
#
# Uso:  powershell -ExecutionPolicy Bypass -File scripts\setup-links.ps1

$ErrorActionPreference = "Stop"
$raiz = Split-Path -Parent $PSScriptRoot

function Set-HardLink($linkRelativo, $targetRelativo) {
    $link = Join-Path $raiz $linkRelativo
    $target = Join-Path $raiz $targetRelativo
    if (-not (Test-Path $target)) {
        Write-Warning "Alvo nao encontrado, pulando: $targetRelativo"
        return
    }
    $linkDir = Split-Path -Parent $link
    if (-not (Test-Path $linkDir)) { New-Item -ItemType Directory -Force -Path $linkDir | Out-Null }
    if (Test-Path $link) {
        # LinkType == "HardLink" so diz que o arquivo E um hardlink de ALGUEM - nao
        # garante que ainda aponta pro TARGET atual. Um editor que salva com
        # write-novo-arquivo+rename (comum) desvincula o inode em silencio: o
        # arquivo continua "sendo hardlink" de outros espelhos, so que nao mais
        # deste CLAUDE.md. Por isso o criterio de verdade e o HASH do conteudo,
        # nao o LinkType.
        $hashLink = (Get-FileHash -Path $link -Algorithm SHA256).Hash
        $hashTarget = (Get-FileHash -Path $target -Algorithm SHA256).Hash
        if ($hashLink -eq $hashTarget) {
            Write-Output "OK (conteudo em dia): $linkRelativo"
            return
        }
        Write-Warning "Desalinhado do alvo (hardlink quebrado por rewrite externo) - recriando: $linkRelativo"
        Remove-Item -Path $link -Force
    }
    New-Item -ItemType HardLink -Path $link -Target $target | Out-Null
    Write-Output "Criado hardlink: $linkRelativo -> $targetRelativo"
}

function Set-Junction($linkRelativo, $targetRelativo) {
    $link = Join-Path $raiz $linkRelativo
    $target = Join-Path $raiz $targetRelativo
    if (-not (Test-Path $target)) {
        Write-Warning "Alvo nao encontrado, pulando: $targetRelativo"
        return
    }
    $linkParent = Split-Path -Parent $link
    if (-not (Test-Path $linkParent)) { New-Item -ItemType Directory -Force -Path $linkParent | Out-Null }
    if (Test-Path $link) {
        $item = Get-Item $link -Force
        if ($item.LinkType -eq "Junction") {
            Write-Output "OK (ja e junction): $linkRelativo"
            return
        }
        Write-Warning "Ja existe e NAO e junction, pulando (apague manualmente se quiser recriar): $linkRelativo"
        return
    }
    New-Item -ItemType Junction -Path $link -Target $target | Out-Null
    Write-Output "Criada junction: $linkRelativo -> $targetRelativo"
}

Write-Output "== Arquivos de instrucao (hardlink de CLAUDE.md) =="
Set-HardLink "AGENTS.md"                                  "CLAUDE.md"
Set-HardLink ".cursor\rules\fabrica-agentica.mdc"         "CLAUDE.md"
Set-HardLink ".windsurfrules"                             "CLAUDE.md"
Set-HardLink ".windsurf\rules\fabrica-agentica.md"        "CLAUDE.md"
Set-HardLink ".clinerules"                                "CLAUDE.md"
Set-HardLink ".github\copilot-instructions.md"            "CLAUDE.md"

Write-Output "`n== MCP (hardlink de .mcp.json, schema compativel) =="
Set-HardLink ".cursor\mcp.json"                           ".mcp.json"

Write-Output "`n== Pastas neutras (junction para .claude\...) =="
Set-Junction "agentic\skills"                             ".claude\skills"
Set-Junction "agentic\agents"                             ".claude\agents"
Set-Junction "agentic\commands"                           ".claude\commands"
Set-Junction "agentic\mcp-servers"                        ".claude\mcp-servers"

Write-Output "`n== Pastas .agents\ (junction para .claude\..., harnesses alternativos) =="
# NAO expor skills\ e mcp-servers\ aqui: .agents\ e o diretorio de agentes do
# Codebuff/Freebuff, que importa e executa os .js/.mjs que encontra dentro dele.
# compilar-livro.mjs roda no import, imprime o USO e chama process.exit(1),
# matando o CLI. Apenas agents\ e commands\ (somente .md) sao seguros aqui.
# Skills e MCP servers seguem disponiveis via agentic\ e .opencode\.
Set-Junction ".agents\agents"                             ".claude\agents"
Set-Junction ".agents\commands"                           ".claude\commands"

Write-Output "`n== Pastas .opencode\ (junction para .claude\..., OpenCode) =="
Set-Junction ".opencode\skills"                             ".claude\skills"
Set-Junction ".opencode\agents"                             ".claude\agents"
Set-Junction ".opencode\commands"                           ".claude\commands"
Set-Junction ".opencode\mcp-servers"                        ".claude\mcp-servers"
Set-HardLink  ".opencode\settings.json"                     ".claude\settings.json"

Write-Output "`n== MCP traduzido para VS Code e OpenCode (schemas diferentes, gerados por script) =="
node "$raiz\scripts\sincronizar-mcp-vscode.mjs"
node "$raiz\scripts\sincronizar-mcp-opencode.mjs"

Write-Output "`n== Hook pre-commit (R16 - copia, .git\hooks nao aceita link) =="
$hookSrc = Join-Path $raiz "scripts\hooks\pre-commit"
$hookDst = Join-Path $raiz ".git\hooks\pre-commit"
Copy-Item -Path $hookSrc -Destination $hookDst -Force
Write-Output "Copiado: scripts\hooks\pre-commit -> .git\hooks\pre-commit"

Write-Output "`nConcluido."
