#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "LDPlayerCharacter.generated.h"

class ULDInventoryComponent;
class ULDSanityComponent;
class ULDRunStateComponent;

UCLASS()
class LIMINALDOMINION_API ALDPlayerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    ALDPlayerCharacter();

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Player")
    ULDInventoryComponent* GetCarriedInventory() const;

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Player")
    ULDInventoryComponent* GetPersonalStorage() const;

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Player")
    ULDSanityComponent* GetSanityComponent() const;

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Player")
    ULDRunStateComponent* GetRunStateComponent() const;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Player")
    void DebugKillPlayer();

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Player")
    bool GiveStarterLoadout(const TArray<FName>& ItemIds);

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Player")
    bool ConsumeAlmondWater();

protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Components")
    TObjectPtr<ULDInventoryComponent> CarriedInventory;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Components")
    TObjectPtr<ULDInventoryComponent> PersonalStorage;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Components")
    TObjectPtr<ULDSanityComponent> SanityComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Components")
    TObjectPtr<ULDRunStateComponent> RunStateComponent;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Items")
    FName AlmondWaterItemId = FName(TEXT("consumable_almond_water"));
};
