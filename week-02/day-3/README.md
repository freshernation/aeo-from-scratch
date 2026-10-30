# Day 3 — Intervals, and a fair comparison

> **By the end of today** you can put an honest interval on a citation rate and say
> whether two runs differ by more than noise.

---

## Read first

- [ ] Evan Miller — [How not to sort by average rating](https://www.evanmiller.org/how-not-to-sort-by-average-rating.html) · 10 min
- [ ] [Sign test](https://en.wikipedia.org/wiki/Sign_test) · 10 min

---

## What you need to know

### Wilson, and why it is too narrow here

The Wilson interval is the right interval for k successes in n independent trials.
Our 600 answers are not independent: they are 30 prompts asked 20 times, and answers to
one prompt move together. **Today's finding: Wilson over the 600 answers gives 69% to
76%; resampling whole prompts (the bootstrap) gives 61% to 84%, three times wider.**
The second is the honest one.

### Pair by prompt

Prompts differ enormously from each other (Tidewell is cited on 100% of P24's samples
and 0% of P12's), and that spread is the same in both runs. Compare each prompt with
itself: did it go up, down or stay? Then ask how likely that many ups would be by
chance: the sign test.

### Noise has a shape

`rerun.jsonl` is the same web run again. 9 prompts went up, 8 went down, 13 stayed: p =
1.0. `fixed.jsonl` removed one robots.txt line: 15 up, 4 down, p = 0.019. Their
intervals overlap; the paired test still tells them apart.

---

## Exercises

**Builders** — copy `metrics.py` and `sampling.py` in, then `pytest week-02/day-3/build -v`.
Write `stats.py`.

**Strategists** — `pytest week-02/day-3/strategy -v`. Write `compare.py`.

---

## Predict-then-run

Before running the paired test on `rerun` against `baseline`, predict how many prompts
moved at all. Nothing changed between them.

---

## Before you close the laptop

Commit, push, fill in the signal log.
