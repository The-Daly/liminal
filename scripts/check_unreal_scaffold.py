#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "LiminalDominion.uproject",
    "Config/DefaultEngine.ini",
    "Config/DefaultGame.ini",
    "Config/DefaultInput.ini",
    "Source/LiminalDominion.Target.cs",
    "Source/LiminalDominionEditor.Target.cs",
    "Source/LiminalDominion/LiminalDominion.Build.cs",
    "Source/LiminalDominion/Public/LiminalDominion.h",
    "Source/LiminalDominion/Private/LiminalDominion.cpp",
    "Source/LiminalDominion/Public/LDDataTypes.h",
    "Source/LiminalDominion/Public/LDHUDTypes.h",
    "Source/LiminalDominion/Public/LDGameDataSubsystem.h",
    "Source/LiminalDominion/Private/LDGameDataSubsystem.cpp",
    "Source/LiminalDominion/Public/LDInteractable.h",
    "Source/LiminalDominion/Public/LDPlayerCharacter.h",
    "Source/LiminalDominion/Private/LDPlayerCharacter.cpp",
    "Source/LiminalDominion/Public/LDRunStateComponent.h",
    "Source/LiminalDominion/Private/LDRunStateComponent.cpp",
    "Source/LiminalDominion/Public/LDInventoryComponent.h",
    "Source/LiminalDominion/Private/LDInventoryComponent.cpp",
    "Source/LiminalDominion/Public/LDSanityComponent.h",
    "Source/LiminalDominion/Private/LDSanityComponent.cpp",
    "Source/LiminalDominion/Public/LDExtractionTrigger.h",
    "Source/LiminalDominion/Private/LDExtractionTrigger.cpp",
    "Source/LiminalDominion/Public/LDLootContainer.h",
    "Source/LiminalDominion/Private/LDLootContainer.cpp",
    "Source/LiminalDominion/Public/LDStorageActor.h",
    "Source/LiminalDominion/Private/LDStorageActor.cpp",
    "Source/LiminalDominion/Public/LDProjectBoardActor.h",
    "Source/LiminalDominion/Private/LDProjectBoardActor.cpp",
    "Source/LiminalDominion/Public/LDFlickerStalker.h",
    "Source/LiminalDominion/Private/LDFlickerStalker.cpp",
]


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        print("FAIL: Unreal scaffold is missing files:")
        for path in missing:
            print(f"- {path}")
        return 1

    with open(ROOT / "LiminalDominion.uproject", "r", encoding="utf-8") as f:
        project = json.load(f)

    modules = project.get("Modules", [])
    if not any(module.get("Name") == "LiminalDominion" for module in modules):
        print("FAIL: LiminalDominion module is not declared in LiminalDominion.uproject")
        return 1

    print(f"OK: Unreal scaffold contains {len(REQUIRED_FILES)} required files")
    print("OK: LiminalDominion runtime module is declared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
