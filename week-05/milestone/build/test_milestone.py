import json

from aeolab import WEB2
from aeolab.fakeweb import FakeWeb


def tool(load):
    for f in ("robots.py", "fetchcheck.py", "sitemap.py", "access.py", "jsonld.py", "entities.py", "schema.py"):
        load(f)
    return load("aeo_audit.py")


def test_audit_keys(load):
    r = tool(load).audit(FakeWeb(overlay=WEB2), "tidewell.example")
    assert set(r) == {"domain", "matrix", "summary", "sitemap", "schema", "entity"}


def test_render_sections(load, capsys):
    assert tool(load).main(["tidewell.example", "--web", str(WEB2)]) == 0
    out = capsys.readouterr().out
    heads = [l for l in out.splitlines() if l.startswith("#")]
    assert heads == ["# Audit: tidewell.example", "## Search crawlers", "## Every crawler", "## Sitemap",
                     "## Structured data", "## Entity", "## Fix first"]
    assert "- 3 of 18 readable pages have markup: FAQPage, Organization, Product" in out
    assert "- /filters/pitcher: price 29.00 in markup is not on the page" in out
    assert "- names: TideWell Inc. (1), Tidewell (16), Tidewell Water Co. (2)" in out
    assert "- founded: 2016 (tidewell.example, wikiwater.example); 2015 (waterdirectory.example)" in out


def test_two_overlays_and_json(load, tmp_path, capsys):
    snap = tmp_path / "s" / "tidewell.example"
    snap.mkdir(parents=True)
    (snap / "_server.json").write_text('{"ua_block": ["OAI-SearchBot"]}')
    out = tmp_path / "a.json"
    tool(load).main(["tidewell.example", "--web", str(tmp_path / "s"), "--web", str(WEB2), "--json", str(out)])
    assert json.loads(out.read_text())["summary"]["unreadable_by_bot"]["OAI-SearchBot"] == 19, \
        "the first --web wins: a server block laid over web2"


def test_other_brand(load):
    r = tool(load).audit(FakeWeb(overlay=WEB2), "purepath.example")
    assert r["schema"]["problems"] == {"https://purepath.example/reverse-osmosis": ["invalid JSON"]}
