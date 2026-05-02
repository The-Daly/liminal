#!/usr/bin/env python3
import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "data" / "seed"
OUT_DIR = ROOT / "generated" / "unreal_datatables"

EXPORTS = {
    "items.seed.json": "DT_Items.csv",
    "factions.seed.json": "DT_Factions.csv",
    "loot_tables.seed.json": "DT_LootTables.csv",
    "entities.seed.json": "DT_Entities.csv",
    "storage.seed.json": "DT_Storage.csv",
    "sanity.seed.json": "DT_Sanity.csv",
    "extractions.seed.json": "DT_Extractions.csv",
    "hub_upgrades.seed.json": "DT_HubUpgrades.csv",
    "player_state.seed.json": "DT_PlayerState.csv",
    "run_state.seed.json": "DT_RunState.csv",
    "traders.seed.json": "DT_Traders.csv",
    "npcs.seed.json": "DT_NPCs.csv",
    "quests.seed.json": "DT_Quests.csv",
}

ROW_NAME_FIELDS = [
    "item_id",
    "faction_id",
    "loot_table_id",
    "entity_id",
    "storage_id",
    "sanity_rule_id",
    "extraction_id",
    "hub_upgrade_id",
    "player_state_id",
    "run_state_id",
    "trader_id",
    "npc_id",
    "quest_id",
]


def load_json(path: Path) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected list seed data: {path}")
    return data


def encode_cell(value: Any) -> Any:
    if isinstance(value, (list, dict)):
        return json.dumps(value, separators=(",", ":"))
    return value


def row_name(record: dict[str, Any]) -> str:
    for field in ROW_NAME_FIELDS:
        if field in record:
            return str(record[field])
    raise ValueError(f"Cannot infer Unreal row name for record: {record}")


def export_seed(seed_name: str, output_name: str) -> int:
    records = load_json(SEED_DIR / seed_name)
    fields = ["Name"]
    for record in records:
        for key in record:
            if key not in fields:
                fields.append(key)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / output_name
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for record in records:
            row = {"Name": row_name(record)}
            row.update({key: encode_cell(value) for key, value in record.items()})
            writer.writerow(row)
    return len(records)


def main() -> None:
    total = 0
    for seed_name, output_name in EXPORTS.items():
        count = export_seed(seed_name, output_name)
        print(f"Exported {output_name}: {count} rows")
        total += count
    print(f"SUCCESS: exported {total} rows to {OUT_DIR}")


if __name__ == "__main__":
    main()
