#include "LDInventoryComponent.h"
#include "Engine/GameInstance.h"
#include "LDGameDataSubsystem.h"

ULDInventoryComponent::ULDInventoryComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

bool ULDInventoryComponent::AddItem(FName ItemId, int32 Quantity, bool bStackable, int32 MaxStack)
{
    if (ItemId.IsNone() || Quantity <= 0 || MaxStack <= 0)
    {
        return false;
    }

    if (!bStackable && Quantity > 1)
    {
        return false;
    }

    TArray<FLDInventoryStack> TrialStacks = Stacks;
    int32 Remaining = Quantity;

    if (bStackable)
    {
        for (FLDInventoryStack& Stack : TrialStacks)
        {
            if (Stack.ItemId != ItemId || Stack.Quantity >= MaxStack)
            {
                continue;
            }

            const int32 Moved = FMath::Min(MaxStack - Stack.Quantity, Remaining);
            Stack.Quantity += Moved;
            Remaining -= Moved;

            if (Remaining == 0)
            {
                Stacks = TrialStacks;
                return true;
            }
        }
    }

    while (Remaining > 0)
    {
        if (TrialStacks.Num() >= MaxSlots)
        {
            return false;
        }

        FLDInventoryStack NewStack;
        NewStack.ItemId = ItemId;
        NewStack.Quantity = bStackable ? FMath::Min(MaxStack, Remaining) : 1;
        TrialStacks.Add(NewStack);
        Remaining -= NewStack.Quantity;
    }

    Stacks = TrialStacks;
    return true;
}

bool ULDInventoryComponent::AddItemFromData(FName ItemId, int32 Quantity)
{
    if (const UGameInstance* GameInstance = GetWorld() ? GetWorld()->GetGameInstance() : nullptr)
    {
        if (const ULDGameDataSubsystem* DataSubsystem = GameInstance->GetSubsystem<ULDGameDataSubsystem>())
        {
            const FLDItemStackRule Rule = DataSubsystem->GetItemStackRule(ItemId);
            if (Rule.bFound)
            {
                return AddItem(ItemId, Quantity, Rule.bStackable, Rule.MaxStack);
            }
        }
    }

    // Early graybox fallback: allows editor placement before DataTables are imported.
    return AddItem(ItemId, Quantity, true, 999);
}

bool ULDInventoryComponent::RemoveItem(FName ItemId, int32 Quantity)
{
    if (ItemId.IsNone() || Quantity <= 0 || GetQuantity(ItemId) < Quantity)
    {
        return false;
    }

    int32 Remaining = Quantity;
    for (int32 Index = Stacks.Num() - 1; Index >= 0 && Remaining > 0; --Index)
    {
        FLDInventoryStack& Stack = Stacks[Index];
        if (Stack.ItemId != ItemId)
        {
            continue;
        }

        const int32 Removed = FMath::Min(Stack.Quantity, Remaining);
        Stack.Quantity -= Removed;
        Remaining -= Removed;

        if (Stack.Quantity <= 0)
        {
            Stacks.RemoveAt(Index);
        }
    }

    return true;
}

int32 ULDInventoryComponent::GetQuantity(FName ItemId) const
{
    int32 Total = 0;
    for (const FLDInventoryStack& Stack : Stacks)
    {
        if (Stack.ItemId == ItemId)
        {
            Total += Stack.Quantity;
        }
    }
    return Total;
}

void ULDInventoryComponent::ClearInventory()
{
    Stacks.Reset();
}

TArray<FLDInventoryStack> ULDInventoryComponent::GetStacks() const
{
    return Stacks;
}
