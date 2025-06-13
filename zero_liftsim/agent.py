from __future__ import annotations

from uuid import uuid4 as uuid
from datetime import datetime, timedelta

try:
    from codenamize import codenamize
except ModuleNotFoundError:  # pragma: no cover
    def codenamize(value: str) -> str:
        return value[:8]

from .logging import Logger
from .experience import AgentRideLoopExperience


class Agent:
    """Represents an individual skier within the simulation."""

    def __init__(
        self,
        agent_id: int,
        logger: "Logger" | None = None,
        self_logging: bool = True,
    ) -> None:
        self.agent_id = agent_id
        self.agent_uuid = str(uuid())
        self.agent_uuid_codename = codenamize(self.agent_uuid)
        self.boarded: bool = False
        self.wait_start: int | None = None
        self.board_time: int | None = None
        self.rides_completed: int = 0
        self.self_logging = self_logging
        self.activity_log: dict[int, dict] = {}
        self.experience_rideloop = AgentRideLoopExperience()
        if logger is not None:
            logger.devlog(
                f"init agent {self.agent_uuid} {self.agent_uuid_codename}"
            )
            self.logger = logger

    def log_event(self, event: str, time: int, timestamp: str,
                  return_event_uuid='', **info) -> None:
        """Append a record to :pyattr:`activity_log` if self logging is enabled."""

        if not self.self_logging:
            return
        record = {
            "return_event_uuid":return_event_uuid,
            "time": timestamp,
            "time_offset": time,
            "event": event,
            "agent_id": self.agent_id,
            "agent_uuid": self.agent_uuid,
            "agent_uuid_codename": self.agent_uuid_codename,
        }
        record.update(info)
        self.activity_log[len(self.activity_log)] = record

    def start_wait(self, time: int, timestamp: str) -> None:
        """Record the time the agent begins waiting in the queue."""

        self.wait_start = time
        self.log_event("start_wait", time, timestamp)

    def finish_ride(self, time: int, timestamp: str, return_event_uuid='') -> int:
        """Mark the current ride complete and return the wait time."""

        wait_start = self.wait_start if self.wait_start is not None else time
        wait_time = time - wait_start
        self.rides_completed += 1
        self.boarded = False
        self.wait_start = None
        self.log_event(
            "ride_complete",
            time,
            timestamp,
            wait_time=wait_time,
            wait_time_readable=f"{wait_time} minutes",
            return_event_uuid=return_event_uuid,
        )
        return wait_time

    def __repr__(self) -> str:  # pragma: no cover - convenience
        return f"Agent({self.agent_id}) {self.agent_uuid_codename} {self.agent_uuid}"
