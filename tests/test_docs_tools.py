import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.docs_tools import new_doc
from zero_liftsim.cli import build_parser
from zero_liftsim import dev


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


def test_generate_docs_toc_includes_all_prompts():
    toc = dev.generate_docs_toc()
    prompt_lines = [l for l in toc.splitlines() if l.startswith("- [prompt")]
    # ensure prompt99 appears first when sorted descending
    assert prompt_lines[0].startswith("- [prompt9")
    assert len(prompt_lines) >= 10
