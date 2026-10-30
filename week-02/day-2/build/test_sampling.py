import random

from aeolab import load_runs


def rows_for(k_by_prompt, n=4):
    out = []
    for pid, k in k_by_prompt.items():
        for s in range(n):
            out.append({"prompt_id": pid, "sample": s, "cited_domains": ["t.ex"] if s < k else []})
    return out


class TestSampling:
    def test_by_prompt(self, load):
        load("metrics.py")
        g = load("sampling.py").by_prompt(rows_for({"A": 1, "B": 2}))
        assert list(g) == ["A", "B"] and len(g["A"]) == 4

    def test_subsample_takes_n_per_prompt(self, load):
        load("metrics.py")
        out = load("sampling.py").subsample(rows_for({"A": 1, "B": 2}), 2, random.Random(0))
        assert [r["prompt_id"] for r in out] == ["A", "A", "B", "B"]

    def test_subsample_draws_with_replacement(self, load):
        load("metrics.py")
        out = load("sampling.py").subsample(rows_for({"A": 1}), 8, random.Random(0))
        assert len(out) == 8, "8 draws from 4 rows: with replacement, rows can repeat"

    def test_no_spread_when_every_sample_agrees(self, load):
        load("metrics.py")
        assert load("sampling.py").spread(rows_for({"A": 4, "B": 0}), "t.ex", 1) == (0.5, 0.5)

    def test_spread_shrinks(self, load):
        load("metrics.py")
        s = load("sampling.py")
        rows = rows_for({p: 2 for p in "ABCDEFGH"})
        lo1, hi1 = s.spread(rows, "t.ex", 1)
        lo3, hi3 = s.spread(rows, "t.ex", 3)
        assert hi1 - lo1 > hi3 - lo3

    def test_stable_at(self, load):
        load("metrics.py")
        s = load("sampling.py")
        assert s.stable_at(rows_for({"A": 4, "B": 0}), "t.ex") == 1
        assert s.stable_at(rows_for({"A": 10}, n=20), "t.ex", width=0.0) is None, \
            "15 of 20 samples still varies - no n in NS gives zero spread"


def test_finding_one_sample_is_not_a_number(load):
    load("metrics.py")
    s = load("sampling.py")
    rows = load_runs("baseline.jsonl")
    lo, hi = s.spread(rows, "tidewell.example", 1)
    assert (round(lo, 3), round(hi, 3)) == (0.633, 0.833), \
        "with one sample per prompt, Tidewell's citation rate lands anywhere from 63% to 83%"
    lo, hi = s.spread(rows, "tidewell.example", 10)
    assert (round(lo, 3), round(hi, 3)) == (0.7, 0.767)
    assert s.stable_at(rows, "tidewell.example", width=0.1) == 10, "10 samples per prompt pins it within 10 points"
    assert s.stable_at(rows, "tidewell.example") is None, "and not even 15 gets it within 5"
