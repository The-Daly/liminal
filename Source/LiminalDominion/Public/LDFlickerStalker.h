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

    virtual void Tick(float DeltaSeconds) override;
    virtual void BeginPlay() override;

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

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Entity")
    float PatrolSpeed = 180.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Entity")
    float ChaseSpeed = 420.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Entity")
    float LoseTargetRadius = 1800.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Entity")
    float AttackCooldownSeconds = 1.25f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Entity")
    TArray<TObjectPtr<AActor>> PatrolPoints;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Entity")
    ELDFlickerStalkerState State = ELDFlickerStalkerState::Patrol;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Entity")
    TObjectPtr<AActor> TargetActor;

    int32 CurrentPatrolIndex = 0;
    float AttackCooldownRemaining = 0.0f;

    void TickPatrol(float DeltaSeconds);
    void TickChase(float DeltaSeconds);
    void TickReturnToPatrol(float DeltaSeconds);
    void MoveToward(const FVector& Destination, float SpeedScale);
    AActor* FindPlayerTarget() const;
    FVector GetCurrentPatrolDestination() const;
    void TryAttackTarget();
};
