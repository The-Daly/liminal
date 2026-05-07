# Unreal Graybox Implementation Spec

This file is the build target for the first Unreal pass. The repo now includes `LiminalDominion.uproject`, but the active path is content-first visualization rather than a compiled C++ gameplay module.

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
- Deployment gate actor that starts the Level 1 run and opens the Service Halls map.
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
- Player HUD widget for sanity, prompts, carried stacks, messages, and run state.
- Run result widget for extraction/death.

## Current Project State

- `LiminalDominion.uproject` opens as a content-first Unreal project and currently starts from the UE5 Open World template.
- `Content/Maps`, `Content/Blueprints`, `Content/Data`, and `Content/UI` are the repo-owned target folders for the first Unreal pass.
- The first saved `.umap` assets and Blueprint assets are still missing and must be created inside the editor.
- The previous gameplay C++ skeletons are preserved in `Source_Legacy/` for later reactivation once the Windows Visual Studio toolchain is fully ready.

## Data Dependency

The current content-first path should import CSV files from `generated/unreal_datatables/` into Unreal DataTables under `Content/Data`.

The first required import is `DT_Items.csv`. That asset becomes the source for stackability, max-stack limits, trader item metadata, and storage UI display.

## Save Dependency

V0.1 save behavior remains intentionally local. The immediate graybox goal is to prove personal storage persistence and hub project completion without committing to the later server-authoritative Realm model.

If the archived C++ save bridge is re-enabled later, it should remain a local-only proof layer until the core loop is playable.

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
