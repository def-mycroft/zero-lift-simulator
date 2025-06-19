"""High level interface for running lift simulations."""

from __future__ import annotations

import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

from zero_liftsim.simulation import Simulation
from zero_liftsim.agent import Agent
from zero_liftsim.events import ArrivalEvent, BoardingEvent, ReturnEvent
from zero_liftsim.lift import Lift
from zero_liftsim.logging import Logger
from zero_liftsim.helpers import seed_from_uuid


class SimulationManager:
    """Configure and execute a lift simulation.

    This class manages the setup, execution, and result archiving of an
    agent-based ski lift simulation. Parameters are supplied via a nested
    configuration dictionary matching the structure returned by
    :func:`zero_liftsim.helpers.base_config`.

    Parameters
    ----------
    config : dict
        Configuration dictionary used to initialize the manager.

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

    def __init__(self, config: dict) -> None:
        sm_cfg = config.get("SimulationManager", {}).get("__init__", {})
        self.n_agents = sm_cfg.get("n_agents", 1)
        self.lift_capacity = sm_cfg.get("lift_capacity", 1)

        start_dt = sm_cfg.get("start_datetime")
        if isinstance(start_dt, str):
            start_dt = datetime.fromisoformat(start_dt)
        self.start_datetime = start_dt or datetime(2025, 3, 12, 9, 0, 0)

        logger = sm_cfg.get("logger")
        self.logger = logger if isinstance(logger, Logger) else Logger()

        self._run_cfg = config.get("SimulationManager", {}).get("run", {})
        self._sim_cfg = config.get("Simulation", {}).get("run", {})
        self._sim_init_cfg = config.get("Simulation", {}).get("__init__", {})
        self._lift_cfg = config.get("Lift", {})
        self._agent_cfg = config.get("Agent", {}).get("__init__", {})

        self.sim: Simulation | None = None
        self.lift: Lift | None = None
        self.agents: list[Agent] = []
        self.arrival_times: list[int] = []
        self.agent_exp_log_data = {}

    def _setup(self) -> None:
        self.sim = Simulation(**self._sim_init_cfg)
        num_chairs = self._lift_cfg.get("num_chairs", 50)
        self.lift = Lift(self.lift_capacity, num_chairs)
        for attr in ("ride_mean", "ride_sd", "traverse_mean", "traverse_sd"):
            if attr in self._lift_cfg:
                setattr(self.lift, attr, self._lift_cfg[attr])
        agent_kwargs = {"logger": self.logger}
        if "self_logging" in self._agent_cfg:
            agent_kwargs["self_logging"] = self._agent_cfg["self_logging"]
        self.agents = [Agent(i + 1, **agent_kwargs) for i in range(self.n_agents)]
        self.arrival_times = []
        for i, agent in enumerate(self.agents):
            self.arrival_times.append(i)
            ts = (self.start_datetime + timedelta(minutes=i)).isoformat()
            agent.enter_queue(i, ts)
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

        if end_datetime is None:
            cfg_end = self._run_cfg.get("end_datetime")
            if isinstance(cfg_end, str):
                end_datetime = datetime.fromisoformat(cfg_end)
            else:
                end_datetime = cfg_end

        if runtime_minutes is None:
            cfg_runtime = self._run_cfg.get("runtime_minutes")
            runtime_minutes = cfg_runtime

        if runtime_minutes is None:
            if end_datetime is None:
                default_end = self.start_datetime.replace(hour=16, minute=0, second=0, microsecond=0)
                end_datetime = default_end
            runtime_minutes = int((end_datetime - self.start_datetime).total_seconds() // 60)
        stop = runtime_minutes
        self.sim.run(
            stop_time=stop,
            logger=self.logger,
            full_agent_logging=self._sim_cfg.get("full_agent_logging", False),
            start_datetime=self.start_datetime,
            random_seed=seed_from_uuid(self.sim.simulation_uuid),
        )
        total_wait = 0.0
        total_rides = 0
        for agent in self.agents:
            total_rides += agent.rides_completed
            for info in agent.experience_rideloop.log.values():
                total_wait += info["time_spent_in_queue"]
        avg_wait = total_wait / total_rides if total_rides > 0 else 0

        return {"total_rides": total_rides, "average_wait": avg_wait, "agents": self.agents}

    # sklearn-style API --------------------------------------------------
    def fit(
        self,
        *,
        end_datetime: datetime | None = None,
        runtime_minutes: int | None = None,
    ) -> "SimulationManager":
        """Run the simulation and store results on the instance.

        Returns
        -------
        SimulationManager
            ``self`` for method chaining.
        """

        self.results_ = self.run(
            end_datetime=end_datetime,
            runtime_minutes=runtime_minutes,
        )
        return self

    def predict(self, X=None):
        """Return results from the most recent :meth:`fit` call."""

        if not hasattr(self, "results_"):
            raise RuntimeError("SimulationManager.fit must be called before predict")
        return self.results_

    def sample_agent(self):
        """Get a simple random sample of agents"""
        a = pd.Series(self.agents).sample().iloc[0]
        return a 

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

    def subset_agent_logs(self, agent):
        """Return log entries for ``agent`` as a DataFrame."""
        self.retrieve_data()
        df = self.agent_exp_log_data["agent_log"].copy(deep=True)
        m = df["agent_uuid"] == agent.agent_uuid
        return df[m]
