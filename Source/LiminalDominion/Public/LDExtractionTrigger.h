#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "LDInteractable.h"
#include "LDExtractionTrigger.generated.h"

class ULDInventoryComponent;

UCLASS()
class LIMINALDOMINION_API ALDExtractionTrigger : public AActor, public ILDInteractable
{
    GENERATED_BODY()

public:
    ALDExtractionTrigger();

    virtual FText GetInteractionText_Implementation() const override;
    virtual bool Interact_Implementation(AActor* InteractingActor) override;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Extraction")
    bool CanExtract(const ULDInventoryComponent* Inventory) const;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Extraction")
    FName GetExtractionId() const;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Extraction")
    FName ExtractionId = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Extraction")
    TArray<FName> RequiredItemIds;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Extraction")
    FName DestinationLevelName = FName(TEXT("LD_PersonalRoom_Greybox"));

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Extraction")
    bool bOpenLevelOnExtract = true;
};
