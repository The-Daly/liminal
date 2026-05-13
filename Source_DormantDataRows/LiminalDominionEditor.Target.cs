using UnrealBuildTool;
using System.Collections.Generic;

public class LiminalDominionEditorTarget : TargetRules
{
    public LiminalDominionEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("LiminalDominion");
    }
}
