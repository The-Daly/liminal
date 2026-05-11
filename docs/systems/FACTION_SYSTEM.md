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
- V0.1 starter loadouts are intentionally minimal: faction identity tool plus flashlight, no weapons, armor, ammo, Almond Water, or Movie Tickets by default.
- Future faction switching must call a Realm reset flow, not a simple team swap.
- In the persistent-world menu direction, faction lock is character-bound per realm until the scheduled mass wipe for that realm.
- Same-faction players are allies. They cannot damage or kill one another.
- Squads are same-faction social groups, not separate combat teams.
- Radios connect squadmates so small groups feel coordinated inside the larger faction team.

## Prototype

Use `scripts/faction_model.py` to resolve starting loadouts and validate item references.
Use `scripts/social_model.py` to enforce no team killing, same-faction squads, and squad radio scope.
