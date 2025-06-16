"""Utility helpers used for experimentation and tutorials."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Dict, TYPE_CHECKING, Union


class UnknownEventError(Exception):
    """Raised when :func:`infer_agent_states` encounters an unknown event."""

if TYPE_CHECKING:  # pragma: no cover - for type hints only
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

def infer_agent_states(
    agents: Union["Agent", Iterable["Agent"]],
    dt: datetime
) -> Dict[str, str]:
    """Categorize agents based on their latest event at a given time.

    Evaluates each agent's most recent activity and assigns a semantic
    state label such as 'in_queue', 'riding_lift', or 'traversing_down'.

    Parameters
    ----------
    agents : Agent or iterable of Agent
        One or more agents to evaluate.
    dt : datetime
        The timestamp at which to evaluate each agent's latest event.

    Returns
    -------
    dict of str to str
        Mapping from agent UUID to inferred state.

    Raises
    ------
    UnknownEventError
        If an agent's latest event is not recognized.
    """
    from .agent import Agent

    results: Dict[str, str] = {}
    if isinstance(agents, Agent):
        agents = [agents]
    for agent in agents:
        latest_event = agent.get_latest_event(dt)
        if latest_event not in _EVENT_STATE_MAP:
            raise UnknownEventError(latest_event)
        results[agent.agent_uuid] = _EVENT_STATE_MAP[latest_event]

    return results

