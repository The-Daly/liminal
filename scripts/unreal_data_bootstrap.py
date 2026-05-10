#!/usr/bin/env python3
import os

import unreal

import ld_datatable_rows


PROJECT_DIR = unreal.Paths.project_dir()
CSV_DIR = os.path.join(PROJECT_DIR, "generated", "unreal_datatables")
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


def log(message: str) -> None:
    unreal.log(f"[LD Data Bootstrap] {message}")


def struct_object(struct_type):
    if hasattr(struct_type, "static_struct"):
        return struct_type.static_struct()
    return struct_type


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
    ensure_data_dir()
    imported_assets = []
    for asset_name, csv_name in DATA_IMPORTS.items():
        create_or_fill_data_table(asset_name, csv_name)
        imported_assets.append(asset_name)

    verify_assets(imported_assets)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("Data bootstrap complete")


if __name__ == "__main__":
    main()
