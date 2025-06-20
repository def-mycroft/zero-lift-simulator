"""Sandbox dev scratchpad"""
try:  # optional dependency for convenience functions
    from zero_helpers.imports import *  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - allow running without package
    pass
from codenamize import codenamize as cd
import json
from copy import deepcopy as copy
from zero_liftsim.simmanager import SimulationManager
from zero_liftsim.helpers import base_config
from zero_liftsim.experience import AgentRideLoopExperience
from zero_liftsim.helpers import load_asset_template
from zero_liftsim import helpers as hp
from zero_liftsim.lift import Lift
import inspect
from zero_liftsim.simmanager import SimulationManager
from zero_liftsim.helpers import base_config
from zero_liftsim.experience import AgentRideLoopExperience
from zero_liftsim.helpers import load_asset_template
from zero_liftsim import helpers as hp
from zero_liftsim.lift import Lift


def sim_reprod():

    # Run Simulation

    x = """
    {
        "git_commit": "d5591c363075a9fa932ba8be140caa96690c7f0d",
        "SimulationManager": {
            "__init__": {
                "n_agents": 3,
                "lift_capacity": 2,
                "start_datetime": null,
                "logger": null
            },
            "run": {
                "end_datetime": null,
                "runtime_minutes": null
            }
        },
        "Simulation": {
            "__init__": {
                "simulation_uuid": null
            },
            "run": {
                "stop_time": null,
                "logger": null,
                "full_agent_logging": false,
                "start_datetime": "2025-03-12T09:00:00",
                "random_seed": null
            }
        },
        "Lift": {
            "num_chairs": 50,
            "ride_mean": 7,
            "ride_sd": 1,
            "traverse_mean": 5,
            "traverse_sd": 1.5
        },
        "Agent": {
            "__init__": {
                "logger": null,
                "self_logging": true
            }
        }
    }
    """
    cfg = json.loads(x)

    cfg['Simulation']['run']['random_seed'] = 'd7a0baf7-61aa-484d-a48e-e7f9b3fb4a6d'

    manager = SimulationManager(cfg)
    result1 = manager.run(runtime_minutes=60)
    print(result1)
    print(result1['average_wait'])

    manager = SimulationManager(cfg)
    result2 = manager.run(runtime_minutes=60)
    print(result2)
    print(result2['average_wait'])

    return result1['average_wait'], result2['average_wait']


def get_sample():    
    cfg = base_config()
    cfg["SimulationManager"]["__init__"].update({"n_agents": 25, "lift_capacity": 4})
    cfg['Lift']['num_chairs'] = 35

    manager = SimulationManager(cfg)
    result = manager.run(runtime_minutes=60*4)

    # get rideloop explogs and agent event log
    exp_log_data = manager.retrieve_data()
    exp = exp_log_data['exp_rideloop']
    log = exp_log_data['agent_log']

    # sample an agent
    agent = manager.sample_agent()
    INDEX_TIME = agent.get_activity_log_df()['time'].sample().iloc[0]

    # this is the agent state @ time as self-determined (based on own logs, self.activity_log via self.get_latest_event)
    state_gotten = agent.get_state(INDEX_TIME)
    event_latest = agent.get_latest_event(INDEX_TIME)

    from zero_liftsim.agent_state_id import _EVENT_STATE_MAP as esm

    edf = agent.get_rideloop_experience_log_df()
    idx = edf.zero_liftsim.get_nearest_time_index(INDEX_TIME)
    eid = edf.loc[idx]['exp_id']
    lines = []
    lines.append(f"* states are mapped to events like this: ")
    for k,v in esm.items():
        lines.append(f"    * {k} (event): {v} (action)")
    lines.append(f"""
    * predicted agent state: {state_gotten}
    * most recent event: {event_latest}
    * experience (id): {cd(eid)} {eid}
    * INDEX_TIME: {INDEX_TIME.strftime('%H:%M')}
    """)
    assert exp['exp_id'].is_unique
    e_params = exp.set_index('exp_id').loc[eid].to_dict()

    ldf = agent.get_activity_log_df()
    l = agent.recent_agent_log_return_event_uuid(e_params['return_event_uuid'])

    for k,v in e_params.items():
        lines.append(f"* {k}: {v}")

    lines.append(f"Recent Activity Log")
    lines.append(l)

    ## analysis vars
    keyParameters = {}
    keyParameters['cfg'] = copy(cfg)
    keyParameters['sample_time'] = INDEX_TIME
    keyParameters['exp'] = e_params
    keyParameters['state_map'] = esm

    kp = copy(keyParameters)
    kp['sample_time'] = kp['sample_time'].isoformat()
    kp['exp']['time'] = kp['exp']['time'].isoformat()
    lines.append('# kp')
    lines.append(f"\n{json.dumps(kp, indent=4)}\n")
    lines.append('# e_params')
    lines.append(f"\n{e_params}\n")

    return {'keyParameters':keyParameters, 'lines':lines,
            'printme':'\n'.join(lines), 'agent_uuid':agent.agent_uuid, 
            'agent_state':agent.get_state(INDEX_TIME)}

