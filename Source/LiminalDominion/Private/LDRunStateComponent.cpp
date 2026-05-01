#include "LDRunStateComponent.h"
#include "LDInventoryComponent.h"

ULDRunStateComponent::ULDRunStateComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void ULDRunStateComponent::StartRun(FName NewRunStateId)
{
    RunStateId = NewRunStateId;
    RunResult = ELDRunResult::InProgress;
    bRunActive = true;
}

void ULDRunStateComponent::Extract()
{
    if (!bRunActive)
    {
        return;
    }

    RunResult = ELDRunResult::Extracted;
    bRunActive = false;
    OnRunEnded.Broadcast(RunResult);
}

void ULDRunStateComponent::Die(ULDInventoryComponent* CarriedInventory)
{
    if (!bRunActive)
    {
        return;
    }

    if (CarriedInventory)
    {
        CarriedInventory->ClearInventory();
    }

    RunResult = ELDRunResult::Dead;
    bRunActive = false;
    OnRunEnded.Broadcast(RunResult);
}

bool ULDRunStateComponent::IsRunActive() const
{
    return bRunActive;
}

ELDRunResult ULDRunStateComponent::GetRunResult() const
{
    return RunResult;
}

FName ULDRunStateComponent::GetRunStateId() const
{
    return RunStateId;
}
