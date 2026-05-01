#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "LDInteractable.generated.h"

UINTERFACE(BlueprintType)
class LIMINALDOMINION_API ULDInteractable : public UInterface
{
    GENERATED_BODY()
};

class LIMINALDOMINION_API ILDInteractable
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, BlueprintNativeEvent, Category="Liminal Dominion|Interaction")
    FText GetInteractionText() const;

    UFUNCTION(BlueprintCallable, BlueprintNativeEvent, Category="Liminal Dominion|Interaction")
    bool Interact(AActor* InteractingActor);
};
