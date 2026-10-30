import csv
import re
from pathlib import Path

from aeolab import load_prompts
from aeolab.fakeweb import FakeWeb

INTENTS = {"brand", "howto", "comparison", "commercial", "informational"}


def rows():
    with open(Path(__file__).parent / "prompts_plus.csv", newline="") as f:
        return list(csv.DictReader(f))


def test_forty_prompts():
    r = rows()
    assert len(r) == 40, f"{len(r)} prompts; the 30 course prompts plus your 10"
    assert len({x["id"] for x in r}) == 40, "ids must be unique"
    assert [x["id"] for x in r[:30]] == [p["id"] for p in load_prompts()], "start with the course's 30, in order"
    assert all(x["intent"] in INTENTS for x in r), "every intent must be one of the five"


def test_new_best_urls_are_real_pages():
    pages = set(FakeWeb().page_urls("tidewell.example"))
    new = rows()[30:]
    assert len(new) == 10, "add your ten new prompts first"
    for x in new:
        assert x["best_url"] == "" or x["best_url"] in pages, f"{x['id']}: {x['best_url']} is not a Tidewell page"


def test_written(source):
    text = source("PROMPT_SET.md")
    assert "<!--" not in text, "Delete the instructions comment in PROMPT_SET.md."
    for heading, words in (("The prompt set", 60), ("Where Tidewell is cited", 60), ("The gaps", 60),
                           ("What I will measure next week", 40)):
        assert f"## {heading}" in text, f"PROMPT_SET.md has no '{heading}' section."
        part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(part.split()) >= words, f"'{heading}' is {len(part.split())} words; it needs {words}."
    cited = text.split("## Where Tidewell is cited", 1)[1].split("\n## ")[0]
    assert re.search(r"\b7 of 7\b|\b7/7\b|100%", cited), "say the brand number: the panel cites Tidewell on 7 of 7 brand prompts"
