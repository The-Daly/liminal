# Weapons, Ammo, Crafting, And Containers

This framework defines combat items and acquisition routes without implementing full gunplay yet.

## V0.1 Intent

Weapons are rare, noisy, and risky. Players do not start with reliable combat gear. The first playable build may use placeholders, but the data should already know:

- which item is a weapon
- what ammo it consumes
- how ammo is found or crafted
- which containers can contain weapons/ammo
- which containers require tools such as a crowbar
- which level zones can spawn those containers
- whether NPCs may carry or reward the item
- how gunshots can trigger level-specific entity/noise responses

## Locked Scope Boundary

V0.1 does not need:

- weapon attachments
- ballistics simulation
- full PvP balance
- deep armor penetration
- complete NPC loot tables

V0.1 can support:

- one crude firearm placeholder
- one melee/crowbar utility path
- two ammo types
- ammo crafting recipe
- supply crates, lockers, cabinets, and NPC/world acquisition tags

## Acquisition Routes

| Route | V0.1 Meaning |
|---|---|
| WorldContainer | Found in cabinets, lockers, crates, or supply caches |
| BreakOpenContainer | Requires a tool such as B.N.T.G. Crowbar |
| NPCDrop | NPC can carry/drop the item later |
| TraderStock | Trader can sell the item later |
| Crafting | Built from resource ingredients |
| QuestReward | Granted by quest completion |

## Container Types

| Container | Typical Contents | Gate |
|---|---|---|
| Cabinet | water, batteries, small ammo | none |
| Locker | tools, ammo, scrap, rare weapon | none or key later |
| SupplyCrate | scrap, ammo, weapon chance | crowbar |
| TheaterCache | Movie Tickets, relic chance, odd ammo | Movie Ticket or hidden route later |

## Ammo Crafting

Ammo crafting is intentionally simple in V0.1:

- consume resources
- produce ammo stacks
- no station tiers yet
- future work can require workbench/hub upgrades

## Data Files

- `data/seed/weapons.seed.json`
- `data/seed/ammo.seed.json`
- `data/seed/crafting_recipes.seed.json`
- `data/seed/containers.seed.json`
