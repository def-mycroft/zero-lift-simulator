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
        "start_wait": (0, 0),
        "board": (1, 1),
        "ride": (2, 0),
        "exit": (3, 1),
        "return": (4, 0),
    }

    agent_log: pd.DataFrame = agent_exp_log_data.get("agent_log", pd.DataFrame())
    if agent_log.empty:
        return
    agent_log = agent_log[agent_log["time"] <= time]
    if agent_log.empty:
        return
    agent_log = agent_log.sort_values("time").groupby("agent_id").tail(1)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis("off")

    for name, (x, y) in state_positions.items():
        circle = plt.Circle((x, y), 0.2, facecolor="lightgray", edgecolor="black")
        ax.add_patch(circle)
        ax.text(x, y + 0.3, name, ha="center", va="bottom", fontsize=8)

    for _, row in agent_log.iterrows():
        event = row.get("event")
        if event not in state_positions:
            continue
        x, y = state_positions[event]
        rect = plt.Rectangle(
            (x - 0.15, y - 0.15),
            0.3,
            0.3,
            facecolor="white",
            edgecolor="black",
        )
        ax.add_patch(rect)
        ax.text(x, y, str(row.get("agent_id")), ha="center", va="center", fontsize=6)

    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 1.5)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    return fig
