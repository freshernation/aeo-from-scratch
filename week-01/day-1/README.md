# Day 1 — Passages, and the panel's trace

> **By the end of today** you can say what an answer engine actually retrieves (a
> passage, not a page), split any page into passages (B), and read the panel's trace
> for a prompt to say why each citation won (S).

---

## Read first

- [ ] GEO paper, sections 1–3 — [GEO: Generative Engine Optimization](https://arxiv.org/abs/2311.09735) · 25 min
- [ ] The panel's docstring — `aeolab/panel.py`, top of the file · 10 min

---

## What you need to know

### Seven steps, not one ranking

Crawl, split, fan out, retrieve, score, cite, answer. A search engine's results page
is the output of roughly the first four. An answer engine adds three more, and a page
can be lost at any of the seven. The panel prints all of them for any prompt.

### The passage is the unit

Engines quote a span of a page: a section under a heading, a paragraph, a table row.
The panel cuts a page at every `h2` and `h3`; the text before the first heading sits
under the `h1`. A page that answers five questions in one wall of text gives the engine
one long passage that matches everything weakly.

### Today's finding

The seeded web is 50 pages and 104 passages, split evenly: 52 on Tidewell, 52
everywhere else. **Nine of Tidewell's 52 passages open with "It", "This" or "They".
Not one passage on any other site does.** Lifted out alone, "It is certified to
NSF/ANSI 53" answers nothing: what is "it"? The panel has a rule for this (R6); find it.

### Reading a trace

`show_trace.py P01` prints the fan-out searches, the top candidates with their
retrieval score (`rrf`) and every boost that is not 1.0, and marks the cited ones. A
page missing from the candidates was lost before scoring; a page in the candidates but
not cited lost on its boosts.

---

## Exercises

**Builders** — `build/`

```bash
pytest week-01/day-1/build -v
```

Write `passages.py`: `tokenize()` and `split_passages()`, from the spec at the top of
the file. The last test is the finding: it runs your splitter over all 50 pages.

**Strategists** — `strategy/`

```bash
python3 week-01/day-1/strategy/show_trace.py P01
pytest week-01/day-1/strategy -v
```

Trace the ten prompts listed in `TRACE.md` and write up each one.

---

## Predict-then-run

Before you run `show_trace.py P10` ("How much does the Tidewell UX3 cost?"), write down
which site you expect to be cited first. Then run it. Look at the price in the answer.

---

## Before you close the laptop

Commit, push, fill in the signal log.
