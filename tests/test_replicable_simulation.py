import sys
from pathlib import Path
from datetime import datetime
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.helpers import base_config
from zero_liftsim.simmanager import SimulationManager


def _run_states(sim_uuid: str):
    cfg = base_config(Simulation={"__init__": {"simulation_uuid": sim_uuid}})
    cfg["SimulationManager"]["__init__"].update(
        {"n_agents": 1, "lift_capacity": 1, "start_datetime": datetime(2025, 3, 12, 9, 0, 0)}
    )
    manager = SimulationManager(cfg)
    manager.run(runtime_minutes=120)
    agent = manager.agents[0]
    data = [agent.get_state(t) for t in range(30)]
    return data


def test_simulation_replicates_with_seed():
    sim_uuid = str(uuid4())
    states1 = _run_states(sim_uuid)
    states2 = _run_states(sim_uuid)
    assert states1 == states2

