# Next Codex Tasks

This file is the recommended execution order for the next Codex work on the repo.

## Priority Order

1. Replace the crashing Unreal DataTable row-struct path.
2. Turn the stamped Blueprint metadata into interaction logic.
3. Wire the first readable playable loop.
4. Bridge persistence and HUD state.
5. Run a full in-editor smoke test and tighten the backlog.

## Task 1: Replace the DataTable Row-Struct Path

- Read `docs/handoff/UNREAL_DATATABLE_IMPORT_PLAN.md`.
- Treat the current Python row structs in `Content/Python/ld_datatable_rows.py` as field references only.
- Keep `scripts/run_unreal_data_bootstrap.ps1` as the validation harness for the import pass, but do not rely on it until the row structs are replaced.
- Create the safe Unreal-side import path using editor-authored row structs or a native struct path.
- Import the exported CSVs into `Content/Data`.
- Start with these eight loop-critical tables:
  - `DT_Items`
  - `DT_LootTables`
  - `DT_Extractions`
  - `DT_Storage`
  - `DT_Sanity`
  - `DT_HubUpgrades`
  - `DT_PlayerState`
  - `DT_RunState`
- Then continue with the broader prototype-support tables.

## Task 2: Turn Metadata Into Core Blueprint Behavior

- Read `docs/handoff/BLUEPRINT_WIRING_PLAN.md`.
- The data variables already exist on the key Blueprint assets, and the placed actors already have prompts, IDs, and map paths stamped into the maps.
- Focus first on these actors:
  - `BP_DeploymentGate`
  - `BP_LootContainer`
  - `BP_ExtractionTrigger_Stable`
  - `BP_ExtractionTrigger_HiddenTicketBooth`
  - `BP_PersonalStorage`
  - `BP_ProjectBoard`
- Keep the implementations simple and testable.
- Prefer one reliable placeholder behavior over overbuilding.

## Task 3: Make the V0.1 Loop Walkable

- Read `docs/handoff/VERSION_0_1_PLAYABLE_LOOP.md`.
- Use the current stamped actor metadata instead of hardcoding values in every interaction graph.
- The first real target is:
  - start in hub
  - deploy
  - loot one or more containers
  - surface sanity loss
  - encounter the Flicker Stalker
  - extract
  - return to personal room
  - deposit loot
  - contribute to project board
- Use the smoke-test signage now stamped into the maps as the guide rails.

## Task 4: Wire HUD + Persistence

- Make `WBP_PlayerHUD` reflect:
  - sanity
  - prompt text
  - carried loot summary
  - player feedback messages
  - run-state feedback
- Make `WBP_RunResult` reflect:
  - extraction success
  - death result
  - carried-loot outcome
- Add simple local SaveGame placeholders only after the basic loop is behaving.

## Task 5: Smoke-Test and Update Docs

- Run the loop in-editor on Windows.
- Note what works, what fakes it, and what is still broken.
- Update:
  - `docs/handoff/CURRENT_STATUS.md`
  - `docs/backlog/CODEX_BACKLOG.md`
  - `docs/status/Liminal_Project_Status_2026-05-10.xlsx` or its successor workbook if the implementation snapshot materially changes

## Important Guardrails

- Do not reactivate the legacy C++ path unless explicitly needed.
- Do not commit generated Unreal folders.
- Do not spend time polishing art while the interaction loop is still incomplete.
- Favor stable Blueprint-first progress over speculative architecture.
