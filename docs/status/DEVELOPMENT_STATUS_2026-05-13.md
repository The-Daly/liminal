# Development Status

Date: May 13, 2026
Project: `LiminalDominion.uproject`
Repo: `https://github.com/The-Daly/liminal`
Platform Focus: Windows + Unreal Engine 5.7

## Executive Summary

Liminal Dominion is currently in a playable graybox prototype stage with a strong repo-side design and systems foundation, a defined serious menu direction, and a working in-engine menu boot path. The project is not yet a full playable extraction game, but it is no longer just documentation and loose shell work either. The repo now contains a real Unreal project, versioned maps, first-wave Blueprint assets, serious frontend/menu contracts, persistence contracts, prototype systems logic, and a visible in-game menu presentation layer.

The project has moved out of the early setup phase and is now in the "turn shells into real interaction" phase.

## Current Development Stage

The game is in a Blueprint-first prototype buildout stage.

That means:
- the core design direction is defined
- the Unreal project is real and versioned
- the maps and placeholder actors exist
- the serious menu look and menu-state model exist
- several systems exist as repo-side data models and simulation logic
- the next major work is runtime interaction wiring inside Unreal

This is not yet:
- a full end-to-end polished gameplay loop
- a final UI implementation
- a live multiplayer/server implementation
- a final DataTable/runtime content pipeline

## What Is Already Built

### 1. Unreal Project Foundation

- `LiminalDominion.uproject` is the active Unreal project.
- The repo is set up for Windows-first Unreal development.
- Unreal launches from the repo correctly.
- The project is content-first and Blueprint-first.
- Legacy C++ scaffolding remains archived under `Source_Legacy` and is not the active path.

### 2. Versioned Graybox Maps

The repo includes these saved maps:
- `Content/Maps/LD_Hub_Greybox.umap`
- `Content/Maps/LD_PersonalRoom_Greybox.umap`
- `Content/Maps/LD_Level1_ServiceHalls_Greybox.umap`

These maps now support the current prototype structure:
- Hub space
- Personal room/storage space
- Level 1 service halls test space

### 3. Serious Frontend / Menu Direction

The project now has a defined serious operations-console menu direction inspired by tense extraction-game presentation, but grounded in Liminal’s own Backrooms tone.

Built menu/frontend work includes:
- title shell
- server browser shell
- character selection shell
- faction selection shell
- character setup shell
- main player menu shell
- deploy panel shell
- stash panel shell
- settings panel shell

Repo-side frontend logic exists for:
- route flow
- target route transitions
- faction lock warnings
- realm/server summaries
- wipe summaries
- character summary snapshots
- operations-hub dashboard copy

### 4. Working In-Game Menu Boot

The project now has a working menu boot presentation inside Unreal.

Current working behavior:
- pressing `Play` boots into a menu presentation state instead of a live gameplay character
- the menu is rendered in front of the camera in the Level 1 menu room
- the menu presentation uses a generated operations overlay and a dedicated menu pawn path

Important note:
- this is a working prototype render path, not the final full UMG-to-viewport implementation yet
- it exists to guarantee that the menu is visible and testable in-engine right now

Key assets and scripts for this:
- `Content/Blueprints/BP_MainMenuPawn.uasset`
- `Content/UI/T_MenuOperationsOverlay.uasset`
- `Content/UI/M_MenuOperationsOverlay.uasset`
- `scripts/generate_menu_overlay.py`
- `scripts/unreal_ingame_menu_spawn.py`

### 5. First-Wave Blueprint Actor Shells

The repo contains first-wave Blueprint assets for the extraction loop structure, including placeholders for:
- deployment
- loot
- extraction
- storage
- project board
- faction/preview anchors
- frontend menu flow
- HUD/menu widgets

Placed map actors have already been stamped with metadata such as:
- prompts
- run IDs
- extraction IDs
- storage IDs
- board IDs
- return map paths

This is important because the project no longer needs to invent these contracts from scratch during the next Blueprint pass.

### 6. Repo-Side Systems Models

The repo-side Python layer already covers a large portion of game logic and design truth, including:
- inventory logic
- storage cap behavior
- carried-vs-personal item handling
- sanity logic
- extraction logic
- project board contributions
- run-state logic
- persistence payloads
- menu flow logic
- persistent world contracts
- realm/faction/wipe modeling
- operator appearance presets
- weapons/ammo/crafting/containers
- NPC roster and quest structures

This means the design intent is much more mature than the current in-editor runtime wiring.

## What Is Working Right Now

### Repo Workflow

- local repo workflow is stable
- git commits and pushes are working
- Windows validation flow is working
- Unreal export and scaffold checks are working

### Validation and Tooling

These repo checks are passing:
- `py -3 -m unittest discover -s tests -v`
- `py -3 scripts/preflight_release.py`
- seed validation
- Unreal CSV export
- scaffold checks

### Unreal Presentation Layer

- maps exist and open
- current menu boot presentation is visible in-engine
- the operations menu overlay has been backtested with generated camera captures
- the menu no longer fails into the blank-room-only state that was blocking progress earlier

## What Is Not Finished Yet

### 1. Final Menu Runtime

The current menu is visible and usable as a presentation boot, but the final intended menu architecture is still ahead.

Still missing:
- proper fullscreen UMG `AddToViewport` implementation
- final controller/mouse/UI input mode setup
- clickable full route flow across all menu screens
- finished menu transitions between screens

### 2. DataTable Import Path

This remains one of the biggest technical blockers.

Current problem:
- UE 5.7 crashes when using Python-defined row structs for the import path

As a result:
- DataTable shapes exist as references
- CSV exports exist
- the actual safe Unreal-native import path is still not finished

### 3. Blueprint Runtime Wiring

The project has many shells and contracts, but the actual runtime gameplay behavior is still incomplete.

Still needs to be wired:
- deployment gate behavior
- loot pickup behavior
- stable extraction behavior
- hidden extraction requirement behavior
- storage deposit behavior
- project board contribution behavior
- sanity feedback during the run
- HUD live updates
- run results screen

### 4. Full Playable Loop

The intended loop is clearly defined, but it is not yet fully live in-editor.

Target loop:
- open menu
- choose path / deploy
- enter service halls
- loot
- manage sanity pressure
- extract or die
- return to room/hub state
- store items
- contribute to board progress

The project is close enough to see the shape of this loop, but not yet fully running as a player experience.

### 5. Persistent Multiplayer/Server Architecture

The long-term model is defined, but the real implementation is not built yet.

Defined at the contract level:
- official vs community servers
- 90-player official target
- 30 players per faction
- realm-bound character progression
- faction lock until wipe
- 2-year wipe cadence

Not built yet:
- actual server browser backend
- account/session integration
- real server population updates
- actual online multiplayer play

## Current Technical Truth

The most important thing to understand about development right now is this:

The repo is ahead of the in-editor runtime.

That means:
- the design contracts are fairly strong
- the system models are much more complete than the actual Blueprint gameplay behavior
- the project now needs implementation passes more than planning passes

The next work should focus less on inventing new documents and more on:
- turning existing menu shells into a real route flow
- turning stamped actor metadata into real interactions
- solving the safe Unreal DataTable path
- making the first full graybox loop playable

## Current Risks / Blockers

### High Priority Blockers

- Unreal DataTable import path is still unstable with Python row structs
- frontend route flow is visually present but not yet fully interactive
- Blueprint interaction graphs are still incomplete

### Medium Priority Risks

- current menu boot uses a reliable prototype render path, but not yet the final intended UMG architecture
- too much additional shell-building without runtime wiring would slow progress
- if interaction logic is added before stable data import, some behavior may need rework later

## Recommended Next Development Steps

### Immediate Next Step

Replace the crashing DataTable struct/import path with a safe Unreal-native path.

### After That

1. Turn the serious menu shells into a working route flow:
   - title
   - server browser
   - character selection
   - faction selection
   - character setup
   - main player menu

2. Wire the first-wave Blueprint actors:
   - deployment
   - loot
   - extraction
   - storage
   - board

3. Make the first graybox loop fully playable.

4. Bridge HUD and persistence into that loop.

## Bottom Line

Liminal Dominion is currently in a strong prototype-construction phase.

The project is no longer blocked by setup, empty maps, or missing direction. It now has:
- a real Unreal repo
- real maps
- a visible serious menu
- strong contracts
- strong prototype data models
- a clear gameplay loop target

The project’s main challenge now is not "what should the game be?" but "finish wiring the existing design into real Unreal runtime behavior."
