# Day 2 — Fetching like a bot

> **By the end of today** you can fetch a URL the way a crawler does and name the first
> reason it cannot be indexed (B), and list every Tidewell page a crawler cannot index,
> with the fix (S).

---

## Read first

- [ ] Vercel — [The rise of the AI crawler](https://vercel.com/blog/the-rise-of-the-ai-crawler) · 15 min
- [ ] Google — [Block indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing) · 10 min

---

## What you need to know

### The order a crawler meets things

robots.txt (before any fetch, including after a redirect), then the status code,
then headers (`X-Robots-Tag`), then the HTML (`<meta name="robots">`, canonical), then
the text. A page blocked at an earlier step never shows its later problems.

### JavaScript

Vercel measured real crawler traffic and found the major AI crawlers did not render
JavaScript. A page whose content is drawn by a script arrives as an empty shell.

### Today's finding

**7 of Tidewell's 19 pages cannot be indexed by a generic search bot: three blocked by
robots.txt, one noindex in a meta tag, one noindex in an HTTP header, one JavaScript-only
page, and one duplicate pointing elsewhere, the only one that is fine.** The header
noindex and the JavaScript page cannot be found by reading the page source or robots.txt.

---

## Exercises

**Builders** — copy `robots.py` in, then `pytest week-03/day-2/build -v`. Write `fetchcheck.py`.

**Strategists** — `python3 week-03/day-2/strategy/view_as_bot.py /warranty`, then
`pytest week-03/day-2/strategy -v`. Fill `INVISIBLE.md`.

---

## Predict-then-run

Before running `view_as_bot.py /compare`, predict the word count a bot reads and the
word count a browser shows.

---

## Before you close the laptop

Commit, push, fill in the signal log.
