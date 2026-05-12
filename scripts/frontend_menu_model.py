#!/usr/bin/env python3
from dataclasses import dataclass

from item_registry import DataRegistry, RegistryError, load_registry
from persistent_world_model import (
    CharacterProfile,
    first_profile_for_realm,
    realm_menu_summary,
    slot_summary,
)


@dataclass(frozen=True)
class MenuRoute:
    menu_route_id: str
    display_name: str
    route_order: int
    next_route_ids: tuple[str, ...]
    blocks_deploy: bool
    description: str


@dataclass(frozen=True)
class MenuFlowState:
    route_id: str
    realm_id: str | None
    has_existing_character: bool
    faction_selected: bool
    character_configured: bool


@dataclass(frozen=True)
class TitleShellCopy:
    headline_text: str
    subhead_text: str
    current_route_id: str
    primary_action_label: str
    secondary_action_label: str


@dataclass(frozen=True)
class ServerBrowserSnapshot:
    current_route_id: str
    selected_realm_id: str
    selected_server_type: str
    server_name_text: str
    server_region_text: str
    ruleset_summary_text: str
    wipe_summary_text: str
    faction_population_summary: str
    queue_summary_text: str
    creation_status_text: str
    primary_action_label: str
    secondary_action_label: str


@dataclass(frozen=True)
class CharacterSelectionSnapshot:
    current_route_id: str
    selected_realm_id: str
    selected_character_id: str
    existing_character_status_text: str
    character_summary_text: str
    primary_action_label: str
    secondary_action_label: str


@dataclass(frozen=True)
class CharacterSetupDefaults:
    current_route_id: str
    selected_faction_id: str
    selected_appearance_id: str
    character_callsign: str
    identity_item_id: str
    primary_action_label: str


@dataclass(frozen=True)
class MainPlayerMenuSnapshot:
    current_route_id: str
    selected_realm_id: str
    selected_character_id: str
    selected_faction_id: str
    server_name_text: str
    server_region_text: str
    wipe_summary_text: str
    faction_population_summary: str
    character_summary_text: str
    deploy_enabled: bool
    primary_action_label: str
    secondary_action_label: str


@dataclass(frozen=True)
class MenuFlowBootstrap:
    current_route_id: str
    next_route_id: str
    selected_realm_id: str
    selected_server_type: str
    has_existing_character: bool
    selected_character_id: str | None
    selected_faction_id: str | None
    character_configured: bool


def menu_route(registry: DataRegistry, menu_route_id: str) -> MenuRoute:
    record = registry.menu_routes.get(menu_route_id)
    if record is None:
        raise RegistryError(f"Unknown menu_route_id: {menu_route_id}")
    return MenuRoute(
        menu_route_id=record["menu_route_id"],
        display_name=record["display_name"],
        route_order=int(record["route_order"]),
        next_route_ids=tuple(record.get("next_route_ids", [])),
        blocks_deploy=bool(record["blocks_deploy"]),
        description=record["description"],
    )


def resolve_next_route(state: MenuFlowState) -> str:
    if state.route_id == "menu_title_shell":
        return "menu_server_browser"
    if state.route_id == "menu_server_browser":
        return "menu_character_selection" if state.has_existing_character else "menu_faction_selection"
    if state.route_id == "menu_character_selection":
        return "menu_main_player_hub" if state.has_existing_character else "menu_faction_selection"
    if state.route_id == "menu_faction_selection":
        return "menu_character_setup"
    if state.route_id == "menu_character_setup":
        return "menu_main_player_hub" if state.character_configured else "menu_character_setup"
    if state.route_id in {"menu_main_player_hub", "menu_deploy_panel", "menu_stash_panel", "menu_settings_panel"}:
        return state.route_id
    raise RegistryError(f"Unsupported route transition from {state.route_id}")


def ordered_routes(registry: DataRegistry) -> list[MenuRoute]:
    return sorted(
        (menu_route(registry, route_id) for route_id in registry.menu_routes),
        key=lambda route: route.route_order,
    )


def build_title_shell_copy(route_id: str = "menu_title_shell") -> TitleShellCopy:
    return TitleShellCopy(
        headline_text="Liminal Dominion",
        subhead_text=(
            "Choose a realm, accept a faction lock, and enter a world that will remember "
            "where you stood until the next mass wipe."
        ),
        current_route_id=route_id,
        primary_action_label="Enter Server Browser",
        secondary_action_label="Review Wipe Terms",
    )


def build_server_browser_snapshot(
    registry: DataRegistry,
    realm_id: str,
    active_counts: dict[str, int] | None = None,
    queue_counts: dict[str, int] | None = None,
    route_id: str = "menu_server_browser",
) -> ServerBrowserSnapshot:
    summary = realm_menu_summary(
        registry,
        realm_id,
        active_counts=active_counts,
        queue_counts=queue_counts,
    )
    creation_status_text = (
        "Character creation available"
        if summary.supports_character_creation
        else "Character creation unavailable"
    )
    queue_summary_text = f"Population {summary.total_active}/{summary.total_capacity} | Queue {summary.total_queue}"
    return ServerBrowserSnapshot(
        current_route_id=route_id,
        selected_realm_id=summary.realm_id,
        selected_server_type=summary.server_type,
        server_name_text=summary.display_name,
        server_region_text=f"{summary.region} | {summary.server_type.title()} Realm",
        ruleset_summary_text=summary.ruleset_summary,
        wipe_summary_text=summary.wipe_summary_text,
        faction_population_summary=summary.faction_population_summary,
        queue_summary_text=queue_summary_text,
        creation_status_text=creation_status_text,
        primary_action_label="Select Realm",
        secondary_action_label="Compare Populations",
    )


def build_character_selection_snapshot(
    profile: CharacterProfile,
    route_id: str = "menu_character_selection",
) -> CharacterSelectionSnapshot:
    slot = slot_summary(profile)
    return CharacterSelectionSnapshot(
        current_route_id=route_id,
        selected_realm_id=slot.realm_id,
        selected_character_id=slot.character_id,
        existing_character_status_text="Existing character found on selected realm.",
        character_summary_text=(
            f"{slot.callsign} | {slot.faction_id.upper()} | Slot {slot.slot_index} | Wipe {slot.wipe_id}"
        ),
        primary_action_label="Enter Character Menu",
        secondary_action_label="Review Faction Lock",
    )


def faction_lock_warning(registry: DataRegistry, realm_id: str, faction_id: str) -> str:
    summary = realm_menu_summary(registry, realm_id)
    faction_name = registry.faction(faction_id)["display_name"]
    return (
        f"{faction_name} becomes your locked faction on {summary.display_name} until the next wipe. "
        f"{summary.wipe_summary_text}."
    )


def character_setup_defaults(
    registry: DataRegistry,
    faction_id: str,
    slot_index: int = 1,
    route_id: str = "menu_character_setup",
) -> CharacterSetupDefaults:
    appearances = sorted(
        (
            record for record in registry.character_appearance.values()
            if record["faction_id"] == faction_id and "player" in record.get("usable_by", [])
        ),
        key=lambda record: record["appearance_id"],
    )
    if not appearances:
        raise RegistryError(f"No player appearance presets found for faction {faction_id}")

    appearance = appearances[0]
    callsign_prefix = faction_id.upper()[:4]
    return CharacterSetupDefaults(
        current_route_id=route_id,
        selected_faction_id=faction_id,
        selected_appearance_id=appearance["appearance_id"],
        character_callsign=f"{callsign_prefix}-{slot_index:02d}",
        identity_item_id=appearance["identity_item_id"],
        primary_action_label="Confirm Character",
    )


def build_main_player_menu_snapshot(
    registry: DataRegistry,
    profile: CharacterProfile,
    active_counts: dict[str, int] | None = None,
    queue_counts: dict[str, int] | None = None,
    route_id: str = "menu_main_player_hub",
) -> MainPlayerMenuSnapshot:
    summary = realm_menu_summary(
        registry,
        profile.realm_id,
        active_counts=active_counts,
        queue_counts=queue_counts,
    )
    slot = slot_summary(profile)
    character_summary_text = (
        f"{slot.callsign} | {slot.faction_id.upper()} | Slot {slot.slot_index} | Wipe {slot.wipe_id}"
    )
    return MainPlayerMenuSnapshot(
        current_route_id=route_id,
        selected_realm_id=profile.realm_id,
        selected_character_id=profile.character_id,
        selected_faction_id=profile.faction_id,
        server_name_text=summary.display_name,
        server_region_text=f"{summary.region} | {summary.server_type.title()} Realm",
        wipe_summary_text=summary.wipe_summary_text,
        faction_population_summary=summary.faction_population_summary,
        character_summary_text=character_summary_text,
        deploy_enabled=not menu_route(registry, route_id).blocks_deploy,
        primary_action_label="Deploy Operator",
        secondary_action_label="Open Stash",
    )


def bootstrap_menu_flow(
    registry: DataRegistry,
    realm_id: str,
    profiles: tuple[CharacterProfile, ...] = (),
    route_id: str = "menu_title_shell",
) -> MenuFlowBootstrap:
    existing_profile = first_profile_for_realm(profiles, realm_id)
    descriptor = realm_menu_summary(registry, realm_id)
    state = MenuFlowState(
        route_id=route_id,
        realm_id=realm_id,
        has_existing_character=existing_profile is not None,
        faction_selected=existing_profile is not None,
        character_configured=existing_profile is not None,
    )
    return MenuFlowBootstrap(
        current_route_id=route_id,
        next_route_id=resolve_next_route(state),
        selected_realm_id=realm_id,
        selected_server_type=descriptor.server_type,
        has_existing_character=existing_profile is not None,
        selected_character_id=existing_profile.character_id if existing_profile else None,
        selected_faction_id=existing_profile.faction_id if existing_profile else None,
        character_configured=existing_profile is not None,
    )


def main() -> None:
    registry = load_registry()
    for route in ordered_routes(registry):
        print(f"{route.route_order}: {route.display_name} -> {', '.join(route.next_route_ids)}")
    print(build_title_shell_copy().headline_text)


if __name__ == "__main__":
    main()
