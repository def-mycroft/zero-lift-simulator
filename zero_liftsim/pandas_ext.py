"""Pandas DataFrame extensions for zero_liftsim."""

from __future__ import annotations

from typing import List

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype


@pd.api.extensions.register_dataframe_accessor("zero_liftsim")
class ZeroAccessor:
    """Provide Zero Lift helper methods for :class:`pandas.DataFrame`."""

    _TIME_COLS: List[str] = ["time", "timestamp", "date"]

    def __init__(self, pandas_obj: pd.DataFrame) -> None:
        self._obj = pandas_obj

    def _find_time_column(self) -> str:
        candidates = [c for c in self._TIME_COLS if c in self._obj.columns]
        if len(candidates) != 1:
            raise ValueError(
                "DataFrame must contain exactly one time column among "
                f"{self._TIME_COLS}."
            )
        col = candidates[0]
        if not is_datetime64_any_dtype(self._obj[col]):
            raise ValueError(f"Column '{col}' is not datetime-like")
        return col

    def get_nearest_time_index(self, index_time: pd.Timestamp) -> int:
        """Return index of row whose time is closest to ``index_time``."""

        col = self._find_time_column()
        diffs = (self._obj[col] - pd.Timestamp(index_time)).abs()
        return diffs.idxmin()

    def subset_agent_uuid(self, agent_uuid):
        """Return copy dataframe subset for agent_uuid"""
        if 'agent_uuid' not in self._obj.columns:
            raise Exception('Must have agent_uuid. ')
        m = self._obj['agent_uuid'] == agent_uuid
        return self._obj[m].copy(deep=True)

