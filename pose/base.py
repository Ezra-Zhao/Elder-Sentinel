"""Estimator interface: any pose source (camera backend or simulator)
plugs into the detectors by yielding SkeletonFrames."""
from abc import ABC, abstractmethod


class PoseEstimator(ABC):
    @abstractmethod
    def estimate(self, image):
        """Map one camera frame -> SkeletonFrame | None.

        Returns None when no person is detected in the frame.
        Live backends MUST emit SkeletonFrame(simulated=False).
        """
