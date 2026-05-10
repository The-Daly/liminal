$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$projectFile = Join-Path $repoRoot "LiminalDominion.uproject"
$editorCmd = "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
$pythonScript = Join-Path $repoRoot "scripts\unreal_data_bootstrap.py"

if (-not (Test-Path $editorCmd)) {
    throw "UnrealEditor-Cmd.exe not found at $editorCmd"
}

if (-not (Test-Path $projectFile)) {
    throw "Project file not found at $projectFile"
}

if (-not (Test-Path $pythonScript)) {
    throw "Python bootstrap script not found at $pythonScript"
}

$runningEditor = Get-Process UnrealEditor -ErrorAction SilentlyContinue
if ($runningEditor) {
    throw "Unreal Editor is running. Close it before running the data bootstrap."
}

Write-Host "Running Unreal data bootstrap..."
& $editorCmd $projectFile "-ExecutePythonScript=$pythonScript" -unattended -nop4
if ($LASTEXITCODE -ne 0) {
    throw "Unreal data bootstrap failed with exit code $LASTEXITCODE"
}

Write-Host "Unreal data bootstrap complete."
