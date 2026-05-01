# Unreal Graybox Implementation Spec

This file is the build target for the first Unreal pass. The current package does not include `.uproject` files yet.

## Project Target

- Engine: Unreal Engine 5.
- Mode: single-player/local graybox prototype.
- Content style: simple BSP/static mesh primitives, clear landmarks, no final art dependency.
- Data source: validated JSON seed data converted to DataTables or imported into equivalent UE assets.

## Required Maps

- `LD_Hub_Greybox`: faction hub shell, personal room entrance, vault placeholder, trader placeholder, project board, deployment gate.
- `LD_PersonalRoom_Greybox`: capped safe storage, relic display placeholder, return point after extraction.
- `LD_Level1_ServiceHalls_Greybox`: service corridor, storage bay, utility rooms, abandoned theater corner, archive office, broken trader kiosk, crawlspace route, Flicker Corridor, stable extraction, hidden extraction.

## Required Gameplay Actors

- Player pawn/controller with interact, pickup, consume, extract, and debug death actions.
- Loot container actor bound to `loot_level1_basic`.
- Extraction trigger actor bound to extraction seed data.
- Storage actor for personal storage and shared faction vault placeholder.
- Project board actor bound to the Signal Lamp Project contribution requirements.
- Flicker Stalker actor with patrol, perception radius, chase, attack, and return-to-patrol.
- Hub project board actor that accepts contribution items and unlocks one visible placeholder upgrade.

## Required UI

- Sanity meter.
- Inventory list.
- Interaction prompt.
- Pickup feedback.
- Extraction/death result screen.
- Minimal faction/loadout debug selector until onboarding is built.
- Player HUD widget bound to `ALDPlayerCharacter` HUD snapshots.
- Run result widget for extraction/death.

## Current Source Skeletons

- `ALDPlayerCharacter`: owns carried inventory, personal storage, sanity, and run state components.
- `FLDHUDSnapshot`: Blueprint-facing UI state for sanity, carried stacks, prompts, and run status.
- `ULDGameDataSubsystem`: runtime lookup for imported DataTables, starting with item stack metadata.
- `ULDRunStateComponent`: starts runs, handles extraction, and clears carried inventory on death.
- `ILDInteractable`: common Blueprint-facing interaction contract.
- `ALDLootContainer`: interactable loot source.
- `ALDExtractionTrigger`: interactable extraction gate.
- `ALDStorageActor`: personal/shared storage placeholder.
- `ALDProjectBoardActor`: contribution/project completion placeholder.
- `ALDFlickerStalker`: entity state and range helper.

## Data Dependency

Item add paths should prefer `ULDInventoryComponent::AddItemFromData`, which asks `ULDGameDataSubsystem` for stackability and max stack size from `DT_Items`. The permissive fallback is only for early graybox use before DataTables are imported.

## Default Input

- Move: `WASD`
- Look: mouse
- Jump: `Space`
- Interact: `E`
- Consume Almond Water: `Q`
- Debug death: `K`

## Smoke Test

1. Start in the hub or personal room.
2. Select a faction starter loadout.
3. Deploy through the diegetic corridor.
4. Loot at least one container.
5. Lose sanity over time.
6. Use Almond Water to restore sanity.
7. Encounter the Flicker Stalker.
8. Extract through the stable extraction.
9. Return to the personal room.
10. Store loot or contribute it to the project board.
11. Trigger death in a second run and verify carried inventory is lost while personal storage remains.
