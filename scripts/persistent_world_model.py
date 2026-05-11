#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Iterable

from item_registry import DataRegistry, RegistryError, load_registry


@dataclass(frozen=True)
class FactionPopulationState:
    faction_id: str
    current_active: int
    cap: int
    queue_count: int

    @property
    def open_slots(self) -> int:
        return max(self.cap - self.current_active, 0)


@dataclass(frozen=True)
class ServerRealmDescriptor:
    realm_id: str
    display_name: str
    server_type: str
    region: str
    population_cap: int
    queue_cap: int
    wipe_schedule_id: str
    ruleset_summary: str
    supports_character_creation: bool
    faction_caps: tuple[FactionPopulationState, ...]


@dataclass(frozen=True)
class WipeSchedule:
    wipe_schedule_id: str
    display_name: str
    cadence_years: int
    last_wipe_utc: str
    next_wipe_utc: str
    warning_window_days: int
    description: str


@dataclass(frozen=True)
class CharacterProfile:
    character_id: str
    realm_id: str
    server_type: str
    faction_id: str
    wipe_schedule_id: str
    wipe_id: str
    slot_index: int
    callsign: str
    appearance_id: str
    role_preset: str
    created_at_utc: str
    last_login_utc: str
    locked_until_wipe: bool


@dataclass(frozen=True)
class CharacterSlotSummary:
    character_id: str
    realm_id: str
    server_type: str
    faction_id: str
    callsign: str
    slot_index: int
    wipe_id: str


def realm_descriptor(
    registry: DataRegistry,
    realm_id: str,
    active_counts: dict[str, int] | None = None,
    queue_counts: dict[str, int] | None = None,
) -> ServerRealmDescriptor:
    realm = registry.server_realms.get(realm_id)
    if realm is None:
        raise RegistryError(f"Unknown realm_id: {realm_id}")

    active_counts = active_counts or {}
    queue_counts = queue_counts or {}
    faction_caps = tuple(
        FactionPopulationState(
            faction_id=entry["faction_id"],
            current_active=int(active_counts.get(entry["faction_id"], 0)),
            cap=int(entry["cap"]),
            queue_count=int(queue_counts.get(entry["faction_id"], 0)),
        )
        for entry in realm["faction_caps"]
    )
    return ServerRealmDescriptor(
        realm_id=realm["realm_id"],
        display_name=realm["display_name"],
        server_type=realm["server_type"],
        region=realm["region"],
        population_cap=int(realm["population_cap"]),
        queue_cap=int(realm["queue_cap"]),
        wipe_schedule_id=realm["wipe_schedule_id"],
        ruleset_summary=realm["ruleset_summary"],
        supports_character_creation=bool(realm["supports_character_creation"]),
        faction_caps=faction_caps,
    )


def wipe_schedule(registry: DataRegistry, wipe_schedule_id: str) -> WipeSchedule:
    schedule = registry.wipe_schedules.get(wipe_schedule_id)
    if schedule is None:
        raise RegistryError(f"Unknown wipe_schedule_id: {wipe_schedule_id}")
    return WipeSchedule(**schedule)


def can_create_character_on_realm(
    registry: DataRegistry,
    realm_id: str,
    faction_id: str,
    active_counts: dict[str, int] | None = None,
) -> bool:
    descriptor = realm_descriptor(registry, realm_id, active_counts=active_counts)
    for state in descriptor.faction_caps:
        if state.faction_id == faction_id:
            return descriptor.supports_character_creation and state.current_active < state.cap
    raise RegistryError(f"Realm {realm_id} does not expose faction {faction_id}")


def create_character_profile(
    registry: DataRegistry,
    realm_id: str,
    faction_id: str,
    callsign: str,
    appearance_id: str,
    slot_index: int,
    timestamp_utc: str,
) -> CharacterProfile:
    descriptor = realm_descriptor(registry, realm_id)
    appearance = registry.character_appearance.get(appearance_id)
    if appearance is None:
        raise RegistryError(f"Unknown appearance_id: {appearance_id}")
    if appearance["faction_id"] != faction_id:
        raise RegistryError(
            f"Appearance {appearance_id} belongs to faction {appearance['faction_id']}, not {faction_id}"
        )
    return CharacterProfile(
        character_id=f"char_{realm_id}_{faction_id}_{slot_index:03d}",
        realm_id=realm_id,
        server_type=descriptor.server_type,
        faction_id=faction_id,
        wipe_schedule_id=descriptor.wipe_schedule_id,
        wipe_id=f"{descriptor.wipe_schedule_id}_{wipe_schedule(registry, descriptor.wipe_schedule_id).next_wipe_utc[:4]}",
        slot_index=slot_index,
        callsign=callsign,
        appearance_id=appearance_id,
        role_preset="operator",
        created_at_utc=timestamp_utc,
        last_login_utc=timestamp_utc,
        locked_until_wipe=True,
    )


def can_change_faction(profile: CharacterProfile, current_wipe_id: str) -> bool:
    return not profile.locked_until_wipe or profile.wipe_id != current_wipe_id


def profiles_by_server_type(
    profiles: Iterable[CharacterProfile],
) -> dict[str, list[CharacterProfile]]:
    grouped = {"official": [], "community": []}
    for profile in profiles:
        grouped.setdefault(profile.server_type, []).append(profile)
    return grouped


def slot_summary(profile: CharacterProfile) -> CharacterSlotSummary:
    return CharacterSlotSummary(
        character_id=profile.character_id,
        realm_id=profile.realm_id,
        server_type=profile.server_type,
        faction_id=profile.faction_id,
        callsign=profile.callsign,
        slot_index=profile.slot_index,
        wipe_id=profile.wipe_id,
    )


def main() -> None:
    registry = load_registry()
    descriptor = realm_descriptor(
        registry,
        "official_north_america_01",
        active_counts={"meg": 30, "bntg": 28, "clippers": 24},
        queue_counts={"meg": 6, "bntg": 1, "clippers": 0},
    )
    print(descriptor.display_name)
    for state in descriptor.faction_caps:
        print(f"{state.faction_id}: {state.current_active}/{state.cap} active, queue {state.queue_count}")


if __name__ == "__main__":
    main()
