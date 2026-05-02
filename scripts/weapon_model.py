#!/usr/bin/env python3
from typing import Optional

from inventory_model import InventoryContainer, InventoryError
from item_registry import DataRegistry, RegistryError, load_registry


def ammo_for_weapon(registry: DataRegistry, weapon_id: str) -> Optional[dict]:
    weapon = registry.weapons.get(weapon_id)
    if weapon is None:
        raise RegistryError(f"Unknown weapon_id: {weapon_id}")
    ammo_type_id = weapon.get("ammo_type_id")
    if ammo_type_id is None:
        return None
    return registry.ammo.get(ammo_type_id)


def can_fire(registry: DataRegistry, weapon_id: str, inventory: InventoryContainer) -> bool:
    ammo = ammo_for_weapon(registry, weapon_id)
    if ammo is None:
        return True
    return inventory.quantity(ammo["item_id"]) > 0


def consume_round(registry: DataRegistry, weapon_id: str, inventory: InventoryContainer) -> None:
    ammo = ammo_for_weapon(registry, weapon_id)
    if ammo is None:
        return
    if inventory.quantity(ammo["item_id"]) <= 0:
        raise InventoryError(f"No ammo available for {weapon_id}")
    inventory.remove_item(ammo["item_id"], 1)


def can_craft(registry: DataRegistry, recipe_id: str, inventory: InventoryContainer) -> bool:
    recipe = registry.crafting_recipes.get(recipe_id)
    if recipe is None:
        raise RegistryError(f"Unknown recipe_id: {recipe_id}")
    return all(inventory.quantity(entry["item_id"]) >= entry["quantity"] for entry in recipe.get("ingredients", []))


def craft_recipe(registry: DataRegistry, recipe_id: str, inventory: InventoryContainer) -> None:
    if not can_craft(registry, recipe_id, inventory):
        raise InventoryError(f"Missing ingredients for {recipe_id}")
    recipe = registry.crafting_recipes[recipe_id]
    for ingredient in recipe.get("ingredients", []):
        inventory.remove_item(ingredient["item_id"], ingredient["quantity"])
    for output in recipe.get("outputs", []):
        inventory.add_item(registry, output["item_id"], output["quantity"])


def can_open_container(registry: DataRegistry, container_id: str, inventory: InventoryContainer) -> bool:
    container = registry.containers.get(container_id)
    if container is None:
        raise RegistryError(f"Unknown container_id: {container_id}")
    required_tool = container.get("required_tool_item_id")
    return required_tool is None or inventory.quantity(required_tool) > 0


def main() -> None:
    registry = load_registry()
    print(f"Weapons: {len(registry.weapons)}")
    print(f"Ammo types: {len(registry.ammo)}")
    print(f"Recipes: {len(registry.crafting_recipes)}")
    print(f"Containers: {len(registry.containers)}")


if __name__ == "__main__":
    main()
