# Current Status

This file replaces the old starter-pack mental model with the current repo state.

## Project State

- Platform focus: Windows + Unreal Engine 5.7.
- Project mode: content-first, Blueprint-first graybox prototype.
- Active Unreal project: `LiminalDominion.uproject`.
- Active git branch target: `main`.
- Current Unreal direction: build the first readable playable loop, not final art and not multiplayer.

## What Exists Now

### Repo + Validation

- Seed validation, cross-reference checking, duplicate-ID checking, and Unreal CSV export are working.
- `py -3 scripts/preflight_release.py` passes on Windows.
- The repo-side Python layer covers inventory, capped storage overflow, sanity, extractions, project-board contribution, playable-loop simulation, persistence payloads, loadouts, loot density, navigation markers, weapons/ammo, and social rules.

### Unreal Project

- The Unreal project opens into `LD_Hub_Greybox`.
- Repo-owned maps exist:
  - `Content/Maps/LD_Hub_Greybox.umap`
  - `Content/Maps/LD_PersonalRoom_Greybox.umap`
  - `Content/Maps/LD_Level1_ServiceHalls_Greybox.umap`
- Placeholder Blueprint assets exist under `Content/Blueprints`.
- Placeholder UI widgets exist under `Content/UI`.
- The automated graybox pass now stamps:
  - shell geometry
  - route landmarks
  - objective pads
  - smoke-test signage

### Current Unreal Automation

- `scripts/start_windows_unreal.ps1`
  - validates data, exports CSVs, ensures repo-owned folders exist, launches Unreal
- `scripts/run_unreal_first_pass.ps1`
  - creates placeholder Blueprint and widget assets if missing
- `scripts/run_unreal_graybox_layout.ps1`
  - stamps the current map shell, route layout, and smoke-test path markers

## What Is Working

- Windows-first repo workflow
- clean local commits and pushes to GitHub
- Unreal opens from the repo-owned project
- graybox maps exist and are versioned
- placeholder hub/personal-room/service-halls spaces exist
- route readability and playtest signage now exist in the maps
- repo-side simulation of the intended loop exists

## What Is Not Done Yet

- DataTables are not safely imported into Unreal yet.
- Most Blueprint actors are still placeholders with little or no behavior.
- The first full interactive deploy -> loot -> sanity -> encounter -> extract -> deposit -> contribute loop is not wired in-editor yet.
- SaveGame and persistence are not yet bridged through Blueprint runtime behavior.
- HUD widgets exist but are not yet driving a real player loop.

## Current Blockers

### DataTable Import

- Automated Python DataTable import is currently unsafe in UE 5.7 when using Python-generated row structs.
- `Content/Python/ld_datatable_rows.py` is useful as a field reference, but not as the safe final import path.
- The practical next move is to create editor-authored row structs or a native struct path, then manually import the CSVs.

### Blueprint Wiring

- The world is readable enough to test flow, but the core interaction actors are not fully wired.
- The next high-value step is interaction wiring, not more static layout.

## Most Important Current Files

- `docs/status/Liminal_Project_Status_2026-05-10.xlsx`
- `docs/systems/PLAYABLE_LOOP_CONTRACT.md`
- `docs/technical/UNREAL_PROJECT_SETUP.md`
- `scripts/unreal_first_pass_setup.py`
- `scripts/unreal_graybox_layout.py`
- `generated/unreal_datatables/`

## Immediate Direction

The repo is ready for a Codex pass focused on:

1. safe Unreal DataTable import planning
2. Blueprint wiring for deployment, loot, extraction, storage, and project board
3. the first real in-editor smoke-test loop
