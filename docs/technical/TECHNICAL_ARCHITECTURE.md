# Technical Architecture

## Engine Target

Unreal Engine 5.

## Development Order

1. Data schemas.
2. Seed data.
3. Validation scripts.
4. Item registry.
5. Inventory model.
6. Storage model.
7. Sanity model.
8. Faction loadout model.
9. Extraction trigger.
10. Entity AI prototype.
11. Unreal integration.

## MVP Data-Driven Systems

| System | Data Source |
|---|---|
| Items | `data/seed/items.seed.json` |
| Factions | `data/seed/factions.seed.json` |
| Loot Tables | `data/seed/loot_tables.seed.json` |
| Entities | `data/seed/entities.seed.json` |
| Storage | `data/seed/storage.seed.json` |
| Sanity | `data/seed/sanity.seed.json` |
| Extractions | `data/seed/extractions.seed.json` |

## Multiplayer

Do not implement full networking in Version 0.1. Keep architecture compatible with later server authority.
