import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.simmanager import SimulationManager
from zero_liftsim.helpers import base_config

from zero_liftsim.lift import Lift


def test_simulation_runs_until_stop_time():
    start = datetime(2025, 3, 12, 9, 0, 0)
    cfg = base_config()
    cfg["SimulationManager"]["__init__"].update(
        {"n_agents": 1, "lift_capacity": 1, "start_datetime": start}
    )
    manager = SimulationManager(cfg)
    manager._setup()
    manager.lift.time_spent_ride_lift = lambda: 5
    manager.lift.time_spent_traverse_down_mountain = lambda: 5
    result = manager.run(runtime_minutes=420)
    agent = manager.agents[0]
    assert agent.rides_completed > 1
    assert manager.sim.current_time <= 420
    assert result["total_rides"] == agent.rides_completed
