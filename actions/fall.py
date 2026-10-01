"""Fall detector (critical alarm).

Watches hip height: if it drops by drop_ratio of the standing baseline
within drop_time_sec, emit a fall_alarm. Baseline comes from config
(standing_hip_y) with a first-frames calibration fallback.

TODO(ezra): field-validate drop_ratio / drop_time_sec; production should
add a post-fall stillness check to cut false positives (sitting down fast
vs. collapsing) and calibrate baseline per camera.
"""
from events import Event


class FallDetector:
    def __init__(self, cfg: dict):
        self.drop_ratio = cfg.get("drop_ratio", 0.45)
        self.drop_time = cfg.get("drop_time_sec", 1.0)
        self.baseline = cfg.get("standing_hip_y")  # may be None -> calibrate
        self._history = []  # (t, hip_y)
        self._alarmed = False

    def _ensure_baseline(self, frame):
        if self.baseline is None:
            self._history.append((frame.t, frame.hip_height()))
            if len(self._history) >= 30:
                ys = sorted(p[1] for p in self._history)
                self.baseline = ys[len(ys) // 2]  # median of first 30 frames

    def update(self, frame) -> list:
        self._ensure_baseline(frame)
        if self.baseline is None:
            return []  # still calibrating
        hip = frame.hip_height()
        self._history.append((frame.t, hip))
        cutoff = frame.t - self.drop_time
        self._history = [p for p in self._history if p[0] >= cutoff]
        if len(self._history) < 2:
            return []
        drop = hip - self._history[0][1]  # y grows downward
        dur = self._history[-1][0] - self._history[0][0]
        if not self._alarmed and drop >= self.baseline * self.drop_ratio:
            self._alarmed = True
            return [Event(
                type="fall_alarm", t=frame.t, severity="critical",
                detail=(f"hip height dropped {drop:.2f} "
                        f"({drop / self.baseline:.0%} of baseline) in {dur:.2f}s"),
                simulated=frame.simulated)]
        return []
