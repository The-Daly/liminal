#include "LDDeploymentGate.h"
#include "Kismet/GameplayStatics.h"
#include "LDPlayerCharacter.h"
#include "LDRunStateComponent.h"

ALDDeploymentGate::ALDDeploymentGate()
{
    PrimaryActorTick.bCanEverTick = false;
}

FText ALDDeploymentGate::GetInteractionText_Implementation() const
{
    return FText::FromString(TEXT("Deploy"));
}

bool ALDDeploymentGate::Interact_Implementation(AActor* InteractingActor)
{
    ALDPlayerCharacter* Player = Cast<ALDPlayerCharacter>(InteractingActor);
    if (!Player || !Player->GetRunStateComponent())
    {
        return false;
    }

    Player->GetRunStateComponent()->StartRun(RunStateId);

    if (bOpenLevelOnDeploy && !TargetLevelName.IsNone())
    {
        UGameplayStatics::OpenLevel(this, TargetLevelName);
    }

    return true;
}
