# Playable Loop Contract

This contract describes the first playable state the project is driving toward.

## Start State

- Player starts in hub or personal room.
- Player has selected a faction.
- Player has a scarce starter loadout: faction identity tool plus flashlight only.
- Personal storage exists and persists locally.
- Same-faction players are allies; friendly fire and team killing are disabled.

## Run Start

- Player interacts with deployment gate.
- Run state becomes active.
- Level 1 Service Halls opens.

## During Run

- Loot containers provide items from `loot_level1_basic`.
- Level 1 loot is slim; weapons and armor are rare.
- Sanity drains over time.
- Almond Water restores sanity.
- Flicker Stalker patrols, detects, chases, and kills at close range.
- Gunshots may trigger no response, a sound-only response, or a level-specific entity approach.
- Trail String can mark a self/squad-visible route for one hour.
- Same-faction squads can share radio connection, Trail String visibility, and squad intent.

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
- SaveGame stores personal storage, partial and completed hub upgrade progress, faction ID, and run history.
- The current repo-side prototype for that payload lives in `scripts/persistence_model.py`.
