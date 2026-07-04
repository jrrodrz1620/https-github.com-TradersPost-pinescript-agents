# setup_brain.ps1: one-command second brain setup (Gemini free tier).
# Run:  .\setup_brain.ps1
# It asks for your API key, wires .env, and tests the connection.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host ""
Write-Host "Get your key at aistudio.google.com/apikey (click Copiar clave / Copy key)."
$k = Read-Host "Now PASTE the key here (right-click pastes in PowerShell), then press Enter"
$k = $k.Trim().Trim('"').Trim("'")

if (-not $k) {
    Write-Host "Nothing was pasted. Run .\setup_brain.ps1 again, paste first, then Enter." -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }

# Last line wins in the wrapper, so appending overrides any earlier mess
Add-Content .env ""
Add-Content .env "SECOND_BRAIN_URL=https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
Add-Content .env "SECOND_BRAIN_MODEL=gemini-2.5-flash"
Add-Content .env "SECOND_BRAIN_KEY=$k"

Write-Host "Saved. Testing the second brain..." -ForegroundColor Cyan
$answer = & "$PSScriptRoot\bin\grok-ask.ps1" "Reply with the single word: ready"
if ($LASTEXITCODE -eq 0 -and $answer) {
    Write-Host "Second brain says: $answer" -ForegroundColor Green
    Write-Host "Setup complete. Gemini is wired in."
} else {
    Write-Host "Test failed, see the error above. Most common cause: an incomplete key. Run .\setup_brain.ps1 again." -ForegroundColor Yellow
    exit 1
}
