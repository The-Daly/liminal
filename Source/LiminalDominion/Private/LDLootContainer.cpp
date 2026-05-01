#include "LDLootContainer.h"

ALDLootContainer::ALDLootContainer()
{
    PrimaryActorTick.bCanEverTick = false;
}

bool ALDLootContainer::TryTakeFirstLoot(FName& OutItemId)
{
    if (AvailableLootItemIds.Num() == 0)
    {
        OutItemId = NAME_None;
        return false;
    }

    OutItemId = AvailableLootItemIds[0];
    AvailableLootItemIds.RemoveAt(0);
    return true;
}

bool ALDLootContainer::HasLoot() const
{
    return AvailableLootItemIds.Num() > 0;
}
