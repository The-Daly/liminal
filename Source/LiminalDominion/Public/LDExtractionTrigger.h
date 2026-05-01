#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "LDExtractionTrigger.generated.h"

class ULDInventoryComponent;

UCLASS()
class LIMINALDOMINION_API ALDExtractionTrigger : public AActor
{
    GENERATED_BODY()

public:
    ALDExtractionTrigger();

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Extraction")
    bool CanExtract(const ULDInventoryComponent* Inventory) const;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Extraction")
    FName GetExtractionId() const;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Extraction")
    FName ExtractionId = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Extraction")
    TArray<FName> RequiredItemIds;
};
