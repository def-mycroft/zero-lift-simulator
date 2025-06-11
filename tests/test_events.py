import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.main import Agent, ArrivalEvent, BoardingEvent, ReturnEvent, Lift, Simulation


def test_single_agent_cycle():
    log = []
    sim = Simulation()
    lift = Lift(capacity=1, cycle_time=5)
    agent = Agent(1)

    class LogArrivalEvent(ArrivalEvent):
        def execute(self, s):
            events = super().execute(s)
            log.append(("arrival", lift.state))
            return [(LogBoardingEvent(e.lift), t) for e, t in events]

    class LogBoardingEvent(BoardingEvent):
        def execute(self, s):
            events = super().execute(s)
            log.append(("boarding", lift.state))
            return [(LogReturnEvent(e.lift), t) for e, t in events]

    class LogReturnEvent(ReturnEvent):
        def execute(self, s):
            events = super().execute(s)
            log.append(("return", lift.state))
            return events

    sim.schedule(LogArrivalEvent(agent, lift), 0)
    sim.run()

    assert log == [
        ("arrival", "idle"),
        ("boarding", "moving"),
        ("return", "idle"),
    ]
    assert agent.boarded
    assert lift.state == "idle"
    assert sim.current_time == 5
