# Day 3 — Citations, and what makes a passage quotable

> **By the end of today** you can check which passage supports each sentence of an
> answer, and say how weak that check is (B); and score any passage on five checks a
> client can understand (S).

---

## Read first

- [ ] Claude web search tool — [how citations come back](https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-search-tool) · 15 min
- [ ] GEO paper, section 3.4 — [the visibility metrics](https://arxiv.org/abs/2311.09735) · 15 min

---

## What you need to know

### A citation is a claim about a sentence

When an engine puts a source next to a sentence, it claims the sentence came from it.
Real engines return citations tied to spans of the answer. The fake model here writes
each answer from the first sentence of each cited passage, and on four prompts adds a
sentence of its own that no passage says.

### Word overlap is a weak witness

**Today's finding: a check that a sentence shares half its words with a cited passage
catches 1 of the 4 invented claims. Raise the bar to 70% and it catches all 4 on this
web, and at every threshold it flags the true answer "No." because "No." has no words
to match.** Overlap says the words are present. It does not say the claim is true.
"Every pitcher filter on the market removes all microplastics" shares most of its words
with a passage that says the opposite.

### Five checks

The course's quotability checklist: a first sentence of 30 words or fewer, no opening
pronoun, a number, 20 to 120 words, and a first sentence that names the heading's
subject. On every passage the panel indexed, Tidewell averages 3.46 of 5. ClearFlow
3.93, AquaMinder 4.17. Only the forum scores lower than the client.

### A checklist is not the engine

Compare the five checks with the panel's boosts. Two map straight onto panel rules (no
opening pronoun, a number) and a third is half of one (a short first sentence); the
other two are not rules the panel has. A checklist is useful to a client because
they can read it, and dangerous because a client will believe it is how the engine works.

---

## Exercises

**Builders** — copy `passages.py` in, then `pytest week-01/day-3/build -v`. Write `cite.py`.

**Strategists** — `pytest week-01/day-3/strategy -v`. Write `citable.py`.

---

## Predict-then-run

Read `aeolab/data/extras.json`. For each invented sentence, predict whether a 0.5
overlap check catches it. Then run the finding test.

---

## Before you close the laptop

Commit, push, fill in the signal log.
