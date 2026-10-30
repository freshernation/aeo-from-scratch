# Day 2 — Retrieval, and what people ask

> **By the end of today** you can score passages against a query with BM25 written by
> hand (B), and sort prompts into the five intents with rules you can explain (S).

---

## Read first

- [ ] Okapi BM25 — [the formula and its parts](https://en.wikipedia.org/wiki/Okapi_BM25) · 15 min
- [ ] Google — [AI Mode and query fan-out](https://blog.google/products/search/google-search-ai-mode-update/) · 10 min

---

## What you need to know

### Retrieval decides who is in the room

Scoring and citing only choose among candidates. If retrieval does not find a passage,
nothing later can rescue it. BM25 rewards a term that is rare across the web (idf),
frequent in the passage (with diminishing returns, k1) and in a passage that is not
padded (length normalisation, b).

### The panel is not BM25

The panel uses TF-IDF with cosine, then fan-out, then boosts. **Today's finding: on
the same web and the same thirty prompts, plain BM25's top passage comes from the page
the panel cites first on only 9 of 30.** Two reasonable engines disagree most of the
time. That is why week 4 asks for a rewrite that wins on both.

### Intent

Answer engines treat "what is X", "best X", "X vs Y", "how do I X" and "Tidewell X"
differently, and buyers ask them at different moments. The course prompt set is 16
informational, 7 brand, 3 commercial, 2 comparison and 2 how-to.

### Rules in order

A prompt can match two intents: "Tidewell Pitcher vs ClearFlow Pitcher" names the
brand and compares. Which rule comes first is a decision. Write it down.

---

## Exercises

**Builders** — copy your `passages.py` from day 1 into `day-2/build/`, then

```bash
pytest week-01/day-2/build -v
```

Write `bm25.py`. The first test is computed by hand; read it before you start.

**Strategists**

```bash
pytest week-01/day-2/strategy -v
```

Write `intent.py`, then add ten new prompts in `NEW_PROMPTS.md`. Six prompts your rules
have never seen are hidden in the test: rules that only fit the thirty will fail them.

---

## Predict-then-run

How many of the 30 prompts will your BM25 and the panel agree on, top result against
first citation? Write a number, then run the finding test.

---

## Before you close the laptop

Commit, push, fill in the signal log.
