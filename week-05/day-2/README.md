# Day 2 — One company, many descriptions

> **By the end of today** you can find every name, founding year and city the web gives
> a company and list the conflicts (B), and write the entity sheet and the corrections (S).

---

## Read first

- [ ] Google — [Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization) · 10 min
- [ ] schema.org — [sameAs](https://schema.org/sameAs) · 5 min

---

## What you need to know

### An entity, not a string

To a reader, "Tidewell", "Tidewell Water Co." and "TideWell Inc." might be three companies.
An engine that retrieves passages from all three quotes whichever scores best.

### Today's finding

**On web2 Tidewell is written three ways: "Tidewell" 16 times, "Tidewell Water Co." twice
and "TideWell Inc." once. One directory page disagrees on everything: TideWell Inc., of
Seattle, founded 2015. Tidewell's own page and the encyclopedia say Portland, 2016.**
Ask the panel "Where is Tidewell based?" and the answer contains both cities.

### What you can fix

Your own pages, your markup (`sameAs`), and a polite request to the directory. Week 6
measures what the request is worth.

---

## Exercises

**Builders** — copy `jsonld.py` in, then `pytest week-05/day-2/build -v`. Write `entities.py`.

**Strategists** — `python3 week-05/day-2/strategy/show_entity.py`, then
`pytest week-05/day-2/strategy -v`. Write `ENTITY.md`.

---

## Predict-then-run

Run the panel on "When was Tidewell founded?" and predict which years the answer contains.

---

## Before you close the laptop

Commit, push, fill in the signal log.
