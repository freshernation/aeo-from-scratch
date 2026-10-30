# Day 3 — Sitemaps, canonicals and llms.txt

> **By the end of today** you can audit a sitemap against what crawlers can actually
> read (B), and write an llms.txt and say honestly what it is worth (S).

---

## Read first

- [ ] [Sitemaps protocol](https://www.sitemaps.org/protocol.html) · 10 min
- [ ] [The llms.txt proposal](https://llmstxt.org/) · 15 min

---

## What you need to know

### A sitemap is a promise

It tells crawlers which URLs matter. A sitemap listing a 404, a redirect or a noindexed
page wastes a crawler's visit and says the site does not know its own pages.

### Today's finding

**Tidewell's sitemap lists 19 URLs: one 404, one redirect, and six pages crawlers may not
index. The one page it leaves out, the carbon-versus-reverse-osmosis guide, is readable,
and it answers one of the thirty prompts.**

### llms.txt: a proposal

A markdown file at the site root listing the pages an agent should read. It is a
proposal (revised in August 2026), not a standard. None of the four vendors' crawler
pages mention it, and the panel ignores it. Write one if it is cheap, point it only at
readable pages, and do not promise a client a lift nobody has measured.

---

## Exercises

**Builders** — copy `robots.py` and `fetchcheck.py` in, then `pytest week-03/day-3/build -v`.
Write `sitemap.py`.

**Strategists** — `pytest week-03/day-3/strategy -v`. Write `llms.txt` and `LLMS_NOTE.md`.

---

## Predict-then-run

How many of the sitemap's 19 URLs will a crawler both fetch with a 200 and be allowed to
index? Write a number.

---

## Before you close the laptop

Commit, push, fill in the signal log.
