import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datetime import datetime, timedelta
from zero_liftsim.main import Agent, Simulation, ArrivalEvent
from zero_liftsim.lift import Lift


def test_wait_and_finish_ride():
    agent = Agent(1)
    start = datetime(2025, 3, 12, 9, 0, 0)
    agent.start_wait(0, start.isoformat())
    agent.boarded = True
    ts = (start + timedelta(minutes=5)).isoformat()
    wait = agent.finish_ride(5, ts)
    assert wait == 5
    assert agent.rides_completed == 1
    assert not agent.boarded


def test_multiple_rides():
    agent = Agent(2)
    start = datetime(2025, 3, 12, 9, 0, 0)
    agent.start_wait(0, start.isoformat())
    agent.boarded = True
    ts1 = (start + timedelta(minutes=3)).isoformat()
    wait1 = agent.finish_ride(3, ts1)
    assert wait1 == 3
    assert agent.rides_completed == 1

    agent.start_wait(10, (start + timedelta(minutes=10)).isoformat())
    agent.boarded = True
    ts2 = (start + timedelta(minutes=15)).isoformat()
    wait2 = agent.finish_ride(15, ts2)
    assert wait2 == 5
    assert agent.rides_completed == 2


def test_activity_log_enabled_via_events():
    sim = Simulation()
    lift = Lift(capacity=1)
    lift.time_spent_ride_lift = lambda: 5
    agent = Agent(3)
    start = datetime(2025, 3, 12, 9, 0, 0)
    agent.start_wait(0, start.isoformat())
    sim.schedule(ArrivalEvent(agent, lift), 0)
    sim.run(start_datetime=start)
    events = [entry["event"] for entry in agent.activity_log.values()]
    assert events == ["start_wait", "arrival", "board", "ride_complete"]
    for entry in agent.activity_log.values():
        datetime.fromisoformat(entry["time"])
    assert "wait_time_readable" in agent.activity_log[3]


def test_activity_log_disabled():
    agent = Agent(4, self_logging=False)
    start = datetime(2025, 3, 12, 9, 0, 0)
    agent.start_wait(0, start.isoformat())
    agent.boarded = True
    agent.finish_ride(5, (start + timedelta(minutes=5)).isoformat())
    assert agent.activity_log == {}

