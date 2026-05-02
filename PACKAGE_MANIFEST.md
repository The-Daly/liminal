# Package Manifest

Created: 2026-05-01

## Codex-Oriented Files

- `AGENTS.md` — persistent Codex repo instructions.
- `CODEX_QUICKSTART.md` — how to start using Codex with this folder.
- `tasks/codex/000_START_HERE.md` — first Codex task flow.
- `tasks/codex/001_VALIDATE_SEED_DATA.md` — first implementation task.
- `docs/source_truth/SOURCE_OF_TRUTH_SUMMARY.md` — condensed source rules.
- `scripts/validate_seed_data.py` — first runnable validation tool.
- `scripts/item_registry.py` — importable data registry loader.
- `scripts/inventory_model.py` — standalone inventory/storage prototype.
- `scripts/survival_model.py` — standalone sanity prototype.
- `scripts/extraction_model.py` — extraction requirement helper.
- `scripts/faction_model.py` — faction starter loadout resolver.
- `scripts/economy_model.py` — V0.1 trader purchase prototype.
- `scripts/quest_model.py` — V0.1 quest objective/reward prototype.
- `scripts/weapon_model.py` — weapon ammo consumption, ammo crafting, and gated container prototype.
- `scripts/navigation_marker_model.py` — Trail String visibility and one-hour expiry prototype.
- `scripts/level_layout_model.py` — route/foothold helpers for Level 1 spatial layout data.
- `scripts/loot_model.py` — loot table preview and roll helper.
- `scripts/export_unreal_datatables.py` — CSV export bridge for Unreal DataTables.
- `scripts/check_dev_environment.py` — macOS/Windows development environment smoke check.
- `scripts/check_unreal_scaffold.py` — validates required source-level Unreal scaffold files.
- `scripts/find_unreal_editor.py` — detects Unreal Editor installations and can open `LiminalDominion.uproject`.
- `scripts/preflight_release.py` — runs local validation, export, scaffold, compile, and tracked-file checks before handoff.
- `tests/test_data_tools.py` — Python validation/model test coverage.
- `requirements.txt` — Python dependency for validation.
- `data/schemas/` — starter schemas.
- `data/seed/` — starter data.
- `docs/planning/MISSING_SYSTEMS_ROADMAP.md` — full gap roadmap.
- `docs/SYSTEM_INDEX.md` — AI/developer navigation index for systems, data, prototypes, and verification.
- `docs/systems/` — AI-readable system contracts for faction, economy/trader, NPC/quest, and playable loop behavior.
- `docs/systems/TRADER_STORAGE_UI_CONTRACT.md` — extraction-style trader/storage UI contract.
- `docs/design/CLIPPERS_BASE_STYLE.md` — original retro-scrap Clippers base style guide.
- `docs/design/LEVEL1_SCALE_AND_FACTION_LAYOUT.md` — Level 1 footprint, travel time, faction foothold spacing, and route topology.
- `docs/technical/UNREAL_GRAYBOX_IMPLEMENTATION.md` — first Unreal graybox implementation target.
- `docs/technical/CROSS_PLATFORM_COMPATIBILITY.md` — Windows-first, macOS-supported development policy and command equivalents.
- `docs/technical/GITHUB_DESKTOP_SETUP.md` — internet/GUI-based GitHub push workflow.
- `docs/technical/UNREAL_PROJECT_SETUP.md` — first Unreal open, map creation, Blueprint pass, and Windows build gate.
- `docs/technical/INSTALL_UNREAL_MAC.md` — GUI install steps for Epic Games Launcher and Unreal Engine on macOS.
- `docs/technical/WINDOWS_UNREAL_HANDOFF.md` — Windows Unreal workstation setup and first smoke test.
- `docs/planning/UE_WINDOWS_TASKS.md` — task breakdown for first compile, maps, Blueprints, HUD, smoke test, and package.
- `Source/` — source-level Unreal Engine module scaffold and first V0.1 gameplay skeletons.
- `Source/LiminalDominion/Public/LDDeploymentGate.h` — interactable run-start gate for the first hub-to-Level-1 transition.
- `Config/DefaultInput.ini` — first playable input mappings for movement, interact, Almond Water, and debug death.
- `Config/DefaultGame.ini` — project metadata, DataTable path hook, and local SaveGame slot config.
- `docs/design/V0_1_PLAYER_JOURNEY.md` — first-session journey, starter loadout use, trader, project board, and relic display behavior.

## Source PDFs Used

- Liminal Dominion Master Framework Mac Compatible.
- Seamless World, Storage & Raids Addendum.
- Level Atlas Research Pack.
- NPC Population Recruitment System.
