import re
from pathlib import Path

from aeolab.fakeweb import FakeWeb
from aeolab.panel import robots_allows

HERE = Path(__file__).parent
SEARCH = ["OAI-SearchBot", "Claude-SearchBot", "PerplexityBot"]
USER = ["ChatGPT-User", "Claude-User", "Perplexity-User"]
TRAINING = ["GPTBot", "ClaudeBot", "Google-Extended"]
PAGES = [u.split(".example", 1)[1] for u in FakeWeb().page_urls("tidewell.example")]


def robots():
    return (HERE / "robots.txt").read_text()


def part(text, heading):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


def test_search_and_user_bots_read_everything_public():
    for bot in SEARCH + USER:
        blocked = [p for p in PAGES if not robots_allows(robots(), bot, p)]
        assert not blocked, f"{bot} is blocked from {blocked}"
    assert any(l.lower().startswith("user-agent") for l in robots().splitlines()), "write the file"


def test_cart_and_account_blocked_for_everyone():
    for bot in SEARCH + USER + TRAINING + ["SomeOtherBot"]:
        for path in ("/cart", "/account/orders"):
            assert not robots_allows(robots(), bot, path), f"{bot} may fetch {path}"


def test_training_decision_matches_the_file(source):
    text = part(source("ROBOTS_POLICY.md"), "Training crawlers")
    for bot in TRAINING:
        m = re.search(rf"^{bot}:\s*(allow|block)\b", text, re.M | re.I)
        assert m, f"write a line '{bot}: allow' or '{bot}: block'"
        says_allow = m.group(1).lower() == "allow"
        assert robots_allows(robots(), bot, "/faq") == says_allow, \
            f"the policy says {bot}: {m.group(1)}, robots.txt does the opposite"


def test_written(source):
    text = source("ROBOTS_POLICY.md")
    assert "<!--" not in text, "Delete the instructions comment."
    for heading, words in (("The three kinds of crawler", 80), ("Training crawlers", 60),
                           ("What robots.txt cannot do", 50)):
        assert f"## {heading}" in text, f"No '{heading}' section."
        assert len(part(text, heading).split()) >= words, f"'{heading}' needs {words} words."
