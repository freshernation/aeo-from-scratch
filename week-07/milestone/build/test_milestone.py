import json

import pytest
from aeolab import HERE, PROMPTS, WEB2, web2

FILES = ("metrics.py", "sampling.py", "stats.py", "adapters.py", "budget.py", "store.py")


def mod(load):
    for f in FILES:
        load(f)
    return load("monitor.py")


def config(tmp_path, **kw):
    c = {"domain": "tidewell.example", "prompts": [str(PROMPTS)], "engines": ["panel", "engine_b"], "samples": 10,
         "temperature": 0.3, "budget_usd": 0, "store": str(tmp_path / "runs.db"), "prices": str(HERE / "data" / "prices.json")}
    c.update(kw)
    return c


def broken(tmp_path):
    site = tmp_path / "bad" / "tidewell.example"
    site.mkdir(parents=True)
    robots = (WEB2 / "tidewell.example" / "robots.txt").read_text()
    (site / "robots.txt").write_text(robots.replace("Disallow: /account\n", "Disallow: /account\nDisallow: /learn/\nDisallow: /filters/\n"))
    return web2(tmp_path / "bad")


def test_config_checked(load, tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"domain": "x"}))
    with pytest.raises(ValueError, match="prompts"):
        mod(load).load_config(p)


def test_budget_guards(load, tmp_path):
    m = mod(load)
    with pytest.raises(ValueError, match="no price"):
        m.run_once(config(tmp_path, engines=["perplexity"]), "2026-10-05")
    with pytest.raises(ValueError, match="over"):
        m.run_once(config(tmp_path, engines=["claude"], budget_usd=5), "2026-10-05")


def test_a_regression_raises_an_alert(load, tmp_path):
    m = mod(load)
    c = config(tmp_path)
    first = m.run_once(c, "2026-10-05")
    assert first["engines"]["panel"]["last"] is None and first["cost"] == 0.0
    second = m.run_once(c, "2026-10-12", broken(tmp_path))
    text = m.report(second, "tidewell.example")
    assert "| panel | 56.3% | 86.3% -> 56.3% (4 up, 18 down, p = 0.004) | drop |" in text
    assert "- engine_b: citation rate dropped beyond noise. Check access first." in text


def test_live_engine_through_a_fake(load, tmp_path):
    m = mod(load)
    fixtures = json.loads((HERE / "data" / "live" / "claude.json").read_text())
    by_text = {p: fixtures[i] for i, p in [(r["id"], r["prompt"]) for r in __import__("aeolab").load_prompts()]}
    rows = m.live_rows("claude", __import__("aeolab").load_prompts()[:3], 2, "claude-x", lambda e, q: by_text[q])
    assert len(rows) == 6 and rows[0]["run_id"] == "claude-x" and rows[0]["cited_urls"]
