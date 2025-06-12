# Bugfix Response - Logger Filepath finish

In `tests/test_alpha_sim.py::test_logger_writes_file`, the assertion failed
because the log file retained entries from earlier runs. The `Logger` class
opened the log file in append mode, so previous contents persisted between
executions. When the test compared the on-disk records to `logger.records()`,
the file contained additional lines and the equality check failed.

The fix updates `Logger.__init__` to open the target log file in write mode.
Starting with an empty file ensures that the in-memory records match the
contents written to disk for each run.
