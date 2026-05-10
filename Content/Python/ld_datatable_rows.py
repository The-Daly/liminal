import unreal


@unreal.ustruct()
class LDItemRow(unreal.TableRowBase):
    item_id = unreal.uproperty(str)
    display_name = unreal.uproperty(str)
    category = unreal.uproperty(str)
    rarity = unreal.uproperty(str)
    stackable = unreal.uproperty(bool)
    max_stack = unreal.uproperty(int)
    weight = unreal.uproperty(float)
    value_tickets = unreal.uproperty(int)
    can_be_lost_on_death = unreal.uproperty(bool)
    can_display_in_room = unreal.uproperty(bool)
    display_location = unreal.uproperty(str)
    faction_restriction = unreal.uproperty(str)
    description = unreal.uproperty(str)


@unreal.ustruct()
class LDLootTableRow(unreal.TableRowBase):
    loot_table_id = unreal.uproperty(str)
    entries = unreal.uproperty(str)


@unreal.ustruct()
class LDExtractionRow(unreal.TableRowBase):
    extraction_id = unreal.uproperty(str)
    display_name = unreal.uproperty(str)
    level_id = unreal.uproperty(str)
    transition_pattern = unreal.uproperty(str)
    availability = unreal.uproperty(str)
    required_item_ids = unreal.uproperty(str)
    description = unreal.uproperty(str)


@unreal.ustruct()
class LDStorageRow(unreal.TableRowBase):
    storage_id = unreal.uproperty(str)
    display_name = unreal.uproperty(str)
    storage_type = unreal.uproperty(str)
    safe_from_death = unreal.uproperty(bool)
    raid_risk = unreal.uproperty(bool)
    caps = unreal.uproperty(str)
    description = unreal.uproperty(str)


@unreal.ustruct()
class LDSanityRow(unreal.TableRowBase):
    sanity_rule_id = unreal.uproperty(str)
    display_name = unreal.uproperty(str)
    min_sanity = unreal.uproperty(float)
    max_sanity = unreal.uproperty(float)
    base_drain_per_minute = unreal.uproperty(float)
    low_sanity_threshold = unreal.uproperty(float)
    almond_water_restore = unreal.uproperty(float)
    description = unreal.uproperty(str)


@unreal.ustruct()
class LDHubUpgradeRow(unreal.TableRowBase):
    hub_upgrade_id = unreal.uproperty(str)
    display_name = unreal.uproperty(str)
    faction_id = unreal.uproperty(str)
    contribution_requirements = unreal.uproperty(str)
    visible_unlock = unreal.uproperty(str)
    description = unreal.uproperty(str)


@unreal.ustruct()
class LDPlayerStateRow(unreal.TableRowBase):
    player_state_id = unreal.uproperty(str)
    faction_id = unreal.uproperty(str)
    carried_storage_id = unreal.uproperty(str)
    personal_storage_id = unreal.uproperty(str)
    starting_sanity = unreal.uproperty(float)
    description = unreal.uproperty(str)


@unreal.ustruct()
class LDRunStateRow(unreal.TableRowBase):
    run_state_id = unreal.uproperty(str)
    level_id = unreal.uproperty(str)
    loot_table_id = unreal.uproperty(str)
    entity_ids = unreal.uproperty(str)
    extraction_ids = unreal.uproperty(str)
    sanity_rule_id = unreal.uproperty(str)
    description = unreal.uproperty(str)


ROW_STRUCTS = {
    "DT_Items": LDItemRow,
    "DT_LootTables": LDLootTableRow,
    "DT_Extractions": LDExtractionRow,
    "DT_Storage": LDStorageRow,
    "DT_Sanity": LDSanityRow,
    "DT_HubUpgrades": LDHubUpgradeRow,
    "DT_PlayerState": LDPlayerStateRow,
    "DT_RunState": LDRunStateRow,
}
