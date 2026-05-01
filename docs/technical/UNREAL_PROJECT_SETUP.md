# Unreal Project Setup

This repo now contains a source-level Unreal Engine 5 scaffold:

```text
LiminalDominion.uproject
Config/
Content/
Source/
```

The current machine does not have Unreal Editor available, so the first editor compile still needs to happen on a Mac or Windows machine with UE5 installed.

## Recommended Engine

- Unreal Engine 5.x.
- Windows 10/11 PC remains the primary playable packaged build target.
- macOS is supported for development/editor iteration when Unreal supports the local hardware.
- On Windows, install Visual Studio 2022 with `Desktop development with C++` and a Windows 10/11 SDK before compiling this C++ project.

## Windows Startup Command

From PowerShell in the repo root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_windows_unreal.ps1
```

This startup script validates seed data, exports DataTables, creates the initial `Content/Maps`, `Content/Blueprints`, and `Content/Data` folders, and launches Unreal Editor. If code modules are enabled later, it also generates project files and builds the editor target.

## First Open

1. Install Unreal Engine 5 through Epic Games Launcher.
2. Open `LiminalDominion.uproject`.
3. If Unreal asks to rebuild modules, choose `Yes`.
4. If Unreal asks to generate project files, allow it.
5. Create these maps in `Content/Maps/`:
   - `LD_Hub_Greybox`
   - `LD_PersonalRoom_Greybox`
   - `LD_Level1_ServiceHalls_Greybox`
6. Set `LD_Hub_Greybox` as the startup map if the editor does not auto-resolve it.

## First Blueprint Pass

Create Blueprint children from the C++ skeletons:

- `BP_LDGameModeBase`
- `BP_LDPlayerCharacter`
- `WBP_PlayerHUD`
- `WBP_RunResult`
- `BP_DeploymentGate`
- `BP_LootContainer`
- `BP_ExtractionTrigger_Stable`
- `BP_ExtractionTrigger_HiddenTicketBooth`
- `BP_PersonalStorage`
- `BP_FactionVaultPlaceholder`
- `BP_ProjectBoard`
- `BP_FlickerStalker`
- `BP_PlayerInventoryComponent`
- `BP_PlayerSanityComponent`
- `BP_PlayerRunStateComponent`

The first interaction pass should use `LDInteractable` implementations already present on loot containers, extraction triggers, storage actors, and the project board.

## Input And HUD Contract

The source scaffold includes classic UE input mappings in `Config/DefaultInput.ini`:

- `WASD`: move
- mouse: look
- `Space`: jump
- `E`: interact
- `Q`: consume Almond Water
- `K`: debug death

`ALDPlayerCharacter` exposes Blueprint delegates for:

- interaction prompt changes
- HUD snapshot changes
- player messages

The first HUD widget should bind to the player character and display sanity, carried inventory stacks, interaction prompt text, player messages, and run result state.

## Data Import

Before importing data:

```bash
python3 scripts/validate_seed_data.py
python3 scripts/export_unreal_datatables.py
```

Import CSV files from:

```text
generated/unreal_datatables/
```

Import `DT_Items.csv` as a DataTable using `FLDItemRow`, then set:

```ini
[/Script/LiminalDominion.LDGameDataSubsystem]
ItemDataTablePath=/Game/Data/DT_Items.DT_Items
```

`ULDGameDataSubsystem` uses that table to resolve stackability and max stack size for starter loadouts, loot pickup, and storage deposits. Additional row structs should be added as each gameplay system moves from Python prototype to Unreal.

## First Playable Milestone

The first editor milestone is not visual polish. It is this loop:

1. Start in `LD_Hub_Greybox`.
2. Enter personal room.
3. Interact with `BP_DeploymentGate` to start `run_level1_service_halls_v0` and open `LD_Level1_ServiceHalls_Greybox`.
4. Pick up loot from a container.
5. Watch sanity drain.
6. Consume Almond Water.
7. Trigger a Flicker Stalker patrol/chase/attack.
8. Extract through the stable exit and return to `LD_PersonalRoom_Greybox`.
9. Return to personal room.
10. Deposit loot into personal storage.
11. Contribute Movie Tickets and scrap to the Signal Lamp Project.
12. Trigger death in a test run and confirm carried inventory clears while personal storage remains.

## Local SaveGame Persistence

V0.1 uses `ULDSaveGameSubsystem` as a local-only persistence bridge. This is not the final server persistence model.

The default slot is configured in `Config/DefaultGame.ini`:

```ini
[/Script/LiminalDominion.LDSaveGameSubsystem]
SaveSlotName=LiminalDominionV0
UserIndex=0
```

Persisted V0.1 state:

- selected faction ID
- personal storage stacks
- completed hub upgrade IDs
- simple run history entries

In the editor, set personal-room storage Blueprints to persist as personal storage, call `LoadFromSave` on BeginPlay, and call `SaveToSaveGame` after manual storage operations that do not go through `DepositFrom`.

## Entity Setup

For `BP_FlickerStalker`:

- Assign one or more patrol point actors in the Flicker Corridor.
- Tune `DetectionRadius`, `AttackRange`, `PatrolSpeed`, and `ChaseSpeed`.
- Confirm attack calls the player death path and clears carried inventory during an active run.

## Windows Build Gate

Before any playtest release:

- Package for Windows.
- Run the full smoke test on Windows.
- Confirm input, UI scaling, save paths, data import, extraction, death wipe, and sanity behavior.
- Commit any project-setting changes after verifying they do not break macOS development.
