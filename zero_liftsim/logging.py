"""Simple file-based event logger."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime


class Logger:
    """Simple event logger that writes to a file and keeps entries in memory."""

    def __init__(self, filename: str = "main.log") -> None:
        """Create a new logger.

        Parameters
        ----------
        filename:
            Name of the log file inside the ``logs`` directory. The directory
            is created if it does not already exist.
        """

        self._records: list[dict] = []

        logs_dir = Path(__file__).resolve().parents[1] / "logs"
        logs_dir.mkdir(exist_ok=True)
        self._path = logs_dir / filename
        # open in write mode so each run starts with a clean log file
        self._file = open(self._path, "w", encoding="utf-8")

    def log(self, event_name: str, time: int, timestamp: str, **info) -> None:
        """Record an event with optional metadata and write it to file."""

        entry = {
            "event": event_name,
            "time": timestamp,
            "time_offset": time,
        }
        entry.update(info)
        self._records.append(entry)

        self._file.write(json.dumps(entry) + "\n")
        self._file.flush()

    def devlog(self, message: str) -> None:
        """Write a timestamped development message to the log file.

        Parameters
        ----------
        message:
            Arbitrary text to append to the log file.

        Notes
        -----
        ``devlog`` only writes to the file; it does not modify
        :pyattr:`_records`.
        """

        stamp = datetime.now().isoformat()
        self._file.write(f"{stamp} {message}\n")
        self._file.flush()

    def records(self) -> list[dict]:
        """Return collected log entries."""
        return list(self._records)

    def __del__(self) -> None:
        try:
            self._file.close()
        except AttributeError:
            pass
