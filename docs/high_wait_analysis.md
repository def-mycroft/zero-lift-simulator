# Investigating Wait Time with Many Chairs

When running `SimulationManager(n_agents=10, lift_capacity=2)` the lift allocates fifty chairs by default. Intuitively this should eliminate queues, yet the summary reports an average wait around two minutes.

The cause lies in how arrivals trigger boarding. `ArrivalEvent.execute` only schedules `BoardingEvent` when the lift state is `"idle"`:

````python
if self.lift.state == "idle" and self.lift.available_chairs() > 0:
    events.append((BoardingEvent(self.lift), simulation.current_time))
````
【F:zero_liftsim/events.py†L80-L83】

Once any chair loads, `Lift.load` marks the lift as `"moving"` and keeps that state until all chairs return:

````python
if boarded:
    self.state = "moving"
    self.current_riders.append(list(boarded))
    self.chairs_available -= 1
    self.chairs_in_transit += 1
````
【F:zero_liftsim/lift.py†L79-L83】

Because at least one chair is always in transit, new arrivals see `lift.state == "moving"`. They are queued and only board when a `ReturnEvent` fires and explicitly schedules boarding:

````python
if self.lift.queue_length() > 0 and self.lift.available_chairs() > 0:
    events.append((BoardingEvent(self.lift), simulation.current_time))
````
【F:zero_liftsim/events.py†L124-L125】

This design throttles boarding to the cadence of returning chairs even if dozens of chairs wait at the base. Agents who arrive shortly after a chair departs must wait until the next return, resulting in non‑zero queue times despite plentiful capacity.

To reduce waiting with many chairs, arrival handling should trigger loading whenever chairs are free regardless of the `moving` state. Adjusting the condition in `ArrivalEvent.execute` or refactoring how `Lift.state` is used would allow immediate boarding when seats are available.

# Git Info
Commit: 082aaf44489caca8c8c31ca3839f5584e73c5436
Date: 2025-06-13T13:25:03Z
