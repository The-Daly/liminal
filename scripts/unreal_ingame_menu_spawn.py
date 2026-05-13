#!/usr/bin/env python3
from pathlib import Path

import unreal


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

MENU_PAWN_PATH = "/Game/Blueprints/BP_MainMenuPawn"
MENU_TEXTURE_PATH = "/Game/UI/T_MenuOperationsOverlay"
MENU_MATERIAL_PATH = "/Game/UI/M_MenuOperationsOverlay"
LEVEL_PATH = "/Game/Maps/LD_Level1_ServiceHalls_Greybox"
MENU_TEXTURE_SOURCE = REPO_ROOT / "generated" / "ui" / "menu_operations_overlay.png"


def log(message: str) -> None:
    unreal.log(f"[LD Ingame Menu] {message}")


def make_rotator(pitch: float, yaw: float, roll: float = 0.0) -> unreal.Rotator:
    rotator = unreal.Rotator()
    rotator.pitch = pitch
    rotator.yaw = yaw
    rotator.roll = roll
    return rotator


def import_menu_texture():
    if not MENU_TEXTURE_SOURCE.exists():
        raise RuntimeError(f"Menu texture source missing: {MENU_TEXTURE_SOURCE}")

    task = unreal.AssetImportTask()
    task.set_editor_property("filename", str(MENU_TEXTURE_SOURCE))
    task.set_editor_property("destination_path", "/Game/UI")
    task.set_editor_property("destination_name", "T_MenuOperationsOverlay")
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("automated", True)
    task.set_editor_property("save", True)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    texture = unreal.EditorAssetLibrary.load_asset(MENU_TEXTURE_PATH)
    if texture is None:
        raise RuntimeError(f"Failed to import menu texture to {MENU_TEXTURE_PATH}")

    texture.set_editor_property("srgb", True)
    texture.set_editor_property("lod_group", unreal.TextureGroup.TEXTUREGROUP_UI)
    unreal.EditorAssetLibrary.save_loaded_asset(texture, only_if_is_dirty=False)
    log(f"Imported {MENU_TEXTURE_PATH}")
    return texture


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
        unreal.MaterialExpressionTextureSample,
        -360,
        0,
    )
    sample.set_editor_property("texture", texture)

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

    unreal.MaterialEditingLibrary.connect_material_property(
        emissive_multiply,
        "",
        unreal.MaterialProperty.MP_EMISSIVE_COLOR,
    )
    unreal.MaterialEditingLibrary.connect_material_property(
        sample,
        "A",
        unreal.MaterialProperty.MP_OPACITY,
    )
    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_loaded_asset(material, only_if_is_dirty=False)
    log(f"Built {MENU_MATERIAL_PATH}")
    return material


def build_menu_pawn(material):
    if unreal.EditorAssetLibrary.does_asset_exist(MENU_PAWN_PATH):
        unreal.EditorAssetLibrary.delete_asset(MENU_PAWN_PATH)
        log(f"Deleted existing {MENU_PAWN_PATH}")

    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", unreal.Pawn)
    blueprint = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        "BP_MainMenuPawn",
        "/Game/Blueprints",
        unreal.Blueprint,
        factory,
    )
    if blueprint is None:
        raise RuntimeError("Failed to create BP_MainMenuPawn")

    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    handles = subsystem.k2_gather_subobject_data_for_blueprint(blueprint)
    root_handle = handles[1]

    camera_params = unreal.AddNewSubobjectParams()
    camera_params.set_editor_property("parent_handle", root_handle)
    camera_params.set_editor_property("new_class", unreal.CameraComponent)
    camera_params.set_editor_property("blueprint_context", blueprint)
    camera_params.set_editor_property("conform_transform_to_parent", True)
    camera_handle, _ = subsystem.add_new_subobject(params=camera_params)

    plane_params = unreal.AddNewSubobjectParams()
    plane_params.set_editor_property("parent_handle", camera_handle)
    plane_params.set_editor_property("new_class", unreal.StaticMeshComponent)
    plane_params.set_editor_property("blueprint_context", blueprint)
    plane_params.set_editor_property("conform_transform_to_parent", True)
    plane_handle, _ = subsystem.add_new_subobject(params=plane_params)

    camera_object = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(
        subsystem.k2_find_subobject_data_from_handle(camera_handle)
    )
    plane_object = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(
        subsystem.k2_find_subobject_data_from_handle(plane_handle)
    )

    camera_object.rename("MenuCamera")
    plane_object.rename("MenuPlane")

    camera_object.set_editor_property("relative_location", unreal.Vector(0.0, 0.0, 140.0))
    camera_object.set_editor_property("relative_rotation", make_rotator(0.0, 0.0, 0.0))
    camera_object.set_editor_property("field_of_view", 50.0)

    plane_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Plane")
    plane_object.set_editor_property("static_mesh", plane_mesh)
    plane_object.set_editor_property("relative_location", unreal.Vector(520.0, 0.0, 0.0))
    plane_object.set_editor_property("relative_rotation", make_rotator(90.0, 0.0, 0.0))
    plane_object.set_editor_property("relative_scale3d", unreal.Vector(2.55, 4.5, 1.0))
    plane_object.set_material(0, material)
    plane_object.set_editor_property("cast_shadow", False)
    plane_object.set_editor_property("visible", True)
    plane_object.set_editor_property("owner_no_see", False)
    plane_object.set_editor_property("only_owner_see", False)
    plane_object.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)

    unreal.BlueprintEditorLibrary.compile_blueprint(blueprint)
    unreal.EditorAssetLibrary.save_loaded_asset(blueprint, only_if_is_dirty=False)
    log(f"Built {MENU_PAWN_PATH}")


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


def place_menu_start() -> None:
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

    capture_camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CameraActor,
        unreal.Vector(-260.0, -40.0, 160.0),
        make_rotator(0.0, 0.0, 0.0),
    )
    capture_camera.set_actor_label("MenuCaptureCamera")

    unreal.EditorLevelLibrary.save_current_level()
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("Placed MenuBootPawn into Level 1 menu room")


def main():
    texture = import_menu_texture()
    material = build_menu_material(texture)
    build_menu_pawn(material)
    configure_game_mode()
    place_menu_start()


if __name__ == "__main__":
    main()
