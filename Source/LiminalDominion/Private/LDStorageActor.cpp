#include "LDStorageActor.h"
#include "LDInventoryComponent.h"

ALDStorageActor::ALDStorageActor()
{
    PrimaryActorTick.bCanEverTick = false;
    StorageInventory = CreateDefaultSubobject<ULDInventoryComponent>(TEXT("StorageInventory"));
}

FText ALDStorageActor::GetInteractionText_Implementation() const
{
    return FText::FromString(TEXT("Open Storage"));
}

bool ALDStorageActor::Interact_Implementation(AActor* InteractingActor)
{
    return InteractingActor != nullptr;
}

bool ALDStorageActor::DepositFrom(ULDInventoryComponent* SourceInventory, FName ItemId, int32 Quantity)
{
    if (!SourceInventory || !StorageInventory || ItemId.IsNone() || Quantity <= 0)
    {
        return false;
    }

    if (SourceInventory->GetQuantity(ItemId) < Quantity)
    {
        return false;
    }

    // Prototype storage does not know item stack metadata yet; Blueprint/DataTable flow should replace these defaults.
    if (!StorageInventory->AddItem(ItemId, Quantity, true, 999))
    {
        return false;
    }

    if (!SourceInventory->RemoveItem(ItemId, Quantity))
    {
        StorageInventory->RemoveItem(ItemId, Quantity);
        return false;
    }

    return true;
}

ULDInventoryComponent* ALDStorageActor::GetStorageInventory() const
{
    return StorageInventory;
}
