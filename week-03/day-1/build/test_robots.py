import urllib.robotparser

from aeolab.fakeweb import FakeWeb

FILE = """# comment
User-agent: GPTBot
User-agent: CCBot
Disallow: /

User-agent: *
Disallow: /learn/      # drafts
Allow: /learn/guides/
Disallow: /*.pdf$
Sitemap: https://x.example/sitemap.xml
Disallow: /cart

user-agent: gptbot
allow: /public
"""


class TestParse:
    def test_groups(self, load):
        g = load("robots.py").parse(FILE)
        assert g[0] == (["gptbot", "ccbot"], [("disallow", "/")])
        assert g[1][0] == ["*"] and ("disallow", "/cart") in g[1][1], "Sitemap does not end a group"
        assert g[2] == (["gptbot"], [("allow", "/public")])

    def test_rules_before_any_agent_are_ignored(self, load):
        assert load("robots.py").parse("Disallow: /\nUser-agent: *\nAllow: /\n") == [(["*"], [("allow", "/")])]


class TestMatch:
    def test_prefix(self, load):
        m = load("robots.py").match
        assert m("/learn/", "/learn/lead") and not m("/learn/", "/lear")

    def test_wildcards(self, load):
        m = load("robots.py").match
        assert m("/*.pdf$", "/a/b.pdf") and not m("/*.pdf$", "/a.pdf?x") and m("/*.pdf", "/a.pdf?x")


class TestAllowed:
    def test_longest_wins(self, load):
        r = load("robots.py")
        assert r.allowed(FILE, "PanelBot", "/learn/guides/pfas")
        assert not r.allowed(FILE, "PanelBot", "/learn/lead")
        assert r.matched_rule(FILE, "PanelBot", "/learn/guides/pfas") == ("allow", "/learn/guides/")

    def test_named_groups_merge_and_replace_star(self, load):
        r = load("robots.py")
        assert r.allowed(FILE, "GPTBot/1.1", "/public/x"), "both gptbot groups apply, merged; the longer allow wins"
        assert not r.allowed(FILE, "GPTBot/1.1", "/faq")
        assert r.allowed(FILE, "GPTBot", "/cart") is False, "Disallow: / covers /cart"
        assert r.allowed(FILE, "OAI-SearchBot", "/faq"), "no group names it: the * group, which allows /faq"

    def test_tie_goes_to_allow(self, load):
        assert load("robots.py").allowed("User-agent: *\nDisallow: /a\nAllow: /a\n", "x", "/a")

    def test_empty_disallow_matches_nothing(self, load):
        assert load("robots.py").matched_rule("User-agent: *\nDisallow:\n", "x", "/a") is None

    def test_robots_txt_always_allowed(self, load):
        assert load("robots.py").allowed("User-agent: *\nDisallow: /\n", "x", "/robots.txt")


def test_finding_python_and_the_rfc_disagree(load):
    r = load("robots.py")
    web = FakeWeb()
    text = web.fetch("https://tidewell.example/robots.txt").text
    py = urllib.robotparser.RobotFileParser()
    py.parse(text.splitlines())
    differ = [u for u in web.page_urls("tidewell.example")
              if py.can_fetch("PanelBot", u) != r.allowed(text, "PanelBot", u.split(".example", 1)[1])]
    assert [u.rsplit("/", 1)[1] for u in differ] == ["carbon-vs-reverse-osmosis", "install-under-sink", "pfas"], \
        "Python's parser takes the first matching rule; RFC 9309 the longest. Three Tidewell guides depend on which"
