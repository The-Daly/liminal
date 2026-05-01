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
Read AGENTS.md first. Then read tasks/codex/000_START_HERE.md. Start with Task 001 only. Verify the data validation pipeline. Do not build gameplay yet.
```

## 4. First Local Test

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_seed_data.py
python3 -m unittest discover -s tests -v
python3 scripts/export_unreal_datatables.py
```

## 5. Codex Operating Rule

Codex builds. It does not redesign. Any new design rule goes into `docs/design/PROPOSALS.md`.
