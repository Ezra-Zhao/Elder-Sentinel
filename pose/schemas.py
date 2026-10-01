"""Skeleton data model.

Coordinates are normalized to [0, 1]; y=0 is the TOP of the image
(standard image coordinates). Every frame carries a `simulated` flag so
downstream consumers (and reports) can never mistake synthetic demo data
for real footage.
"""
from __future__ import annotations

from dataclasses import dataclass, field

JOINTS = (
    "nose",
    "l_shoulder", "r_shoulder",
    "l_elbow", "r_elbow",
    "l_wrist", "r_wrist",
    "l_hip", "r_hip",
    "l_knee", "r_knee",
    "l_ankle", "r_ankle",
)


@dataclass
class SkeletonFrame:
    t: float  # seconds since sequence start
    joints: dict  # name -> (x, y)
    simulated: bool = True

    def joint(self, name: str) -> tuple:
        return self.joints[name]

    def centroid(self) -> tuple:
        """Body centroid from shoulders + hips (stable against limb motion)."""
        pts = [self.joints[n] for n in
               ("l_shoulder", "r_shoulder", "l_hip", "r_hip")]
        return (sum(p[0] for p in pts) / 4, sum(p[1] for p in pts) / 4)

    def hip_height(self) -> float:
        return (self.joints["l_hip"][1] + self.joints["r_hip"][1]) / 2
