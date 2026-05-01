#include "LDExtractionTrigger.h"
#include "LDInventoryComponent.h"

ALDExtractionTrigger::ALDExtractionTrigger()
{
    PrimaryActorTick.bCanEverTick = false;
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
