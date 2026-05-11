#!/usr/bin/env python3
from dataclasses import dataclass

from item_registry import DataRegistry, RegistryError, load_registry


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


def main() -> None:
    registry = load_registry()
    for route in ordered_routes(registry):
        print(f"{route.route_order}: {route.display_name} -> {', '.join(route.next_route_ids)}")


if __name__ == "__main__":
    main()
