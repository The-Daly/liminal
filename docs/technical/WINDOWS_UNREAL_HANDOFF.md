# Windows Unreal Handoff

Use this when moving Liminal Dominion from this Mac setup machine to a Windows PC with enough storage for Unreal Engine.

## Windows Machine Requirements

- Windows 10/11.
- Epic Games Launcher.
- Unreal Engine 5.x.
- Visual Studio 2022 with:
  - Game development with C++
  - Windows 10/11 SDK
  - MSVC v143 toolset
- GitHub Desktop or Git.
- Python 3.9+.
- At least 150 GB free disk space recommended for Unreal, generated files, builds, and Derived Data Cache.

## Clone

With GitHub Desktop:

1. Sign in.
2. `File > Clone Repository`.
3. Select `The-Daly/liminal`.
4. Clone somewhere like:

```text
C:\Projects\LiminalDominion
```

With PowerShell:

```powershell
cd C:\Projects
git clone https://github.com/The-Daly/liminal.git LiminalDominion
cd C:\Projects\LiminalDominion
```

## Preflight

```powershell
py -m pip install -r requirements.txt
py scripts/check_dev_environment.py
py scripts/check_unreal_scaffold.py
py scripts/find_unreal_editor.py
py scripts/export_unreal_datatables.py
```

## First Unreal Open

1. Double-click `LiminalDominion.uproject`.
2. If prompted, rebuild modules.
3. If prompted, generate project files.
4. If compile fails, copy the first compiler error into Codex.
5. If compile succeeds, create the first maps:
   - `Content/Maps/LD_Hub_Greybox`
   - `Content/Maps/LD_PersonalRoom_Greybox`
   - `Content/Maps/LD_Level1_ServiceHalls_Greybox`

## Data Import

1. Run:

```powershell
py scripts/export_unreal_datatables.py
```

2. In Unreal, create `Content/Data`.
3. Import `generated/unreal_datatables/DT_Items.csv` as a DataTable using `FLDItemRow`.
4. Set this config value after import:

```ini
[/Script/LiminalDominion.LDGameDataSubsystem]
ItemDataTablePath=/Game/Data/DT_Items.DT_Items
```

## First Blueprint Assets

Create Blueprint children:

- `BP_LDGameModeBase`
- `BP_LDPlayerCharacter`
- `BP_DeploymentGate`
- `BP_LootContainer`
- `BP_ExtractionTrigger_Stable`
- `BP_ExtractionTrigger_HiddenTicketBooth`
- `BP_PersonalStorage`
- `BP_FactionVaultPlaceholder`
- `BP_ProjectBoard`
- `BP_FlickerStalker`
- `WBP_PlayerHUD`
- `WBP_RunResult`

## First Playtest Loop

1. Start in hub.
2. Interact with deployment gate.
3. Load Level 1 Service Halls.
4. Loot a container.
5. Watch sanity drain.
6. Press `Q` to consume Almond Water.
7. Let Flicker Stalker detect/chase/attack.
8. Extract through stable exit.
9. Return to personal room.
10. Deposit loot into personal storage.
11. Restart editor and confirm personal storage can reload from SaveGame.

## Do Not Commit

Do not commit generated Unreal folders:

- `Binaries/`
- `Build/`
- `DerivedDataCache/`
- `Intermediate/`
- `Saved/`
- `.vs/`

These are ignored by `.gitignore`.
