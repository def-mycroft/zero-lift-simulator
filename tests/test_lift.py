import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.main import Agent, Lift


def test_fifo_loading_and_capacity():
    lift = Lift(capacity=2, cycle_time=5)
    a1, a2, a3 = Agent(1), Agent(2), Agent(3)
    lift.enqueue(a1)
    lift.enqueue(a2)
    lift.enqueue(a3)

    boarded = lift.load()
    assert [a.agent_id for a in boarded] == [1, 2]
    assert all(a.boarded for a in boarded)
    assert lift.queue_length() == 1
    assert lift.state == "moving"


def test_state_transitions():
    lift = Lift(capacity=1, cycle_time=3)
    a1 = Agent(1)
    lift.enqueue(a1)
    assert lift.state == "idle"
    lift.load()
    assert lift.state == "moving"
    lift.mark_idle()
    assert lift.state == "idle"


def test_load_when_fewer_agents_than_capacity():
    lift = Lift(capacity=3, cycle_time=5)
    a1 = Agent(1)
    lift.enqueue(a1)

    boarded = lift.load()
    assert boarded == [a1]
    assert lift.queue_length() == 0
    assert lift.state == "moving"
