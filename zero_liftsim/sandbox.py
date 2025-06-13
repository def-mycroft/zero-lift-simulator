"""Utility helpers used for experimentation and tutorials."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Dict

from .agent import Agent

# State constants used when categorizing agents
state_riding_lift = "riding_lift"
state_in_queue = "in_queue"
state_traversing_down = "traversing_down"


def infer_agent_states(agents: Iterable[Agent], dt: datetime) -> Dict[str, str]:
    """Categorize agents based on their activity log at ``dt``.

    Parameters
    ----------
    agents:
        Iterable of :class:`Agent` instances.
    dt:
        Timestamp to evaluate.

    Returns
    -------
    dict
        Mapping of ``agent_uuid`` to one of the three state constants.
    """
    results: Dict[str, str] = {}
    for agent in agents:
        latest_time = None
        latest_event = None
        for entry in agent.activity_log.values():
            t = datetime.fromisoformat(entry["time"])
            if t <= dt and (latest_time is None or t > latest_time):
                latest_time = t
                latest_event = entry.get("event")
        if latest_event == "board":
            state = state_riding_lift # <- this one
        elif latest_event == "ride_complete":
            state = state_traversing_down # <- this one
        else:
            state = state_in_queue # <- this is the problem
        results[agent.agent_uuid] = state
    return results


