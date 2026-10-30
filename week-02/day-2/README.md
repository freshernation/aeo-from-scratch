# Day 2 — The same question, twenty answers

> **By the end of today** you can show how far a citation rate moves when you measure
> with fewer samples (B), list the prompts whose answer changes run to run (S), and
> say how many samples you would pay for.

---

## Read first

- [ ] Anthropic — [Adding error bars to evals](https://www.anthropic.com/research/statistical-approach-to-model-evals) · 20 min

---

## What you need to know

### Engines are not deterministic

Live engines sample: the same prompt cites different pages on different runs. The
panel imitates this with temperature, a random factor on every passage score. At
temperature 0 it always answers the same; the run files use 0.3.

### Today's finding

**19 of the 30 prompts cite Tidewell on some samples and not on others. With one
sample per prompt, Tidewell's overall rate lands anywhere from 63% to 83%; with ten,
70% to 77%; not even fifteen pin it within five points.** A one-off check is a coin
toss on two-thirds of the prompts.

### With replacement

To ask "what would a fresh run of n samples say?", draw n answers per prompt *with*
replacement from the recorded 20. Drawing without replacement makes large n look
falsely certain: 15 of the same 20 answers are mostly the same answers.

---

## Exercises

**Builders** — copy `metrics.py` in, then `pytest week-02/day-2/build -v`. Write `sampling.py`.

**Strategists** — `pytest week-02/day-2/strategy -v`. Write `stability.py`, then `STABILITY.md`.

---

## Predict-then-run

Guess the range at one sample per prompt before running it. Most people guess five
points.

---

## Before you close the laptop

Commit, push, fill in the signal log.
