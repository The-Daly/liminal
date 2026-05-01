#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional


class SanityError(ValueError):
    pass


@dataclass
class SanityState:
    current: float
    minimum: int
    maximum: int
    low_threshold: int
    drain_per_minute: float
    almond_water_restore: int

    @classmethod
    def from_rule(cls, rule: dict, starting_sanity: Optional[int] = None) -> "SanityState":
        maximum = int(rule["max_sanity"])
        minimum = int(rule["min_sanity"])
        current = maximum if starting_sanity is None else starting_sanity
        if current < minimum or current > maximum:
            raise SanityError("Starting sanity is outside the configured range")
        return cls(
            current=float(current),
            minimum=minimum,
            maximum=maximum,
            low_threshold=int(rule["low_sanity_threshold"]),
            drain_per_minute=float(rule["base_drain_per_minute"]),
            almond_water_restore=int(rule.get("almond_water_restore", 0)),
        )

    @property
    def is_low(self) -> bool:
        return self.current <= self.low_threshold

    def drain_seconds(self, seconds: float) -> None:
        if seconds < 0:
            raise SanityError("Seconds cannot be negative")
        self.current = max(self.minimum, self.current - (self.drain_per_minute / 60.0) * seconds)

    def consume_almond_water(self) -> None:
        self.current = min(self.maximum, self.current + self.almond_water_restore)
