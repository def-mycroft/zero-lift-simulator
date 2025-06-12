# Agent Experience

The simulation records per-agent ride loop metrics using the
`AgentExperience` system. Every `Agent` owns an instance of
`AgentRideLoopExperience` which logs the duration of each stage of a ski
loop. Durations are sampled from the lift during boarding and when the
ride completes.

Each entry is keyed by the simulation timestamp (as a `datetime`) and
contains the sampled ride time, traverse time, and the time spent in the
queue inferred from arrival and boarding events.

Example logged entry:

```json
{
  "2025-03-12T09:15:00": {
    "time_cost_ride_lift": 7.2,
    "time_cost_traverse_down_mountain": 5.1,
    "time_cost_in_queue": 4.6
  }
}
```
