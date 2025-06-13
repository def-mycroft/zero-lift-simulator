"""Utility helpers used for experimentation and tutorials."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Dict

from .agent import Agent

# State constants used when categorizing agents
state_riding_lift = "state_riding_lift"
state_in_queue = "state_in_queue"
state_traversing_down = "state_traversing_down"

# Explicit mapping from activity log events to the above states
_EVENT_STATE_MAP = {
    "board": state_riding_lift,
    "ride_complete": state_traversing_down,
    "start_wait": state_in_queue,
    "arrival": state_in_queue,
}

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

        if latest_event is None:
            # if no event has occurred yet, the agent is still waiting in queue
            state = state_in_queue
        else:
            state = _EVENT_STATE_MAP.get(latest_event, state_in_queue)
        results[agent.agent_uuid] = state
    return results
