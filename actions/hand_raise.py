"""Hand-raise counter.

A raise = wrist rises above (shoulder - raise_margin) and holds for
min_hold_frames, then comes back down. Counts completed up->down cycles
per side — e.g. "resident waved right hand 4 times in the last minute"
(call-for-help signal).

TODO(ezra): field-validate raise_margin / min_hold_frames; consider
per-camera calibration (angle changes apparent geometry).
"""
from events import Event


class HandRaiseCounter:
    def __init__(self, cfg: dict):
        self.margin = cfg.get("raise_margin", 0.05)
        self.min_hold = cfg.get("min_hold_frames", 3)
        self._state = {"left": "down", "right": "down"}
        self._hold = {"left": 0, "right": 0}
        self.count = {"left": 0, "right": 0}

    def update(self, frame) -> list:
        events = []
        pairs = (("left", "l_wrist", "l_shoulder"),
                 ("right", "r_wrist", "r_shoulder"))
        for side, wrist, shoulder in pairs:
            raised = (frame.joint(wrist)[1]
                      < frame.joint(shoulder)[1] - self.margin)
            if raised:
                self._hold[side] += 1
                if self._state[side] == "down" and self._hold[side] >= self.min_hold:
                    self._state[side] = "up"
            else:
                if self._state[side] == "up":
                    self.count[side] += 1
                    events.append(Event(
                        type="hand_raise", t=frame.t, severity="info",
                        detail=f"{side} hand raise #{self.count[side]}",
                        simulated=frame.simulated))
                self._state[side] = "down"
                self._hold[side] = 0
        return events

    @property
    def total(self) -> int:
        return self.count["left"] + self.count["right"]
