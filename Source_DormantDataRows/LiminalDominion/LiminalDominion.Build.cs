using UnrealBuildTool;

public class LiminalDominion : ModuleRules
{
    public LiminalDominion(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new[]
        {
            "Core",
            "CoreUObject",
            "Engine"
        });

        PrivateDependencyModuleNames.AddRange(new string[] { });
    }
}
