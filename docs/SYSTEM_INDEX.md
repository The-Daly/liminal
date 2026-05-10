# Liminal Dominion System Index

This is the navigation page for AI agents and developers working without Unreal Editor access.

## Current Handoff Pack

- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_CODEX_TASKS.md`
- `docs/handoff/UNREAL_DATATABLE_IMPORT_PLAN.md`
- `docs/handoff/BLUEPRINT_WIRING_PLAN.md`
- `docs/handoff/VERSION_0_1_PLAYABLE_LOOP.md`
- `docs/status/Liminal_Project_Status_2026-05-10.xlsx`

## Locked Rules

- `AGENTS.md`
- `docs/source_truth/SOURCE_OF_TRUTH_SUMMARY.md`
- `docs/design/LOCKED_SYSTEMS.md`
- `docs/design/MVP_SCOPE_LOCK.md`

## V0.1 Runtime Data

- Items: `data/seed/items.seed.json`
- Factions: `data/seed/factions.seed.json`
- Loot: `data/seed/loot_tables.seed.json`
- Entities: `data/seed/entities.seed.json`
- Storage: `data/seed/storage.seed.json`
- Sanity: `data/seed/sanity.seed.json`
- Extractions: `data/seed/extractions.seed.json`
- Hub upgrades: `data/seed/hub_upgrades.seed.json`
- Player state: `data/seed/player_state.seed.json`
- Run state: `data/seed/run_state.seed.json`
- Traders: `data/seed/traders.seed.json`
- NPCs: `data/seed/npcs.seed.json`
- Master NPC roster: `data/seed/npc_roster.seed.json`
- Quests: `data/seed/quests.seed.json`
- Weapons: `data/seed/weapons.seed.json`
- Ammo: `data/seed/ammo.seed.json`
- Crafting: `data/seed/crafting_recipes.seed.json`
- Containers: `data/seed/containers.seed.json`
- Level layouts: `data/seed/level_layouts.seed.json`
- Navigation markers: `data/seed/navigation_markers.seed.json`
- Noise responses: `data/seed/noise_responses.seed.json`
- Loot density: `data/seed/loot_density.seed.json`
- Social rules: `data/seed/social_rules.seed.json`

## System Docs

- `docs/systems/AI_CONTEXT_BRIEF.md`
- `docs/systems/FACTION_SYSTEM.md`
- `docs/systems/ECONOMY_AND_TRADER_SYSTEM.md`
- `docs/systems/NPC_AND_QUEST_SYSTEM.md`
- `docs/design/MASTER_NPC_ROSTER.md`
- `docs/systems/PLAYABLE_LOOP_CONTRACT.md`
- `docs/systems/WEAPONS_AMMO_AND_CONTAINERS.md`
- `docs/systems/TRADER_STORAGE_UI_CONTRACT.md`
- `docs/systems/SOCIAL_AND_TEAM_SAFETY.md`
- `docs/design/FACTION_BASE_STYLE_GUIDE.md`
- `docs/design/CLIPPERS_BASE_STYLE.md`
- `docs/design/LEVEL1_SCALE_AND_FACTION_LAYOUT.md`

## Python Prototypes

- Registry: `scripts/item_registry.py`
- Inventory: `scripts/inventory_model.py`
- Loot: `scripts/loot_model.py`
- Survival: `scripts/survival_model.py`
- Extraction: `scripts/extraction_model.py`
- Factions: `scripts/faction_model.py`
- Economy/trader: `scripts/economy_model.py`
- Quests: `scripts/quest_model.py`
- Master NPC roster: `scripts/npc_roster_model.py`
- Weapons/ammo/crafting/containers: `scripts/weapon_model.py`
- Level layout: `scripts/level_layout_model.py`
- Navigation markers: `scripts/navigation_marker_model.py`
- Social/team safety: `scripts/social_model.py`

## Verification

Run:

```bash
python3 scripts/preflight_release.py
```
