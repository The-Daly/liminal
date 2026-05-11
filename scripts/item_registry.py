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
    traders: dict[str, dict[str, Any]]
    npcs: dict[str, dict[str, Any]]
    npc_roster: dict[str, dict[str, Any]]
    quests: dict[str, dict[str, Any]]
    weapons: dict[str, dict[str, Any]]
    ammo: dict[str, dict[str, Any]]
    crafting_recipes: dict[str, dict[str, Any]]
    containers: dict[str, dict[str, Any]]
    level_layouts: dict[str, dict[str, Any]]
    navigation_markers: dict[str, dict[str, Any]]
    noise_responses: dict[str, dict[str, Any]]
    loot_density: dict[str, dict[str, Any]]
    social_rules: dict[str, dict[str, Any]]
    server_realms: dict[str, dict[str, Any]]
    wipe_schedules: dict[str, dict[str, Any]]
    character_appearance: dict[str, dict[str, Any]]
    menu_routes: dict[str, dict[str, Any]]

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
        traders=index_by(load_json(seed_dir / "traders.seed.json"), "trader_id", "traders.seed.json"),
        npcs=index_by(load_json(seed_dir / "npcs.seed.json"), "npc_id", "npcs.seed.json"),
        npc_roster=index_by(load_json(seed_dir / "npc_roster.seed.json"), "npc_roster_id", "npc_roster.seed.json"),
        quests=index_by(load_json(seed_dir / "quests.seed.json"), "quest_id", "quests.seed.json"),
        weapons=index_by(load_json(seed_dir / "weapons.seed.json"), "weapon_id", "weapons.seed.json"),
        ammo=index_by(load_json(seed_dir / "ammo.seed.json"), "ammo_type_id", "ammo.seed.json"),
        crafting_recipes=index_by(load_json(seed_dir / "crafting_recipes.seed.json"), "recipe_id", "crafting_recipes.seed.json"),
        containers=index_by(load_json(seed_dir / "containers.seed.json"), "container_id", "containers.seed.json"),
        level_layouts=index_by(load_json(seed_dir / "level_layouts.seed.json"), "level_id", "level_layouts.seed.json"),
        navigation_markers=index_by(load_json(seed_dir / "navigation_markers.seed.json"), "marker_id", "navigation_markers.seed.json"),
        noise_responses=index_by(load_json(seed_dir / "noise_responses.seed.json"), "noise_response_id", "noise_responses.seed.json"),
        loot_density=index_by(load_json(seed_dir / "loot_density.seed.json"), "density_profile_id", "loot_density.seed.json"),
        social_rules=index_by(load_json(seed_dir / "social_rules.seed.json"), "social_rule_id", "social_rules.seed.json"),
        server_realms=index_by(load_json(seed_dir / "server_realms.seed.json"), "realm_id", "server_realms.seed.json"),
        wipe_schedules=index_by(load_json(seed_dir / "wipe_schedules.seed.json"), "wipe_schedule_id", "wipe_schedules.seed.json"),
        character_appearance=index_by(load_json(seed_dir / "character_appearance.seed.json"), "appearance_id", "character_appearance.seed.json"),
        menu_routes=index_by(load_json(seed_dir / "menu_routes.seed.json"), "menu_route_id", "menu_routes.seed.json"),
    )


def main() -> None:
    registry = load_registry()
    print(f"Loaded {len(registry.items)} items")
    print(f"Loaded {len(registry.factions)} factions")
    print(f"Loaded {len(registry.loot_tables)} loot tables")
    print(f"Loaded {len(registry.entities)} entities")
    print(f"Loaded {len(registry.extractions)} extractions")
    print(f"Loaded {len(registry.run_states)} run states")
    print(f"Loaded {len(registry.traders)} traders")
    print(f"Loaded {len(registry.npcs)} NPCs")
    print(f"Loaded {len(registry.npc_roster)} master NPC roster entries")
    print(f"Loaded {len(registry.quests)} quests")
    print(f"Loaded {len(registry.weapons)} weapons")
    print(f"Loaded {len(registry.ammo)} ammo types")
    print(f"Loaded {len(registry.crafting_recipes)} crafting recipes")
    print(f"Loaded {len(registry.containers)} containers")
    print(f"Loaded {len(registry.level_layouts)} level layouts")
    print(f"Loaded {len(registry.navigation_markers)} navigation markers")
    print(f"Loaded {len(registry.noise_responses)} noise response tables")
    print(f"Loaded {len(registry.loot_density)} loot density profiles")
    print(f"Loaded {len(registry.social_rules)} social rule sets")
    print(f"Loaded {len(registry.server_realms)} server realms")
    print(f"Loaded {len(registry.wipe_schedules)} wipe schedules")
    print(f"Loaded {len(registry.character_appearance)} character appearance presets")
    print(f"Loaded {len(registry.menu_routes)} menu routes")


if __name__ == "__main__":
    main()
