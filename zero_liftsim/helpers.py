
try:
    from codenamize import codenamize as cd
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without the package
    def cd(value: str) -> str:
        """Simplistic fallback that returns the first eight characters."""
        return value[:8]
from uuid import uuid4 as uuid
from pathlib import Path
import inspect

from typing import Any, Callable, Dict

try:
    from jinja2 import Environment, FileSystemLoader
except ModuleNotFoundError:  # pragma: no cover - fallback if jinja2 missing
    Environment = None
    FileSystemLoader = None


def codename():
    """Generate random codename"""
    i = str(uuid())
    return {'uuid':i, 'name':cd(i)}


def load_asset_template(name: str):
    """Load a jinja2 template bundled in ``assets``.

    Parameters
    ----------
    name:
        File name of the template to load.
    """

    assets = Path(__file__).resolve().parent / "assets"
    if Environment is None:
        # jinja2 missing, fall back to plain text
        path = assets / name
        return path.read_text(encoding="utf-8")

    env = Environment(loader=FileSystemLoader(str(assets)))
    template = env.get_template(name)
    return template


def _defaults_from_callable(obj: Callable[..., Any]) -> Dict[str, Any]:
    """Return a dictionary of parameter defaults for ``obj``."""
    sig = inspect.signature(obj)
    defaults: Dict[str, Any] = {}
    for name, param in sig.parameters.items():
        if param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY):
            if param.default is not inspect.Parameter.empty:
                defaults[name] = param.default
    return defaults


def _deep_update(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively update ``base`` with ``updates`` and return ``base``."""
    for key, value in updates.items():
        if (
            isinstance(value, dict)
            and isinstance(base.get(key), dict)
        ):
            _deep_update(base[key], value)
        else:
            base[key] = value
    return base


def base_config(**overrides: Any) -> Dict[str, Any]:
    """Return the base simulation configuration with optional overrides."""
    from . import git_tools
    from .simmanager import SimulationManager
    from .simulation import Simulation
    from .lift import Lift
    from .agent import Agent

    cfg: Dict[str, Any] = {
        "git_commit": git_tools.HEAD_COMMIT,
        "SimulationManager": {
            "__init__": _defaults_from_callable(SimulationManager.__init__),
            "run": _defaults_from_callable(SimulationManager.run),
        },
        "Simulation": {
            "run": _defaults_from_callable(Simulation.run),
        },
        "Lift": _defaults_from_callable(Lift.__init__),
        "Agent": {
            "__init__": _defaults_from_callable(Agent.__init__),
        },
    }

    # include common runtime attributes for lift that are not part of __init__
    if all(
        hasattr(Lift, attr)
        for attr in ("ride_mean", "ride_sd", "traverse_mean", "traverse_sd")
    ):
        lift_attrs = {
            "ride_mean": Lift.ride_mean,
            "ride_sd": Lift.ride_sd,
            "traverse_mean": Lift.traverse_mean,
            "traverse_sd": Lift.traverse_sd,
        }
    else:
        default_lift = Lift(capacity=1)
        lift_attrs = {
            "ride_mean": default_lift.ride_mean,
            "ride_sd": default_lift.ride_sd,
            "traverse_mean": default_lift.traverse_mean,
            "traverse_sd": default_lift.traverse_sd,
        }
    cfg["Lift"].update(lift_attrs)

    if overrides:
        _deep_update(cfg, overrides)
    return cfg


def update_params(**kwargs: Any) -> Dict[str, Any]:
    """Return the default config updated with ``kwargs`` (recursive)."""
    return base_config(**kwargs)

