# Codex Start Here

## Do This First

Read these files in order:

1. `AGENTS.md`
2. `docs/source_truth/SOURCE_OF_TRUTH_SUMMARY.md`
3. `docs/design/MVP_SCOPE_LOCK.md`
4. `docs/technical/TECHNICAL_ARCHITECTURE.md`
5. `docs/backlog/CODEX_BACKLOG.md`

## First Development Sequence

### Task 001 — Validate Seed Data

Goal:
- Make sure the repo has working JSON schemas and seed data validation.

Acceptance:
- `python3 scripts/validate_seed_data.py` runs without errors.
- Missing required fields are caught.
- Bad enum values are caught.
- Output is readable.

### Task 002 — Create Item Registry Prototype

Goal:
- Create a simple item registry loader that loads all item seed data and exposes lookup by `item_id`.

Acceptance:
- Duplicate IDs fail validation.
- Missing referenced item IDs in faction loadouts fail validation.
- CLI prints loaded item and faction counts.

### Task 003 — Create Inventory Model Prototype

Goal:
- Create a standalone inventory/storage prototype before Unreal implementation.

Acceptance:
- Add/remove item operations work.
- Stackable item support works.
- Death inventory wipe clears carried inventory and preserves personal storage.

## Do Not Start With

- Full Unreal gameplay.
- Multiplayer.
- Procedural generation.
- Weapon ballistics.
- Full raid system.
