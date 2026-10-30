import pytest
from aeolab import load_runs

ROWS = [
    {"prompt_id": "P1", "cited_domains": ["a.ex", "b.ex"], "answer": "Tidewell is good."},
    {"prompt_id": "P1", "cited_domains": ["b.ex"], "answer": "nothing"},
    {"prompt_id": "P2", "cited_domains": ["b.ex", "a.ex", "c.ex"], "answer": "tidewell"},
    {"prompt_id": "P2", "cited_domains": [], "answer": ""},
]


def test_citation_rate(load):
    assert load("metrics.py").citation_rate(ROWS, "a.ex") == 0.5
    assert load("metrics.py").citation_rate([], "a.ex") == 0.0


def test_share_of_voice(load):
    assert load("metrics.py").share_of_voice(ROWS) == {"a.ex": pytest.approx(1 / 3), "b.ex": 0.5,
                                                        "c.ex": pytest.approx(1 / 6)}


def test_mention_rate(load):
    assert load("metrics.py").mention_rate(ROWS, "Tidewell") == 0.5, "ignore case"


def test_finding_share_of_voice(load):
    m = load("metrics.py")
    rows = load_runs("baseline.jsonl")
    sov = {d: round(v, 3) for d, v in m.share_of_voice(rows).items()}
    assert sov["clearflow.example"] == 0.312 and sov["tidewell.example"] == 0.233, \
        "ClearFlow takes 31% of all citations, Tidewell 23%"
    assert round(m.mention_rate(rows, "Tidewell"), 3) == 0.483
