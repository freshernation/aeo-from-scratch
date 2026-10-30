import json
from pathlib import Path

import pytest

PASSAGES = [
    {"url": "a", "text": "Carbon filters reduce chlorine taste."},
    {"url": "b", "text": "Reverse osmosis removes fluoride and nitrates."},
]


class TestSupport:
    def test_example(self, load):
        assert load("cite.py").support("Lead pipes leak lead.", "Old pipes contain lead.") == pytest.approx(2 / 3)

    def test_distinct_tokens(self, load):
        assert load("cite.py").support("lead lead lead", "lead") == 1.0, "count each sentence token once"

    def test_empty_sentence(self, load):
        assert load("cite.py").support("No.", "No, it does not.") == 0.0, "'No.' has no tokens - support 0.0"


class TestAttribute:
    def test_best_passage(self, load):
        assert load("cite.py").attribute(["Reverse osmosis removes fluoride."], PASSAGES) == ["b"]

    def test_below_threshold(self, load):
        assert load("cite.py").attribute(["Boiling concentrates arsenic."], PASSAGES) == [None]

    def test_threshold_is_inclusive(self, load):
        # tokens: carbon, remove, fluoride, arsenic -> passage b has remove, fluoride = 0.5
        assert load("cite.py").attribute(["Carbon removes fluoride arsenic."], PASSAGES[1:]) == ["b"]

    def test_tie_goes_to_first(self, load):
        twins = [{"url": "x", "text": "lead"}, {"url": "y", "text": "lead"}]
        assert load("cite.py").attribute(["lead"], twins) == ["x"]

    def test_unsupported(self, load):
        out = load("cite.py").unsupported(["Carbon reduces chlorine.", "Boiling concentrates arsenic."], PASSAGES)
        assert out == ["Boiling concentrates arsenic."]


def test_finding_overlap_misses_invented_claims(load, prompts, panel):
    """The day's finding. The fake model adds one invented sentence to four of the
    thirty answers. How many does a word-overlap check catch?"""
    cite = load("cite.py")
    extras = set(json.loads((Path(__file__).parents[3] / "aeolab/data/extras.json").read_text()).values())
    by_id = {p.id: {"url": p.url, "text": p.text} for p in panel.passages}

    def count(threshold):
        caught = flagged_true = 0
        for x in prompts:
            a = panel.ask(x["prompt"])
            for s in cite.unsupported(a.sentences, [by_id[i] for i in a.trace["cited"]], threshold):
                if s in extras:
                    caught += 1
                else:
                    flagged_true += 1
        return caught, flagged_true

    assert count(0.5) == (1, 2), "at 0.5 overlap catches 1 of 4 invented claims, and flags 2 true answers ('No.')"
    assert count(0.7) == (4, 2), "at 0.7 it catches all 4 - on this web. Overlap is not truth: it only says the words are there"
