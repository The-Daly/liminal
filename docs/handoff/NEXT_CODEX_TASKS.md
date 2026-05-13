# Next Codex Tasks

This file is the recommended execution order for the next Codex work on the repo.

## Priority Order

1. Replace the crashing Unreal DataTable row-struct path.
2. Turn the serious frontend menu shells into a real flow controller pass.
3. Turn the stamped Blueprint metadata into interaction logic.
4. Wire the first readable playable loop.
5. Bridge persistence and HUD state.

## Task 1: Replace the DataTable Row-Struct Path

- Read `docs/handoff/UNREAL_DATATABLE_IMPORT_PLAN.md`.
- Read `docs/technical/DATATABLE_IMPORT_FIX_PLAN.md`.
- Treat the current Python row structs in `Content/Python/ld_datatable_rows.py` as field references only.
- Keep `scripts/run_unreal_data_bootstrap.ps1` as the validation harness for the import pass, but do not rely on it until the row structs are replaced.
- Create the safe Unreal-side import path using editor-authored row structs or a native struct path.
- The repo now already contains a dormant minimal native row-struct module under `Source_DormantDataRows/`; move it back into an active `Source/` path only after the Windows MSVC toolchain is updated, or continue with editor-authored struct assets immediately.
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
- Note that starter loadouts are currently derived from `DT_Factions` + `scripts/faction_model.py`; there is not yet a separate exported `DT_Loadouts.csv`.

## Task 2: Turn the Serious Frontend Shell Into Real Menu Flow

- The repo now has server/wipe/faction/menu contracts plus local frontend session persistence.
- The menu controller and widgets now have variables for:
  - current and next route
  - primary, secondary, and back target routes
  - selected realm/server type/faction/character/appearance
  - server name, region, wipe summary, faction population summary
  - faction-lock warning, callsign, identity item, and deploy-enabled state
- The frontend shell pass now also stamps default class values into:
  - `BP_MenuFlowController`
  - `WBP_TitleShell`
  - `WBP_ServerBrowser`
  - `WBP_CharacterSelection`
  - `WBP_FactionSelection`
  - `WBP_CharacterSetup`
  - `WBP_MainPlayerMenu`
  - `WBP_DeployPanel`
  - `WBP_StashPanel`
  - `WBP_SettingsPanel`
- The hub map now also contains a serious frontend staging wing with:
  - one placed `BP_MenuFlowController`
  - one operator preview anchor
  - three faction/NPC preview anchors
- Use the repo-side helpers in:
  - `scripts/frontend_menu_model.py`
  - `scripts/persistent_world_model.py`
  - `scripts/persistence_model.py`
- The route model now exposes validated transition targets and invalid-hop rejection for:
  - title to server browser
  - server browser to character/faction paths
  - hub to deploy/stash
  - subpanel return to hub
- The operations-hub presentation model now exposes:
  - left-rail nav defaults
  - center deployment brief copy
  - right-rail operator status copy
  - footer telemetry copy
- The frontend shell pass now also rebuilds `WBP_MainPlayerMenu` into the current operations-console layout before wiring variables and defaults.
- The frontend shell pass now also rebuilds and places `BP_MainMenuPawn` in `LD_Level1_ServiceHalls_Greybox`, and `BP_LDGameMode` now boots directly into that menu pawn so the selection screen does not drop into a live player character.
- The current graybox menu path also has a repo-owned runtime state controller in `Content/Python/ld_menu_runtime.py` for keyboard/click-driven shell navigation while the final UMG graph path is unfinished.
- The current graybox playable loop also has a repo-owned PIE runtime bridge in `Content/Python/ld_playable_loop_runtime.py` that can exercise deploy, loot, sanity, extract, deposit, and board flow before the final Blueprint graph pass is complete.
- Wire the title -> server browser -> faction selection -> character setup -> main player hub sequence in Unreal.
- Keep it shell-simple but functional.

## Task 3: Turn Metadata Into Core Blueprint Behavior

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

## Task 4: Make the V0.1 Loop Walkable

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

## Task 5: Wire HUD + Persistence

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

## Task 6: Smoke-Test and Update Docs

- Run the loop in-editor on Windows.
- Start each pass from `powershell -ExecutionPolicy Bypass -File .\scripts\run_v01_smoke_check.ps1`.
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
