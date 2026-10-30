from collections import Counter

import pytest
from aeolab import load_pages, load_prompts, web2
from aeolab.llm import FakeModel
from aeolab.panel import Panel


def mod(load):
    for f in ("passages.py", "bm25.py", "fanout.py"):
        load(f)
    return load("boosts.py")


class TestBoosts:
    def test_first_sentence(self, load):
        assert mod(load).first_sentence("It holds 2.4 litres. Costs $12.50 each.") == "It holds 2.4 litres."

    def test_values(self, load):
        b = mod(load).boosts({"text": "It removes lead: 99% at 150 litres, NSF/ANSI 53, $34."}, "remove lead")
        assert b == {"self_contained": 0.7, "answer_first": 1.25, "specific": pytest.approx(1.24)}

    def test_answer_first_needs_half(self, load):
        assert mod(load).boosts({"text": "Carbon filters work well."}, "carbon lead pfas")["answer_first"] == 1.0

    def test_rerank(self, load):
        b = mod(load)
        a = {"text": "This is vague and long-winded about filters."}
        c = {"text": "Lead filters reduce lead by 99%."}
        assert b.rerank([a, c], "lead filters") == [c, a], "the boosted second passage overtakes the first"


def test_finding_copying_the_rules_does_not_copy_the_engine(load):
    """Your week 1 retrieval, with and without the boosts, against the panel, on web2."""
    b = mod(load)
    split = load("passages.py").split_passages
    web = web2()
    bm = load("bm25.py").BM25([p for url, html in load_pages(web).items() for p in split(url, html)])
    fan, panel, model = load("fanout.py").search_fanout, Panel(web), FakeModel()

    def cites(passages):
        out, per = [], Counter()
        for p in passages:
            d = p["url"].split("/")[2]
            if p["url"] in out or per[d] >= 2:
                continue
            out.append(p["url"])
            per[d] += 1
            if len(out) == 4:
                break
        return out

    plain = boosted = 0
    for x in load_prompts():
        hits = fan(bm, model, x["prompt"], 20)
        theirs = {c.url for c in panel.ask(x["prompt"]).citations}
        plain += len(set(cites(hits)) & theirs)
        boosted += len(set(cites(b.rerank(hits, x["prompt"]))) & theirs)
    assert (plain, boosted) == (80, 75), \
        "with the panel's boosts your engine agrees with the panel LESS: boosts reorder what retrieval found, and your retrieval is not the panel's"
