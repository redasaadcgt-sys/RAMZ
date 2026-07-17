Write-Host "=== RAMZ Refresh ==="

# Project root (parent of the scripts folder)
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (!(Test-Path $VenvPython)) {
    Write-Host "Virtual environment not found. Run setup first."
    exit 1
}

Write-Host "Refreshing RAMZ..."

& $VenvPython -m pip install -e $ProjectRoot

if ($LASTEXITCODE -ne 0) {
    Write-Host "Refresh failed."
    exit 1
}

Write-Host "Refresh complete."