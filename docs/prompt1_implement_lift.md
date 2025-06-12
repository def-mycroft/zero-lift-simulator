prompt1 - lift class 

random codname: 

```copy
ruthless-ladder 3238db4e
```


*** 

# Prompt for Codex prompt1 – Follow‑up to “ajar-passenger 2738f5a9”

Implement the Lift class in zero_liftsim/main.py.
Simulation is already complete from the previous prompt. Lift is currently only a placeholder with a descriptive docstring. Following the project notes (docs/main_notes_implementation.md and docs/devplan-capable-push-34aa005b.md), expand Lift to manage skiers waiting for a single lift.

Key requirements:

State and Queue

Maintain a FIFO queue (collections.deque) of Agent instances.

Track lift capacity (int), cycle time (int), and operational state ("idle" or "moving").

Provide methods to add agents to the queue and query the current state.

Loading Logic

Implement load() (name can vary) to remove up to capacity agents from the queue, mark them as boarded, and set state to "moving".

Return the list of boarded agents so events such as BoardingEvent can schedule a ReturnEvent.

Reset / Return

Provide a method to mark the lift as idle again once a cycle is complete.

Docstrings & Clarity

Document each public method following the style of the existing module.

Emphasize that Lift itself does not schedule events; it only exposes state and queue operations.

Unit Tests

Add tests under tests/ verifying:

Enqueued agents are loaded in FIFO order.

State transitions from "idle" → "moving" → "idle" are correct.

Loading more agents than present only boards those available.

Best Practices

Follow docs/best_practices_coding_with_codex.md: small, testable methods, clear docstrings, and run pytest before committing.

This continues the work started with the “Simulation” class implementation.
# Git Info
Commit: c936e3318795d8493c35cb3f8299b583141a5be0
Date: 2025-06-11T08:52:59-07:00
