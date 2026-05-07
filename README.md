# Liminal Dominion — Codex Starter Repo

This package is structured for **Codex**, not Claude.

Codex should use `AGENTS.md` as the persistent project instruction file, then work from `tasks/codex/000_START_HERE.md`.

## What This Is

A repo scaffold for starting development of Liminal Dominion Version 0.1.

## What This Is Not

This is not the full game. This is not a finished Unreal build. This repo is the planning, data, prototype, and content scaffold the team is using to build Version 0.1.

## Recommended First Codex Prompt

```text
Read AGENTS.md, then read tasks/codex/000_START_HERE.md. Start with Task 001 only: verify and improve the data validation pipeline. Do not build gameplay yet.
```

## Current Prototype Target

- Unreal Engine 5
- Primary playable target: Windows 10/11 PC
- Secondary development target: macOS
- Graybox-only
- Data-driven items/factions
- One faction hub shell
- One personal room shell
- One Level 1 Service Halls raid zone
- One entity
- One extraction loop

## Current Executable Foundation

- Expanded JSON schemas and seed data cover V0.1 items, factions, loot, entities, storage, sanity, extractions, hub upgrades, player state, and run state.
- `scripts/validate_seed_data.py` validates schemas, duplicate IDs, and cross-data references.
- Prototype Python modules model registries, loot rolls, inventory/storage, capped personal-storage overflow, sanity, extraction requirements, project-board contributions, end-to-end run outcomes, and local profile persistence before Unreal integration.
- A content-first UE5 project now exists in `LiminalDominion.uproject`, `Config/`, and `Content/`.
- The earlier C++ gameplay scaffold is preserved in `Source_Legacy/` and can be re-enabled later when the Windows toolchain is ready.
- Non-Unreal framework docs and prototypes now cover faction loadouts, no-team-kill social rules, trader purchases, the 21-NPC master roster, NPC/quest contracts, weapons/ammo, Trail String navigation, gun-noise responses, loot density, project-board contribution rules, the playable loop contract, and a local save-profile contract.
- `docs/planning/MISSING_SYSTEMS_ROADMAP.md` tracks the gap between this scaffold, the V0.1 graybox, and the full game.

Start with `docs/SYSTEM_INDEX.md` when handing the project to another AI agent or developer.

## Local Verification

On macOS Terminal:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_seed_data.py
python3 -m unittest discover -s tests -v
python3 scripts/check_dev_environment.py
python3 scripts/playable_loop_model.py
python3 scripts/persistence_model.py
```

On Windows PowerShell:

```powershell
py -3 -m pip install -r requirements.txt
py -3 scripts/validate_seed_data.py
py -3 -m unittest discover -s tests -v
py -3 scripts/check_dev_environment.py
py -3 scripts/playable_loop_model.py
py -3 scripts/persistence_model.py
```

To run the Windows Unreal startup sequence from the repo:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_windows_unreal.ps1
```

The current visualization-first startup opens the UE5 Open World template by default. If code modules are re-enabled later, the same script will require Visual Studio 2022 build tools and a Windows 10/11 SDK.

See `docs/technical/CROSS_PLATFORM_COMPATIBILITY.md` for macOS Terminal basics, Windows PowerShell equivalents, and the Windows-first build policy.
See `docs/technical/UNREAL_PROJECT_SETUP.md` for the first UE5 editor open, map creation, Blueprint pass, and Windows build gate.
See `docs/technical/INSTALL_UNREAL_MAC.md` for installing Unreal Engine through Epic Games Launcher on this Mac.
See `docs/technical/WINDOWS_UNREAL_HANDOFF.md` for moving setup to a Windows PC with enough storage for Unreal.

## GitHub Sync

This repo is configured for the GitHub remote `https://github.com/The-Daly/liminal.git`.

Use GitHub Desktop for browser/app-based sign-in and pushing without Terminal credential prompts. See `docs/technical/GITHUB_DESKTOP_SETUP.md`.
