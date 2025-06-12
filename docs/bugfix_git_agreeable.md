
random codename: agreeable-pride a290a658


*** 

code isn't working. when I run `pip install -e .` I get this 

```

m on  main is 📦 v0.1.0 via 🐍 v3.11.8 via 🅒 zero 
❯ pip install -e . 
Obtaining file:///home/zero/code-repos/zero-lift-simulator
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... error
  error: subprocess-exited-with-error
  
  × Getting requirements to build editable did not run successfully.
  │ exit code: 1
  ╰─> [14 lines of output]
      error: Multiple top-level packages discovered in a flat-layout: ['logs', 'notebooks', 'zero_liftsim'].
      
      To avoid accidental inclusion of unwanted files or directories,
      setuptools will not proceed with this build.
      
      If you are trying to create a single distribution with multiple packages
      on purpose, you should not rely on automatic discovery.
      Instead, consider the following options:
      
      1. set up custom discovery (`find` directive with `include` or `exclude`)
      2. use a `src-layout`
      3. explicitly set `py_modules` or `packages` with a list of names
      
      To find more information, look for "package discovery" on setuptools docs.
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: subprocess-exited-with-error

× Getting requirements to build editable did not run successfully.
│ exit code: 1
╰─> See above for output.

note: This error originates from a subprocess, and is likely not a problem with pip.

m on  main is 📦 v0.1.0 via 🐍 v3.11.8 via 🅒 zero took 2s 
❯ 

```

...and output of pytest:

```

m on  main is 📦 v0.1.0 via 🐍 v3.11.8 via 🅒 zero 
❯ pytest
=========================================================== test session starts ============================================================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /home/zero/code-repos/zero-lift-simulator
collected 16 items / 1 error                                                                                                               

================================================================== ERRORS ==================================================================
_________________________________________________ ERROR collecting tests/test_git_tools.py _________________________________________________
ImportError while importing test module '/home/zero/code-repos/zero-lift-simulator/tests/test_git_tools.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_git_tools.py:6: in <module>
    from zero_liftsim.git_tools import last_commit_info
zero_liftsim/git_tools.py:10: in <module>
    from git import Repo
E   ModuleNotFoundError: No module named 'git'
========================================================= short test summary info ==========================================================
ERROR tests/test_git_tools.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
============================================================= 1 error in 0.06s =============================================================

m on  main is 📦 v0.1.0 via 🐍 v3.11.8 via 🅒 zero 
❯ 

```


apply a fix. this might be an misudnersatnding of how GitPython works? 
