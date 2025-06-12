prompt5 - full agent logging

random codname:

```copy
cosmic-octopus 1f7d9e34
```

***

# Prompt for Codex prompt5 – Follow-up to "cobalt-sparrow d7dca612"

Implement a comprehensive agent-level logging feature that can be toggled from
`Simulation.run` via a new boolean argument `full_agent_logging`. When this
flag is `True`, the simulation should record every event involving an agent to
`logs/agent.log`. The goal is to reconstruct each agent's actions throughout the
run.

## Requirements

- Extend `Simulation.run` with an optional `full_agent_logging: bool = False`
  parameter. When enabled, use the Logger class to setup this logger. modify logger class as needed to support this. 
- Whenever an `Event` executes and it references an `Agent` (directly or
  indirectly), write a log entry containing at minimum:
  - the agent's UUID and codename
  - the event type and a description of what occurred
  - timestamps and any other contextual data useful to replay the agent's
    history (e.g., queue length, lift state, wait time, etc.)
- Design the log format as newline-delimited JSON so it can be parsed easily.
- The logging should be implemented in a general way—preferably by adding a
  helper method on the base `Event` class so subclasses can call it when
  `full_agent_logging` is active.
- Store the collected entries in memory as well so tests can inspect them.
- Ensure existing logging to `main.log` (via `Logger`) continues to work.

## Tests

- Add unit tests that run a small simulation with `full_agent_logging=True` and
  verify that `logs/agent.log` is created and contains entries for each agent
  event in chronological order.
- Confirm that simulations run without this flag do not produce the agent log.
- Follow the guidance in `docs/best_practices_coding_with_codex.md` and run
  `pytest` before committing.
# Git Info
Commit: 5de18aa7b74b06096b9ab32fc8cf8880d2c9e262
Date: 2025-06-12T05:33:01-07:00
