#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    ("Seed data validation", [sys.executable, "scripts/validate_seed_data.py"]),
    ("Unit tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
    ("Unreal DataTable export", [sys.executable, "scripts/export_unreal_datatables.py"]),
    ("Unreal scaffold check", [sys.executable, "scripts/check_unreal_scaffold.py"]),
    ("Python compile", [sys.executable, "-m", "compileall", "scripts", "tests"]),
]

FORBIDDEN_TRACKED_DIRS = [
    "Binaries/",
    "Build/",
    "DerivedDataCache/",
    "Intermediate/",
    "Saved/",
]


def run(label: str, command: list[str]) -> bool:
    print(f"\n== {label} ==")
    result = subprocess.run(command, cwd=ROOT, text=True)
    if result.returncode == 0:
        print(f"OK: {label}")
        return True
    print(f"FAIL: {label}")
    return False


def check_forbidden_tracked_dirs() -> bool:
    print("\n== Tracked Unreal generated folders ==")
    result = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True, stdout=subprocess.PIPE, text=True)
    offenders = [
        path for path in result.stdout.splitlines()
        if any(path.startswith(prefix) for prefix in FORBIDDEN_TRACKED_DIRS)
    ]
    if offenders:
        print("FAIL: generated Unreal files are tracked:")
        for path in offenders:
            print(f"- {path}")
        return False
    print("OK: no generated Unreal folders are tracked")
    return True


def main() -> int:
    results = [run(label, command) for label, command in CHECKS]
    results.append(check_forbidden_tracked_dirs())
    if all(results):
        print("\nSUCCESS: preflight passed")
        return 0
    print("\nFAIL: preflight failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
