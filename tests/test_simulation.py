import sys
from pathlib import Path

import pytest
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.main import Simulation, Event


class RecorderEvent(Event):
    def __init__(self, label, log):
        self.label = label
        self.log = log

    def execute(self, sim):
        self.log.append((self.label, sim.current_time))
        return []


def test_events_execute_in_time_order():
    log = []
    sim = Simulation()
    sim.schedule(RecorderEvent('e1', log), 5)
    sim.schedule(RecorderEvent('e2', log), 1)
    sim.schedule(RecorderEvent('e3', log), 3)
    sim.run(start_datetime=datetime(2025, 3, 12, 9, 0, 0))
    assert [label for label, _ in log] == ['e2', 'e3', 'e1']
    assert [time for _, time in log] == [1, 3, 5]


def test_tied_events_preserve_insertion_order():
    log = []
    sim = Simulation()
    sim.schedule(RecorderEvent('first', log), 2)
    sim.schedule(RecorderEvent('second', log), 2)
    sim.run(start_datetime=datetime(2025, 3, 12, 9, 0, 0))
    assert [label for label, _ in log] == ['first', 'second']
    assert [time for _, time in log] == [2, 2]
