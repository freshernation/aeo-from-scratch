# Day 3 — Does structured data change citation?

> **By the end of today** you can run an experiment with and without structured data on
> two engines, and say exactly what its result does and does not show.

---

## Read first

- [ ] Google — [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) · 10 min
- [ ] Google — [Changes to HowTo and FAQ rich results (2023)](https://developers.google.com/search/blog/2023/08/howto-faq-changes) · 5 min: markup's rewards change

---

## What you need to know

### The claim

Google: "There are no additional requirements to appear in AI Overviews or AI Mode, nor
other special optimizations necessary." Many vendors say the opposite about markup.

### Today's finding

**Removing every piece of JSON-LD from every site on web2 changes 0 of 600 answers on the
panel and 0 of 600 on Engine B. Adding correct markup to three Tidewell pages also changes
0 of 600.** Neither engine reads markup as content; the panel reads it only for a date,
and only when a page shows none.

### What a null result means

We built both engines and could have read this in their source. The experiment's value is
the method: same prompts, same seed, one change, count what moves. Run it on a live engine
in week 7 and the result is evidence. Here it is a check that the method works.

---

## Exercises

**Builders** — copy `jsonld.py` in, then `pytest week-05/day-3/build -v`. Write
`schema_experiment.py`.

**Strategists** — `python3 week-05/day-3/strategy/show_experiment.py`, then
`pytest week-05/day-3/strategy -v`. Write `SCHEMA_EXPERIMENT.md`.

---

## Predict-then-run

Before running it: how many of 600 answers will change when every block is removed?

---

## Before you close the laptop

Commit, push, fill in the signal log.
