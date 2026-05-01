# Install Unreal Engine On This Mac

Unreal Engine installation on macOS is a GUI/browser flow because Epic Games Launcher requires account sign-in.

## Install Flow

1. Open the official Unreal download page:
   - https://www.unrealengine.com/download
2. Download and install Epic Games Launcher for Mac.
3. Open Epic Games Launcher.
4. Sign in with the Epic/GitHub account you want to use.
5. Go to `Unreal Engine > Library`.
6. Click `+` next to Engine Versions.
7. Install Unreal Engine 5.x.
8. After installation, return to this repo and run:

```bash
cd /Users/seanybear/Downloads/LiminalDominion_Codex_Starter
python3 scripts/find_unreal_editor.py
python3 scripts/find_unreal_editor.py --open
```

## First Project Open

When `LiminalDominion.uproject` opens:

1. Let Unreal rebuild modules if prompted.
2. Let Unreal generate project files if prompted.
3. If compile fails, keep the error window open and copy the first compile error into Codex.
4. If compile succeeds, create the maps listed in `docs/technical/UNREAL_PROJECT_SETUP.md`.

## Notes

- Windows remains the primary playable/package target.
- macOS is being used here for development and editor setup.
- Unreal is large; leave plenty of disk space and expect a long download.
