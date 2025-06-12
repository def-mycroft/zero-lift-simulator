prompt3 - agent class

random codname:

```copy
wandering-marmot 3897c21d
```

***

# Prompt for Codex prompt3 – Follow-up to "buoyant-yeti 9463ae29"

Implement the `Agent` class in `zero_liftsim/main.py` so that agents carry enough
state for tracking a full day of skiing. The simulation and event classes are
already working; agents currently only store an `agent_id` and a `boarded` flag.
Expand them with fields and logic to measure wait times and rides completed.

## Required additions

- Track when each agent enters the lift queue (`wait_start`).
- Record the time an agent boards the lift (`board_time`).
- Maintain a counter of `rides_completed`.
- Provide a method `start_wait(time)` to set `wait_start`.
- Provide a method `finish_ride(time)` that updates `rides_completed`, clears
  `boarded`, and returns the wait time for that ride (`time - wait_start`).

## Tests

Add unit tests verifying that:

1. `start_wait` and `finish_ride` correctly compute wait time and increment
   `rides_completed`.
2. Agents can complete multiple rides with their counters updating as expected.

Follow the style in existing tests and run `pytest` before committing.
# Git Info
Commit: c936e3318795d8493c35cb3f8299b583141a5be0
Date: 2025-06-11T08:52:59-07:00
