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
    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point for the CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    zls.run(args)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
