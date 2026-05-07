# Package Manifest

Created: 2026-05-07

## Codex-Oriented Files

- `AGENTS.md` - persistent Codex repo instructions
- `CODEX_QUICKSTART.md` - first-run Codex usage notes
- `tasks/codex/000_START_HERE.md` - ordered startup task flow
- `tasks/codex/001_VALIDATE_SEED_DATA.md` - validation task
- `tasks/codex/002_ITEM_REGISTRY.md` - registry task
- `tasks/codex/003_INVENTORY_MODEL.md` - inventory task
- `docs/source_truth/SOURCE_OF_TRUTH_SUMMARY.md` - condensed source rules
- `docs/planning/MISSING_SYSTEMS_ROADMAP.md` - current package gaps and build order
- `docs/planning/UE_WINDOWS_TASKS.md` - Windows Unreal buildout checklist
- `docs/technical/UNREAL_GRAYBOX_IMPLEMENTATION.md` - first Unreal graybox target
- `docs/technical/UNREAL_PROJECT_SETUP.md` - content-first Unreal setup path
- `docs/technical/CROSS_PLATFORM_COMPATIBILITY.md` - Windows/macOS command policy
- `docs/systems/` - AI-readable system contracts
- `data/schemas/` - runtime schema definitions
- `data/seed/` - seed data for the V0.1 prototype

## Runtime And Prototype Scripts

- `scripts/validate_seed_data.py` - schema, duplicate-id, and reference validation
- `scripts/item_registry.py` - importable seed-data registry
- `scripts/inventory_model.py` - inventory and personal-storage overflow prototype
- `scripts/survival_model.py` - sanity prototype
- `scripts/extraction_model.py` - extraction requirement helper
- `scripts/faction_model.py` - faction loadout and reset helper
- `scripts/economy_model.py` - trader purchase helper
- `scripts/quest_model.py` - quest objective and reward helper
- `scripts/npc_roster_model.py` - NPC role/service helper
- `scripts/weapon_model.py` - ammo, crafting, and gated-container helper
- `scripts/navigation_marker_model.py` - trail-string visibility and expiry helper
- `scripts/social_model.py` - same-faction squad/radio/no-team-kill helper
- `scripts/level_layout_model.py` - Level 1 route and foothold helper
- `scripts/loot_model.py` - loot preview and roll helper
- `scripts/export_unreal_datatables.py` - Unreal CSV export bridge
- `scripts/check_dev_environment.py` - local dev smoke check
- `scripts/check_unreal_scaffold.py` - content-first/legacy Unreal scaffold verification
- `scripts/preflight_release.py` - validation, export, scaffold, compile, and tracked-file preflight
- `scripts/start_windows_unreal.ps1` - Windows Unreal startup path

## Unreal Project State

- `LiminalDominion.uproject` - active content-first Unreal project
- `Config/` - project settings, input bindings, and reserved data/save config
- `Content/Maps/` - repo-owned target folder for saved graybox maps
- `Content/Blueprints/` - repo-owned target folder for Blueprint placeholders
- `Content/Data/` - repo-owned target folder for imported DataTables
- `Content/UI/` - repo-owned target folder for HUD and run-result widgets
- `generated/unreal_datatables/` - exported CSVs for Unreal imports
- `Source_Legacy/` - archived C++ gameplay scaffold preserved for later reactivation

## Verification

- `tests/test_data_tools.py` - Python test coverage for the prototype layer
- `requirements.txt` - Python dependency declaration

## Source PDFs Used

- Liminal Dominion Master Framework Mac Compatible
- Seamless World, Storage & Raids Addendum
- Level Atlas Research Pack
- NPC Population Recruitment System
