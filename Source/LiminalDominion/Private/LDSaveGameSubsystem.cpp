#include "LDSaveGameSubsystem.h"
#include "Kismet/GameplayStatics.h"
#include "LDSaveGame.h"

void ULDSaveGameSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    LoadOrCreateSave();
}

ULDSaveGame* ULDSaveGameSubsystem::LoadOrCreateSave()
{
    if (CurrentSave)
    {
        return CurrentSave;
    }

    if (UGameplayStatics::DoesSaveGameExist(SaveSlotName, UserIndex))
    {
        CurrentSave = Cast<ULDSaveGame>(UGameplayStatics::LoadGameFromSlot(SaveSlotName, UserIndex));
    }

    if (!CurrentSave)
    {
        CurrentSave = Cast<ULDSaveGame>(UGameplayStatics::CreateSaveGameObject(ULDSaveGame::StaticClass()));
        if (CurrentSave)
        {
            CurrentSave->PersonalStorage.ContainerId = FName(TEXT("storage_personal_room_tier0"));
            SaveCurrentGame();
        }
    }

    return CurrentSave;
}

bool ULDSaveGameSubsystem::SaveCurrentGame()
{
    return CurrentSave && UGameplayStatics::SaveGameToSlot(CurrentSave, SaveSlotName, UserIndex);
}

void ULDSaveGameSubsystem::SetFactionId(FName FactionId)
{
    ULDSaveGame* Save = LoadOrCreateSave();
    if (!Save || FactionId.IsNone())
    {
        return;
    }

    Save->FactionId = FactionId;
    SaveCurrentGame();
}

FName ULDSaveGameSubsystem::GetFactionId() const
{
    return CurrentSave ? CurrentSave->FactionId : NAME_None;
}

void ULDSaveGameSubsystem::SavePersonalStorage(const TArray<FLDInventoryStack>& Stacks)
{
    ULDSaveGame* Save = LoadOrCreateSave();
    if (!Save)
    {
        return;
    }

    Save->PersonalStorage.ContainerId = FName(TEXT("storage_personal_room_tier0"));
    Save->PersonalStorage.Stacks = Stacks;
    SaveCurrentGame();
}

TArray<FLDInventoryStack> ULDSaveGameSubsystem::GetPersonalStorageStacks() const
{
    return CurrentSave ? CurrentSave->PersonalStorage.Stacks : TArray<FLDInventoryStack>();
}

void ULDSaveGameSubsystem::MarkHubUpgradeComplete(FName HubUpgradeId)
{
    ULDSaveGame* Save = LoadOrCreateSave();
    if (!Save || HubUpgradeId.IsNone())
    {
        return;
    }

    Save->CompletedHubUpgradeIds.AddUnique(HubUpgradeId);
    SaveCurrentGame();
}

bool ULDSaveGameSubsystem::IsHubUpgradeComplete(FName HubUpgradeId) const
{
    return CurrentSave && CurrentSave->CompletedHubUpgradeIds.Contains(HubUpgradeId);
}

void ULDSaveGameSubsystem::AddRunHistoryEntry(FName RunStateId, FName Result, int32 TicketsExtracted)
{
    ULDSaveGame* Save = LoadOrCreateSave();
    if (!Save)
    {
        return;
    }

    FLDRunHistoryEntry Entry;
    Entry.RunStateId = RunStateId;
    Entry.Result = Result;
    Entry.TicketsExtracted = TicketsExtracted;
    Save->RunHistory.Add(Entry);
    SaveCurrentGame();
}
