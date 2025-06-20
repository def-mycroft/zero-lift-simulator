import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.helpers import base_config
from zero_liftsim.simmanager import SimulationManager


def _run_wait(seed):
    cfg = base_config(Simulation={"run": {"random_seed": seed}})
    cfg["SimulationManager"]["__init__"].update({"n_agents": 3, "lift_capacity": 2})
    manager = SimulationManager(cfg)
    result = manager.run(runtime_minutes=60)
    return result["average_wait"]


def test_simulation_replicates_with_random_seed():
    seed = str(uuid4())
    wait1 = _run_wait(seed)
    wait2 = _run_wait(seed)
    assert wait1 == wait2
