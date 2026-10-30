# Day 4 — Fan-out, and the searches nobody answers

> **By the end of today** you can fan a prompt out into several searches and fuse the
> results (B), and list the searches Tidewell has no passage for (S).

---

## Read first

- [ ] Cormack, Clarke, Büttcher — [Reciprocal rank fusion](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) · 10 min
- [ ] OpenAI — [web search in the API](https://platform.openai.com/docs/guides/tools-web-search) · 10 min

---

## What you need to know

### One prompt, several searches

Google describes AI Mode as breaking a question into subtopics and issuing many
searches at once. The fake model's scripts do this for the thirty prompts: "Does a
water filter pitcher remove PFAS?" also searches "NSF 53 PFOA PFOS pitcher".

### Fusion by rank

Scores from different searches are not comparable; ranks are. Reciprocal rank fusion
adds 1/(60 + rank) for every list a passage appears in, so a passage that is fourth in
three searches beats one that is first in one.

### Today's finding

**Fan-out changes the top passage on 12 of the 30 prompts, but it puts Tidewell's best
page into the top four on only one more prompt (19 of 28 without, 20 with).** Fan-out
moves winners more than it finds pages. And of the 62 fan-out searches, 8 return no
Tidewell passage in the panel's top five: those are the places a competitor's sentence
goes into Tidewell's answer.

### A gap is not always missing content

Look at the gaps' searches: "NSF 53 lead reduction filter" is answered by Tidewell's
lead page, which exists. The panel cannot crawl it. Week 3 tells the two apart.

---

## Exercises

**Builders** — copy `passages.py` and `bm25.py` in, then `pytest week-01/day-4/build -v`.
Write `fanout.py`.

**Strategists** — `pytest week-01/day-4/strategy -v`. Write `gaps.py`, then `GAPS.md`.

---

## Predict-then-run

Pick P18 ("best water filter pitcher in 2026"). Predict which of its searches Tidewell
has no answer for, then run your `gaps()` on it alone.

---

## Before you close the laptop

Commit, push, fill in the signal log.
