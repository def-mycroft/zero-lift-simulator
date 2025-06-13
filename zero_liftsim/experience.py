from __future__ import annotations

from datetime import datetime
from uuid import uuid4 as uuid


class AgentExperienceHistory:
    """Base class for tracking per-agent experience data."""

    def __init__(self) -> None:
        self.log: dict[datetime, dict] = {}


class AgentRideLoopExperience(AgentExperienceHistory):
    """Record time costs for a single ride loop.

    This log is intended to serve as a measurement collector and 
    will be a primary one for the codebase for the conceivable 
    future of the project. For example, if we want to infer a prob
    distribution of the time spent in queue for a day per rider, 
    then we're going to generate a simulation and retrieve agent 
    log here and sum time_spent_in_queue. 

    This class extends `AgentExperienceHistory` to log detailed timing
    information for each segment of an agent's lift ride loop. Each
    log entry includes time spent riding the lift, descending the
    mountain, and waiting in queue.

    Entries are stored in `self.log` using timestamps as keys. The
    recorded values enable time-based analysis of per-agent flow
    through the lift system.

    Parameters
    ----------
    dt : datetime
        Timestamp marking when the ride loop completed or was
        recorded.
    ride : float
        Time spent riding the lift, in minutes.
    traverse : float
        Time spent traversing or descending after lift exit, in
        minutes.
    queue : float
        Time spent waiting in queue for the lift, in minutes.
    """
    def add_entry(self, agent, return_event_uuid, dt: datetime, ride: float, traverse: float, 
                  queue: float) -> None:
        self.log[dt] = {
            "exp_id": str(uuid()), 
            "return_event_uuid": return_event_uuid,
            "agent_uuid": agent.agent_uuid,
            "agent_uuid_codename": agent.agent_uuid_codename,
            "time_spent_ride_lift": ride,
            "time_spent_traverse_down_mountain": traverse,
            "time_spent_in_queue": queue,
            "time_spent_total": ride + traverse + queue,
        }
