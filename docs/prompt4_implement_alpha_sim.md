prompt4 - alpha simulation and logging

random codname:

```copy
cobalt-sparrow d7dca612
```

***

# Prompt for Codex prompt4 – Follow-up to "pink-walk 44320cd6"

Implement the first end-to-end "alpha" simulation and create a minimal logging utility. The core classes (`Simulation`, `Lift`, `Agent`, and the event subclasses) are already in place.

## Alpha Simulation
- Add a function `run_alpha_sim(n_agents: int, lift_capacity: int, cycle_time: int) -> dict` in `zero_liftsim/main.py`.
- Generate `n_agents` with sequential arrival times starting at 0 (one agent per minute) and schedule `ArrivalEvent`s for them.
- Instantiate a `Lift` with the provided capacity and cycle time.
- Run the `Simulation` until no events remain.
- Return summary metrics such as total rides completed and average wait time.

## Logging Kernel
- Create a module `zero_liftsim/logging.py` containing a simple `Logger` class.
- `Logger.log(event_name, time, **info)` should append a dictionary to an internal list.
- Provide a `records()` method returning the list of log entries.
- Update `Simulation.run` to accept an optional `logger` parameter. When supplied, call `logger.log` before executing each event with the event's class name, timestamp, and queue length.

## Tests
- Verify `run_alpha_sim` processes all agents and reports reasonable metrics.
- Verify that logging captures the expected event sequence when a logger is passed.
- Follow `docs/best_practices_coding_with_codex.md` and run `pytest` before committing.
