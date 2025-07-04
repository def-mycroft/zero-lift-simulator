import sys
from pathlib import Path

import pytest
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.main import Agent, ArrivalEvent, BoardingEvent, ReturnEvent, Simulation
from zero_liftsim.lift import Lift


def test_single_agent_cycle():
    log = []
    sim = Simulation()
    lift = Lift(capacity=1)
    lift.time_spent_ride_lift = lambda: 5
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
    sim.run(start_datetime=datetime(2025, 3, 12, 9, 0, 0))

    assert log == [
        ("arrival", "idle"),
        ("boarding", "moving"),
        ("return", "idle"),
    ]
    assert agent.boarded
    assert lift.state == "idle"
    assert sim.current_time == 5
