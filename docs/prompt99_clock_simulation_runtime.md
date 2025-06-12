# prompt99 - clock simulation runtime

random codename:

```copy
frosty-clock 8e7c2a1b
```

***

# Prompt for Codex prompt99 – Run Simulation for a Daily Time Window

Currently the simulation stops after each agent completes a single ride loop. The `SimulationManager` schedules one arrival per agent and the event chain ends once all agents exit the lift. Running `manager.run()` with ten agents therefore yields `total_rides` equal to ten.

Upgrade the system so that a simulation runs continuously until a specified end time, defaulting to **4:00 PM** on the same day as `start_datetime`. There must be a single global clock driving all events. If multiple timing notions exist, consolidate them so that event timestamps and logging all reference the same clock.

## Requirements

1. **Global Clock**
   - Ensure there is one authoritative clock (`Simulation.current_time` in minutes from `start_datetime`).
   - All events and logging must derive their timestamps from this clock. If any component maintains its own time, refactor to use the global clock.

2. **Simulation Duration**
   - Extend `SimulationManager` with an optional `end_datetime` parameter (or `runtime_minutes`), defaulting to 4 PM the same day.
   - Pass this limit to `Simulation.run(stop_time=...)` so the event loop halts when the clock reaches this value.

3. **Agent Ride Looping**
   - After an agent completes a ride and traverses down the mountain, schedule its next `ArrivalEvent` provided the next arrival time is before `end_datetime`.
   - Continue cycling agents through arrivals, boarding, and returns until the global clock hits the stop time.

4. **Metrics Update**
   - Update the summary returned by `SimulationManager.run()` to report total rides completed across all agents during the runtime window and the average wait per ride.

5. **Tests**
   - Add unit tests to verify that a simulation running from 9 AM to 4 PM produces multiple rides per agent and respects the stop time.

Use the existing project style for docstrings, logging, and tests. Focus on clarity so future prompts can extend the simulation further.

# Git Info
