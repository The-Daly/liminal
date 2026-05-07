#!/usr/bin/env python3
from dataclasses import dataclass, field

from inventory_model import InventoryContainer, InventoryError
from item_registry import DataRegistry, RegistryError, load_registry


@dataclass(frozen=True)
class ContributionStatus:
    item_id: str
    required_quantity: int
    contributed_quantity: int

    @property
    def remaining_quantity(self) -> int:
        return max(self.required_quantity - self.contributed_quantity, 0)

    @property
    def is_complete(self) -> bool:
        return self.remaining_quantity == 0


@dataclass(frozen=True)
class ContributionResult:
    hub_upgrade_id: str
    item_id: str
    moved_quantity: int
    remaining_quantity: int
    completed_upgrade: bool


@dataclass
class HubProgressState:
    faction_id: str
    contributions: dict[str, dict[str, int]] = field(default_factory=dict)
    completed_upgrades: set[str] = field(default_factory=set)


def upgrades_for_faction(registry: DataRegistry, faction_id: str) -> list[dict]:
    if faction_id not in registry.factions:
        raise RegistryError(f"Unknown faction_id: {faction_id}")
    return [
        upgrade for upgrade in registry.hub_upgrades.values()
        if upgrade["faction_id"] == faction_id
    ]


def contribution_statuses(
    registry: DataRegistry,
    state: HubProgressState,
    hub_upgrade_id: str,
) -> list[ContributionStatus]:
    upgrade = registry.hub_upgrades.get(hub_upgrade_id)
    if upgrade is None:
        raise RegistryError(f"Unknown hub_upgrade_id: {hub_upgrade_id}")
    if upgrade["faction_id"] != state.faction_id:
        raise RegistryError(
            f"Hub upgrade {hub_upgrade_id} belongs to faction {upgrade['faction_id']}, not {state.faction_id}"
        )

    contributed = state.contributions.get(hub_upgrade_id, {})
    return [
        ContributionStatus(
            item_id=requirement["item_id"],
            required_quantity=int(requirement["quantity"]),
            contributed_quantity=int(contributed.get(requirement["item_id"], 0)),
        )
        for requirement in upgrade.get("contribution_requirements", [])
    ]


def is_upgrade_complete(registry: DataRegistry, state: HubProgressState, hub_upgrade_id: str) -> bool:
    if hub_upgrade_id in state.completed_upgrades:
        return True
    return all(status.is_complete for status in contribution_statuses(registry, state, hub_upgrade_id))


def contribute_item(
    registry: DataRegistry,
    state: HubProgressState,
    hub_upgrade_id: str,
    source: InventoryContainer,
    item_id: str,
    quantity: int,
) -> ContributionResult:
    if quantity <= 0:
        raise InventoryError("Quantity must be positive")

    statuses = {status.item_id: status for status in contribution_statuses(registry, state, hub_upgrade_id)}
    status = statuses.get(item_id)
    if status is None:
        raise RegistryError(f"Hub upgrade {hub_upgrade_id} does not accept item {item_id}")

    allowed = min(quantity, status.remaining_quantity, source.quantity(item_id))
    if allowed <= 0:
        return ContributionResult(
            hub_upgrade_id=hub_upgrade_id,
            item_id=item_id,
            moved_quantity=0,
            remaining_quantity=status.remaining_quantity,
            completed_upgrade=is_upgrade_complete(registry, state, hub_upgrade_id),
        )

    source.remove_item(item_id, allowed)
    upgrade_progress = state.contributions.setdefault(hub_upgrade_id, {})
    upgrade_progress[item_id] = int(upgrade_progress.get(item_id, 0)) + allowed

    if is_upgrade_complete(registry, state, hub_upgrade_id):
        state.completed_upgrades.add(hub_upgrade_id)

    updated_status = {s.item_id: s for s in contribution_statuses(registry, state, hub_upgrade_id)}[item_id]
    return ContributionResult(
        hub_upgrade_id=hub_upgrade_id,
        item_id=item_id,
        moved_quantity=allowed,
        remaining_quantity=updated_status.remaining_quantity,
        completed_upgrade=hub_upgrade_id in state.completed_upgrades,
    )


def contribute_all_possible(
    registry: DataRegistry,
    state: HubProgressState,
    hub_upgrade_id: str,
    source: InventoryContainer,
) -> list[ContributionResult]:
    results: list[ContributionResult] = []
    for status in contribution_statuses(registry, state, hub_upgrade_id):
        if status.remaining_quantity <= 0:
            continue
        results.append(
            contribute_item(
                registry,
                state,
                hub_upgrade_id,
                source,
                status.item_id,
                status.remaining_quantity,
            )
        )
    return results


def main() -> None:
    registry = load_registry()
    state = HubProgressState(faction_id="meg")
    storage = InventoryContainer("demo", max_slots=10)
    storage.add_item(registry, "currency_old_movie_ticket", 25)
    storage.add_item(registry, "item_scrap_metal", 5)
    results = contribute_all_possible(registry, state, "hub_project_board_signal_lamp_v0", storage)
    for result in results:
        print(
            f"{result.item_id}: moved {result.moved_quantity}, "
            f"remaining {result.remaining_quantity}, complete={result.completed_upgrade}"
        )


if __name__ == "__main__":
    main()
