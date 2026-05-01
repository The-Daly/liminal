#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "LDHUDTypes.h"
#include "LDPlayerCharacter.generated.h"

class ULDInventoryComponent;
class ULDSanityComponent;
class ULDRunStateComponent;
class ILDInteractable;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FLDInteractionPromptChangedSignature, const FText&, PromptText);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FLDHUDSnapshotChangedSignature, const FLDHUDSnapshot&, Snapshot);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FLDPlayerMessageSignature, const FText&, Message);

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

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Player")
    bool TryInteract();

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|HUD")
    FLDHUDSnapshot BuildHUDSnapshot() const;

    virtual void Tick(float DeltaSeconds) override;
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

    UPROPERTY(BlueprintAssignable, Category="Liminal Dominion|HUD")
    FLDInteractionPromptChangedSignature OnInteractionPromptChanged;

    UPROPERTY(BlueprintAssignable, Category="Liminal Dominion|HUD")
    FLDHUDSnapshotChangedSignature OnHUDSnapshotChanged;

    UPROPERTY(BlueprintAssignable, Category="Liminal Dominion|HUD")
    FLDPlayerMessageSignature OnPlayerMessage;

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

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Interaction")
    float InteractionRange = 350.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Interaction")
    TObjectPtr<AActor> FocusedInteractableActor;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Interaction")
    FText CurrentInteractionText;

    void MoveForward(float Value);
    void MoveRight(float Value);
    void Turn(float Value);
    void LookUp(float Value);
    void RefreshFocusedInteractable();
    void BroadcastHUDSnapshot();
};
