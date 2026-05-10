# Codex Quickstart

## 1. Install Codex CLI

Use the official Codex CLI install path for your system.

## 2. Open This Folder

```bash
cd LiminalDominion_Codex_Starter
codex
```

## 3. First Prompt to Paste into Codex

```text
Read AGENTS.md first. Then read docs/handoff/CURRENT_STATUS.md, docs/handoff/NEXT_CODEX_TASKS.md, docs/handoff/UNREAL_DATATABLE_IMPORT_PLAN.md, docs/handoff/BLUEPRINT_WIRING_PLAN.md, and docs/handoff/VERSION_0_1_PLAYABLE_LOOP.md. Continue from the current Unreal graybox/DataTable/Blueprint wiring phase. Do not restart the old validation-only scaffold tasks.
```

## 4. First Local Test

On macOS Terminal:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_seed_data.py
python3 -m unittest discover -s tests -v
python3 scripts/export_unreal_datatables.py
python3 scripts/check_dev_environment.py
```

On Windows PowerShell:

```powershell
py -3 -m pip install -r requirements.txt
py -3 scripts/validate_seed_data.py
py -3 -m unittest discover -s tests -v
py -3 scripts/export_unreal_datatables.py
py -3 scripts/check_dev_environment.py
```

## 5. Platform Rule

Windows 10/11 PC is the primary playable target. macOS remains supported for development and editor iteration. See `docs/technical/CROSS_PLATFORM_COMPATIBILITY.md`.

## 6. Codex Operating Rule

Codex builds. It does not redesign. Any new design rule goes into `docs/design/PROPOSALS.md`.
