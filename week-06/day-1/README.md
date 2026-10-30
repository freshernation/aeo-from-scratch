# Day 1 — Who else talks about you

> **By the end of today** you can count who mentions, links to and repeats a company's
> claims (B), and map what other sites say about Tidewell, right and wrong (S).

---

## Read first

- [ ] GEO paper, section 6 — [the same methods on a deployed engine](https://arxiv.org/abs/2311.09735) · 15 min: what changes when you cannot see inside
- [ ] Bing — [Webmaster Guidelines](https://www.bing.com/webmasters/help/webmasters-guidelines-30fba23a) · 10 min: what an engine says it values

---

## What you need to know

### Three kinds of outside support

A **mention** names you. A **link** points at you; the panel's R9 counts linking
domains. **Corroboration** repeats a claim of yours, which lets an engine quote it with
confidence and lets a reader check it.

### Today's finding

**Five sites name Tidewell (twelve paragraphs) and all five link to it; ClearFlow is
linked from four. Four repeat the UX3's PFOA certification. And three of the five state
something about Tidewell that is wrong today.** Outside support is not always support.

---

## Exercises

**Builders** — `pytest week-06/day-1/build -v`. Write `corroborate.py`.

**Strategists** — `python3 week-06/day-1/strategy/show_mentions.py`, then
`pytest week-06/day-1/strategy -v`. Write `MENTIONS.md`.

---

## Predict-then-run

Which site mentions Tidewell most often? Guess before you count.

---

## Before you close the laptop

Commit, push, fill in the signal log.
