"""Lift model for Zero Lift Simulator."""

from __future__ import annotations

from collections import deque
from random import gauss

from .agent import Agent


class Lift:
    """Single ski lift managing a FIFO queue and transport cycles."""

    def __init__(self, capacity: int, num_chairs: int = 50) -> None:
        """Initialize lift parameters.

        Parameters
        ----------
        capacity:
            Number of riders each chair can hold.
        num_chairs:
            Total number of chairs circulating on the lift.
        """

        self.capacity = capacity
        self.num_chairs = num_chairs
        self.queue: deque[Agent] = deque()
        self.state: str = "idle"
        self.current_riders: list[list[Agent]] = []
        self.chairs_available = num_chairs
        self.chairs_in_transit = 0

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

        if self.chairs_available == 0:
            return []

        boarded: list[Agent] = []
        while self.queue and len(boarded) < self.capacity:
            agent = self.queue.popleft()
            agent.boarded = True
            boarded.append(agent)

        if boarded:
            self.state = "moving"
            self.current_riders.append(list(boarded))
            self.chairs_available -= 1
            self.chairs_in_transit += 1

        return boarded

    def mark_idle(self) -> None:
        """Mark the lift completely idle, resetting all chairs."""

        self.state = "idle"
        self.current_riders = []
        self.chairs_available = self.num_chairs
        self.chairs_in_transit = 0

    def chair_return(self, riders: list[Agent]) -> None:
        """Mark a single chair as returned to the base."""

        if riders in self.current_riders:
            self.current_riders.remove(riders)
        self.chairs_available += 1
        self.chairs_in_transit = max(self.chairs_in_transit - 1, 0)
        if self.chairs_in_transit == 0:
            self.state = "idle"

    # -- chair info ------------------------------------------------------
    def available_chairs(self) -> int:
        """Return the number of chairs currently at the base."""

        return self.chairs_available

    def total_chairs(self) -> int:
        """Return the total number of chairs on the lift."""

        return self.num_chairs

    def riders_in_transit(self) -> int:
        """Return the number of riders currently on the lift."""

        return sum(len(r) for r in self.current_riders)
