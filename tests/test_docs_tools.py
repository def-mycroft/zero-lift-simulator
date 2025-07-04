import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.docs_tools import (
    new_doc,
    generate_docs_toc,
    generate_prompts_index,
)
from zero_liftsim.cli import build_parser


def test_cli_parses_new_doc():
    parser = build_parser()
    args = parser.parse_args(["dev", "--new-doc"])
    assert args.new_doc


def test_cli_parses_build_docs():
    parser = build_parser()
    args = parser.parse_args(["dev", "--build-docs"])
    assert args.build_docs


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


def test_generate_prompts_index(tmp_path):
    docs = tmp_path / "docs"
    target = tmp_path / "src" / "prompts"
    docs.mkdir(parents=True)
    (docs / "prompt1_a.md").write_text("#prompt\n", encoding="utf-8")
    (docs / "prompt2_b.md").write_text("#prompt\n", encoding="utf-8")
    generate_prompts_index(docs_dir=docs, target_dir=target)
    assert (target / "prompt2_b.md").exists()
    index_text = (target / "index.rst").read_text()
    order = [line.strip() for line in index_text.splitlines() if line.startswith("   ")]
    assert order == ["prompt2_b.md", "prompt1_a.md"]

