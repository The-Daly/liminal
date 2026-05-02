#!/usr/bin/env python3
from collections import defaultdict, deque
from typing import Optional

from item_registry import DataRegistry, RegistryError, load_registry


def get_layout(registry: DataRegistry, level_id: str) -> dict:
    layout = registry.level_layouts.get(level_id)
    if layout is None:
        raise RegistryError(f"Unknown level_id: {level_id}")
    return layout


def faction_foothold_zones(registry: DataRegistry, level_id: str) -> dict[str, str]:
    layout = get_layout(registry, level_id)
    return {entry["faction_id"]: entry["zone_id"] for entry in layout.get("faction_footholds", [])}


def shortest_route_seconds(registry: DataRegistry, level_id: str, start_zone_id: str, end_zone_id: str) -> Optional[int]:
    layout = get_layout(registry, level_id)
    graph = defaultdict(list)
    for route in layout.get("routes", []):
        graph[route["from_zone_id"]].append((route["to_zone_id"], route["estimated_seconds"]))
        graph[route["to_zone_id"]].append((route["from_zone_id"], route["estimated_seconds"]))

    best = {start_zone_id: 0}
    queue = deque([start_zone_id])
    while queue:
        zone = queue.popleft()
        for next_zone, seconds in graph[zone]:
            candidate = best[zone] + seconds
            if next_zone not in best or candidate < best[next_zone]:
                best[next_zone] = candidate
                queue.append(next_zone)
    return best.get(end_zone_id)


def main() -> None:
    registry = load_registry()
    level_id = "level1_service_halls"
    footholds = faction_foothold_zones(registry, level_id)
    print(f"{level_id}: {len(footholds)} faction footholds")
    for faction_id, zone_id in footholds.items():
        print(f"{faction_id}: {zone_id}")


if __name__ == "__main__":
    raise SystemExit(main())
