#include "LDProjectBoardActor.h"
#include "Engine/GameInstance.h"
#include "LDInventoryComponent.h"
#include "LDSaveGameSubsystem.h"

ALDProjectBoardActor::ALDProjectBoardActor()
{
    PrimaryActorTick.bCanEverTick = false;
}

FText ALDProjectBoardActor::GetInteractionText_Implementation() const
{
    return bComplete ? FText::FromString(TEXT("Project Complete")) : FText::FromString(TEXT("Contribute to Project"));
}

bool ALDProjectBoardActor::Interact_Implementation(AActor* InteractingActor)
{
    return InteractingActor != nullptr;
}

bool ALDProjectBoardActor::CanContribute(const ULDInventoryComponent* SourceInventory) const
{
    if (!SourceInventory || bComplete)
    {
        return false;
    }

    for (const FLDContributionRequirement& Requirement : Requirements)
    {
        if (Requirement.ItemId.IsNone() || Requirement.Quantity <= 0)
        {
            return false;
        }

        if (SourceInventory->GetQuantity(Requirement.ItemId) < Requirement.Quantity)
        {
            return false;
        }
    }

    return Requirements.Num() > 0;
}

bool ALDProjectBoardActor::Contribute(ULDInventoryComponent* SourceInventory)
{
    if (!CanContribute(SourceInventory))
    {
        return false;
    }

    for (const FLDContributionRequirement& Requirement : Requirements)
    {
        if (!SourceInventory->RemoveItem(Requirement.ItemId, Requirement.Quantity))
        {
            return false;
        }
    }

    bComplete = true;
    if (UGameInstance* GameInstance = GetWorld() ? GetWorld()->GetGameInstance() : nullptr)
    {
        if (ULDSaveGameSubsystem* SaveSubsystem = GameInstance->GetSubsystem<ULDSaveGameSubsystem>())
        {
            SaveSubsystem->MarkHubUpgradeComplete(HubUpgradeId);
        }
    }
    return true;
}

bool ALDProjectBoardActor::IsComplete() const
{
    return bComplete;
}

void ALDProjectBoardActor::LoadCompletionFromSave()
{
    if (UGameInstance* GameInstance = GetWorld() ? GetWorld()->GetGameInstance() : nullptr)
    {
        if (const ULDSaveGameSubsystem* SaveSubsystem = GameInstance->GetSubsystem<ULDSaveGameSubsystem>())
        {
            bComplete = SaveSubsystem->IsHubUpgradeComplete(HubUpgradeId);
        }
    }
}
