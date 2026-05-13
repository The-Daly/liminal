# DataTable Import Fix Plan

## Problem

The current Unreal Engine 5.7 import path crashes when `scripts/run_unreal_data_bootstrap.ps1` attempts to import `generated/unreal_datatables/DT_Items.csv` using Python-defined row structs from `Content/Python/ld_datatable_rows.py`.

`ld_datatable_rows.py` is still useful as a field reference, but it should not remain the final import path for loop-critical gameplay tables.

## Why The Current Python Row-Struct Path Crashes

- The current path relies on `@unreal.ustruct()` definitions created from the Python bridge at editor runtime.
- UE 5.7 is not handling the `DT_Items` CSV import safely when the row struct only exists through that Python-generated reflection layer.
- The crash is reproducible through the existing harness:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_unreal_data_bootstrap.ps1`
- The failure happens early enough that the exported CSV pipeline itself is not the issue.
- The exported CSV files should remain the source of truth.
- The unstable piece is the transient Python-defined row-struct import target.

## Recommended Replacement Approach

### Recommended for the current repo

Use **editor-authored Unreal Blueprint Struct assets** for the loop-critical table row types, then import the CSV files into `Content/Data` using those struct assets.

This is the recommended path because:

- the active project is content-first and Blueprint-first
- the live Unreal project is already functioning without an enabled native source module
- the repo keeps `Source_Legacy`, but does not currently use an active C++ gameplay path
- the user asked to keep scope tight and move the graybox loop forward, not reactivate a broader native stack

### Not recommended for the current pass

Do **not** keep the final import path on Python-generated row structs.

### Native struct fallback

If the team later decides to re-enable a native module, the same field layouts below can be moved into `FTableRowBase` structs in C++. That is a valid long-term path, but it is not required to unblock the current Blueprint-first graybox loop.

## Current Repo State

The repo now includes a **minimal dormant native module scaffold** under:

- `Source/LiminalDominion/`
- `Source/LiminalDominion.Target.cs`
- `Source/LiminalDominionEditor.Target.cs`

That scaffold contains native row-struct definitions for the loop-critical tables. It is intentionally **not active in the `.uproject` boot path yet** because this machine currently fails Unreal 5.7 native compilation with an outdated MSVC toolchain.

Current local compiler blocker:

- Unreal 5.7 requires a newer Visual Studio 2022 MSVC v143 toolchain than the one installed on this machine
- `scripts/run_unreal_data_bootstrap.ps1` now reports that clearly and falls back to editor-authored struct assets if they exist

This means the repo now supports **both** of the real replacement paths:

1. native row structs after the Windows toolchain is updated
2. editor-authored struct assets immediately, without waiting for native compile

## Loop-Critical Tables To Prioritize

Import these first:

1. `DT_Items`
2. `DT_Factions`
3. `DT_LootTables`
4. `DT_Extractions`
5. `DT_Storage`
6. `DT_HubUpgrades`
7. `DT_PlayerState`
8. `DT_RunState`

Also import `DT_Sanity` in the same pass because the first smoke-test loop depends on it directly.

## Required Row Struct Fields

The fields below should be copied from the exported CSV headers and the existing Python field reference.

### `ST_ItemRow` for `DT_Items`

- `item_id` `String`
- `display_name` `String`
- `category` `String`
- `rarity` `String`
- `stackable` `Boolean`
- `max_stack` `Integer`
- `weight` `Float`
- `value_tickets` `Integer`
- `can_be_lost_on_death` `Boolean`
- `can_display_in_room` `Boolean`
- `display_location` `String`
- `faction_restriction` `String`
- `description` `String`

### `ST_FactionRow` for `DT_Factions`

- `faction_id` `String`
- `display_name` `String`
- `role` `String`
- `starting_items` `String`
- `hub_upgrade_focus` `String`
- `description` `String`

Note:
- `starting_items` and `hub_upgrade_focus` are currently exported as JSON strings.
- For the first safe import pass, keep them as plain `String` fields rather than trying to import nested arrays in the struct.

### `ST_LootTableRow` for `DT_LootTables`

- `loot_table_id` `String`
- `entries` `String`

Note:
- `entries` should remain a JSON string in the first import pass.

### `ST_ExtractionRow` for `DT_Extractions`

- `extraction_id` `String`
- `display_name` `String`
- `level_id` `String`
- `transition_pattern` `String`
- `availability` `String`
- `required_item_ids` `String`
- `description` `String`

### `ST_StorageRow` for `DT_Storage`

- `storage_id` `String`
- `display_name` `String`
- `storage_type` `String`
- `safe_from_death` `Boolean`
- `raid_risk` `Boolean`
- `caps` `String`
- `description` `String`

### `ST_SanityRow` for `DT_Sanity`

- `sanity_rule_id` `String`
- `display_name` `String`
- `min_sanity` `Float`
- `max_sanity` `Float`
- `base_drain_per_minute` `Float`
- `low_sanity_threshold` `Float`
- `almond_water_restore` `Float`
- `description` `String`

### `ST_HubUpgradeRow` for `DT_HubUpgrades`

- `hub_upgrade_id` `String`
- `display_name` `String`
- `faction_id` `String`
- `contribution_requirements` `String`
- `visible_unlock` `String`
- `description` `String`

### `ST_PlayerStateRow` for `DT_PlayerState`

- `player_state_id` `String`
- `faction_id` `String`
- `carried_storage_id` `String`
- `personal_storage_id` `String`
- `starting_sanity` `Float`
- `description` `String`

### `ST_RunStateRow` for `DT_RunState`

- `run_state_id` `String`
- `level_id` `String`
- `loot_table_id` `String`
- `entity_ids` `String`
- `extraction_ids` `String`
- `sanity_rule_id` `String`
- `description` `String`

## Loadout Note

There is currently **no exported `DT_Loadouts.csv`** in `generated/unreal_datatables/`.

Starter loadouts are presently derived from:

- `data/seed/factions.seed.json`
- `scripts/faction_model.py`

For the current smoke-test loop, treat faction starter loadouts as a faction-data concern rather than inventing a new Unreal DataTable. Do not add a new gameplay mechanic here.

## Exact Unreal 5.7 Execution Plan

### Step 1: Create struct assets in the editor

Inside Unreal:

1. Open `LiminalDominion.uproject`.
2. In `Content/Data`, create Blueprint Struct assets:
   - `ST_ItemRow`
   - `ST_FactionRow`
   - `ST_LootTableRow`
   - `ST_ExtractionRow`
   - `ST_StorageRow`
   - `ST_SanityRow`
   - `ST_HubUpgradeRow`
   - `ST_PlayerStateRow`
   - `ST_RunStateRow`
3. Add the fields listed above exactly.
4. Keep JSON-like columns as `String` fields for this pass.

### Step 2: Import the CSV files

Import from `generated/unreal_datatables/` into `Content/Data`:

- `DT_Items.csv` using `ST_ItemRow`
- `DT_Factions.csv` using `ST_FactionRow`
- `DT_LootTables.csv` using `ST_LootTableRow`
- `DT_Extractions.csv` using `ST_ExtractionRow`
- `DT_Storage.csv` using `ST_StorageRow`
- `DT_Sanity.csv` using `ST_SanityRow`
- `DT_HubUpgrades.csv` using `ST_HubUpgradeRow`
- `DT_PlayerState.csv` using `ST_PlayerStateRow`
- `DT_RunState.csv` using `ST_RunStateRow`

### Step 3: Save repo-owned assets

Save all created struct and DataTable assets under:

- `Content/Data`

### Step 4: Confirm config alignment

`Config/DefaultGame.ini` already points to the intended DataTable asset paths:

- `/Game/Data/DT_Items.DT_Items`
- `/Game/Data/DT_LootTables.DT_LootTables`
- `/Game/Data/DT_Extractions.DT_Extractions`
- `/Game/Data/DT_Storage.DT_Storage`
- `/Game/Data/DT_Sanity.DT_Sanity`
- `/Game/Data/DT_HubUpgrades.DT_HubUpgrades`
- `/Game/Data/DT_PlayerState.DT_PlayerState`
- `/Game/Data/DT_RunState.DT_RunState`

If the imported assets use those exact names, no config change is needed.

## Validation Steps

The fix is proven only when all of the following are true:

1. Unreal imports the first nine tables above without crashing.
2. Unreal closes and reopens cleanly after those imports.
3. The imported DataTables remain present in `Content/Data`.
4. The row counts match the exported CSVs.
5. The default IDs in `Config/DefaultGame.ini` still resolve to valid rows:
   - `player_state_v0_meg`
   - `run_level1_service_halls_v0`
   - `hub_project_board_signal_lamp_v0`
6. First-wave Blueprint assets can reference the DataTables without editor errors.
7. The smoke-test loop can use imported table values for:
   - loot lookup
   - sanity defaults
   - extraction rules
   - storage caps
   - board contribution requirements

## What Stays Preserved

- `data/seed/*.seed.json` remains the source data layer.
- `scripts/validate_seed_data.py` remains the validation pass.
- `scripts/export_unreal_datatables.py` remains the export pass.
- `generated/unreal_datatables/` remains the Unreal CSV handoff layer.

## Out Of Scope For This Fix

- final nested struct cleanup for every JSON-like field
- multiplayer replication
- new mechanics
- full inventory UI polish
- reactivation of the legacy source tree just for this import pass
