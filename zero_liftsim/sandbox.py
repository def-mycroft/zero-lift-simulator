"""Utility helpers used for experimentation and tutorials."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Dict

from .agent import Agent

# State constants used when categorizing agents
state_riding_lift = "riding_lift"
state_in_queue = "in_queue"
state_traversing_down = "traversing_down"


# Explicit mapping from activity log events to the above states
# NOTE: Agent.get_latest_event should return exactly one of these keys in _EVENT_STATE_MAP below
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
        latest_event = agent.get_latest_event(dt)
        results[agent.agent_uuid] = _EVENT_STATE_MAP[latest_event]

    return results
