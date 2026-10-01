"""Threshold config loader."""
import os

import yaml


def load_thresholds(path: str = None) -> dict:
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "action_thresholds.yaml")
    with open(path) as f:
        return yaml.safe_load(f)
