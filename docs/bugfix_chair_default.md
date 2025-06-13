# Bugfix - Lift default chairs

random codename: patient-boundary 8e12345f

***

Running the full test suite showed a failure in
`tests/test_alpha_sim.py::test_run_alpha_sim_metrics`. The test
expected the average wait time to be roughly `2.33` minutes but the
returned metric was `0.0`. Investigation revealed that the `Lift`
class defaulted to `100` chairs, allowing every agent to board
immediately. The simulation metrics test assumes a single chair so
that later agents must wait for the chair to return.

The fix resets the default `num_chairs` parameter of `Lift.__init__`
to `1`. With only one chair available, wait times accumulate and the
metric matches the test expectation.

# Git Info
Commit: ab41e4eaf0d5c30f09aac09ff2e02b13686c767a
Date: 2025-06-13T01:26:53+00:00

