# grok-ask.ps1: send a prompt to xAI's Grok API and print ONLY the answer.
# Usage: .\bin\grok-ask.ps1 "prompt"    or    Get-Content prompt.txt | .\bin\grok-ask.ps1
# Needs XAI_API_KEY in the environment or in a local .env file.

param(
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [string]$Prompt
)

$ErrorActionPreference = "Stop"

if (-not $Prompt) {
    # Pipeline input first (PowerShell-to-PowerShell), raw stdin as fallback
    $Prompt = ($input | Out-String)
    if (-not $Prompt.Trim()) { $Prompt = [Console]::In.ReadToEnd() }
}
if (-not $Prompt) {
    Write-Error "grok-ask: no prompt given (argument or stdin)"
    exit 1
}

$apiKey = $env:XAI_API_KEY
if (-not $apiKey -and (Test-Path ".env")) {
    $line = Select-String -Path ".env" -Pattern "^XAI_API_KEY=" | Select-Object -First 1
    if ($line) { $apiKey = $line.Line.Split("=", 2)[1].Trim().Trim('"').Trim("'") }
}
if (-not $apiKey) {
    Write-Error "grok-ask: XAI_API_KEY not set (env or .env), cannot reach Grok"
    exit 1
}

$body = @{
    model       = "grok-4"
    messages    = @(@{ role = "user"; content = $Prompt })
    temperature = 0.3
} | ConvertTo-Json -Depth 6

try {
    $resp = Invoke-RestMethod -Uri "https://api.x.ai/v1/chat/completions" `
        -Method Post `
        -Headers @{ Authorization = "Bearer $apiKey" } `
        -ContentType "application/json" `
        -Body $body `
        -TimeoutSec 300
    $answer = $resp.choices[0].message.content
    if ($answer) {
        Write-Output $answer
    } else {
        Write-Error "grok-ask: no answer from Grok, raw response follows"
        Write-Error ($resp | ConvertTo-Json -Depth 6)
        exit 1
    }
} catch {
    Write-Error "grok-ask: request failed: $_"
    exit 1
}
