#!/usr/bin/env python3
from dataclasses import dataclass

from item_registry import DataRegistry, RegistryError, load_registry


@dataclass(frozen=True)
class CharacterAppearanceDefinition:
    appearance_id: str
    display_name: str
    faction_id: str
    body_frame: str
    head_preset: str
    hair_preset: str
    headwear_preset: str
    outfit_preset: str
    voice_preset: str | None
    usable_by: tuple[str, ...]
    identity_item_id: str
    description: str


@dataclass(frozen=True)
class FactionCharacterRules:
    faction_id: str
    allowed_appearance_ids: tuple[str, ...]
    starter_identity_item_id: str


def appearance_definition(registry: DataRegistry, appearance_id: str) -> CharacterAppearanceDefinition:
    record = registry.character_appearance.get(appearance_id)
    if record is None:
        raise RegistryError(f"Unknown appearance_id: {appearance_id}")
    return CharacterAppearanceDefinition(
        appearance_id=record["appearance_id"],
        display_name=record["display_name"],
        faction_id=record["faction_id"],
        body_frame=record["body_frame"],
        head_preset=record["head_preset"],
        hair_preset=record["hair_preset"],
        headwear_preset=record["headwear_preset"],
        outfit_preset=record["outfit_preset"],
        voice_preset=record.get("voice_preset"),
        usable_by=tuple(record["usable_by"]),
        identity_item_id=record["identity_item_id"],
        description=record["description"],
    )


def faction_character_rules(registry: DataRegistry, faction_id: str) -> FactionCharacterRules:
    appearances = [
        appearance["appearance_id"]
        for appearance in registry.character_appearance.values()
        if appearance["faction_id"] == faction_id
    ]
    if not appearances:
        raise RegistryError(f"No appearance presets configured for faction {faction_id}")
    return FactionCharacterRules(
        faction_id=faction_id,
        allowed_appearance_ids=tuple(sorted(appearances)),
        starter_identity_item_id=registry.faction(faction_id)["starting_items"][0],
    )


def appearance_presets_for_faction(
    registry: DataRegistry,
    faction_id: str,
    usable_by: str = "player",
) -> list[CharacterAppearanceDefinition]:
    presets = [
        appearance_definition(registry, appearance_id)
        for appearance_id in faction_character_rules(registry, faction_id).allowed_appearance_ids
    ]
    return [preset for preset in presets if usable_by in preset.usable_by]


def can_use_appearance(
    registry: DataRegistry,
    faction_id: str,
    appearance_id: str,
    usable_by: str,
) -> bool:
    preset = appearance_definition(registry, appearance_id)
    return preset.faction_id == faction_id and usable_by in preset.usable_by


def main() -> None:
    registry = load_registry()
    for faction_id in registry.factions:
        presets = appearance_presets_for_faction(registry, faction_id)
        print(f"{faction_id}: {len(presets)} player presets")


if __name__ == "__main__":
    main()
