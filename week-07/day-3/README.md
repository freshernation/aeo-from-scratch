# Day 3 — Runs over time

> **By the end of today** you can keep every run in SQLite and alert only when a week's
> change is beyond noise (B), and explain nine weeks of runs (S).

---

## Read first

- [ ] Python — [sqlite3](https://docs.python.org/3/library/sqlite3.html) · 10 min
- [ ] Your week 2 `stats.py` or `compare.py` · 5 min

---

## What you need to know

### Keep the rows, not the numbers

A stored rate cannot be re-analysed; stored rows can. Save every answer with its run,
engine and date.

### Today's finding

**Nine weekly runs in `aeolab/runs/history/`. The paired test raises exactly two alerts:
a drop on 24 August (84.7% to 69.7%, 3 prompts up, 13 down, p = 0.021) and a rise on
7 September (18 up, 4 down, p = 0.004). The other six comparisons are noise.** A threshold
on the raw rate ("alert below 80%") would have alerted on 31 August too, telling nobody
anything new.

---

## Exercises

**Builders** — copy week 2's `metrics.py`, `sampling.py`, `stats.py` in, then
`pytest week-07/day-3/build -v`. Write `store.py`.

**Strategists** — `python3 week-07/day-3/strategy/show_drift.py`, then
`pytest week-07/day-3/strategy -v`. Write `DRIFT.md`.

---

## Predict-then-run

Before running it: which weeks will alert? Look at the rates first, then the paired test.

---

## Before you close the laptop

Commit, push, fill in the signal log.
