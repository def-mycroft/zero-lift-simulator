# prompt14 - Force Agent State Map unnamed aggressive-week 801baa1b

#prompt
random codename: aggressive-week 801baa1b

***

Implement `Agent.get_latest_event(dt: datetime) -> str` which returns the event string for the latest activity log entry whose timestamp is less than or equal to `dt`. The agent has an attribute `activity_log`, a dict mapping integer indices to dicts containing at least a `"time"` (ISO string) and `"event"` (str). Raise a `ValueError` if no valid event exists before `dt`. The returned string must be a key in `_EVENT_STATE_MAP`; if it's not, raise `KeyError`. This method is used by `infer_agent_states`, which assumes correctness and completeness of the log, and maps each agent to an unambiguous state. This enforces that state inference relies only on recognized events, with failure being explicit.


note that I've disabled sandbox/infer_agent_states with NotImplementedError; but you should be re-writing to fix and then remove that line. 

note that this should be pulling from agent's own activity log too. 

