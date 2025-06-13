"""High level interface for running lift simulations."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timedelta

from zero_liftsim.main import (
    Simulation,
    Agent,
    ArrivalEvent,
    BoardingEvent,
    ReturnEvent,
)
from zero_liftsim.lift import Lift
from zero_liftsim.logging import Logger


class SimulationManager:
    """Configure and execute a lift simulation.

    This class manages the setup, execution, and result archiving
    of an agent-based ski lift simulation. It handles agent creation,
    lift initialization, event scheduling, and result summarization. Use
    :py:meth:`run` to execute the simulation for a given time window.

    Parameters
    ----------
    n_agents : int
        Number of agents that will participate in the simulation.
    lift_capacity : int
        Number of agents a lift can board per cycle.
    start_datetime : datetime, optional
        When the simulation begins. Defaults to 2025-03-12 09:00.
    logger : Logger, optional
        Logger used during the run. Created automatically if omitted.

    Attributes
    ----------
    sim : Simulation or None
        The simulation engine instance.
    lift : Lift or None
        The lift used during the simulation.
    agents : list of Agent
        All agents participating in the simulation.
    arrival_times : list of int
        Scheduled arrival times for agents.
    """
    def __init__(
        self,
        *,
        n_agents: int,
        lift_capacity: int,
        start_datetime: datetime | None = None,
        logger: Logger | None = None,
    ) -> None:
        self.n_agents = n_agents
        self.lift_capacity = lift_capacity
        self.start_datetime = start_datetime or datetime(2025, 3, 12, 9, 0, 0)
        self.logger = logger or Logger()
        self.sim: Simulation | None = None
        self.lift: Lift | None = None
        self.agents: list[Agent] = []
        self.arrival_times: list[int] = []
        self.agent_exp_log_data = {}

    def _setup(self) -> None:
        self.sim = Simulation()
        self.lift = Lift(self.lift_capacity)
        self.agents = [Agent(i + 1, logger=self.logger) for i in range(self.n_agents)]
        self.arrival_times = []
        for i, agent in enumerate(self.agents):
            self.arrival_times.append(i)
            ts = (self.start_datetime + timedelta(minutes=i)).isoformat()
            agent.start_wait(i, ts)
            self.sim.schedule(ArrivalEvent(agent, self.lift), i)

    def run(
        self,
        *,
        end_datetime: datetime | None = None,
        runtime_minutes: int | None = None,
    ) -> dict:
        """Execute the simulation and return summary metrics.

        Parameters
        ----------
        end_datetime:
            Optional absolute end time for the simulation. Takes precedence over
            ``runtime_minutes`` if both are provided.
        runtime_minutes:
            Duration of the run in minutes. Defaults to the number of minutes
            between ``start_datetime`` and 4 PM the same day.
        """
        if self.sim is None:
            self._setup()
        assert self.sim is not None  # mypy hint
        if runtime_minutes is None:
            if end_datetime is None:
                default_end = self.start_datetime.replace(hour=16, minute=0, second=0, microsecond=0)
                end_datetime = default_end
            runtime_minutes = int((end_datetime - self.start_datetime).total_seconds() // 60)
        stop = runtime_minutes
        self.sim.run(
            stop_time=stop,
            logger=self.logger,
            full_agent_logging=True,
            start_datetime=self.start_datetime,
        )
        total_wait = 0.0
        total_rides = 0
        for agent in self.agents:
            total_rides += agent.rides_completed
            for info in agent.experience_rideloop.log.values():
                total_wait += info["time_spent_in_queue"]
        avg_wait = total_wait / total_rides if total_rides > 0 else 0
        return {"total_rides": total_rides, "average_wait": avg_wait, "agents": self.agents}

    def archive_agent_rideloop_experience(self, directory: str | Path) -> None:
        """Write each agent's ride loop log to ``directory`` in JSON format."""
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        for agent in self.agents:
            data = {dt.isoformat(): info for dt, info in agent.experience_rideloop.log.items()}
            outfile = path / f"agent-id-{agent.agent_id}-uuid-{agent.agent_uuid}.json"
            with outfile.open("w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2)

    def lookup_agent(self, agent_uuid):
        """Return agent class given agent_uuid"""
        d = {i:v for i,v in [(a.agent_uuid, a) for a in self.agents]}
        return d[agent_uuid]

    def retrieve_data(self):
        """Retrieve key dataframes that summarize simulation"""
        import pandas as pd
        data = {}
        for k in ['exp_rideloop', 'agent_log']:
            data[k] = pd.DataFrame()
        for agent in self.agents:
            exp_rideloop = {dt.isoformat(): info 
                            for dt, info in agent.experience_rideloop.log.items()}
            e = pd.DataFrame(exp_rideloop).T
            data['exp_rideloop'] = pd.concat([e, data['exp_rideloop']])

            # agent log 
            l = pd.DataFrame(agent.activity_log).T
            data['agent_log'] = pd.concat([l, data['agent_log']])

        data['exp_rideloop'] = (data['exp_rideloop'].reset_index(drop=False)
                                                    .rename(columns={'index':'time'})
                                )
        for k in data.keys():
            data[k]['time'] = pd.to_datetime(data[k]['time'])

        self.agent_exp_log_data = data

        return data


