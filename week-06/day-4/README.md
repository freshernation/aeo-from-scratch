# Day 4 — Every loss, one step

> **By the end of today** you can attribute every prompt Tidewell loses to the step that
> lost it (B), and explain where and why competitors win (S).

---

## Read first

- [ ] The panel's docstring and `ask()` — `aeolab/panel.py` · 15 min: what `trace["all"]` holds
- [ ] Your week 1 `TRACE.md` or day 1 test · 5 min: the same question, six weeks ago

---

## What you need to know

### Six answers

For each prompt: **no-page** (Tidewell has none), **cited**, **not-crawled**,
**not-retrieved** (never a candidate), **capped** (scored high enough, cut by the
two-per-site rule), **out-scored** (a candidate that lost on score).

### Today's finding

**On web2, before week 4's rewrites: of 33 prompts with a Tidewell page, 17 cite it, 12
lost on score and 4 were never retrieved. None is lost to crawling.** In week 1 half the
losses were access. Week 3 moved every remaining problem into content and retrieval.
Tidewell is cited first on 13 of the 30 prompts, ClearFlow on 8.

---

## Exercises

**Builders** — `pytest week-06/day-4/build -v`. Write `attribution.py`.

**Strategists** — `python3 week-06/day-4/strategy/show_losses.py`, then
`pytest week-06/day-4/strategy -v`. Write `COMPETITOR_GAPS.md`.

---

## Predict-then-run

How many losses will be "not-crawled" now? Think back to week 3.

---

## Before you close the laptop

Commit, push, fill in the signal log.
