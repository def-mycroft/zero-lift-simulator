prompt6 - agent logging

random codname:

```copy
magnetic-barnacle 4d5f3a21
```

***

# Prompt for Codex prompt6 – Follow-up to "cobalt-sparrow d7dca612"

Implement per-agent self-logging so that each agent retains a detailed history of its activity during a simulation. The log should be optional and easy to access after the run.

## Agent log structure
- Each `Agent` gets an attribute `activity_log` storing a list of dictionaries.
- Every dictionary represents one event affecting the agent and must at least contain:
  - `time`: the simulation timestamp of the event.
  - `event`: short string describing the type of event (``arrival``, ``board``, ``ride_complete`` …).
  - `agent_id`, `agent_uuid`, and `agent_uuid_codename` for traceability.
- Include any other helpful info such as queue length, lift state, or wait time.

## API changes
- Add a boolean flag to `Agent.__init__` (e.g. ``self_logging: bool = True``). When ``False`` the agent should not collect any logs.
- Provide a helper method ``log_event(event: str, time: int, **info)`` that appends a record to ``activity_log`` only when logging is enabled.

## Event hooks
- Call ``log_event`` in key locations:
  - ``ArrivalEvent.execute`` after the agent is enqueued.
  - ``BoardingEvent.execute`` for each agent that boards the lift.
  - ``ReturnEvent.execute`` when each boarded agent finishes a ride (this may require passing the boarded agent list from ``BoardingEvent`` to ``ReturnEvent``).
  - Inside ``Agent.start_wait`` and ``Agent.finish_ride`` so manual uses also record events.

## Accessing logs
- After ``run_alpha_sim`` or any simulation run, users can examine ``agent.activity_log`` for a chronological history of that agent’s actions.

## Tests
- Add unit tests ensuring that enabled agents collect the expected sequence of log records while disabled agents leave ``activity_log`` empty.
- Continue running ``pytest`` before commits as described in earlier prompts.
