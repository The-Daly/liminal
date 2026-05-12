#!/usr/bin/env python3
import unreal


BLUEPRINT_PATH = "/Game/Blueprints/BP_MainMenuPawn"
WIDGET_PATH = "/Game/UI/WBP_MainPlayerMenu"
LEVEL_PATH = "/Game/Maps/LD_Level1_ServiceHalls_Greybox"


def log(message: str) -> None:
    unreal.log(f"[LD Ingame Menu] {message}")


def build_blueprint():
    if unreal.EditorAssetLibrary.does_asset_exist(BLUEPRINT_PATH):
        unreal.EditorAssetLibrary.delete_asset(BLUEPRINT_PATH)
        log(f"Deleted existing {BLUEPRINT_PATH}")

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

    widget_params = unreal.AddNewSubobjectParams()
    widget_params.set_editor_property("parent_handle", root_handle)
    widget_params.set_editor_property("new_class", unreal.WidgetComponent)
    widget_params.set_editor_property("blueprint_context", blueprint)
    widget_params.set_editor_property("conform_transform_to_parent", True)
    widget_handle, _ = subsystem.add_new_subobject(params=widget_params)

    camera_object = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(
        subsystem.k2_find_subobject_data_from_handle(camera_handle)
    )
    widget_object = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(
        subsystem.k2_find_subobject_data_from_handle(widget_handle)
    )

    camera_object.rename("MenuCamera")
    widget_object.rename("MenuWidget")

    camera_object.set_editor_property("relative_location", unreal.Vector(0.0, 0.0, 140.0))
    camera_object.set_editor_property("relative_rotation", unreal.Rotator(0.0, 0.0, 0.0))
    camera_object.set_editor_property("field_of_view", 44.0)

    widget_class = unreal.EditorAssetLibrary.load_blueprint_class(WIDGET_PATH)
    widget_object.set_editor_property("widget_class", widget_class)
    widget_object.set_widget_space(unreal.WidgetSpace.WORLD)
    widget_object.set_editor_property("draw_size", unreal.IntPoint(1920, 1080))
    widget_object.set_editor_property("pivot", unreal.Vector2D(0.5, 0.5))
    widget_object.set_editor_property("relative_location", unreal.Vector(620.0, 0.0, 140.0))
    widget_object.set_editor_property("relative_rotation", unreal.Rotator(0.0, 180.0, 0.0))
    widget_object.set_editor_property("relative_scale3d", unreal.Vector(0.22, 0.22, 0.22))
    widget_object.set_editor_property("blend_mode", unreal.WidgetBlendMode.TRANSPARENT)
    widget_object.set_editor_property("receive_hardware_input", True)
    widget_object.set_editor_property("window_focusable", True)
    widget_object.set_draw_at_desired_size(False)

    unreal.BlueprintEditorLibrary.compile_blueprint(blueprint)
    unreal.EditorAssetLibrary.save_loaded_asset(blueprint, only_if_is_dirty=False)
    log(f"Built {BLUEPRINT_PATH}")
    return blueprint


def configure_game_mode() -> None:
    game_mode = unreal.EditorAssetLibrary.load_asset("/Game/Blueprints/BP_LDGameMode")
    menu_pawn_class = unreal.EditorAssetLibrary.load_blueprint_class(BLUEPRINT_PATH)
    if game_mode is None:
        raise RuntimeError("Missing /Game/Blueprints/BP_LDGameMode")
    if menu_pawn_class is None:
        raise RuntimeError(f"Missing generated class for {BLUEPRINT_PATH}")

    generated_class = unreal.BlueprintEditorLibrary.generated_class(game_mode)
    default_object = unreal.get_default_object(generated_class)
    default_object.set_editor_property("default_pawn_class", menu_pawn_class)
    default_object.set_editor_property("start_players_as_spectators", False)

    unreal.BlueprintEditorLibrary.compile_blueprint(game_mode)
    unreal.EditorAssetLibrary.save_loaded_asset(game_mode, only_if_is_dirty=False)
    log("Configured BP_LDGameMode to spawn BP_MainMenuPawn for menu boot")


def place_menu_start() -> None:
    unreal.EditorLevelLibrary.load_level(LEVEL_PATH)
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor.get_actor_label() in {"BP_MainMenuPawn", "MenuPlayerStart"}:
            unreal.EditorLevelLibrary.destroy_actor(actor)

    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PlayerStart,
        unreal.Vector(-260.0, -40.0, 20.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label("MenuPlayerStart")

    unreal.EditorLevelLibrary.save_current_level()
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("Placed MenuPlayerStart into Level 1 menu scene")


def main():
    build_blueprint()
    configure_game_mode()
    place_menu_start()


if __name__ == "__main__":
    main()
