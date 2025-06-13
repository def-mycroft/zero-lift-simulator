import sys
from pathlib import Path
from datetime import datetime
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

pd = pytest.importorskip("pandas")
plt = pytest.importorskip("matplotlib.pyplot")

from zero_liftsim.visualize import visualize_states


def test_visualize_states_returns_figure(tmp_path):
    df = pd.DataFrame({
        "time": pd.to_datetime([
            "2025-03-12 09:00:00",
            "2025-03-12 09:05:00",
            "2025-03-12 09:02:00",
        ]),
        "agent_id": [1, 1, 2],
        "event": ["start_wait", "board", "start_wait"],
    })

    fig = visualize_states({"agent_log": df}, pd.to_datetime("2025-03-12 09:03:00"), out_path=None)
    assert hasattr(fig, "savefig")
    assert fig.axes
