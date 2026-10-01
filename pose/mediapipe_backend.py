"""MediaPipe live-camera backend (STUB — not implemented in scaffold).

TODO(ezra): implement with mediapipe.tasks.vision.PoseLandmarker:
  1. pip install -r requirements-optional.txt
  2. Download the pose_landmarker.task model bundle.
  3. In estimate(): run detection, map the 33 MediaPipe landmarks onto this
     repo's JOINTS subset (pose/schemas.py), and return
     SkeletonFrame(t=..., joints=..., simulated=False).

Mapping hint (MediaPipe -> JOINTS):
  0 nose | 11/12 shoulders | 13/14 elbows | 15/16 wrists |
  23/24 hips | 25/26 knees | 27/28 ankles
"""
from .base import PoseEstimator


class MediaPipeBackend(PoseEstimator):
    def __init__(self, model_path: str):
        raise NotImplementedError(
            "TODO(ezra): wire MediaPipe PoseLandmarker here. "
            "See module docstring for the recipe."
        )

    def estimate(self, image):  # pragma: no cover
        raise NotImplementedError("TODO(ezra): see module docstring.")
