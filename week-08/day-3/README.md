# Day 3 — Make the changes

> **By the end of today** you have changed at least three pages (and anything else the fix
> order puts first) in `site/after/`, without inventing a fact, and on the real site if you can.

---

## Read first

- [ ] Your week 4 `PROJECT1.md` or day 1 linter · 10 min
- [ ] Your `AUDIT.md`'s fix order · 5 min

---

## What you need to know

### after/ replaces whole files

Put only changed files in `site/after/YOUR-DOMAIN/`, at the same path as in the snapshot.
Anything there replaces the snapshot's file, including a robots.txt you did not mean to change.

### The rules from week 4

Name the subject. Answer first. Facts early. Nothing under twelve words. Move facts, never
invent them: the test compares every number on a changed page with every number already
on your site.

### Make it real

If you can, ship the same changes to the real site today and write the date in `CHANGES.md`.
The thirty-day clock starts then.

---

## Exercises

```bash
pytest week-08/day-3 -v
```

Then `CHANGES.md`.

---

## Before you close the laptop

Commit, push, fill in the signal log.
