Write-Host "=== Removing Ramz LLVM Configuration ==="

# Get stored LLVM path
$llvmBin = [Environment]::GetEnvironmentVariable(
    "RAMZ_LLVM_BIN",
    "User"
)

if ($llvmBin) {

    Write-Host "Removing LLVM path: $llvmBin"

    $llvmNormalized = $llvmBin.Trim().TrimEnd("\").ToLower()

    # Remove from persistent User PATH
    $userPath = [Environment]::GetEnvironmentVariable(
        "Path",
        "User"
    )

    if ($userPath) {

        $newPath = (
            $userPath -split ";" |
            Where-Object {
                $_.Trim().TrimEnd("\").ToLower() -ne $llvmNormalized
            }
        ) -join ";"

        [Environment]::SetEnvironmentVariable(
            "Path",
            $newPath,
            "User"
        )
    }

    # Remove from current PowerShell session PATH
    $currentPath = (
        $env:Path -split ";" |
        Where-Object {
            $_.Trim().TrimEnd("\").ToLower() -ne $llvmNormalized
        }
    ) -join ";"

    $env:Path = $currentPath

    # Remove stored LLVM variable
    [Environment]::SetEnvironmentVariable(
        "RAMZ_LLVM_BIN",
        $null,
        "User"
    )

    # Remove current process variable
    Remove-Item Env:RAMZ_LLVM_BIN -ErrorAction SilentlyContinue

    Write-Host "LLVM environment removed"
}
else {
    Write-Host "RAMZ LLVM variable not found"
}

Write-Host ""
Write-Host "LLVM cleanup complete"