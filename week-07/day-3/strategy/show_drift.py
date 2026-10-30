"""Given. Nine weekly panel runs, and how each week compares with the one before.

    python3 week-07/day-3/strategy/show_drift.py
"""
import glob
import math
from pathlib import Path

from aeolab import RUNS, load_runs

D = "tidewell.example"


def rates(rows):
    by = {}
    for r in rows:
        by.setdefault(r["prompt_id"], []).append(D in r["cited_domains"])
    return {p: sum(v) / len(v) for p, v in by.items()}


def main():
    files = sorted(glob.glob(str(RUNS / "history" / "*.jsonl")))
    prev = None
    for f in files:
        rows = load_runs(f)
        r = rates(rows)
        overall = sum(D in x["cited_domains"] for x in rows) / len(rows)
        line = f"{Path(f).stem[6:]}  cited {overall:.1%}"
        if prev:
            up = sum(r[p] > prev[p] for p in r)
            down = sum(r[p] < prev[p] for p in r)
            n, k = up + down, min(up, down)
            pval = 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)
            line += f"   vs last week: {up} up, {down} down, p = {pval:.3f}"
        print(line)
        prev = r


if __name__ == "__main__":
    main()
