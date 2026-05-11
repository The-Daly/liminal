#!/usr/bin/env python3
import unreal


STRING = unreal.BlueprintEditorLibrary.get_basic_type_by_name("string")
FLOAT = unreal.BlueprintEditorLibrary.get_basic_type_by_name("float")
BOOL = unreal.BlueprintEditorLibrary.get_basic_type_by_name("bool")
INT = unreal.BlueprintEditorLibrary.get_basic_type_by_name("int")

BLUEPRINT_VARIABLES = {
    "/Game/Blueprints/BP_LDGameMode": [
        ("ItemDataTablePath", STRING, False),
        ("LootTablesDataTablePath", STRING, False),
        ("ExtractionsDataTablePath", STRING, False),
        ("StorageDataTablePath", STRING, False),
        ("SanityDataTablePath", STRING, False),
        ("HubUpgradesDataTablePath", STRING, False),
        ("PlayerStateDataTablePath", STRING, False),
        ("RunStateDataTablePath", STRING, False),
        ("ServerRealmsDataTablePath", STRING, False),
        ("WipeSchedulesDataTablePath", STRING, False),
        ("CharacterAppearanceDataTablePath", STRING, False),
        ("MenuRoutesDataTablePath", STRING, False),
        ("DefaultHubMapPath", STRING, False),
        ("DefaultPersonalRoomMapPath", STRING, False),
        ("DefaultRunMapPath", STRING, False),
        ("DefaultOfficialRealmId", STRING, False),
        ("DefaultCommunityRealmId", STRING, False),
        ("DefaultMenuRouteId", STRING, False),
        ("ActivePlayerStateId", STRING, False),
        ("ActiveRunStateId", STRING, False),
        ("ActiveHubUpgradeId", STRING, False),
    ],
    "/Game/Blueprints/BP_MenuFlowController": [
        ("CurrentRouteId", STRING, False),
        ("NextRouteId", STRING, False),
        ("SelectedRealmId", STRING, False),
        ("SelectedServerType", STRING, False),
        ("SelectedFactionId", STRING, False),
        ("SelectedCharacterId", STRING, False),
        ("SelectedAppearanceId", STRING, False),
        ("CharacterCallsign", STRING, False),
        ("HasExistingCharacter", BOOL, False),
        ("CharacterConfigured", BOOL, False),
        ("CurrentWipeLabel", STRING, False),
        ("CurrentServerName", STRING, False),
        ("CurrentServerRegion", STRING, False),
        ("FactionPopulationSummary", STRING, False),
        ("FactionLockWarningText", STRING, False),
        ("DeployEnabled", BOOL, False),
    ],
    "/Game/Blueprints/BP_CharacterPreviewAnchor": [
        ("AppearanceId", STRING, True),
        ("FactionId", STRING, True),
        ("PreviewRole", STRING, True),
    ],
    "/Game/Blueprints/BP_FactionNpcPreviewAnchor": [
        ("AppearanceId", STRING, True),
        ("FactionId", STRING, True),
        ("PreviewRole", STRING, True),
    ],
    "/Game/Blueprints/BP_LDPlayer": [
        ("CurrentSanity", FLOAT, False),
        ("InteractionPrompt", STRING, False),
        ("RunStateLabel", STRING, False),
        ("CarriedInventorySummary", STRING, False),
        ("FeedbackMessage", STRING, False),
        ("SelectedFactionId", STRING, False),
        ("ActiveRunStateId", STRING, False),
        ("CurrentRunOutcome", STRING, False),
    ],
    "/Game/Blueprints/BP_DeploymentGate": [
        ("InteractionPrompt", STRING, True),
        ("TargetMapPath", STRING, True),
        ("ReturnMapPath", STRING, True),
        ("RunStateId", STRING, True),
        ("PlayerStateId", STRING, True),
        ("BoardUpgradeId", STRING, True),
        ("StartsRun", BOOL, True),
    ],
    "/Game/Blueprints/BP_LootContainer": [
        ("InteractionPrompt", STRING, True),
        ("LootTableId", STRING, True),
        ("ContainerLabel", STRING, True),
        ("SingleUse", BOOL, True),
        ("TracksCarriedInventory", BOOL, True),
    ],
    "/Game/Blueprints/BP_ExtractionTrigger_Stable": [
        ("InteractionPrompt", STRING, True),
        ("ExtractionId", STRING, True),
        ("ReturnMapPath", STRING, True),
        ("RequiredItemId", STRING, True),
        ("ReturnsToPersonalRoom", BOOL, True),
    ],
    "/Game/Blueprints/BP_ExtractionTrigger_HiddenTicketBooth": [
        ("InteractionPrompt", STRING, True),
        ("ExtractionId", STRING, True),
        ("ReturnMapPath", STRING, True),
        ("RequiredItemId", STRING, True),
        ("ReturnsToPersonalRoom", BOOL, True),
    ],
    "/Game/Blueprints/BP_PersonalStorage": [
        ("InteractionPrompt", STRING, True),
        ("StorageId", STRING, True),
        ("DepositLabel", STRING, True),
        ("PreservesLootOnDeath", BOOL, True),
    ],
    "/Game/Blueprints/BP_ProjectBoard": [
        ("InteractionPrompt", STRING, True),
        ("HubUpgradeId", STRING, True),
        ("FactionId", STRING, True),
        ("TracksPartialProgress", BOOL, True),
        ("VisibleUnlockLabel", STRING, True),
    ],
    "/Game/Blueprints/BP_FlickerStalker": [
        ("EncounterLabel", STRING, True),
        ("SanityRuleId", STRING, True),
        ("ForcesRetreatPath", BOOL, True),
    ],
    "/Game/UI/WBP_PlayerHUD": [
        ("CurrentSanity", FLOAT, False),
        ("InteractionPrompt", STRING, False),
        ("RunStateLabel", STRING, False),
        ("CarriedInventorySummary", STRING, False),
        ("FeedbackMessage", STRING, False),
    ],
    "/Game/UI/WBP_TitleShell": [
        ("HeadlineText", STRING, False),
        ("SubheadText", STRING, False),
        ("CurrentRouteId", STRING, False),
        ("NextRouteId", STRING, False),
    ],
    "/Game/UI/WBP_ServerBrowser": [
        ("CurrentRouteId", STRING, False),
        ("SelectedRealmId", STRING, False),
        ("SelectedServerType", STRING, False),
        ("ServerNameText", STRING, False),
        ("ServerRegionText", STRING, False),
        ("RulesetSummaryText", STRING, False),
        ("WipeSummaryText", STRING, False),
        ("FactionPopulationSummary", STRING, False),
        ("QueueSummaryText", STRING, False),
        ("CreationStatusText", STRING, False),
    ],
    "/Game/UI/WBP_FactionSelection": [
        ("CurrentRouteId", STRING, False),
        ("SelectedRealmId", STRING, False),
        ("SelectedFactionId", STRING, False),
        ("FactionLockWarningText", STRING, False),
        ("WipeSummaryText", STRING, False),
    ],
    "/Game/UI/WBP_CharacterSetup": [
        ("CurrentRouteId", STRING, False),
        ("SelectedFactionId", STRING, False),
        ("SelectedAppearanceId", STRING, False),
        ("CharacterCallsign", STRING, False),
        ("IdentityItemId", STRING, False),
    ],
    "/Game/UI/WBP_MainPlayerMenu": [
        ("CurrentRouteId", STRING, False),
        ("SelectedRealmId", STRING, False),
        ("SelectedCharacterId", STRING, False),
        ("SelectedFactionId", STRING, False),
        ("ServerNameText", STRING, False),
        ("ServerRegionText", STRING, False),
        ("WipeSummaryText", STRING, False),
        ("FactionPopulationSummary", STRING, False),
        ("CharacterSummaryText", STRING, False),
        ("DeployEnabled", BOOL, False),
    ],
    "/Game/UI/WBP_RunResult": [
        ("RunOutcomeLabel", STRING, False),
        ("KeptLootSummary", STRING, False),
        ("LostLootSummary", STRING, False),
        ("ReturnDestinationLabel", STRING, False),
        ("ContributionSummary", STRING, False),
    ],
}


def log(message: str) -> None:
    unreal.log(f"[LD Blueprint Wiring] {message}")


def load_blueprint(path: str):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if asset is None:
        raise RuntimeError(f"Blueprint asset not found: {path}")
    return asset


def ensure_variable(blueprint, name: str, pin_type, instance_editable: bool) -> None:
    created = unreal.BlueprintEditorLibrary.add_member_variable(blueprint, name, pin_type)
    if created:
        log(f"Added variable {name} to {blueprint.get_path_name()}")
    unreal.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(
        blueprint,
        name,
        instance_editable,
    )


def compile_and_save(blueprint) -> None:
    unreal.BlueprintEditorLibrary.compile_blueprint(blueprint)
    unreal.EditorAssetLibrary.save_loaded_asset(blueprint, only_if_is_dirty=False)


def main() -> None:
    for path, variables in BLUEPRINT_VARIABLES.items():
        blueprint = load_blueprint(path)
        for variable_name, variable_type, instance_editable in variables:
            ensure_variable(blueprint, variable_name, variable_type, instance_editable)
        compile_and_save(blueprint)
        log(f"Wired data variables for {path}")

    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("Blueprint data wiring complete")


if __name__ == "__main__":
    main()
