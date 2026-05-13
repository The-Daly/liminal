#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "LDNativeDataRows.generated.h"

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDItemRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString item_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString display_name;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString category;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString rarity;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    bool stackable = false;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 max_stack = 1;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float weight = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 value_tickets = 0;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    bool can_be_lost_on_death = true;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    bool can_display_in_room = false;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString display_location;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString faction_restriction;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString description;
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDFactionRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString faction_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString display_name;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString role;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString starting_items;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString hub_upgrade_focus;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString description;
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDLootTableRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString loot_table_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString entries;
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDExtractionRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString extraction_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString display_name;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString level_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString transition_pattern;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString availability;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString required_item_ids;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString description;
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDStorageRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString storage_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString display_name;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString storage_type;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    bool safe_from_death = false;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    bool raid_risk = false;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString caps;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString description;
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDSanityRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString sanity_rule_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString display_name;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float min_sanity = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float max_sanity = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float base_drain_per_minute = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float low_sanity_threshold = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float almond_water_restore = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString description;
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDHubUpgradeRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString hub_upgrade_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString display_name;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString faction_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString contribution_requirements;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString visible_unlock;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString description;
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDPlayerStateRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString player_state_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString faction_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString carried_storage_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString personal_storage_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float starting_sanity = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString description;
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDRunStateRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString run_state_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString level_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString loot_table_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString entity_ids;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString extraction_ids;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString sanity_rule_id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString description;
};
