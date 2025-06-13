"""Visualization utilities for agent state snapshots."""

from __future__ import annotations

from datetime import datetime
from typing import Mapping

import matplotlib.pyplot as plt
import pandas as pd


def visualize_states(
    agent_exp_log_data: pd.DataFrame | Mapping[str, pd.DataFrame],
    time: datetime,
    out_path: str = "state_diagram.png",
) -> None:
    """Render a simple state diagram showing agent positions.

    Parameters
    ----------
    agent_exp_log_data : pandas.DataFrame or Mapping[str, pandas.DataFrame]
        Data containing an ``"agent_log"`` table. If a mapping is supplied it
        must provide this key. The table must include ``"event"``,
        ``"agent_uuid`` and ``"time`` columns. Older logs may instead use a
        ``"description"`` column in place of ``"event``, which will be handled
        automatically.
    time : datetime
        Point in time to visualize.
    out_path : str, optional
        File path where the PNG diagram will be written.
    """

    if isinstance(agent_exp_log_data, pd.DataFrame):
        df = agent_exp_log_data
    else:
        try:
            df = agent_exp_log_data["agent_log"]
        except Exception as exc:  # pragma: no cover - type/KeyError
            raise ValueError(
                "agent_exp_log_data must be a DataFrame or mapping containing 'agent_log'"
            ) from exc

    required_cols = {"event", "agent_uuid", "time"}
    missing = required_cols - set(df.columns)
    if missing:
        # Some older logs used 'description' instead of 'event'. Handle that
        # transparently so visualization still works.
        if "event" not in df.columns and "description" in df.columns:
            df = df.rename(columns={"description": "event"})
            missing = required_cols - set(df.columns)

    if missing:
        raise ValueError(
            "agent_log missing columns: "
            + ", ".join(sorted(missing))
            + ". Did you pass SimulationManager.retrieve_data()['agent_log']?"
        )

    df = df.sort_values("time")
    latest = df[df["time"] <= time].groupby("agent_uuid").tail(1)

    state_positions = {
        "start_wait": (0, 0),
        "arrival": (1, 0.5),
        "board": (2, 0),
        "ride_complete": (3, 0.5),
    }

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 1.5)
    ax.axis("off")

    for state, (x, y) in state_positions.items():
        ax.add_patch(plt.Circle((x, y), 0.15, color="gray", zorder=1))
        ax.text(x, y + 0.25, state, ha="center", fontsize=9)

    for _, row in latest.iterrows():
        event = row["event"]
        agent_uuid = row["agent_uuid"]
        if event in state_positions:
            x, y = state_positions[event]
            ax.add_patch(
                plt.Rectangle((x - 0.05, y - 0.05), 0.1, 0.1, color="blue", zorder=2)
            )
            ax.text(
                x,
                y,
                str(agent_uuid)[:4],
                ha="center",
                va="center",
                color="white",
                fontsize=6,
                zorder=3,
            )

    fig.savefig(out_path, dpi=150)
    plt.close(fig)
