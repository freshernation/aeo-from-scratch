from aeolab.fakeweb import FakeWeb

T = "https://tidewell.example"
XML = """<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc> https://a.example/ </loc></url><url><loc>https://a.example/b</loc><lastmod>2026-01-01</lastmod></url></urlset>"""


def mod(load):
    load("robots.py")
    load("fetchcheck.py")
    return load("sitemap.py")


def test_sitemap_urls(load):
    assert mod(load).sitemap_urls(XML) == ["https://a.example/", "https://a.example/b"]


def test_llms_txt(load):
    out = mod(load).llms_txt("Tidewell", "Water filters.", {
        "Products": [("Pitcher", T + "/filters/pitcher", "2.4 litres"), ("FAQ", T + "/faq", "")]})
    assert out.splitlines()[:7] == ["# Tidewell", "", "> Water filters.", "", "## Products", "",
                                    f"- [Pitcher]({T}/filters/pitcher): 2.4 litres"]
    assert f"- [FAQ]({T}/faq)" in out.splitlines()


def test_finding_the_sitemap_misleads(load):
    a = mod(load).audit_sitemap(FakeWeb(), "tidewell.example")
    assert a["listed"] == 19
    assert a["listed_broken"] == [T + "/filters/shower-v1", T + "/blog/pfas-2023"], "one 404, one redirect"
    assert len(a["listed_unreadable"]) == 6, "six listed pages the bot may not index"
    assert a["unlisted_readable"] == [T + "/learn/guides/carbon-vs-reverse-osmosis"], \
        "the one guide that answers 'carbon or RO?' is not in the sitemap"
