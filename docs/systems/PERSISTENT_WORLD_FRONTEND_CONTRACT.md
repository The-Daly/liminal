# Persistent World Frontend Contract

## Purpose

This document defines the product contract for the serious frontend and persistent-world-facing menu flow.

It does not commit the game to shipping full backend persistence yet. It defines the menu, data, and character rules the repo should build around now.

## World Model

- One official persistent world cluster exists alongside separate community servers.
- Official and community characters do not share progression.
- Official shard target is 90 players.
- Population target is 30 M.E.G., 30 B.N.T.G., and 30 Clippers.
- Faction commitment is bound to the character on that realm.
- Realm-wide mass wipes happen every 2 years.

## Menu Order

1. Title shell
2. Server browser
3. Character selection
4. Faction selection if needed
5. Minimal character setup
6. Main player menu

## Faction Commitment Rules

- Server selection comes before faction selection.
- A player can have separate characters on different realms.
- A character cannot switch faction until the current realm wipe completes.
- Returning players should go straight from server selection to existing character selection and then the main player menu.

## Character Framework Rules

- Character setup is preset-driven and minimal.
- The same lightweight parts library should support both player operators and NPC presets.
- Faction presentation should be readable at a glance.
- Identity-first presentation matters more than deep cosmetic variety in this phase.

## Required Data Contracts

- `ServerRealmDescriptor`
- `FactionPopulationState`
- `WipeSchedule`
- `CharacterProfile`
- `CharacterAppearanceDefinition`
- `FactionCharacterRules`
- `MenuFlowState`
- `MenuRoute`
- `CharacterSlotSummary`

## UI Shells Needed

- `WBP_TitleShell`
- `WBP_ServerBrowser`
- `WBP_FactionSelection`
- `WBP_CharacterSetup`
- `WBP_MainPlayerMenu`

## Unreal Notes

The current repo should treat these as shell assets first:

- widgets
- menu flow controller state
- preview actor anchors
- validated data contracts

The serious frontend pass should become real before full server authority is attempted.
