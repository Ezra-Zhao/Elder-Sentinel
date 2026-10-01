"""Procedural skeleton-sequence generator (SIMULATED data).

Produces deterministic, clearly-labeled synthetic pose sequences for the demo
and tests. No real footage, no real people — every emitted frame has
simulated=True.
"""
import math
import random

from .schemas import SkeletonFrame

# Reference standing pose, normalized coords (y=0 at top).
_STANDING = {
    "nose": (0.50, 0.12),
    "l_shoulder": (0.42, 0.28), "r_shoulder": (0.58, 0.28),
    "l_elbow": (0.38, 0.42), "r_elbow": (0.62, 0.42),
    "l_wrist": (0.36, 0.55), "r_wrist": (0.64, 0.55),
    "l_hip": (0.44, 0.62), "r_hip": (0.56, 0.62),
    "l_knee": (0.44, 0.78), "r_knee": (0.56, 0.78),
    "l_ankle": (0.44, 0.95), "r_ankle": (0.56, 0.95),
}

_RAISED_WRIST_Y = 0.14  # well above shoulder line (0.28 - margin 0.05)


def _jittered(base: dict, rng: random.Random, amt: float = 0.004) -> dict:
    return {k: (x + rng.uniform(-amt, amt), y + rng.uniform(-amt, amt))
            for k, (x, y) in base.items()}


def _frame(t: float, joints: dict) -> SkeletonFrame:
    # Round timestamps: avoids float-accumulation drift breaking
    # duration comparisons in detectors (e.g. 34.900000000000226).
    return SkeletonFrame(t=round(t, 4), joints=joints, simulated=True)


def make_hand_raise_sequence(n_raises: int = 3, fps: int = 15,
                             seed: int = 7, side: str = "both") -> list:
    """Both (or one) hands rise above the shoulder `n_raises` times."""
    rng = random.Random(seed)
    frames, t = [], 0.0
    dt = 1.0 / fps
    sides = ("l", "r") if side == "both" else (side,)
    for _ in range(n_raises):
        # 1.0 s raise cycle: wrist 0.55 -> 0.14 -> 0.55 (sine profile)
        steps = fps
        for i in range(steps):
            p = i / steps
            lift = math.sin(math.pi * p)  # 0 -> 1 -> 0
            pose = dict(_STANDING)
            for s in sides:
                wy = 0.55 - (0.55 - _RAISED_WRIST_Y) * lift
                ey = 0.42 - (0.42 - 0.20) * lift
                pose[f"{s}_wrist"] = (pose[f"{s}_wrist"][0], wy)
                pose[f"{s}_elbow"] = (pose[f"{s}_elbow"][0], ey)
            frames.append(_frame(t, _jittered(pose, rng)))
            t += dt
        # 0.5 s rest between raises
        for _ in range(fps // 2):
            frames.append(_frame(t, _jittered(_STANDING, rng)))
            t += dt
    return frames


def make_loiter_sequence(dwell_sec: float = 35.0, fps: int = 10,
                         seed: int = 11) -> list:
    """Person shuffles inside a small box (stays 'stationary')."""
    rng = random.Random(seed)
    frames, t = [], 0.0
    dt = 1.0 / fps
    ox, oy = 0.0, 0.0  # offset from reference, clamped to +-0.03
    n = int(dwell_sec * fps)
    for _ in range(n):
        ox = max(-0.03, min(0.03, ox + rng.uniform(-0.004, 0.004)))
        oy = max(-0.03, min(0.03, oy + rng.uniform(-0.004, 0.004)))
        pose = {k: (x + ox, y + oy) for k, (x, y) in _STANDING.items()}
        frames.append(_frame(t, _jittered(pose, rng)))
        t += dt
    return frames


def make_fall_sequence(fps: int = 15, seed: int = 13) -> list:
    """2 s standing, 0.7 s collapse, 2 s lying still."""
    rng = random.Random(seed)
    frames, t = [], 0.0
    dt = 1.0 / fps

    def lerp(a, b, p):
        return a + (b - a) * p

    # Phase 1: standing with slight sway
    for _ in range(2 * fps):
        frames.append(_frame(t, _jittered(_STANDING, rng, amt=0.003)))
        t += dt
    # Phase 2: collapse — hips/shoulders/head drop, arms splay
    fallen = {
        "nose": (0.50, 0.52),
        "l_shoulder": (0.38, 0.66), "r_shoulder": (0.62, 0.66),
        "l_elbow": (0.30, 0.72), "r_elbow": (0.70, 0.72),
        "l_wrist": (0.24, 0.76), "r_wrist": (0.76, 0.76),
        "l_hip": (0.44, 0.92), "r_hip": (0.56, 0.92),
        "l_knee": (0.50, 0.92), "r_knee": (0.54, 0.92),
        "l_ankle": (0.46, 0.94), "r_ankle": (0.54, 0.94),
    }
    steps = int(0.7 * fps)
    for i in range(steps):
        p = (i + 1) / steps
        pose = {k: (lerp(_STANDING[k][0], fallen[k][0], p),
                    lerp(_STANDING[k][1], fallen[k][1], p))
                for k in _STANDING}
        frames.append(_frame(t, _jittered(pose, rng)))
        t += dt
    # Phase 3: lying still
    for _ in range(2 * fps):
        frames.append(_frame(t, _jittered(fallen, rng, amt=0.002)))
        t += dt
    return frames
