import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib.figure import Figure
from typing import Any, Mapping


def visualize_states(agent_exp_log_data: Any, time: datetime, out_path: str | None = "state_diagram.png") -> Figure:
    """Return a state diagram for all agents at ``time``.

    Parameters
    ----------
    agent_exp_log_data:
        A DataFrame representing the agent log or an object containing an
        ``agent_log`` attribute or key.
    time:
        Moment in time to visualize.
    out_path:
        Optional path where the diagram should be saved. If ``None`` the figure
        is not written to disk.

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.
    """
    # Determine the dataframe containing the agent log
    if isinstance(agent_exp_log_data, pd.DataFrame):
        df = agent_exp_log_data
    elif isinstance(agent_exp_log_data, Mapping) and "agent_log" in agent_exp_log_data:
        df = agent_exp_log_data["agent_log"]
    elif hasattr(agent_exp_log_data, "agent_log"):
        df = getattr(agent_exp_log_data, "agent_log")
    else:
        raise TypeError(
            "agent_exp_log_data must be a DataFrame or contain an 'agent_log' field"
        )

    df = df.copy()
    if "time" not in df.columns or "agent_id" not in df.columns or "event" not in df.columns:
        raise ValueError("agent_log DataFrame must contain 'time', 'agent_id', and 'event' columns")

    # ensure time column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df["time"]):
        df["time"] = pd.to_datetime(df["time"])

    df.sort_values("time", inplace=True)

    # Define positions for each possible state
    state_positions = {
        "start_wait": (0, 0),
        "board": (1, 1),
        "ride": (2, 0),
        "exit": (3, 1),
        "return": (4, 0),
    }

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 2)
    ax.axis("off")

    for state, (x, y) in state_positions.items():
        ax.add_patch(plt.Circle((x, y), 0.2, color="gray", zorder=1))
        ax.text(x, y + 0.3, state, ha="center", fontsize=10)

    # Get the latest event for each agent before or at the provided time
    latest = df[df["time"] <= time].groupby("agent_id").tail(1)

    for _, row in latest.iterrows():
        state = row["event"]
        agent_id = row["agent_id"]
        if state in state_positions:
            x, y = state_positions[state]
            ax.add_patch(plt.Rectangle((x - 0.05, y - 0.05), 0.1, 0.1, color="blue", zorder=2))
            ax.text(x, y, str(agent_id), ha="center", va="center", color="white", fontsize=6, zorder=3)

    if out_path is not None:
        fig.savefig(out_path, dpi=150)
    return fig
