param([switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$webRoot = Join-Path $projectRoot 'web'
$port = 11451
$url = "http://127.0.0.1:$port/OI-in-XCPC/"

try {
    $Host.UI.RawUI.WindowTitle = 'OI in XCPC - Close this window to stop'
    $node = (Get-Command node.exe -ErrorAction Stop).Source
    $vite = Join-Path $webRoot 'node_modules\vite\bin\vite.js'
    if (-not (Test-Path -LiteralPath $vite)) {
        throw 'Dependencies missing. Run npm install in the web directory first.'
    }
    $existing = $false
    try {
        $response = Invoke-WebRequest -Uri ($url + 'favicon.svg') -UseBasicParsing -TimeoutSec 2
        $existing = $response.StatusCode -eq 200 -and $response.Content -match '#153e75'
    } catch { }
    if ($existing) {
        if (-not $NoBrowser) { Start-Process $url }
        Write-Host 'Already running. Use the original server window to stop the application.'
        if (-not $NoBrowser) { Start-Sleep -Seconds 3 }
        exit 0
    }
    Set-Location -LiteralPath $webRoot
    Write-Host 'Close this terminal window or press Ctrl+C to stop OI in XCPC.' -ForegroundColor Cyan
    $viteArgs = @($vite, '--host', '127.0.0.1', '--port', "$port", '--strictPort')
    if (-not $NoBrowser) { $viteArgs += @('--open', '/OI-in-XCPC/') }
    & $node @viteArgs
    if ($LASTEXITCODE -ne 0) { throw "Server exited with code $LASTEXITCODE." }
} catch {
    if ($NoBrowser) { throw }
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host 'Press Enter to close'
    exit 1
}
