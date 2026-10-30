import pytest
from aeolab import load_runs


def test_wilson(load):
    lo, hi = load("compare.py").wilson(7, 20)
    assert (round(lo, 4), round(hi, 4)) == (0.1812, 0.5671)
    assert load("compare.py").wilson(0, 0) == (0.0, 1.0)


def test_prompt_rates(load):
    rows = [{"prompt_id": "A", "cited_domains": ["t"]}, {"prompt_id": "A", "cited_domains": []}]
    assert load("compare.py").prompt_rates(rows, "t") == {"A": 0.5}


def test_sign(load):
    c = load("compare.py")
    assert c.sign_test(0, 0) == 1.0 and c.sign_test(9, 8) == 1.0
    assert c.sign_test(15, 4) == pytest.approx(0.019211, abs=1e-6)


def test_finding_noise_and_a_real_change(load):
    c = load("compare.py")
    base = load_runs("baseline.jsonl")
    assert c.wins_losses(base, load_runs("rerun.jsonl"), "tidewell.example") == (9, 8, 13), \
        "nothing changed between these runs, and still 17 prompts moved"
    w, l, t = c.wins_losses(base, load_runs("fixed.jsonl"), "tidewell.example")
    assert (w, l, t) == (15, 4, 11) and c.sign_test(w, l) < 0.05
