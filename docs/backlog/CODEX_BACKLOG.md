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
- [x] Weight placeholder.
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
- [x] Same-faction no-team-kill social rule data.
- [x] Same-faction squad and radio rule prototype.
- [x] Full Realm reset stub.
- [x] Faction hub upgrade project data.

## Phase 4.5 — Quest / Trader / NPC Framework

- [x] Trader schema and seed data.
- [x] NPC schema and seed data.
- [x] Quest schema and seed data.
- [x] Trader purchase prototype.
- [x] Quest completion prototype.
- [x] AI-readable system docs.
- [x] Master 21-NPC roster for traders, quest givers, security, and security brokers.

## Phase 4.6 — Weapons / Ammo / Containers Framework

- [x] Weapon schema and seed data.
- [x] Ammo schema and seed data.
- [x] Ammo crafting recipe schema and seed data.
- [x] Container schema and seed data.
- [x] Crowbar-gated supply crate data.
- [x] Weapon ammo consumption prototype.
- [x] Ammo crafting prototype.
- [x] Gated container prototype.
- [x] Gun-noise entity response table.
- [x] Level 1 slim loot density profile.
- [x] Trail String marker data and prototype.
- [x] Extraction-style trader/storage UI contract.
- [x] Clippers retro-scrap base style guide.
- [x] Faction base visual identity guide.

## Phase 5 — Storage Prototype

- [x] Personal storage container model.
- [x] Shared faction vault data placeholder.
- [x] Storage caps.
- [ ] Overflow stub.

## Phase 6 — Unreal Graybox

- [x] Add source-level Unreal project scaffold.
- [x] Add Level 1 scale, route, and faction foothold layout data.
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
