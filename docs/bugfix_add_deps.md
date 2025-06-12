Bugfix - Add Dependencies 

delicate-lay a0df759a

***


```

~ via 🐍 v3.11.8 via 🅒 zero
❯

~ via 🐍 v3.11.8 via 🅒 zero
❯ cdm
/home/zero/code-repos/zero-lift-simulator

m on  main [!?] is 📦 v0.1.0 via 🐍 v3.11.8 via 🅒 zero
❯ pytest
=========================================================== test session starts ============================================================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /home/zero/code-repos/zero-lift-simulator
collected 0 items / 5 errors

================================================================== ERRORS ==================================================================
___________________________________________________ ERROR collecting tests/test_agent.py ___________________________________________________
ImportError while importing test module '/home/zero/code-repos/zero-lift-simulator/tests/test_agent.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_agent.py:6: in <module>
    from zero_liftsim.main import Agent
zero_liftsim/__init__.py:6: in <module>
    from . import main
zero_liftsim/main.py:7: in <module>
    from codenamize import codenamize
E   ModuleNotFoundError: No module named 'codenamize'
_________________________________________________ ERROR collecting tests/test_alpha_sim.py _________________________________________________
ImportError while importing test module '/home/zero/code-repos/zero-lift-simulator/tests/test_alpha_sim.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_alpha_sim.py:7: in <module>
    from zero_liftsim.main import run_alpha_sim, Simulation, Lift, Agent, ArrivalEvent, BoardingEvent, ReturnEvent
zero_liftsim/__init__.py:6: in <module>
    from . import main
zero_liftsim/main.py:7: in <module>
    from codenamize import codenamize
E   ModuleNotFoundError: No module named 'codenamize'
__________________________________________________ ERROR collecting tests/test_events.py ___________________________________________________
ImportError while importing test module '/home/zero/code-repos/zero-lift-simulator/tests/test_events.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_events.py:8: in <module>
    from zero_liftsim.main import Agent, ArrivalEvent, BoardingEvent, ReturnEvent, Lift, Simulation
zero_liftsim/__init__.py:6: in <module>
    from . import main
zero_liftsim/main.py:7: in <module>
    from codenamize import codenamize
E   ModuleNotFoundError: No module named 'codenamize'
___________________________________________________ ERROR collecting tests/test_lift.py ____________________________________________________
ImportError while importing test module '/home/zero/code-repos/zero-lift-simulator/tests/test_lift.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_lift.py:8: in <module>
    from zero_liftsim.main import Agent, Lift
zero_liftsim/__init__.py:6: in <module>
    from . import main
zero_liftsim/main.py:7: in <module>
    from codenamize import codenamize
E   ModuleNotFoundError: No module named 'codenamize'
________________________________________________ ERROR collecting tests/test_simulation.py _________________________________________________
ImportError while importing test module '/home/zero/code-repos/zero-lift-simulator/tests/test_simulation.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_simulation.py:8: in <module>
    from zero_liftsim.main import Simulation, Event
zero_liftsim/__init__.py:6: in <module>
    from . import main
zero_liftsim/main.py:7: in <module>
    from codenamize import codenamize
E   ModuleNotFoundError: No module named 'codenamize'
========================================================= short test summary info ==========================================================
ERROR tests/test_agent.py
ERROR tests/test_alpha_sim.py
ERROR tests/test_events.py
ERROR tests/test_lift.py
ERROR tests/test_simulation.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 5 errors during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
============================================================ 5 errors in 0.07s =============================================================

m on  main [!?] is 📦 v0.1.0 via 🐍 v3.11.8 via 🅒 zero
❯

```

--- I would like to use codenamize and other packages that are common to use.
write a wiki article in docs/ which describe how to update deps. also fix this
codenamize dep. 
