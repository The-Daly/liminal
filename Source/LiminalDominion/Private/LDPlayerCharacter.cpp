#include "LDPlayerCharacter.h"
#include "LDInventoryComponent.h"
#include "LDRunStateComponent.h"
#include "LDSanityComponent.h"

ALDPlayerCharacter::ALDPlayerCharacter()
{
    PrimaryActorTick.bCanEverTick = true;

    CarriedInventory = CreateDefaultSubobject<ULDInventoryComponent>(TEXT("CarriedInventory"));
    PersonalStorage = CreateDefaultSubobject<ULDInventoryComponent>(TEXT("PersonalStorage"));
    SanityComponent = CreateDefaultSubobject<ULDSanityComponent>(TEXT("SanityComponent"));
    RunStateComponent = CreateDefaultSubobject<ULDRunStateComponent>(TEXT("RunStateComponent"));
}

ULDInventoryComponent* ALDPlayerCharacter::GetCarriedInventory() const
{
    return CarriedInventory;
}

ULDInventoryComponent* ALDPlayerCharacter::GetPersonalStorage() const
{
    return PersonalStorage;
}

ULDSanityComponent* ALDPlayerCharacter::GetSanityComponent() const
{
    return SanityComponent;
}

ULDRunStateComponent* ALDPlayerCharacter::GetRunStateComponent() const
{
    return RunStateComponent;
}

void ALDPlayerCharacter::DebugKillPlayer()
{
    if (RunStateComponent)
    {
        RunStateComponent->Die(CarriedInventory);
    }
}

bool ALDPlayerCharacter::GiveStarterLoadout(const TArray<FName>& ItemIds)
{
    if (!CarriedInventory)
    {
        return false;
    }

    for (const FName ItemId : ItemIds)
    {
        if (ItemId.IsNone())
        {
            return false;
        }

        // Prototype loadouts use permissive stack defaults until DataTable item metadata is imported.
        if (!CarriedInventory->AddItem(ItemId, 1, true, 999))
        {
            return false;
        }
    }

    return true;
}

bool ALDPlayerCharacter::ConsumeAlmondWater()
{
    if (!CarriedInventory || !SanityComponent)
    {
        return false;
    }

    if (!CarriedInventory->RemoveItem(AlmondWaterItemId, 1))
    {
        return false;
    }

    SanityComponent->ConsumeAlmondWater();
    return true;
}
