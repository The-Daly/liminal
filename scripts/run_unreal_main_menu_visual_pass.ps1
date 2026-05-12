$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$projectFile = Join-Path $repoRoot "LiminalDominion.uproject"
$pythonScript = Join-Path $repoRoot "scripts\unreal_main_menu_visual_pass.py"
$editorCmd = "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"

if (-not (Test-Path $editorCmd)) {
    throw "UnrealEditor-Cmd.exe not found at $editorCmd"
}

if (-not (Test-Path $projectFile)) {
    throw "Project file not found at $projectFile"
}

if (-not (Test-Path $pythonScript)) {
    throw "Python visual layout script not found at $pythonScript"
}

& $editorCmd $projectFile "-ExecutePythonScript=$pythonScript" -unattended -nop4

if ($LASTEXITCODE -ne 0) {
    throw "Unreal main menu visual pass failed with exit code $LASTEXITCODE"
}

Write-Host "Unreal main menu visual pass complete."
