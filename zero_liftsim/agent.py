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


class Agent:
    """Represents an individual skier within the simulation."""

    def __init__(
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
        self.activity_log: dict[int, dict] = {}
        self.experience_rideloop = AgentRideLoopExperience()
        if logger is not None:
            logger.devlog(
                f"init agent {self.agent_uuid} {self.agent_uuid_codename}"
            )
            self.logger = logger

    def log_event(
        self,
        event: str,
        time: int,
        timestamp: str,
        return_event_uuid: str = "",
        **info,
    ) -> None:
        """Record an event in :attr:`activity_log`.

        Parameters
        ----------
        event : str
            Event name.
        time : int
            Simulation time of the event.
        timestamp : str
            ISO formatted timestamp.
        return_event_uuid : str, optional
            Identifier for a related :class:`ReturnEvent`.
        **info
            Additional metadata to record.
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

    def start_wait(self, time: int, timestamp: str) -> None:
        """Record when the agent enters the queue."""

        self.wait_start = time
        self.log_event("start_wait", time, timestamp)

    def finish_ride(
        self, time: int, timestamp: str, return_event_uuid: str = ""
    ) -> int:
        """Mark the ride complete and return wait time."""

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

    def get_latest_event(self, dt: datetime) -> str:
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
            if record_time <= dt and (latest_time is None or record_time > latest_time):
                latest_time = record_time
                latest_event = record.get("event")

        if latest_event is None:
            raise ValueError("no event before provided datetime")

        return latest_event

    def traceback_experience(self, experience_id: str) -> str:
        """Return a formatted summary for the given experience.

        Parameters
        ----------
        experience_id : str
            Identifier of the experience entry to summarize.

        Returns
        -------
        str
            Rendered text describing the experience.

        Raises
        ------
        KeyError
            If ``experience_id`` does not exist.
        """

        from .helpers import load_asset_template

        for dt, info in self.experience_rideloop.log.items():
            if info.get("exp_id") == experience_id:
                context = {"time": dt.isoformat(), **info}

                context['full_dict'] = json.dumps(info, indent=4)
                context['agent_log_str'] = self.recent_agent_log_return_event_uuid(info["return_event_uuid"])
                tmpl = load_asset_template("agent-ride-exp.md.j2")
                if hasattr(tmpl, "render"):
                    return tmpl.render(**context)
                return tmpl.format(**context)

        raise KeyError(experience_id)


    def recent_agent_log_return_event_uuid(self, return_event_uuid):
        """Create a subset of log and return readable json string"""
        data = self.activity_log
        data = {str(uuid()):v for k,v in data.items()}
        df = pd.DataFrame.from_dict(data, orient='index')

        time = df[df['return_event_uuid'] == return_event_uuid]['time'].iloc[0]
        idx = (df[df['time'] <= time].sort_values(by=['time'], ascending=False)
                 .head(5).index.tolist())
        agent_log_str = json.dumps({k:v for k,v in data.items() if k in idx}, 
                                   indent=4)
        return agent_log_str


    def __repr__(self) -> str:  # pragma: no cover - convenience
        return f"Agent({self.agent_id}) {self.agent_uuid_codename} {self.agent_uuid}"
