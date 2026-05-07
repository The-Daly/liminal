# Storage Architecture

## Storage Tiers

| Tier | Description |
|---|---|
| Carried | Player run inventory; lost on death |
| Personal | Safe storage in personal room; capped |
| Shared | Faction storage; larger but raid-risk |

## Starting Personal Caps

| Item Class | Cap |
|---|---:|
| Movie Tickets | 5,000 |
| Almond Water | 50 |
| Bulk Salvage | 200 |
| Weapons | 18 total |
| Armor Plates | 20 |
| Ammunition | 1,500 |
| Relic-Class | Unlimited |

## Version 0.1 Implementation

Caps are implemented as data in `data/seed/storage.seed.json` and enforced by the Python prototype layer in `scripts/inventory_model.py`.

Current overflow stub behavior:

- Personal storage accepts items until the relevant class cap is reached.
- Any excess is returned as an overflow result instead of being silently discarded.
- When transferring from carried inventory to personal storage, only the stored quantity is removed from carried inventory.
- Overflow remains in the source container for manual player handling until the final Unreal UI/flow exists.
