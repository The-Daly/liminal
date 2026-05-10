# Unreal DataTable Import Plan

This file describes the safest current plan for getting the repo CSV exports into Unreal.

## Current Situation

- CSV export is working from `generated/unreal_datatables/`.
- The UE 5.7 automated Python import path is currently unsafe when using Python-generated row structs.
- `scripts/run_unreal_data_bootstrap.ps1` and `scripts/unreal_data_bootstrap.py` now attempt the eight-table import pass directly and currently reproduce the crash during `DT_Items` import.
- The reference row definitions currently live in `Content/Python/ld_datatable_rows.py`.
- Those Python structs now cover the first eight loop-critical table shapes, but they are still a field reference rather than the safe final import path.

## Goal

Import the repo CSVs into Unreal DataTables under `Content/Data` without crashing the editor.

## Recommended Safe Path

### Step 1: Use Editor-Authored or Native Row Structs

Create stable Unreal row structs for the first required tables:

- item row
- loot table row
- extraction row
- storage row
- sanity row
- hub upgrade row
- player state row
- run state row

If Blueprint struct assets are sufficient and stable, use those.
If they are not reliable enough for the final import path, use a native struct path later.

## Step 2: Import The First Required Tables

Import these first:

- `DT_Items.csv`
- `DT_LootTables.csv`
- `DT_Extractions.csv`
- `DT_Storage.csv`
- `DT_Sanity.csv`
- `DT_HubUpgrades.csv`
- `DT_PlayerState.csv`
- `DT_RunState.csv`

These unlock the first interaction wiring pass:

- item metadata
- loot rules
- extraction requirements
- storage caps
- sanity numbers

## Step 3: Import The Extended Support Tables

After the first eight are stable, import:

- `DT_Traders.csv`
- `DT_NPCs.csv`
- `DT_NPCRoster.csv`
- `DT_Quests.csv`
- `DT_Weapons.csv`
- `DT_Ammo.csv`
- `DT_CraftingRecipes.csv`
- `DT_Containers.csv`
- `DT_LevelLayouts.csv`
- `DT_NavigationMarkers.csv`
- `DT_NoiseResponses.csv`
- `DT_LootDensity.csv`
- `DT_SocialRules.csv`
- `DT_Factions.csv`
- `DT_Entities.csv`

## Import Location

Save imported DataTables under:

- `Content/Data`

Keep names aligned with the exported CSV names when practical.

## Field Reference Source

Use `Content/Python/ld_datatable_rows.py` as the field-shape reference for:

- field names
- field ordering
- broad data types

Do not treat it as the final safe automation path.

## Acceptance Criteria

The DataTable pass is complete when:

- the first required eight DataTables exist in `Content/Data`
- Unreal opens without a crash after those imports
- the tables can be referenced by Blueprint assets
- the project remains commit-clean outside intended content/config changes

## Known Risks

- Python-generated row structs may still crash the editor during automated import.
- Some CSV columns may need mild normalization if Unreal struct typing is stricter than the prototype export.
- Complex fields stored as strings may need Blueprint-side parsing or later schema tightening.

## Best Next Move For Codex

Codex should guide or implement the import plan in this order:

1. verify the exported CSV set
2. replace the Python-row-struct import path with editor-authored or native row structs
3. run `scripts/run_unreal_data_bootstrap.ps1`
4. confirm the first eight DataTables can be consumed by the first Blueprint wiring pass
