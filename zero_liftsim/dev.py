from __future__ import annotations

"""Developer utilities for zero-liftsim."""

from pathlib import Path



def _title_from_file(path: Path) -> str:
    """Return the first non-empty line of ``path`` stripped of Markdown heading marks."""
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            return stripped.lstrip("#").strip()
    return ""

def _title_from_filename(name: str) -> str:
    base = Path(name).stem
    base = base.replace("_", " ").replace("-", " ")
    return base.title()


def generate_docs_toc() -> str:
    """Generate a Markdown table of contents for Markdown files in ``docs``."""
    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    main_paths: list[Path] = sorted(docs_dir.glob("main_notes*md"))
    prompt_paths: list[Path] = []
    other_paths: list[Path] = []

    for path in sorted(docs_dir.glob("*.md")):
        name = path.name.lower()
        if name in {"readme.md", "contents.md"}:
            continue
        if path in main_paths:
            continue
        if path.stem.lower().startswith("prompt"):
            prompt_paths.append(path)
        else:
            other_paths.append(path)

    lines = []
    lines.append("## Main Notes")
    if main_paths:
        for path in main_paths:
            title = _title_from_file(path)
            lines.append(f"- [{title}]({path.name})")
        lines.append("")
    else:
        lines.append("- Place files named `main_notes*.md` in the docs folder to include them here.")
        lines.append("")
    if prompt_paths:
        lines.append("## Prompt Articles")
        for path in prompt_paths:
            title = _title_from_file(path)
            lines.append(f"- [{title}]({path.name})")
        lines.append("")

    lines.append("## Articles")
    for path in other_paths:
        title = _title_from_file(path)
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


def analyze_docs() -> None:
    """Append git commit info to all Markdown docs."""
    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    from .git_tools import append_git_info

    for path in sorted(docs_dir.glob("*.md")):
        append_git_info(path)
