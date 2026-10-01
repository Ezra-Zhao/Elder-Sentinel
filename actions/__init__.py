"""Action detectors: hand-raise counting, loitering, fall alarm.

Rule-based baselines driven by config/action_thresholds.yaml.
TODO(ezra): field-validate every threshold; consider learned models
for production (these rules are the honest v0.1 starting point).
"""
from .hand_raise import HandRaiseCounter
from .loiter import LoiteringDetector
from .fall import FallDetector

__all__ = ["HandRaiseCounter", "LoiteringDetector", "FallDetector"]
