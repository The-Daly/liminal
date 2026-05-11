$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$projectFile = Join-Path $repoRoot "LiminalDominion.uproject"
$editorCmd = "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
$pythonScript = Join-Path $repoRoot "scripts\unreal_frontend_state_defaults.py"

if (-not (Test-Path $editorCmd)) {
    throw "UnrealEditor-Cmd.exe not found at $editorCmd"
}

if (-not (Test-Path $projectFile)) {
    throw "Project file not found at $projectFile"
}

if (-not (Test-Path $pythonScript)) {
    throw "Python frontend defaults script not found at $pythonScript"
}

if (Get-Process UnrealEditor -ErrorAction SilentlyContinue) {
    throw "Unreal Editor is running. Close it before running the frontend defaults pass."
}

Write-Host "Running Unreal frontend state defaults..."
& $editorCmd $projectFile "-ExecutePythonScript=$pythonScript" -unattended -nop4
if ($LASTEXITCODE -ne 0) {
    throw "Unreal frontend state defaults failed with exit code $LASTEXITCODE"
}

Write-Host "Unreal frontend state defaults complete."
