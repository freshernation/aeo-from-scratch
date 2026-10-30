import pytest
from aeolab import load_runs

ROWS = [
    {"prompt_id": "P1", "cited_domains": ["a.ex", "b.ex"], "answer": "Tidewell's filter is good."},
    {"prompt_id": "P1", "cited_domains": ["b.ex"], "answer": "Nothing here."},
    {"prompt_id": "P2", "cited_domains": ["b.ex", "a.ex", "c.ex"], "answer": "TIDEWELL and Tidewellness."},
    {"prompt_id": "P2", "cited_domains": [], "answer": ""},
]


class TestMetrics:
    def test_citation_rate(self, load):
        assert load("metrics.py").citation_rate(ROWS, "a.ex") == 0.5

    def test_first_rate(self, load):
        assert load("metrics.py").first_rate(ROWS, "a.ex") == 0.25

    def test_prompt_rates(self, load):
        assert load("metrics.py").prompt_rates(ROWS, "a.ex") == {"P1": 0.5, "P2": 0.5}

    def test_share_of_voice(self, load):
        sov = load("metrics.py").share_of_voice(ROWS)
        assert sov == {"b.ex": 0.5, "a.ex": pytest.approx(1 / 3), "c.ex": pytest.approx(1 / 6)}
        assert list(sov) == ["b.ex", "a.ex", "c.ex"], "most cited first"

    def test_mention_whole_word_any_case(self, load):
        assert load("metrics.py").mention_rate(ROWS, "Tidewell") == 0.5

    def test_mentioned_not_cited(self, load):
        assert load("metrics.py").mentioned_not_cited(ROWS, "Tidewell", "c.ex") == 1

    def test_empty(self, load):
        m = load("metrics.py")
        assert m.citation_rate([], "a") == m.first_rate([], "a") == m.mention_rate([], "x") == 0.0


def test_finding_cited_is_not_first(load):
    m = load("metrics.py")
    rows = load_runs("baseline.jsonl")
    assert round(m.citation_rate(rows, "tidewell.example"), 3) == 0.73
    assert round(m.first_rate(rows, "tidewell.example"), 3) == 0.215, \
        "cited in 73% of answers, first in barely one in five"
    assert round(m.first_rate(rows, "clearflow.example"), 3) == 0.363
    assert m.mentioned_not_cited(rows, "Tidewell", "tidewell.example") == 91, \
        "91 answers name Tidewell and cite someone else for it"
