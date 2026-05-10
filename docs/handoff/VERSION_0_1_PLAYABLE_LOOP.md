# Version 0.1 Playable Loop

This file is the practical target loop for the current repo state.

## Purpose

Turn the current Unreal graybox into a short, readable, replayable local prototype.

The loop does not need polish yet. It needs clarity.

## Start State

- Player starts in `LD_Hub_Greybox` or returns to `LD_PersonalRoom_Greybox`.
- Player has a selected faction or a temporary debug default.
- Player has a minimal starter state:
  - flashlight or equivalent debug baseline
  - empty or nearly empty carried inventory

## Loop Steps

### Step 1: Prepare In Hub

- player can orient in the hub
- player can identify:
  - deployment gate
  - project board
  - trader
  - quartermaster
  - faction selector
- player can move to the deployment gate

### Step 2: Deploy

- interacting with the deployment gate starts a run
- player transitions into `LD_Level1_ServiceHalls_Greybox`
- HUD reflects active run state

### Step 3: Loot

- player can find at least one obvious loot container
- interacting with loot containers awards readable test loot
- carried inventory reflects the change

### Step 4: Pressure

- sanity drains during the run
- player can consume Almond Water or the equivalent placeholder recovery
- Flicker Stalker encounter space is readable and testable
- death/failure can be triggered

### Step 5: Extract

- stable extraction works without a special item
- hidden extraction works only with Movie Ticket if that path is tested
- extraction ends the run and returns the player to the personal room

### Step 6: Post-Run

- player can deposit kept loot into personal storage
- player can contribute qualifying items to the Signal Lamp Project
- result feedback is visible

### Step 7: Failure Case

- death ends the run
- carried inventory is cleared
- personal storage remains intact
- player can restart the loop

## Success Conditions

Version 0.1 is playable in the intended sense when a tester can:

1. start in the hub
2. deploy
3. loot
4. experience sanity pressure
5. encounter danger
6. extract or die
7. return
8. store loot
9. contribute to the board
10. repeat the loop

## Minimum Proof Requirements

- one successful run
- one failed run
- visible inventory change
- visible extraction result
- visible death result
- persistence of personal storage across failure

## Out Of Scope For This Loop

- multiplayer
- faction raids
- polished combat
- full NPC quest content
- final economy balance
- final art, sound, and animation passes

## Best Immediate Follow-Up

Once this loop works, the next pass should tighten:

- persistence
- HUD clarity
- board progression feedback
- trader/quartermaster utility
- atmosphere and pacing
