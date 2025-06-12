from __future__ import annotations

from datetime import datetime


class AgentExperience:
    """Base class for tracking per-agent experience data."""

    def __init__(self) -> None:
        self.log: dict[datetime, dict] = {}


class AgentRideLoopExperience(AgentExperience):
    """Record time costs for a single ride loop."""

    def add_entry(self, dt: datetime, ride: float, traverse: float, queue: float) -> None:
        self.log[dt] = {
            "time_cost_ride_lift": ride,
            "time_cost_traverse_down_mountain": traverse,
            "time_cost_in_queue": queue,
        }
