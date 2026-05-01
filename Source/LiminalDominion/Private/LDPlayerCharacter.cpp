#include "LDPlayerCharacter.h"
#include "GameFramework/Controller.h"
#include "LDInventoryComponent.h"
#include "LDInteractable.h"
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

        if (!CarriedInventory->AddItemFromData(ItemId, 1))
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
        OnPlayerMessage.Broadcast(FText::FromString(TEXT("No Almond Water")));
        return false;
    }

    SanityComponent->ConsumeAlmondWater();
    OnPlayerMessage.Broadcast(FText::FromString(TEXT("Consumed Almond Water")));
    BroadcastHUDSnapshot();
    return true;
}

void ALDPlayerCharacter::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    RefreshFocusedInteractable();
    BroadcastHUDSnapshot();
}

void ALDPlayerCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    if (!PlayerInputComponent)
    {
        return;
    }

    PlayerInputComponent->BindAxis(TEXT("MoveForward"), this, &ALDPlayerCharacter::MoveForward);
    PlayerInputComponent->BindAxis(TEXT("MoveRight"), this, &ALDPlayerCharacter::MoveRight);
    PlayerInputComponent->BindAxis(TEXT("Turn"), this, &ALDPlayerCharacter::Turn);
    PlayerInputComponent->BindAxis(TEXT("LookUp"), this, &ALDPlayerCharacter::LookUp);
    PlayerInputComponent->BindAction(TEXT("Jump"), IE_Pressed, this, &ACharacter::Jump);
    PlayerInputComponent->BindAction(TEXT("Jump"), IE_Released, this, &ACharacter::StopJumping);
    PlayerInputComponent->BindAction(TEXT("Interact"), IE_Pressed, this, &ALDPlayerCharacter::TryInteract);
    PlayerInputComponent->BindAction(TEXT("ConsumeAlmondWater"), IE_Pressed, this, &ALDPlayerCharacter::ConsumeAlmondWater);
    PlayerInputComponent->BindAction(TEXT("DebugKillPlayer"), IE_Pressed, this, &ALDPlayerCharacter::DebugKillPlayer);
}

bool ALDPlayerCharacter::TryInteract()
{
    RefreshFocusedInteractable();

    if (!FocusedInteractableActor || !FocusedInteractableActor->GetClass()->ImplementsInterface(ULDInteractable::StaticClass()))
    {
        OnPlayerMessage.Broadcast(FText::FromString(TEXT("Nothing to interact with")));
        return false;
    }

    const bool bInteracted = ILDInteractable::Execute_Interact(FocusedInteractableActor, this);
    BroadcastHUDSnapshot();
    return bInteracted;
}

FLDHUDSnapshot ALDPlayerCharacter::BuildHUDSnapshot() const
{
    FLDHUDSnapshot Snapshot;
    if (SanityComponent)
    {
        Snapshot.Sanity = SanityComponent->GetCurrentSanity();
        Snapshot.bLowSanity = SanityComponent->IsLowSanity();
    }
    if (CarriedInventory)
    {
        Snapshot.CarriedStacks = CarriedInventory->GetStacks();
    }
    Snapshot.InteractionText = CurrentInteractionText;
    Snapshot.bHasInteraction = !CurrentInteractionText.IsEmpty();
    if (RunStateComponent)
    {
        Snapshot.bRunActive = RunStateComponent->IsRunActive();
        Snapshot.RunResult = RunStateComponent->GetRunResult();
    }
    return Snapshot;
}

void ALDPlayerCharacter::MoveForward(float Value)
{
    if (Controller && !FMath::IsNearlyZero(Value))
    {
        const FRotator Rotation(0.0f, Controller->GetControlRotation().Yaw, 0.0f);
        AddMovementInput(FRotationMatrix(Rotation).GetUnitAxis(EAxis::X), Value);
    }
}

void ALDPlayerCharacter::MoveRight(float Value)
{
    if (Controller && !FMath::IsNearlyZero(Value))
    {
        const FRotator Rotation(0.0f, Controller->GetControlRotation().Yaw, 0.0f);
        AddMovementInput(FRotationMatrix(Rotation).GetUnitAxis(EAxis::Y), Value);
    }
}

void ALDPlayerCharacter::Turn(float Value)
{
    AddControllerYawInput(Value);
}

void ALDPlayerCharacter::LookUp(float Value)
{
    AddControllerPitchInput(Value);
}

void ALDPlayerCharacter::RefreshFocusedInteractable()
{
    AActor* PreviousActor = FocusedInteractableActor;
    const FText PreviousText = CurrentInteractionText;
    FocusedInteractableActor = nullptr;
    CurrentInteractionText = FText::GetEmpty();

    FVector ViewLocation;
    FRotator ViewRotation;
    if (!Controller)
    {
        return;
    }

    Controller->GetPlayerViewPoint(ViewLocation, ViewRotation);
    const FVector TraceEnd = ViewLocation + ViewRotation.Vector() * InteractionRange;

    FHitResult Hit;
    FCollisionQueryParams QueryParams(SCENE_QUERY_STAT(LDInteractionTrace), false, this);
    if (GetWorld() && GetWorld()->LineTraceSingleByChannel(Hit, ViewLocation, TraceEnd, ECC_Visibility, QueryParams))
    {
        AActor* HitActor = Hit.GetActor();
        if (HitActor && HitActor->GetClass()->ImplementsInterface(ULDInteractable::StaticClass()))
        {
            FocusedInteractableActor = HitActor;
            CurrentInteractionText = ILDInteractable::Execute_GetInteractionText(HitActor);
        }
    }

    if (PreviousActor != FocusedInteractableActor || !PreviousText.EqualTo(CurrentInteractionText))
    {
        OnInteractionPromptChanged.Broadcast(CurrentInteractionText);
    }
}

void ALDPlayerCharacter::BroadcastHUDSnapshot()
{
    OnHUDSnapshotChanged.Broadcast(BuildHUDSnapshot());
}
