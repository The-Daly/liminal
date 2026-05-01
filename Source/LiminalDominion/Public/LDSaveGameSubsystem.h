#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "LDDataTypes.h"
#include "LDSaveGameSubsystem.generated.h"

class ULDSaveGame;

UCLASS(Config=Game)
class LIMINALDOMINION_API ULDSaveGameSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Save")
    ULDSaveGame* LoadOrCreateSave();

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Save")
    bool SaveCurrentGame();

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Save")
    void SetFactionId(FName FactionId);

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Save")
    FName GetFactionId() const;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Save")
    void SavePersonalStorage(const TArray<FLDInventoryStack>& Stacks);

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Save")
    TArray<FLDInventoryStack> GetPersonalStorageStacks() const;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Save")
    void MarkHubUpgradeComplete(FName HubUpgradeId);

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Save")
    bool IsHubUpgradeComplete(FName HubUpgradeId) const;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Save")
    void AddRunHistoryEntry(FName RunStateId, FName Result, int32 TicketsExtracted);

protected:
    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category="Save")
    FString SaveSlotName = TEXT("LiminalDominionV0");

    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category="Save")
    int32 UserIndex = 0;

    UPROPERTY(Transient)
    TObjectPtr<ULDSaveGame> CurrentSave;
};
