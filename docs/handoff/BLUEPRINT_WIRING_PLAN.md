# Blueprint Wiring Plan

This file defines the first Blueprint behaviors that should turn the current graybox into a testable loop.

## Principle

Wire the smallest believable behavior first.

Do not aim for final systems. Aim for:

- readable
- testable
- stable
- easy to iterate

## First-Wave Actors

### `BP_DeploymentGate`

Minimum behavior:

- show interaction prompt
- on interact, begin run
- transition from hub to `LD_Level1_ServiceHalls_Greybox`

Needed data:

- simple run-active flag
- optional selected faction/loadout placeholder

### `BP_LootContainer`

Minimum behavior:

- show prompt
- allow one interaction
- award one or more test items
- prevent infinite reuse unless intentionally marked reusable

Needed data:

- `DT_Items`
- `DT_LootTables`

### `BP_ExtractionTrigger_Stable`

Minimum behavior:

- show prompt
- allow extraction with no special item
- end run successfully
- send player back to `LD_PersonalRoom_Greybox`

Needed data:

- `DT_Extractions`

### `BP_ExtractionTrigger_HiddenTicketBooth`

Minimum behavior:

- show prompt
- require Movie Ticket
- fail gracefully if the requirement is missing
- extract successfully if requirement is met

Needed data:

- `DT_Items`
- `DT_Extractions`

### `BP_PersonalStorage`

Minimum behavior:

- show prompt
- open a simple deposit UI or temporary debug interaction
- move carried loot into personal storage
- keep personal storage safe from death

Needed data:

- `DT_Items`
- `DT_Storage`

### `BP_ProjectBoard`

Minimum behavior:

- show prompt
- accept contribution items
- track partial progress
- visibly complete one placeholder upgrade state

Needed data:

- `DT_HubUpgrades`
- `DT_Items`

## Second-Wave Actors

### `BP_FlickerStalker`

Minimum behavior:

- patrol or idle in the service-halls encounter zone
- detect player
- chase
- trigger a death/failure state at close range

### `BP_TraderPlaceholder`

Minimum behavior:

- open a simple placeholder interaction
- optionally swap Movie Tickets for one test item

### `BP_QuartermasterPlaceholder`

Minimum behavior:

- identify as hub support interaction
- optionally provide starter loadout/debug refill behavior

### `BP_FactionSelectorPlaceholder`

Minimum behavior:

- let the player choose one faction in a debug-friendly way
- store the selection locally for the current session

## HUD Wiring

### `WBP_PlayerHUD`

Should display:

- sanity
- run state
- prompt text
- short carried-inventory summary
- feedback text for pickup, extract, fail, and deposit

### `WBP_RunResult`

Should display:

- extracted or died
- what was kept
- what was lost
- where the player returns next

## Map Ownership

Wire these map roles as the baseline:

- `LD_Hub_Greybox`
  - deployment gate
  - project board
  - trader
  - quartermaster
  - faction selector
- `LD_PersonalRoom_Greybox`
  - personal storage
  - relic display
- `LD_Level1_ServiceHalls_Greybox`
  - loot containers
  - stable extraction
  - hidden extraction
  - Flicker Stalker

## Acceptance Criteria

This pass is successful when:

- each first-wave Blueprint can be interacted with in-editor
- the player can complete a basic run and return
- the player can also fail a run and lose carried inventory
- personal storage survives failure
- the board can accept at least one contribution

## Do Not Overbuild Yet

- no multiplayer assumptions
- no final UI polish
- no economy balancing pass
- no final AI behavior tree complexity
- no art pass beyond clarity and readability
