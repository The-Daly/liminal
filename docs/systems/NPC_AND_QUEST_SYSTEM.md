# NPC And Quest System

## V0.1 Purpose

NPC and quest systems are placeholders that give the first player journey structure. They do not implement recruitment depth, compatibility matrices, NPC capture, or continuous quest pipelines yet.

## Data Source

- `data/seed/npcs.seed.json`
- `data/seed/npc_roster.seed.json`
- `data/seed/quests.seed.json`

The master roster lives in `docs/design/MASTER_NPC_ROSTER.md`. The small runtime NPC seed remains V0.1-focused; the roster seed tracks the wider cast that future quest, trader, and security systems can promote into runtime NPCs.
- `data/seed/items.seed.json`

## V0.1 NPCs

- Marrow Vell / Quartermaster: static hub NPC.
- Gives or frames the first recovery objective.
- Points the player toward deployment and storage.

## V0.1 Quests

First five quests:

- Still Water: extract with Almond Water.
- The Floor Gives Way: fall through a weak floor hole to a deeper pocket.
- Back to One: return from another level/pocket back to Level 1.
- Pry Rights: find a crowbar and open a supply crate.
- Ticket Hunger: find Movie Tickets to buy survival gear from The Turnstile.

## Runtime Contract

- Quests have objectives and rewards.
- Required objective item IDs must exist.
- Reward item IDs must exist.
- NPC quest references must exist.
- Recruitment is not purchasable.

## Prototype

Use `scripts/quest_model.py` for item-objective completion checks and reward preview.
