#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "LDDataTypes.h"
#include "LDSaveGame.generated.h"

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDStoredContainerState
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FName ContainerId = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FLDInventoryStack> Stacks;
};

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDRunHistoryEntry
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FName RunStateId = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FName Result = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 TicketsExtracted = 0;
};

UCLASS()
class LIMINALDOMINION_API ULDSaveGame : public USaveGame
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Save")
    int32 SaveVersion = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Save")
    FName FactionId = FName(TEXT("meg"));

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Save")
    FLDStoredContainerState PersonalStorage;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Save")
    TArray<FName> CompletedHubUpgradeIds;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Save")
    TArray<FLDRunHistoryEntry> RunHistory;
};
