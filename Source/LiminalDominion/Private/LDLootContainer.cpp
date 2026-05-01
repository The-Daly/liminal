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

    // Prototype containers add one stackable item. DataTable-driven stack metadata comes next.
    return Player->GetCarriedInventory()->AddItem(LootItemId, 1, true, 999);
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
