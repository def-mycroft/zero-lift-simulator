# prompt20 pytest tossup breakable-scratch 689c423e

random codename: breakable-scratch 689c423e

***


below is an error of some sort. I guessing this is something trivial. apply a fix. if it 
would happen to be a vim fold marker that is getting in the way, just remove it or remove the pair. 



```python
============================= test session starts ==============================
platform linux -- Python 3.11.8, pytest-8.4.0, pluggy-1.6.0
rootdir: /home/zero/code-repos/zero-lift-simulator
configfile: pyproject.toml
plugins: dash-2.18.2, anyio-4.6.2
collected 34 items

tests/test_agent.py FF......                                             [ 23%]
tests/test_agent_state.py ..                                             [ 29%]
tests/test_alpha_sim.py F...                                             [ 41%]
tests/test_docs_tools.py ..F                                             [ 50%]
tests/test_events.py .                                                   [ 52%]
tests/test_full_agent_logging.py ..                                      [ 58%]
tests/test_git_tools.py ..                                               [ 64%]
tests/test_helpers.py ...                                                [ 73%]
tests/test_lift.py ....                                                  [ 85%]
tests/test_pandas_ext.py ..                                              [ 91%]
tests/test_runtime.py .                                                  [ 94%]
tests/test_simulation.py ..                                              [100%]

=================================== FAILURES ===================================
__________________________ test_wait_and_finish_ride ___________________________

    def test_wait_and_finish_ride():
        agent = Agent(1)
        start = datetime(2025, 3, 12, 9, 0, 0)
        agent.enter_queue(0, start.isoformat())
        agent.boarded = True
        ts = (start + timedelta(minutes=5)).isoformat()
        wait = agent.finish_ride(5, ts)
>       assert wait == 5
E       assert 0 == 5

tests/test_agent.py:19: AssertionError
_____________________________ test_multiple_rides ______________________________

    def test_multiple_rides():
        agent = Agent(2)
        start = datetime(2025, 3, 12, 9, 0, 0)
        agent.enter_queue(0, start.isoformat())
        agent.boarded = True
        ts1 = (start + timedelta(minutes=3)).isoformat()
        wait1 = agent.finish_ride(3, ts1)
>       assert wait1 == 3
E       assert 0 == 3

tests/test_agent.py:31: AssertionError
__________________________ test_run_alpha_sim_metrics __________________________

    def test_run_alpha_sim_metrics():
        start = datetime(2025, 3, 12, 9, 0, 0)
        # ensure deterministic lift timing for this test
        orig = Lift.time_spent_ride_lift
        Lift.time_spent_ride_lift = lambda self: 5
        result = run_alpha_sim(
            n_agents=3,
            lift_capacity=2,
            start_datetime=start,
            runtime_minutes=10,
        )
        Lift.time_spent_ride_lift = orig
        assert result["total_rides"] == 3
>       assert abs(result["average_wait"] - (0 + 4 + 3) / 3) < 1e-6
E       assert 2.3333333333333335 < 1e-06
E        +  where 2.3333333333333335 = abs((0.0 - (((0 + 4) + 3) / 3)))

tests/test_alpha_sim.py:33: AssertionError
_________________ test_generate_docs_toc_includes_all_prompts __________________

    def test_generate_docs_toc_includes_all_prompts():
        toc = generate_docs_toc()
        prompt_lines = [l for l in toc.splitlines() if l.startswith("- [prompt")]
        numbers = []
        for line in prompt_lines:
            link = line.split("(")[1].split(")")[0]
            num = int(re.search(r"prompt[_-]?(\d+)", link).group(1))
            numbers.append(num)
>       assert numbers == sorted(numbers, reverse=True)
E       assert [19, 18, 17, 16, 15, 14, ...] == [20, 19, 18, 17, 16, 15, ...]
E         
E         At index 0 diff: 19 != 20
E         Use -v to get more diff

tests/test_docs_tools.py:35: AssertionError
=========================== short test summary info ============================
FAILED tests/test_agent.py::test_wait_and_finish_ride - assert 0 == 5
FAILED tests/test_agent.py::test_multiple_rides - assert 0 == 3
FAILED tests/test_alpha_sim.py::test_run_alpha_sim_metrics - assert 2.3333333...
FAILED tests/test_docs_tools.py::test_generate_docs_toc_includes_all_prompts
========================= 4 failed, 30 passed in 0.98s =========================
```


