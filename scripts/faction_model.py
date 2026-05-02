#!/usr/bin/env python3
from item_registry import DataRegistry, RegistryError, load_registry


def resolve_starting_loadout(registry: DataRegistry, faction_id: str) -> list[dict]:
    faction = registry.factions.get(faction_id)
    if faction is None:
        raise RegistryError(f"Unknown faction_id: {faction_id}")
    return [registry.item(item_id) for item_id in faction.get("starting_items", [])]


def hub_upgrade_focus(registry: DataRegistry, faction_id: str) -> list[str]:
    faction = registry.factions.get(faction_id)
    if faction is None:
        raise RegistryError(f"Unknown faction_id: {faction_id}")
    return list(faction.get("hub_upgrade_focus", []))


def main() -> None:
    registry = load_registry()
    for faction_id in registry.factions:
        loadout = resolve_starting_loadout(registry, faction_id)
        print(f"{faction_id}: {len(loadout)} starter items")


if __name__ == "__main__":
    main()
