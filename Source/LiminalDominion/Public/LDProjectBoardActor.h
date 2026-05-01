#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "LDInteractable.h"
#include "LDProjectBoardActor.generated.h"

class ULDInventoryComponent;

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDContributionRequirement
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FName ItemId = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Quantity = 1;
};

UCLASS()
class LIMINALDOMINION_API ALDProjectBoardActor : public AActor, public ILDInteractable
{
    GENERATED_BODY()

public:
    ALDProjectBoardActor();

    virtual FText GetInteractionText_Implementation() const override;
    virtual bool Interact_Implementation(AActor* InteractingActor) override;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Progression")
    bool CanContribute(const ULDInventoryComponent* SourceInventory) const;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Progression")
    bool Contribute(ULDInventoryComponent* SourceInventory);

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Progression")
    bool IsComplete() const;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Progression")
    FName HubUpgradeId = FName(TEXT("hub_project_board_signal_lamp_v0"));

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Progression")
    TArray<FLDContributionRequirement> Requirements;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Progression")
    bool bComplete = false;
};
