#!/usr/bin/env python3
from dataclasses import dataclass, field

from item_registry import DataRegistry, RegistryError, load_registry


class InventoryError(ValueError):
    pass


@dataclass
class InventoryStack:
    item_id: str
    quantity: int


@dataclass
class InventoryContainer:
    container_id: str
    max_slots: int
    stacks: list[InventoryStack] = field(default_factory=list)

    def quantity(self, item_id: str) -> int:
        return sum(stack.quantity for stack in self.stacks if stack.item_id == item_id)

    def add_item(self, registry: DataRegistry, item_id: str, quantity: int = 1) -> None:
        if quantity <= 0:
            raise InventoryError("Quantity must be positive")

        trial_stacks = [InventoryStack(stack.item_id, stack.quantity) for stack in self.stacks]
        item = registry.item(item_id)
        max_stack = int(item.get("max_stack", 1))
        stackable = bool(item.get("stackable", False))

        if not stackable and quantity > 1:
            raise InventoryError(f"Non-stackable item cannot be added in quantity > 1: {item_id}")

        remaining = quantity
        if stackable:
            for stack in trial_stacks:
                if stack.item_id != item_id or stack.quantity >= max_stack:
                    continue
                moved = min(max_stack - stack.quantity, remaining)
                stack.quantity += moved
                remaining -= moved
                if remaining == 0:
                    return

        while remaining > 0:
            if len(trial_stacks) >= self.max_slots:
                raise InventoryError(f"Container {self.container_id} is full")
            moved = min(max_stack, remaining) if stackable else 1
            trial_stacks.append(InventoryStack(item_id=item_id, quantity=moved))
            remaining -= moved

        self.stacks = trial_stacks

    def remove_item(self, item_id: str, quantity: int = 1) -> None:
        if quantity <= 0:
            raise InventoryError("Quantity must be positive")
        if self.quantity(item_id) < quantity:
            raise InventoryError(f"Not enough {item_id} to remove")

        remaining = quantity
        for stack in list(self.stacks):
            if stack.item_id != item_id:
                continue
            moved = min(stack.quantity, remaining)
            stack.quantity -= moved
            remaining -= moved
            if stack.quantity == 0:
                self.stacks.remove(stack)
            if remaining == 0:
                return

    def clear(self) -> None:
        self.stacks.clear()


@dataclass
class PlayerInventory:
    carried: InventoryContainer
    personal: InventoryContainer

    def apply_death(self) -> None:
        self.carried.clear()


def build_player_inventory(registry: DataRegistry, player_state_id: str = "player_state_v0_meg") -> PlayerInventory:
    player_state = registry.player_states[player_state_id]
    carried_def = registry.storage[player_state["carried_storage_id"]]
    personal_def = registry.storage[player_state["personal_storage_id"]]
    return PlayerInventory(
        carried=InventoryContainer(
            container_id=carried_def["storage_id"],
            max_slots=int(carried_def["caps"].get("slots", 12)),
        ),
        personal=InventoryContainer(
            container_id=personal_def["storage_id"],
            max_slots=int(personal_def["caps"].get("slots", 80)),
        ),
    )


def main() -> None:
    registry = load_registry()
    inventory = build_player_inventory(registry)
    for item_id in registry.faction("meg")["starting_items"]:
        inventory.carried.add_item(registry, item_id)
    print(f"Carried stacks: {len(inventory.carried.stacks)}")
    inventory.apply_death()
    print(f"Carried stacks after death: {len(inventory.carried.stacks)}")


if __name__ == "__main__":
    main()
