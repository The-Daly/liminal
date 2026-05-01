#!/usr/bin/env python3
from item_registry import DataRegistry, RegistryError
from inventory_model import InventoryContainer


def can_extract(registry: DataRegistry, extraction_id: str, carried: InventoryContainer) -> bool:
    extraction = registry.extractions.get(extraction_id)
    if extraction is None:
        raise RegistryError(f"Unknown extraction_id: {extraction_id}")
    return all(carried.quantity(item_id) > 0 for item_id in extraction.get("required_item_ids", []))


def extract_destination(extraction_id: str) -> str:
    if extraction_id.startswith("extract_level1_"):
        return "LD_PersonalRoom_Greybox"
    return "LD_Hub_Greybox"
