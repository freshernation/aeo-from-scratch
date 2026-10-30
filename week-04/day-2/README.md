# Day 2 — Facts, early

> **By the end of today** you can pull the facts out of a passage by pattern (B), and
> move the facts in two system pages into their first sentences (S).

---

## Read first

- [ ] GEO paper, sections 3.3 and 4 — [the methods and what raised visibility](https://arxiv.org/abs/2311.09735) · 20 min: statistics and quotations, measured
- [ ] Google — [Creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) · 10 min

---

## What you need to know

### A fact is something a reader could check

A price, a percentage, a volume, a certification, a duration, a year. The GEO paper
found adding statistics raised visibility in its engines; the panel encodes that as R8.

### Today's finding

**ClearFlow's passages carry 7.7 facts per 100 words; Tidewell's 2.95. And 57% of
ClearFlow's passages have a fact in the first sentence, against 20% of Tidewell's.**
Tidewell has the facts. The UX3's certifications and price sit in its third and fourth
sections.

### Only digits count here

"Six months" is not a fact to the extractor, and to the panel's R8 it is not a number
either. Whether to write "6 months" is a style choice with a measured cost; make it on
purpose.

---

## Exercises

**Builders** — `pytest week-04/day-2/build -v`. Write `facts.py`. Week 6 reuses it.

**Strategists** — edit `under-sink.html` and `reverse-osmosis.html` in the snapshot, then
`pytest week-04/day-2/strategy -v`, then `BEFORE_AFTER.md`.

---

## Predict-then-run

Which of Tidewell's pages has the most facts that are not in any first sentence?

---

## Before you close the laptop

Commit, push, fill in the signal log.
