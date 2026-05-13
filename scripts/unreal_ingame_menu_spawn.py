#!/usr/bin/env python3
from pathlib import Path

import unreal


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

MENU_PAWN_PATH = "/Game/Blueprints/BP_MainMenuPawn"
MENU_MATERIAL_PATH = "/Game/UI/M_MenuOperationsOverlay"
LEVEL_PATH = "/Game/Maps/LD_Level1_ServiceHalls_Greybox"
MENU_TEXTURE_DIR = REPO_ROOT / "generated" / "ui"
MENU_TEXTURES = {
    "deploy": ("T_MenuDeployOverlay", MENU_TEXTURE_DIR / "menu_deploy_overlay.png"),
    "loadout": ("T_MenuLoadoutOverlay", MENU_TEXTURE_DIR / "menu_loadout_overlay.png"),
    "operators": ("T_MenuOperatorsOverlay", MENU_TEXTURE_DIR / "menu_operators_overlay.png"),
    "market": ("T_MenuMarketOverlay", MENU_TEXTURE_DIR / "menu_market_overlay.png"),
    "intel": ("T_MenuIntelOverlay", MENU_TEXTURE_DIR / "menu_intel_overlay.png"),
    "settings": ("T_MenuSettingsOverlay", MENU_TEXTURE_DIR / "menu_settings_overlay.png"),
    "exit": ("T_MenuExitOverlay", MENU_TEXTURE_DIR / "menu_exit_overlay.png"),
}


def log(message: str) -> None:
    unreal.log(f"[LD Ingame Menu] {message}")


def make_rotator(pitch: float, yaw: float, roll: float = 0.0) -> unreal.Rotator:
    rotator = unreal.Rotator()
    rotator.pitch = pitch
    rotator.yaw = yaw
    rotator.roll = roll
    return rotator


def import_menu_textures():
    imported = {}
    for state, (asset_name, source_path) in MENU_TEXTURES.items():
        if not source_path.exists():
            raise RuntimeError(f"Menu texture source missing: {source_path}")

        task = unreal.AssetImportTask()
        task.set_editor_property("filename", str(source_path))
        task.set_editor_property("destination_path", "/Game/UI")
        task.set_editor_property("destination_name", asset_name)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("automated", True)
        task.set_editor_property("save", True)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

        texture_path = f"/Game/UI/{asset_name}"
        texture = unreal.EditorAssetLibrary.load_asset(texture_path)
        if texture is None:
            raise RuntimeError(f"Failed to import menu texture to {texture_path}")
        texture.set_editor_property("srgb", True)
        texture.set_editor_property("lod_group", unreal.TextureGroup.TEXTUREGROUP_UI)
        unreal.EditorAssetLibrary.save_loaded_asset(texture, only_if_is_dirty=False)
        imported[state] = texture
        log(f"Imported {texture_path}")
    return imported


def build_menu_material(texture):
    if unreal.EditorAssetLibrary.does_asset_exist(MENU_MATERIAL_PATH):
        unreal.EditorAssetLibrary.delete_asset(MENU_MATERIAL_PATH)
        log(f"Deleted existing {MENU_MATERIAL_PATH}")

    factory = unreal.MaterialFactoryNew()
    material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        "M_MenuOperationsOverlay",
        "/Game/UI",
        unreal.Material,
        factory,
    )
    if material is None:
        raise RuntimeError("Failed to create M_MenuOperationsOverlay")

    material.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
    material.set_editor_property("two_sided", True)
    material.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)

    sample = unreal.MaterialEditingLibrary.create_material_expression(
        material,
        unreal.MaterialExpressionTextureSampleParameter2D,
        -360,
        0,
    )
    sample.set_editor_property("texture", texture)
    sample.set_editor_property("parameter_name", "MenuTexture")

    intensity = unreal.MaterialEditingLibrary.create_material_expression(
        material,
        unreal.MaterialExpressionConstant,
        -360,
        180,
    )
    intensity.set_editor_property("r", 4.0)

    emissive_multiply = unreal.MaterialEditingLibrary.create_material_expression(
        material,
        unreal.MaterialExpressionMultiply,
        -120,
        40,
    )
    unreal.MaterialEditingLibrary.connect_material_expressions(sample, "RGB", emissive_multiply, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(intensity, "", emissive_multiply, "B")
    unreal.MaterialEditingLibrary.connect_material_property(emissive_multiply, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    unreal.MaterialEditingLibrary.connect_material_property(sample, "A", unreal.MaterialProperty.MP_OPACITY)
    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_loaded_asset(material, only_if_is_dirty=False)
    log(f"Built {MENU_MATERIAL_PATH}")
    return material


def configure_existing_menu_pawn(material):
    blueprint = unreal.EditorAssetLibrary.load_asset(MENU_PAWN_PATH)
    if blueprint is None:
        raise RuntimeError(f"Missing existing menu pawn asset at {MENU_PAWN_PATH}")

    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    handles = subsystem.k2_gather_subobject_data_for_blueprint(blueprint)
    for handle in handles:
        data = subsystem.k2_find_subobject_data_from_handle(handle)
        obj = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data)
        if obj and obj.get_name() == "MenuWidget":
            obj.set_editor_property("visible", False)
        if obj and obj.get_name() == "MenuPlane":
            obj.set_material(0, material)
            obj.set_editor_property("visible", True)
            obj.set_editor_property("hidden_in_game", False)
            obj.set_collision_enabled(unreal.CollisionEnabled.QUERY_ONLY)
            obj.set_collision_response_to_all_channels(unreal.CollisionResponse.IGNORE)
            obj.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY, unreal.CollisionResponse.BLOCK)

    unreal.BlueprintEditorLibrary.compile_blueprint(blueprint)
    unreal.EditorAssetLibrary.save_loaded_asset(blueprint, only_if_is_dirty=False)
    log("Updated existing BP_MainMenuPawn with runtime menu material")


def configure_game_mode() -> None:
    game_mode = unreal.EditorAssetLibrary.load_asset("/Game/Blueprints/BP_LDGameMode")
    if game_mode is None:
        raise RuntimeError("Missing /Game/Blueprints/BP_LDGameMode")

    generated_class = unreal.BlueprintEditorLibrary.generated_class(game_mode)
    default_object = unreal.get_default_object(generated_class)
    default_object.set_editor_property("default_pawn_class", unreal.SpectatorPawn)
    default_object.set_editor_property("start_players_as_spectators", True)

    unreal.BlueprintEditorLibrary.compile_blueprint(game_mode)
    unreal.EditorAssetLibrary.save_loaded_asset(game_mode, only_if_is_dirty=False)
    log("Configured BP_LDGameMode for placed menu pawn boot")


def place_menu_scene() -> None:
    unreal.EditorLevelLibrary.load_level(LEVEL_PATH)
    menu_pawn_class = unreal.EditorAssetLibrary.load_blueprint_class(MENU_PAWN_PATH)
    if menu_pawn_class is None:
        raise RuntimeError(f"Missing generated class for {MENU_PAWN_PATH}")

    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor.get_actor_label() in {"MenuPlayerStart", "MenuBootPawn", "MenuCaptureCamera"}:
            unreal.EditorLevelLibrary.destroy_actor(actor)

    player_start = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PlayerStart,
        unreal.Vector(-260.0, -40.0, 20.0),
        make_rotator(0.0, 0.0, 0.0),
    )
    player_start.set_actor_label("MenuPlayerStart")

    menu_pawn = unreal.EditorLevelLibrary.spawn_actor_from_class(
        menu_pawn_class,
        unreal.Vector(-260.0, -40.0, 20.0),
        make_rotator(0.0, 0.0, 0.0),
    )
    menu_pawn.set_actor_label("MenuBootPawn")
    menu_pawn.set_editor_property("auto_possess_player", unreal.AutoReceiveInput.PLAYER0)
    menu_pawn.set_editor_property("is_spatially_loaded", False)

    capture_camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CameraActor,
        unreal.Vector(-260.0, -40.0, 160.0),
        make_rotator(0.0, 0.0, 0.0),
    )
    capture_camera.set_actor_label("MenuCaptureCamera")
    capture_camera.set_editor_property("is_spatially_loaded", False)
    capture_camera.set_editor_property("auto_activate_for_player", unreal.AutoReceiveInput.PLAYER0)

    unreal.EditorLevelLibrary.save_current_level()
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("Placed MenuBootPawn into Level 1 menu room")


def main():
    textures = import_menu_textures()
    material = build_menu_material(textures["deploy"])
    configure_existing_menu_pawn(material)
    configure_game_mode()
    place_menu_scene()


if __name__ == "__main__":
    main()
