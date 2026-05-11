#!/usr/bin/env python3
import unreal


PREFIX = "LDG_"
CUBE_PATH = "/Engine/BasicShapes/Cube.Cube"
DEFAULT_WALL_HEIGHT_M = 4.5
DEFAULT_FLOOR_THICKNESS_M = 0.5
DEFAULT_WALL_THICKNESS_M = 0.35
DEFAULT_CEILING_THICKNESS_M = 0.3

HUB_MAP = "/Game/Maps/LD_Hub_Greybox"
PERSONAL_ROOM_MAP = "/Game/Maps/LD_PersonalRoom_Greybox"
SERVICE_HALLS_MAP = "/Game/Maps/LD_Level1_ServiceHalls_Greybox"

LEGACY_PLACEHOLDER_LABELS = {
    "BP_MenuFlowController",
    "BP_CharacterPreviewAnchor",
    "BP_FactionNpcPreviewAnchor",
    "BP_DeploymentGate",
    "BP_ProjectBoard",
    "BP_FactionVaultPlaceholder",
    "BP_QuartermasterPlaceholder",
    "BP_TraderPlaceholder",
    "BP_FactionSelectorPlaceholder",
    "BP_PersonalStorage",
    "BP_RelicDisplayPlaceholder",
    "BP_LootContainer",
    "BP_ExtractionTrigger_Stable",
    "BP_ExtractionTrigger_HiddenTicketBooth",
    "BP_FlickerStalker",
}

BLUEPRINT_PATHS = {
    "MenuFlowController": "/Game/Blueprints/BP_MenuFlowController",
    "CharacterPreviewAnchor": "/Game/Blueprints/BP_CharacterPreviewAnchor",
    "FactionNpcPreviewAnchor": "/Game/Blueprints/BP_FactionNpcPreviewAnchor",
    "DeploymentGate": "/Game/Blueprints/BP_DeploymentGate",
    "ProjectBoard": "/Game/Blueprints/BP_ProjectBoard",
    "FactionVault": "/Game/Blueprints/BP_FactionVaultPlaceholder",
    "Quartermaster": "/Game/Blueprints/BP_QuartermasterPlaceholder",
    "Trader": "/Game/Blueprints/BP_TraderPlaceholder",
    "FactionSelector": "/Game/Blueprints/BP_FactionSelectorPlaceholder",
    "PersonalStorage": "/Game/Blueprints/BP_PersonalStorage",
    "RelicDisplay": "/Game/Blueprints/BP_RelicDisplayPlaceholder",
    "LootContainer": "/Game/Blueprints/BP_LootContainer",
    "StableExtraction": "/Game/Blueprints/BP_ExtractionTrigger_Stable",
    "HiddenExtraction": "/Game/Blueprints/BP_ExtractionTrigger_HiddenTicketBooth",
    "FlickerStalker": "/Game/Blueprints/BP_FlickerStalker",
}


def log(message: str) -> None:
    unreal.log(f"[LD Graybox] {message}")


def meters(x: float, y: float, z: float = 0.0) -> unreal.Vector:
    return unreal.Vector(x * 100.0, y * 100.0, z * 100.0)


def load_asset(path: str):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if asset is None:
        raise RuntimeError(f"Required asset was not found: {path}")
    return asset


def remove_generated_actors() -> None:
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        label = actor.get_actor_label()
        if label.startswith(PREFIX) or label in LEGACY_PLACEHOLDER_LABELS:
            unreal.EditorLevelLibrary.destroy_actor(actor)
            log(f"Removed {label}")


def spawn_actor(actor_class, label: str, location: unreal.Vector, rotation: unreal.Rotator | None = None):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        actor_class,
        location,
        rotation or unreal.Rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label(label)
    return actor


def stamp_properties(actor, properties: dict[str, object] | None) -> None:
    if not properties:
        return

    for property_name, property_value in properties.items():
        try:
            actor.set_editor_property(property_name, property_value)
        except Exception as exc:
            log(f"Skipped property {property_name} on {actor.get_actor_label()}: {exc}")


def spawn_blueprint_actor(
    asset_path: str,
    label: str,
    location: unreal.Vector,
    properties: dict[str, object] | None = None,
):
    blueprint = load_asset(asset_path)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
        blueprint,
        location,
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label(label)
    stamp_properties(actor, properties)
    return actor


def spawn_box(label: str, location: unreal.Vector, size_m: tuple[float, float, float]) -> unreal.Actor:
    actor = spawn_actor(unreal.StaticMeshActor, label, location)
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    component.set_static_mesh(load_asset(CUBE_PATH))
    actor.set_actor_scale3d(
        unreal.Vector(
            size_m[0],
            size_m[1],
            size_m[2],
        )
    )
    return actor


def spawn_floor(label: str, center_xy_m: tuple[float, float], size_m: tuple[float, float], top_z_m: float = 0.0):
    thickness_m = DEFAULT_FLOOR_THICKNESS_M
    location = meters(center_xy_m[0], center_xy_m[1], top_z_m - (thickness_m / 2.0))
    return spawn_box(label, location, (size_m[0], size_m[1], thickness_m))


def spawn_ceiling(label: str, center_xy_m: tuple[float, float], size_m: tuple[float, float], bottom_z_m: float = DEFAULT_WALL_HEIGHT_M):
    thickness_m = DEFAULT_CEILING_THICKNESS_M
    location = meters(center_xy_m[0], center_xy_m[1], bottom_z_m + (thickness_m / 2.0))
    return spawn_box(label, location, (size_m[0], size_m[1], thickness_m))


def spawn_wall(label: str, center_m: tuple[float, float], size_m: tuple[float, float], height_m: float = DEFAULT_WALL_HEIGHT_M):
    location = meters(center_m[0], center_m[1], height_m / 2.0)
    return spawn_box(label, location, (size_m[0], size_m[1], height_m))


def build_room_shell(
    name: str,
    center_xy_m: tuple[float, float],
    size_m: tuple[float, float],
    open_sides: tuple[str, ...] = (),
    with_ceiling: bool = True,
) -> None:
    half_x = size_m[0] / 2.0
    half_y = size_m[1] / 2.0
    wall_t = DEFAULT_WALL_THICKNESS_M
    x = center_xy_m[0]
    y = center_xy_m[1]

    spawn_floor(f"{PREFIX}{name}_Floor", center_xy_m, size_m)
    if with_ceiling:
        spawn_ceiling(f"{PREFIX}{name}_Ceiling", center_xy_m, size_m)

    if "north" not in open_sides:
        spawn_wall(
            f"{PREFIX}{name}_NorthWall",
            (x, y + half_y - (wall_t / 2.0)),
            (size_m[0], wall_t),
        )
    if "south" not in open_sides:
        spawn_wall(
            f"{PREFIX}{name}_SouthWall",
            (x, y - half_y + (wall_t / 2.0)),
            (size_m[0], wall_t),
        )
    if "east" not in open_sides:
        spawn_wall(
            f"{PREFIX}{name}_EastWall",
            (x + half_x - (wall_t / 2.0), y),
            (wall_t, size_m[1]),
        )
    if "west" not in open_sides:
        spawn_wall(
            f"{PREFIX}{name}_WestWall",
            (x - half_x + (wall_t / 2.0), y),
            (wall_t, size_m[1]),
        )


def build_corridor(name: str, start_m: tuple[float, float], end_m: tuple[float, float], width_m: float = 8.0, with_ceiling: bool = True) -> None:
    wall_t = DEFAULT_WALL_THICKNESS_M
    height_m = DEFAULT_WALL_HEIGHT_M

    def horizontal_segment(seg_name: str, x1: float, x2: float, y: float) -> None:
        length_m = abs(x2 - x1) + width_m
        center_x = (x1 + x2) / 2.0
        spawn_floor(f"{PREFIX}{seg_name}_Floor", (center_x, y), (length_m, width_m))
        if with_ceiling:
            spawn_ceiling(f"{PREFIX}{seg_name}_Ceiling", (center_x, y), (length_m, width_m))
        spawn_wall(f"{PREFIX}{seg_name}_NorthWall", (center_x, y + (width_m / 2.0) - (wall_t / 2.0)), (length_m, wall_t), height_m)
        spawn_wall(f"{PREFIX}{seg_name}_SouthWall", (center_x, y - (width_m / 2.0) + (wall_t / 2.0)), (length_m, wall_t), height_m)

    def vertical_segment(seg_name: str, x: float, y1: float, y2: float) -> None:
        length_m = abs(y2 - y1) + width_m
        center_y = (y1 + y2) / 2.0
        spawn_floor(f"{PREFIX}{seg_name}_Floor", (x, center_y), (width_m, length_m))
        if with_ceiling:
            spawn_ceiling(f"{PREFIX}{seg_name}_Ceiling", (x, center_y), (width_m, length_m))
        spawn_wall(f"{PREFIX}{seg_name}_EastWall", (x + (width_m / 2.0) - (wall_t / 2.0), center_y), (wall_t, length_m), height_m)
        spawn_wall(f"{PREFIX}{seg_name}_WestWall", (x - (width_m / 2.0) + (wall_t / 2.0), center_y), (wall_t, length_m), height_m)

    if start_m[0] != end_m[0]:
        horizontal_segment(f"{name}_H", start_m[0], end_m[0], start_m[1])
    if start_m[1] != end_m[1]:
        vertical_segment(f"{name}_V", end_m[0], start_m[1], end_m[1])


def spawn_point_light(label: str, location_m: tuple[float, float, float], intensity: float = 25000.0, attenuation_radius: float = 2800.0):
    actor = spawn_actor(unreal.PointLight, f"{PREFIX}{label}", meters(*location_m))
    component = actor.get_component_by_class(unreal.PointLightComponent)
    component.set_editor_property("intensity", intensity)
    component.set_editor_property("attenuation_radius", attenuation_radius)
    return actor


def spawn_player_start(label: str, location_m: tuple[float, float, float]):
    return spawn_actor(unreal.PlayerStart, f"{PREFIX}{label}", meters(*location_m))


def spawn_text(label: str, text_value: str, location_m: tuple[float, float, float], scale: float = 2.5) -> None:
    try:
        actor = spawn_actor(unreal.TextRenderActor, f"{PREFIX}{label}", meters(*location_m))
        component = actor.get_component_by_class(unreal.TextRenderComponent)
        component.set_editor_property("text", text_value)
        actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
    except Exception as exc:
        log(f"Skipped text actor {label}: {exc}")


def add_landmark_pillar(label: str, location_m: tuple[float, float, float], size_m: tuple[float, float, float]) -> None:
    spawn_box(f"{PREFIX}{label}", meters(*location_m), size_m)


def add_objective_pad(label: str, center_xy_m: tuple[float, float], size_m: tuple[float, float]) -> None:
    spawn_floor(f"{PREFIX}{label}", center_xy_m, size_m, top_z_m=0.08)


def build_hub_map() -> None:
    unreal.EditorLevelLibrary.load_level(HUB_MAP)
    remove_generated_actors()

    build_room_shell("HubMainHall", (0.0, 0.0), (34.0, 24.0), open_sides=("east", "west"))
    build_corridor("HubToPersonal", (-26.0, 0.0), (-8.0, 0.0), width_m=6.0)
    build_corridor("HubToDeployment", (8.0, 0.0), (28.0, 0.0), width_m=7.0)
    build_corridor("HubToFrontendOps", (0.0, -12.0), (0.0, -17.0), width_m=6.0)
    build_room_shell("HubFrontendOps", (0.0, -24.0), (24.0, 14.0), open_sides=("north",))

    spawn_floor(f"{PREFIX}HubBoardPad", (0.0, 8.0), (7.0, 4.0))
    spawn_floor(f"{PREFIX}HubVaultPad", (-10.0, 8.0), (7.0, 4.0))
    spawn_floor(f"{PREFIX}HubQuartermasterPad", (-8.0, -8.0), (7.0, 4.0))
    spawn_floor(f"{PREFIX}HubTraderPad", (8.0, -8.0), (7.0, 4.0))
    spawn_floor(f"{PREFIX}HubFactionSelectorPad", (0.0, -4.0), (5.0, 3.0))
    spawn_floor(f"{PREFIX}HubFrontendControllerPad", (0.0, -21.0), (6.0, 2.6))
    spawn_floor(f"{PREFIX}HubFrontendOperatorPad", (0.0, -26.0), (4.0, 4.0))
    spawn_floor(f"{PREFIX}HubFrontendFactionPadA", (-7.0, -26.0), (3.2, 3.2))
    spawn_floor(f"{PREFIX}HubFrontendFactionPadB", (7.0, -26.0), (3.2, 3.2))
    spawn_floor(f"{PREFIX}HubFrontendFactionPadC", (0.0, -29.2), (3.2, 3.2))
    add_objective_pad("HubDeployStepPad", (20.0, 0.0), (6.0, 3.2))
    add_objective_pad("HubStoreStepPad", (-2.0, 8.0), (7.0, 2.8))
    add_objective_pad("HubContributeStepPad", (5.5, 8.0), (8.0, 2.8))
    add_objective_pad("HubFrontendServerStepPad", (-7.0, -20.8), (4.4, 2.2))
    add_objective_pad("HubFrontendFactionStepPad", (0.0, -20.8), (4.4, 2.2))
    add_objective_pad("HubFrontendCharacterStepPad", (7.0, -20.8), (4.4, 2.2))

    add_landmark_pillar("HubSignalLampBase", (11.0, 8.0, 2.0), (1.2, 1.2, 4.0))
    add_landmark_pillar("HubSignalLampCore", (11.0, 8.0, 4.8), (0.5, 0.5, 1.2))
    add_landmark_pillar("HubDeploymentFrameLeft", (30.0, -2.5, 2.5), (1.0, 1.0, 5.0))
    add_landmark_pillar("HubDeploymentFrameRight", (30.0, 2.5, 2.5), (1.0, 1.0, 5.0))
    add_landmark_pillar("HubQuartermasterDesk", (-8.0, -6.4, 1.1), (4.5, 1.2, 2.2))
    add_landmark_pillar("HubTraderDesk", (8.0, -6.4, 1.1), (4.5, 1.2, 2.2))
    add_landmark_pillar("HubFactionSelectorMonolith", (0.0, -4.0, 1.8), (1.2, 1.2, 3.6))
    add_landmark_pillar("HubFrontendWallNorth", (0.0, -17.2, 2.0), (10.0, 0.8, 4.0))
    add_landmark_pillar("HubFrontendWallWest", (-10.5, -24.0, 2.0), (0.8, 5.8, 4.0))
    add_landmark_pillar("HubFrontendWallEast", (10.5, -24.0, 2.0), (0.8, 5.8, 4.0))
    add_landmark_pillar("HubFrontendOpsDesk", (0.0, -21.2, 1.1), (5.0, 1.0, 2.2))

    spawn_player_start("HubPlayerStart", (-12.0, 0.0, 0.5))
    spawn_point_light("HubLight01", (-10.0, 0.0, 3.6), intensity=20000.0)
    spawn_point_light("HubLight02", (0.0, 0.0, 3.6), intensity=22000.0)
    spawn_point_light("HubLight03", (12.0, 0.0, 3.6), intensity=22000.0)
    spawn_point_light("HubLight04", (0.0, 8.0, 3.6), intensity=18000.0)
    spawn_point_light("HubLight05", (-8.0, -8.0, 3.4), intensity=17000.0)
    spawn_point_light("HubLight06", (8.0, -8.0, 3.4), intensity=17000.0)
    spawn_point_light("HubLight07", (0.0, -20.5, 3.4), intensity=15000.0)
    spawn_point_light("HubLight08", (-7.0, -26.0, 3.0), intensity=9500.0, attenuation_radius=1800.0)
    spawn_point_light("HubLight09", (7.0, -26.0, 3.0), intensity=9500.0, attenuation_radius=1800.0)
    spawn_point_light("HubLight10", (0.0, -29.2, 2.8), intensity=8500.0, attenuation_radius=1600.0)
    spawn_point_light("HubSignalLampLight", (11.0, 8.0, 5.2), intensity=30000.0, attenuation_radius=2200.0)

    spawn_text("HubSignDeployment", "DEPLOYMENT", (22.0, 0.0, 3.2))
    spawn_text("HubSignPersonalRoom", "PERSONAL ROOM", (-22.0, 0.0, 3.2))
    spawn_text("HubSignBoard", "SIGNAL LAMP PROJECT", (0.0, 10.0, 2.4), scale=1.5)
    spawn_text("HubSignQuartermaster", "QUARTERMASTER", (-8.0, -10.2, 2.2), scale=1.2)
    spawn_text("HubSignTrader", "TRADER", (8.0, -10.2, 2.2), scale=1.2)
    spawn_text("HubSignFaction", "FACTION SELECTOR", (0.0, -1.6, 2.3), scale=1.1)
    spawn_text("HubFrontendTitle", "SERIOUS FRONTEND STAGING", (0.0, -17.2, 3.0), scale=1.1)
    spawn_text("HubFrontendIntro", "TITLE -> SERVER -> FACTION -> CHARACTER -> MENU", (0.0, -18.7, 2.2), scale=0.85)
    spawn_text("HubFrontendStepServer", "STEP A: SERVER REALM", (-7.0, -19.0, 1.8), scale=0.8)
    spawn_text("HubFrontendStepFaction", "STEP B: FACTION LOCK", (0.0, -19.0, 1.8), scale=0.8)
    spawn_text("HubFrontendStepCharacter", "STEP C: CHARACTER SETUP", (7.0, -19.0, 1.8), scale=0.8)
    spawn_text("HubFrontendPreview", "OPERATOR PREVIEW", (0.0, -23.0, 2.0), scale=0.9)
    spawn_text("HubFrontendMeg", "M.E.G.", (-7.0, -23.0, 1.9), scale=0.85)
    spawn_text("HubFrontendBntg", "B.N.T.G.", (7.0, -23.0, 1.9), scale=0.85)
    spawn_text("HubFrontendClippers", "CLIPPERS", (0.0, -31.0, 1.9), scale=0.85)
    spawn_text("HubStepDeploy", "STEP 1: DEPLOY", (20.0, 2.8, 1.4), scale=0.95)
    spawn_text("HubStepStore", "STEP 5: STORE LOOT", (-2.0, 10.4, 1.4), scale=0.85)
    spawn_text("HubStepContribute", "STEP 6: CONTRIBUTE", (5.5, 10.4, 1.4), scale=0.85)
    spawn_text("HubFlowReminder", "RUN FLOW: DEPLOY -> LOOT -> EXTRACT -> RETURN", (0.0, -11.0, 2.0), scale=0.9)

    spawn_blueprint_actor(
        BLUEPRINT_PATHS["MenuFlowController"],
        f"{PREFIX}HubMenuFlowController",
        meters(0.0, -21.0, 1.2),
        {
            "CurrentRouteId": "menu_title_shell",
            "NextRouteId": "menu_server_browser",
            "SelectedRealmId": "official_north_america_01",
            "SelectedServerType": "official",
            "SelectedFactionId": "meg",
            "SelectedCharacterId": "",
            "SelectedAppearanceId": "appearance_meg_operator_field_v0",
            "CharacterCallsign": "MEG-01",
            "HasExistingCharacter": False,
            "CharacterConfigured": False,
            "CurrentWipeLabel": "Biannual Official Wipe | Next wipe 2028-01-01",
            "CurrentServerName": "Official Realm NA-01",
            "CurrentServerRegion": "US East | Official Realm",
            "FactionPopulationSummary": "MEG 27/30 | BNTG 24/30 | CLIPPERS 22/30",
            "FactionLockWarningText": "M.E.G. becomes your locked faction on Official Realm NA-01 until the next wipe.",
            "DeployEnabled": False,
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["CharacterPreviewAnchor"],
        f"{PREFIX}HubOperatorPreviewAnchor",
        meters(0.0, -26.0, 1.2),
        {
            "AppearanceId": "appearance_meg_operator_field_v0",
            "FactionId": "meg",
            "PreviewRole": "PlayerOperator",
            "DisplayNameText": "M.E.G. Field Operator",
            "IdentityItemId": "tool_meg_entity_scanner",
            "PreviewSceneLabel": "Main Menu Character Preview",
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["FactionNpcPreviewAnchor"],
        f"{PREFIX}HubMegNpcPreview",
        meters(-7.0, -26.0, 1.2),
        {
            "AppearanceId": "appearance_meg_archive_staff_v0",
            "FactionId": "meg",
            "PreviewRole": "FactionNpc",
            "DisplayNameText": "M.E.G. Archive Staff",
            "IdentityItemId": "tool_meg_entity_scanner",
            "PreviewSceneLabel": "Faction Preview Left",
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["FactionNpcPreviewAnchor"],
        f"{PREFIX}HubBntgNpcPreview",
        meters(7.0, -26.0, 1.2),
        {
            "AppearanceId": "appearance_bntg_market_clerk_v0",
            "FactionId": "bntg",
            "PreviewRole": "FactionNpc",
            "DisplayNameText": "B.N.T.G. Market Clerk",
            "IdentityItemId": "tool_bntg_crowbar",
            "PreviewSceneLabel": "Faction Preview Right",
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["FactionNpcPreviewAnchor"],
        f"{PREFIX}HubClippersNpcPreview",
        meters(0.0, -29.2, 1.2),
        {
            "AppearanceId": "appearance_clippers_route_scribe_v0",
            "FactionId": "clippers",
            "PreviewRole": "FactionNpc",
            "DisplayNameText": "Clippers Route Scribe",
            "IdentityItemId": "tool_clippers_camcorder",
            "PreviewSceneLabel": "Faction Preview Rear",
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["DeploymentGate"],
        f"{PREFIX}HubDeploymentGate",
        meters(29.0, 0.0, 1.2),
        {
            "InteractionPrompt": "Press E to deploy to the Service Halls.",
            "TargetMapPath": "/Game/Maps/LD_Level1_ServiceHalls_Greybox.LD_Level1_ServiceHalls_Greybox",
            "ReturnMapPath": "/Game/Maps/LD_PersonalRoom_Greybox.LD_PersonalRoom_Greybox",
            "RunStateId": "run_level1_service_halls_v0",
            "PlayerStateId": "player_state_v0_meg",
            "BoardUpgradeId": "hub_project_board_signal_lamp_v0",
            "StartsRun": True,
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["ProjectBoard"],
        f"{PREFIX}HubProjectBoard",
        meters(0.0, 8.0, 1.2),
        {
            "InteractionPrompt": "Press E to contribute loot to the Signal Lamp Project.",
            "HubUpgradeId": "hub_project_board_signal_lamp_v0",
            "FactionId": "meg",
            "TracksPartialProgress": True,
            "VisibleUnlockLabel": "Signal Lamp Project",
        },
    )
    spawn_blueprint_actor(BLUEPRINT_PATHS["FactionVault"], f"{PREFIX}HubFactionVault", meters(-10.0, 8.0, 1.2))
    spawn_blueprint_actor(BLUEPRINT_PATHS["Quartermaster"], f"{PREFIX}HubQuartermaster", meters(-8.0, -8.0, 1.2))
    spawn_blueprint_actor(BLUEPRINT_PATHS["Trader"], f"{PREFIX}HubTrader", meters(8.0, -8.0, 1.2))
    spawn_blueprint_actor(BLUEPRINT_PATHS["FactionSelector"], f"{PREFIX}HubFactionSelector", meters(0.0, -4.0, 1.2))

    unreal.EditorLevelLibrary.save_current_level()
    log("Saved LD_Hub_Greybox")


def build_personal_room_map() -> None:
    unreal.EditorLevelLibrary.load_level(PERSONAL_ROOM_MAP)
    remove_generated_actors()

    build_room_shell("PersonalRoomMain", (0.0, 0.0), (16.0, 11.0), open_sides=("west",))
    build_corridor("PersonalRoomEntry", (-14.0, 0.0), (-6.0, 0.0), width_m=4.5)

    spawn_floor(f"{PREFIX}PersonalStoragePad", (4.0, 3.0), (5.0, 2.6))
    spawn_floor(f"{PREFIX}RelicDisplayPad", (-2.5, 3.0), (3.5, 2.2))
    spawn_floor(f"{PREFIX}BedPad", (2.0, -2.8), (4.0, 2.4))
    spawn_floor(f"{PREFIX}WorkbenchPad", (-1.0, -2.6), (3.6, 2.0))
    add_objective_pad("PersonalReturnPad", (-3.5, 0.0), (4.2, 2.4))
    add_objective_pad("PersonalDepositPad", (4.0, 3.0), (5.8, 3.0))

    add_landmark_pillar("PersonalRoomLocker", (5.8, 3.0, 1.6), (0.8, 0.8, 3.2))
    add_landmark_pillar("PersonalRoomDisplayCase", (-2.5, 3.0, 1.4), (1.0, 0.8, 2.8))
    add_landmark_pillar("PersonalRoomWorkbench", (-1.0, -2.4, 1.0), (3.2, 1.0, 2.0))

    spawn_player_start("PersonalRoomPlayerStart", (-3.5, 0.0, 0.5))
    spawn_point_light("PersonalRoomLight01", (-3.0, 0.0, 3.2), intensity=18000.0, attenuation_radius=2200.0)
    spawn_point_light("PersonalRoomLight02", (4.0, 0.0, 3.2), intensity=15000.0, attenuation_radius=2200.0)
    spawn_point_light("PersonalRoomLight03", (-2.5, 3.0, 2.8), intensity=12000.0, attenuation_radius=1800.0)

    spawn_text("PersonalRoomSignStorage", "SAFE STORAGE", (4.0, 4.8, 2.2), scale=1.2)
    spawn_text("PersonalRoomSignRelics", "RELIC DISPLAY", (-2.5, 4.8, 2.2), scale=1.2)
    spawn_text("PersonalRoomSignWorkbench", "WORKBENCH", (-1.0, -0.7, 2.1), scale=1.0)
    spawn_text("PersonalRoomStepReturn", "RETURN POINT", (-3.5, 1.6, 1.7), scale=0.8)
    spawn_text("PersonalRoomStepDeposit", "STEP 5: DEPOSIT LOOT", (4.0, 1.2, 1.7), scale=0.8)

    spawn_blueprint_actor(
        BLUEPRINT_PATHS["PersonalStorage"],
        f"{PREFIX}PersonalRoomStorage",
        meters(4.0, 3.0, 1.2),
        {
            "InteractionPrompt": "Press E to deposit carried loot into safe storage.",
            "StorageId": "storage_personal_room_tier0",
            "DepositLabel": "Personal Room Safe Storage",
            "PreservesLootOnDeath": True,
        },
    )
    spawn_blueprint_actor(BLUEPRINT_PATHS["RelicDisplay"], f"{PREFIX}PersonalRoomRelicDisplay", meters(-2.5, 3.0, 1.2))

    unreal.EditorLevelLibrary.save_current_level()
    log("Saved LD_PersonalRoom_Greybox")


def build_service_halls_map() -> None:
    unreal.EditorLevelLibrary.load_level(SERVICE_HALLS_MAP)
    remove_generated_actors()

    anchors = {
        "HubArrivalGate": (0.0, 0.0),
        "MainServiceSpine": (220.0, 70.0),
        "ServiceHallNorth": (240.0, 270.0),
        "FoggedStorageBay": (-90.0, 250.0),
        "ArchiveOffice": (70.0, 470.0),
        "FlickerCorridor": (500.0, 340.0),
        "UtilityRooms": (620.0, 70.0),
        "TraderKiosk": (540.0, -190.0),
        "TheaterCorner": (140.0, -210.0),
        "CrawlspaceRoute": (220.0, -420.0),
        "ClippersRouteWall": (470.0, -520.0),
        "StableExtraction": (-240.0, 90.0),
        "HiddenTicketBooth": (40.0, -560.0),
    }

    rooms = {
        "HubArrivalGate": ((0.0, 0.0), (26.0, 16.0), ("east", "west")),
        "MainServiceSpine": ((220.0, 70.0), (72.0, 18.0), ("west", "east", "north")),
        "ServiceHallNorth": ((240.0, 270.0), (46.0, 20.0), ("west", "east", "south")),
        "FoggedStorageBay": ((-90.0, 250.0), (58.0, 40.0), ("east", "south")),
        "ArchiveOffice": ((70.0, 470.0), (30.0, 24.0), ("south",)),
        "FlickerCorridor": ((500.0, 340.0), (96.0, 14.0), ("west", "south")),
        "UtilityRooms": ((620.0, 70.0), (52.0, 34.0), ("west", "north")),
        "TraderKiosk": ((540.0, -190.0), (34.0, 26.0), ("west",)),
        "TheaterCorner": ((140.0, -210.0), (38.0, 30.0), ("north", "east", "south")),
        "CrawlspaceRoute": ((220.0, -420.0), (28.0, 12.0), ("north", "east", "south")),
        "ClippersRouteWall": ((470.0, -520.0), (36.0, 16.0), ("west",)),
        "StableExtraction": ((-240.0, 90.0), (24.0, 18.0), ("east",)),
        "HiddenTicketBooth": ((40.0, -560.0), (18.0, 18.0), ("north", "east")),
    }

    for room_name, room_spec in rooms.items():
        build_room_shell(room_name, room_spec[0], room_spec[1], open_sides=room_spec[2])

    build_corridor("HubToSpine", anchors["HubArrivalGate"], anchors["MainServiceSpine"], width_m=8.0)
    build_corridor("HubToStable", anchors["HubArrivalGate"], anchors["StableExtraction"], width_m=7.0)
    build_corridor("SpineToNorth", anchors["MainServiceSpine"], anchors["ServiceHallNorth"], width_m=8.0)
    build_corridor("NorthToStorage", anchors["ServiceHallNorth"], anchors["FoggedStorageBay"], width_m=8.0)
    build_corridor("NorthToArchive", anchors["ServiceHallNorth"], anchors["ArchiveOffice"], width_m=7.0)
    build_corridor("NorthToFlicker", anchors["ServiceHallNorth"], anchors["FlickerCorridor"], width_m=7.0)
    build_corridor("FlickerToUtility", anchors["FlickerCorridor"], anchors["UtilityRooms"], width_m=7.0)
    build_corridor("SpineToTheater", anchors["MainServiceSpine"], anchors["TheaterCorner"], width_m=7.0)
    build_corridor("TheaterToKiosk", anchors["TheaterCorner"], anchors["TraderKiosk"], width_m=7.0)
    build_corridor("TheaterToCrawlspace", anchors["TheaterCorner"], anchors["CrawlspaceRoute"], width_m=5.0)
    build_corridor("CrawlspaceToHiddenExit", anchors["CrawlspaceRoute"], anchors["HiddenTicketBooth"], width_m=4.5)
    build_corridor("HiddenExitToClippers", anchors["HiddenTicketBooth"], anchors["ClippersRouteWall"], width_m=5.0)

    spawn_player_start("ServiceHallsPlayerStart", (-6.0, 0.0, 0.5))

    spawn_point_light("ServiceLightHubArrival", (0.0, 0.0, 3.5), intensity=14000.0, attenuation_radius=2400.0)
    spawn_point_light("ServiceLightSpineA", (180.0, 70.0, 3.5), intensity=12000.0, attenuation_radius=2600.0)
    spawn_point_light("ServiceLightSpineB", (260.0, 70.0, 3.5), intensity=12000.0, attenuation_radius=2600.0)
    spawn_point_light("ServiceLightNorth", (240.0, 270.0, 3.5), intensity=13500.0, attenuation_radius=2400.0)
    spawn_point_light("ServiceLightStorage", (-90.0, 250.0, 3.5), intensity=9000.0, attenuation_radius=2600.0)
    spawn_point_light("ServiceLightArchive", (70.0, 470.0, 3.5), intensity=10000.0, attenuation_radius=2200.0)
    spawn_point_light("ServiceLightFlickerA", (460.0, 340.0, 3.2), intensity=7000.0, attenuation_radius=2200.0)
    spawn_point_light("ServiceLightFlickerB", (540.0, 340.0, 2.9), intensity=5000.0, attenuation_radius=2200.0)
    spawn_point_light("ServiceLightUtility", (620.0, 70.0, 3.2), intensity=9500.0, attenuation_radius=2500.0)
    spawn_point_light("ServiceLightTheater", (140.0, -210.0, 3.2), intensity=8500.0, attenuation_radius=2300.0)
    spawn_point_light("ServiceLightKiosk", (540.0, -190.0, 3.2), intensity=9000.0, attenuation_radius=2200.0)
    spawn_point_light("ServiceLightHiddenExit", (40.0, -560.0, 2.8), intensity=7000.0, attenuation_radius=1800.0)

    add_landmark_pillar("ArchiveMonolith", (70.0, 470.0, 2.8), (2.0, 2.0, 5.6))
    add_landmark_pillar("KioskCounter", (540.0, -190.0, 1.1), (4.0, 1.2, 2.2))
    add_landmark_pillar("TheaterScreen", (148.0, -196.0, 2.2), (0.8, 6.0, 4.4))
    add_landmark_pillar("ClippersWall", (470.0, -520.0, 2.8), (10.0, 0.8, 5.6))

    add_landmark_pillar("StorageCrateStackA", (-106.0, 240.0, 1.0), (3.5, 2.0, 2.0))
    add_landmark_pillar("StorageCrateStackB", (-72.0, 258.0, 0.8), (2.8, 1.6, 1.6))
    add_landmark_pillar("UtilityBenchA", (606.0, 58.0, 0.6), (4.0, 1.2, 1.2))
    add_landmark_pillar("UtilityBenchB", (634.0, 88.0, 0.6), (3.4, 1.3, 1.2))
    add_objective_pad("ServiceStartPad", (18.0, 0.0), (5.0, 3.2))
    add_objective_pad("ServiceLootPad", (-92.0, 246.0), (6.0, 3.0))
    add_objective_pad("ServiceEncounterPad", (500.0, 340.0), (8.0, 3.0))
    add_objective_pad("ServiceExtractPad", (-240.0, 90.0), (6.0, 3.0))
    add_objective_pad("ServiceHiddenExitPad", (40.0, -560.0), (5.0, 3.0))

    spawn_text("ServiceSignArchive", "M.E.G. ARCHIVE", (70.0, 482.0, 2.6), scale=1.3)
    spawn_text("ServiceSignStorage", "FOGGED STORAGE BAY", (-90.0, 264.0, 2.5), scale=1.1)
    spawn_text("ServiceSignTheater", "ABANDONED THEATER", (140.0, -196.0, 2.4), scale=1.1)
    spawn_text("ServiceSignFlicker", "FLICKER CORRIDOR", (500.0, 350.0, 2.6), scale=1.2)
    spawn_text("ServiceSignKiosk", "B.N.T.G. KIOSK", (540.0, -176.0, 2.4), scale=1.2)
    spawn_text("ServiceSignCrawlspace", "CRAWLSPACE ROUTE", (220.0, -408.0, 2.2), scale=1.0)
    spawn_text("ServiceSignRouteWall", "CLIPPERS ROUTE WALL", (470.0, -506.0, 2.4), scale=1.0)
    spawn_text("ServiceSignChalkA", "TICKETS ->", (206.0, -438.0, 1.8), scale=0.8)
    spawn_text("ServiceSignChalkB", "EXIT?", (456.0, -534.0, 1.8), scale=0.8)
    spawn_text("ServiceSignHidden", "TICKET BOOTH EXIT", (40.0, -548.0, 2.4), scale=1.1)
    spawn_text("ServiceSignStable", "STABLE EXTRACTION", (-240.0, 102.0, 2.4), scale=1.1)
    spawn_text("ServiceStepStart", "STEP 2: ENTER RAID ZONE", (18.0, 12.0, 1.8), scale=0.8)
    spawn_text("ServiceStepLoot", "STEP 3: LOOT HERE", (-92.0, 230.0, 1.8), scale=0.9)
    spawn_text("ServiceStepEncounter", "STEP 4: ENTITY ENCOUNTER", (500.0, 356.0, 1.9), scale=0.9)
    spawn_text("ServiceStepExtract", "STEP 4B: EXTRACT", (-240.0, 76.0, 1.9), scale=0.9)
    spawn_text("ServiceStepHidden", "ALT EXIT: MOVIE TICKET", (40.0, -576.0, 1.9), scale=0.8)
    spawn_text("ServiceFlowReminder", "FOLLOW SIGNS: LOOT -> STALKER -> EXTRACT", (220.0, 90.0, 2.0), scale=0.9)

    spawn_blueprint_actor(
        BLUEPRINT_PATHS["LootContainer"],
        f"{PREFIX}LootContainer_StartRoute",
        meters(32.0, 14.0, 1.2),
        {
            "InteractionPrompt": "Press E to search the arrival cache.",
            "LootTableId": "loot_level1_basic",
            "ContainerLabel": "Arrival Cache",
            "SingleUse": True,
            "TracksCarriedInventory": True,
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["LootContainer"],
        f"{PREFIX}LootContainer_FoggedStorage",
        meters(-92.0, 246.0, 1.2),
        {
            "InteractionPrompt": "Press E to search the fogged storage crates.",
            "LootTableId": "loot_level1_basic",
            "ContainerLabel": "Fogged Storage Crates",
            "SingleUse": True,
            "TracksCarriedInventory": True,
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["LootContainer"],
        f"{PREFIX}LootContainer_ArchiveOffice",
        meters(74.0, 466.0, 1.2),
        {
            "InteractionPrompt": "Press E to search the archive office desk.",
            "LootTableId": "loot_level1_basic",
            "ContainerLabel": "Archive Office Desk",
            "SingleUse": True,
            "TracksCarriedInventory": True,
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["LootContainer"],
        f"{PREFIX}LootContainer_UtilityRooms",
        meters(614.0, 76.0, 1.2),
        {
            "InteractionPrompt": "Press E to search the utility workbench.",
            "LootTableId": "loot_level1_basic",
            "ContainerLabel": "Utility Workbench",
            "SingleUse": True,
            "TracksCarriedInventory": True,
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["LootContainer"],
        f"{PREFIX}LootContainer_TheaterCorner",
        meters(132.0, -216.0, 1.2),
        {
            "InteractionPrompt": "Press E to search the theater corner stash.",
            "LootTableId": "loot_level1_basic",
            "ContainerLabel": "Theater Corner Stash",
            "SingleUse": True,
            "TracksCarriedInventory": True,
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["LootContainer"],
        f"{PREFIX}LootContainer_KioskPocket",
        meters(546.0, -202.0, 1.2),
        {
            "InteractionPrompt": "Press E to search the kiosk pocket cache.",
            "LootTableId": "loot_level1_basic",
            "ContainerLabel": "Kiosk Pocket Cache",
            "SingleUse": True,
            "TracksCarriedInventory": True,
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["LootContainer"],
        f"{PREFIX}LootContainer_CrawlspaceRoute",
        meters(228.0, -426.0, 1.2),
        {
            "InteractionPrompt": "Press E to search the crawlspace stash.",
            "LootTableId": "loot_level1_basic",
            "ContainerLabel": "Crawlspace Stash",
            "SingleUse": True,
            "TracksCarriedInventory": True,
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["StableExtraction"],
        f"{PREFIX}Extraction_Stable",
        meters(-240.0, 90.0, 1.2),
        {
            "InteractionPrompt": "Press E to extract through the stable service door.",
            "ExtractionId": "extract_level1_stable_service_door",
            "ReturnMapPath": "/Game/Maps/LD_PersonalRoom_Greybox.LD_PersonalRoom_Greybox",
            "RequiredItemId": "",
            "ReturnsToPersonalRoom": True,
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["HiddenExtraction"],
        f"{PREFIX}Extraction_HiddenTicketBooth",
        meters(40.0, -560.0, 1.2),
        {
            "InteractionPrompt": "Press E to use the hidden ticket booth exit.",
            "ExtractionId": "extract_level1_hidden_ticket_booth",
            "ReturnMapPath": "/Game/Maps/LD_PersonalRoom_Greybox.LD_PersonalRoom_Greybox",
            "RequiredItemId": "currency_old_movie_ticket",
            "ReturnsToPersonalRoom": True,
        },
    )
    spawn_blueprint_actor(
        BLUEPRINT_PATHS["FlickerStalker"],
        f"{PREFIX}FlickerStalker_MainPatrol",
        meters(500.0, 340.0, 1.2),
        {
            "EncounterLabel": "Flicker Stalker Patrol",
            "SanityRuleId": "sanity_level1_service_halls_v0",
            "ForcesRetreatPath": True,
        },
    )
    spawn_blueprint_actor(BLUEPRINT_PATHS["Trader"], f"{PREFIX}ServiceTraderKioskPlaceholder", meters(540.0, -190.0, 1.2))

    unreal.EditorLevelLibrary.save_current_level()
    log("Saved LD_Level1_ServiceHalls_Greybox")


def main() -> None:
    build_hub_map()
    build_personal_room_map()
    build_service_halls_map()
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("Graybox layout pass complete")


if __name__ == "__main__":
    main()
