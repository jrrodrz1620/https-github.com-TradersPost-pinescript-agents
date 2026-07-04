# grok-ask.ps1: send a prompt to the second brain and print ONLY the answer.
# Usage: .\bin\grok-ask.ps1 "prompt"    or    $prompt | .\bin\grok-ask.ps1
#
# The second brain is any OpenAI-compatible chat API, configured in .env:
#   SECOND_BRAIN_URL   (default https://api.x.ai/v1/chat/completions)
#   SECOND_BRAIN_MODEL (default grok-4)
#   SECOND_BRAIN_KEY   (falls back to XAI_API_KEY)
# Works with xAI Grok, Google Gemini, Kimi/Moonshot, DeepSeek, OpenRouter,
# Groq, Mistral. See .env.example for ready-made configs.

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

function Get-EnvValue([string]$Name) {
    $v = [Environment]::GetEnvironmentVariable($Name)
    if (-not $v -and (Test-Path ".env")) {
        $line = Select-String -Path ".env" -Pattern "^$Name=" | Select-Object -First 1
        if ($line) { $v = $line.Line.Split("=", 2)[1].Trim().Trim('"').Trim("'") }
    }
    return $v
}

$apiKey = Get-EnvValue "SECOND_BRAIN_KEY"
if (-not $apiKey) { $apiKey = Get-EnvValue "XAI_API_KEY" }
$url = Get-EnvValue "SECOND_BRAIN_URL"
if (-not $url) { $url = "https://api.x.ai/v1/chat/completions" }
$model = Get-EnvValue "SECOND_BRAIN_MODEL"
if (-not $model) { $model = "grok-4" }

if (-not $apiKey) {
    Write-Error "grok-ask: no API key. Set SECOND_BRAIN_KEY (or XAI_API_KEY) in .env"
    exit 1
}

$body = @{
    model       = $model
    messages    = @(@{ role = "user"; content = $Prompt })
    temperature = 0.3
} | ConvertTo-Json -Depth 6

try {
    $resp = Invoke-RestMethod -Uri $url `
        -Method Post `
        -Headers @{ Authorization = "Bearer $apiKey" } `
        -ContentType "application/json" `
        -Body $body `
        -TimeoutSec 300
    $answer = $resp.choices[0].message.content
    if ($answer) {
        Write-Output $answer
    } else {
        Write-Error "grok-ask: no answer from $model, raw response follows"
        Write-Error ($resp | ConvertTo-Json -Depth 6)
        exit 1
    }
} catch {
    Write-Error "grok-ask: request to $url failed: $_"
    exit 1
}
