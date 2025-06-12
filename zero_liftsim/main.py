"""Core library for Zero Lift Simulator."""

from __future__ import annotations

import heapq
from uuid import uuid4 as uuid
try:
    from codenamize import codenamize
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without the package
    def codenamize(value: str) -> str:
        """Simplistic fallback that returns the first eight characters."""
        return value[:8]
from collections import deque

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
                logger.log(event.__class__.__name__, time, queue_length=q_len)
            new_events = event.execute(self)
            if new_events:
                for evt, evt_time in new_events:
                    self.schedule(evt, evt_time)
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
# }}}

class Agent:
    """Represents an individual skier within the simulation.
    # {{{

    # {{{
    Each agent tracks its interaction with the lift system, including
    wait times, boarding events, and the number of completed rides. This
    class supports state updates necessary to compute performance metrics
    such as total wait time and ride count.

    Parameters
    ----------
    agent_id : int
        Unique identifier assigned to the agent.

    Attributes
    ----------
    agent_id : int
        Identifier for the agent instance.
    boarded : bool
        Whether the agent is currently on the lift.
    wait_start : int or None
        Simulation time when the agent began waiting in the queue.
    board_time : int or None
        Time at which the agent boarded the lift.
    rides_completed : int
        Number of lift rides completed by the agent.
    # }}}
    """
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
        if logger is not None:
            logger.devlog(
                f"init agent {self.agent_uuid} {self.agent_uuid_codename}"
            )
            self.logger = logger

    def log_event(self, event: str, time: int, **info) -> None:
        """Append a record to :pyattr:`activity_log` if self logging is enabled."""

        if not self.self_logging:
            return
        record = {
            "time": time,
            "event": event,
            "agent_id": self.agent_id,
            "agent_uuid": self.agent_uuid,
            "agent_uuid_codename": self.agent_uuid_codename,
        }
        record.update(info)
        self.activity_log[len(self.activity_log)] = record

    def start_wait(self, time: int) -> None:
        """Record the time the agent begins waiting in the queue."""

        self.wait_start = time
        self.log_event("start_wait", time)

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
        self.log_event("ride_complete", time, wait_time=wait_time)
        return wait_time

    def __repr__(self) -> str:  # pragma: no cover - convenience
        return f"Agent({self.agent_id})"
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
        self.agent.log_event(
            "arrival",
            simulation.current_time,
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
            agent.log_event(
                "board",
                simulation.current_time,
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
            agent.finish_ride(simulation.current_time)
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
    agents = [Agent(i + 1, logger=logger) for i in range(n_agents)]
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

    return {"total_rides": n_agents, "average_wait": avg_wait, "agents": agents}


def run(args) -> None:
    """Handle CLI commands."""
    if getattr(args, "command", None) == "dev" and args.update_toc:
        from . import dev

        dev.update_toc()

