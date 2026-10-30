"""The snapshot is laid over the seeded web; the panel then crawls the result.

To see the lift yourself:
    from aeolab import load_prompts, load_runs
    from aeolab.fakeweb import FakeWeb
    from aeolab.panel import Panel
    rows = Panel(FakeWeb(overlay="week-03/milestone/strategy/snapshot")).run(
        load_prompts(), samples=20, temperature=0.3, seed=5)
"""
import re
from pathlib import Path

from aeolab import load_prompts, load_runs
from aeolab.fakeweb import FakeWeb
from aeolab.panel import Panel, robots_allows

SNAP = Path(__file__).parent / "snapshot"
T = "https://tidewell.example"
SEARCH = ["PanelBot", "OAI-SearchBot", "Claude-SearchBot", "PerplexityBot"]
TRAINING = ["GPTBot", "ClaudeBot", "Google-Extended"]


def web():
    return FakeWeb(overlay=SNAP)


def part(text, heading):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


def test_every_page_readable_by_every_search_bot():
    for bot in SEARCH:
        p = Panel(web(), bot=bot)
        bad = {u: p.readable(u)[1] for u in web().page_urls("tidewell.example") if not p.readable(u)[0]}
        assert bad == {T + "/filters/pitcher-blue": "canonical-elsewhere"}, f"{bot} still cannot read {bad}"


def test_learn_open_and_private_paths_still_blocked():
    robots = web().fetch(T + "/robots.txt").text
    assert robots_allows(robots, "PanelBot", "/learn/lead-in-water"), "open /learn/ first"
    for bot in SEARCH + TRAINING:
        assert not robots_allows(robots, bot, "/cart") and not robots_allows(robots, bot, "/account")


def test_training_lines_match_what_the_site_does(source):
    text = part(source("FIXES.md"), "Training crawlers")
    for bot in TRAINING:
        m = re.search(rf"^{bot}:\s*(allow|block)\b", text, re.M | re.I)
        assert m, f"write '{bot}: allow' or '{bot}: block'"
        readable = Panel(web(), bot=bot).readable(T + "/faq")[0]
        assert readable == (m.group(1).lower() == "allow"), \
            f"FIXES.md says {bot}: {m.group(1)}, the snapshot does the opposite (check robots.txt AND the server)"


def test_the_lift_is_real():
    rows = Panel(web()).run(load_prompts(), samples=20, temperature=0.3, seed=5)
    base = load_runs("baseline.jsonl")
    rate = sum("tidewell.example" in r["cited_domains"] for r in rows) / len(rows)
    assert rate >= 0.8, f"citation rate {rate:.3f}; fixing access should take it above 0.80"
    by = {}
    for name, rs in (("a", base), ("b", rows)):
        for r in rs:
            by.setdefault((name, r["prompt_id"]), []).append("tidewell.example" in r["cited_domains"])
    ups = sum(sum(by[("b", p)]) > sum(by[("a", p)]) for p in {r["prompt_id"] for r in base})
    downs = sum(sum(by[("b", p)]) < sum(by[("a", p)]) for p in {r["prompt_id"] for r in base})
    assert ups >= 15 and ups > 2 * downs, f"{ups} prompts up, {downs} down"


def test_written(source):
    text = source("FIXES.md")
    assert "<!--" not in text, "Delete the instructions comment."
    for heading, words in (("Summary", 40), ("What I left alone", 40), ("The lift", 60),
                           ("What this does not prove", 50)):
        assert len(part(text, heading).split()) >= words, f"'{heading}' needs {words} words."
    rows = [l for l in part(text, "What I fixed").splitlines() if l.startswith("|") and not l.startswith(("| File", "|---"))]
    assert len(rows) >= 5, "at least five fixes in the table"
    assert re.search(r"\d+(\.\d+)?\s?%", part(text, "The lift")), "report the numbers"
