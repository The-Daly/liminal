#!/usr/bin/env python3
from dataclasses import dataclass
import random

from extraction_model import can_extract, extract_destination
from faction_model import build_new_realm_inventory
from inventory_model import InventoryError, PlayerInventory
from item_registry import DataRegistry, RegistryError, load_registry
from loot_model import roll_loot
from project_board_model import HubProgressState, contribute_all_possible
from survival_model import SanityState


@dataclass(frozen=True)
class LoopOutcome:
    faction_id: str
    run_state_id: str
    extracted: bool
    died: bool
    extraction_id: str | None
    destination_map: str | None
    looted_item_ids: tuple[str, ...]
    deposited_item_ids: tuple[str, ...]
    completed_upgrades: tuple[str, ...]
    remaining_sanity: float


def move_all_carried_to_personal(registry: DataRegistry, inventory: PlayerInventory) -> list[str]:
    moved_items: list[str] = []
    carried_snapshot = [(stack.item_id, stack.quantity) for stack in list(inventory.carried.stacks)]
    for item_id, quantity in carried_snapshot:
        result = inventory.move_carried_to_personal(registry, item_id, quantity)
        if result.moved_quantity > 0:
            moved_items.append(item_id)
    return moved_items


def simulate_successful_run(
    registry: DataRegistry,
    faction_id: str = "meg",
    run_state_id: str = "run_level1_service_halls_v0",
    loot_rolls: int = 4,
    rng: random.Random | None = None,
) -> LoopOutcome:
    if faction_id not in registry.factions:
        raise RegistryError(f"Unknown faction_id: {faction_id}")

    player_state = next(
        (
            player_state_id
            for player_state_id, player_state in registry.player_states.items()
            if player_state["faction_id"] == faction_id
        ),
        None,
    )
    if player_state is None:
        raise RegistryError(f"No player_state is configured for faction {faction_id}")

    run_state = registry.run_states.get(run_state_id)
    if run_state is None:
        raise RegistryError(f"Unknown run_state_id: {run_state_id}")

    rng = rng or random.Random()
    inventory = build_new_realm_inventory(registry, player_state)
    sanity = SanityState.from_rule(
        registry.sanity_rules[run_state["sanity_rule_id"]],
        starting_sanity=registry.player_states[player_state]["starting_sanity"],
    )

    looted_item_ids: list[str] = []
    for _ in range(loot_rolls):
        item_id = roll_loot(registry, run_state["loot_table_id"], rng)
        inventory.carried.add_item(registry, item_id)
        looted_item_ids.append(item_id)

    sanity.drain_seconds(600)
    if sanity.is_low and inventory.carried.quantity("consumable_almond_water") > 0:
        inventory.carried.remove_item("consumable_almond_water", 1)
        sanity.consume_almond_water()

    extraction_id = next(
        (
            candidate
            for candidate in run_state.get("extraction_ids", [])
            if can_extract(registry, candidate, inventory.carried)
        ),
        None,
    )
    if extraction_id is None:
        raise InventoryError("No extraction is currently available for the carried inventory")

    deposited_item_ids = move_all_carried_to_personal(registry, inventory)
    progress = HubProgressState(faction_id=faction_id)
    for upgrade in registry.hub_upgrades.values():
        if upgrade["faction_id"] == faction_id:
            contribute_all_possible(registry, progress, upgrade["hub_upgrade_id"], inventory.personal)

    return LoopOutcome(
        faction_id=faction_id,
        run_state_id=run_state_id,
        extracted=True,
        died=False,
        extraction_id=extraction_id,
        destination_map=extract_destination(extraction_id),
        looted_item_ids=tuple(looted_item_ids),
        deposited_item_ids=tuple(deposited_item_ids),
        completed_upgrades=tuple(sorted(progress.completed_upgrades)),
        remaining_sanity=sanity.current,
    )


def simulate_death_run(
    registry: DataRegistry,
    faction_id: str = "meg",
    run_state_id: str = "run_level1_service_halls_v0",
    loot_rolls: int = 3,
    rng: random.Random | None = None,
) -> LoopOutcome:
    if faction_id not in registry.factions:
        raise RegistryError(f"Unknown faction_id: {faction_id}")
    if run_state_id not in registry.run_states:
        raise RegistryError(f"Unknown run_state_id: {run_state_id}")

    player_state = next(
        (
            player_state_id
            for player_state_id, player_state in registry.player_states.items()
            if player_state["faction_id"] == faction_id
        ),
        None,
    )
    if player_state is None:
        raise RegistryError(f"No player_state is configured for faction {faction_id}")

    rng = rng or random.Random()
    inventory = build_new_realm_inventory(registry, player_state)
    looted_item_ids: list[str] = []
    for _ in range(loot_rolls):
        item_id = roll_loot(registry, registry.run_states[run_state_id]["loot_table_id"], rng)
        inventory.carried.add_item(registry, item_id)
        looted_item_ids.append(item_id)

    inventory.apply_death()

    return LoopOutcome(
        faction_id=faction_id,
        run_state_id=run_state_id,
        extracted=False,
        died=True,
        extraction_id=None,
        destination_map=None,
        looted_item_ids=tuple(looted_item_ids),
        deposited_item_ids=(),
        completed_upgrades=(),
        remaining_sanity=float(
            registry.player_states[player_state]["starting_sanity"]
        ),
    )


def main() -> None:
    registry = load_registry()
    success = simulate_successful_run(registry, rng=random.Random(7))
    print(
        f"Success run: extracted via {success.extraction_id}, "
        f"deposited {len(success.deposited_item_ids)} item types, "
        f"completed upgrades={list(success.completed_upgrades)}"
    )
    death = simulate_death_run(registry, rng=random.Random(7))
    print(
        f"Death run: looted {len(death.looted_item_ids)} item types, "
        f"carried inventory wiped={death.died}"
    )


if __name__ == "__main__":
    main()
