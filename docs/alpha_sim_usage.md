# Running the Alpha Simulation

The alpha simulation provides a quick demonstration of the lift engine.
Use `run_alpha_sim` to execute a short run and gather basic metrics.

```python
from zero_liftsim.main import run_alpha_sim

summary = run_alpha_sim(n_agents=3, lift_capacity=2, cycle_time=5)
print(summary)
```

`summary` contains the total number of rides processed and the average
wait time before boarding.

## Logging Events

The `Simulation.run` method accepts an optional `Logger` instance. This
captures the event name, timestamp and queue length before each event
executes.

```python
from zero_liftsim.logging import Logger
from zero_liftsim.main import Simulation, Lift, Agent, ArrivalEvent

logger = Logger()
sim = Simulation()
lift = Lift(capacity=1, cycle_time=5)
agent = Agent(1)
sim.schedule(ArrivalEvent(agent, lift), 0)
sim.run(logger=logger)
print(logger.records())
```

Each logged entry is also appended to ``logs/main.log`` by default.
You can supply a different filename to ``Logger`` and it will be
created inside the ``logs`` directory:

```python
logger = Logger("my_run.log")
```

The ``records()`` method still returns the in-memory list of log
entries.
