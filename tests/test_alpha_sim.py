import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.main import (
    run_alpha_sim,
    Simulation,
    Agent,
    ArrivalEvent,
    BoardingEvent,
    ReturnEvent,
)
from zero_liftsim.lift import Lift
from zero_liftsim.logging import Logger


def test_run_alpha_sim_metrics():
    start = datetime(2025, 3, 12, 9, 0, 0)
    # ensure deterministic lift timing for this test
    orig = Lift.time_spent_ride_lift
    Lift.time_spent_ride_lift = lambda self: 5
    result = run_alpha_sim(
        n_agents=3, lift_capacity=2, start_datetime=start
    )
    Lift.time_spent_ride_lift = orig
    assert result["total_rides"] == 3
    assert abs(result["average_wait"] - (0 + 4 + 3) / 3) < 1e-6


def test_logging_records_events():
    logger = Logger()
    sim = Simulation()
    lift = Lift(capacity=1)
    lift.time_spent_ride_lift = lambda: 5
    agent = Agent(1)
    sim.schedule(ArrivalEvent(agent, lift), 0)
    start = datetime(2025, 3, 12, 9, 0, 0)
    sim.run(logger=logger, start_datetime=start)
    records = logger.records()
    assert [r["event"] for r in records] == ["ArrivalEvent", "BoardingEvent", "ReturnEvent"]
    expected_times = [
        start.isoformat(),
        start.isoformat(),
        (start + timedelta(minutes=5)).isoformat(),
    ]
    assert [r["time"] for r in records] == expected_times
    assert [r["queue_length"] for r in records] == [0, 1, 0]


def test_logger_writes_file(tmp_path):
    log_name = "test.log"
    logger = Logger(log_name)
    sim = Simulation()
    lift = Lift(capacity=1)
    lift.time_spent_ride_lift = lambda: 5
    agent = Agent(1)
    sim.schedule(ArrivalEvent(agent, lift), 0)
    start = datetime(2025, 3, 12, 9, 0, 0)
    sim.run(logger=logger, start_datetime=start)

    log_path = Path(__file__).resolve().parents[1] / "logs" / log_name
    assert log_path.exists()
    with open(log_path, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f]
    assert lines == logger.records()


def test_devlog_writes_message():
    log_name = "dev_test.log"
    logger = Logger(log_name)
    logger.devlog("hello world")

    log_path = Path(__file__).resolve().parents[1] / "logs" / log_name
    assert log_path.exists()
    with open(log_path, "r", encoding="utf-8") as f:
        line = f.readline().strip()
    ts, msg = line.split(" ", 1)
    from datetime import datetime

    # ensure timestamp parses and message matches
    datetime.fromisoformat(ts)
    assert msg == "hello world"
    assert logger.records() == []
