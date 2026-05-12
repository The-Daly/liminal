$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$projectFile = Join-Path $repoRoot "LiminalDominion.uproject"
$pythonScript = Join-Path $repoRoot "scripts\unreal_ingame_menu_spawn.py"
$editorCmd = "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"

if (-not (Test-Path $editorCmd)) {
    throw "UnrealEditor-Cmd.exe not found at $editorCmd"
}

if (-not (Test-Path $projectFile)) {
    throw "Project file not found at $projectFile"
}

if (-not (Test-Path $pythonScript)) {
    throw "Python in-game menu script not found at $pythonScript"
}

& $editorCmd $projectFile "-ExecutePythonScript=$pythonScript" -unattended -nop4

if ($LASTEXITCODE -ne 0) {
    throw "Unreal in-game menu spawn pass failed with exit code $LASTEXITCODE"
}

Write-Host "Unreal in-game menu spawn pass complete."
