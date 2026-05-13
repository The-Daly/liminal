# V0.1 Smoke Test

This checklist is the repeatable manual test for the first graybox playable loop:

`title/server/faction/character/main menu -> deploy -> loot -> sanity -> encounter -> extract -> deposit -> contribute`

## Scope

This test is intentionally narrow.

It does **not** validate:

- multiplayer
- full raids
- polished UI
- final NPC AI
- full weapon systems
- final DataTable polish

It does validate the first playable-loop backbone.

## Pre-Run Repo Check

From the repo root:

```powershell
cd "C:\Users\seand\Documents\New project\liminal"
powershell -ExecutionPolicy Bypass -File .\scripts\run_v01_smoke_check.ps1
```

Expected result:

- seed validation passes
- CSV export passes
- unit tests pass
- the script prints the editor checklist below

## Unreal Manual Test Setup

1. Open:
   - `C:\Users\seand\Documents\New project\liminal\LiminalDominion.uproject`
2. Confirm the startup flow opens into the menu presentation state instead of a live gameplay character.
3. Use the current menu controls to move through the shell flow:
   - title
   - server browser
   - character selection
   - faction selection
   - character setup
   - main menu

## Manual Test Checklist

### 1. Menu Boot

- [ ] Project opens without crash.
- [ ] Play enters the menu presentation state.
- [ ] The player is not dropped into a normal gameplay pawn.

### 2. Frontend Routing

- [ ] Title route advances forward.
- [ ] Server browser route advances forward.
- [ ] Character selection route advances forward.
- [ ] Faction selection route advances forward.
- [ ] Character setup route advances forward.
- [ ] Main player menu becomes reachable.
- [ ] Basic back-route behavior works.

### 3. Deploy

- [ ] The deploy control routes into `LD_Level1_ServiceHalls_Greybox`.
- [ ] The Level 1 run starts from the intended graybox state.

### 4. Loot

- [ ] At least one `BP_LootContainer` can be interacted with.
- [ ] The interaction grants placeholder loot.
- [ ] Test pickup includes expected prototype items such as:
  - `currency_old_movie_ticket`
  - `consumable_almond_water`
- [ ] Inventory or debug feedback updates after pickup.

### 5. Sanity

- [ ] Run sanity starts at the expected default value.
- [ ] Sanity drains during the run or through the runtime debug path.
- [ ] Almond Water restores sanity.
- [ ] The player receives visible or log feedback for sanity changes.

### 6. Encounter

- [ ] The Flicker Stalker placeholder creates a real threat.
- [ ] The threat produces at least one of:
  - chase pressure
  - damage
  - sanity loss
  - retreat pressure

### 7. Extraction

- [ ] Stable extraction returns the player from Level 1.
- [ ] Extracted inventory is preserved.
- [ ] Conditional extraction respects its requirement if used.

### 8. Personal Storage

- [ ] The player can deposit extracted loot.
- [ ] Deposited loot is separate from carried run inventory.
- [ ] Personal storage survives the post-run transition.

### 9. Project Board

- [ ] The player can contribute Movie Tickets or placeholder resources.
- [ ] Board progress changes after contribution.
- [ ] Signal Lamp progress is visible as the current placeholder upgrade target.

## Pass Criteria

The smoke test passes when a tester can complete:

1. menu boot
2. frontend route to main menu
3. deploy into Level 1
4. loot pickup
5. sanity feedback
6. encounter pressure
7. extraction
8. deposit
9. contribution

## Current Known Gaps

- The DataTable asset import path is still blocked until the editor-authored struct pass is completed.
- The serious frontend is still a graybox shell/runtime path, not a final clickable UMG implementation.
- Some interactions may still use placeholder runtime values before imported DataTables are fully live inside Unreal.

## Failure Logging

When a step fails, record:

- exact screen or map
- actor or widget name
- expected behavior
- actual behavior
- whether it blocks the rest of the loop
