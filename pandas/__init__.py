from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Iterable, List

class _Timestamp(datetime):
    """Minimal ``Timestamp`` using :class:`~datetime.datetime`."""

    @classmethod
    def fromisoformat(cls, date_string: str) -> "_Timestamp":
        dt = datetime.fromisoformat(date_string)
        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            dt.tzinfo,
        )


def Timestamp(value: str | datetime) -> _Timestamp:
    if isinstance(value, _Timestamp):
        return value
    if isinstance(value, datetime):
        dt = value
    else:
        dt = datetime.fromisoformat(str(value))
    return _Timestamp(
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second,
        dt.microsecond,
        dt.tzinfo,
    )

def date_range(start: str | datetime, periods: int, freq: str = "D") -> List[Timestamp]:
    if isinstance(start, str):
        start_dt = datetime.fromisoformat(start)
    else:
        start_dt = start
    step = timedelta(hours=1)
    if freq and freq.lower().startswith("h"):
        step = timedelta(hours=1)
    elif freq and freq.lower().startswith("m"):
        step = timedelta(minutes=1)
    elif freq and freq.lower().startswith("d"):
        step = timedelta(days=1)
    return [_Timestamp.fromtimestamp((start_dt + i * step).timestamp()) for i in range(periods)]

class Series(list):
    def __sub__(self, other: Timestamp):
        return Series([x - other for x in self])
    def __eq__(self, other):
        return [x == other for x in self]
    def abs(self):
        return Series([abs(x) for x in self])
    def idxmin(self) -> int:
        return self.index(min(self))

class DataFrame:
    def __init__(self, data: dict[str, Iterable[Any]]):
        self._data = {k: list(v) for k, v in data.items()}
        lengths = {len(v) for v in self._data.values()}
        if lengths:
            length = lengths.pop()
            if lengths:
                raise ValueError("Columns must have equal length")
            self.index = list(range(length))
        else:
            self.index = []

    def __iter__(self):
        return iter(self.index)

    def __len__(self) -> int:
        return len(self.index)

    @property
    def columns(self) -> List[str]:
        return list(self._data.keys())

    def __getitem__(self, key: str | List[bool]):
        if isinstance(key, str):
            return Series(self._data[key])
        if isinstance(key, list) and all(isinstance(v, bool) for v in key):
            data = {k: [val for val, flag in zip(vals, key) if flag] for k, vals in self._data.items()}
            return DataFrame(data)
        raise KeyError(key)

    def __setitem__(self, key: str, value: Iterable[Any]):
        self._data[key] = list(value)

    def copy(self, deep: bool = True):
        return DataFrame({k: list(v) for k, v in self._data.items()})

# -- pandas.api ---------------------------------------------------------------
class _Types:
    @staticmethod
    def is_datetime64_any_dtype(col: Iterable[Any]) -> bool:
        return all(isinstance(x, datetime) or isinstance(x, Timestamp) for x in col)

class _Extensions:
    @staticmethod
    def register_dataframe_accessor(name: str):
        def decorator(cls):
            def accessor(self):
                return cls(self)
            setattr(DataFrame, name, property(accessor))
            return cls
        return decorator

class _API:
    def __init__(self):
        self.types = _Types()
        self.extensions = _Extensions()

import sys
import types

api = _API()
sys.modules[__name__ + ".api"] = types.ModuleType("api")
sys.modules[__name__ + ".api"].types = api.types
sys.modules[__name__ + ".api"].extensions = api.extensions
sys.modules[__name__ + ".api.types"] = api.types
sys.modules[__name__ + ".api.extensions"] = api.extensions

__all__ = [
    "DataFrame",
    "Series",
    "Timestamp",
    "date_range",
    "api",
]

