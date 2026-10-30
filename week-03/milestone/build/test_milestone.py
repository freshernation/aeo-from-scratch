import json

from aeolab.fakeweb import FakeWeb


def tool(load):
    for f in ("robots.py", "fetchcheck.py", "sitemap.py", "access.py"):
        load(f)
    return load("aeo_audit.py")


def test_audit_keys(load):
    r = tool(load).audit(FakeWeb(), "tidewell.example")
    assert set(r) == {"domain", "matrix", "summary", "sitemap"} and r["summary"]["pages"] == 19


def test_render(load):
    t = tool(load)
    out = t.render(t.audit(FakeWeb(), "tidewell.example"))
    heads = [l for l in out.splitlines() if l.startswith("#")]
    assert heads == ["# Access audit: tidewell.example", "## Search crawlers", "## Every crawler",
                     "## Sitemap", "## Fix first"]
    assert "| /faq | ok | status-403 | status-403 |" in out
    assert "- Claude-SearchBot (search): 19 of 19 pages unreadable" in out
    assert "- 19 listed, 2 broken, 6 listed but unreadable, 1 readable but unlisted" in out
    assert "- /filters/under-sink: noindex-meta" in out


def test_cli_json(load, tmp_path, capsys):
    out = tmp_path / "a.json"
    assert tool(load).main(["tidewell.example", "--json", str(out)]) == 0
    data = json.loads(out.read_text())
    assert data["summary"]["unreadable_by_bot"]["PerplexityBot"] == 19
    assert capsys.readouterr().out.startswith("# Access audit: tidewell.example")


def test_cli_audits_a_fixed_copy(load, tmp_path, capsys):
    site = tmp_path / "tidewell.example"
    site.mkdir()
    (site / "_server.json").write_text("{}")
    assert tool(load).main(["tidewell.example", "--web", str(tmp_path)]) == 0
    assert "- Claude-SearchBot (search): 6 of 19 pages unreadable" in capsys.readouterr().out, \
        "an empty _server.json drops the bot block AND the warranty page's noindex header: 6 left"


def test_other_sites(load):
    t = tool(load)
    r = t.audit(FakeWeb(), "clearflow.example")
    assert r["summary"]["invisible_to_all_search"] == [], "ClearFlow hides nothing from anyone"
