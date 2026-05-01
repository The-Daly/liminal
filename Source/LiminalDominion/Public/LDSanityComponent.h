#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "LDSanityComponent.generated.h"

UCLASS(ClassGroup=(LiminalDominion), meta=(BlueprintSpawnableComponent))
class LIMINALDOMINION_API ULDSanityComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    ULDSanityComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Sanity")
    void Drain(float Seconds);

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Sanity")
    void Restore(float Amount);

    UFUNCTION(BlueprintCallable, Category="Liminal Dominion|Sanity")
    void ConsumeAlmondWater();

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Sanity")
    bool IsLowSanity() const;

    UFUNCTION(BlueprintPure, Category="Liminal Dominion|Sanity")
    float GetCurrentSanity() const;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Sanity")
    float MaxSanity = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Sanity")
    float CurrentSanity = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Sanity")
    float DrainPerMinute = 4.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Sanity")
    float LowSanityThreshold = 30.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Sanity")
    float AlmondWaterRestore = 25.0f;
};
