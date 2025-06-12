"""High level interface for running lift simulations."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timedelta

from zero_liftsim.main import (
    Simulation,
    Lift,
    Agent,
    ArrivalEvent,
    BoardingEvent,
    ReturnEvent,
)
from zero_liftsim.logging import Logger


class SimulationManager:
    """Configure and execute a lift simulation.

    Parameters
    ----------
    n_agents : int
        Number of agents that will participate in the simulation.
    lift_capacity : int
        Number of agents a lift can board per cycle.
    cycle_time : int
        Minutes for the lift to complete one round trip.
    start_datetime : datetime, optional
        When the simulation begins. Defaults to 2025-03-12 09:00.
    logger : Logger, optional
        Logger used during the run. Created automatically if omitted.
    """

    def __init__(
        self,
        *,
        n_agents: int,
        lift_capacity: int,
        cycle_time: int,
        start_datetime: datetime | None = None,
        logger: Logger | None = None,
    ) -> None:
        self.n_agents = n_agents
        self.lift_capacity = lift_capacity
        self.cycle_time = cycle_time
        self.start_datetime = start_datetime or datetime(2025, 3, 12, 9, 0, 0)
        self.logger = logger or Logger()
        self.sim: Simulation | None = None
        self.lift: Lift | None = None
        self.agents: list[Agent] = []
        self.arrival_times: list[int] = []

    def _setup(self) -> None:
        self.sim = Simulation()
        self.lift = Lift(self.lift_capacity, self.cycle_time)
        self.agents = [Agent(i + 1, logger=self.logger) for i in range(self.n_agents)]
        self.arrival_times = []
        for i, agent in enumerate(self.agents):
            self.arrival_times.append(i)
            ts = (self.start_datetime + timedelta(minutes=i)).isoformat()
            agent.start_wait(i, ts)
            self.sim.schedule(ArrivalEvent(agent, self.lift), i)

    def run(self) -> dict:
        """Execute the simulation and return summary metrics."""
        if self.sim is None:
            self._setup()
        assert self.sim is not None  # mypy hint
        self.sim.run(logger=self.logger, full_agent_logging=True, start_datetime=self.start_datetime)
        total_wait = 0
        for agent, arrive in zip(self.agents, self.arrival_times):
            if agent.board_time is not None:
                total_wait += agent.board_time - arrive
        avg_wait = total_wait / self.n_agents if self.n_agents > 0 else 0
        return {"total_rides": self.n_agents, "average_wait": avg_wait, "agents": self.agents}

    def archive_agent_rideloop_experience(self, directory: str | Path) -> None:
        """Write each agent's ride loop log to ``directory`` in JSON format."""
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        for agent in self.agents:
            data = {dt.isoformat(): info for dt, info in agent.rideloop.log.items()}
            outfile = path / f"agent_{agent.agent_id}.json"
            with outfile.open("w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2)

