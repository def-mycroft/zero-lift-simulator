from __future__ import annotations

"""Developer utilities for zero-liftsim."""

from pathlib import Path


def _title_from_filename(name: str) -> str:
    base = Path(name).stem
    base = base.replace("_", " ").replace("-", " ")
    return base.title()


def generate_docs_toc() -> str:
    """Generate a Markdown table of contents for Markdown files in ``docs``."""
    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    prompt_paths: list[Path] = []
    other_paths: list[Path] = []

    for path in sorted(docs_dir.glob("*.md")):
        name = path.name.lower()
        if name in {"readme.md", "contents.md"}:
            continue
        if path.stem.lower().startswith("prompt"):
            prompt_paths.append(path)
        else:
            other_paths.append(path)

    lines = []
    if prompt_paths:
        lines.append("## Prompt Articles")
        for path in prompt_paths:
            title = _title_from_filename(path.name)
            lines.append(f"- [{title}]({path.name})")
        lines.append("")

    lines.append("## Articles")
    for path in other_paths:
        title = _title_from_filename(path.name)
        lines.append(f"- [{title}]({path.name})")

    return "\n".join(lines)


def update_toc() -> None:
    """Write an auto-generated TOC to ``docs/CONTENTS.md``."""
    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    contents = docs_dir / "CONTENTS.md"
    toc = generate_docs_toc()
    with contents.open("w", encoding="utf-8") as fh:
        fh.write("# Table of Contents\n\n")
        fh.write(toc)
        fh.write("\n")

