# Day 1 — JSON-LD, by hand

> **By the end of today** you can extract, validate and fact-check JSON-LD (B), and
> write correct, true markup for three Tidewell pages (S).

---

## Read first

- [ ] Google — [Introduction to structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) · 15 min
- [ ] Google — [Structured data general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) · 10 min: markup must describe what is on the page
- [ ] schema.org — [Product](https://schema.org/Product) and [Organization](https://schema.org/Organization) · 10 min, skim

---

## What you need to know

### JSON-LD

A `<script type="application/ld+json">` block in the page describing what the page is
about in schema.org's vocabulary. Engines and search crawlers receive it like any other
HTML; whether they use it is up to each.

### Today's finding

**Nine pages on web2 carry JSON-LD. Two are broken: PurePath's is not valid JSON
(a trailing comma) and AquaMinder's Product has no offers. Tidewell's pitcher markup is
valid and says the price is $29; the page says $34.** A validator passes it.

### Required, in this course

Product needs a name and offers; an Offer needs a price and a currency; an Organization a
name and a url. That is a minimum this course chose, not Google's full rule book, which
varies by feature.

---

## Exercises

**Builders** — `pytest week-05/day-1/build -v`. Write `jsonld.py`.

**Strategists** — edit `week-05/snapshot/tidewell.example/filters/pitcher.html`,
`filters/shower.html` and `about.html`, then `pytest week-05/day-1/strategy -v`.

---

## Predict-then-run

How many of the nine blocks will your validator call clean? Then: how many are true?

---

## Before you close the laptop

Commit, push, fill in the signal log.
