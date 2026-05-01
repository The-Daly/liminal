# UE Windows Task Breakdown

This is the first task list for the Windows machine with Unreal Engine installed.

## Task 1: Compile Project

- Clone `The-Daly/liminal`.
- Run `py scripts/preflight_release.py`.
- Open `LiminalDominion.uproject`.
- Rebuild modules.
- Record the first compile error if build fails.
- Commit only source/config fixes, not generated Unreal folders.

## Task 2: Create Core Maps

- Create `LD_Hub_Greybox`.
- Create `LD_PersonalRoom_Greybox`.
- Create `LD_Level1_ServiceHalls_Greybox`.
- Save maps under `Content/Maps`.
- Confirm project starts at `LD_Hub_Greybox`.

## Task 3: Import DataTables

- Run `py scripts/export_unreal_datatables.py`.
- Import `DT_Items.csv` as `FLDItemRow`.
- Set `ItemDataTablePath=/Game/Data/DT_Items.DT_Items`.
- Confirm starter loadouts and loot pickup use real stack limits.

## Task 4: Blueprint Loop

- Create Blueprint children for deployment gate, loot containers, extraction triggers, storage, project board, player, and Flicker Stalker.
- Place deployment gate in hub.
- Place loot containers and Flicker Stalker in Service Halls.
- Place extraction trigger in Service Halls.
- Place storage and project board in personal room/hub.

## Task 5: HUD

- Create `WBP_PlayerHUD`.
- Bind to `ALDPlayerCharacter` HUD snapshot events.
- Display sanity, prompt, carried stacks, messages, and run result state.

## Task 6: First Smoke Test

- Deploy from hub.
- Loot one container.
- Consume Almond Water.
- Get killed by Flicker Stalker and verify carried inventory clears.
- Repeat, extract successfully, and verify return to personal room.
- Deposit loot and verify local SaveGame reload.

## Task 7: Windows Package

- Package a Windows Development build.
- Run the smoke test from the packaged executable.
- Commit build-setting changes only if they are source/config assets that belong in Git.
