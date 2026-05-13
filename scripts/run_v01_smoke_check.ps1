$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

Write-Host "== Liminal Dominion V0.1 Smoke Check ==" -ForegroundColor Cyan
Write-Host "Repo: $repoRoot"

Write-Host ""
Write-Host "[1/3] Validate seed data" -ForegroundColor Yellow
py -3 scripts/validate_seed_data.py

Write-Host ""
Write-Host "[2/3] Export Unreal CSVs" -ForegroundColor Yellow
py -3 scripts/export_unreal_datatables.py

Write-Host ""
Write-Host "[3/3] Run unit tests" -ForegroundColor Yellow
py -3 -m unittest discover -s tests -v

Write-Host ""
Write-Host "Smoke-check prerequisites passed." -ForegroundColor Green
Write-Host ""
Write-Host "Next Unreal manual test:"
Write-Host "1. Open LiminalDominion.uproject"
Write-Host "2. Press Play"
Write-Host "3. Walk this flow:"
Write-Host "   title -> server -> character -> faction -> setup -> main menu -> deploy -> loot -> sanity -> encounter -> extract -> deposit -> contribute"
Write-Host ""
Write-Host "Checklist doc:"
Write-Host "docs/testing/V0_1_SMOKE_TEST.md"
