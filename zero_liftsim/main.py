"""Core library for Zero Lift Simulator."""

from __future__ import annotations

import heapq
from uuid import uuid4 as uuid
from datetime import datetime, timedelta
try:
    from codenamize import codenamize
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without the package
    def codenamize(value: str) -> str:
        """Simplistic fallback that returns the first eight characters."""
        return value[:8]
from collections import deque
from random import gauss

from .agent import Agent

from .logging import Logger


class Simulation:
    """Engine for managing event-driven skier-lift interactions.
    # {{{

    # {{{
    The Simulation class implements a discrete-event simulation
    architecture where system evolution is driven by time-stamped
    events. Events are managed in a min-heap priority queue sorted by
    execution time and insertion order. The simulation clock advances to
    the time of each event, which is then executed to update system
    state and potentially schedule future events.

    Events are scheduled using `schedule`, and the simulation is
    started via `run`. Each event may return new events to be scheduled
    dynamically. A logger may be passed to `run` to record per-event
    state for analysis or debugging.

    Parameters
    ----------
    None

    Attributes
    ----------
    current_time : int
        The current time in simulation units (typically minutes).
    _counter : int
        A tie-breaker counter to ensure deterministic event ordering.
    _queue : list of tuple[int, int, Event]
        Priority queue of scheduled events, ordered by time and counter.

    Notes
    -----
    The simulation engine is agnostic to domain logic. It provides
    deterministic execution of arbitrary event objects that implement
    an `execute(sim)` method.
    # }}}
    """
    def __init__(self) -> None:
        self.current_time: int = 0
        self._counter: int = 0
        self._queue: list[tuple[int, int, Event]] = []
        self._agent_logger: Logger | None = None
        self._agent_records: list[dict] = []
        self.simulation_uuid = str(uuid())
        self.simulation_codename = codenamize(self.simulation_uuid)

    def schedule(self, event: "Event", time: int) -> None:
        """Schedule ``event`` to run at ``time``.

        Parameters
        ----------
        event:
            The event instance to schedule.
        time:
            Timestamp at which the event should execute.
        """

        heapq.heappush(self._queue, (time, self._counter, event))
        self._counter += 1

    def run(
        self,
        stop_time: int | None = None,
        logger: "Logger" | None = None,
        *,
        full_agent_logging: bool = False,
        start_datetime: datetime = datetime(2025, 3, 12, 9, 0, 0),
    ) -> None:
        """Execute events in chronological order.

        Parameters
        ----------
        stop_time:
            Optional time limit. The simulation stops when the next event's
            timestamp exceeds this value.
        """

        self.start_datetime = start_datetime
        if full_agent_logging:
            self._agent_logger = Logger("agent.log")
            self._agent_records = []
        else:
            self._agent_logger = None
            self._agent_records = []

        i = str(uuid())
        while self._queue:
            time, _, event = heapq.heappop(self._queue)
            if stop_time is not None and time > stop_time:
                self.current_time = stop_time
                break
            self.current_time = time
            if logger is not None:
                q_len = getattr(event, "lift", None)
                q_len = q_len.queue_length() if q_len else 0
                timestamp = (self.start_datetime + timedelta(minutes=time)).isoformat()
                logger.log(
                    event.__class__.__name__,
                    time,
                    timestamp,
                    queue_length=q_len,
                )
            new_events = event.execute(self)
            if new_events:
                for evt, evt_time in new_events:
                    self.schedule(evt, evt_time)

        self._agent_logger = None

    def agent_records(self) -> list[dict]:
        """Return collected agent-level log entries."""

        return list(self._agent_records)
# }}}

class Lift: 
    """Single ski lift managing a FIFO queue and transport cycles.
    # {{{

    # {{{
    The Lift handles agent queuing, loading, and state transitions between
    idle and moving. It does not schedule simulation events directly; instead,
    it exposes methods that allow external events to enqueue agents, load
    passengers, and mark the lift as idle after completing a cycle.

    Parameters
    ----------
    capacity : int
        Maximum number of agents that can board the lift per cycle.
    cycle_time : int
        Total time, in minutes, for the lift to complete a round trip.

    Attributes
    ----------
    queue : deque of Agent
        The FIFO queue of agents waiting to board.
    state : str
        Current state of the lift, either 'idle' or 'moving'.

    Notes
    -----
    Agents are removed from the queue in order of arrival. Once boarding is
    complete, the lift enters the 'moving' state and must be marked idle by
    an external event (typically a ReturnEvent) before boarding can resume.
    """

    """Represents a single ski lift with queue and transport behavior.

    Parameters
    ----------
    capacity:
        Maximum number of agents that can board per cycle.
    cycle_time:
        Minutes from departure to return.

    Notes
    -----
    The lift is passive: it exposes state and queue operations but does not
    schedule events itself. External ``Event`` objects manipulate the lift via
    these methods.
    # }}}
    """
    def __init__(self, capacity: int, cycle_time: int) -> None:
        self.capacity = capacity
        self.cycle_time = cycle_time
        self.queue: deque[Agent] = deque()
        self.state: str = "idle"
        self.current_riders: list[Agent] = []
        self.ride_mean = 7
        self.ride_sd = 1
        self.traverse_mean = 5
        self.traverse_sd = 1.5

    def time_spent_ride_lift(self) -> float:
        """Sample the time to ride the lift."""

        return max(1, gauss(self.ride_mean, self.ride_sd))

    def time_spent_traverse_down_mountain(self) -> float:
        """Sample the time to ski down from the lift."""

        return max(1, gauss(self.traverse_mean, self.traverse_sd))

    # -- queue operations -------------------------------------------------
    def enqueue(self, agent: Agent) -> None:
        """Add ``agent`` to the end of the waiting queue."""

        self.queue.append(agent)

    def queue_length(self) -> int:
        """Return the current number of waiting agents."""

        return len(self.queue)

    # -- loading ----------------------------------------------------------
    def load(self) -> list[Agent]:
        """Load agents from the queue up to ``capacity`` and set state.

        Returns
        -------
        list[Agent]
            Agents that boarded the lift.
        """

        if self.state != "idle":
            return []

        boarded: list[Agent] = []
        while self.queue and len(boarded) < self.capacity:
            agent = self.queue.popleft()
            agent.boarded = True
            boarded.append(agent)

        if boarded:
            self.state = "moving"
            self.current_riders = list(boarded)

        return boarded

    def mark_idle(self) -> None:
        """Mark the lift as idle after completing a cycle."""

        self.state = "idle"
        self.current_riders = []
# }}}

class Event:
    """Abstract base class for all simulation events.
    # {{{

    # {{{
    Each event represents a discrete occurrence at a specific simulation
    timestamp. Events are responsible for advancing the simulation state
    by executing their logic and optionally scheduling new events.

    Subclasses must implement the `execute` method, which modifies the
    simulation and returns an iterable of `(event, time)` pairs to be
    added to the event queue.

    Notes
    -----
    All event subclasses should be stateless beyond the data required
    to perform their task. They should not hold references to global
    objects or manipulate simulation state outside their intended scope.
    # }}}
    """
    def execute(self, simulation: "Simulation") -> list[tuple["Event", int]] | None:
        """Execute the event.

        Parameters
        ----------
        simulation:
            The :class:`Simulation` instance managing the event loop.

        Returns
        -------
        list[tuple[Event, int]] | None
            Optional iterable of new events and their execution times.
        """

        raise NotImplementedError

    # ------------------------------------------------------------------
    def _log_agent_event(
        self,
        simulation: "Simulation",
        agent: "Agent",
        description: str,
        **info,
    ) -> None:
        """Log an agent-related event if agent logging is active."""

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
# }}}


class ArrivalEvent(Event):
    """Event representing a skier's arrival at the lift queue.
    # {{{

    # {{{
    This event models the moment an agent reaches the lift line and 
    joins the queue. If the lift is currently idle, this event also 
    schedules a `BoardingEvent` immediately to initiate loading.

    Parameters
    ----------
    agent : Agent
        The skier agent arriving at the lift.
    lift : Lift
        The lift the agent will attempt to board.

    Notes
    -----
    This event does not handle skiing down or departure; it only 
    concerns lift-side behavior at arrival.
    # }}}
    """
    def __init__(self, agent: Agent, lift: Lift) -> None:
        self.agent = agent
        self.lift = lift

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Enqueue the agent and possibly trigger boarding."""

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
        if self.lift.state == "idle":
            events.append((BoardingEvent(self.lift), simulation.current_time))
        return events
# }}}

class BoardingEvent(Event):
    """Event indicating the lift begins boarding agents from the queue.
    # {{{

    # {{{
    When triggered, this event attempts to load agents onto the lift up to
    its capacity. If agents are successfully boarded, it schedules a
    `ReturnEvent` corresponding to the end of the lift's cycle. Boarding only
    occurs if the lift is currently idle.

    Parameters
    ----------
    lift : Lift
        The lift instance associated with this boarding event.

    Returns
    -------
    list of tuple[Event, int]
        A list containing the next scheduled `ReturnEvent` if agents were
        loaded; otherwise, an empty list.

    Notes
    -----
    This event modifies agent state by setting their `board_time` to the
    current simulation time and updating the lift's internal state to "moving".
    # }}}
    """
    def __init__(self, lift: Lift) -> None:
        self.lift = lift

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Load agents and schedule the lift's return."""

        boarded = self.lift.load()
        for agent in boarded:
            agent.board_time = simulation.current_time
            agent._ride_duration = self.lift.time_spent_ride_lift()
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
        if boarded:
            return [
                (
                    ReturnEvent(self.lift, boarded),
                    simulation.current_time + self.lift.cycle_time,
                )
            ]
        return []
# }}}

class ReturnEvent(Event):
    """Event indicating the lift completes its transport cycle.
    # {{{

    # {{{
    This event is scheduled when the lift finishes a run and becomes available
    to load new agents. Upon execution, it sets the lift state to "idle" and
    optionally schedules a new `BoardingEvent` if agents are still queued.

    Parameters
    ----------
    lift : Lift
        The lift instance associated with this return event.

    Returns
    -------
    list[tuple[Event, int]]
        A list containing a new `BoardingEvent` scheduled at the current time,
        if the lift queue is non-empty. Otherwise, returns an empty list.

    Notes
    -----
    ReturnEvent does not manipulate agent state directly. It only updates the
    lift's availability and determines whether a boarding cycle should resume.
    # }}}
    """
    def __init__(self, lift: Lift, boarded: list[Agent] | None = None) -> None:
        self.lift = lift
        self.boarded = boarded or []

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Mark the lift idle and trigger new boarding if needed."""
        for agent in self.boarded:
            timestamp_dt = (
                simulation.start_datetime
                + timedelta(minutes=simulation.current_time)
            )
            queue_duration = 0
            if agent.wait_start is not None and agent.board_time is not None:
                queue_duration = agent.board_time - agent.wait_start
            ride_dur = getattr(agent, "_ride_duration", self.lift.cycle_time)
            traverse_dur = self.lift.time_spent_traverse_down_mountain()
            agent.experience_rideloop.add_entry(
                timestamp_dt,
                ride_dur,
                traverse_dur,
                queue_duration,
            )
            agent.finish_ride(simulation.current_time, timestamp_dt.isoformat())
        self.lift.mark_idle()
        for agent in self.boarded:
            self._log_agent_event(
                simulation,
                agent,
                "completed ride",
                queue_length=self.lift.queue_length(),
                lift_state=self.lift.state,
            )
        events: list[tuple[Event, int]] = []
        if self.lift.queue_length() > 0:
            events.append((BoardingEvent(self.lift), simulation.current_time))
        return events
# }}}

def run_alpha_sim(
    n_agents: int,
    lift_capacity: int,
    cycle_time: int,
    *,
    start_datetime: datetime | None = None,
) -> dict:
    """Run a minimal simulation and return basic metrics."""

    from zero_liftsim.simmanager import SimulationManager

    manager = SimulationManager(
        n_agents=n_agents,
        lift_capacity=lift_capacity,
        cycle_time=cycle_time,
        start_datetime=start_datetime,
    )
    return manager.run()

