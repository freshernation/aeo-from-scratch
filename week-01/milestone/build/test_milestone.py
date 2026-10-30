import json
from pathlib import Path

from aeolab.llm import FakeModel


def engine(load, pages):
    for f in ("passages.py", "bm25.py", "cite.py", "fanout.py"):
        load(f)
    return load("engine.py").Engine(pages)


def test_answer_shape(load, pages):
    a = engine(load, pages).answer("Do water filters remove lead?")
    assert set(a) == {"citations", "sentences", "unsupported"}
    assert len(a["citations"]) == 4 == len(set(a["citations"])), "four different urls"


def test_at_most_two_per_domain(load, pages, prompts):
    e = engine(load, pages)
    for x in prompts:
        domains = [u.split("/")[2] for u in e.answer(x["prompt"])["citations"]]
        assert max(domains.count(d) for d in domains) <= 2, f"{x['id']}: {domains}"


def test_uses_the_model_given(load, pages):
    for f in ("passages.py", "bm25.py", "cite.py", "fanout.py"):
        load(f)
    m = FakeModel(fanout={}, extras={"q lead": "Invented."})
    a = load("engine.py").Engine(pages, model=m, k=2).answer("q lead")
    assert len(a["citations"]) == 2 and a["sentences"][-1] == "Invented."
    assert a["unsupported"] == ["Invented."], "the invented sentence has no support in any cited passage"


def test_deterministic(load, pages):
    e = engine(load, pages)
    assert e.answer("Which water filters remove PFAS?") == e.answer("Which water filters remove PFAS?")


def test_finding_two_engines(load, pages, prompts, panel):
    """Your engine against the panel, on the same thirty prompts."""
    e = engine(load, pages)
    shared = best_mine = best_panel = 0
    for x in prompts:
        mine = e.answer(x["prompt"])["citations"]
        theirs = [c.url for c in panel.ask(x["prompt"]).citations]
        shared += len(set(mine) & set(theirs))
        best_mine += x["best_url"] in mine
        best_panel += x["best_url"] in theirs
    assert shared == 69, f"the two engines share {shared} of 120 citations, expected 69"
    assert (best_mine, best_panel) == (20, 10), \
        "your engine cites Tidewell's best page on 20 prompts, the panel on 10. Yours reads every page on disk - week 3 finds out what a crawler cannot"
