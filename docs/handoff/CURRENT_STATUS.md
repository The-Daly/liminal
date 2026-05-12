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
- Frontend shell widget targets are now defined for title, server browser, character selection, faction selection, character setup, and main player menu.
- Blueprint data-contract variables now exist on the first-wave interaction actors, the player shell, the game mode shell, the menu flow controller, and the serious frontend widgets.
- The placed graybox actors are now stamped with repo-owned prompts, run IDs, extraction IDs, storage IDs, hub-upgrade IDs, and map-return paths.
- The automated graybox pass now stamps:
  - shell geometry
  - route landmarks
  - objective pads
  - smoke-test signage
  - first-pass interaction metadata on placed Blueprint instances
  - a serious frontend staging wing inside the hub with menu controller placement and operator/faction preview anchors

### Current Unreal Automation

- `scripts/start_windows_unreal.ps1`
  - validates data, exports CSVs, ensures repo-owned folders exist, launches Unreal
- `scripts/run_unreal_first_pass.ps1`
  - creates placeholder Blueprint and widget assets if missing
- `scripts/run_unreal_blueprint_data_wiring.ps1`
  - adds the first Blueprint-side data variables needed for the deploy -> loot -> extract -> store -> contribute loop
- `scripts/run_unreal_frontend_shell_pass.ps1`
  - refreshes the serious frontend shell widgets, menu controller variables, and default frontend state
- `scripts/run_unreal_frontend_state_defaults.ps1`
  - stamps default title/server/faction/character/main-menu values into the frontend controller and widgets
- `WBP_CharacterSelection`
  - now exists as a dedicated shell between server browser and faction selection/main player hub
- `scripts/run_unreal_data_bootstrap.ps1`
  - attempts the eight-table Unreal import pass and currently serves as the reproducible UE 5.7 crash harness for Python-defined row structs
- `scripts/run_unreal_graybox_layout.ps1`
  - stamps the current map shell, route layout, smoke-test path markers, and first-wave interaction metadata

## What Is Working

- Windows-first repo workflow
- clean local commits and pushes to GitHub
- Unreal opens from the repo-owned project
- graybox maps exist and are versioned
- placeholder hub/personal-room/service-halls spaces exist
- route readability and playtest signage now exist in the maps
- first-wave Blueprint assets now carry instance-editable data variables for prompts, IDs, and target map paths
- the current graybox maps now place deployment, loot, extraction, storage, project-board, and Flicker Stalker actors with loop-specific metadata
- `Config/DefaultGame.ini` now points at the intended DataTable asset paths and the default map/run IDs for the V0.1 loop
- persistent-world contract seeds now exist for server realms, wipe schedules, minimal character appearance presets, and menu routes
- repo-side menu helpers now generate title copy, server browser summaries, faction-lock warnings, character setup defaults, main-menu snapshots, and saved frontend session state
- the hub now contains a repo-owned serious frontend staging area for title/server/faction/character/main-menu visualization
- the frontend controller and serious widgets now carry repo-owned default realm/faction/wipe/callsign state in their class defaults
- repo-side simulation of the intended loop exists

## What Is Not Done Yet

- DataTables are still not safely imported into Unreal as assets under `Content/Data`.
- The serious frontend exists as a repo-side shell target, not yet as a fully interactive menu implementation.
- The serious frontend now has repo-backed state and summary helpers, but its UMG graphs are still shell-level rather than interactive.
- The serious frontend now has an in-world staging space and preview-anchor placements, but it is still not a clickable UMG flow yet.
- Most Blueprint actors now have their data contracts in place, but they still need real interaction graph behavior.
- The first full interactive deploy -> loot -> sanity -> encounter -> extract -> deposit -> contribute loop is not yet running in-editor.
- SaveGame and persistence are not yet bridged through Blueprint runtime behavior.
- HUD widgets exist but are not yet driving a real player loop.

## Current Blockers

### DataTable Import

- Automated Python DataTable import is now reproducibly crashing in UE 5.7 during `DT_Items` import when Python-generated row structs are used.
- `Content/Python/ld_datatable_rows.py` now covers the first eight loop-critical table shapes, but it remains a field reference, not the safe final import path.
- `scripts/run_unreal_data_bootstrap.ps1` is useful for regression-checking the crash, but the practical next move is still to replace the row-struct path with editor-authored or native structs.

### Blueprint Wiring

- The world is readable enough to test flow, and the placed actors now know which run/item/extraction/storage records they represent.
- The next high-value step is interaction graph wiring, not more static layout.

## Most Important Current Files

- `docs/status/Liminal_Project_Status_2026-05-10.xlsx`
- `docs/systems/PLAYABLE_LOOP_CONTRACT.md`
- `docs/technical/UNREAL_PROJECT_SETUP.md`
- `Config/DefaultGame.ini`
- `Content/Python/ld_datatable_rows.py`
- `scripts/unreal_first_pass_setup.py`
- `scripts/unreal_blueprint_data_wiring.py`
- `scripts/unreal_data_bootstrap.py`
- `scripts/unreal_graybox_layout.py`
- `scripts/frontend_menu_model.py`
- `scripts/persistent_world_model.py`
- `scripts/persistence_model.py`
- `generated/unreal_datatables/`

## Immediate Direction

The repo is ready for a Codex pass focused on:

1. replacing the crashing Python-row-struct DataTable import path with editor-authored or native structs
2. turning the menu controller and serious frontend widgets into an actual title -> server -> faction -> character -> main-menu flow
3. turning the stamped Blueprint metadata into real deployment, loot, extraction, storage, and board behavior
4. the first real in-editor smoke-test loop
