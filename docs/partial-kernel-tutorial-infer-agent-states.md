# Infer State from Agent Log and Exp (Tutorial Stub)

random codename: obsequious-spend 3d8813f7

***


```python
%load_ext autoreload
%autoreload 2
```


```python
from zero_helpers.imports import * 
```


```python
from zero_liftsim.simmanager import SimulationManager
from zero_liftsim.experience import AgentRideLoopExperience
import inspect
from zero_liftsim.helpers import load_asset_template
```

# Run Simulation


```python
# setup and run simulation
manager = SimulationManager(
    n_agents=10,
    lift_capacity=2,
)
result = manager.run()
print(result)
```

    {'total_rides': 331, 'average_wait': 1.5166163141993958, 'agents': [Agent(1) unequaled-point 59a0a711-e839-4e3a-b747-2aa1d264e387, Agent(2) abhorrent-tourist 6dc3ace6-2752-41e1-be34-6260acf962be, Agent(3) thoughtful-charge 6fb2ff63-ac6b-4e82-9216-2c5f8fbe17bb, Agent(4) parsimonious-sensitive 11eebf05-fd19-4cef-b36a-5136c5d65c85, Agent(5) halting-fat d9250988-5517-4523-a012-708330e7d2a2, Agent(6) awesome-style 3d10c05e-470e-4abd-8540-92b84b95258d, Agent(7) unable-drama 5cea574a-a1ec-489d-9f25-21cfe3bec394, Agent(8) marvelous-hearing d583e0cd-853c-43d9-bb4e-595c821313cd, Agent(9) crowded-piano cf2ca7ca-436e-4160-b248-36bd51e701aa, Agent(10) valuable-physical 7a998518-ffc3-441d-952f-4ca173581440]}



```python
lift = manager.lift
lift.total_chairs()
```




    50



## Retrieve Data from Simulation


```python
# get rideloop explogs and agent event log
exp_log_data = manager.retrieve_data()
e = exp_log_data['exp_rideloop']
l = exp_log_data['agent_log']
```

# Identify Agent State


```python
# get ride loop logs and agent event logs
log = manager.retrieve_data()
rlog = log['exp_rideloop'] # dataframe of all agent rideloop experiences 
alog = log['agent_log'] # combined agent logs (i.e. activity logs for all agents)

# sample a random timestamp within the agent log timeframe
INDEX_TIME = pd.Series(pd.date_range(alog['time'].min(), alog['time'].max(), freq='1s')).sample().iloc[0]

# sample a random agent from ride loop log
row = rlog.sample().iloc[0]
aid = row['agent_uuid']
agent = manager.lookup_agent(aid)

# find the nearest time index in the agent log
l = alog.zero_liftsim.subset_agent_uuid(agent.agent_uuid)
e = rlog.zero_liftsim.subset_agent_uuid(agent.agent_uuid)
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
