import glob
from pathlib import Path

from aeolab import RUNS, load_runs


def mod(load):
    for f in ("metrics.py", "sampling.py", "stats.py"):
        load(f)
    return load("store.py")


def rows(run, cited):
    return [{"run_id": run, "prompt_id": f"P{i}", "sample": 0, "cited_urls": [], "cited_domains": ["t"] if c else [],
             "answer": ""} for i, c in enumerate(cited)]


def test_store_round_trip(load, tmp_path):
    s = mod(load).RunStore(tmp_path / "r.db")
    s.save(rows("b", [1, 0]), "panel", "2026-01-08")
    s.save(rows("a", [1, 1]), "panel", "2026-01-01")
    s.save(rows("c", [0]), "other", "2026-01-02")
    assert [r["run_id"] for r in s.runs()] == ["a", "c", "b"]
    assert [r["run_id"] for r in s.runs("panel")] == ["a", "b"]
    assert s.rows("b") == rows("b", [1, 0])


def test_store_survives_reopening(load, tmp_path):
    m = mod(load)
    m.RunStore(tmp_path / "r.db").save(rows("a", [1]), "panel", "2026-01-01")
    assert len(m.RunStore(tmp_path / "r.db").rows("a")) == 1


def test_drift_alerts(load, tmp_path):
    m = mod(load)
    s = m.RunStore(tmp_path / "r.db")
    s.save(rows("a", [1] * 12), "panel", "2026-01-01")
    s.save(rows("b", [0] * 12), "panel", "2026-01-08")
    d = m.drift(s, "t", "panel")
    assert d == [{"from": "2026-01-01", "to": "2026-01-08", "before": 1.0, "after": 0.0, "wins": 0, "losses": 12,
                  "p": d[0]["p"], "alert": "drop"}] and d[0]["p"] < 0.001


def test_finding_one_bad_week(load, tmp_path):
    m = mod(load)
    s = m.RunStore(tmp_path / "r.db")
    for f in sorted(glob.glob(str(RUNS / "history" / "*.jsonl"))):
        s.save(load_runs(f), "panel", Path(f).stem[6:])
    alerts = [(d["to"], d["alert"]) for d in m.drift(s, "tidewell.example", "panel") if d["alert"]]
    assert alerts == [("2026-08-24", "drop"), ("2026-09-07", "rise")], \
        "a redeploy on 24 August and its fix two weeks later - and no false alarm in the other six weeks"
