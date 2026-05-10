$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$projectFile = Join-Path $repoRoot "LiminalDominion.uproject"
$editorCmd = "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
$pythonScript = Join-Path $repoRoot "scripts\unreal_blueprint_data_wiring.py"

if (-not (Test-Path $editorCmd)) {
    throw "UnrealEditor-Cmd.exe not found at $editorCmd"
}

if (-not (Test-Path $projectFile)) {
    throw "Project file not found at $projectFile"
}

if (-not (Test-Path $pythonScript)) {
    throw "Python blueprint wiring script not found at $pythonScript"
}

$runningEditor = Get-Process UnrealEditor -ErrorAction SilentlyContinue
if ($runningEditor) {
    throw "Unreal Editor is running. Close it before running the blueprint data wiring pass."
}

Write-Host "Running Unreal blueprint data wiring..."
& $editorCmd $projectFile "-ExecutePythonScript=$pythonScript" -unattended -nop4
if ($LASTEXITCODE -ne 0) {
    throw "Unreal blueprint data wiring failed with exit code $LASTEXITCODE"
}

Write-Host "Unreal blueprint data wiring complete."
