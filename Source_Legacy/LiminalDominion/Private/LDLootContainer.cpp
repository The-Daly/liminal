#include "LDLootContainer.h"
#include "LDInventoryComponent.h"
#include "LDPlayerCharacter.h"

ALDLootContainer::ALDLootContainer()
{
    PrimaryActorTick.bCanEverTick = false;
}

FText ALDLootContainer::GetInteractionText_Implementation() const
{
    return HasLoot() ? FText::FromString(TEXT("Search Container")) : FText::FromString(TEXT("Empty"));
}

bool ALDLootContainer::Interact_Implementation(AActor* InteractingActor)
{
    ALDPlayerCharacter* Player = Cast<ALDPlayerCharacter>(InteractingActor);
    if (!Player || !Player->GetCarriedInventory())
    {
        return false;
    }

    FName LootItemId;
    if (!TryTakeFirstLoot(LootItemId))
    {
        return false;
    }

    return Player->GetCarriedInventory()->AddItemFromData(LootItemId, 1);
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
