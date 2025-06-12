"""Command line interface for zero-liftsim."""

from __future__ import annotations

import argparse
from pathlib import Path

from zero_liftsim import main as zls, __version__


_DEF_HELP = None


def load_help() -> str:
    """Load CLI help documentation from the bundled markdown file."""
    global _DEF_HELP
    if _DEF_HELP is None:
        path = Path(__file__).with_name("cli_help.md")
        _DEF_HELP = path.read_text()
    return _DEF_HELP


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="zero-liftsim",
        description=load_help(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"zero-liftsim {__version__}",
        help="Show the version and exit.",
    )
    parser.add_argument(
        "--config",
        metavar="FILE",
        help="Path to configuration file.",
    )
    subparsers = parser.add_subparsers(dest="command", required=False)
    dev = subparsers.add_parser("dev", help="Developer utilities")
    dev.add_argument(
        "--update-toc",
        action="store_true",
        help="Update docs README with table of contents.",
    )
    dev.add_argument(
        "--exec-hook",
        action="store_true",
        help="Throwaway util for development / testing. "
    )
    dev.add_argument(
        "--analyze-docs",
        action="store_true",
        help="Append git info to all markdown docs.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point for the CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    run(args)


def run(args) -> None:
    """Handle CLI commands."""
    if getattr(args, "command", None) == "dev" and args.update_toc:
        from . import dev
        dev.update_toc()
    if getattr(args, "command", None) == "dev" and args.exec_hook:
        ########################################################################
        import pandas as pd
        from zero_liftsim.main import run_alpha_sim
        data = run_alpha_sim(n_agents=3, lift_capacity=2, cycle_time=5)
        agents = data['agents']
        ########################################################################
    if getattr(args, "command", None) == "dev" and args.analyze_docs:
        from . import dev
        dev.analyze_docs()


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
