import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.main import run_alpha_sim, Simulation, Lift, Agent, ArrivalEvent, BoardingEvent, ReturnEvent
from zero_liftsim.logging import Logger


def test_run_alpha_sim_metrics():
    result = run_alpha_sim(n_agents=3, lift_capacity=2, cycle_time=5)
    assert result["total_rides"] == 3
    assert abs(result["average_wait"] - (0 + 4 + 3) / 3) < 1e-6


def test_logging_records_events():
    logger = Logger()
    sim = Simulation()
    lift = Lift(capacity=1, cycle_time=5)
    agent = Agent(1)
    sim.schedule(ArrivalEvent(agent, lift), 0)
    sim.run(logger=logger)
    records = logger.records()
    assert [r["event"] for r in records] == ["ArrivalEvent", "BoardingEvent", "ReturnEvent"]
    assert [r["time"] for r in records] == [0, 0, 5]
    assert [r["queue_length"] for r in records] == [0, 1, 0]


def test_logger_writes_file(tmp_path):
    log_name = "test.log"
    logger = Logger(log_name)
    sim = Simulation()
    lift = Lift(capacity=1, cycle_time=5)
    agent = Agent(1)
    sim.schedule(ArrivalEvent(agent, lift), 0)
    sim.run(logger=logger)

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
