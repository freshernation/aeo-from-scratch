"""The given package's own tests. They pass from day zero; if one fails, your copy of
aeolab/ has been changed - restore it with git."""

import json

from aeolab import load_pages, load_prompts, load_runs
from aeolab.fakeweb import FakeWeb
from aeolab.llm import FakeModel, first_sentence
from aeolab.panel import Panel, robots_allows, tokenize

T = "https://tidewell.example"


class TestFakeWeb:
    def test_serves_a_page(self):
        r = FakeWeb().fetch(T + "/faq")
        assert r.status == 200 and "<h1>" in r.text

    def test_missing_page_is_404(self):
        assert FakeWeb().fetch(T + "/nope").status == 404

    def test_redirect_is_not_followed(self):
        r = FakeWeb().fetch(T + "/blog/pfas-2023")
        assert r.status == 301 and r.headers["location"] == T + "/blog/pfas"

    def test_server_blocks_some_bots_whatever_robots_says(self):
        assert FakeWeb().fetch(T + "/faq", user_agent="Claude-SearchBot/1.0").status == 403
        assert FakeWeb().fetch(T + "/faq", user_agent="OAI-SearchBot/1.0").status == 200

    def test_noindex_can_arrive_as_a_header(self):
        assert FakeWeb().fetch(T + "/warranty").headers["x-robots-tag"] == "noindex"

    def test_javascript_only_content_needs_rendering(self):
        web = FakeWeb()
        assert "Side by side" not in web.fetch(T + "/compare").text.split("text/x-render")[0]
        assert '<div id="app"><article>' in web.fetch(T + "/compare", render_js=True).text

    def test_overlay_wins(self, tmp_path):
        (tmp_path / "tidewell.example").mkdir()
        (tmp_path / "tidewell.example" / "robots.txt").write_text("User-agent: *\nAllow: /\n")
        assert FakeWeb(overlay=tmp_path).fetch(T + "/robots.txt").text == "User-agent: *\nAllow: /\n"

    def test_load_pages_reads_everything(self):
        assert len(load_pages()) == 50


class TestRobots:
    ROBOTS = "User-agent: *\nDisallow: /learn/\nAllow: /learn/guides/\n\nUser-agent: GPTBot\nDisallow: /\n"

    def test_longest_match_wins(self):
        assert robots_allows(self.ROBOTS, "PanelBot", "/learn/guides/pfas")
        assert not robots_allows(self.ROBOTS, "PanelBot", "/learn/lead")

    def test_named_group_beats_star(self):
        assert not robots_allows(self.ROBOTS, "GPTBot/1.1", "/faq")

    def test_wildcards(self):
        assert not robots_allows("User-agent: *\nDisallow: /*.pdf$\n", "x", "/a/b.pdf")
        assert robots_allows("User-agent: *\nDisallow: /*.pdf$\n", "x", "/a/b.pdf?x")


class TestModel:
    def test_fan_out_starts_with_the_prompt(self):
        q = "Do water filters remove lead?"
        assert FakeModel().fan_out(q)[0] == q and len(FakeModel().fan_out(q)) == 3

    def test_unscripted_prompt_fans_out_to_itself(self):
        assert FakeModel().fan_out("hello") == ["hello"]

    def test_first_sentence(self):
        assert first_sentence("It costs $34. Cartridges cost $12.") == "It costs $34."


class TestPanel:
    def test_tokenize(self):
        assert tokenize("Which filters remove PFAS?") == ["filter", "remove", "pfa"]

    def test_deterministic_at_temperature_zero(self):
        p = Panel()
        a, b = p.ask("Do water filters remove lead?"), p.ask("Do water filters remove lead?")
        assert [c.url for c in a.citations] == [c.url for c in b.citations]

    def test_cites_four_distinct_urls_at_most_two_per_domain(self):
        a = Panel().ask("Which water filters remove PFAS?")
        urls = [c.url for c in a.citations]
        assert len(urls) == 4 == len(set(urls))
        assert max(a.cited_domains.count(d) for d in a.cited_domains) <= 2

    def test_cannot_see_the_noindex_page(self):
        assert Panel().readable(T + "/filters/under-sink") == (False, "noindex-meta")

    def test_prompts_and_runs_load(self):
        assert len(load_prompts()) == 30
        assert len(load_runs("baseline.jsonl")) == 600


class TestLaterWeb:
    def test_web2_has_the_access_fixes(self):
        from aeolab import web2
        w = web2()
        assert w.fetch(T + "/faq", user_agent="Claude-SearchBot/1.0").status == 200
        assert Panel(w).readable(T + "/filters/under-sink") == (True, "")
        assert "wikiwater.example" in w.domains()

    def test_overlays_stack_first_wins(self, tmp_path):
        from aeolab import web2
        (tmp_path / "tidewell.example").mkdir()
        (tmp_path / "tidewell.example" / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
        assert web2(tmp_path).fetch(T + "/robots.txt").text.endswith("Disallow: /\n")

    def test_cloaking_serves_crawlers_another_page(self):
        from aeolab import web2
        u = "https://purepath.example/learn/ro-myths"
        assert "100%" in web2().fetch(u, user_agent="OAI-SearchBot").text
        assert "100%" not in web2().fetch(u).text

    def test_cloak_files_are_not_pages(self):
        from aeolab import web2
        assert not any("_cloak" in u for u in web2().page_urls("purepath.example"))

    def test_more_prompts(self):
        from aeolab import PROMPTS_MORE
        assert [p["id"] for p in load_prompts(PROMPTS_MORE)] == ["P31", "P32", "P33", "P34", "P35", "P36"]


class TestEngineB:
    def test_answers_and_differs(self):
        from aeolab import web2
        from aeolab.engine_b import EngineB
        q = "Do water filters remove lead?"
        b = EngineB(web2()).ask(q)
        assert len(b.citations) == 4 and b.trace["queries"] == [q], "no fan-out"

    def test_runs_like_the_panel(self):
        from aeolab import web2
        from aeolab.engine_b import EngineB
        rows = EngineB(web2()).run(load_prompts()[:2], samples=2, temperature=0.3, seed=1)
        assert len(rows) == 4 and set(rows[0]) == {"run_id", "prompt_id", "sample", "cited_urls", "cited_domains", "answer"}


class TestSnapshot:
    def test_snapshot_of_a_mock_site(self, tmp_path):
        import httpx

        from aeolab.fakeweb import FakeWeb
        from aeolab.snapshot import take_snapshot

        site = {
            "/robots.txt": (200, {"content-type": "text/plain"}, "User-agent: *\nDisallow: /private/\n"),
            "/sitemap.xml": (200, {"content-type": "application/xml"},
                             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://s.example/hidden</loc></url></urlset>'),
            "/": (200, {"content-type": "text/html"}, '<a href="/a">a</a> <a href="/private/x">p</a> <a href="/old">o</a> <a href="/a?x=1">q</a>'),
            "/a": (200, {"content-type": "text/html", "x-robots-tag": "noindex"}, "<p>A</p>"),
            "/old": (301, {"location": "/a"}, ""),
            "/hidden": (200, {"content-type": "text/html"}, "<p>only in the sitemap</p>"),
            "/private/x": (200, {"content-type": "text/html"}, "<p>never fetched</p>"),
        }
        asked = []

        def handler(request):
            asked.append(request.url.path)
            status, headers, body = site.get(request.url.path, (404, {}, ""))
            return httpx.Response(status, headers=headers, text=body)

        client = httpx.Client(transport=httpx.MockTransport(handler))
        counts = take_snapshot(["https://s.example/"], tmp_path, delay=0, client=client)
        assert counts == {"s.example": 3}
        assert "/private/x" not in asked, "robots.txt is obeyed"
        server = json.loads((tmp_path / "s.example" / "_server.json").read_text())
        assert server == {"redirects": {"/old": "/a"}, "headers": {"/a": {"X-Robots-Tag": "noindex"}}}
        web = FakeWeb(root=tmp_path)
        assert web.fetch("https://s.example/hidden").status == 200
        assert web.fetch("https://s.example/old").status == 301
        assert Panel(web).readable("https://s.example/a") == (False, "noindex-header")
