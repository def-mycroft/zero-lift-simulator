from __future__ import annotations

from datetime import datetime
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:  # pragma: no cover - fallback if matplotlib missing
    plt = None


def visualize_states(
    agent_exp_log_data: dict,
    time: datetime,
    out_path: str = "state_diagram.png",
) -> None:
    """Generate a static visualization of agent states.

    The visualization groups agents into three high level states -
    ``in_queue``, ``on_lift`` and ``down_mountain``. The latest
    logged event for each agent prior to ``time`` is mapped to one of
    these states and a count of agents is displayed at the state node.

    Parameters
    ----------
    agent_exp_log_data : dict
        Dictionary containing ``agent_log`` and ``exp_rideloop`` data frames.
    time : datetime
        Timestamp to snapshot.
    out_path : str, optional
        File path for the PNG output.
    """

    if plt is None:  # pragma: no cover - avoid failure if matplotlib is absent
        raise RuntimeError("matplotlib is required for visualize_states")

    import pandas as pd

    state_positions = {
        "in_queue": (0, 0),
        "on_lift": (1, 1),
        "down_mountain": (2, 0),
    }

    event_state_map = {
        "start_wait": "in_queue",
        "arrival": "in_queue",
        "board": "on_lift",
        "ride_complete": "down_mountain",
    }

    agent_log: pd.DataFrame = agent_exp_log_data.get("agent_log", pd.DataFrame())
    if agent_log.empty:
        return
    agent_log = agent_log[agent_log["time"] <= time]
    if agent_log.empty:
        return
    agent_log = agent_log.sort_values("time").groupby("agent_id").tail(1)

    state_counts = {name: 0 for name in state_positions}
    for _, row in agent_log.iterrows():
        state = event_state_map.get(row.get("event"))
        if state in state_counts:
            state_counts[state] += 1

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis("off")

    for name, (x, y) in state_positions.items():
        circle = plt.Circle((x, y), 0.3, facecolor="lightgray", edgecolor="black")
        ax.add_patch(circle)
        ax.text(x, y + 0.35, name, ha="center", va="bottom", fontsize=8)
        ax.text(x, y, str(state_counts[name]), ha="center", va="center", fontsize=8, weight="bold")

    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 1.5)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    return fig
