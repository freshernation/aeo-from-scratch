# Day 1 — Passages that survive being quoted alone

> **By the end of today** you can find the four problems that cost a passage its quote
> (B), and rewrite two product pages so every passage stands alone (S).

---

## Read first

- [ ] Anthropic — [Contextual retrieval](https://www.anthropic.com/engineering/contextual-retrieval) · 15 min: chunks that lose their context
- [ ] [Inverted pyramid](https://en.wikipedia.org/wiki/Inverted_pyramid_(journalism)) · 5 min

---

## What you need to know

### Four problems

**Pronoun opener**: "It is certified..." What is? **Long first sentence**: the part an
engine quotes. **Thin**: under 12 words, which the panel drops. **Buried answer**: the
heading's subject appears in the passage, but not in its first sentence.

### Today's finding

**42% of Tidewell's passages have at least one of the four problems; 13% of ClearFlow's.
Tidewell's count: 10 thin, 9 pronoun openers, 5 buried answers.** The pitcher's price
("The Tidewell Pitcher costs $34 and comes with one cartridge.") is 9 words: the panel
never indexes it, so "How much does the Tidewell Pitcher cost?" is answered without
Tidewell's price.

### Rewriting rules

Name the subject in every passage. Answer in the first sentence. Put the number there
too. Keep every passage over 12 words. Use only facts already on the site: the tests
compare every number you write with every number Tidewell already publishes.

---

## Exercises

**Builders** — copy `passages.py` from `week-01/milestone/build/`, then
`pytest week-04/day-1/build -v`. Write `lint.py`.

**Strategists** — edit `week-04/snapshot/tidewell.example/filters/pitcher.html` and
`shower.html`, then `pytest week-04/day-1/strategy -v`, then `BEFORE_AFTER.md`.

---

## Predict-then-run

Before running the linter on Tidewell: which code will be most common? Write it down.

---

## Before you close the laptop

Commit, push, fill in the signal log.
