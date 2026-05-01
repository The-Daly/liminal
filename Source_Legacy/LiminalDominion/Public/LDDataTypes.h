#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "LDDataTypes.generated.h"

UENUM(BlueprintType)
enum class ELDItemRarity : uint8
{
    Common,
    Uncommon,
    Rare,
    VeryRare,
    RelicClass,
    Quest
};

UENUM(BlueprintType)
enum class ELDStorageType : uint8
{
    Carried,
    Personal,
    Shared
};

UENUM(BlueprintType)
enum class ELDExtractionAvailability : uint8
{
    Stable,
    Hidden,
    Conditional
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDItemRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FName ItemId;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FName Category;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    ELDItemRarity Rarity = ELDItemRarity::Common;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    bool bStackable = false;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 MaxStack = 1;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float Weight = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 ValueTickets = 0;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    bool bCanBeLostOnDeath = true;
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDInventoryStack
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FName ItemId = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Quantity = 0;
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDExtractionRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FName ExtractionId;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FName LevelId;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    ELDExtractionAvailability Availability = ELDExtractionAvailability::Stable;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    TArray<FName> RequiredItemIds;
};
