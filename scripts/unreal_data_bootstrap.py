#!/usr/bin/env python3
import os
import json

import unreal


PROJECT_DIR = unreal.Paths.project_dir()
CSV_DIR = os.path.join(PROJECT_DIR, "generated", "unreal_datatables")
STATUS_PATH = os.path.join(PROJECT_DIR, "outputs", "unreal_data_bootstrap_status.json")
DATA_IMPORTS = {
    "DT_Items": "DT_Items.csv",
    "DT_Factions": "DT_Factions.csv",
    "DT_LootTables": "DT_LootTables.csv",
    "DT_Extractions": "DT_Extractions.csv",
    "DT_Storage": "DT_Storage.csv",
    "DT_Sanity": "DT_Sanity.csv",
    "DT_HubUpgrades": "DT_HubUpgrades.csv",
    "DT_PlayerState": "DT_PlayerState.csv",
    "DT_RunState": "DT_RunState.csv",
}

NATIVE_ROW_STRUCTS = {
    "DT_Items": "/Script/LiminalDominion.LDItemRow",
    "DT_Factions": "/Script/LiminalDominion.LDFactionRow",
    "DT_LootTables": "/Script/LiminalDominion.LDLootTableRow",
    "DT_Extractions": "/Script/LiminalDominion.LDExtractionRow",
    "DT_Storage": "/Script/LiminalDominion.LDStorageRow",
    "DT_Sanity": "/Script/LiminalDominion.LDSanityRow",
    "DT_HubUpgrades": "/Script/LiminalDominion.LDHubUpgradeRow",
    "DT_PlayerState": "/Script/LiminalDominion.LDPlayerStateRow",
    "DT_RunState": "/Script/LiminalDominion.LDRunStateRow",
}

EDITOR_ROW_STRUCTS = {
    "DT_Items": "/Game/Data/Structs/ST_ItemRow.ST_ItemRow",
    "DT_Factions": "/Game/Data/Structs/ST_FactionRow.ST_FactionRow",
    "DT_LootTables": "/Game/Data/Structs/ST_LootTableRow.ST_LootTableRow",
    "DT_Extractions": "/Game/Data/Structs/ST_ExtractionRow.ST_ExtractionRow",
    "DT_Storage": "/Game/Data/Structs/ST_StorageRow.ST_StorageRow",
    "DT_Sanity": "/Game/Data/Structs/ST_SanityRow.ST_SanityRow",
    "DT_HubUpgrades": "/Game/Data/Structs/ST_HubUpgradeRow.ST_HubUpgradeRow",
    "DT_PlayerState": "/Game/Data/Structs/ST_PlayerStateRow.ST_PlayerStateRow",
    "DT_RunState": "/Game/Data/Structs/ST_RunStateRow.ST_RunStateRow",
}


def log(message: str) -> None:
    unreal.log(f"[LD Data Bootstrap] {message}")


def write_status(success: bool, message: str, imported_assets: list[str] | None = None) -> None:
    os.makedirs(os.path.dirname(STATUS_PATH), exist_ok=True)
    with open(STATUS_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {
                "success": success,
                "message": message,
                "imported_assets": imported_assets or [],
            },
            f,
            indent=2,
        )


def load_native_row_struct(asset_name: str):
    struct_path = NATIVE_ROW_STRUCTS[asset_name]
    row_struct = unreal.load_object(None, struct_path)
    return row_struct


def load_editor_row_struct(asset_name: str):
    struct_path = EDITOR_ROW_STRUCTS[asset_name]
    return unreal.load_object(None, struct_path)


def resolve_row_struct(asset_name: str):
    native_struct = load_native_row_struct(asset_name)
    if native_struct is not None:
        log(f"Using native row struct for {asset_name}: {NATIVE_ROW_STRUCTS[asset_name]}")
        return native_struct

    editor_struct = load_editor_row_struct(asset_name)
    if editor_struct is not None:
        log(f"Using editor-authored row struct for {asset_name}: {EDITOR_ROW_STRUCTS[asset_name]}")
        return editor_struct

    raise RuntimeError(
        f"No usable row struct found for {asset_name}. "
        f"Expected either native struct {NATIVE_ROW_STRUCTS[asset_name]} or editor struct asset {EDITOR_ROW_STRUCTS[asset_name]}."
    )


def ensure_data_dir() -> None:
    if not unreal.EditorAssetLibrary.does_directory_exist("/Game/Data"):
        unreal.EditorAssetLibrary.make_directory("/Game/Data")
        log("Created /Game/Data")


def save_asset(asset) -> None:
    unreal.EditorAssetLibrary.save_loaded_asset(asset, only_if_is_dirty=False)


def create_or_fill_data_table(asset_name: str, csv_name: str):
    asset_path = f"/Game/Data/{asset_name}"
    csv_path = os.path.join(CSV_DIR, csv_name)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found for import: {csv_path}")

    row_struct = resolve_row_struct(asset_name)
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
        log(f"Created asset shell {asset_path}")

    problems = asset.fill_from_csv_file(csv_path)
    save_asset(asset)
    if problems:
        raise RuntimeError(f"Import reported problems for {asset_name}: {problems}")

    row_names = [str(name) for name in unreal.DataTableFunctionLibrary.get_data_table_row_names(asset)]
    log(f"Imported {csv_name} into {asset_path} with rows: {', '.join(row_names)}")
    return asset


def verify_assets(asset_names: list[str]) -> None:
    for asset_name in asset_names:
        asset_path = f"/Game/Data/{asset_name}"
        asset = unreal.EditorAssetLibrary.load_asset(asset_path)
        if asset is None:
            raise RuntimeError(f"Failed to reload imported asset {asset_path}")
        row_names = unreal.DataTableFunctionLibrary.get_data_table_row_names(asset)
        if not row_names:
            raise RuntimeError(f"Imported data table is empty: {asset_path}")
        log(f"Verified reload for {asset_path} ({len(row_names)} rows)")


def main() -> None:
    imported_assets: list[str] = []
    try:
        ensure_data_dir()
        for asset_name, csv_name in DATA_IMPORTS.items():
            create_or_fill_data_table(asset_name, csv_name)
            imported_assets.append(asset_name)

        verify_assets(imported_assets)
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
        message = "Data bootstrap complete"
        write_status(True, message, imported_assets)
        log(message)
    except Exception as exc:
        message = f"Data bootstrap failed: {exc}"
        write_status(False, message, imported_assets)
        unreal.log_error(f"[LD Data Bootstrap] {message}")
        raise


if __name__ == "__main__":
    main()
