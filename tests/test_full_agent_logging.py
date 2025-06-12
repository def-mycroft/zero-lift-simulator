import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datetime import datetime
from zero_liftsim.main import Simulation, Lift, Agent, ArrivalEvent


def test_agent_log_created_and_contains_entries():
    sim = Simulation()
    lift = Lift(capacity=1, cycle_time=5)
    agent = Agent(1)
    sim.schedule(ArrivalEvent(agent, lift), 0)
    start = datetime(2025, 3, 12, 9, 0, 0)
    sim.run(full_agent_logging=True, start_datetime=start)

    log_path = Path(__file__).resolve().parents[1] / "logs" / "agent.log"
    assert log_path.exists()
    with open(log_path, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f]

    events = [l["event"] for l in lines]
    assert events == ["ArrivalEvent", "BoardingEvent", "ReturnEvent"]
    assert events == [r["event"] for r in sim.agent_records()]


def test_agent_log_not_created_when_disabled():
    log_path = Path(__file__).resolve().parents[1] / "logs" / "agent.log"
    if log_path.exists():
        log_path.unlink()

    sim = Simulation()
    lift = Lift(capacity=1, cycle_time=5)
    agent = Agent(1)
    sim.schedule(ArrivalEvent(agent, lift), 0)
    sim.run(start_datetime=datetime(2025, 3, 12, 9, 0, 0))

    assert not log_path.exists()
    assert sim.agent_records() == []
