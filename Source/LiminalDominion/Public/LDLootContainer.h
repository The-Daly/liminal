#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "LDLootContainer.generated.h"

UCLASS()
class LIMINALDOMINION_API ALDLootContainer : public AActor
{
    GENERATED_BODY()

public:
    ALDLootContainer();

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Loot")
    bool TryTakeFirstLoot(FName& OutItemId);

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Loot")
    bool HasLoot() const;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Loot")
    FName LootTableId = FName(TEXT("loot_level1_basic"));

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Loot")
    TArray<FName> AvailableLootItemIds;
};
