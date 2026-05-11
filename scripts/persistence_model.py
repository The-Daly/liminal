#!/usr/bin/env python3
from dataclasses import dataclass, field
import json
import random
from pathlib import Path
from tempfile import TemporaryDirectory

from inventory_model import InventoryContainer, build_player_inventory
from item_registry import DataRegistry, RegistryError, load_registry
from playable_loop_model import LoopOutcome, simulate_successful_run
from project_board_model import HubProgressState


@dataclass(frozen=True)
class RunHistoryEntry:
    faction_id: str
    run_state_id: str
    extracted: bool
    died: bool
    extraction_id: str | None
    destination_map: str | None
    looted_item_ids: tuple[str, ...]
    deposited_item_ids: tuple[str, ...]
    completed_upgrades: tuple[str, ...]
    remaining_sanity: float


@dataclass
class LocalProfileState:
    player_state_id: str
    faction_id: str
    personal: InventoryContainer
    hub_progress: HubProgressState
    run_history: list[RunHistoryEntry] = field(default_factory=list)

    def append_run(self, outcome: LoopOutcome, max_entries: int = 20) -> None:
        if max_entries <= 0:
            raise ValueError("max_entries must be positive")
        if outcome.faction_id != self.faction_id:
            raise RegistryError(
                f"Run outcome faction {outcome.faction_id} does not match profile faction {self.faction_id}"
            )

        self.run_history.append(
            RunHistoryEntry(
                faction_id=outcome.faction_id,
                run_state_id=outcome.run_state_id,
                extracted=outcome.extracted,
                died=outcome.died,
                extraction_id=outcome.extraction_id,
                destination_map=outcome.destination_map,
                looted_item_ids=tuple(outcome.looted_item_ids),
                deposited_item_ids=tuple(outcome.deposited_item_ids),
                completed_upgrades=tuple(outcome.completed_upgrades),
                remaining_sanity=float(outcome.remaining_sanity),
            )
        )
        if len(self.run_history) > max_entries:
            del self.run_history[:-max_entries]


@dataclass(frozen=True)
class RealmCharacterRecord:
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


@dataclass
class PersistentRealmCollection:
    official_characters: list[RealmCharacterRecord] = field(default_factory=list)
    community_characters: list[RealmCharacterRecord] = field(default_factory=list)
    wipe_state: dict[str, dict] = field(default_factory=dict)


@dataclass
class FrontendSessionState:
    current_route_id: str = "menu_title_shell"
    selected_realm_id: str | None = None
    selected_server_type: str | None = None
    selected_faction_id: str | None = None
    selected_character_id: str | None = None
    selected_appearance_id: str | None = None
    character_callsign: str = ""
    has_existing_character: bool = False
    character_configured: bool = False
    current_wipe_label: str = ""


def new_local_profile(registry: DataRegistry, player_state_id: str = "player_state_v0_meg") -> LocalProfileState:
    player_state = registry.player_states.get(player_state_id)
    if player_state is None:
        raise RegistryError(f"Unknown player_state_id: {player_state_id}")

    inventory = build_player_inventory(registry, player_state_id)
    faction_id = player_state["faction_id"]
    return LocalProfileState(
        player_state_id=player_state_id,
        faction_id=faction_id,
        personal=inventory.personal,
        hub_progress=HubProgressState(faction_id=faction_id),
    )


def inventory_records(container: InventoryContainer) -> list[dict[str, int | str]]:
    return [
        {"item_id": item_id, "quantity": container.quantity(item_id)}
        for item_id in sorted({stack.item_id for stack in container.stacks})
    ]


def profile_to_dict(profile: LocalProfileState) -> dict:
    return {
        "player_state_id": profile.player_state_id,
        "faction_id": profile.faction_id,
        "personal_storage": inventory_records(profile.personal),
        "hub_progress": {
            "contributions": {
                hub_upgrade_id: {
                    item_id: int(quantity)
                    for item_id, quantity in sorted(item_progress.items())
                }
                for hub_upgrade_id, item_progress in sorted(profile.hub_progress.contributions.items())
            },
            "completed_upgrades": sorted(profile.hub_progress.completed_upgrades),
        },
        "run_history": [
            {
                "faction_id": entry.faction_id,
                "run_state_id": entry.run_state_id,
                "extracted": entry.extracted,
                "died": entry.died,
                "extraction_id": entry.extraction_id,
                "destination_map": entry.destination_map,
                "looted_item_ids": list(entry.looted_item_ids),
                "deposited_item_ids": list(entry.deposited_item_ids),
                "completed_upgrades": list(entry.completed_upgrades),
                "remaining_sanity": entry.remaining_sanity,
            }
            for entry in profile.run_history
        ],
    }


def profile_from_dict(registry: DataRegistry, data: dict) -> LocalProfileState:
    player_state_id = data.get("player_state_id")
    if not player_state_id:
        raise RegistryError("Profile data is missing player_state_id")

    profile = new_local_profile(registry, player_state_id)
    if data.get("faction_id", profile.faction_id) != profile.faction_id:
        raise RegistryError(
            f"Profile faction {data.get('faction_id')} does not match player state faction {profile.faction_id}"
        )

    for record in data.get("personal_storage", []):
        profile.personal.add_item(registry, str(record["item_id"]), int(record["quantity"]))

    progress_data = data.get("hub_progress", {})
    profile.hub_progress = HubProgressState(
        faction_id=profile.faction_id,
        contributions={
            str(hub_upgrade_id): {
                str(item_id): int(quantity)
                for item_id, quantity in item_progress.items()
            }
            for hub_upgrade_id, item_progress in progress_data.get("contributions", {}).items()
        },
        completed_upgrades=set(progress_data.get("completed_upgrades", [])),
    )
    profile.run_history = [
        RunHistoryEntry(
            faction_id=str(entry["faction_id"]),
            run_state_id=str(entry["run_state_id"]),
            extracted=bool(entry["extracted"]),
            died=bool(entry["died"]),
            extraction_id=str(entry["extraction_id"]) if entry["extraction_id"] is not None else None,
            destination_map=str(entry["destination_map"]) if entry["destination_map"] is not None else None,
            looted_item_ids=tuple(str(item_id) for item_id in entry.get("looted_item_ids", [])),
            deposited_item_ids=tuple(str(item_id) for item_id in entry.get("deposited_item_ids", [])),
            completed_upgrades=tuple(str(upgrade_id) for upgrade_id in entry.get("completed_upgrades", [])),
            remaining_sanity=float(entry["remaining_sanity"]),
        )
        for entry in data.get("run_history", [])
    ]
    return profile


def save_profile(path: Path, profile: LocalProfileState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(profile_to_dict(profile), handle, indent=2)


def load_profile(registry: DataRegistry, path: Path) -> LocalProfileState:
    with path.open("r", encoding="utf-8") as handle:
        return profile_from_dict(registry, json.load(handle))


def persistent_collection_to_dict(collection: PersistentRealmCollection) -> dict:
    return {
        "official_characters": [record.__dict__ for record in collection.official_characters],
        "community_characters": [record.__dict__ for record in collection.community_characters],
        "wipe_state": collection.wipe_state,
    }


def persistent_collection_from_dict(data: dict) -> PersistentRealmCollection:
    def records(key: str) -> list[RealmCharacterRecord]:
        return [RealmCharacterRecord(**entry) for entry in data.get(key, [])]

    return PersistentRealmCollection(
        official_characters=records("official_characters"),
        community_characters=records("community_characters"),
        wipe_state=dict(data.get("wipe_state", {})),
    )


def save_persistent_collection(path: Path, collection: PersistentRealmCollection) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(persistent_collection_to_dict(collection), handle, indent=2)


def load_persistent_collection(path: Path) -> PersistentRealmCollection:
    with path.open("r", encoding="utf-8") as handle:
        return persistent_collection_from_dict(json.load(handle))


def frontend_session_to_dict(session: FrontendSessionState) -> dict:
    return {
        "current_route_id": session.current_route_id,
        "selected_realm_id": session.selected_realm_id,
        "selected_server_type": session.selected_server_type,
        "selected_faction_id": session.selected_faction_id,
        "selected_character_id": session.selected_character_id,
        "selected_appearance_id": session.selected_appearance_id,
        "character_callsign": session.character_callsign,
        "has_existing_character": session.has_existing_character,
        "character_configured": session.character_configured,
        "current_wipe_label": session.current_wipe_label,
    }


def frontend_session_from_dict(data: dict) -> FrontendSessionState:
    return FrontendSessionState(
        current_route_id=str(data.get("current_route_id", "menu_title_shell")),
        selected_realm_id=str(data["selected_realm_id"]) if data.get("selected_realm_id") is not None else None,
        selected_server_type=(
            str(data["selected_server_type"]) if data.get("selected_server_type") is not None else None
        ),
        selected_faction_id=(
            str(data["selected_faction_id"]) if data.get("selected_faction_id") is not None else None
        ),
        selected_character_id=(
            str(data["selected_character_id"]) if data.get("selected_character_id") is not None else None
        ),
        selected_appearance_id=(
            str(data["selected_appearance_id"]) if data.get("selected_appearance_id") is not None else None
        ),
        character_callsign=str(data.get("character_callsign", "")),
        has_existing_character=bool(data.get("has_existing_character", False)),
        character_configured=bool(data.get("character_configured", False)),
        current_wipe_label=str(data.get("current_wipe_label", "")),
    )


def save_frontend_session(path: Path, session: FrontendSessionState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(frontend_session_to_dict(session), handle, indent=2)


def load_frontend_session(path: Path) -> FrontendSessionState:
    with path.open("r", encoding="utf-8") as handle:
        return frontend_session_from_dict(json.load(handle))


def main() -> None:
    registry = load_registry()
    profile = new_local_profile(registry)
    profile.personal.add_item(registry, "currency_old_movie_ticket", 12)
    profile.hub_progress.contributions["hub_project_board_signal_lamp_v0"] = {
        "currency_old_movie_ticket": 12
    }
    profile.append_run(simulate_successful_run(registry, rng=random.Random(7)))

    with TemporaryDirectory() as temp_dir:
        profile_path = Path(temp_dir) / "local_profile.json"
        save_profile(profile_path, profile)
        restored = load_profile(registry, profile_path)
        session_path = Path(temp_dir) / "frontend_session.json"
        save_frontend_session(
            session_path,
            FrontendSessionState(
                selected_realm_id="official_north_america_01",
                selected_server_type="official",
                selected_faction_id="meg",
                character_callsign="MEG-01",
                current_wipe_label="Biannual Official Wipe | Next wipe 2028-01-01",
            ),
        )
        restored_session = load_frontend_session(session_path)
        print(
            f"Saved profile for {restored.faction_id} with "
            f"{len(inventory_records(restored.personal))} stored item types and "
            f"{len(restored.run_history)} run record(s)"
        )
        print(f"Saved frontend session for realm {restored_session.selected_realm_id}")


if __name__ == "__main__":
    main()
