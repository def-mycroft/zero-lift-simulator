# prompt21 traceback sampling error  wary-bitter 1b487118

random codename: wary-bitter 1b487118
#prompt 


***

```python
%load_ext autoreload
%autoreload 2

# example for blog post 

from zero_helpers.imports import * 
from zero_liftsim.simmanager import SimulationManager
from zero_liftsim.helpers import base_config
from zero_liftsim.experience import AgentRideLoopExperience
from zero_liftsim.helpers import load_asset_template
from zero_liftsim import helpers as hp
from zero_liftsim.lift import Lift

import inspect

cfg = base_config()
cfg["SimulationManager"]["__init__"].update({"n_agents": 25, "lift_capacity": 4})
cfg['Lift']['num_chairs'] = 35

manager = SimulationManager(cfg)
result = manager.run(runtime_minutes=60*4)

# get rideloop explogs and agent event log
exp_log_data = manager.retrieve_data()
exp = exp_log_data['exp_rideloop']
log = exp_log_data['agent_log']

def sample_agent(manager, log, exp):
    # sample agent and subset exp/log to e/l for agent subset of those
    m = log['event'] == 'ride_complete'
    event_ride_comp = log[m].sample().iloc[0].to_dict()
    agent = manager.lookup_agent(event_ride_comp['agent_uuid'])
    l = log[log['agent_uuid'] == agent.agent_uuid]
    idx = (exp['time'] - event_ride_comp['time']).dt.total_seconds().abs().idxmin()
    e = exp.loc[idx].to_dict()
    return agent, l, e

agent, l, e = sample_agent(manager, log, exp)
agent.traceback_experience(e['exp_id'])
```


when I run the above, I get 

```
KeyError                                  Traceback (most recent call last)
Cell In[1], line 37
     34     return agent, l, e
     36 agent, l, e = sample_agent(manager, log, exp)
---> 37 agent.traceback_experience(e['exp_id'])

File ~/code-repos/zero-lift-simulator/zero_liftsim/agent.py:250, in Agent.traceback_experience(self, experience_id)
    247             return tmpl.render(**context)
    248         return tmpl.format(**context)
--> 250 raise KeyError(experience_id)

KeyError: '40d8a0dc-529a-4307-91f2-64c63861eb1d'
```


see code above, called "# example for blog post  and note what happens when I run it. 

apply a fix to either the underlying code and maybe review notebook "# example for blog post " and "# Scratchpad "section there that I'm trying to work on 