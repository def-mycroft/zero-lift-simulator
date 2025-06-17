# prompt17 sandbox module test issue enchanting-curve ff38f89e

random codename: enchanting-curve ff38f89e

#prompt 

***

I moved a function out of sandbox and into an agent method. update test 

```

m on  main [!?] is 📦 v0.1.0 via 🐍 v3.13.5 via 🅒 zero 
❯ pytest
========================================== test session starts ==========================================
platform linux -- Python 3.13.5, pytest-8.4.0, pluggy-1.6.0
rootdir: /home/zero/code-repos/zero-lift-simulator
configfile: pyproject.toml
collected 32 items / 1 error                                                                            

================================================ ERRORS =================================================
________________________________ ERROR collecting tests/test_sandbox.py _________________________________
ImportError while importing test module '/home/zero/code-repos/zero-lift-simulator/tests/test_sandbox.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../miniconda3/envs/zero/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_sandbox.py:8: in <module>
    from zero_liftsim.sandbox import (
E   ModuleNotFoundError: No module named 'zero_liftsim.sandbox'
======================================== short test summary info ========================================
ERROR tests/test_sandbox.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
=========================================== 1 error in 0.48s ============================================

m on  main [!?] is 📦 v0.1.0 via 🐍 v3.13.5 via 🅒 zero 
❯ 

```

