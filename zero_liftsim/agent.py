"""Agent model used in the Zero Lift simulator."""

from __future__ import annotations

import pandas as pd
import json
from uuid import uuid4 as uuid
from datetime import datetime, timedelta

try:
    from codenamize import codenamize
except ModuleNotFoundError:  # pragma: no cover
    def codenamize(value: str) -> str:
        return value[:8]

from .logging import Logger
from .experience import AgentRideLoopExperience
from .agent_state_id import infer_agent_states


class Agent:
    """Represents an individual participant in the Zero Lift simulation.

    Each Agent maintains a unique identity, an internal log of events,
    and an encapsulated record of experiential data. Agents can log
    simulation events, track waiting and ride durations, and summarize
    past experiences for analysis or debugging.

    Parameters
    ----------
    agent_id : int
        Integer identifier for the agent.
    logger : Logger, optional
        If provided, used for structured development logging.
    self_logging : bool, default=True
        Enables or disables internal event logging.

    Attributes
    ----------
    agent_uuid : str
        Globally unique identifier for the agent.
    agent_uuid_codename : str
        Shortened mnemonic form of the UUID.
    boarded : bool
        Indicates whether the agent is currently on a ride.
    wait_start : int or None
        Simulation time when the agent entered a queue.
    board_time : int or None
        Simulation time when the agent boarded the lift.
    rides_completed : int
        Count of completed ride cycles.
    activity_log : dict of int to dict
        Ordered log of simulation events and metadata.
    experience_rideloop : AgentRideLoopExperience
        Stores summaries of each lift ride experience.
    """
    def __init__(
# {{{
        self,
        agent_id: int,
        logger: "Logger" | None = None,
        self_logging: bool = True,
    ) -> None:
        self.agent_id = agent_id
        self.agent_uuid = str(uuid())
        self.agent_uuid_codename = codenamize(self.agent_uuid)
        self.boarded: bool = False
        self.wait_start: int | None = None
        self.board_time: int | None = None
        self.rides_completed: int = 0
        self.self_logging = self_logging
        self.current_state = ''
        self.activity_log: dict[int, dict] = {}
        self.experience_rideloop = AgentRideLoopExperience()
        if logger is not None:
            logger.devlog(
                f"init agent {self.agent_uuid} {self.agent_uuid_codename}"
            )
            self.logger = logger
# }}}
    # Record an event in :attr:`activity_log`.
    def log_event(
# {{{
        self,
        event: str,
        time: int,
        timestamp: str,
        return_event_uuid: str = "",
        **info,
    ) -> None:
        """Record an event in the agent's activity log.

        Adds a structured entry to the internal log, capturing simulation
        time, timestamp, event name, agent metadata, and optional details.

        Parameters
        ----------
        event : str
            Name of the event to record.
        time : int
            Simulation time of the event.
        timestamp : str
            ISO 8601-formatted real-time string.
        return_event_uuid : str, optional
            Identifier of a corresponding return event, if any.
        **info
            Additional metadata fields to include in the log.
        """
        if not self.self_logging:
            return
        record = {
            "return_event_uuid":return_event_uuid,
            "time": timestamp,
            "time_offset": time,
            "event": event,
            "agent_id": self.agent_id,
            "agent_uuid": self.agent_uuid,
            "agent_uuid_codename": self.agent_uuid_codename,
        }
        record.update(info)
        self.activity_log[len(self.activity_log)] = record

# }}}
    # """Record when the agent enters the queue."""
    def enter_queue(self, time: int, timestamp: str) -> None:
# {{{
        """Record when the agent enters the queue."""
        # TODO - codex: the entire phrase "start_wait" is ambigious. use
        # less ambiguous language.
        self.wait_start = time
        self.log_event("start_wait", time, timestamp)
# }}}
    # Mark the ride complete and return wait time."""
    def finish_ride(
# {{{
        self, time: int, timestamp: str, return_event_uuid: str = ""
    ) -> int:
        """Complete the agent's current ride and record experience data.

        Marks the end of a ride cycle, updates ride counters, and logs a
        'ride_complete' event. Calculates the wait time based on when the
        agent entered the queue and resets relevant state fields.

        Parameters
        ----------
        time : int
            Simulation time at which the ride ends.
        timestamp : str
            ISO 8601-formatted real-time string.
        return_event_uuid : str, optional
            Identifier linking this ride completion to a prior event.

        Returns
        -------
        int
            Wait time in minutes from queue entry to ride completion.
        """
        wait_start = self.wait_start if self.wait_start is not None else time
        wait_time = time - wait_start
        self.rides_completed += 1
        self.boarded = False
        self.wait_start = None
        self.log_event(
            "ride_complete",
            time,
            timestamp,
            wait_time=wait_time,
            wait_time_readable=f"{wait_time} minutes",
            return_event_uuid=return_event_uuid,
        )
        return wait_time

# }}}
    # Return the most recent event not after ``dt``.
    def get_latest_event(self, dt: datetime) -> str:
# {{{
        """Return the most recent event not after ``dt``.

        Parameters
        ----------
        dt:
            Timestamp cutoff.

        Returns
        -------
        str
            Event name from the agent's activity log.

        Raises
        ------
        ValueError
            If no event occurred at or before ``dt``.
        """
        from datetime import datetime as _dt

        latest_event = None
        latest_time = None
        for record in self.activity_log.values():
            record_time = _dt.fromisoformat(record["time"])
            if (record_time <= dt and 
                    (latest_time is None or record_time > latest_time)):
                latest_time = record_time
                latest_event = record.get("event")

        if latest_event is None:
            raise ValueError("no event before provided datetime")

        return latest_event

# }}}
    # Return a formatted summary for the given experience.
    def traceback_experience(self, experience_id: str) -> str:
# {{{
        """Return a formatted summary for a specific agent experience.

        Retrieves the experience log matching the given ID and formats it
        into a human-readable report using a Jinja2 or string template. The
        report includes the logged metadata and a slice of recent agent
        activity for context.

        Parameters
        ----------
        experience_id : str
            Identifier of the experience entry to summarize.

        Returns
        -------
        str
            Rendered text describing the experience and context.

        Raises
        ------
        KeyError
            If no experience matches the provided ID.
        """
        from .helpers import load_asset_template

        for dt, info in self.experience_rideloop.log.items():
            if info.get("exp_id") == experience_id:
                context = {"time": dt.isoformat(), **info}

                context['full_dict'] = json.dumps(info, indent=4)
                context['agent_log_str'] = \
                    self.recent_agent_log_return_event_uuid(info["return_event_uuid"])
                tmpl = load_asset_template("agent-ride-exp.md.j2")
                if hasattr(tmpl, "render"):
                    return tmpl.render(**context)
                return tmpl.format(**context)

        raise KeyError(experience_id)

# }}}
    # Return a formatted slice of the agent log for a given return event.
    def recent_agent_log_return_event_uuid(self, return_event_uuid):
# {{{
        """Return a formatted slice of the agent log for a given return event.

        Finds the log entry matching the specified return event UUID and
        extracts a small window of prior events for context. Returns the
        subset as a pretty-printed JSON string.

        Parameters
        ----------
        return_event_uuid : str
            UUID of the return event to anchor the log slice.

        Returns
        -------
        str
            JSON-formatted string of recent log entries leading up to the event.
        """
        data = self.activity_log
        data = {str(uuid()):v for k,v in data.items()}
        df = pd.DataFrame.from_dict(data, orient='index')

        time = df[df['return_event_uuid'] == return_event_uuid]['time'].iloc[0]
        idx = (df[df['time'] <= time].sort_values(by=['time'], ascending=False)
                 .head(5).index.tolist())
        agent_log_str = json.dumps({k:v for k,v in data.items() if k in idx}, 
                                   indent=4)
        return agent_log_str
# }}}
    # Given a time, get agent state"""
    def get_state(self, time):
# {{{
        """Given a time, get agent state"""
        # TODO - if this needs to be exec cost optimized, can do a couple things
        # here 
        self.assert_possible_log_time(time)
        d = infer_agent_states(self, time)
        assert len(d) == 1
        self.current_state = next(iter(d.values())) 
        return self.current_state
# }}}
    # Raise exception if given time not within bounds of act log"""
    def assert_possible_log_time(self, time):
# {{{
        """Raise exception if given time not within bounds of act log"""
        df = self.get_activity_log_df()
        msg = 'given time should be within limits'
        assert time >= df['time_offset'].min() and time <= df['time_offset'].max(), msg
# }}}

    def get_rideloop_experience_log_df(self):
# {{{
        """Return dataframe version of activity log"""
        df = (pd.DataFrame.from_dict(self.experience_rideloop.log, orient='index')
                .reset_index().rename(columns={"index":"time"}))
        df['time'] = pd.to_datetime(df['time'])
        return df
# }}}

# {{{
    def get_activity_log_df(self):
# {{{
        """Return dataframe version of activity log"""
        df = pd.DataFrame.from_dict(self.activity_log, orient='index')
        df['time'] = pd.to_datetime(df['time'])
        return df
# }}}

    def __repr__(self) -> str:  # pragma: no cover - convenience
        return f"Agent({self.agent_id}) {self.agent_uuid_codename} {self.agent_uuid}"
