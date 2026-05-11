#!/usr/bin/env python3
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "data" / "schemas"
SEED_DIR = ROOT / "data" / "seed"


def dependency_install_hint():
    requirements_path = ROOT / "requirements.txt"
    if sys.platform.startswith("win") and shutil.which("py"):
        if requirements_path.exists():
            return "py -3 -m pip install -r requirements.txt"
        return "py -3 -m pip install jsonschema"
    if requirements_path.exists():
        return f"\"{sys.executable}\" -m pip install -r \"{requirements_path}\""
    return f"\"{sys.executable}\" -m pip install jsonschema"


try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("Missing dependency: jsonschema")
    print("Install project dependencies with:")
    print(f"  {dependency_install_hint()}")
    sys.exit(1)

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
    "npc_roster.seed.json": "npc_roster.schema.json",
    "quests.seed.json": "quest.schema.json",
    "weapons.seed.json": "weapon.schema.json",
    "ammo.seed.json": "ammo.schema.json",
    "crafting_recipes.seed.json": "crafting_recipe.schema.json",
    "containers.seed.json": "container.schema.json",
    "level_layouts.seed.json": "level_layout.schema.json",
    "navigation_markers.seed.json": "navigation_marker.schema.json",
    "noise_responses.seed.json": "noise_response.schema.json",
    "loot_density.seed.json": "loot_density.schema.json",
    "social_rules.seed.json": "social_rule.schema.json",
    "server_realms.seed.json": "server_realm.schema.json",
    "wipe_schedules.seed.json": "wipe_schedule.schema.json",
    "character_appearance.seed.json": "character_appearance.schema.json",
    "menu_routes.seed.json": "menu_route.schema.json",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_json_path(parts):
    rendered = []
    for part in parts:
        if isinstance(part, int):
            rendered.append(f"[{part}]")
        else:
            rendered.append(f".{part}")
    return "".join(rendered)


def format_validation_error(seed_name, record_index, error):
    location = f"{seed_name}[{record_index}]"
    record_path = format_json_path(error.path)
    if record_path:
        location += record_path
    return f"{location} ({error.validator}): {error.message}"


def error_sort_key(error):
    return tuple(str(part) for part in error.path)


def validate_records(seed_name, schema, data):
    validator = Draft202012Validator(schema)
    records = data if isinstance(data, list) else [data]
    errors = []

    for index, record in enumerate(records):
        for error in sorted(validator.iter_errors(record), key=error_sort_key):
            errors.append(format_validation_error(seed_name, index, error))

    if errors:
        raise ValueError("\n".join(errors))

    return len(records)


def validate_file(seed_name, schema_name):
    seed_path = SEED_DIR / seed_name
    schema_path = SCHEMA_DIR / schema_name

    if not seed_path.exists():
        raise FileNotFoundError(f"Missing seed file: {seed_path}")
    if not schema_path.exists():
        raise FileNotFoundError(f"Missing schema file: {schema_path}")

    data = load_json(seed_path)
    schema = load_json(schema_path)
    return validate_records(seed_name, schema, data)

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
    npc_roster = load_json(SEED_DIR / "npc_roster.seed.json")
    quests = load_json(SEED_DIR / "quests.seed.json")
    weapons = load_json(SEED_DIR / "weapons.seed.json")
    ammo = load_json(SEED_DIR / "ammo.seed.json")
    recipes = load_json(SEED_DIR / "crafting_recipes.seed.json")
    containers = load_json(SEED_DIR / "containers.seed.json")
    level_layouts = load_json(SEED_DIR / "level_layouts.seed.json")
    navigation_markers = load_json(SEED_DIR / "navigation_markers.seed.json")
    noise_responses = load_json(SEED_DIR / "noise_responses.seed.json")
    loot_density = load_json(SEED_DIR / "loot_density.seed.json")
    server_realms = load_json(SEED_DIR / "server_realms.seed.json")
    wipe_schedules = load_json(SEED_DIR / "wipe_schedules.seed.json")
    character_appearance = load_json(SEED_DIR / "character_appearance.seed.json")
    menu_routes = load_json(SEED_DIR / "menu_routes.seed.json")

    item_ids = {item["item_id"] for item in items}
    faction_ids = {faction["faction_id"] for faction in factions}
    entity_ids = {entity["entity_id"] for entity in entities}
    storage_ids = {entry["storage_id"] for entry in storage}
    sanity_rule_ids = {entry["sanity_rule_id"] for entry in sanity}
    extraction_ids = {entry["extraction_id"] for entry in extractions}
    loot_table_ids = {entry["loot_table_id"] for entry in loot_tables}
    npc_ids = {entry["npc_id"] for entry in npcs}
    quest_ids = {entry["quest_id"] for entry in quests}
    weapon_ids = {entry["weapon_id"] for entry in weapons}
    ammo_type_ids = {entry["ammo_type_id"] for entry in ammo}
    density_profile_ids = {entry["density_profile_id"] for entry in loot_density}
    wipe_schedule_ids = {entry["wipe_schedule_id"] for entry in wipe_schedules}
    menu_route_ids = {entry["menu_route_id"] for entry in menu_routes}

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

    for npc in npc_roster:
        faction_id = npc.get("faction_id")
        if faction_id is not None and faction_id not in faction_ids:
            missing.append(f"NPC roster {npc['npc_roster_id']} references missing faction {faction_id}")

    for quest in quests:
        if quest["giver_npc_id"] not in npc_ids:
            missing.append(f"Quest {quest['quest_id']} references missing giver NPC {quest['giver_npc_id']}")
        for objective in quest.get("objectives", []):
            objective_item_id = objective.get("item_id")
            if objective_item_id is not None and objective_item_id not in item_ids:
                missing.append(f"Quest {quest['quest_id']} objective references missing item {objective_item_id}")
        for reward in quest.get("rewards", []):
            if reward["item_id"] not in item_ids:
                missing.append(f"Quest {quest['quest_id']} reward references missing item {reward['item_id']}")

    for weapon in weapons:
        if weapon["item_id"] not in item_ids:
            missing.append(f"Weapon {weapon['weapon_id']} references missing item {weapon['item_id']}")
        ammo_type_id = weapon.get("ammo_type_id")
        if ammo_type_id is not None and ammo_type_id not in ammo_type_ids:
            missing.append(f"Weapon {weapon['weapon_id']} references missing ammo type {ammo_type_id}")

    for ammo_entry in ammo:
        if ammo_entry["item_id"] not in item_ids:
            missing.append(f"Ammo {ammo_entry['ammo_type_id']} references missing item {ammo_entry['item_id']}")
        for weapon_id in ammo_entry.get("compatible_weapon_ids", []):
            if weapon_id not in weapon_ids:
                missing.append(f"Ammo {ammo_entry['ammo_type_id']} references missing weapon {weapon_id}")

    for recipe in recipes:
        for ingredient in recipe.get("ingredients", []):
            if ingredient["item_id"] not in item_ids:
                missing.append(f"Recipe {recipe['recipe_id']} ingredient references missing item {ingredient['item_id']}")
        for output in recipe.get("outputs", []):
            if output["item_id"] not in item_ids:
                missing.append(f"Recipe {recipe['recipe_id']} output references missing item {output['item_id']}")

    for container in containers:
        if container["loot_table_id"] not in loot_table_ids:
            missing.append(f"Container {container['container_id']} references missing loot table {container['loot_table_id']}")
        required_tool = container.get("required_tool_item_id")
        if required_tool is not None and required_tool not in item_ids:
            missing.append(f"Container {container['container_id']} references missing required tool {required_tool}")
        owner_faction_id = container.get("owner_faction_id")
        if owner_faction_id is not None and owner_faction_id not in faction_ids:
            missing.append(f"Container {container['container_id']} references missing owner faction {owner_faction_id}")
        density_profile_id = container.get("density_profile_id")
        if density_profile_id is not None and density_profile_id not in density_profile_ids:
            missing.append(f"Container {container['container_id']} references missing density profile {density_profile_id}")

    for layout in level_layouts:
        zone_ids = {zone["zone_id"] for zone in layout.get("zones", [])}
        for route in layout.get("routes", []):
            if route["from_zone_id"] not in zone_ids:
                missing.append(f"Level layout {layout['level_id']} route {route['route_id']} references missing from-zone {route['from_zone_id']}")
            if route["to_zone_id"] not in zone_ids:
                missing.append(f"Level layout {layout['level_id']} route {route['route_id']} references missing to-zone {route['to_zone_id']}")
            required_item = route.get("requires_item_id")
            if required_item is not None and required_item not in item_ids:
                missing.append(f"Level layout {layout['level_id']} route {route['route_id']} references missing required item {required_item}")
        for foothold in layout.get("faction_footholds", []):
            if foothold["faction_id"] not in faction_ids:
                missing.append(f"Level layout {layout['level_id']} references missing faction {foothold['faction_id']}")
            if foothold["zone_id"] not in zone_ids:
                missing.append(f"Level layout {layout['level_id']} foothold references missing zone {foothold['zone_id']}")

    for marker in navigation_markers:
        if marker["item_id"] not in item_ids:
            missing.append(f"Navigation marker {marker['marker_id']} references missing item {marker['item_id']}")

    for response_table in noise_responses:
        for response in response_table.get("responses", []):
            entity_id = response.get("entity_id")
            if entity_id is not None and entity_id not in entity_ids:
                missing.append(f"Noise response {response_table['noise_response_id']} references missing entity {entity_id}")

    for realm in server_realms:
        if realm["wipe_schedule_id"] not in wipe_schedule_ids:
            missing.append(f"Server realm {realm['realm_id']} references missing wipe schedule {realm['wipe_schedule_id']}")
        for faction_cap in realm.get("faction_caps", []):
            if faction_cap["faction_id"] not in faction_ids:
                missing.append(f"Server realm {realm['realm_id']} references missing faction {faction_cap['faction_id']}")

    for appearance in character_appearance:
        if appearance["faction_id"] not in faction_ids:
            missing.append(f"Character appearance {appearance['appearance_id']} references missing faction {appearance['faction_id']}")
        starter_item = appearance.get("identity_item_id")
        if starter_item is not None and starter_item not in item_ids:
            missing.append(f"Character appearance {appearance['appearance_id']} references missing identity item {starter_item}")

    for route in menu_routes:
        for next_route_id in route.get("next_route_ids", []):
            if next_route_id not in menu_route_ids:
                missing.append(f"Menu route {route['menu_route_id']} references missing next route {next_route_id}")

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
    check_duplicate_ids("npc_roster.seed.json", "npc_roster_id")
    check_duplicate_ids("quests.seed.json", "quest_id")
    check_duplicate_ids("weapons.seed.json", "weapon_id")
    check_duplicate_ids("ammo.seed.json", "ammo_type_id")
    check_duplicate_ids("crafting_recipes.seed.json", "recipe_id")
    check_duplicate_ids("containers.seed.json", "container_id")
    check_duplicate_ids("level_layouts.seed.json", "level_id")
    check_duplicate_ids("navigation_markers.seed.json", "marker_id")
    check_duplicate_ids("noise_responses.seed.json", "noise_response_id")
    check_duplicate_ids("loot_density.seed.json", "density_profile_id")
    check_duplicate_ids("social_rules.seed.json", "social_rule_id")
    check_duplicate_ids("server_realms.seed.json", "realm_id")
    check_duplicate_ids("wipe_schedules.seed.json", "wipe_schedule_id")
    check_duplicate_ids("character_appearance.seed.json", "appearance_id")
    check_duplicate_ids("menu_routes.seed.json", "menu_route_id")
    check_references()

    print(f"SUCCESS: validated {total} records.")

if __name__ == "__main__":
    main()
