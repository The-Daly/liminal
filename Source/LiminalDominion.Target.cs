using UnrealBuildTool;
using System.Collections.Generic;

public class LiminalDominionTarget : TargetRules
{
    public LiminalDominionTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("LiminalDominion");
    }
}
