#!/usr/bin/env python3
from dataclasses import dataclass

from inventory_model import PlayerInventory, build_player_inventory
from item_registry import DataRegistry, RegistryError, load_registry


@dataclass(frozen=True)
class FactionLoadout:
    faction_id: str
    item_ids: tuple[str, ...]
    items: tuple[dict, ...]

    def __iter__(self):
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def apply_to(self, registry: DataRegistry, inventory: PlayerInventory) -> None:
        for item_id in self.item_ids:
            inventory.carried.add_item(registry, item_id)


def resolve_starting_loadout(registry: DataRegistry, faction_id: str) -> FactionLoadout:
    faction = registry.faction(faction_id)
    item_ids = tuple(faction.get("starting_items", []))
    for item_id in item_ids:
        item = registry.item(item_id)
        restricted_to = item.get("faction_restriction")
        if restricted_to is not None and restricted_to != faction_id:
            raise RegistryError(f"Faction {faction_id} cannot receive restricted item {item_id}")
    return FactionLoadout(
        faction_id=faction_id,
        item_ids=item_ids,
        items=tuple(registry.item(item_id) for item_id in item_ids),
    )


def hub_upgrade_focus(registry: DataRegistry, faction_id: str) -> list[str]:
    faction = registry.factions.get(faction_id)
    if faction is None:
        raise RegistryError(f"Unknown faction_id: {faction_id}")
    return list(faction.get("hub_upgrade_focus", []))


def build_new_realm_inventory(registry: DataRegistry, player_state_id: str = "player_state_v0_meg") -> PlayerInventory:
    player_state = registry.player_states[player_state_id]
    inventory = build_player_inventory(registry, player_state_id)
    resolve_starting_loadout(registry, player_state["faction_id"]).apply_to(registry, inventory)
    return inventory


def reset_realm_for_faction(
    registry: DataRegistry, faction_id: str, player_state_id: str = "player_state_v0_meg"
) -> PlayerInventory:
    inventory = build_player_inventory(registry, player_state_id)
    resolve_starting_loadout(registry, faction_id).apply_to(registry, inventory)
    return inventory


def main() -> None:
    registry = load_registry()
    for faction_id in registry.factions:
        loadout = resolve_starting_loadout(registry, faction_id)
        print(f"{faction_id}: {len(loadout)} starter items")


if __name__ == "__main__":
    main()
