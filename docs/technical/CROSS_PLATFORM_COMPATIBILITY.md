# Cross-Platform Compatibility

Liminal Dominion should be developed on macOS when convenient, but the primary playable target is Windows PC. macOS support is required for development, data tools, validation, and early editor testing.

## Platform Targets

| Platform | Priority | Target |
|---|---:|---|
| Windows 10/11 PC | Primary | Playable packaged builds, QA, playtests |
| macOS Apple Silicon / Intel | Secondary | Development, data tooling, editor iteration where UE support allows |

## Development Rules

- Keep Python tooling compatible with the system Python on macOS and current Python on Windows.
- Prefer forward-slash paths in docs and scripts; use `pathlib.Path` in Python instead of hard-coded separators.
- Do not rely on shell-only behavior for core tooling. Provide Python scripts for repeatable tasks.
- Do not commit machine-local Unreal folders such as `Binaries/`, `Build/`, `DerivedDataCache/`, `Intermediate/`, or `Saved/`.
- Keep gameplay data in JSON seed files and export/import bridges so Windows and macOS builds use the same source data.
- Treat Windows packaged build checks as the release gate once the Unreal project exists.

## Command Equivalents

| Task | macOS Terminal | Windows PowerShell |
|---|---|---|
| Change folder | `cd /path/to/project` | `cd C:\path\to\project` |
| Install Python deps | `python3 -m pip install -r requirements.txt` | `py -m pip install -r requirements.txt` |
| Validate data | `python3 scripts/validate_seed_data.py` | `py scripts/validate_seed_data.py` |
| Run tests | `python3 -m unittest discover -s tests -v` | `py -m unittest discover -s tests -v` |
| Export DataTables | `python3 scripts/export_unreal_datatables.py` | `py scripts/export_unreal_datatables.py` |
| Full preflight | `python3 scripts/preflight_release.py` | `py scripts/preflight_release.py` |

## macOS Bash Basics

1. Open Terminal with Spotlight: press `Command + Space`, type `Terminal`, press `Return`.
2. Go to the project folder:

```bash
cd /Users/seanybear/Downloads/LiminalDominion_Codex_Starter
```

3. Run a command by pasting it and pressing `Return`:

```bash
python3 scripts/validate_seed_data.py
```

4. Useful Terminal commands:

```bash
pwd          # show current folder
ls           # list files
cd folder    # enter a folder
cd ..        # go up one folder
clear        # clear the screen
```

macOS now uses `zsh` by default, but almost every command in this repo is written as portable shell/Python and can be run from Terminal the same way.

## Unreal Build Expectations

When the UE5 project exists:

- Windows builds should be created and smoke-tested before any public playtest.
- macOS editor runs are allowed for iteration, but a macOS editor pass does not replace Windows packaged-build testing.
- Input, UI scaling, file paths, save paths, and data import/export must be tested on both platforms.
- Any platform-specific workaround belongs in docs or build scripts, not hidden in local machine settings.

See `docs/technical/WINDOWS_UNREAL_HANDOFF.md` before moving the project to a Windows Unreal workstation.
