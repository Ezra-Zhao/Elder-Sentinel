"""Event data model."""
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class Event:
    type: str        # hand_raise | loiter_alert | fall_alarm
    t: float         # seconds since sequence start
    severity: str    # info | warning | critical
    detail: str
    simulated: bool = True

    def to_dict(self) -> dict:
        return asdict(self)
