# Day 4 — The structured data audit

> **By the end of today** you can add a structured-data and entity module to the audit
> tool (B), and write the structured-data audit with a fix order (S).

---

## Read first

- [ ] Your own `jsonld.py` or `SCHEMA_EXPERIMENT.md` · 10 min
- [ ] Google — [Structured data general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) · 10 min, again

---

## What you need to know

### Only readable pages

Markup on a page no crawler can read helps nobody. The module audits the pages
`check()` says a search crawler can index, 18 of Tidewell's 19 on web2.

### Today's finding

**Three of Tidewell's 18 readable pages carry markup (Product, Organization, FAQPage),
and one of them is false.** Next to the access matrix this finishes the audit of the
pages Tidewell owns.

### Order the fixes

False markup first, then missing identity (sameAs), then coverage: correct Product markup
on every product page, generated from the same data as the visible price.

---

## Exercises

**Builders** — copy `jsonld.py`, `entities.py`, `robots.py`, `fetchcheck.py` in, then
`pytest week-05/day-4/build -v`. Write `schema.py`.

**Strategists** — `python3 week-05/day-4/strategy/show_schema.py`, then
`pytest week-05/day-4/strategy -v`. Write `SCHEMA_AUDIT.md`.

---

## Predict-then-run

Which competitor has the most complete markup? Check.

---

## Before you close the laptop

Commit, push, fill in the signal log.
