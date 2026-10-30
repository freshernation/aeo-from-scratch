# Day 2 — Price it first

> **By the end of today** you can cost a run before running it and refuse to plan what
> nobody has priced (B), and write a sampling plan with its monthly cost (S).

---

## Read first

- [ ] Claude — [web search pricing](https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-search-tool) · 5 min: $10 per 1,000 searches plus tokens
- [ ] OpenAI — [pricing: web search](https://platform.openai.com/docs/pricing) · 5 min
- [ ] Perplexity — [pricing](https://docs.perplexity.ai/getting-started/pricing) · 10 min

---

## What you need to know

### What one answer costs

Searches × the search fee, plus the tokens the model reads (search results count as
input) and writes. `aeolab/data/prices.json` has Claude's verified prices, OpenAI's search
fee, and nothing for Perplexity; the tokens per answer are course assumptions.

### Today's finding

**Week 2's ten samples per prompt, on Claude, cost $19.20 a run on the course's
assumptions, about $83 a month weekly. A $50 budget buys 26 samples per prompt for one run.
Two of the three live engines cannot be planned at all until someone fills in a price.**

### Unknown is not zero

An engine with a missing price is not free. Code that treats null as 0 approves a budget
nobody checked.

---

## Exercises

**Builders** — `pytest week-07/day-2/build -v`. Write `budget.py`.

**Strategists** — `pytest week-07/day-2/strategy -v`. Write `plan.py`, then `SAMPLING_PLAN.md`.

---

## Predict-then-run

Guess the monthly cost of weekly monitoring on Claude before you compute it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
