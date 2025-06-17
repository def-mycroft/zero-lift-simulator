"""Command line interface for zero-liftsim."""

from __future__ import annotations

import argparse
from pathlib import Path
from datetime import datetime

from zero_liftsim import main as zls, __version__
from zero_liftsim.helpers import docstring_prompt


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
        "--start-datetime",
        metavar="ISO",
        help="Start datetime for dev simulation runs.",
    )
    dev.add_argument(
        "--analyze-docs",
        action="store_true",
        help="Append git info to all markdown docs.",
    )
    dev.add_argument(
        "--new-doc",
        action="store_true",
        help="Create a blank documentation stub in docs/.",
    )
    dev.add_argument(
        "--build-docs",
        action="store_true",
        help="Build Sphinx documentation.",
    )
    dev.add_argument(
        "--docstring-prompt", "-dp",
        action="store_true",
        help="prompt for updating docstring. ",
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
        from . import docs_tools
        docs_tools.update_toc()
    if getattr(args, "command", None) == "dev" and args.docstring_prompt:
        # get docs prompt
        docstring_prompt()
    if getattr(args, "command", None) == "dev" and args.exec_hook:
        from git import Repo
        print('loaded git.Repo')
        ########################################################################
        # I'm just putting code here when I'm testing things. codex: don't edit
        # unless it needs to be updated due to a functionality change. 
        #import pandas as pd
        #from zero_liftsim.main import run_alpha_sim

        #start = (
        #    datetime.fromisoformat(args.start_datetime)
        #    if args.start_datetime
        #    else datetime(2025, 3, 12, 9, 0, 0)
        #)
        #data = run_alpha_sim(
        #    n_agents=3,
        #    lift_capacity=2,
        #    cycle_time=5,
        #    start_datetime=start,
        #)
        #agents = data['agents']
        #a = agents[0]
        #print(a.activity_log)
        ########################################################################
    if getattr(args, "command", None) == "dev" and args.analyze_docs:
        from . import docs_tools
        docs_tools.analyze_docs()
    if getattr(args, "command", None) == "dev" and args.new_doc:
        from . import docs_tools
        docs_tools.new_doc()
        docs_tools.update_toc()
    if getattr(args, "command", None) == "dev" and args.build_docs:
        from . import docs_tools
        docs_tools.build_docs()


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
