"""Core library for Zero Lift Simulator."""

from __future__ import annotations

"""
One-lift simulation kernel scaffold.
This module defines the foundational class structure for an agent-based
simulation of skier-lift interaction at a ski resort. Each class is a placeholder
with a development-oriented docstring describing its intended role and expansion path.
"""

import heapq
from collections import deque

from .logging import Logger


class Simulation:  
    """Simulation engine that manages global time and the event queue.
    # {{{

    The simulator runs a discrete-event loop. Events are stored in a ``heapq``
    as ``(timestamp, counter, event)`` tuples. ``counter`` ensures deterministic
    ordering of events scheduled for the same ``timestamp``.

    ``schedule`` is used to add events to the queue. ``run`` pops events in
    time order, advances ``current_time`` and executes each event. ``Event``
    objects may optionally return iterables of ``(event, time)`` pairs which are
    automatically scheduled.
    """

    def __init__(self) -> None:
        self.current_time: int = 0
        self._counter: int = 0
        self._queue: list[tuple[int, int, Event]] = []

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

    def run(self, stop_time: int | None = None, logger: "Logger" | None = None) -> None:
        """Execute events in chronological order.

        Parameters
        ----------
        stop_time:
            Optional time limit. The simulation stops when the next event's
            timestamp exceeds this value.
        """

        while self._queue:
            time, _, event = heapq.heappop(self._queue)
            if stop_time is not None and time > stop_time:
                self.current_time = stop_time
                break
            self.current_time = time
            if logger is not None:
                q_len = getattr(event, "lift", None)
                q_len = q_len.queue_length() if q_len else 0
                logger.log(event.__class__.__name__, time, queue_length=q_len)
            new_events = event.execute(self)
            if new_events:
                for evt, evt_time in new_events:
                    self.schedule(evt, evt_time)
# }}}


class Lift: 
    """Represents a single ski lift with queue and transport behavior.
    # {{{

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
    """

    def __init__(self, capacity: int, cycle_time: int) -> None:
        self.capacity = capacity
        self.cycle_time = cycle_time
        self.queue: deque[Agent] = deque()
        self.state: str = "idle"

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

        return boarded

    def mark_idle(self) -> None:
        """Mark the lift as idle after completing a cycle."""

        self.state = "idle"
# }}}


class Event:  
    """Abstract base class for all simulation events.
    # {{{

    Each event represents a time stamped occurrence that alters the state of
    the system. Subclasses must override :py:meth:`execute` and may optionally
    return an iterable of ``(event, time)`` pairs to schedule additional
    events.
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
# }}}


class Agent:  
    """Represents a skier and their evolving state during the simulation.
    # {{{

    Parameters
    ----------
    agent_id:
        Unique identifier for the agent.

    Notes
    -----
    Agents track when they start waiting for the lift, the time they board,
    and how many rides they have completed. ``start_wait`` and ``finish_ride``
    update this state so statistics can be gathered over the course of a day.
    """

    def __init__(self, agent_id: int) -> None:
        self.agent_id = agent_id
        self.boarded: bool = False
        self.wait_start: int | None = None
        self.board_time: int | None = None
        self.rides_completed: int = 0

    def start_wait(self, time: int) -> None:
        """Record the time the agent begins waiting in the queue."""

        self.wait_start = time

    def finish_ride(self, time: int) -> int:
        """Mark the current ride complete and return the wait time.

        Parameters
        ----------
        time:
            Timestamp when the ride finishes.

        Returns
        -------
        int
            The wait time experienced for this ride.
        """

        wait_start = self.wait_start if self.wait_start is not None else time
        wait_time = time - wait_start
        self.rides_completed += 1
        self.boarded = False
        self.wait_start = None
        return wait_time

    def __repr__(self) -> str:  # pragma: no cover - convenience
        return f"Agent({self.agent_id})"
# }}}


class ArrivalEvent(Event):  
    """Event representing an agent arriving at the lift queue."""
    # {{{

    def __init__(self, agent: Agent, lift: Lift) -> None:
        self.agent = agent
        self.lift = lift

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Enqueue the agent and possibly trigger boarding."""

        self.lift.enqueue(self.agent)
        events: list[tuple[Event, int]] = []
        if self.lift.state == "idle":
            events.append((BoardingEvent(self.lift), simulation.current_time))
        return events
# }}}


class BoardingEvent(Event):  
    """Event indicating the lift starts loading queued agents."""
    # {{{

    def __init__(self, lift: Lift) -> None:
        self.lift = lift

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Load agents and schedule the lift's return."""

        boarded = self.lift.load()
        for agent in boarded:
            agent.board_time = simulation.current_time
        if boarded:
            return [
                (ReturnEvent(self.lift), simulation.current_time + self.lift.cycle_time)
            ]
        return []
# }}}


class ReturnEvent(Event):  
    """Event signifying the lift has returned from its cycle."""
    # {{{

    def __init__(self, lift: Lift) -> None:
        self.lift = lift

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Mark the lift idle and trigger new boarding if needed."""

        self.lift.mark_idle()
        events: list[tuple[Event, int]] = []
        if self.lift.queue_length() > 0:
            events.append((BoardingEvent(self.lift), simulation.current_time))
        return events
# }}}


def run_alpha_sim(n_agents: int, lift_capacity: int, cycle_time: int) -> dict:
    """Run a minimal simulation and return basic metrics."""

    logger = Logger()
    sim = Simulation()
    lift = Lift(lift_capacity, cycle_time)
    agents = [Agent(i + 1) for i in range(n_agents)]
    arrival_times: list[int] = []

    for i, agent in enumerate(agents):
        arrival_times.append(i)
        agent.start_wait(i)
        sim.schedule(ArrivalEvent(agent, lift), i)

    sim.run(logger=logger)

    total_wait = 0
    for agent, arrive in zip(agents, arrival_times):
        if agent.board_time is not None:
            total_wait += agent.board_time - arrive

    avg_wait = total_wait / n_agents if n_agents > 0 else 0

    return {"total_rides": n_agents, "average_wait": avg_wait}


def run(args) -> None:
    """Handle CLI commands."""
    if getattr(args, "command", None) == "dev" and args.update_toc:
        from . import dev

        dev.update_toc()

