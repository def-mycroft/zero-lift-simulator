import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


def visualize_states(agent_exp_log_data, time: datetime, out_path="state_diagram.png") -> None:
    """Visualize agent states as blocks on a state machine diagram.

    Parameters
    ----------
    agent_exp_log_data:
        Either a dictionary containing a DataFrame under the ``"agent_log"`` key
        or a DataFrame itself.
    time:
        Point in time to visualize.
    out_path:
        File path for the output PNG.
    """
    # Fixed layout for states
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
    ax.axis('off')

    # Draw state nodes
    for state, (x, y) in state_positions.items():
        ax.add_patch(plt.Circle((x, y), 0.2, color='gray', zorder=1))
        ax.text(x, y + 0.3, state, ha='center', fontsize=10)

    if isinstance(agent_exp_log_data, pd.DataFrame):
        df = agent_exp_log_data
    else:
        try:
            df = agent_exp_log_data["agent_log"]
        except (TypeError, KeyError) as exc:
            raise ValueError(
                "agent_exp_log_data must be a DataFrame or a dict containing 'agent_log'"
            ) from exc

    df = df.sort_values("time")  # Ensure time ordering

    # Latest event per agent before or at the given time
    latest_states = (
        df[df["time"] <= time]
        .groupby("agent_id")
        .tail(1)
    )

    # Draw agent boxes
    for _, row in latest_states.iterrows():
        event = row["event"]
        agent_id = row["agent_id"]
        if event in state_positions:
            x, y = state_positions[event]
            ax.add_patch(plt.Rectangle((x - 0.05, y - 0.05), 0.1, 0.1, color='blue', zorder=2))
            ax.text(x, y, str(agent_id), ha='center', va='center', color='white', fontsize=6, zorder=3)

    plt.savefig(out_path, dpi=150)
    plt.close()

"ready to use – just feed it `agent_exp_log_data` and a datetime to generate frame PNGs."

