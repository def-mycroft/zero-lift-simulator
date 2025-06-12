Bugfix - missing riders object 

random codename: complex-government 3d6a2886

*** 
============================= test session starts ==============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /home/zero/code-repos/zero-lift-simulator
collected 16 items

tests/test_agent.py ..F.                                                 [ 25%]
tests/test_alpha_sim.py FFF.                                             [ 50%]
tests/test_events.py F                                                   [ 56%]
tests/test_full_agent_logging.py FF                                      [ 68%]
tests/test_lift.py ...                                                   [ 87%]
tests/test_simulation.py ..                                              [100%]

=================================== FAILURES ===================================
_____________________ test_activity_log_enabled_via_events _____________________

    def test_activity_log_enabled_via_events():
        sim = Simulation()
        lift = Lift(capacity=1, cycle_time=5)
        agent = Agent(3)
        agent.start_wait(0)
        sim.schedule(ArrivalEvent(agent, lift), 0)
>       sim.run()

tests/test_agent.py:40: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
zero_liftsim/main.py:110: in run
    new_events = event.execute(self)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <zero_liftsim.main.ReturnEvent object at 0x7f2c71d600d0>
simulation = <zero_liftsim.main.Simulation object at 0x7f2c71d9d810>

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Mark the lift idle and trigger new boarding if needed."""
        for agent in self.boarded:
            agent.finish_ride(simulation.current_time)
        self.lift.mark_idle()
>       for agent in riders:
E       NameError: name 'riders' is not defined

zero_liftsim/main.py:508: NameError
__________________________ test_run_alpha_sim_metrics __________________________

    def test_run_alpha_sim_metrics():
>       result = run_alpha_sim(n_agents=3, lift_capacity=2, cycle_time=5)

tests/test_alpha_sim.py:12: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
zero_liftsim/main.py:536: in run_alpha_sim
    sim.run(logger=logger)
zero_liftsim/main.py:110: in run
    new_events = event.execute(self)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <zero_liftsim.main.ReturnEvent object at 0x7f2c71d8f450>
simulation = <zero_liftsim.main.Simulation object at 0x7f2c71d8ee90>

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Mark the lift idle and trigger new boarding if needed."""
        for agent in self.boarded:
            agent.finish_ride(simulation.current_time)
        self.lift.mark_idle()
>       for agent in riders:
E       NameError: name 'riders' is not defined

zero_liftsim/main.py:508: NameError
_________________________ test_logging_records_events __________________________

    def test_logging_records_events():
        logger = Logger()
        sim = Simulation()
        lift = Lift(capacity=1, cycle_time=5)
        agent = Agent(1)
        sim.schedule(ArrivalEvent(agent, lift), 0)
>       sim.run(logger=logger)

tests/test_alpha_sim.py:23: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
zero_liftsim/main.py:110: in run
    new_events = event.execute(self)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <zero_liftsim.main.ReturnEvent object at 0x7f2c71f27290>
simulation = <zero_liftsim.main.Simulation object at 0x7f2c71f47d50>

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Mark the lift idle and trigger new boarding if needed."""
        for agent in self.boarded:
            agent.finish_ride(simulation.current_time)
        self.lift.mark_idle()
>       for agent in riders:
E       NameError: name 'riders' is not defined

zero_liftsim/main.py:508: NameError
___________________________ test_logger_writes_file ____________________________

tmp_path = PosixPath('/tmp/pytest-of-zero/pytest-22/test_logger_writes_file0')

    def test_logger_writes_file(tmp_path):
        log_name = "test.log"
        logger = Logger(log_name)
        sim = Simulation()
        lift = Lift(capacity=1, cycle_time=5)
        agent = Agent(1)
        sim.schedule(ArrivalEvent(agent, lift), 0)
>       sim.run(logger=logger)

tests/test_alpha_sim.py:37: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
zero_liftsim/main.py:110: in run
    new_events = event.execute(self)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <zero_liftsim.main.ReturnEvent object at 0x7f2c71c5bd90>
simulation = <zero_liftsim.main.Simulation object at 0x7f2c71c50b90>

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Mark the lift idle and trigger new boarding if needed."""
        for agent in self.boarded:
            agent.finish_ride(simulation.current_time)
        self.lift.mark_idle()
>       for agent in riders:
E       NameError: name 'riders' is not defined

zero_liftsim/main.py:508: NameError
___________________________ test_single_agent_cycle ____________________________

    def test_single_agent_cycle():
        log = []
        sim = Simulation()
        lift = Lift(capacity=1, cycle_time=5)
        agent = Agent(1)
    
        class LogArrivalEvent(ArrivalEvent):
            def execute(self, s):
                events = super().execute(s)
                log.append(("arrival", lift.state))
                return [(LogBoardingEvent(e.lift), t) for e, t in events]
    
        class LogBoardingEvent(BoardingEvent):
            def execute(self, s):
                events = super().execute(s)
                log.append(("boarding", lift.state))
                return [(LogReturnEvent(e.lift), t) for e, t in events]
    
        class LogReturnEvent(ReturnEvent):
            def execute(self, s):
                events = super().execute(s)
                log.append(("return", lift.state))
                return events
    
        sim.schedule(LogArrivalEvent(agent, lift), 0)
>       sim.run()

tests/test_events.py:36: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
zero_liftsim/main.py:110: in run
    new_events = event.execute(self)
tests/test_events.py:31: in execute
    events = super().execute(s)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <test_events.test_single_agent_cycle.<locals>.LogReturnEvent object at 0x7f2c71c61fd0>
simulation = <zero_liftsim.main.Simulation object at 0x7f2c71c62110>

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Mark the lift idle and trigger new boarding if needed."""
        for agent in self.boarded:
            agent.finish_ride(simulation.current_time)
        self.lift.mark_idle()
>       for agent in riders:
E       NameError: name 'riders' is not defined

zero_liftsim/main.py:508: NameError
_________________ test_agent_log_created_and_contains_entries __________________

    def test_agent_log_created_and_contains_entries():
        sim = Simulation()
        lift = Lift(capacity=1, cycle_time=5)
        agent = Agent(1)
        sim.schedule(ArrivalEvent(agent, lift), 0)
>       sim.run(full_agent_logging=True)

tests/test_full_agent_logging.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
zero_liftsim/main.py:110: in run
    new_events = event.execute(self)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <zero_liftsim.main.ReturnEvent object at 0x7f2c71eeb3d0>
simulation = <zero_liftsim.main.Simulation object at 0x7f2c71d8cf10>

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Mark the lift idle and trigger new boarding if needed."""
        for agent in self.boarded:
            agent.finish_ride(simulation.current_time)
        self.lift.mark_idle()
>       for agent in riders:
E       NameError: name 'riders' is not defined

zero_liftsim/main.py:508: NameError
___________________ test_agent_log_not_created_when_disabled ___________________

    def test_agent_log_not_created_when_disabled():
        log_path = Path(__file__).resolve().parents[1] / "logs" / "agent.log"
        if log_path.exists():
            log_path.unlink()
    
        sim = Simulation()
        lift = Lift(capacity=1, cycle_time=5)
        agent = Agent(1)
        sim.schedule(ArrivalEvent(agent, lift), 0)
>       sim.run()

tests/test_full_agent_logging.py:36: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
zero_liftsim/main.py:110: in run
    new_events = event.execute(self)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <zero_liftsim.main.ReturnEvent object at 0x7f2c71c591d0>
simulation = <zero_liftsim.main.Simulation object at 0x7f2c71c5b950>

    def execute(self, simulation: Simulation) -> list[tuple[Event, int]]:
        """Mark the lift idle and trigger new boarding if needed."""
        for agent in self.boarded:
            agent.finish_ride(simulation.current_time)
        self.lift.mark_idle()
>       for agent in riders:
E       NameError: name 'riders' is not defined

zero_liftsim/main.py:508: NameError
=========================== short test summary info ============================
FAILED tests/test_agent.py::test_activity_log_enabled_via_events - NameError:...
FAILED tests/test_alpha_sim.py::test_run_alpha_sim_metrics - NameError: name ...
FAILED tests/test_alpha_sim.py::test_logging_records_events - NameError: name...
FAILED tests/test_alpha_sim.py::test_logger_writes_file - NameError: name 'ri...
FAILED tests/test_events.py::test_single_agent_cycle - NameError: name 'rider...
FAILED tests/test_full_agent_logging.py::test_agent_log_created_and_contains_entries
FAILED tests/test_full_agent_logging.py::test_agent_log_not_created_when_disabled
========================= 7 failed, 9 passed in 0.08s ==========================
# Git Info
Commit: f60222e2fbdac593f5970f3ba01b2c1345229cfb
Date: 2025-06-12T05:57:19-07:00
