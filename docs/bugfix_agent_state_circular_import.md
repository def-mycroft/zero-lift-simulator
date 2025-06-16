# Bugfix - Agent state circular import

random codename: nervous-circle 9d2bfa1e

***

Importing ``infer_agent_states`` in ``zero_liftsim.agent`` caused a
circular dependency when ``zero_liftsim.agent_state_id`` imported the
``Agent`` class for type checking. During module initialization Python
tried to load ``Agent`` before ``infer_agent_states`` was defined,
raising ``ImportError: cannot import name 'Agent'``.

The fix defers importing ``Agent`` until ``infer_agent_states`` executes
and only imports it for ``TYPE_CHECKING`` at module load time. This keeps
type hints intact while avoiding the circular import.

# Git Info
Commit: 41ec1b166f14f28c3e9fd9ef1960a2dee6548990
Date: 2025-06-16T06:40:21+00:00
