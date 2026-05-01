#include "LDFlickerStalker.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"
#include "LDPlayerCharacter.h"

ALDFlickerStalker::ALDFlickerStalker()
{
    PrimaryActorTick.bCanEverTick = true;
}

void ALDFlickerStalker::BeginPlay()
{
    Super::BeginPlay();

    if (UCharacterMovementComponent* Movement = GetCharacterMovement())
    {
        Movement->MaxWalkSpeed = PatrolSpeed;
    }
}

void ALDFlickerStalker::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);

    AttackCooldownRemaining = FMath::Max(0.0f, AttackCooldownRemaining - DeltaSeconds);

    switch (State)
    {
    case ELDFlickerStalkerState::Patrol:
        TickPatrol(DeltaSeconds);
        break;
    case ELDFlickerStalkerState::Chase:
        TickChase(DeltaSeconds);
        break;
    case ELDFlickerStalkerState::Attack:
        TryAttackTarget();
        break;
    case ELDFlickerStalkerState::ReturnToPatrol:
        TickReturnToPatrol(DeltaSeconds);
        break;
    default:
        break;
    }
}

void ALDFlickerStalker::SetState(ELDFlickerStalkerState NewState)
{
    State = NewState;
}

ELDFlickerStalkerState ALDFlickerStalker::GetState() const
{
    return State;
}

bool ALDFlickerStalker::IsPlayerInDetectionRange(const AActor* PlayerActor) const
{
    return PlayerActor && FVector::DistSquared(GetActorLocation(), PlayerActor->GetActorLocation()) <= FMath::Square(DetectionRadius);
}

bool ALDFlickerStalker::IsPlayerInAttackRange(const AActor* PlayerActor) const
{
    return PlayerActor && FVector::DistSquared(GetActorLocation(), PlayerActor->GetActorLocation()) <= FMath::Square(AttackRange);
}

void ALDFlickerStalker::TickPatrol(float)
{
    TargetActor = FindPlayerTarget();
    if (TargetActor)
    {
        SetState(ELDFlickerStalkerState::Chase);
        return;
    }

    if (PatrolPoints.Num() > 0)
    {
        const FVector Destination = GetCurrentPatrolDestination();
        MoveToward(Destination, PatrolSpeed);
        if (FVector::DistSquared(GetActorLocation(), Destination) <= FMath::Square(120.0f))
        {
            CurrentPatrolIndex = (CurrentPatrolIndex + 1) % PatrolPoints.Num();
        }
    }
}

void ALDFlickerStalker::TickChase(float)
{
    if (!TargetActor || FVector::DistSquared(GetActorLocation(), TargetActor->GetActorLocation()) > FMath::Square(LoseTargetRadius))
    {
        TargetActor = nullptr;
        SetState(ELDFlickerStalkerState::ReturnToPatrol);
        return;
    }

    if (IsPlayerInAttackRange(TargetActor))
    {
        SetState(ELDFlickerStalkerState::Attack);
        TryAttackTarget();
        return;
    }

    MoveToward(TargetActor->GetActorLocation(), ChaseSpeed);
}

void ALDFlickerStalker::TickReturnToPatrol(float)
{
    TargetActor = FindPlayerTarget();
    if (TargetActor)
    {
        SetState(ELDFlickerStalkerState::Chase);
        return;
    }

    if (PatrolPoints.Num() == 0)
    {
        SetState(ELDFlickerStalkerState::Patrol);
        return;
    }

    const FVector Destination = GetCurrentPatrolDestination();
    MoveToward(Destination, PatrolSpeed);
    if (FVector::DistSquared(GetActorLocation(), Destination) <= FMath::Square(120.0f))
    {
        SetState(ELDFlickerStalkerState::Patrol);
    }
}

void ALDFlickerStalker::MoveToward(const FVector& Destination, float Speed)
{
    if (UCharacterMovementComponent* Movement = GetCharacterMovement())
    {
        Movement->MaxWalkSpeed = Speed;
    }

    const FVector Direction = Destination - GetActorLocation();
    if (!Direction.IsNearlyZero())
    {
        AddMovementInput(Direction.GetSafeNormal());
    }
}

AActor* ALDFlickerStalker::FindPlayerTarget() const
{
    ACharacter* PlayerCharacter = UGameplayStatics::GetPlayerCharacter(this, 0);
    return IsPlayerInDetectionRange(PlayerCharacter) ? PlayerCharacter : nullptr;
}

FVector ALDFlickerStalker::GetCurrentPatrolDestination() const
{
    if (PatrolPoints.Num() == 0 || !PatrolPoints.IsValidIndex(CurrentPatrolIndex) || !PatrolPoints[CurrentPatrolIndex])
    {
        return GetActorLocation();
    }

    return PatrolPoints[CurrentPatrolIndex]->GetActorLocation();
}

void ALDFlickerStalker::TryAttackTarget()
{
    if (!TargetActor)
    {
        SetState(ELDFlickerStalkerState::ReturnToPatrol);
        return;
    }

    if (!IsPlayerInAttackRange(TargetActor))
    {
        SetState(ELDFlickerStalkerState::Chase);
        return;
    }

    if (AttackCooldownRemaining > 0.0f)
    {
        return;
    }

    if (ALDPlayerCharacter* Player = Cast<ALDPlayerCharacter>(TargetActor))
    {
        Player->DebugKillPlayer();
    }

    AttackCooldownRemaining = AttackCooldownSeconds;
}
