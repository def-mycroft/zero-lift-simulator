"""Legacy entry point exposing simulation primitives."""

from __future__ import annotations

from .simulation import Simulation, run_alpha_sim
from .events import Event, ArrivalEvent, BoardingEvent, ReturnEvent
from .agent import Agent
from .lift import Lift

__all__ = [
    "Simulation",
    "run_alpha_sim",
    "Event",
    "ArrivalEvent",
    "BoardingEvent",
    "ReturnEvent",
    "Agent",
    "Lift",
]
