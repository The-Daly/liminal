#!/usr/bin/env python3
from typing import Optional

from item_registry import DataRegistry, load_registry


def npcs_by_service(registry: DataRegistry, service: str) -> list[dict]:
    return [npc for npc in registry.npc_roster.values() if service in npc["services"]]


def hireable_security_npcs(registry: DataRegistry) -> list[dict]:
    return [npc for npc in registry.npc_roster.values() if npc["security_profile"]["can_be_hired"]]


def security_brokers(registry: DataRegistry) -> list[dict]:
    return [npc for npc in registry.npc_roster.values() if npc["security_profile"]["can_hire_security"]]


def faction_roster(registry: DataRegistry, faction_id: Optional[str]) -> list[dict]:
    return [npc for npc in registry.npc_roster.values() if npc["faction_id"] == faction_id]


if __name__ == "__main__":
    loaded_registry = load_registry()
    print(f"Master NPC roster: {len(loaded_registry.npc_roster)} entries")
    print(f"Hireable security: {len(hireable_security_npcs(loaded_registry))}")
