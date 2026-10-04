# Elder-Sentinel

**Pose-based action recognition for elder-care safety monitoring.**

A real-time pipeline that watches body movement — not identity — and flags
safety-relevant events: help-seeking gestures, wandering into off-limits
areas, and falls. Built for the realities of care homes, where caregivers
can't be in every room at once, and where a fall detected minutes earlier
can save a life.

> **Project status: scaffold v0.1 (honest edition).**
> The end-to-end pipeline runs today on **procedurally generated, simulated**
> skeleton sequences. What is real: pose data model, rule-based action detectors
> (hand-raise counting, loitering, fall alarm), event reporting.
> What is still TODO (clearly marked in code): the field-validated action
> thresholds and the MediaPipe live-camera backend. This repo contains
> **no face recognition and no identity matching** — pose only.

---

## Background

In a care home, caregivers can't watch every room at once. This system
defines measurable *action standards* — e.g. "hand raised above shoulder
N times in M seconds" as a call-for-help signal, "resident stationary
near a stairwell or exit for T seconds", "sudden vertical drop consistent
with a fall" — and raises alerts the moment a live pose stream matches
one. The same architecture applies anywhere safety depends on body
movement without identifying the person: elder-care fall detection,
hospital ward monitoring, assisted-living wandering alerts.

## What it does

| Module | Input | Output |
|---|---|---|
| Pose estimation | camera frame (or simulated skeleton) | `SkeletonFrame` joint coordinates |
| Hand-raise counter | wrist/shoulder trajectories | count + timestamps per side |
| Loitering detector | body centroid trajectory | `loiter_alert` after dwell threshold |
| Fall detector | hip-height trajectory | `fall_alarm` (critical) on sudden drop |
| Event reporter | all detector outputs | console summary + JSON report |

## Architecture

```
                +------------------+
                |  Pose source     |
                |  MediaPipe cam   |  (TODO: live backend)
                |  Simulated seq   |  <-- demo runs on this
                +--------+---------+
                         | SkeletonFrame stream
          +--------------+--------------+
          |              |              |
   HandRaiseCounter LoiteringDetector FallDetector
   (config thresholds — TODO: field values)
          |              |              |
          +--------------+--------------+
                         v
                  EventReporter
                  console + report.json
```

## Quickstart

```bash
cd Elder-Sentinel
pip install -r requirements.txt
python examples/demo.py        # simulated end-to-end demo
python -m pytest tests/ -q     # unit tests
```

The demo runs three simulated scenarios — hand raises, loitering, a fall —
and writes `examples/demo_report.json`.

## Configuration

All action thresholds live in `config/action_thresholds.yaml`. The shipped
values are **placeholders**, not standards:

```yaml
hand_raise:
  raise_margin: 0.05   # TODO(ezra): field-validated value
```

**TODO(ezra):** replace every threshold with values validated from your real
deployments (raise margins, dwell times, drop ratios, zone geometry). The
detectors are deliberately dumb rules — your experience is what makes them
trustworthy. Do not present placeholder values as operational standards.

## Live camera backend (TODO)

`pose/mediapipe_backend.py` is a stub. To go live:

1. `pip install -r requirements-optional.txt` (MediaPipe + OpenCV)
2. Implement `MediaPipeBackend.estimate()` mapping the 33 MediaPipe pose
   landmarks onto this repo's joint set, emitting `SkeletonFrame(simulated=False)`.

## Ethics & lawful use

- **Pose only.** This repository contains no face recognition, no identity
  matching, and no person re-identification. It answers "what is the body
  doing", never "who is this".
- **Authorized safety use only.** Intended solely for lawful, authorized safety
  deployments (e.g. licensed elder-care facilities, with family/guardian
  consent). Do not use for covert surveillance, and do not deploy without
  proper legal authorization and oversight.
- **Simulated data.** Every demo frame is procedurally generated and labeled
  `simulated: true`. Nothing here was recorded from real people.

## Roadmap

- [ ] Field-validated thresholds (Ezra's deployment experience)
- [ ] MediaPipe live backend + zone polygons on floor plans
- [ ] Multi-person tracking (ID by track, not by face)
- [ ] Alert routing (SMS/dashboard webhook)
- [ ] Recurring-pattern analytics (e.g. agitation escalation over hours)
