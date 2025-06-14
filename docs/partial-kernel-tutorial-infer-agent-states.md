# Tutorial - Infer Agent State

random codename: obsequious-spend 3d8813f7

#process-notes 

***


# Imports 

```python
from zero_liftsim.simmanager import SimulationManager
from zero_liftsim.helpers import base_config
from zero_liftsim.experience import AgentRideLoopExperience
from zero_liftsim.helpers import load_asset_template
from zero_liftsim import helpers as hp
from zero_liftsim.lift import Lift

from zero_helpers.imports import * 
import inspect
```

# Run Simulation


```python
cfg = base_config()
cfg["SimulationManager"]["__init__"].update({"n_agents": 3, "lift_capacity": 2})
manager = SimulationManager(cfg)
result = manager.run(runtime_minutes=60)
print(result)
```




# Retrieve Data from Simulation


```python
# get rideloop explogs and agent event log
exp_log_data = manager.retrieve_data()
exp = exp_log_data['exp_rideloop']
log = exp_log_data['agent_log']
```

# Get agent log and explog

```python
# sample agent and subset exp/log to e/l for agent subset of those
m = log['event'] == 'ride_complete'
event_ride_comp = log[m].sample().iloc[0].to_dict()
agent = manager.lookup_agent(event_ride_comp['agent_uuid'])
l = log[log['agent_uuid'] == agent.agent_uuid]
idx = (exp['time'] - event_ride_comp['time']).dt.total_seconds().abs().idxmin()
e = exp.loc[idx].to_dict()
```

# Agent experience traceback

```python
x = agent.traceback_experience(e['exp_id'])
print(x)
```


# Identify Agent State


```python
# get ride loop logs and agent event logs
log = manager.retrieve_data()
exp = log['exp_rideloop'] # dataframe of all agent rideloop experiences 
log = log['agent_log'] # combined agent logs (i.e. activity logs for all agents)

# sample a random timestamp within the agent log timeframe
INDEX_TIME = pd.Series(pd.date_range(log['time'].min(), log['time'].max(), freq='1s')).sample().iloc[0]

# sample a random agent from ride loop log
row = exp.sample().iloc[0]
aid = row['agent_uuid']
agent = manager.lookup_agent(aid)

# find the nearest time index in the agent log
l = log.zero_liftsim.subset_agent_uuid(agent.agent_uuid)
e = exp.zero_liftsim.subset_agent_uuid(agent.agent_uuid)
idx = l.zero_liftsim.get_nearest_time_index(INDEX_TIME)
```

for the ride loop agent experience, the total time is broken down into riding the lift, traversing down the mountain and waiting in the queue, i.e. `"time_spent_total": ride + traverse + queue` below: 


```python
s = inspect.getsource(AgentRideLoopExperience)
lines = s.split('\n')
idx = [i for i,x in enumerate(lines) if x.strip() == '"""'][-1]
print('\n'.join(lines[idx+1:]))
```

        def add_entry(self, agent, return_event_uuid, dt: datetime, ride: float, traverse: float, 
                      queue: float) -> None:
            self.log[dt] = {
                "exp_id": str(uuid()), 
                "return_event_uuid": return_event_uuid,
                "agent_uuid": agent.agent_uuid,
                "agent_uuid_codename": agent.agent_uuid_codename,
                "time_spent_ride_lift": ride,
                "time_spent_traverse_down_mountain": traverse,
                "time_spent_in_queue": queue,
                "time_spent_total": ride + traverse + queue,
            }
    



```python
state_riding_lift = "state_riding_lift"
state_in_queue = "state_in_queue"
state_traversing_down = "state_traversing_down"
```

The logs in ``exp_rideloop`` record how long each ride loop took, while
``agent_log`` lists the events an agent experienced. By looking at the most
recent event at a particular timestamp we can classify where the agent is.

```python
from datetime import datetime
from zero_liftsim.sandbox import infer_agent_states

SNAPSHOT_TIME = manager.start_datetime + timedelta(minutes=5)
state_map = infer_agent_states(manager.agents, SNAPSHOT_TIME)
```

This ``state_map`` dictionary now contains an entry for each ``agent_uuid``
mapping to ``state_in_queue``, ``state_riding_lift`` or ``state_traversing_down``.
You might see one agent flagged as ``state_traversing_down`` and another still in
``state_riding_lift`` depending on ``SNAPSHOT_TIME``.

Below is the helper used in the tutorial.

```python
from datetime import datetime
from typing import Iterable, Dict
from zero_liftsim.agent import Agent

state_riding_lift = "state_riding_lift"
state_in_queue = "state_in_queue"
state_traversing_down = "state_traversing_down"


def infer_agent_states(agents: Iterable[Agent], dt: datetime) -> Dict[str, str]:
    """Return a mapping of agent UUIDs to a simple state."""
    states: Dict[str, str] = {}
    for agent in agents:
        last_event = None
        last_time = None
        for rec in agent.activity_log.values():
            t = datetime.fromisoformat(rec["time"])
            if t <= dt and (last_time is None or t > last_time):
                last_time = t
                last_event = rec["event"]
        if last_event == "board":
            state = state_riding_lift
        elif last_event == "ride_complete":
            state = state_traversing_down
        else:
            state = state_in_queue
        states[agent.agent_uuid] = state
    return states
```
