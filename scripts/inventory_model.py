#!/usr/bin/env python3
from dataclasses import dataclass, field

from item_registry import DataRegistry, RegistryError, load_registry


class InventoryError(ValueError):
    pass


@dataclass(frozen=True)
class StorageOverflow:
    item_id: str
    quantity: int
    reason: str
    cap_key: str | None = None


@dataclass(frozen=True)
class StorageTransferResult:
    requested_quantity: int
    moved_quantity: int
    overflow: StorageOverflow | None = None


@dataclass
class InventoryStack:
    item_id: str
    quantity: int


@dataclass
class InventoryContainer:
    container_id: str
    max_slots: int
    max_weight: float | None = None
    class_caps: dict[str, int] = field(default_factory=dict)
    stacks: list[InventoryStack] = field(default_factory=list)

    def quantity(self, item_id: str) -> int:
        return sum(stack.quantity for stack in self.stacks if stack.item_id == item_id)

    def total_weight(self, registry: DataRegistry) -> float:
        return sum(float(registry.item(stack.item_id).get("weight", 0)) * stack.quantity for stack in self.stacks)

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

        if self.max_weight is not None:
            trial_weight = sum(float(registry.item(stack.item_id).get("weight", 0)) * stack.quantity for stack in trial_stacks)
            if trial_weight > self.max_weight:
                raise InventoryError(
                    f"Container {self.container_id} exceeds weight cap: {trial_weight:.2f}/{self.max_weight:.2f}"
                )

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

    def cap_key_for_item(self, registry: DataRegistry, item_id: str) -> str | None:
        item = registry.item(item_id)
        if item_id == "currency_old_movie_ticket":
            return "MovieTickets"
        if item_id == "consumable_almond_water":
            return "AlmondWater"

        category = item.get("category")
        if category == "Resource":
            return "BulkSalvage"
        if category == "Weapon":
            return "Weapons"
        if category == "Armor":
            return "ArmorPlates"
        if category == "Ammo":
            return "Ammunition"
        if category == "Relic" or item.get("rarity") == "RelicClass":
            return "RelicClass"
        return None

    def class_quantity(self, registry: DataRegistry, cap_key: str) -> int:
        total = 0
        for stack in self.stacks:
            if self.cap_key_for_item(registry, stack.item_id) == cap_key:
                total += stack.quantity
        return total

    def remaining_class_capacity(self, registry: DataRegistry, item_id: str) -> tuple[str | None, int | None]:
        cap_key = self.cap_key_for_item(registry, item_id)
        if cap_key is None or cap_key not in self.class_caps:
            return cap_key, None
        cap = int(self.class_caps[cap_key])
        return cap_key, max(cap - self.class_quantity(registry, cap_key), 0)

    def store_with_overflow(
        self,
        registry: DataRegistry,
        item_id: str,
        quantity: int = 1,
    ) -> StorageTransferResult:
        if quantity <= 0:
            raise InventoryError("Quantity must be positive")

        item = registry.item(item_id)
        max_stack = int(item.get("max_stack", 1))
        stackable = bool(item.get("stackable", False))
        cap_key, remaining_capacity = self.remaining_class_capacity(registry, item_id)
        capped_quantity = quantity if remaining_capacity is None else min(quantity, remaining_capacity)

        stored = 0
        remaining = capped_quantity
        failure_reason: str | None = None
        base_chunk = max_stack if stackable else 1

        while remaining > 0:
            chunk = min(base_chunk, remaining)
            moved_this_round = False

            while chunk > 0:
                try:
                    self.add_item(registry, item_id, chunk)
                    stored += chunk
                    remaining -= chunk
                    moved_this_round = True
                    break
                except InventoryError as exc:
                    failure_reason = str(exc)
                    if chunk == 1:
                        chunk = 0
                    else:
                        chunk = max(1, chunk // 2)

            if not moved_this_round:
                break

        overflow_quantity = quantity - stored
        if overflow_quantity <= 0:
            return StorageTransferResult(requested_quantity=quantity, moved_quantity=stored)

        if remaining_capacity is not None and stored == capped_quantity and quantity > capped_quantity:
            overflow_reason = (
                f"Container {self.container_id} reached {cap_key} cap: "
                f"{self.class_quantity(registry, cap_key)}/{int(self.class_caps[cap_key])}"
            )
        else:
            overflow_reason = failure_reason or f"Container {self.container_id} could not store the full quantity"

        return StorageTransferResult(
            requested_quantity=quantity,
            moved_quantity=stored,
            overflow=StorageOverflow(
                item_id=item_id,
                quantity=overflow_quantity,
                reason=overflow_reason,
                cap_key=cap_key,
            ),
        )


@dataclass
class PlayerInventory:
    carried: InventoryContainer
    personal: InventoryContainer

    def apply_death(self) -> None:
        self.carried.clear()

    def move_carried_to_personal(
        self,
        registry: DataRegistry,
        item_id: str,
        quantity: int = 1,
    ) -> StorageTransferResult:
        if self.carried.quantity(item_id) < quantity:
            raise InventoryError(f"Not enough {item_id} in carried inventory")

        result = self.personal.store_with_overflow(registry, item_id, quantity)
        if result.moved_quantity > 0:
            self.carried.remove_item(item_id, result.moved_quantity)
        return result


def build_player_inventory(registry: DataRegistry, player_state_id: str = "player_state_v0_meg") -> PlayerInventory:
    player_state = registry.player_states[player_state_id]
    carried_def = registry.storage[player_state["carried_storage_id"]]
    personal_def = registry.storage[player_state["personal_storage_id"]]
    return PlayerInventory(
        carried=InventoryContainer(
            container_id=carried_def["storage_id"],
            max_slots=int(carried_def["caps"].get("slots", 12)),
            max_weight=float(carried_def["caps"]["weight"]) if "weight" in carried_def["caps"] else None,
        ),
        personal=InventoryContainer(
            container_id=personal_def["storage_id"],
            max_slots=int(personal_def["caps"].get("slots", 80)),
            max_weight=float(personal_def["caps"]["weight"]) if "weight" in personal_def["caps"] else None,
            class_caps={key: int(value) for key, value in personal_def["caps"].items() if isinstance(value, (int, float))},
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
