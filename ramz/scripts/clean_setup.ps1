Write-Host "Removing Ramz from PATH..."

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvScripts = Join-Path $ProjectRoot ".venv\Scripts"

$venvScriptsNormalized = $VenvScripts.Trim().TrimEnd("\").ToLower()

# Remove from User PATH
$userPath = [Environment]::GetEnvironmentVariable(
    "Path",
    "User"
)

if ($userPath) {

    $newPath = (
        $userPath -split ";" |
        Where-Object {
            $_.Trim().TrimEnd("\").ToLower() -ne $venvScriptsNormalized
        }
    ) -join ";"

    [Environment]::SetEnvironmentVariable(
        "Path",
        $newPath,
        "User"
    )

    Write-Host "Ramz removed from User PATH"
}

# Remove from current PowerShell session PATH
$currentPath = (
    $env:Path -split ";" |
    Where-Object {
        $_.Trim().TrimEnd("\").ToLower() -ne $venvScriptsNormalized
    }
) -join ";"

$env:Path = $currentPath

Write-Host "Running LLVM cleaning..."
& "$ProjectRoot\scripts\clean_llvm.ps1"

Write-Host ""
Write-Host "Done"