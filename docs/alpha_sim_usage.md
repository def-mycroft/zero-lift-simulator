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

## Development Log

Use ``Logger.devlog`` to write ad-hoc messages directly to the log
file. Each line is prefixed with an ISO timestamp.

```python
logger = Logger("debug.log")
logger.devlog("initializing setup")
```

The file ``logs/debug.log`` will contain a line similar to::

```
2025-06-19T12:00:00 initializing setup
```
# Git Info
Commit: 2123fb0b47c5df266f76bdbf8a0f945c1fcc72b6
Date: 2025-06-11T18:41:52-07:00
