# Liminal Dominion — Codex Starter Repo

This package is structured for **Codex**, not Claude.

Codex should use `AGENTS.md` as the persistent project instruction file, then work from `tasks/codex/000_START_HERE.md`.

## What This Is

A repo scaffold for starting development of Liminal Dominion Version 0.1.

## What This Is Not

This is not the full game. This is not a final Unreal project. This is the planning/data/tooling skeleton Codex should use before building gameplay systems.

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
- Prototype Python modules model registries, loot rolls, inventory/storage, sanity, and extraction requirements before Unreal integration.
- A source-level UE5 scaffold now exists in `LiminalDominion.uproject`, `Config/`, `Content/`, and `Source/`.
- Non-Unreal framework docs and prototypes now cover faction loadouts, no-team-kill social rules, trader purchases, NPC/quest contracts, weapons/ammo, Trail String navigation, gun-noise responses, loot density, and the playable loop contract.
- `docs/planning/MISSING_SYSTEMS_ROADMAP.md` tracks the gap between this scaffold, the V0.1 graybox, and the full game.

Start with `docs/SYSTEM_INDEX.md` when handing the project to another AI agent or developer.

## Local Verification

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_seed_data.py
python3 -m unittest discover -s tests -v
python3 scripts/check_dev_environment.py
```

See `docs/technical/CROSS_PLATFORM_COMPATIBILITY.md` for macOS Terminal basics, Windows PowerShell equivalents, and the Windows-first build policy.
See `docs/technical/UNREAL_PROJECT_SETUP.md` for the first UE5 editor open, map creation, Blueprint pass, and Windows build gate.
See `docs/technical/INSTALL_UNREAL_MAC.md` for installing Unreal Engine through Epic Games Launcher on this Mac.
See `docs/technical/WINDOWS_UNREAL_HANDOFF.md` for moving setup to a Windows PC with enough storage for Unreal.

## GitHub Sync

This repo is configured for the GitHub remote `https://github.com/The-Daly/liminal.git`.

Use GitHub Desktop for browser/app-based sign-in and pushing without Terminal credential prompts. See `docs/technical/GITHUB_DESKTOP_SETUP.md`.
