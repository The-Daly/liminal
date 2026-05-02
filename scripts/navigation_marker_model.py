#!/usr/bin/env python3
from item_registry import DataRegistry, RegistryError, load_registry


def marker_expires_at(created_at_seconds: int, duration_seconds: int) -> int:
    return created_at_seconds + duration_seconds


def is_marker_expired(created_at_seconds: int, now_seconds: int, duration_seconds: int) -> bool:
    return now_seconds >= marker_expires_at(created_at_seconds, duration_seconds)


def marker_visibility(registry: DataRegistry, marker_id: str) -> str:
    marker = registry.navigation_markers.get(marker_id)
    if marker is None:
        raise RegistryError(f"Unknown marker_id: {marker_id}")
    return marker["visibility"]


def main() -> None:
    registry = load_registry()
    for marker_id, marker in registry.navigation_markers.items():
        print(f"{marker_id}: {marker['duration_seconds']} seconds, {marker['visibility']}")


if __name__ == "__main__":
    main()
