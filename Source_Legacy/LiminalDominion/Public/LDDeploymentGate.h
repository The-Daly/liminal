#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "LDInteractable.h"
#include "LDDeploymentGate.generated.h"

UCLASS()
class LIMINALDOMINION_API ALDDeploymentGate : public AActor, public ILDInteractable
{
    GENERATED_BODY()

public:
    ALDDeploymentGate();

    virtual FText GetInteractionText_Implementation() const override;
    virtual bool Interact_Implementation(AActor* InteractingActor) override;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Deployment")
    FName RunStateId = FName(TEXT("run_level1_service_halls_v0"));

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Deployment")
    FName TargetLevelName = FName(TEXT("LD_Level1_ServiceHalls_Greybox"));

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Deployment")
    bool bOpenLevelOnDeploy = true;
};
