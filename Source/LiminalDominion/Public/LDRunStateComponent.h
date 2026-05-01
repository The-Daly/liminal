#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "LDRunStateComponent.generated.h"

class ULDInventoryComponent;

UENUM(BlueprintType)
enum class ELDRunResult : uint8
{
    InProgress,
    Extracted,
    Dead
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FLDRunEndedSignature, ELDRunResult, Result);

UCLASS(ClassGroup=(LiminalDominion), meta=(BlueprintSpawnableComponent))
class LIMINALDOMINION_API ULDRunStateComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    ULDRunStateComponent();

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Run")
    void StartRun(FName NewRunStateId);

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Run")
    void Extract();

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Run")
    void Die(ULDInventoryComponent* CarriedInventory);

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Run")
    bool IsRunActive() const;

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Run")
    ELDRunResult GetRunResult() const;

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Run")
    FName GetRunStateId() const;

    UPROPERTY(BlueprintAssignable, Category="Liminal Dominion|Run")
    FLDRunEndedSignature OnRunEnded;

protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Run")
    FName RunStateId = NAME_None;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Run")
    ELDRunResult RunResult = ELDRunResult::InProgress;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Run")
    bool bRunActive = false;
};
