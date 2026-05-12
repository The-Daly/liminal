#!/usr/bin/env python3
from dataclasses import dataclass
from datetime import datetime

from item_registry import DataRegistry, RegistryError, load_registry
from persistent_world_model import CharacterProfile, realm_menu_summary


@dataclass(frozen=True)
class NavMenuEntry:
    label_text: str
    route_id: str
    icon_hint: str
    highlighted: bool
    enabled: bool


@dataclass(frozen=True)
class OperationBrief:
    operation_title_text: str
    zone_code_text: str
    threat_level_text: str
    extraction_windows_text: str
    environmental_anomaly_text: str
    recommended_team_size_text: str
    brief_objective_text: str
    primary_action_label: str
    primary_action_subtext: str


@dataclass(frozen=True)
class OperatorStatusSnapshot:
    operator_name_text: str
    operator_id_text: str
    faction_name_text: str
    faction_role_text: str
    health_condition_text: str
    reputation_summary_text: str
    currency_summary_text: str
    kit_summary_text: str


@dataclass(frozen=True)
class FooterTelemetrySnapshot:
    build_label_text: str
    environment_label_text: str
    footer_status_text: str
    local_time_text: str


@dataclass(frozen=True)
class OperationsHubSnapshot:
    nav_section_title_text: str
    nav_entries: tuple[NavMenuEntry, ...]
    operation_brief: OperationBrief
    operator_status: OperatorStatusSnapshot
    footer: FooterTelemetrySnapshot


def _format_operator_id(character_id: str) -> str:
    compact = character_id.replace("char_", "").replace("_", "-").upper()
    return compact[:14]


def build_operations_nav(deploy_enabled: bool) -> tuple[NavMenuEntry, ...]:
    return (
        NavMenuEntry("Deploy", "menu_deploy_panel", "crosshair", True, deploy_enabled),
        NavMenuEntry("Loadout", "menu_stash_panel", "rifle", False, True),
        NavMenuEntry("Operators", "menu_character_selection", "operator", False, True),
        NavMenuEntry("Market", "menu_stash_panel", "cart", False, True),
        NavMenuEntry("Intel", "menu_server_browser", "crate", False, True),
        NavMenuEntry("Settings", "menu_settings_panel", "gear", False, True),
        NavMenuEntry("Exit", "menu_title_shell", "door", False, True),
    )


def build_operation_brief(registry: DataRegistry, level_id: str = "level1_service_halls") -> OperationBrief:
    layout = registry.level_layouts.get(level_id)
    if layout is None:
        raise RegistryError(f"Unknown level_id: {level_id}")
    return OperationBrief(
        operation_title_text=f"Operation: {layout['display_name'].replace('Level 1 ', '')}",
        zone_code_text="Zone // SH-17",
        threat_level_text="High",
        extraction_windows_text="00:20-00:30 | 00:50-01:00 | 01:20-01:30",
        environmental_anomaly_text="Disorientation / Signal Interference",
        recommended_team_size_text="1 - 3",
        brief_objective_text="Investigate service halls and recover diagnostics from terminal nodes.",
        primary_action_label="Deploy",
        primary_action_subtext="Enter Zone",
    )


def build_operator_status_snapshot(
    registry: DataRegistry,
    profile: CharacterProfile,
    local_credits: int = 18420,
    research_points: int = 450,
    contract_tokens: int = 12,
) -> OperatorStatusSnapshot:
    faction = registry.faction(profile.faction_id)
    appearance = registry.character_appearance.get(profile.appearance_id, {})
    kit_name = str(appearance.get("role_label", appearance.get("display_name", "Field Kit")))
    return OperatorStatusSnapshot(
        operator_name_text=profile.callsign,
        operator_id_text=_format_operator_id(profile.character_id),
        faction_name_text=faction["display_name"],
        faction_role_text=str(faction["role"]),
        health_condition_text="Good | 100%",
        reputation_summary_text="Tier I - Field Clearance",
        currency_summary_text=(
            f"Credits {local_credits:,} | Research {research_points:,} | Contracts {contract_tokens:,}"
        ),
        kit_summary_text=kit_name,
    )


def build_footer_telemetry(
    build_label_text: str = "Build: V0.1.0",
    environment_label_text: str = "ENV: LOCAL TEST",
    footer_status_text: str = "All systems nominal... standby",
    now: datetime | None = None,
) -> FooterTelemetrySnapshot:
    now = now or datetime.now()
    return FooterTelemetrySnapshot(
        build_label_text=build_label_text,
        environment_label_text=environment_label_text,
        footer_status_text=footer_status_text,
        local_time_text=now.strftime("%H:%M:%S"),
    )


def build_operations_hub_snapshot(
    registry: DataRegistry,
    profile: CharacterProfile,
    deploy_enabled: bool,
) -> OperationsHubSnapshot:
    realm_summary = realm_menu_summary(registry, profile.realm_id)
    footer = build_footer_telemetry(
        footer_status_text=(
            f"{realm_summary.display_name} online | {realm_summary.region} | "
            f"{realm_summary.total_active}/{realm_summary.total_capacity} operators"
        )
    )
    return OperationsHubSnapshot(
        nav_section_title_text="Main Menu",
        nav_entries=build_operations_nav(deploy_enabled),
        operation_brief=build_operation_brief(registry),
        operator_status=build_operator_status_snapshot(registry, profile),
        footer=footer,
    )


def main() -> None:
    registry = load_registry()
    from persistent_world_model import create_character_profile

    profile = create_character_profile(
        registry,
        realm_id="official_north_america_01",
        faction_id="meg",
        callsign="Archive-Delta",
        appearance_id="appearance_meg_operator_field_v0",
        slot_index=1,
        timestamp_utc="2026-05-11T12:00:00Z",
    )
    snapshot = build_operations_hub_snapshot(registry, profile, deploy_enabled=True)
    print(snapshot.operation_brief.operation_title_text)
    print(snapshot.operator_status.currency_summary_text)


if __name__ == "__main__":
    main()
