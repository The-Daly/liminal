#!/usr/bin/env python3
import argparse
import platform
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "LiminalDominion.uproject"

MAC_SEARCH_ROOTS = [
    Path("/Applications"),
    Path.home() / "Applications",
    Path("/Users/Shared/Epic Games"),
]

WINDOWS_SEARCH_ROOTS = [
    Path("C:/Program Files/Epic Games"),
    Path("C:/Program Files/Unreal Engine"),
]


def find_mac_editors() -> list[Path]:
    found: list[Path] = []
    for root in MAC_SEARCH_ROOTS:
        if not root.exists():
            continue
        found.extend(root.glob("**/UnrealEditor.app"))
    return sorted(set(found), reverse=True)


def find_windows_editors() -> list[Path]:
    found: list[Path] = []
    for root in WINDOWS_SEARCH_ROOTS:
        if not root.exists():
            continue
        found.extend(root.glob("**/UnrealEditor.exe"))
    return sorted(set(found), reverse=True)


def find_editors() -> list[Path]:
    system = platform.system()
    if system == "Darwin":
        return find_mac_editors()
    if system == "Windows":
        return find_windows_editors()
    return []


def open_project(editor: Path) -> int:
    if platform.system() == "Darwin" and editor.suffix == ".app":
        return subprocess.call(["open", "-a", str(editor), str(PROJECT)])
    return subprocess.call([str(editor), str(PROJECT)])


def main() -> int:
    parser = argparse.ArgumentParser(description="Find Unreal Editor and optionally open Liminal Dominion.")
    parser.add_argument("--open", action="store_true", help="Open LiminalDominion.uproject with the first detected editor.")
    args = parser.parse_args()

    editors = find_editors()
    if not editors:
        print("No Unreal Editor installation found.")
        print("Install Unreal Engine through Epic Games Launcher, then run this script again.")
        return 1

    print("Detected Unreal Editor installations:")
    for editor in editors:
        print(f"- {editor}")

    if args.open:
        if not PROJECT.exists():
            print(f"Project file is missing: {PROJECT}")
            return 1
        return open_project(editors[0])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
