from __future__ import annotations

"""Developer utilities for zero-liftsim."""

from pathlib import Path


def _title_from_filename(name: str) -> str:
    base = Path(name).stem
    base = base.replace("_", " ").replace("-", " ")
    return base.title()


def generate_docs_toc() -> str:
    """Generate a Markdown table of contents for files in ``docs``."""
    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    lines = []
    for path in sorted(docs_dir.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        title = _title_from_filename(path.name)
        lines.append(f"- [{title}]({path.name})")
    return "\n".join(lines)


def update_toc() -> None:
    """Append an auto-generated TOC to ``docs/README.md``."""
    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    readme = docs_dir / "README.md"
    toc = generate_docs_toc()
    with readme.open("a", encoding="utf-8") as fh:
        fh.write("\n## Table of Contents\n\n")
        fh.write(toc)
        fh.write("\n")

