from collections import Counter

from aeolab import PROMPTS_MORE, load_prompts, web2
from aeolab.fakeweb import FakeWeb
from aeolab.panel import Panel


def test_kinds_on_the_original_web(load):
    a = load("attribution.py")
    p = Panel(FakeWeb())
    by_id = {x["id"]: x for x in load_prompts()}
    assert a.attribute(p, by_id["P03"]) == "not-crawled", "week 1: the lead page was blocked by robots.txt"
    assert a.attribute(p, by_id["P20"]) == "no-page"
    assert a.attribute(p, by_id["P24"]) == "cited"


def test_all_and_first(load):
    a = load("attribution.py")
    p = Panel(web2())
    prompts = load_prompts()[:3]
    assert set(a.attribute_all(p, prompts)) == {"P01", "P02", "P03"}
    assert sum(a.first_cited_by(p, prompts).values()) == 3


def test_finding_after_access_every_loss_is_content(load):
    a = load("attribution.py")
    p = Panel(web2())
    r = a.attribute_all(p, load_prompts() + load_prompts(PROMPTS_MORE))
    assert Counter(r.values()) == {"cited": 17, "out-scored": 12, "not-retrieved": 4, "no-page": 3}, \
        "on web2 nothing is lost to crawling any more: 12 out-scored, 4 never retrieved"
    assert a.first_cited_by(p, load_prompts()).most_common(2) == [("tidewell.example", 13), ("clearflow.example", 8)]
