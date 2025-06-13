"""Simulation engine for Zero Lift."""

from __future__ import annotations

import heapq
from uuid import uuid4 as uuid
from datetime import datetime, timedelta

try:
    from codenamize import codenamize
except ModuleNotFoundError:  # pragma: no cover
    def codenamize(value: str) -> str:
        return value[:8]

from .agent import Agent
from .lift import Lift
from .logging import Logger
from .events import Event, ArrivalEvent, BoardingEvent, ReturnEvent


class Simulation:
    """Discrete-event simulation engine."""

    def __init__(self) -> None:
        self.current_time: int = 0
        self._counter: int = 0
        self._queue: list[tuple[int, int, Event]] = []
        self._agent_logger: Logger | None = None
        self._agent_records: list[dict] = []
        self.simulation_uuid = str(uuid())
        self.simulation_codename = codenamize(self.simulation_uuid)
        self.stop_time: int | None = None

    def schedule(self, event: Event, time: int) -> None:
        """Schedule ``event`` at ``time``."""
        heapq.heappush(self._queue, (time, self._counter, event))
        self._counter += 1

    def run(
        self,
        stop_time: int | None = None,
        logger: Logger | None = None,
        *,
        full_agent_logging: bool = False,
        start_datetime: datetime = datetime(2025, 3, 12, 9, 0, 0),
    ) -> None:
        """Execute scheduled events."""
        self.start_datetime = start_datetime
        self.stop_time = stop_time
        if full_agent_logging:
            self._agent_logger = Logger("agent.log")
            self._agent_records = []
        else:
            self._agent_logger = None
            self._agent_records = []

        while self._queue:
            time, _, event = heapq.heappop(self._queue)
            if stop_time is not None and time > stop_time:
                self.current_time = stop_time
                break
            self.current_time = time
            if logger is not None:
                q_len = getattr(event, "lift", None)
                q_len = q_len.queue_length() if q_len else 0
                timestamp = (self.start_datetime + timedelta(minutes=time)).isoformat()
                logger.log(
                    event.__class__.__name__,
                    time,
                    timestamp,
                    queue_length=q_len,
                )
            new_events = event.execute(self)
            if new_events:
                for evt, evt_time in new_events:
                    self.schedule(evt, evt_time)

        self._agent_logger = None

    def agent_records(self) -> list[dict]:
        """Return collected agent-level log entries."""
        return list(self._agent_records)


def run_alpha_sim(
    n_agents: int,
    lift_capacity: int,
    *,
    start_datetime: datetime | None = None,
    runtime_minutes: int | None = None,
) -> dict:
    """Run a small simulation and return metrics."""
    from zero_liftsim.simmanager import SimulationManager

    manager = SimulationManager(
        n_agents=n_agents,
        lift_capacity=lift_capacity,
        start_datetime=start_datetime,
    )
    return manager.run(runtime_minutes=runtime_minutes)
