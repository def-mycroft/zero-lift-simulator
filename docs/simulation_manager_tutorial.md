# Using SimulationManager
random codename: animated-event e6b82433
***
The `SimulationManager` class orchestrates configuration and execution
of a lift simulation. Instantiate it with parameters similar to an
`sklearn` estimator and call ``run`` to execute the simulation.

```python
from zero_liftsim.simmanager import SimulationManager

manager = SimulationManager(
    n_agents=3,
    lift_capacity=2,
    cycle_time=5,
)
result = manager.run()
print(result)
```

The returned dictionary matches ``run_alpha_sim`` but ``SimulationManager``
exposes additional helpers like :py:meth:`archive_agent_rideloop_experience`.
