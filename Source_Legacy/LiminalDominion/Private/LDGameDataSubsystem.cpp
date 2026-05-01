#include "LDGameDataSubsystem.h"
#include "Engine/DataTable.h"

void ULDGameDataSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);

    if (!ItemDataTable && ItemDataTablePath.IsValid())
    {
        ItemDataTable = Cast<UDataTable>(ItemDataTablePath.TryLoad());
    }
}

void ULDGameDataSubsystem::SetItemDataTable(UDataTable* InItemDataTable)
{
    ItemDataTable = InItemDataTable;
}

const FLDItemRow* ULDGameDataSubsystem::FindItemRow(FName ItemId) const
{
    if (!ItemDataTable || ItemId.IsNone())
    {
        return nullptr;
    }

    const FString ContextString = TEXT("LDGameDataSubsystem::FindItemRow");
    return ItemDataTable->FindRow<FLDItemRow>(ItemId, ContextString);
}

FLDItemStackRule ULDGameDataSubsystem::GetItemStackRule(FName ItemId) const
{
    FLDItemStackRule Rule;
    const FLDItemRow* Row = FindItemRow(ItemId);
    if (!Row)
    {
        return Rule;
    }

    Rule.bFound = true;
    Rule.bStackable = Row->bStackable;
    Rule.MaxStack = FMath::Max(1, Row->MaxStack);
    return Rule;
}
