import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.docs_tools import new_doc
from zero_liftsim.cli import build_parser


def test_cli_parses_new_doc():
    parser = build_parser()
    args = parser.parse_args(["dev", "--new-doc"])
    assert args.new_doc


def test_new_doc_creates_file(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    path = new_doc(docs_dir=docs)
    assert path.exists()
    text = path.read_text()
    assert text.startswith("# unnamed")
    assert "random codename:" in text
