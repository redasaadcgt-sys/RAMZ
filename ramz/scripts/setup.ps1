Write-Host "=== RAMZ Compiler Setup ==="


$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$VenvScripts = Join-Path $ProjectRoot ".venv\Scripts"

if (!(Test-Path (Join-Path $ProjectRoot "pyproject.toml"))) {
    Write-Host "Could not locate the Ramz project root."
    exit 1
}

# 0. Check Python exists
$python = Get-Command python -ErrorAction SilentlyContinue

if (-not $python) {
    Write-Host "Python is not installed or not in PATH."
    exit 1
}

Write-Host "Python found at $($python.Source)"

# 1. Create venv
if (!(Test-Path "$ProjectRoot\.venv")) {
    python -m venv "$ProjectRoot\.venv"
}

# 2. Upgrade pip 
& $VenvPython -m pip install --upgrade pip

# 3. Install dependencies 
& $VenvPython -m pip install -r "$ProjectRoot\requirements.txt"

# 4. Install RAMZ 
Write-Host "Installing RAMZ (editable mode)"
& $VenvPython -m pip install -e "$ProjectRoot"

# 5. LLVM setup
Write-Host "Running LLVM setup..."
& "$ProjectRoot\scripts\install_llvm.ps1"

$llvmBin = [Environment]::GetEnvironmentVariable(
    "RAMZ_LLVM_BIN",
    "User"
)

# 6. Add to PATH 
Write-Host "Adding ramz to PATH..."

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $userPath) { $userPath = "" }

$pathList = $userPath -split ";" | ForEach-Object { $_.Trim() }

$venvNormalized = $VenvScripts.TrimEnd("\").ToLower()

$pathListNormalized = $pathList | ForEach-Object {
    $_.TrimEnd("\").ToLower()
}

if ($pathListNormalized -notcontains $venvNormalized) {

    $newPath = ($pathList + $VenvScripts) -join ";"

    [Environment]::SetEnvironmentVariable(
        "Path",
        $newPath,
        "User"
    )

    Write-Host "Ramz added to PATH"
}
else {
    Write-Host "Ramz already in PATH"
}

# update current session PATH

foreach ($path in @($VenvScripts, $llvmBin)) {

    if ($path) {

        $normalized = $path.TrimEnd("\").ToLower()

        $currentPathNormalized = $env:Path -split ";" | ForEach-Object {
            $_.Trim().TrimEnd("\").ToLower()
        }

        if ($currentPathNormalized -notcontains $normalized) {
            $env:Path += ";$path"
        }
    }
}

Write-Host ""
Write-Host "Setup complete"