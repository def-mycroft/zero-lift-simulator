# Dev Notes: Zero Lift Simulator

## Overview
Zero Lift Simulator ("LiftSim") is an agent-based simulation of skier-lift dynamics at a ski resort. The goal is to model individual skier behavior interacting with constrained lift infrastructure over a simulated day. The system is built around an event-driven simulation engine where agents arrive, queue for a single lift, ride, ski down, and repeat.

The simulation is designed to help explore operational bottlenecks, especially how arrival patterns, lift capacities, and cycle times affect queue lengths, wait times, and throughput. Eventually, this platform will serve as the foundation for more complex modeling including pricing schemes, weather variability, and multi-lift resort maps.

## Core Concepts
- **Discrete Event Simulation**: Simulation clock advances based on time-stamped events (e.g., agent arrival, lift boarding, lift return). This avoids unnecessary time-stepping.
- **Agent-Based Modeling**: Each skier is an agent with their own state (arrival time, number of rides, wait times, etc.). Agent behavior is deterministic for now, but future versions will include probabilistic rules.
- **Single-Lift System**: For the kernel, we assume one lift with fixed capacity and fixed round-trip duration.

## Initial Goals
- Run a valid simulation of N agents arriving over time.
- Compute and log: average wait time, lift utilization, queue length over time.
- Use a FIFO queue at the lift.
- Assume deterministic lift cycle time and constant ski-down time (or fixed distribution).

## Object Model
### Classes
- `Simulation`: Core engine holding the clock and event queue.
- `Event` (abstract): Base class for all events.
  - `ArrivalEvent`
  - `BoardingEvent`
  - `ReturnEvent`
- `Agent`: Represents a skier and their evolving state.
- `Lift`: Tracks queue, capacity, state (idle/moving).

### Agent Lifecycle
1. Arrives at resort via `ArrivalEvent`.
2. Joins lift queue.
3. Boards lift in `BoardingEvent` (if within capacity).
4. Lift departs; lift becomes unavailable.
5. Lift returns in `ReturnEvent`.
6. Skier skis down (either implicit or via another event).
7. Agent re-queues (if there's enough time in the day).

## Key Parameters
- `n_agents`: total number of simulated agents
- `arrival_distribution`: uniform or exponential
- `lift_capacity`: fixed number of skiers per ride
- `lift_cycle_time`: time from departure to return
- `ski_down_time`: time spent skiing before rejoining queue
- `sim_duration`: total simulated time (e.g., 480 minutes)

## Planned Phases
1. **Minimal Working Kernel**: functional event loop, 1 lift, valid outputs
2. **Agent Looping**: ski down + rejoin queue
3. **Data Logging**: metrics per agent, per lift
4. **Visualization**: queue size over time, wait time histograms
5. **Complexity**: new events (breaks, leave early), stateful agents
6. **Persistence**: results into SQLite or parquet via DuckDB
7. **Scenario Testing**: simulate free lift day, delayed openings, etc.

## Dev Practices
- Code is modular and testable. Avoid global state.
- Use class-by-class implementation with rich docstrings.
- Unit test each event execution logic.
- Maintain clear separation between simulation engine and domain logic.

## Notes for Codex or LLM-Based Agents
If you’re generating or expanding code from these notes:
- Always refer to class-level docstrings for intended behavior.
- Preserve naming conventions (`ArrivalEvent`, `execute(simulation)`, etc.).
- Keep the simulation loop event-driven (do not introduce tick-based logic).
- Assume FIFO semantics in the lift queue unless stated otherwise.
- All simulation time is in integer minutes unless extended.

---
This document should be included in the repo as a core reference alongside the initial kernel module and expanded incrementally as the project grows.

