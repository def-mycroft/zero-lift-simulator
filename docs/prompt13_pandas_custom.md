# prompt13 - Integrate .zero pandas custom accessor

amused-medium 8ca7de1e

***


You are working inside the `zero_liftsim` package. Implement a **custom pandas DataFrame accessor** named `zero` that exposes a method `get_nearest_time_index()`.

This should be done by creating a new module `pandas_ext.py` inside `zero_liftsim/`. The accessor should be registered using `@pd.api.extensions.register_dataframe_accessor("zero")`.

The exposed method `get_nearest_time_index(index_time)` must return the index of the row in the DataFrame whose datetime-like column value is closest to the given `index_time`. The accessor **must not require the user to pass the time column explicitly**. Instead, it should:

* Search for columns named `"time"`, `"timestamp"`, `"date"`, etc. (use a small ordered list of candidates, like `["time", "timestamp", "date"]`).
* Ensure only one such column exists and is datetime-like. If multiple candidates exist or if none exist, raise a clear `ValueError`.
* Use vectorized computation to efficiently find the row whose time value is closest to `index_time`.

Once implemented:

1. Import this module in `zero_liftsim/__init__.py` to ensure registration.
2. Add a simple test in `tests/test_helpers.py` or make a new test file `tests/test_pandas_ext.py`.
3. Write minimal inline docstrings consistent with the style used in the rest of the codebase (see `docstring_style_guide.md` in `docs/`).
4. Do not affect core simulation code or require pandas subclasses—this should be a clean, optional extension usable via `df.zero.get_nearest_time_index(...)`.

Final behavior should allow the following pattern:

```python
df.zero.get_nearest_time_index(index_time=pd.Timestamp("2025-01-01T12:00:00"))
```

This will be used for simulations and logs, so correctness and clarity matter more than excessive configurability. Keep it clean and idiomatic.


plan on collecting a few custom pandas df functions and maybe shifting this into a general purpose tool 
