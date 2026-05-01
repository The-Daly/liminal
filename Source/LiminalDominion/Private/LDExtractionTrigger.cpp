#include "LDExtractionTrigger.h"
#include "LDInventoryComponent.h"
#include "LDPlayerCharacter.h"
#include "LDRunStateComponent.h"

ALDExtractionTrigger::ALDExtractionTrigger()
{
    PrimaryActorTick.bCanEverTick = false;
}

FText ALDExtractionTrigger::GetInteractionText_Implementation() const
{
    return FText::FromString(TEXT("Extract"));
}

bool ALDExtractionTrigger::Interact_Implementation(AActor* InteractingActor)
{
    ALDPlayerCharacter* Player = Cast<ALDPlayerCharacter>(InteractingActor);
    if (!Player || !CanExtract(Player->GetCarriedInventory()) || !Player->GetRunStateComponent())
    {
        return false;
    }

    Player->GetRunStateComponent()->Extract();
    return true;
}

bool ALDExtractionTrigger::CanExtract(const ULDInventoryComponent* Inventory) const
{
    if (!Inventory)
    {
        return false;
    }

    for (const FName RequiredItemId : RequiredItemIds)
    {
        if (Inventory->GetQuantity(RequiredItemId) <= 0)
        {
            return false;
        }
    }

    return true;
}

FName ALDExtractionTrigger::GetExtractionId() const
{
    return ExtractionId;
}
