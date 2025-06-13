import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim import pandas_ext  # noqa: F401


def test_get_nearest_time_index():
    df = pd.DataFrame({
        'time': pd.date_range('2025-01-01', periods=3, freq='h'),
        'value': [1, 2, 3]
    })
    idx = df.zero_liftsim.get_nearest_time_index(pd.Timestamp('2025-01-01T01:20:00'))
    assert idx == 1


def test_missing_or_multiple_time_columns():
    df_missing = pd.DataFrame({'value': [1, 2, 3]})
    with pytest.raises(ValueError):
        df_missing.zero_liftsim.get_nearest_time_index(pd.Timestamp('2025-01-01'))

    df_multi = pd.DataFrame({
        'time': pd.date_range('2025-01-01', periods=3, freq='h'),
        'timestamp': pd.date_range('2025-01-01', periods=3, freq='h'),
    })
    with pytest.raises(ValueError):
        df_multi.zero_liftsim.get_nearest_time_index(pd.Timestamp('2025-01-01'))
