import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.git_tools import last_commit_info
from zero_liftsim.cli import build_parser


def test_last_commit_info_returns_data():
    path = Path(__file__).resolve().parents[1] / "README.md"
    sha, dt = last_commit_info(path)
    assert len(sha) >= 7
    assert dt.tzinfo is not None


def test_cli_parses_analyze_docs():
    parser = build_parser()
    args = parser.parse_args(["dev", "--analyze-docs"])
    assert args.analyze_docs
