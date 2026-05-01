# AGENTS.md — Codex Operating Instructions for Liminal Dominion

Codex must read this file before doing any work in this repository.

## Project

**Liminal Dominion** is a Backrooms-inspired hard-loss extraction survival PvPvE game.

## Source-of-Truth Rule

Do not invent or silently replace locked design rules. If a change is needed, add a proposal to:

`docs/design/PROPOSALS.md`

Then ask the user before implementing the change.

## Locked Core Decisions

- Engine target: Unreal Engine 5.
- Genre: hard-loss extraction survival PvPvE.
- Player death: carried inventory is lost.
- Currency: Movie Tickets.
- Survival systems: Almond Water and sanity.
- Main factions: M.E.G., B.N.T.G., Clippers.
- Faction switching: full Realm reset.
- Personal rooms: safe, non-raidable, capped storage.
- Shared faction storage: larger than personal storage and raidable when the owning faction has online presence.
- Transitions: no conventional loading screens; all transitions must be diegetic.
- NPC recruitment: earned through quests, not purchased.
- Prototype scope: Version 0.1 only.

## Version 0.1 Goal

Build a graybox prototype proving this loop:

1. Start in faction hub / personal room.
2. Deploy into Level 1 — Service Halls sub-section.
3. Loot Movie Tickets, Almond Water, batteries, scrap, and basic items.
4. Manage sanity.
5. Encounter one entity, the Flicker Stalker.
6. Extract through a diegetic transition.
7. Return to personal safe room.
8. Store loot or contribute to shared faction progression.

## Codex Work Rules

1. Start with data and tooling before gameplay logic.
2. Keep constants data-driven.
3. Prefer JSON/DataTable-ready structures.
4. Write small, testable modules.
5. Add validation scripts before expanding seed data.
6. Do not build full multiplayer yet.
7. Do not build all 160 relic models yet.
8. Do not build full faction raids yet.
9. Do not build full NPC compatibility matrices yet.
10. Keep prototype implementation ugly but playable.

## First Tasks

Use `tasks/codex/000_START_HERE.md`.

## Verification

For non-Unreal data/tooling tasks, run:

```bash
python3 scripts/validate_seed_data.py
```

If Unreal project files exist later, add Unreal-specific build/test instructions here.
