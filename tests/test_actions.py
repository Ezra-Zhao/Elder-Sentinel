"""Unit tests — all on SIMULATED skeleton sequences (deterministic seeds)."""
from actions import HandRaiseCounter, LoiteringDetector, FallDetector
from config import load_thresholds
from pose.simulator import (make_hand_raise_sequence, make_loiter_sequence,
                            make_fall_sequence)

CFG = load_thresholds()


def _run(frames, detectors):
    events = []
    for f in frames:
        assert f.simulated, "test data must be labeled simulated"
        for d in detectors:
            events.extend(d.update(f))
    return events


def test_hand_raise_counts_three_per_side():
    counter = HandRaiseCounter(CFG["hand_raise"])
    events = _run(make_hand_raise_sequence(n_raises=3), [counter])
    assert counter.count == {"left": 3, "right": 3}
    assert len([e for e in events if e.type == "hand_raise"]) == 6


def test_loiter_alert_fires_once():
    cfg = {"dwell_time_sec": 3.0, "radius": 0.08}
    events = _run(make_loiter_sequence(dwell_sec=5.0), [LoiteringDetector(cfg)])
    alerts = [e for e in events if e.type == "loiter_alert"]
    assert len(alerts) == 1
    assert alerts[0].severity == "warning"


def test_fall_alarm_is_critical():
    events = _run(make_fall_sequence(), [FallDetector(CFG["fall"])])
    alarms = [e for e in events if e.type == "fall_alarm"]
    assert len(alarms) == 1
    assert alarms[0].severity == "critical"


def test_no_fall_alarm_without_fall():
    # Loitering (no collapse) must not trigger the fall detector.
    events = _run(make_loiter_sequence(dwell_sec=5.0), [FallDetector(CFG["fall"])])
    assert not [e for e in events if e.type == "fall_alarm"]


def test_config_has_all_sections():
    assert set(CFG) >= {"hand_raise", "loitering", "fall"}
