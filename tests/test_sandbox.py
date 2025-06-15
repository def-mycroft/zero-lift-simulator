import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.agent import Agent
from zero_liftsim.agent_state_id import (
    infer_agent_states,
    state_riding_lift,
    state_in_queue,
    state_traversing_down,
    UnknownEventError,
)
import pytest


def test_infer_agent_states_basic():
    agent = Agent(1)
    start = datetime(2025, 3, 12, 9, 0, 0)
    agent.start_wait(0, start.isoformat())
    agent.log_event("arrival", 0, start.isoformat())
    agent.log_event("board", 1, (start + timedelta(minutes=1)).isoformat())

    dt = start + timedelta(minutes=2)
    result = infer_agent_states([agent], dt)
    assert result[agent.agent_uuid] == state_riding_lift

    agent.log_event("ride_complete", 5, (start + timedelta(minutes=5)).isoformat())
    dt2 = start + timedelta(minutes=5, seconds=30)
    result2 = infer_agent_states([agent], dt2)
    assert result2[agent.agent_uuid] == state_traversing_down

    agent.start_wait(7, (start + timedelta(minutes=7)).isoformat())
    dt3 = start + timedelta(minutes=8)
    result3 = infer_agent_states([agent], dt3)
    assert result3[agent.agent_uuid] == state_in_queue


def test_infer_agent_states_unknown_event():
    agent = Agent(2)
    start = datetime(2025, 3, 12, 9, 0, 0)
    agent.log_event("foo", 0, start.isoformat())
    with pytest.raises(UnknownEventError):
        infer_agent_states([agent], start)
