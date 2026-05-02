# NPC And Quest System

## V0.1 Purpose

NPC and quest systems are placeholders that give the first player journey structure. They do not implement recruitment depth, compatibility matrices, NPC capture, or continuous quest pipelines yet.

## Data Source

- `data/seed/npcs.seed.json`
- `data/seed/quests.seed.json`
- `data/seed/items.seed.json`

## V0.1 NPCs

- Tom / Quartermaster: static hub NPC.
- Gives or frames the first recovery objective.
- Points the player toward deployment and storage.

## V0.1 Quest

First quest: recover basic supplies from Level 1 and return.

Completion should be possible when the player has the required items after extraction.

## Runtime Contract

- Quests have objectives and rewards.
- Required objective item IDs must exist.
- Reward item IDs must exist.
- NPC quest references must exist.
- Recruitment is not purchasable.

## Prototype

Use `scripts/quest_model.py` for item-objective completion checks and reward preview.
