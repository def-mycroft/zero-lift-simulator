"""Lift model for Zero Lift Simulator."""

from __future__ import annotations

from collections import deque
from random import gauss

from .agent import Agent


class Lift:
    """Single ski lift managing a FIFO queue and transport cycles."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
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
