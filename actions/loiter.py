"""Loitering detector.

Tracks the body centroid over a sliding window of `dwell_time_sec`.
If the centroid never leaves a `radius` box for the whole window, emit
one loiter_alert (re-arms once the person moves away).

TODO(ezra): field-validate dwell_time_sec / radius; production version
should gate on zone polygons (kitchen, stairwell, exit), not the whole frame.
"""
from events import Event


class LoiteringDetector:
    def __init__(self, cfg: dict):
        self.dwell = cfg.get("dwell_time_sec", 30.0)
        self.radius = cfg.get("radius", 0.08)
        self._window = []  # (t, x, y)
        self._alerted = False

    def update(self, frame) -> list:
        cx, cy = frame.centroid()
        self._window.append((frame.t, cx, cy))
        cutoff = frame.t - self.dwell
        self._window = [p for p in self._window if p[0] >= cutoff]
        if len(self._window) < 2:
            return []
        xs = [p[1] for p in self._window]
        ys = [p[2] for p in self._window]
        span = max(max(xs) - min(xs), max(ys) - min(ys))
        dur = self._window[-1][0] - self._window[0][0]
        if span > self.radius:
            self._alerted = False  # person moved — re-arm
            return []
        if dur >= self.dwell and not self._alerted:
            self._alerted = True
            return [Event(
                type="loiter_alert", t=frame.t, severity="warning",
                detail=(f"stationary {dur:.1f}s within radius {self.radius} "
                        f"(threshold {self.dwell:.0f}s)"),
                simulated=frame.simulated)]
        return []
