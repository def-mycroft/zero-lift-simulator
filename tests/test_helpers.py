import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.helpers import load_asset_template


def test_load_asset_template_returns_template():
    tmpl = load_asset_template("new_doc_template.md.j2")
    if hasattr(tmpl, "render"):
        text = tmpl.render(codename="example")
    else:
        text = tmpl.replace("{{ codename }}", "example")
    assert "example" in text
