# Playable Loop Contract

This contract describes the first playable state the project is driving toward.

## Start State

- Player starts in hub or personal room.
- Player has selected a faction.
- Player has a starter loadout.
- Personal storage exists and persists locally.

## Run Start

- Player interacts with deployment gate.
- Run state becomes active.
- Level 1 Service Halls opens.

## During Run

- Loot containers provide items from `loot_level1_basic`.
- Sanity drains over time.
- Almond Water restores sanity.
- Flicker Stalker patrols, detects, chases, and kills at close range.

## Extract

- Stable extraction requires no item.
- Hidden ticket booth extraction requires a Movie Ticket.
- Extraction ends active run and returns player to personal room.

## Death

- Death ends active run.
- Carried inventory clears.
- Personal storage remains.

## Post-Run

- Player can deposit loot into personal storage.
- Player can contribute resources to Signal Lamp Project.
- SaveGame stores personal storage, completed hub upgrades, faction ID, and run history.
