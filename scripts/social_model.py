#!/usr/bin/env python3
from item_registry import DataRegistry, RegistryError, load_registry


DEFAULT_SOCIAL_RULE_ID = "social_faction_safe_squads_v0"


def social_rule(registry: DataRegistry, rule_id: str = DEFAULT_SOCIAL_RULE_ID) -> dict:
    try:
        return registry.social_rules[rule_id]
    except KeyError as exc:
        raise RegistryError(f"Unknown social_rule_id: {rule_id}") from exc


def can_players_damage_each_other(
    registry: DataRegistry,
    attacker_faction_id: str,
    target_faction_id: str,
    same_squad: bool = False,
    rule_id: str = DEFAULT_SOCIAL_RULE_ID,
) -> bool:
    rule = social_rule(registry, rule_id)
    friendly_fire = rule["friendly_fire"]
    if same_squad:
        return bool(friendly_fire["same_squad_damage_enabled"])
    if attacker_faction_id == target_faction_id:
        return bool(friendly_fire["same_faction_damage_enabled"])
    return True


def can_form_squad(
    registry: DataRegistry,
    member_faction_ids: list[str],
    rule_id: str = DEFAULT_SOCIAL_RULE_ID,
) -> bool:
    rule = social_rule(registry, rule_id)
    if len(member_faction_ids) > rule["squad_rules"]["max_members"]:
        return False
    if not member_faction_ids:
        return False
    if rule["squad_rules"]["same_faction_only"] and len(set(member_faction_ids)) != 1:
        return False
    return all(faction_id in registry.factions for faction_id in member_faction_ids)


def radio_connects_squadmates(registry: DataRegistry, rule_id: str = DEFAULT_SOCIAL_RULE_ID) -> bool:
    rule = social_rule(registry, rule_id)
    return rule["radio_rules"]["connects_scope"] == "SquadOnly"


if __name__ == "__main__":
    loaded_registry = load_registry()
    rule = social_rule(loaded_registry)
    print(f"{rule['display_name']}: team kill enabled = {rule['friendly_fire']['team_kill_enabled']}")
