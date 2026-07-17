Write-Host "=== LLVM Detection ==="

$ProjectRoot = Split-Path -Parent $PSScriptRoot

$toolchainDir = Join-Path $ProjectRoot "toolchain\LLVM"
$programLLVM  = "C:\Program Files\LLVM\bin\clang.exe"


function Set-RamzLLVM($clangExe) {

    $binPath = Split-Path $clangExe
    $binPathNormalized = $binPath.TrimEnd("\").ToLower()

    Write-Host "LLVM found at: $binPath"

    # store env var
    $env:RAMZ_LLVM_BIN = $binPath
    [Environment]::SetEnvironmentVariable("RAMZ_LLVM_BIN", $binPath, "User")

    # read USER PATH only
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if (-not $userPath) { $userPath = "" }

    $pathList = $userPath -split ";" | ForEach-Object {
        $_.Trim().TrimEnd("\")
    }

    # normalize for comparison ONLY
    $pathListNormalized = $pathList | ForEach-Object { $_.ToLower() }

    if ($pathListNormalized -notcontains $binPathNormalized) {

        Write-Host "Adding LLVM to PATH..."

        # IMPORTANT: store original (NOT normalized)
        $newPath = if ($userPath) {
            "$userPath;$binPath"
        } else {
            $binPath
        }

        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    }
    else {
        Write-Host "LLVM already in PATH"
    }
}


# 1. Bundled LLVM
$toolchainClang = Join-Path $toolchainDir "bin\clang.exe"
if (Test-Path $toolchainClang) {
    Set-RamzLLVM $toolchainClang
    return
}

# 2. Program Files LLVM
if (Test-Path $programLLVM) {
    Set-RamzLLVM $programLLVM
    return
}

# 3. System PATH LLVM
$clangCmd = Get-Command clang -ErrorAction SilentlyContinue
if ($clangCmd) {
    Set-RamzLLVM $clangCmd.Source
    return
}

# FAILURE
Write-Host ""
Write-Host "LLVM NOT FOUND"
Write-Host "Please install LLVM or place it in one of:"
Write-Host "  - C:\Program Files\LLVM"
Write-Host "  - toolchain\LLVM"

exit 1