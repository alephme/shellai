# PowerShell wrapper for the `ai` command-line tool.
#
# HOW IT WORKS:
#   1. Calls `ai.exe -p <your prompt>` → Python generates the command, prints it raw.
#   2. Displays the command and asks for confirmation (y/n/e).
#   3. Runs it with Invoke-Expression — IN YOUR CURRENT SHELL.
#
#   This means `cd`, `Set-Location`, environment changes, and all other side
#   effects actually stick around in your session.
#
# MANAGED BY: `ai --setup` / `ai --teardown`

function ai {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Args
    )

    $prompt = $Args -join ' '
    $first = $Args[0]

    # ---- Special commands: pass through to ai.exe directly ----
    $special = @("--setup", "--teardown", "-c", "--clip", "--print", "--help")
    if ($first -in $special) {
        ai.exe @Args
        return
    }

    if (-not $prompt) {
        Write-Host @"

ai — AI Command Generator

Usage: ai <natural language description>

Examples:
  ai list all PDF files modified in the last 7 days
  ai find processes using port 3000 and kill them
  ai convert all .png files in current directory to .webp
"@
        return
    }

    Write-Host "`nGenerating command..." -ForegroundColor Yellow
    $cmd = ai.exe -p @Args 2>$null

    if ($LASTEXITCODE -ne 0 -or -not $cmd) {
        Write-Host "Error: Failed to generate command." -ForegroundColor Red
        return
    }

    Write-Host "`nGenerated Command:" -ForegroundColor Cyan
    Write-Host "  $cmd`n" -ForegroundColor Yellow

    $choice = Read-Host "Execute this command? (y/n/e)"
    switch ($choice) {
        'y' {
            Write-Host "`nExecuting...`n" -ForegroundColor Green
            Invoke-Expression $cmd
        }
        'n' {
            Write-Host "Cancelled." -ForegroundColor Gray
        }
        'e' {
            $edited = Read-Host "Edit command" -Default $cmd
            if ($edited) {
                Write-Host "`nExecuting...`n" -ForegroundColor Green
                Invoke-Expression $edited
            } else {
                Write-Host "Cancelled." -ForegroundColor Gray
            }
        }
        default {
            Write-Host "Invalid choice, cancelled." -ForegroundColor Gray
        }
    }
}
