# Day 1 — Five ways to say "visible"

> **By the end of today** you can compute, from a run file, a site's citation rate,
> first-cited rate, share of voice and mention rate, and say which one flatters.

---

## Read first

- [ ] GEO paper, section 3.4 — [how visibility is measured](https://arxiv.org/abs/2311.09735) · 15 min
- [ ] One line of `aeolab/runs/baseline.jsonl` — read every field · 5 min

---

## What you need to know

### A run file

One row per answer: which prompt, which sample, which URLs and domains were cited, in
order, and the answer text. 30 prompts × 20 samples = 600 rows.

### Five numbers

**Citation rate**: share of answers citing the site anywhere. **First-cited rate**:
share where it is the first source, which is usually the one quoted most. **Share of
voice**: its share of all citations, across every site. **Mention rate**: share of
answers that name the brand. **Mentioned, not cited**: answers that talk about you and
credit someone else.

### Today's finding

**Tidewell is cited in 73% of answers but first in only 21.5%, against ClearFlow's
36.3%. And 91 of 600 answers name Tidewell while citing another site for it.** A
dashboard showing only the 73% would tell Tidewell it is winning.

---

## Exercises

**Builders** — `pytest week-02/day-1/build -v`. Write `metrics.py` (six functions).

**Strategists** — `pytest week-02/day-1/strategy -v`. Write `metrics.py` (three functions).

---

## Predict-then-run

Before you compute it: is Tidewell's share of voice higher or lower than its citation
rate, and why must it be lower than 100% / (number of sites cited per answer)?

---

## Before you close the laptop

Commit, push, fill in the signal log.
