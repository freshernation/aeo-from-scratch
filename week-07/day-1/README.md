# Day 1 — Three engines, one shape

> **By the end of today** you can parse Claude's, OpenAI's and Perplexity's answers into
> week 2's rows (B), and compare live-shaped answers with the panel, honestly labelled (S).

---

## Read first

- [ ] Claude — [web search tool: citations](https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-search-tool) · 15 min
- [ ] OpenAI — [web search: output and citations](https://platform.openai.com/docs/guides/tools-web-search) · 10 min
- [ ] Perplexity — [quickstart](https://docs.perplexity.ai/getting-started/quickstart) · 10 min

---

## What you need to know

### Three shapes

Claude returns text blocks, each with `citations` of type `web_search_result_location`
(url, title, cited_text). OpenAI's Responses API returns a `web_search_call` item and a
`message` whose text carries `url_citation` annotations. Perplexity's Sonar returns
`citations`, a list of URLs, and `search_results`. All three checked on 2026-10-30.

### The fixtures are not evidence

`aeolab/data/live/` follows those shapes with invented content built from the course's
engines. They test parsers. Say so whenever you use them.

### Today's finding

**Across thirty answers per vendor, about 85 distinct citation strings are about 45 pages:
the same page arrives with tracking parameters, text fragments and trailing slashes.** On
the fixtures these are planted; on live engines check how often it happens.

---

## Exercises

**Builders** — `pytest week-07/day-1/build -v`. Write `adapters.py`.

**Strategists** — `python3 week-07/day-1/strategy/show_live.py`, then
`pytest week-07/day-1/strategy -v`. Write `LIVE_CHECK.md`.

---

## Predict-then-run

How many of a vendor's raw citation strings will survive normalisation as separate pages?

---

## Before you close the laptop

Commit, push, fill in the signal log.
