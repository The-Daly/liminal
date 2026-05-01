#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "LDInteractable.h"
#include "LDStorageActor.generated.h"

class ULDInventoryComponent;

UCLASS()
class LIMINALDOMINION_API ALDStorageActor : public AActor, public ILDInteractable
{
    GENERATED_BODY()

public:
    ALDStorageActor();

    virtual FText GetInteractionText_Implementation() const override;
    virtual bool Interact_Implementation(AActor* InteractingActor) override;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Storage")
    bool DepositFrom(ULDInventoryComponent* SourceInventory, FName ItemId, int32 Quantity);

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Storage")
    ULDInventoryComponent* GetStorageInventory() const;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Storage")
    FName StorageId = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Storage")
    bool bSafeFromDeath = true;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Storage")
    bool bRaidRisk = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Components")
    TObjectPtr<ULDInventoryComponent> StorageInventory;
};
