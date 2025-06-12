import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.main import Agent, Simulation, Lift, ArrivalEvent


def test_wait_and_finish_ride():
    agent = Agent(1)
    agent.start_wait(0)
    agent.boarded = True
    wait = agent.finish_ride(5)
    assert wait == 5
    assert agent.rides_completed == 1
    assert not agent.boarded


def test_multiple_rides():
    agent = Agent(2)
    agent.start_wait(0)
    agent.boarded = True
    wait1 = agent.finish_ride(3)
    assert wait1 == 3
    assert agent.rides_completed == 1

    agent.start_wait(10)
    agent.boarded = True
    wait2 = agent.finish_ride(15)
    assert wait2 == 5
    assert agent.rides_completed == 2


def test_activity_log_enabled_via_events():
    sim = Simulation()
    lift = Lift(capacity=1, cycle_time=5)
    agent = Agent(3)
    agent.start_wait(0)
    sim.schedule(ArrivalEvent(agent, lift), 0)
    sim.run()
    events = [entry["event"] for entry in agent.activity_log.values()]
    assert events == ["start_wait", "arrival", "board", "ride_complete"]


def test_activity_log_disabled():
    agent = Agent(4, self_logging=False)
    agent.start_wait(0)
    agent.boarded = True
    agent.finish_ride(5)
    assert agent.activity_log == {}

