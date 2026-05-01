#!/usr/bin/env python3
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def run_check(label: str, command: list[str]) -> bool:
    try:
        subprocess.run(command, cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"OK: {label}")
        return True
    except subprocess.CalledProcessError as exc:
        print(f"FAIL: {label}")
        if exc.stdout:
            print(exc.stdout.strip())
        if exc.stderr:
            print(exc.stderr.strip())
        return False


def main() -> int:
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Project: {ROOT}")

    checks = []
    checks.append(("Python 3.9+", sys.version_info >= (3, 9)))
    checks.append(("Git available", command_exists("git")))

    for label, passed in checks:
        print(f"{'OK' if passed else 'FAIL'}: {label}")

    command_checks = [
        ("Seed data validation", [sys.executable, "scripts/validate_seed_data.py"]),
        ("Unit tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
        ("Unreal DataTable export", [sys.executable, "scripts/export_unreal_datatables.py"]),
        ("Unreal scaffold check", [sys.executable, "scripts/check_unreal_scaffold.py"]),
    ]

    command_results = [run_check(label, command) for label, command in command_checks]
    all_passed = all(passed for _, passed in checks) and all(command_results)

    if platform.system() == "Darwin":
        print("Note: macOS is supported for development; Windows remains the primary playable build target.")
        print("Run 'python3 scripts/find_unreal_editor.py' after installing Unreal Engine.")
    elif platform.system() == "Windows":
        print("Note: this is the primary playable build target.")
    else:
        print("Note: Linux is not a target platform for V0.1.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
