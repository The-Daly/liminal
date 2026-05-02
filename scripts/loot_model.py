#!/usr/bin/env python3
import random
from typing import Optional
from typing import Any

from item_registry import DataRegistry, RegistryError


def roll_loot(registry: DataRegistry, loot_table_id: str, rng: Optional[random.Random] = None) -> str:
    table = registry.loot_tables.get(loot_table_id)
    if table is None:
        raise RegistryError(f"Unknown loot_table_id: {loot_table_id}")

    entries = table.get("entries", [])
    total_weight = sum(entry["weight"] for entry in entries)
    if total_weight <= 0:
        raise RegistryError(f"Loot table has no positive weight entries: {loot_table_id}")

    rng = rng or random.Random()
    pick = rng.uniform(0, total_weight)
    running = 0.0
    for entry in entries:
        running += entry["weight"]
        if pick <= running:
            return entry["item_id"]

    return entries[-1]["item_id"]


def preview_table(registry: DataRegistry, loot_table_id: str) -> list[dict[str, Any]]:
    table = registry.loot_tables.get(loot_table_id)
    if table is None:
        raise RegistryError(f"Unknown loot_table_id: {loot_table_id}")
    total_weight = sum(entry["weight"] for entry in table["entries"])
    return [
        {
            "item_id": entry["item_id"],
            "display_name": registry.item(entry["item_id"])["display_name"],
            "weight": entry["weight"],
            "chance": entry["weight"] / total_weight if total_weight else 0,
        }
        for entry in table["entries"]
    ]


def container_owner(registry: DataRegistry, container_id: str) -> Optional[str]:
    container = registry.containers.get(container_id)
    if container is None:
        raise RegistryError(f"Unknown container_id: {container_id}")
    return container.get("owner_faction_id")


def is_level1_weapon_armor_sparse(registry: DataRegistry, density_profile_id: str = "density_level1_slim_v0") -> bool:
    density = registry.loot_density.get(density_profile_id)
    if density is None:
        raise RegistryError(f"Unknown density_profile_id: {density_profile_id}")
    for table in registry.loot_tables.values():
        if not table["loot_table_id"].startswith("loot_level1_"):
            continue
        for entry in table.get("entries", []):
            item = registry.item(entry["item_id"])
            if item.get("category") == "Weapon" and entry["weight"] > density["weapon_weight_cap"]:
                return False
            if item.get("category") == "Armor" and entry["weight"] > density["armor_weight_cap"]:
                return False
    return True
