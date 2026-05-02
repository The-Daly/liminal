# AI Context Brief

Use this brief when a coding agent needs quick project context.

## Game

Liminal Dominion is a Backrooms-inspired hard-loss extraction survival PvPvE game. Version 0.1 is a graybox prototype proving one loop, not the full MMO/faction-war game.

## V0.1 Loop

Hub/personal room -> deploy to Level 1 Service Halls -> loot -> manage sanity -> encounter Flicker Stalker -> extract or die -> return to personal room -> store loot or contribute to hub progression.

## Non-Negotiables

- Unreal Engine 5 target.
- Windows PC is the primary playable build target.
- macOS is a supported development/tooling target.
- Death deletes carried inventory.
- Personal storage is safe and capped.
- Shared faction storage is larger and raid-risk later.
- Faction switching means full Realm reset later.
- NPC recruitment is earned through quests, not purchase.
- No full multiplayer, raids, procedural generation, or deep NPC systems in V0.1.

## Data Rule

Prefer seed JSON and validation first. Do not hard-code game constants that already belong in seed data.

## Current Source Status

The repo has a UE5 source scaffold and C++ classes, but first Unreal Editor compile still needs to happen on a machine with Unreal installed. Until then, use Python prototypes and data validation for non-editor work.
