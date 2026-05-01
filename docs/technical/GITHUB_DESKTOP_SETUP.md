# GitHub Desktop Setup

Use this path when you want to connect/push the project through the internet with a normal app login instead of typing Git credentials in Terminal.

## Current Remote

The local repo is already pointed at:

```text
https://github.com/The-Daly/liminal.git
```

## One-Time Setup

1. Install GitHub Desktop:
   - https://desktop.github.com/
2. Open GitHub Desktop.
3. Sign in with the GitHub account that has access to `The-Daly/liminal`.
4. Choose `File > Add Local Repository...`.
5. Select:

```text
/Users/seanybear/Downloads/LiminalDominion_Codex_Starter
```

6. GitHub Desktop should show the repository on branch `main`.
7. Click `Push origin`.

## Daily Workflow

1. Open GitHub Desktop.
2. Select `LiminalDominion_Codex_Starter`.
3. Review changed files.
4. Enter a short summary.
5. Click `Commit to main`.
6. Click `Push origin`.

## If GitHub Desktop Says It Cannot Access The Repo

- Make sure the repo exists at `https://github.com/The-Daly/liminal`.
- Make sure your GitHub account has access to that private repo.
- In GitHub Desktop, use `GitHub Desktop > Settings > Accounts` and sign out/sign in again.

## Terminal Is Optional

The Terminal commands still work, but GitHub Desktop is the preferred route for authentication and pushing if you want to avoid command-line credential prompts.
