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

The C++ row structs currently define the first item and extraction row shapes. Additional row structs should be added as each gameplay system moves from Python prototype to Unreal.

## First Playable Milestone

The first editor milestone is not visual polish. It is this loop:

1. Start in `LD_Hub_Greybox`.
2. Enter personal room.
3. Deploy into `LD_Level1_ServiceHalls_Greybox`.
4. Pick up loot from a container.
5. Watch sanity drain.
6. Consume Almond Water.
7. Trigger a Flicker Stalker chase/attack.
8. Extract through the stable exit.
9. Return to personal room.
10. Deposit loot into personal storage.
11. Contribute Movie Tickets and scrap to the Signal Lamp Project.
12. Trigger death in a test run and confirm carried inventory clears while personal storage remains.

## Windows Build Gate

Before any playtest release:

- Package for Windows.
- Run the full smoke test on Windows.
- Confirm input, UI scaling, save paths, data import, extraction, death wipe, and sanity behavior.
- Commit any project-setting changes after verifying they do not break macOS development.
