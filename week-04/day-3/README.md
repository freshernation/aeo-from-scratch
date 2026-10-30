# Day 3 — Structure, and what the engine rewards

> **By the end of today** you can give your engine the panel's three boosts and explain
> what happened (B), and turn an FAQ into questions answered in their first sentence (S).

---

## Read first

- [ ] The panel's docstring, rules R6 to R8 — `aeolab/panel.py` · 5 min
- [ ] Google — [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) · 10 min

---

## What you need to know

### Headings as questions

A question heading tells an engine which question the passage answers, and gives the
first sentence an obvious job. Tidewell's FAQ already has question headings. Its answers
start with "Great question" and "We get this one often", which is what the panel quotes.

### Today's finding

**Builders: with the panel's three boosts added, your week 1 engine agrees with the panel
less, not more: 75 shared citations of 120 instead of 80.** The boosts reorder the
candidates your retrieval found, and your retrieval (BM25 over your passages) is not the
panel's (TF-IDF over its passages, thin ones dropped). Copying a ranking rule does not copy
an engine. Strategists: the FAQ rewrite makes a Tidewell page the first source for P11,
where PurePath's was.

### Tables

A table row becomes a sentence like "Filter Pitcher, Removes Chlorine, lead." in the panel.
It is retrievable and quotable, but rarely answer-first. Use a table to back up an answer
that is already in a sentence, not as the only place a fact lives.

---

## Exercises

**Builders** — copy `passages.py`, `bm25.py`, `fanout.py` from `week-01/milestone/build/`,
then `pytest week-04/day-3/build -v`. Write `boosts.py`.

**Strategists** — edit `faq.html` in the snapshot, then `pytest week-04/day-3/strategy -v`,
then `BEFORE_AFTER.md`.

---

## Predict-then-run

Builders: will the boosts raise or lower agreement with the panel? Write the number.

---

## Before you close the laptop

Commit, push, fill in the signal log.
