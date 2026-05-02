#!/usr/bin/env python3
import json
from pathlib import Path
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("Missing dependency: jsonschema")
    print("Install with: python3 -m pip install jsonschema")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "data" / "schemas"
SEED_DIR = ROOT / "data" / "seed"

PAIRINGS = {
    "items.seed.json": "item.schema.json",
    "factions.seed.json": "faction.schema.json",
    "entities.seed.json": "entity.schema.json",
    "loot_tables.seed.json": "loot_table.schema.json",
    "storage.seed.json": "storage.schema.json",
    "sanity.seed.json": "sanity.schema.json",
    "extractions.seed.json": "extraction.schema.json",
    "hub_upgrades.seed.json": "hub_upgrade.schema.json",
    "player_state.seed.json": "player_state.schema.json",
    "run_state.seed.json": "run_state.schema.json",
    "traders.seed.json": "trader.schema.json",
    "npcs.seed.json": "npc.schema.json",
    "quests.seed.json": "quest.schema.json",
}

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_file(seed_name, schema_name):
    seed_path = SEED_DIR / seed_name
    schema_path = SCHEMA_DIR / schema_name

    if not seed_path.exists():
        raise FileNotFoundError(f"Missing seed file: {seed_path}")
    if not schema_path.exists():
        raise FileNotFoundError(f"Missing schema file: {schema_path}")

    data = load_json(seed_path)
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)

    errors = []
    records = data if isinstance(data, list) else [data]
    for i, record in enumerate(records):
        for error in sorted(validator.iter_errors(record), key=lambda e: e.path):
            errors.append(f"{seed_name}[{i}]: {error.message}")

    if errors:
        raise ValueError("\\n".join(errors))

    return len(records)

def check_duplicate_ids(seed_name, id_field):
    data = load_json(SEED_DIR / seed_name)
    seen = set()
    dupes = []
    for record in data:
        rid = record.get(id_field)
        if rid in seen:
            dupes.append(rid)
        seen.add(rid)
    if dupes:
        raise ValueError(f"Duplicate IDs in {seed_name}: {dupes}")

def check_references():
    items = load_json(SEED_DIR / "items.seed.json")
    factions = load_json(SEED_DIR / "factions.seed.json")
    loot_tables = load_json(SEED_DIR / "loot_tables.seed.json")
    entities = load_json(SEED_DIR / "entities.seed.json")
    storage = load_json(SEED_DIR / "storage.seed.json")
    sanity = load_json(SEED_DIR / "sanity.seed.json")
    extractions = load_json(SEED_DIR / "extractions.seed.json")
    hub_upgrades = load_json(SEED_DIR / "hub_upgrades.seed.json")
    player_states = load_json(SEED_DIR / "player_state.seed.json")
    run_states = load_json(SEED_DIR / "run_state.seed.json")
    traders = load_json(SEED_DIR / "traders.seed.json")
    npcs = load_json(SEED_DIR / "npcs.seed.json")
    quests = load_json(SEED_DIR / "quests.seed.json")

    item_ids = {item["item_id"] for item in items}
    faction_ids = {faction["faction_id"] for faction in factions}
    entity_ids = {entity["entity_id"] for entity in entities}
    storage_ids = {entry["storage_id"] for entry in storage}
    sanity_rule_ids = {entry["sanity_rule_id"] for entry in sanity}
    extraction_ids = {entry["extraction_id"] for entry in extractions}
    loot_table_ids = {entry["loot_table_id"] for entry in loot_tables}
    npc_ids = {entry["npc_id"] for entry in npcs}
    quest_ids = {entry["quest_id"] for entry in quests}

    missing = []

    for faction in factions:
        for item_id in faction.get("starting_items", []):
            if item_id not in item_ids:
                missing.append(f"Faction {faction['faction_id']} references missing item {item_id}")

    for table in loot_tables:
        for entry in table.get("entries", []):
            if entry["item_id"] not in item_ids:
                missing.append(f"Loot table {table['loot_table_id']} references missing item {entry['item_id']}")

    for extraction in extractions:
        for item_id in extraction.get("required_item_ids", []):
            if item_id not in item_ids:
                missing.append(f"Extraction {extraction['extraction_id']} references missing item {item_id}")

    for upgrade in hub_upgrades:
        if upgrade["faction_id"] not in faction_ids:
            missing.append(f"Hub upgrade {upgrade['hub_upgrade_id']} references missing faction {upgrade['faction_id']}")
        for requirement in upgrade.get("contribution_requirements", []):
            if requirement["item_id"] not in item_ids:
                missing.append(f"Hub upgrade {upgrade['hub_upgrade_id']} references missing item {requirement['item_id']}")

    for player_state in player_states:
        if player_state["faction_id"] not in faction_ids:
            missing.append(f"Player state {player_state['player_state_id']} references missing faction {player_state['faction_id']}")
        if player_state["carried_storage_id"] not in storage_ids:
            missing.append(f"Player state {player_state['player_state_id']} references missing carried storage {player_state['carried_storage_id']}")
        if player_state["personal_storage_id"] not in storage_ids:
            missing.append(f"Player state {player_state['player_state_id']} references missing personal storage {player_state['personal_storage_id']}")

    for run_state in run_states:
        if run_state["loot_table_id"] not in loot_table_ids:
            missing.append(f"Run state {run_state['run_state_id']} references missing loot table {run_state['loot_table_id']}")
        if run_state["sanity_rule_id"] not in sanity_rule_ids:
            missing.append(f"Run state {run_state['run_state_id']} references missing sanity rule {run_state['sanity_rule_id']}")
        for entity_id in run_state.get("entity_ids", []):
            if entity_id not in entity_ids:
                missing.append(f"Run state {run_state['run_state_id']} references missing entity {entity_id}")
        for extraction_id in run_state.get("extraction_ids", []):
            if extraction_id not in extraction_ids:
                missing.append(f"Run state {run_state['run_state_id']} references missing extraction {extraction_id}")

    for trader in traders:
        for stock in trader.get("stock", []):
            if stock["item_id"] not in item_ids:
                missing.append(f"Trader {trader['trader_id']} references missing stock item {stock['item_id']}")

    for npc in npcs:
        for quest_id in npc.get("quest_ids", []):
            if quest_id not in quest_ids:
                missing.append(f"NPC {npc['npc_id']} references missing quest {quest_id}")

    for quest in quests:
        if quest["giver_npc_id"] not in npc_ids:
            missing.append(f"Quest {quest['quest_id']} references missing giver NPC {quest['giver_npc_id']}")
        for objective in quest.get("objectives", []):
            if objective["item_id"] not in item_ids:
                missing.append(f"Quest {quest['quest_id']} objective references missing item {objective['item_id']}")
        for reward in quest.get("rewards", []):
            if reward["item_id"] not in item_ids:
                missing.append(f"Quest {quest['quest_id']} reward references missing item {reward['item_id']}")

    if missing:
        raise ValueError("\\n".join(missing))

def main():
    total = 0
    for seed_name, schema_name in PAIRINGS.items():
        count = validate_file(seed_name, schema_name)
        print(f"OK: {seed_name} ({count} records)")
        total += count

    check_duplicate_ids("items.seed.json", "item_id")
    check_duplicate_ids("factions.seed.json", "faction_id")
    check_duplicate_ids("entities.seed.json", "entity_id")
    check_duplicate_ids("loot_tables.seed.json", "loot_table_id")
    check_duplicate_ids("storage.seed.json", "storage_id")
    check_duplicate_ids("sanity.seed.json", "sanity_rule_id")
    check_duplicate_ids("extractions.seed.json", "extraction_id")
    check_duplicate_ids("hub_upgrades.seed.json", "hub_upgrade_id")
    check_duplicate_ids("player_state.seed.json", "player_state_id")
    check_duplicate_ids("run_state.seed.json", "run_state_id")
    check_duplicate_ids("traders.seed.json", "trader_id")
    check_duplicate_ids("npcs.seed.json", "npc_id")
    check_duplicate_ids("quests.seed.json", "quest_id")
    check_references()

    print(f"SUCCESS: validated {total} records.")

if __name__ == "__main__":
    main()
