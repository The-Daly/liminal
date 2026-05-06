#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "LiminalDominion.uproject",
    "Config/DefaultEngine.ini",
    "Config/DefaultGame.ini",
    "Config/DefaultInput.ini",
]

REQUIRED_SOURCE_FILES = [
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
    "Source/LiminalDominion/Public/LDSaveGame.h",
    "Source/LiminalDominion/Private/LDSaveGame.cpp",
    "Source/LiminalDominion/Public/LDSaveGameSubsystem.h",
    "Source/LiminalDominion/Private/LDSaveGameSubsystem.cpp",
    "Source/LiminalDominion/Public/LDInventoryComponent.h",
    "Source/LiminalDominion/Private/LDInventoryComponent.cpp",
    "Source/LiminalDominion/Public/LDSanityComponent.h",
    "Source/LiminalDominion/Private/LDSanityComponent.cpp",
    "Source/LiminalDominion/Public/LDExtractionTrigger.h",
    "Source/LiminalDominion/Private/LDExtractionTrigger.cpp",
    "Source/LiminalDominion/Public/LDDeploymentGate.h",
    "Source/LiminalDominion/Private/LDDeploymentGate.cpp",
    "Source/LiminalDominion/Public/LDLootContainer.h",
    "Source/LiminalDominion/Private/LDLootContainer.cpp",
    "Source/LiminalDominion/Public/LDStorageActor.h",
    "Source/LiminalDominion/Private/LDStorageActor.cpp",
    "Source/LiminalDominion/Public/LDProjectBoardActor.h",
    "Source/LiminalDominion/Private/LDProjectBoardActor.cpp",
    "Source/LiminalDominion/Public/LDFlickerStalker.h",
    "Source/LiminalDominion/Private/LDFlickerStalker.cpp",
]

LEGACY_SOURCE_FILES = [
    "Source_Legacy/LiminalDominion.Target.cs.disabled",
    "Source_Legacy/LiminalDominionEditor.Target.cs.disabled",
    "Source_Legacy/LiminalDominion/LiminalDominion.Build.cs.disabled",
    "Source_Legacy/LiminalDominion/Public/LiminalDominion.h",
    "Source_Legacy/LiminalDominion/Private/LiminalDominion.cpp",
    "Source_Legacy/LiminalDominion/Public/LDDataTypes.h",
    "Source_Legacy/LiminalDominion/Public/LDHUDTypes.h",
    "Source_Legacy/LiminalDominion/Public/LDGameDataSubsystem.h",
    "Source_Legacy/LiminalDominion/Private/LDGameDataSubsystem.cpp",
    "Source_Legacy/LiminalDominion/Public/LDInteractable.h",
    "Source_Legacy/LiminalDominion/Public/LDPlayerCharacter.h",
    "Source_Legacy/LiminalDominion/Private/LDPlayerCharacter.cpp",
    "Source_Legacy/LiminalDominion/Public/LDRunStateComponent.h",
    "Source_Legacy/LiminalDominion/Private/LDRunStateComponent.cpp",
    "Source_Legacy/LiminalDominion/Public/LDInventoryComponent.h",
    "Source_Legacy/LiminalDominion/Private/LDInventoryComponent.cpp",
    "Source_Legacy/LiminalDominion/Public/LDSanityComponent.h",
    "Source_Legacy/LiminalDominion/Private/LDSanityComponent.cpp",
    "Source_Legacy/LiminalDominion/Public/LDExtractionTrigger.h",
    "Source_Legacy/LiminalDominion/Private/LDExtractionTrigger.cpp",
    "Source_Legacy/LiminalDominion/Public/LDLootContainer.h",
    "Source_Legacy/LiminalDominion/Private/LDLootContainer.cpp",
    "Source_Legacy/LiminalDominion/Public/LDStorageActor.h",
    "Source_Legacy/LiminalDominion/Private/LDStorageActor.cpp",
    "Source_Legacy/LiminalDominion/Public/LDProjectBoardActor.h",
    "Source_Legacy/LiminalDominion/Private/LDProjectBoardActor.cpp",
    "Source_Legacy/LiminalDominion/Public/LDFlickerStalker.h",
    "Source_Legacy/LiminalDominion/Private/LDFlickerStalker.cpp",
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
    has_runtime_module = any(module.get("Name") == "LiminalDominion" for module in modules)
    source_missing = [path for path in REQUIRED_SOURCE_FILES if not (ROOT / path).exists()]

    if has_runtime_module:
        if source_missing:
            print("FAIL: LiminalDominion module is declared, but source files are missing:")
            for path in source_missing:
                print(f"- {path}")
            return 1
        print(f"OK: Unreal scaffold contains {len(REQUIRED_FILES) + len(REQUIRED_SOURCE_FILES)} required files")
        print("OK: LiminalDominion runtime module is declared")
        return 0

    legacy_missing = [path for path in LEGACY_SOURCE_FILES if not (ROOT / path).exists()]
    if legacy_missing:
        print("FAIL: project has no active code module and disabled source scaffold is incomplete:")
        for path in legacy_missing:
            print(f"- {path}")
        return 1

    print(f"OK: module-free Unreal visualization scaffold contains {len(REQUIRED_FILES)} required files")
    print("OK: disabled C++ scaffold is preserved under Source_Legacy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
