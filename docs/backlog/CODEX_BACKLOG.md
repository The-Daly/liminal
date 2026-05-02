# Codex Backlog — Version 0.1

## Phase 1 — Data Foundation

- [x] Validate current schemas.
- [x] Validate current seed data.
- [x] Add schemas for loot tables, entities, sanity, storage, extraction, hub upgrades.
- [x] Add seed data for each schema.
- [x] Add duplicate-ID detection.
- [x] Add reference validation: faction starting items must exist in item registry.
- [x] Add reference validation for loot tables, extractions, hub upgrades, player state, and run state.

## Phase 2 — Item / Inventory Prototype

- [x] Item registry loader.
- [x] Inventory slot model.
- [x] Stackable item support.
- [ ] Weight placeholder.
- [x] Add/remove item operations.
- [x] Death inventory wipe operation.

## Phase 3 — Survival Prototype

- [x] Sanity component model.
- [x] Almond Water consumable effect.
- [x] Sanity drain by level.
- [x] Low sanity threshold events.

## Phase 4 — Faction Prototype

- [x] Faction registry.
- [x] Starting loadout resolver.
- [ ] Full Realm reset stub.
- [x] Faction hub upgrade project data.

## Phase 4.5 — Quest / Trader / NPC Framework

- [x] Trader schema and seed data.
- [x] NPC schema and seed data.
- [x] Quest schema and seed data.
- [x] Trader purchase prototype.
- [x] Quest completion prototype.
- [x] AI-readable system docs.

## Phase 5 — Storage Prototype

- [x] Personal storage container model.
- [x] Shared faction vault data placeholder.
- [x] Storage caps.
- [ ] Overflow stub.

## Phase 6 — Unreal Graybox

- [x] Add source-level Unreal project scaffold.
- [x] Add first C++ gameplay skeletons for inventory, sanity, loot, extraction, and Flicker Stalker.
- [x] Add player, interaction, run-state, storage, and project-board skeletons.
- [x] Add input mappings and HUD-facing player delegates.
- [x] Add item DataTable lookup subsystem for stack metadata.
- [x] Add local SaveGame bridge for personal storage, hub upgrades, and run history.
- [x] Add deployment gate and extraction map transition hooks.
- [x] Add simple Flicker Stalker patrol/chase/attack runtime behavior.
- [ ] Create hub shell.
- [ ] Create personal room shell.
- [ ] Create Level 1 Service Halls shell.
- [ ] Add loot containers.
- [ ] Add extraction trigger.
- [ ] Add Flicker Stalker placeholder.
- [ ] Add player HUD widget.

## Phase 7 — Playtest Loop

- [ ] Deploy.
- [ ] Loot.
- [ ] Sanity drain.
- [ ] Entity encounter.
- [ ] Extract.
- [ ] Store loot.
- [ ] Contribute to project board.
