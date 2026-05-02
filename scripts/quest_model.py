#!/usr/bin/env python3
from inventory_model import InventoryContainer
from item_registry import DataRegistry, RegistryError, load_registry


def is_quest_complete(registry: DataRegistry, quest_id: str, inventory: InventoryContainer) -> bool:
    quest = registry.quests.get(quest_id)
    if quest is None:
        raise RegistryError(f"Unknown quest_id: {quest_id}")
    for objective in quest.get("objectives", []):
        item_id = objective.get("item_id")
        if item_id is None:
            return False
        if inventory.quantity(item_id) < objective["quantity"]:
            return False
    return True


def quest_ids_for_npc(registry: DataRegistry, npc_id: str) -> list[str]:
    npc = registry.npcs.get(npc_id)
    if npc is None:
        raise RegistryError(f"Unknown npc_id: {npc_id}")
    return list(npc.get("quest_ids", []))


def reward_preview(registry: DataRegistry, quest_id: str) -> list[tuple[str, int]]:
    quest = registry.quests.get(quest_id)
    if quest is None:
        raise RegistryError(f"Unknown quest_id: {quest_id}")
    return [(reward["item_id"], reward["quantity"]) for reward in quest.get("rewards", [])]


def main() -> None:
    registry = load_registry()
    for quest_id in registry.quests:
        rewards = reward_preview(registry, quest_id)
        print(f"{quest_id}: {len(rewards)} rewards")


if __name__ == "__main__":
    main()
