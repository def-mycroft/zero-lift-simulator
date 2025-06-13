# Launching a Simulation
random codename: outgoing-way cd797da0
***
This tutorial demonstrates how to start a lift simulation using
`SimulationManager` and the configuration dictionary returned by
`base_config`.

```python
from zero_liftsim.helpers import base_config
from zero_liftsim.simmanager import SimulationManager

cfg = base_config()
cfg["SimulationManager"]["__init__"].update({
    "n_agents": 5,
    "lift_capacity": 2,
})
manager = SimulationManager(cfg)
summary = manager.run(runtime_minutes=60)
print(summary)
```

The example sets up a simple one hour run with five agents and a
two-person lift. `summary` contains the total rides and average wait time.
