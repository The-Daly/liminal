#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "LDFlickerStalker.generated.h"

UENUM(BlueprintType)
enum class ELDFlickerStalkerState : uint8
{
    Patrol,
    Chase,
    Attack,
    ReturnToPatrol
};

UCLASS()
class LIMINALDOMINION_API ALDFlickerStalker : public ACharacter
{
    GENERATED_BODY()

public:
    ALDFlickerStalker();

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Entity")
    void SetState(ELDFlickerStalkerState NewState);

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Entity")
    ELDFlickerStalkerState GetState() const;

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Entity")
    bool IsPlayerInDetectionRange(const AActor* PlayerActor) const;

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Entity")
    bool IsPlayerInAttackRange(const AActor* PlayerActor) const;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Entity")
    float DetectionRadius = 1200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Entity")
    float AttackRange = 160.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Entity")
    ELDFlickerStalkerState State = ELDFlickerStalkerState::Patrol;
};
