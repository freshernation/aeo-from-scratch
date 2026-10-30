from aeolab.fakeweb import FakeWeb

T = "https://tidewell.example"


def check(load, path, bot="PanelBot"):
    load("robots.py")
    return load("fetchcheck.py").check(FakeWeb(), T + path, bot)


class TestReasons:
    def test_readable(self, load):
        c = check(load, "/faq")
        assert c["readable"] and c["reason"] == "" and c["status"] == 200
        assert set(c) == {"url", "status", "final_url", "hops", "noindex", "js_shell", "canonical", "readable", "reason"}

    def test_robots_first(self, load):
        c = check(load, "/learn/lead-in-water")
        assert c["reason"] == "robots" and c["status"] is None, "a blocked page is never fetched"

    def test_server_block(self, load):
        assert check(load, "/faq", "Claude-SearchBot/1.0")["reason"] == "status-403"

    def test_404(self, load):
        assert check(load, "/filters/shower-v1")["reason"] == "status-404"

    def test_noindex_header(self, load):
        c = check(load, "/warranty")
        assert c["noindex"] == "header" and c["reason"] == "noindex-header"

    def test_noindex_meta(self, load):
        assert check(load, "/filters/under-sink")["reason"] == "noindex-meta"

    def test_js_shell(self, load):
        c = check(load, "/compare")
        assert c["js_shell"] and c["reason"] == "js-only"

    def test_canonical(self, load):
        c = check(load, "/filters/pitcher-blue")
        assert c["canonical"] == T + "/filters/pitcher" and c["reason"] == "canonical-elsewhere"


class TestRedirects:
    def test_chain(self, load):
        c = check(load, "/blog/pfas-2023")
        assert c["readable"] and c["final_url"] == T + "/learn/guides/pfas"
        assert c["hops"] == [T + "/blog/pfas-2023", T + "/blog/pfas"]

    def test_loop(self, load, tmp_path):
        (tmp_path / "tidewell.example").mkdir()
        (tmp_path / "tidewell.example" / "_server.json").write_text('{"redirects": {"/a": "/b", "/b": "/a"}}')
        load("robots.py")
        c = load("fetchcheck.py").check(FakeWeb(overlay=tmp_path), T + "/a", "PanelBot")
        assert c["reason"] == "redirect-loop"

    def test_robots_checked_on_the_target(self, load, tmp_path):
        (tmp_path / "tidewell.example").mkdir()
        (tmp_path / "tidewell.example" / "_server.json").write_text('{"redirects": {"/go": "/learn/hard-water"}}')
        load("robots.py")
        assert load("fetchcheck.py").check(FakeWeb(overlay=tmp_path), T + "/go", "PanelBot")["reason"] == "robots"


def test_finding_seven_unreadable(load):
    load("robots.py")
    fc = load("fetchcheck.py")
    web = FakeWeb()
    bad = {u.rsplit(".example", 1)[1]: fc.check(web, u, "PanelBot")["reason"]
           for u in web.page_urls("tidewell.example") if not fc.check(web, u, "PanelBot")["readable"]}
    assert bad == {"/compare": "js-only", "/filters/pitcher-blue": "canonical-elsewhere",
                   "/filters/under-sink": "noindex-meta", "/learn/filter-lifespan": "robots",
                   "/learn/hard-water": "robots", "/learn/lead-in-water": "robots",
                   "/warranty": "noindex-header"}, \
        "7 of 19 pages: 3 robots, 2 noindex, 1 JavaScript, 1 duplicate (the only one that is fine)"
