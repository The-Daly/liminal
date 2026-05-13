$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$projectFile = Join-Path $repoRoot "LiminalDominion.uproject"
$editorCmd = "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
$buildBat = "C:\Program Files\Epic Games\UE_5.7\Engine\Build\BatchFiles\Build.bat"
$pythonScript = Join-Path $repoRoot "scripts\unreal_data_bootstrap.py"
$statusFile = Join-Path $repoRoot "outputs\unreal_data_bootstrap_status.json"

if (-not (Test-Path $editorCmd)) {
    throw "UnrealEditor-Cmd.exe not found at $editorCmd"
}

if (-not (Test-Path $buildBat)) {
    throw "Build.bat not found at $buildBat"
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

Write-Host "Building native LiminalDominion data-row module..."
& $buildBat LiminalDominionEditor Win64 Development $projectFile -WaitMutex -NoHotReloadFromIDE
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Native module build failed. Falling back to editor-authored struct assets if they exist."
    Write-Warning "If no struct assets exist yet, create them using docs/technical/DATATABLE_IMPORT_FIX_PLAN.md."
}

Write-Host "Running Unreal data bootstrap..."
if (Test-Path $statusFile) {
    Remove-Item $statusFile -Force
}

& $editorCmd $projectFile "-ExecutePythonScript=$pythonScript" -unattended -nop4
if ($LASTEXITCODE -ne 0) {
    throw "Unreal data bootstrap failed with exit code $LASTEXITCODE"
}

if (-not (Test-Path $statusFile)) {
    throw "Unreal data bootstrap did not produce a status file. Check Unreal logs."
}

$status = Get-Content $statusFile | ConvertFrom-Json
if (-not $status.success) {
    throw "Unreal data bootstrap failed: $($status.message)"
}

Write-Host "Unreal data bootstrap complete."
