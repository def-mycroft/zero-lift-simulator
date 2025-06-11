class Logger:
    """Simple in-memory event logger."""

    def __init__(self) -> None:
        self._records: list[dict] = []

    def log(self, event_name: str, time: int, **info) -> None:
        """Record an event with optional metadata."""
        entry = {"event": event_name, "time": time}
        entry.update(info)
        self._records.append(entry)

    def records(self) -> list[dict]:
        """Return collected log entries."""
        return list(self._records)
