# Next Codex Tasks

This file is the recommended execution order for the next Codex work on the repo.

## Priority Order

1. Complete the Unreal DataTable import path.
2. Wire the core Blueprint interactions.
3. Wire the first readable playable loop.
4. Bridge persistence and HUD state.
5. Run a full in-editor smoke test and tighten the backlog.

## Task 1: Finish the DataTable Path

- Read `docs/handoff/UNREAL_DATATABLE_IMPORT_PLAN.md`.
- Treat the current Python row structs in `Content/Python/ld_datatable_rows.py` as field references only.
- Create the safe Unreal-side import path using editor-authored row structs or a native struct path.
- Import the exported CSVs into `Content/Data`.
- Start with:
  - `DT_Items`
  - `DT_LootTables`
  - `DT_Extractions`
  - `DT_Storage`
  - `DT_Sanity`
- Then continue with the broader prototype-support tables.

## Task 2: Wire Core Blueprint Actors

- Read `docs/handoff/BLUEPRINT_WIRING_PLAN.md`.
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
  - `docs/status/Liminal_Project_Status_2026-05-10.xlsx` or its successor workbook if needed

## Important Guardrails

- Do not reactivate the legacy C++ path unless explicitly needed.
- Do not commit generated Unreal folders.
- Do not spend time polishing art while the interaction loop is still incomplete.
- Favor stable Blueprint-first progress over speculative architecture.
