
try:
    from codenamize import codenamize as cd
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without the package
    def cd(value: str) -> str:
        """Simplistic fallback that returns the first eight characters."""
        return value[:8]

try:
    from zero_helpers.imports import *  # type: ignore
    from zero_helpers.main import string_to_clipboard
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    from os.path import join, exists, expanduser

    def string_to_clipboard(text: str) -> None:
        """Fallback no-op if ``zero_helpers`` is unavailable."""
        return None

from uuid import uuid4 as uuid
from pathlib import Path
import pandas as pd
import inspect

from typing import Any, Callable, Dict

try:
    from jinja2 import Environment, FileSystemLoader
except ModuleNotFoundError:  # pragma: no cover - fallback if jinja2 missing
    Environment = None
    FileSystemLoader = None


def docstring_prompt():
    """Load project docstring spec and write out prompt"""
    # TODO - this is hard coded and should be loaded locally
    # just a dev func though 
    fp_docs = join(expanduser('~'),  ('code-repos/zero-lift-simulator/docs/'
                                      'main_notes_docstring_style_guide.md'))
    assert exists(fp_docs)
    with open(fp_docs, 'r') as f:
        docs_text = f.read()
    text = (f"here is a styleguide for docstrings in this project: \n***\n"
            f"\n{docs_text}\n\n***\nnow use this to write a new docstring "
            f"\n for this: \n```python\nxxx\n```\n\nreturn the docstring without"
            f"\n comment so that I can easily paste it into source. ")
    print(text)
    fp = '/l/tmp/prompt.md'
    with open(fp, 'w') as f:
        f.write(text)
    print(f"wrote '{fp}'")


def codename():
    """Generate random codename"""
    i = str(uuid())
    return {'uuid':i, 'name':cd(i)}


def seed_from_uuid(value: str) -> int:
    """Return a deterministic integer seed derived from ``value``.

    Parameters
    ----------
    value:
        UUID string used to derive the seed.

    Returns
    -------
    int
        Integer representation of the UUID truncated to 32 bits.
    """
    from uuid import UUID

    try:
        uid = UUID(value)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise ValueError("invalid uuid string") from exc

    return uid.int & 0xFFFFFFFF


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
            "__init__": {
                "n_agents": 1,
                "lift_capacity": 1,
                "start_datetime": None,
                "logger": None,
            },
            "run": _defaults_from_callable(SimulationManager.run),
        },
        "Simulation": {
            "__init__": _defaults_from_callable(Simulation.__init__),
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

    # setup dtypes for serialization 
    cfg['Simulation']['run']['start_datetime'] = pd.to_datetime(cfg['Simulation']['run']['start_datetime']).isoformat()
    return cfg


def update_params(**kwargs: Any) -> Dict[str, Any]:
    """Return the default config updated with ``kwargs`` (recursive)."""
    return base_config(**kwargs)

