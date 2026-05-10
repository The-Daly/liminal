# UE Windows Task Breakdown

This is the first task list for the Windows machine with Unreal Engine installed.

## Task 1: Launch The Content-First Project

- Clone `The-Daly/liminal`.
- Run `py -3 scripts/preflight_release.py`.
- Run `powershell -ExecutionPolicy Bypass -File scripts/start_windows_unreal.ps1`.
- Open `LiminalDominion.uproject`.
- Confirm the project reaches the editor and opens `LD_Hub_Greybox`.
- If the repo-owned maps do not exist yet, save them first.
- Close the editor and run `powershell -ExecutionPolicy Bypass -File scripts/run_unreal_first_pass.ps1` to create and place the first placeholder Blueprint/UI assets.
- Close the editor again and run `powershell -ExecutionPolicy Bypass -File scripts/run_unreal_graybox_layout.ps1` to stamp the hub, personal room, and Service Halls shell layouts into the maps.
- If Unreal asks to build missing modules, cancel unless you are intentionally re-enabling the legacy C++ path.
- Commit only source/config/content changes, not generated Unreal folders.

## Task 2: Save Core Maps

- Save the current world as `LD_Hub_Greybox`.
- Create `LD_PersonalRoom_Greybox`.
- Create `LD_Level1_ServiceHalls_Greybox`.
- Save all maps under `Content/Maps`.
- Confirm the project starts at `LD_Hub_Greybox`.

## Task 3: Import DataTables

- Run `py -3 scripts/export_unreal_datatables.py`.
- Import `DT_Items.csv`.
- Import `DT_LootTables.csv`.
- Import `DT_Extractions.csv`.
- Import `DT_Storage.csv`.
- Import `DT_Sanity.csv`.
- Save the imported assets under `Content/Data`.
- Current limitation: the automated Python import path crashes in UE 5.7 when using Python-generated row structs, so this CSV import step remains manual for now.

## Task 4: Blueprint Loop

- Create Blueprint-only placeholders for deployment gate, loot containers, extraction triggers, storage, project board, player, and Flicker Stalker.
- The repo automation script already creates the first pass of these placeholders if they are missing.
- The repo automation now creates and places the first pass of these placeholders and stamps them into the graybox shells.

## Task 5: HUD

- Create `WBP_PlayerHUD` under `Content/UI`.
- Create `WBP_RunResult` under `Content/UI`.
- Display sanity, prompt text, carried stacks, messages, and run result state.

## Task 6: First Smoke Test

- Deploy from hub.
- Loot one container.
- Consume Almond Water.
- Trigger a death path and verify carried inventory clears.
- Repeat, extract successfully, and verify return to the personal room.
- Deposit loot and verify local persistence.

## Task 7: Optional Legacy C++ Reactivation

- Install Visual Studio 2022 Build Tools with MSVC v143 and the Windows 10/11 SDK.
- Restore `Source_Legacy` back into an active `Source` module layout.
- Regenerate project files.
- Rebuild the editor target.
- Reparent Blueprint placeholders if the legacy gameplay classes are restored.

## Task 8: Windows Package

- Package a Windows Development build.
- Run the smoke test from the packaged executable.
- Commit build-setting changes only if they are source/config/content assets that belong in git.
