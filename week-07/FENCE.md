# Week 7 — Concept fence

## Allowed

**Everything from weeks 1 to 6**, plus:

- The three vendors' response shapes: Claude's text citations, OpenAI's url_citation
  annotations, Perplexity's citations and search_results; `aeolab/live.py`
- URL normalisation: tracking parameters, fragments, trailing slashes
- Prices per search and per token; assumptions labelled as assumptions; unpriced engines
- `sqlite3` (B); week 2's paired test as a drift alert
- Combined log format; published bot IP ranges; `ipaddress`; referrers and utm tags

## Not yet

Your own site (week 8) · dashboards and schedulers (cut: cron runs the monitor) ·
reverse-DNS verification (Google's method, not covered) · buying an AEO tool (cut)

---

## Why fixtures and not live answers in the tests

A test that calls a live engine costs money, fails when a vendor is slow, and gives a
different answer every run. The fixtures keep the vendors' documented shapes and invent the
content, so the parsers are tested exactly and nobody mistakes them for evidence. Live
evidence comes from running `aeolab/live.py` yourself, and the course says so every time.
