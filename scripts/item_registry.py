#!/usr/bin/env python3
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "data" / "seed"


class RegistryError(ValueError):
    pass


def load_json(path: Path) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise RegistryError(f"Expected list data in {path}")
    return data


def index_by(records: list[dict[str, Any]], id_field: str, source_name: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for record in records:
        record_id = record.get(id_field)
        if not record_id:
            raise RegistryError(f"Missing {id_field} in {source_name}: {record}")
        if record_id in indexed:
            raise RegistryError(f"Duplicate {id_field} in {source_name}: {record_id}")
        indexed[record_id] = record
    return indexed


@dataclass(frozen=True)
class DataRegistry:
    items: dict[str, dict[str, Any]]
    factions: dict[str, dict[str, Any]]
    loot_tables: dict[str, dict[str, Any]]
    entities: dict[str, dict[str, Any]]
    storage: dict[str, dict[str, Any]]
    sanity_rules: dict[str, dict[str, Any]]
    extractions: dict[str, dict[str, Any]]
    hub_upgrades: dict[str, dict[str, Any]]
    player_states: dict[str, dict[str, Any]]
    run_states: dict[str, dict[str, Any]]

    def item(self, item_id: str) -> dict[str, Any]:
        try:
            return self.items[item_id]
        except KeyError as exc:
            raise RegistryError(f"Unknown item_id: {item_id}") from exc

    def faction(self, faction_id: str) -> dict[str, Any]:
        try:
            return self.factions[faction_id]
        except KeyError as exc:
            raise RegistryError(f"Unknown faction_id: {faction_id}") from exc


def load_registry(seed_dir: Path = SEED_DIR) -> DataRegistry:
    return DataRegistry(
        items=index_by(load_json(seed_dir / "items.seed.json"), "item_id", "items.seed.json"),
        factions=index_by(load_json(seed_dir / "factions.seed.json"), "faction_id", "factions.seed.json"),
        loot_tables=index_by(load_json(seed_dir / "loot_tables.seed.json"), "loot_table_id", "loot_tables.seed.json"),
        entities=index_by(load_json(seed_dir / "entities.seed.json"), "entity_id", "entities.seed.json"),
        storage=index_by(load_json(seed_dir / "storage.seed.json"), "storage_id", "storage.seed.json"),
        sanity_rules=index_by(load_json(seed_dir / "sanity.seed.json"), "sanity_rule_id", "sanity.seed.json"),
        extractions=index_by(load_json(seed_dir / "extractions.seed.json"), "extraction_id", "extractions.seed.json"),
        hub_upgrades=index_by(load_json(seed_dir / "hub_upgrades.seed.json"), "hub_upgrade_id", "hub_upgrades.seed.json"),
        player_states=index_by(load_json(seed_dir / "player_state.seed.json"), "player_state_id", "player_state.seed.json"),
        run_states=index_by(load_json(seed_dir / "run_state.seed.json"), "run_state_id", "run_state.seed.json"),
    )


def main() -> None:
    registry = load_registry()
    print(f"Loaded {len(registry.items)} items")
    print(f"Loaded {len(registry.factions)} factions")
    print(f"Loaded {len(registry.loot_tables)} loot tables")
    print(f"Loaded {len(registry.entities)} entities")
    print(f"Loaded {len(registry.extractions)} extractions")
    print(f"Loaded {len(registry.run_states)} run states")


if __name__ == "__main__":
    main()
