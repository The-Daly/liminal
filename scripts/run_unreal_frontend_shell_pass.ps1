$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$firstPass = Join-Path $repoRoot "scripts\run_unreal_first_pass.ps1"
$visualPass = Join-Path $repoRoot "scripts\run_unreal_main_menu_visual_pass.ps1"
$ingamePass = Join-Path $repoRoot "scripts\run_unreal_ingame_menu_spawn.ps1"
$wiringPass = Join-Path $repoRoot "scripts\run_unreal_blueprint_data_wiring.ps1"
$defaultsPass = Join-Path $repoRoot "scripts\run_unreal_frontend_state_defaults.ps1"

if (-not (Test-Path $firstPass)) {
    throw "Missing first-pass script at $firstPass"
}

if (-not (Test-Path $wiringPass)) {
    throw "Missing blueprint wiring script at $wiringPass"
}

if (-not (Test-Path $visualPass)) {
    throw "Missing main-menu visual script at $visualPass"
}

if (-not (Test-Path $ingamePass)) {
    throw "Missing in-game menu script at $ingamePass"
}

if (-not (Test-Path $defaultsPass)) {
    throw "Missing frontend defaults script at $defaultsPass"
}

& powershell -ExecutionPolicy Bypass -File $firstPass
& powershell -ExecutionPolicy Bypass -File $visualPass
& powershell -ExecutionPolicy Bypass -File $ingamePass
& powershell -ExecutionPolicy Bypass -File $wiringPass
& powershell -ExecutionPolicy Bypass -File $defaultsPass

Write-Host "Unreal frontend shell pass complete."
