"""Event definitions for the Zero Lift simulator."""

from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4 as uuid

from .agent import Agent
from .lift import Lift
from .logging import Logger


class Event:
    """Base class for simulation events."""

    def execute(self, simulation: "Simulation") -> list[tuple["Event", int]] | None:
        """Execute the event."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    def _log_agent_event(
        self,
        simulation: "Simulation",
        agent: Agent,
        description: str,
        **info,
    ) -> None:
        if simulation._agent_logger is None:
            return
        entry = {
            "agent_uuid": agent.agent_uuid,
            "agent_codename": agent.agent_uuid_codename,
            "simulation_uuid": simulation.simulation_uuid,
            "simulation_codename": simulation.simulation_codename,
            "description": description,
        }
        entry.update(info)
        timestamp = (
            simulation.start_datetime + timedelta(minutes=simulation.current_time)
        ).isoformat()
        simulation._agent_logger.log(
            self.__class__.__name__, simulation.current_time, timestamp, **entry
        )
        simulation._agent_records.append(
            {
                "event": self.__class__.__name__,
                "time": timestamp,
                "time_offset": simulation.current_time,
                **entry,
            }
        )


class ArrivalEvent(Event):
    """Agent arrives at the lift queue."""

    def __init__(self, agent: Agent, lift: Lift) -> None:
        self.agent = agent
        self.lift = lift

    def execute(self, simulation: "Simulation") -> list[tuple[Event, int]]:
        self.lift.enqueue(self.agent)
        timestamp = (
            simulation.start_datetime + timedelta(minutes=simulation.current_time)
        ).isoformat()
        self.agent.log_event(
            "arrival",
            simulation.current_time,
            timestamp,
            queue_length=self.lift.queue_length(),
            lift_state=self.lift.state,
        )
        self._log_agent_event(
            simulation,
            self.agent,
            "arrival",
            queue_length=self.lift.queue_length(),
            lift_state=self.lift.state,
        )
        events: list[tuple[Event, int]] = []
        if self.lift.state == "idle" and self.lift.available_chairs() > 0:
            events.append((BoardingEvent(self.lift), simulation.current_time))
        return events


class BoardingEvent(Event):
    """Load agents onto the lift."""

    def __init__(self, lift: Lift) -> None:
        self.lift = lift

    def execute(self, simulation: "Simulation") -> list[tuple[Event, int]]:
        boarded = self.lift.load()
        ride_time = self.lift.time_spent_ride_lift() if boarded else 0
        for agent in boarded:
            agent.board_time = simulation.current_time
            agent._ride_duration = ride_time
            timestamp = (
                simulation.start_datetime
                + timedelta(minutes=simulation.current_time)
            ).isoformat()
            agent.log_event(
                "board",
                simulation.current_time,
                timestamp,
                queue_length=self.lift.queue_length(),
                lift_state=self.lift.state,
            )
            self._log_agent_event(
                simulation,
                agent,
                "board",
                queue_length=self.lift.queue_length(),
                lift_state=self.lift.state,
            )
        events: list[tuple[Event, int]] = []
        if boarded:
            events.append(
                (
                    ReturnEvent(self.lift, boarded),
                    simulation.current_time + int(ride_time),
                )
            )
            if self.lift.queue_length() > 0 and self.lift.available_chairs() > 0:
                events.append((BoardingEvent(self.lift), simulation.current_time))
        return events


class ReturnEvent(Event):
    """Lift returns to base and agents complete ride."""

    def __init__(self, lift: Lift, boarded: list[Agent] | None = None) -> None:
        self.lift = lift
        self.boarded = boarded or []
        self.return_event_uuid = str(uuid())

    def execute(self, simulation: "Simulation") -> list[tuple[Event, int]]:
        events: list[tuple[Event, int]] = []
        for agent in self.boarded:
            timestamp_dt = (
                simulation.start_datetime
                + timedelta(minutes=simulation.current_time)
            )
            queue_duration = 0
            if agent.wait_start is not None and agent.board_time is not None:
                queue_duration = agent.board_time - agent.wait_start
            ride_dur = getattr(agent, "_ride_duration", self.lift.time_spent_ride_lift())
            traverse_dur = self.lift.time_spent_traverse_down_mountain()
            agent.experience_rideloop.add_entry(
                agent,
                self.return_event_uuid,
                timestamp_dt,
                ride_dur,
                traverse_dur,
                queue_duration,
            )
            agent.finish_ride(
                simulation.current_time,
                timestamp_dt.isoformat(),
                self.return_event_uuid,
            )
            next_arrival = simulation.current_time + int(traverse_dur)
            if simulation.stop_time is not None and next_arrival < simulation.stop_time:
                ts = (
                    simulation.start_datetime
                    + timedelta(minutes=next_arrival)
                ).isoformat()
                agent.enter_queue(next_arrival, ts)
                events.append((ArrivalEvent(agent, self.lift), next_arrival))
        self.lift.chair_return(self.boarded)
        for agent in self.boarded:
            self._log_agent_event(
                simulation,
                agent,
                "completed ride",
                queue_length=self.lift.queue_length(),
                lift_state=self.lift.state,
            )
        if self.lift.queue_length() > 0 and self.lift.available_chairs() > 0:
            events.append((BoardingEvent(self.lift), simulation.current_time))
        return events
