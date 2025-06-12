from __future__ import annotations

"""Utilities for working with documentation."""

from pathlib import Path

from .helpers import codename

try:
    from jinja2 import Environment, FileSystemLoader
except ModuleNotFoundError:  # pragma: no cover - fallback if jinja2 missing
    Environment = None
    FileSystemLoader = None


_TEMPLATE_NAME = "new_doc_template.md.j2"


def _load_template() -> str:
    assets = Path(__file__).resolve().parent / "assets"
    if Environment is None:
        # fallback simple template
        path = assets / _TEMPLATE_NAME
        return path.read_text(encoding="utf-8")
    env = Environment(loader=FileSystemLoader(str(assets)))
    template = env.get_template(_TEMPLATE_NAME)
    return template


def new_doc(*, docs_dir: Path | None = None) -> Path:
    """Create a new documentation stub and return the path.

    Parameters
    ----------
    docs_dir:
        Optional target directory. Defaults to ``docs`` in the project root.
    """
    docs_dir = docs_dir or Path(__file__).resolve().parent.parent / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    info = codename()
    code_str = f"{info['name']} {info['uuid'][:8]}"
    slug = f"unnamed-{info['name']}-{info['uuid'][:8]}".replace(" ", "-")

    tmpl = _load_template()
    if hasattr(tmpl, "render"):
        content = tmpl.render(codename=code_str)
    else:
        # simple string replacement fallback
        content = tmpl.replace("{{ codename }}", code_str)

    path = docs_dir / f"{slug}.md"
    path.write_text(content, encoding="utf-8")
    return path
