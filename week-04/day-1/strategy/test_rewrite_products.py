"""Day 1: the pitcher and shower pages, rewritten in week-04/snapshot/tidewell.example/filters/."""
from aeolab import PROMPTS_MORE, load_prompts
from aeolab.panel import Panel
from rewrite_checks import best_cited, doc_sections, rewrite_problems

TARGETS = ["P07", "P13", "P18", "P27", "P33", "P34"]


def test_pitcher():
    assert rewrite_problems("/filters/pitcher") == []


def test_shower():
    assert rewrite_problems("/filters/shower") == []


def test_the_panel_now_cites_them(snapshot_web):
    prompts = [x for x in load_prompts() + load_prompts(PROMPTS_MORE) if x["id"] in TARGETS]
    got = best_cited(Panel(snapshot_web), prompts)
    assert sum(got.values()) >= 4, \
        f"the right Tidewell page is cited on {sum(got.values())} of 6 target prompts (none before); aim for 4: {got}"


def test_before_after(source):
    problem = doc_sections(source("BEFORE_AFTER.md"), (("Pitcher", 60), ("Shower", 60)))
    assert problem is None, problem
