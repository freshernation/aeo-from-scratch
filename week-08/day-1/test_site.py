import csv
import json

from site_checks import SITE, check_sections, info

INTENTS = {"brand", "howto", "comparison", "commercial", "informational"}


def prompts():
    with open(SITE / "prompts.csv", newline="") as f:
        return list(csv.DictReader(f))


def test_site_json():
    data = info()
    assert len(data.get("competitors", [])) >= 2, "name at least two other sites that answer your customers' questions"


def test_thirty_prompts():
    rows = prompts()
    assert len(rows) == 30, f"{len(rows)} prompts; write 30"
    assert len({r["id"] for r in rows}) == 30 and all(r["intent"] in INTENTS for r in rows)
    domain = info()["domain"]
    bad = [r["id"] for r in rows if r["best_url"] and f"://{domain}" not in r["best_url"]]
    assert not bad, f"best_url must be a page on {domain}: {bad}"
    assert sum(bool(r["best_url"]) for r in rows) >= 20, "most prompts should have a page of yours that ought to answer them"


def test_fanout():
    fan = json.loads((SITE / "fanout.json").read_text())
    texts = {r["prompt"] for r in prompts()}
    assert len(fan) >= 5, "write the searches for at least five prompts"
    assert set(fan) <= texts, "every key in fanout.json must be one of your prompts, word for word"


def test_written(source):
    check_sections(source("SITE.md"), (("The site", 40), ("Permission", 20), ("Competitors and sources", 40),
                                      ("The customers' questions", 60)))
