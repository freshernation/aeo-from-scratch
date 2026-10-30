import pytest
from aeolab import load_runs


def loaded(load):
    load("metrics.py")
    load("sampling.py")
    return load("stats.py")


class TestWilson:
    def test_known_value(self, load):
        lo, hi = loaded(load).wilson(7, 20)
        assert (round(lo, 4), round(hi, 4)) == (0.1812, 0.5671)

    def test_edges(self, load):
        s = loaded(load)
        assert s.wilson(0, 0) == (0.0, 1.0)
        assert s.wilson(0, 10)[0] == 0.0 and s.wilson(10, 10)[1] == pytest.approx(1.0)


class TestSign:
    def test_values(self, load):
        s = loaded(load)
        assert s.sign_test(0, 0) == 1.0
        assert s.sign_test(9, 8) == 1.0, "capped at 1"
        assert s.sign_test(15, 4) == pytest.approx(0.019211, abs=1e-6)
        assert s.sign_test(4, 15) == s.sign_test(15, 4), "two-sided"


class TestPaired:
    def test_paired(self, load):
        a = [{"prompt_id": p, "cited_domains": d} for p, d in [("A", ["t"]), ("B", []), ("C", ["t"])]]
        b = [{"prompt_id": p, "cited_domains": d} for p, d in [("A", ["t"]), ("B", ["t"]), ("C", [])]]
        assert loaded(load).paired(a, b, "t") == {"wins": 1, "losses": 1, "ties": 1, "p": 1.0}


def test_finding_two_intervals_and_two_runs(load):
    s = loaded(load)
    base = load_runs("baseline.jsonl")
    k = sum("tidewell.example" in r["cited_domains"] for r in base)
    w = s.wilson(k, len(base))
    b = s.prompt_bootstrap(base, "tidewell.example")
    assert (round(w[0], 3), round(w[1], 3)) == (0.693, 0.764)
    assert (round(b[0], 3), round(b[1], 3)) == (0.61, 0.84), \
        "Wilson over 600 answers is 7 points wide; resampling prompts, 23 points: the answers are not independent"
    noise = s.paired(base, load_runs("rerun.jsonl"), "tidewell.example")
    real = s.paired(base, load_runs("fixed.jsonl"), "tidewell.example")
    assert (noise["wins"], noise["losses"], noise["p"]) == (9, 8, 1.0), "a rerun with nothing changed: 9 up, 8 down"
    assert (real["wins"], real["losses"]) == (15, 4) and real["p"] < 0.05
