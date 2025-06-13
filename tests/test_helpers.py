import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zero_liftsim.helpers import load_asset_template, base_config, update_params


def test_load_asset_template_returns_template():
    tmpl = load_asset_template("new_doc_template.md.j2")
    if hasattr(tmpl, "render"):
        text = tmpl.render(codename="example")
    else:
        text = tmpl.replace("{{ codename }}", "example")
    assert "example" in text


def test_base_config_contains_commit():
    cfg = base_config()
    assert "git_commit" in cfg
    assert len(cfg["git_commit"]) >= 7


def test_update_params_overrides_nested_values():
    cfg = update_params(Lift={"ride_sd": 2})
    assert cfg["Lift"]["ride_sd"] == 2
