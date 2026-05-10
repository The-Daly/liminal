$projectRoot = Split-Path -Parent $PSScriptRoot
$uproject = Join-Path $projectRoot "LiminalDominion.uproject"
$editorCmd = "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
$scriptPath = Join-Path $projectRoot "scripts\unreal_graybox_layout.py"

if (-not (Test-Path $editorCmd)) {
    throw "UnrealEditor-Cmd.exe was not found at $editorCmd"
}

if (-not (Test-Path $uproject)) {
    throw "Project file was not found at $uproject"
}

if (-not (Test-Path $scriptPath)) {
    throw "Graybox layout script was not found at $scriptPath"
}

if (Get-Process UnrealEditor -ErrorAction SilentlyContinue) {
    throw "Close Unreal Editor before running the automated graybox layout pass."
}

& $editorCmd $uproject "-ExecutePythonScript=$scriptPath" -unattended -nop4 -nosplash -NoSound
if ($LASTEXITCODE -ne 0) {
    throw "Unreal graybox layout pass failed with exit code $LASTEXITCODE"
}
