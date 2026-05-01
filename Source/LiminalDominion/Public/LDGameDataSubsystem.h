#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "LDDataTypes.h"
#include "LDGameDataSubsystem.generated.h"

class UDataTable;

USTRUCT(BlueprintType)
struct LIMINALDOMINION_API FLDItemStackRule
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly)
    bool bFound = false;

    UPROPERTY(BlueprintReadOnly)
    bool bStackable = false;

    UPROPERTY(BlueprintReadOnly)
    int32 MaxStack = 1;
};

UCLASS(Config=Game)
class LIMINALDOMINION_API ULDGameDataSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Data")
    void SetItemDataTable(UDataTable* InItemDataTable);

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Data")
    const FLDItemRow* FindItemRow(FName ItemId) const;

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Data")
    FLDItemStackRule GetItemStackRule(FName ItemId) const;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Data")
    TObjectPtr<UDataTable> ItemDataTable;

    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category="Data")
    FSoftObjectPath ItemDataTablePath;
};
