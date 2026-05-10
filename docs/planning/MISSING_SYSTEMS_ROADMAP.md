# Missing Systems Roadmap

This roadmap tracks what is missing from the starter package before Liminal Dominion can become a playable game. Locked rules still live in `AGENTS.md` and `docs/design/LOCKED_SYSTEMS.md`; changes to those rules belong in `docs/design/PROPOSALS.md`.

## Current Package State

- The repo is a Codex-oriented data, planning, tooling, and visualization scaffold.
- `LiminalDominion.uproject` now exists and launches as a content-first Unreal Engine 5 project.
- `Config/`, `Content/`, generated DataTable CSV exports, and Windows startup tooling are now in the repo.
- The previous C++ gameplay scaffold is preserved in `Source_Legacy/` but is not active in the current visualization-first project path.
- Saved repo-owned maps, Blueprint/UI placeholders, and automated graybox shell passes now exist in the UE5 project.
- A packaged playable build still does not exist yet.
- Python validation exists and requires `jsonschema` from `requirements.txt`.
- Version 0.1 remains a graybox, single-player/local prototype target.
- The repo-side Python layer can now simulate successful and failed runs, including loot, sanity drain, extraction, personal storage deposit, death wipe, project-board contribution, and local profile persistence.

## V0.1 Foundation

- Data schemas and seeds for items, factions, loot tables, entities, inventory, storage, sanity, extractions, hub upgrades, player state, and run state.
- Importable Python prototypes for registry loading, loot rolls, inventory, storage, sanity, extraction, project-board contribution, local save payloads, and basic run-state outcomes.
- Validation for duplicate IDs and cross-data references.
- Negative validation tests for enum errors, duplicate IDs, missing item references, and invalid runtime data.

## V0.1 Playable Loop

- Unreal Engine 5 project.
- Graybox hub shell, personal room, faction vault placeholder, deployment corridor, and Level 1 Service Halls.
- Stable extraction and one hidden/conditional extraction.
- Loot containers using the validated loot table.
- Carried inventory, personal storage, shared vault placeholder, death wipe, capped personal-storage overflow handling, and extraction result handling.
- Sanity meter, sanity drain, Almond Water effect, and low-sanity event hook.
- Flicker Stalker prototype with patrol, perception, chase, attack, and return-to-patrol.
- Minimal HUD for sanity, inventory, prompts, pickup feedback, extraction, and death.
- Repo-side simulation coverage for successful extraction and failed-run inventory loss before Unreal implementation.

## Full Game Gaps

- Server-authoritative multiplayer architecture, session flow, matchmaking, party flow, and online-presence rules.
- Persistent player account, realm state, faction storage, personal room state, hub progression, run history, and migrations.
- Faction raid lifecycle, eligibility, warnings, breach rules, reward rules, and anti-grief limits.
- Level 0, Level 2, expansion bases, streaming transitions, and routing rules.
- NPC spawning, quest-giver/recruitable archetypes, recruitment quests, quarters, and continuous quest pipelines.
- Economy depth: trader inventories, price curves, sinks, faction market differences, and balance telemetry.
- Combat/tools: weapons, armor, batteries, scanner, camcorder, crowbar, chalk, noise, and counterplay hooks.
- Content production: modular kits, art direction, audio direction, animation, entity VFX, UI style, and asset budgets.
- QA/live ops: playtest checklists, crash reporting, telemetry, balance dashboards, and release gates.
- Legal/content review for Backrooms inspiration boundaries, citations, original names, and entities.

## Build Order

1. Finish data validation and Python prototypes.
2. Save repo-owned maps and first Blueprint/UI assets into the existing UE5 project.
3. Build the complete graybox extraction loop.
4. Playtest V0.1 until the 10-minute loop is readable.
5. Add persistence/session architecture only after the loop works.
6. Expand factions, raids, NPCs, economy, and levels through approved proposals.
