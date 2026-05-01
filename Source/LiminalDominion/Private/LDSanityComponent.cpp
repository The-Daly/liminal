#include "LDSanityComponent.h"

ULDSanityComponent::ULDSanityComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void ULDSanityComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    Drain(DeltaTime);
}

void ULDSanityComponent::Drain(float Seconds)
{
    if (Seconds <= 0.0f)
    {
        return;
    }
    CurrentSanity = FMath::Clamp(CurrentSanity - (DrainPerMinute / 60.0f) * Seconds, 0.0f, MaxSanity);
}

void ULDSanityComponent::Restore(float Amount)
{
    if (Amount <= 0.0f)
    {
        return;
    }
    CurrentSanity = FMath::Clamp(CurrentSanity + Amount, 0.0f, MaxSanity);
}

void ULDSanityComponent::ConsumeAlmondWater()
{
    Restore(AlmondWaterRestore);
}

bool ULDSanityComponent::IsLowSanity() const
{
    return CurrentSanity <= LowSanityThreshold;
}

float ULDSanityComponent::GetCurrentSanity() const
{
    return CurrentSanity;
}
