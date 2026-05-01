#pragma once

#include "CoreMinimal.h"
#include "LDDataTypes.h"
#include "LDRunStateComponent.h"
#include "LDHUDTypes.generated.h"

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDHUDSnapshot
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly)
    float Sanity = 100.0f;

    UPROPERTY(BlueprintReadOnly)
    bool bLowSanity = false;

    UPROPERTY(BlueprintReadOnly)
    TArray<FLDInventoryStack> CarriedStacks;

    UPROPERTY(BlueprintReadOnly)
    FText InteractionText;

    UPROPERTY(BlueprintReadOnly)
    bool bHasInteraction = false;

    UPROPERTY(BlueprintReadOnly)
    bool bRunActive = false;

    UPROPERTY(BlueprintReadOnly)
    ELDRunResult RunResult = ELDRunResult::InProgress;
};
