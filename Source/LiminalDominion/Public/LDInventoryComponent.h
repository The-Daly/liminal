#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "LDDataTypes.h"
#include "LDInventoryComponent.generated.h"

UCLASS(ClassGroup=(LiminalDominion), meta=(BlueprintSpawnableComponent))
class LIMINALDOMINION_API ULDInventoryComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    ULDInventoryComponent();

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Inventory")
    bool AddItem(FName ItemId, int32 Quantity, bool bStackable, int32 MaxStack);

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Inventory")
    bool RemoveItem(FName ItemId, int32 Quantity);

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Inventory")
    int32 GetQuantity(FName ItemId) const;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Inventory")
    void ClearInventory();

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Inventory")
    TArray<FLDInventoryStack> GetStacks() const;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Inventory")
    int32 MaxSlots = 12;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Inventory")
    TArray<FLDInventoryStack> Stacks;
};
