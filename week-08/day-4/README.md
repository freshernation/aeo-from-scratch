# Day 4 — Re-measure, write it up, book the live check

> **By the end of today** you have the before-and-after on two engines, the case study, and
> a dated plan to check on live engines in thirty days or more.

---

## Read first

- [ ] Your week 7 `MONITORING_PLAN.md` or `monitor.py` · 10 min
- [ ] The reference case study's limits section, as read aloud by your instructor

---

## What you need to know

```bash
python3 week-08/measure.py
```

Twenty samples per prompt at temperature 0.3, seed 8, on the panel and Engine B, with and
without `after/`. It writes `site/results.json`; the test re-runs it, so your file must match
your site as it is.

### What your numbers are about

With a handful of sites in the snapshot, a cited rate near 100% says there were few other
sites to cite. First-cited and the paired results are the evidence. The reference case
study says this in its first limit.

### The live check

Engines re-crawl slowly. Book the live run at least thirty days after you measured, with a
monitor config, a budget and the result that would change your mind.

---

## Exercises

```bash
pytest week-08/day-4 -v
```

Write `CASE_STUDY.md` and `REMEASURE.md`.

---

## Before you close the laptop

Commit, push, fill in the signal log, then rehearse with `ai/interviewer.md`.
