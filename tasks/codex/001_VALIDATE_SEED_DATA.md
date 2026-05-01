# Task 001 — Validate Seed Data

## Goal

Make the seed data validation script reliable.

## Files

- `scripts/validate_seed_data.py`
- `data/schemas/*.schema.json`
- `data/seed/*.seed.json`

## Acceptance Criteria

- `python3 scripts/validate_seed_data.py` runs successfully.
- Duplicate IDs fail.
- Missing faction starting item references fail.
- Missing loot table item references fail.
- Bad rarity enum values fail.
- Output is readable.

## Do Not

- Build gameplay systems yet.
