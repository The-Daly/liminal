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
