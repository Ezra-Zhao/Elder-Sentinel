"""Demo: three SIMULATED scenarios through the full pipeline.

Scenario 1: resident waves for help 3x      -> hand_raise counts
Scenario 2: resident wanders / dwells 35 s in one spot
                                            -> loiter_alert (warning)
Scenario 3: resident collapses              -> fall_alarm (critical)

All input data is procedurally generated (pose/simulator.py) and every
frame/event is labeled simulated=True. Writes examples/demo_report.json.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from actions import HandRaiseCounter, LoiteringDetector, FallDetector
from config import load_thresholds
from events import EventReporter
from pose.simulator import (make_hand_raise_sequence, make_loiter_sequence,
                            make_fall_sequence)


def run_scenario(name: str, frames: list, detectors: list,
                 reporter: EventReporter) -> None:
    print(f"\n--- {name} ({len(frames)} frames, SIMULATED) ---")
    for frame in frames:
        for det in detectors:
            reporter.add_many(det.update(frame))
    reporter.print_console()


def main() -> None:
    cfg = load_thresholds()
    reporter = EventReporter(source="simulated-demo")

    run_scenario("help-seeking wave x3",
                 make_hand_raise_sequence(n_raises=3),
                 [HandRaiseCounter(cfg["hand_raise"])], reporter)
    run_scenario("wandering/dwelling 35s",
                 make_loiter_sequence(dwell_sec=35.0),
                 [LoiteringDetector(cfg["loitering"])], reporter)
    run_scenario("fall",
                 make_fall_sequence(),
                 [FallDetector(cfg["fall"])], reporter)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "demo_report.json")
    reporter.save(out)
    print(f"\nFull report -> {out}")
    print("Summary:", reporter.summary()["by_type"])


if __name__ == "__main__":
    main()
