# Day 2 — Snapshot and audit

> **By the end of today** you have an offline copy of your site and its competitors, an
> audit of it, and a fix order with evidence.

---

## Read first

- [ ] The docstring of `aeolab/snapshot.py` · 10 min: what it saves, and what it cannot see
- [ ] Your week 6 audit report or audit tool · 10 min

---

## What you need to know

### The snapshot

```bash
python3 -m aeolab.snapshot week-08/site/snapshot https://YOUR-SITE/ https://COMPETITOR-1/ https://COMPETITOR-2/
```

It reads robots.txt and obeys it, waits a second between requests, stops at 40 pages per
site, and saves pages, robots.txt, sitemap.xml, redirects and X-Robots-Tag headers. It does
not run JavaScript and it is not an AI crawler, so a CDN rule that blocks AI bots will not
show: check that in your server log (week 7) or your CDN's settings. The snapshot folder is
ignored by git: other sites' pages stay on your machine.

### The audit

Builders: `python3 week-06/milestone/build/aeo_audit.py YOUR-DOMAIN --web week-08/site/snapshot --prompts week-08/site/prompts.csv`.
Strategists: `python3 week-08/audit_site.py`. Then read the output yourself: the reference
audit found its own tool counting the word "lumen" as mentions of a brand called Lumen.

---

## Exercises

```bash
pytest week-08/day-2 -v
```

Write `AUDIT.md`, ending in `## Fix first`.

---

## Predict-then-run

Which step loses most of your prompts: crawling, retrieval or score?

---

## Before you close the laptop

Commit, push, fill in the signal log.
