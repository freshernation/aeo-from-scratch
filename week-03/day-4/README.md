# Day 4 — Every page, every crawler

> **By the end of today** you can produce the full access matrix for a site and its
> summary (B), and write an access audit that tells engineering what to fix first (S).

---

## Read first

- [ ] Your own `fetchcheck.py` or `INVISIBLE.md` · 10 min
- [ ] Google — [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) · 10 min

---

## What you need to know

### The matrix

Nineteen pages by nine crawlers is 171 answers to "can it read this?". Most audits
check one crawler. The interesting faults are the ones that differ between crawlers.

### Today's finding

**Claude-SearchBot and PerplexityBot cannot read a single Tidewell page. robots.txt
allows them; the server refuses them with a 403, robots.txt included. ClaudeBot, which
robots.txt also allows, is refused the same way.** The block lives in the CDN's bot
setting, so no review of robots.txt would ever find it. Under RFC 9309, a 4xx on
robots.txt itself means "no rules", so a crawler would have been allowed everywhere,
if the server had let it in.

### Fix order

Order by what each fix unlocks: the server block hides every page from two engines;
the /learn/ line hides three guides from all of them; one noindex hides the main
product page. Cost matters too: a CDN setting is one switch.

---

## Exercises

**Builders** — copy `robots.py` and `fetchcheck.py` in, then `pytest week-03/day-4/build -v`.
Write `access.py`.

**Strategists** — `python3 week-03/day-4/strategy/show_access.py`, then
`pytest week-03/day-4/strategy -v`. Write `ACCESS_AUDIT.md`.

---

## Predict-then-run

How many of the 171 cells are readable? Predict, then count.

---

## Before you close the laptop

Commit, push, fill in the signal log.
