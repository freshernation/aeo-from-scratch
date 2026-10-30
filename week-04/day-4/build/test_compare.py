from pathlib import Path

from aeolab import load_prompts, web2
from aeolab.engine_b import EngineB
from aeolab.panel import Panel

FIX = Path(__file__).parent / "fixtures"


def mod(load):
    for f in ("metrics.py", "sampling.py", "stats.py"):
        load(f)
    return load("compare.py")


def test_firsts(load):
    rows = [{"prompt_id": "A", "cited_domains": ["a", "b"]}]
    assert mod(load).firsts(rows) == [{"prompt_id": "A", "cited_domains": ["a"]}] and rows[0]["cited_domains"] == ["a", "b"]


def test_verdict(load):
    v = mod(load).verdict
    assert v({"paired_first": {"wins": 9, "losses": 1, "p": 0.02}}) == "helps"
    assert v({"paired_first": {"wins": 1, "losses": 9, "p": 0.02}}) == "hurts"
    assert v({"paired_first": {"wins": 3, "losses": 1, "p": 0.6}}) == "no clear change"


def test_lift_of_nothing_is_nothing(load):
    r = mod(load).lift(Panel, web2(), web2(), load_prompts()[:5], "tidewell.example", samples=3)
    assert r["cited"][0] == r["cited"][1] and r["paired"]["wins"] == r["paired"]["losses"] == 0


def test_finding_stuffing_gets_cited_and_says_nothing(load):
    c = mod(load)
    prompts = load_prompts()
    for engine in (Panel, EngineB):
        for name in ("honest", "stuffed"):
            r = c.lift(engine, web2(), web2(FIX / name), prompts, "tidewell.example")
            assert c.verdict(r) == "no clear change", f"{name} on {engine.__name__}"
    r = c.lift(Panel, web2(), web2(FIX / "stuffed"), prompts, "tidewell.example")
    assert (round(r["cited"][0], 3), round(r["cited"][1], 3)) == (0.842, 0.912), \
        "the stuffed page is cited more often..."
    answer = Panel(web2(FIX / "stuffed")).ask("How long does it take to install an under-sink filter?").sentences
    assert any(s.startswith("Install under-sink filter install") for s in answer), \
        "...and when it is, the answer quotes a string of keywords"
