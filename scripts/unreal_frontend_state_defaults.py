#!/usr/bin/env python3
import sys
from pathlib import Path

import unreal


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontend_menu_model import (
    bootstrap_menu_flow,
    build_character_selection_snapshot,
    build_main_player_menu_snapshot,
    build_server_browser_snapshot,
    build_title_shell_copy,
    character_setup_defaults,
    faction_lock_warning,
)
from item_registry import load_registry
from persistent_world_model import create_character_profile


ACTIVE_COUNTS = {"meg": 27, "bntg": 24, "clippers": 22}
QUEUE_COUNTS = {"meg": 2, "bntg": 1, "clippers": 0}
DEFAULT_REALM_ID = "official_north_america_01"
DEFAULT_FACTION_ID = "meg"


def log(message: str) -> None:
    unreal.log(f"[LD Frontend Defaults] {message}")


def load_blueprint(path: str):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if asset is None:
        raise RuntimeError(f"Blueprint asset not found: {path}")
    return asset


def class_default_object(blueprint):
    generated_class = unreal.BlueprintEditorLibrary.generated_class(blueprint)
    if generated_class is None:
        raise RuntimeError(f"Generated class missing for {blueprint.get_path_name()}")
    return unreal.get_default_object(generated_class)


def set_properties(asset_path: str, properties: dict[str, object]) -> None:
    blueprint = load_blueprint(asset_path)
    default_object = class_default_object(blueprint)
    for property_name, property_value in properties.items():
        try:
            default_object.set_editor_property(property_name, property_value)
        except Exception as exc:
            log(f"Skipped property {property_name} on {asset_path}: {exc}")
    unreal.BlueprintEditorLibrary.compile_blueprint(blueprint)
    unreal.EditorAssetLibrary.save_loaded_asset(blueprint, only_if_is_dirty=False)
    log(f"Stamped defaults for {asset_path}")


def main() -> None:
    registry = load_registry()
    title_copy = build_title_shell_copy()
    bootstrap = bootstrap_menu_flow(registry, DEFAULT_REALM_ID, profiles=(), route_id="menu_title_shell")
    server_snapshot = build_server_browser_snapshot(
        registry,
        DEFAULT_REALM_ID,
        active_counts=ACTIVE_COUNTS,
        queue_counts=QUEUE_COUNTS,
    )
    setup_defaults = character_setup_defaults(registry, DEFAULT_FACTION_ID, slot_index=1)
    preview_profile = create_character_profile(
        registry,
        realm_id=DEFAULT_REALM_ID,
        faction_id=DEFAULT_FACTION_ID,
        callsign="Archive-Delta",
        appearance_id=setup_defaults.selected_appearance_id,
        slot_index=1,
        timestamp_utc="2026-05-11T12:00:00Z",
    )
    menu_snapshot = build_main_player_menu_snapshot(
        registry,
        preview_profile,
        active_counts=ACTIVE_COUNTS,
        queue_counts=QUEUE_COUNTS,
    )
    lock_warning = faction_lock_warning(registry, DEFAULT_REALM_ID, DEFAULT_FACTION_ID)

    set_properties(
        "/Game/Blueprints/BP_MenuFlowController",
        {
            "CurrentRouteId": bootstrap.current_route_id,
            "NextRouteId": bootstrap.next_route_id,
            "SelectedRealmId": bootstrap.selected_realm_id,
            "SelectedServerType": bootstrap.selected_server_type,
            "SelectedFactionId": setup_defaults.selected_faction_id,
            "SelectedCharacterId": bootstrap.selected_character_id or "",
            "SelectedAppearanceId": setup_defaults.selected_appearance_id,
            "CharacterCallsign": setup_defaults.character_callsign,
            "HasExistingCharacter": bootstrap.has_existing_character,
            "CharacterConfigured": bootstrap.character_configured,
            "CurrentWipeLabel": server_snapshot.wipe_summary_text,
            "CurrentServerName": server_snapshot.server_name_text,
            "CurrentServerRegion": server_snapshot.server_region_text,
            "FactionPopulationSummary": server_snapshot.faction_population_summary,
            "FactionLockWarningText": lock_warning,
            "DeployEnabled": False,
            "PrimaryActionLabel": title_copy.primary_action_label,
            "SecondaryActionLabel": title_copy.secondary_action_label,
        },
    )

    character_selection_snapshot = build_character_selection_snapshot(preview_profile)

    set_properties(
        "/Game/UI/WBP_TitleShell",
        {
            "HeadlineText": title_copy.headline_text,
            "SubheadText": title_copy.subhead_text,
            "CurrentRouteId": title_copy.current_route_id,
            "NextRouteId": bootstrap.next_route_id,
            "PrimaryActionLabel": title_copy.primary_action_label,
            "SecondaryActionLabel": title_copy.secondary_action_label,
        },
    )
    set_properties(
        "/Game/UI/WBP_ServerBrowser",
        {
            "CurrentRouteId": server_snapshot.current_route_id,
            "SelectedRealmId": server_snapshot.selected_realm_id,
            "SelectedServerType": server_snapshot.selected_server_type,
            "ServerNameText": server_snapshot.server_name_text,
            "ServerRegionText": server_snapshot.server_region_text,
            "RulesetSummaryText": server_snapshot.ruleset_summary_text,
            "WipeSummaryText": server_snapshot.wipe_summary_text,
            "FactionPopulationSummary": server_snapshot.faction_population_summary,
            "QueueSummaryText": server_snapshot.queue_summary_text,
            "CreationStatusText": server_snapshot.creation_status_text,
            "PrimaryActionLabel": server_snapshot.primary_action_label,
            "SecondaryActionLabel": server_snapshot.secondary_action_label,
        },
    )
    set_properties(
        "/Game/UI/WBP_CharacterSelection",
        {
            "CurrentRouteId": character_selection_snapshot.current_route_id,
            "SelectedRealmId": character_selection_snapshot.selected_realm_id,
            "SelectedCharacterId": character_selection_snapshot.selected_character_id,
            "ExistingCharacterStatusText": character_selection_snapshot.existing_character_status_text,
            "CharacterSummaryText": character_selection_snapshot.character_summary_text,
            "PrimaryActionLabel": character_selection_snapshot.primary_action_label,
            "SecondaryActionLabel": character_selection_snapshot.secondary_action_label,
        },
    )
    set_properties(
        "/Game/UI/WBP_FactionSelection",
        {
            "CurrentRouteId": "menu_faction_selection",
            "SelectedRealmId": DEFAULT_REALM_ID,
            "SelectedFactionId": DEFAULT_FACTION_ID,
            "FactionLockWarningText": lock_warning,
            "WipeSummaryText": server_snapshot.wipe_summary_text,
        },
    )
    set_properties(
        "/Game/UI/WBP_CharacterSetup",
        {
            "CurrentRouteId": setup_defaults.current_route_id,
            "SelectedFactionId": setup_defaults.selected_faction_id,
            "SelectedAppearanceId": setup_defaults.selected_appearance_id,
            "CharacterCallsign": setup_defaults.character_callsign,
            "IdentityItemId": setup_defaults.identity_item_id,
            "PrimaryActionLabel": setup_defaults.primary_action_label,
        },
    )
    set_properties(
        "/Game/UI/WBP_MainPlayerMenu",
        {
            "CurrentRouteId": menu_snapshot.current_route_id,
            "SelectedRealmId": menu_snapshot.selected_realm_id,
            "SelectedCharacterId": menu_snapshot.selected_character_id,
            "SelectedFactionId": menu_snapshot.selected_faction_id,
            "ServerNameText": menu_snapshot.server_name_text,
            "ServerRegionText": menu_snapshot.server_region_text,
            "WipeSummaryText": menu_snapshot.wipe_summary_text,
            "FactionPopulationSummary": menu_snapshot.faction_population_summary,
            "CharacterSummaryText": menu_snapshot.character_summary_text,
            "DeployEnabled": menu_snapshot.deploy_enabled,
            "PrimaryActionLabel": menu_snapshot.primary_action_label,
            "SecondaryActionLabel": menu_snapshot.secondary_action_label,
        },
    )

    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("Frontend state defaults pass complete")


if __name__ == "__main__":
    main()
