#!/usr/bin/env python3
import os

import unreal

import ld_datatable_rows


PROJECT_DIR = unreal.Paths.project_dir()
CSV_DIR = os.path.join(PROJECT_DIR, "generated", "unreal_datatables")
DO_DATA_IMPORT = os.environ.get("LD_ENABLE_DATA_IMPORT") == "1"

DATA_IMPORTS = {
    "DT_Items": "DT_Items.csv",
    "DT_LootTables": "DT_LootTables.csv",
    "DT_Extractions": "DT_Extractions.csv",
    "DT_Storage": "DT_Storage.csv",
    "DT_Sanity": "DT_Sanity.csv",
    "DT_HubUpgrades": "DT_HubUpgrades.csv",
    "DT_PlayerState": "DT_PlayerState.csv",
    "DT_RunState": "DT_RunState.csv",
}

BLUEPRINTS = [
    ("BP_LDPlayer", unreal.Character),
    ("BP_LDGameMode", unreal.GameModeBase),
    ("BP_MenuFlowController", unreal.Actor),
    ("BP_CharacterPreviewAnchor", unreal.Actor),
    ("BP_FactionNpcPreviewAnchor", unreal.Actor),
    ("BP_DeploymentGate", unreal.Actor),
    ("BP_LootContainer", unreal.Actor),
    ("BP_ExtractionTrigger_Stable", unreal.Actor),
    ("BP_ExtractionTrigger_HiddenTicketBooth", unreal.Actor),
    ("BP_PersonalStorage", unreal.Actor),
    ("BP_FactionVaultPlaceholder", unreal.Actor),
    ("BP_ProjectBoard", unreal.Actor),
    ("BP_QuartermasterPlaceholder", unreal.Actor),
    ("BP_TraderPlaceholder", unreal.Actor),
    ("BP_FactionSelectorPlaceholder", unreal.Actor),
    ("BP_RelicDisplayPlaceholder", unreal.Actor),
    ("BP_FlickerStalker", unreal.Character),
]

WIDGETS = [
    "WBP_TitleShell",
    "WBP_ServerBrowser",
    "WBP_FactionSelection",
    "WBP_CharacterSetup",
    "WBP_MainPlayerMenu",
    "WBP_PlayerHUD",
    "WBP_RunResult",
]

MAP_PLACEMENTS = {
    "/Game/Maps/LD_Hub_Greybox": [
        ("BP_DeploymentGate", unreal.Vector(0.0, 0.0, 120.0)),
        ("BP_ProjectBoard", unreal.Vector(300.0, 0.0, 120.0)),
        ("BP_FactionVaultPlaceholder", unreal.Vector(-300.0, 0.0, 120.0)),
        ("BP_QuartermasterPlaceholder", unreal.Vector(-150.0, -250.0, 120.0)),
        ("BP_TraderPlaceholder", unreal.Vector(150.0, -250.0, 120.0)),
        ("BP_FactionSelectorPlaceholder", unreal.Vector(0.0, -150.0, 120.0)),
    ],
    "/Game/Maps/LD_PersonalRoom_Greybox": [
        ("BP_PersonalStorage", unreal.Vector(0.0, 0.0, 120.0)),
        ("BP_RelicDisplayPlaceholder", unreal.Vector(-250.0, 0.0, 120.0)),
    ],
    "/Game/Maps/LD_Level1_ServiceHalls_Greybox": [
        ("BP_LootContainer", unreal.Vector(0.0, 0.0, 120.0)),
        ("BP_ExtractionTrigger_Stable", unreal.Vector(500.0, 0.0, 120.0)),
        ("BP_ExtractionTrigger_HiddenTicketBooth", unreal.Vector(900.0, 0.0, 120.0)),
        ("BP_FlickerStalker", unreal.Vector(-500.0, 0.0, 120.0)),
    ],
}


def log(message: str) -> None:
    unreal.log(f"[LD First Pass] {message}")


def struct_object(struct_type):
    if hasattr(struct_type, "static_struct"):
        return struct_type.static_struct()
    return struct_type


def ensure_dirs() -> None:
    for path in ("/Game/Data", "/Game/Blueprints", "/Game/UI"):
        if not unreal.EditorAssetLibrary.does_directory_exist(path):
            unreal.EditorAssetLibrary.make_directory(path)
            log(f"Created directory {path}")


def save_asset(asset) -> None:
    unreal.EditorAssetLibrary.save_loaded_asset(asset, only_if_is_dirty=False)


def compile_blueprint_if_possible(asset) -> None:
    if hasattr(unreal, "BlueprintEditorLibrary"):
        unreal.BlueprintEditorLibrary.compile_blueprint(asset)


def create_blueprint_asset(asset_name: str, parent_class) -> object:
    asset_path = f"/Game/Blueprints/{asset_name}"
    existing = unreal.EditorAssetLibrary.load_asset(asset_path)
    if existing:
        log(f"Blueprint already exists: {asset_path}")
        return existing

    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name,
        "/Game/Blueprints",
        unreal.Blueprint,
        factory,
    )
    compile_blueprint_if_possible(asset)
    save_asset(asset)
    log(f"Created blueprint {asset_path}")
    return asset


def create_widget_asset(asset_name: str) -> object:
    asset_path = f"/Game/UI/{asset_name}"
    existing = unreal.EditorAssetLibrary.load_asset(asset_path)
    if existing:
        log(f"Widget already exists: {asset_path}")
        return existing

    factory = unreal.WidgetBlueprintFactory()
    factory.set_editor_property("parent_class", unreal.UserWidget)
    asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name,
        "/Game/UI",
        unreal.WidgetBlueprint,
        factory,
    )
    save_asset(asset)
    log(f"Created widget {asset_path}")
    return asset


def create_or_fill_data_table(asset_name: str, csv_name: str) -> object:
    asset_path = f"/Game/Data/{asset_name}"
    row_struct = struct_object(ld_datatable_rows.ROW_STRUCTS[asset_name])
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if asset is None:
        factory = unreal.DataTableFactory()
        factory.set_editor_property("struct", row_struct)
        asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            asset_name,
            "/Game/Data",
            unreal.DataTable,
            factory,
        )
        log(f"Created data table asset shell: {asset_path}")

    csv_path = os.path.join(CSV_DIR, csv_name)
    success = asset.fill_from_csv_file(csv_path)
    save_asset(asset)
    if not success:
        raise RuntimeError(f"Failed to import {csv_name} into {asset_path}")
    log(f"Imported {csv_name} into {asset_path}")
    return asset


def remove_existing_actors(labels: set[str]) -> None:
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        label = actor.get_actor_label()
        if label in labels:
            unreal.EditorLevelLibrary.destroy_actor(actor)
            log(f"Removed existing actor {label}")


def place_blueprints_in_map(map_path: str, placements: list[tuple[str, unreal.Vector]]) -> None:
    unreal.EditorLevelLibrary.load_level(map_path)
    labels = {label for label, _ in placements}
    remove_existing_actors(labels)

    for asset_name, location in placements:
        blueprint = unreal.EditorAssetLibrary.load_asset(f"/Game/Blueprints/{asset_name}")
        actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
            blueprint,
            location,
            unreal.Rotator(0.0, 0.0, 0.0),
        )
        actor.set_actor_label(asset_name)
        log(f"Placed {asset_name} in {map_path}")

    unreal.EditorLevelLibrary.save_current_level()
    log(f"Saved map {map_path}")


def main() -> None:
    ensure_dirs()

    for asset_name, parent_class in BLUEPRINTS:
        create_blueprint_asset(asset_name, parent_class)

    for asset_name in WIDGETS:
        create_widget_asset(asset_name)

    if DO_DATA_IMPORT:
        for asset_name, csv_name in DATA_IMPORTS.items():
            create_or_fill_data_table(asset_name, csv_name)
    else:
        log("Skipping DataTable import by default; run scripts/run_unreal_data_bootstrap.ps1 when you want the full Unreal data pass")

    for map_path, placements in MAP_PLACEMENTS.items():
        place_blueprints_in_map(map_path, placements)

    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("First pass setup complete")


if __name__ == "__main__":
    main()
