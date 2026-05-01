#include "LDStorageActor.h"
#include "Engine/GameInstance.h"
#include "LDInventoryComponent.h"
#include "LDSaveGameSubsystem.h"

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

    if (!StorageInventory->AddItemFromData(ItemId, Quantity))
    {
        return false;
    }

    if (!SourceInventory->RemoveItem(ItemId, Quantity))
    {
        StorageInventory->RemoveItem(ItemId, Quantity);
        return false;
    }

    SaveToSaveGame();
    return true;
}

ULDInventoryComponent* ALDStorageActor::GetStorageInventory() const
{
    return StorageInventory;
}

void ALDStorageActor::LoadFromSave()
{
    if (!bPersistAsPersonalStorage || !StorageInventory)
    {
        return;
    }

    if (UGameInstance* GameInstance = GetWorld() ? GetWorld()->GetGameInstance() : nullptr)
    {
        if (const ULDSaveGameSubsystem* SaveSubsystem = GameInstance->GetSubsystem<ULDSaveGameSubsystem>())
        {
            StorageInventory->SetStacks(SaveSubsystem->GetPersonalStorageStacks());
        }
    }
}

void ALDStorageActor::SaveToSaveGame()
{
    if (!bPersistAsPersonalStorage || !StorageInventory)
    {
        return;
    }

    if (UGameInstance* GameInstance = GetWorld() ? GetWorld()->GetGameInstance() : nullptr)
    {
        if (ULDSaveGameSubsystem* SaveSubsystem = GameInstance->GetSubsystem<ULDSaveGameSubsystem>())
        {
            SaveSubsystem->SavePersonalStorage(StorageInventory->GetStacks());
        }
    }
}
