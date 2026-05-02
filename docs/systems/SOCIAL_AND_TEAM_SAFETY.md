# Social And Team Safety

This system defines how players group up without creating team-kill griefing.

## Locked Intent

- Players in the same faction are already on the same team.
- Players cannot damage or kill members of their own faction.
- Squads are opt-in social groups inside a faction, not a separate team allegiance.
- Squads must be same-faction only.
- Radios connect squadmates to one another.
- Cross-faction radio channels are not part of V0.1.

## Friendly Fire

Friendly fire is disabled at two layers:

- Same faction damage: disabled.
- Same squad damage: disabled.

Future PvP only applies between opposing factions or approved raid/conflict rules. It should never allow a player to kill a same-faction teammate.

## Squads

V0.1 squads are designed to make players feel connected while preserving faction identity.

- Max squad size: 4.
- Membership: same faction only.
- Shared channels: radio, Trail String visibility, squad pings, quest intent.

## Radios

Radios are the first communication-binding item/system.

- A radio connects the squad, not the whole world.
- Radios do not create cross-faction voice/comms by default.
- Later upgrades can improve range, signal quality, or interference resistance without changing the no-team-kill rule.

## Data Files

- `data/seed/social_rules.seed.json`
- `data/schemas/social_rule.schema.json`
- `scripts/social_model.py`
