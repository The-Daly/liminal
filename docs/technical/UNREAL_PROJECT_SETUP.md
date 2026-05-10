# Unreal Project Setup

This repo now contains a content-first Unreal Engine 5 scaffold:

```text
LiminalDominion.uproject
Config/
Content/
Source_Legacy/
```

The active project path is visualization-first. The archived C++ gameplay scaffold lives in `Source_Legacy/` and should stay there until the Windows MSVC toolchain is fully ready.

## Recommended Engine

- Unreal Engine 5.7 on Windows.
- Windows 10/11 PC remains the primary playable packaged build target.
- macOS is still acceptable for docs, planning, and data work.
- If legacy C++ modules are re-enabled later, install Visual Studio 2022 Build Tools with the MSVC v143 x64/x86 toolchain and a Windows 10/11 SDK first.

## Windows Startup Command

From PowerShell in the repo root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_windows_unreal.ps1
```

This startup script validates seed data, exports DataTables, ensures `Content/Maps`, `Content/Blueprints`, `Content/Data`, and `Content/UI` exist, and launches Unreal Editor into the repo-owned hub map. If code modules are re-enabled later, it can also generate project files and build the editor target.

For the first automated placeholder pass after the maps exist, close the editor and run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_unreal_first_pass.ps1
```

That pass safely creates the first Blueprint and widget placeholders and places them into the repo-owned maps.

For the current shell-layout automation pass after the placeholder assets exist, close the editor and run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_unreal_graybox_layout.ps1
```

That pass stamps the current hub, personal room, and Level 1 Service Halls graybox geometry into the repo-owned maps.
It also adds route signage and objective pads for the current smoke-test flow.

## First Open

1. Install Unreal Engine 5 through Epic Games Launcher.
2. Run the startup script above or open `LiminalDominion.uproject` directly.
3. Let the project open into `LD_Hub_Greybox`.
4. If the repo-owned maps do not exist yet, immediately save the current level into `Content/Maps/LD_Hub_Greybox`.
5. Create or duplicate and save if needed:
   - `Content/Maps/LD_PersonalRoom_Greybox`
   - `Content/Maps/LD_Level1_ServiceHalls_Greybox`
6. Set `LD_Hub_Greybox` as the startup map after the first save so the repo opens into a repo-owned world.

## First Blueprint Pass

For the current content-first pass, create Blueprint-only placeholder assets under `Content/Blueprints`:

- `BP_LDPlayer`
- `BP_LDGameMode`
- `BP_DeploymentGate`
- `BP_LootContainer`
- `BP_ExtractionTrigger_Stable`
- `BP_ExtractionTrigger_HiddenTicketBooth`
- `BP_PersonalStorage`
- `BP_FactionVaultPlaceholder`
- `BP_ProjectBoard`
- `BP_FlickerStalker`

Create UI assets under `Content/UI`:

- `WBP_PlayerHUD`
- `WBP_RunResult`

If the legacy C++ module path is re-enabled later, these Blueprint assets can be reparented to the archived gameplay classes instead of being recreated.

The current `run_unreal_first_pass.ps1` script creates these placeholder assets automatically if they are missing, then places them into the current graybox maps. The `run_unreal_graybox_layout.ps1` script then adds the first shell geometry and landmark layout around them.

## Input And HUD Contract

`Config/DefaultInput.ini` already reserves the first-pass controls:

- `WASD`: move
- mouse: look
- `Space`: jump
- `E`: interact
- `Q`: consume Almond Water
- `K`: debug death

The first HUD pass should display:

- sanity
- carried inventory stacks
- interaction prompt text
- player feedback messages
- extraction/death result state

## Data Import

Before importing data on Windows:

```powershell
py -3 scripts/validate_seed_data.py
py -3 scripts/export_unreal_datatables.py
```

Import CSV files from:

```text
generated/unreal_datatables/
```

Import at least:

- `DT_Items.csv`
- `DT_LootTables.csv`
- `DT_Extractions.csv`
- `DT_Storage.csv`
- `DT_Sanity.csv`

Place the imported assets under `Content/Data`. The first required dependency is `DT_Items`, because that drives stackability, max-stack limits, storage UI readouts, and loot pickup behavior.

Current limitation on Windows with UE 5.7:

- automated CSV-to-DataTable import through Python currently crashes when the row struct is Python-generated
- placeholder assets and map placement can be automated safely
- DataTable import should still be completed manually in the editor until the project has native or editor-authored row structs

`Config/DefaultGame.ini` still reserves `ItemDataTablePath` and local save-slot settings for the later legacy-C++ reactivation path.

## First Playable Milestone

The first editor milestone is not polish. It is this readable loop:

1. Start in `LD_Hub_Greybox`.
2. Enter or transition to `LD_PersonalRoom_Greybox`.
3. Deploy into `LD_Level1_ServiceHalls_Greybox`.
4. Pick up loot from at least one container.
5. Watch sanity drain.
6. Consume Almond Water.
7. Encounter a Flicker Stalker placeholder.
8. Extract through the stable exit.
9. Return to the personal room.
10. Deposit loot into personal storage.
11. Contribute Movie Tickets and scrap to the Signal Lamp Project.
12. Trigger death in a second run and confirm carried inventory clears while personal storage remains.

## Local SaveGame Persistence

V0.1 save behavior should remain local-only.

The reserved slot config in `Config/DefaultGame.ini` is:

```ini
[/Script/LiminalDominion.LDSaveGameSubsystem]
SaveSlotName=LiminalDominionV0
UserIndex=0
```

If the current content-only pass needs persistence before the legacy C++ bridge returns, use Blueprint/local SaveGame placeholders that preserve:

- selected faction ID
- personal storage stacks
- completed hub upgrade IDs
- simple run history entries

## Legacy C++ Reactivation

Only do this after the Windows toolchain is fixed:

1. Restore `Source_Legacy/` back to `Source/`.
2. Re-enable module entries in `LiminalDominion.uproject`.
3. Generate project files.
4. Rebuild the editor target.
5. Reparent Blueprint placeholders to the gameplay classes as needed.

## Windows Build Gate

Before any playtest release:

- package for Windows
- run the full smoke test on Windows
- confirm input, UI scaling, save paths, data import, extraction, death wipe, and sanity behavior
- commit only source/config/content assets that belong in git
