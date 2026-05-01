#include "LDFlickerStalker.h"

ALDFlickerStalker::ALDFlickerStalker()
{
    PrimaryActorTick.bCanEverTick = true;
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
