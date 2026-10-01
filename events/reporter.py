"""EventReporter: collects detector outputs, renders console + JSON reports."""
import json


class EventReporter:
    def __init__(self, source: str = "simulated"):
        self.source = source
        self.events = []

    def add_many(self, events: list) -> None:
        self.events.extend(events)

    def summary(self) -> dict:
        counts = {}
        for e in self.events:
            counts[e.type] = counts.get(e.type, 0) + 1
        return {
            "source": self.source,
            "total_events": len(self.events),
            "by_type": counts,
            "critical": [e.to_dict() for e in self.events
                         if e.severity == "critical"],
        }

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "simulated": all(e.simulated for e in self.events) if self.events else True,
            "events": [e.to_dict() for e in self.events],
            "summary": self.summary(),
        }

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def print_console(self) -> None:
        s = self.summary()
        print(f"[{self.source}] {s['total_events']} events: {s['by_type']}")
        for e in self.events:
            if e.severity != "info":
                print(f"  ! [{e.severity.upper()}] t={e.t:6.1f}s "
                      f"{e.type}: {e.detail}")
