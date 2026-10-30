# Day 4 — Two engines, not one

> **By the end of today** you can measure any rewrite on any engine with a paired test
> on first-cited (B), and show your rewrites help on the panel without hurting on
> Engine B (S).

---

## Read first

- [ ] `aeolab/engine_b.py`, the docstring · 5 min
- [ ] Google — [Spam policies: keyword stuffing](https://developers.google.com/search/docs/essentials/spam-policies) · 10 min

---

## What you need to know

### Why two engines

Live engines differ, change without notice, and cannot be inspected. A rewrite that wins
on one by exploiting its rules may lose on the next. Engine B shares the panel's crawler
and nothing else: two-sentence windows, word density, no fan-out, no boosts.

### Today's finding

**Builders: a keyword-stuffed install guide raises Tidewell's citation rate on the panel
from 84.2% to 91.2% and is still no clear change on first-cited, on either engine. When
the panel does cite it, the answer quotes "Install under-sink filter install under-sink
water filter...".** Being cited and being useful are different results.

**Strategists: the five reference rewrites move the panel's first-cited rate from 35.5%
to 55.5% (22 prompts up, 2 down) and Engine B's from 39.8% to 43.2% (4 up, 2 down,
p = 0.69).** One engine moved a lot and the other did not move against it. That is the
pass mark.

### Same seed, before and after

Both runs use seed 4. The noise for a passage is keyed by seed, sample and prompt, so
the two runs share their luck, and the difference is mostly the change.

---

## Exercises

**Builders** — copy `metrics.py`, `sampling.py`, `stats.py` from week 2's milestone, then
`pytest week-04/day-4/build -v`. Write `compare.py`.

**Strategists** — `python3 week-04/day-4/strategy/show_lift.py`, then
`pytest week-04/day-4/strategy -v`, then `LIFT.md`.

---

## Predict-then-run

Before running it: will your rewrite move Engine B up, down, or not at all?

---

## Before you close the laptop

Commit, push, fill in the signal log.
