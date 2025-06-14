import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.docs_tools import new_doc, generate_docs_toc
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


def test_generate_docs_toc_includes_all_prompts():
    toc = generate_docs_toc()
    prompt_lines = [l for l in toc.splitlines() if l.startswith("- [prompt")]
    numbers = []
    for line in prompt_lines:
        link = line.split("(")[1].split(")")[0]
        num = int(re.search(r"prompt[_-]?(\d+)", link).group(1))
        numbers.append(num)
    assert numbers == sorted(numbers, reverse=True)
    assert len(prompt_lines) >= 10
