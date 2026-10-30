"""Day 2: the UX3 and RO-5 pages - facts moved into first sentences."""
from aeolab import PROMPTS_MORE, load_prompts
from aeolab.panel import Panel
from rewrite_checks import best_cited, doc_sections, rewrite_problems

TARGETS = ["P05", "P08", "P10", "P15", "P19", "P21", "P36"]


def test_under_sink():
    assert rewrite_problems("/filters/under-sink") == []


def test_reverse_osmosis():
    assert rewrite_problems("/filters/reverse-osmosis") == []


def test_the_panel_now_cites_them(snapshot_web):
    prompts = [x for x in load_prompts() + load_prompts(PROMPTS_MORE) if x["id"] in TARGETS]
    got = best_cited(Panel(snapshot_web), prompts)
    assert sum(got.values()) >= 5, f"{sum(got.values())} of 7 target prompts cite the right page (2 before); aim for 5: {got}"


def test_before_after(source):
    problem = doc_sections(source("BEFORE_AFTER.md"), (("UX3", 60), ("RO-5", 60)))
    assert problem is None, problem
