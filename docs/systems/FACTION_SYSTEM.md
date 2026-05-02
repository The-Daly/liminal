# Faction System

## V0.1 Purpose

Factions provide starter identity and loadout flavor. They do not yet implement full Realm resets, raids, faction servers, or deep progression.

## V0.1 Factions

- M.E.G.: safer/research identity, entity scanner.
- B.N.T.G.: trade/salvage identity, crowbar.
- Clippers: route-running identity, camcorder and chalk.

## Data Source

- `data/seed/factions.seed.json`
- `data/seed/items.seed.json`
- `data/seed/hub_upgrades.seed.json`

## Runtime Contract

- A faction has a unique `faction_id`.
- A faction has `starting_items`.
- Every starting item must exist in the item registry.
- V0.1 faction selection grants a loadout only.
- Future faction switching must call a Realm reset flow, not a simple team swap.

## Prototype

Use `scripts/faction_model.py` to resolve starting loadouts and validate item references.
