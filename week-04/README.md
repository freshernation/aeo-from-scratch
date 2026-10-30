# Week 4 — Content an engine can lift (Project 1)

> **Destination**
> You can rewrite a page so an engine can quote any passage of it alone, without
> inventing a fact, and show with a paired test that it helped on one engine and did not
> hurt on another. Builders finish an engine that crawls, boosts and cites; Strategists
> ship five rewritten pages.

Three weeks of measurement and access lead here, because this is the week everybody
wants to start with. Rewriting is now safe to measure: every crawler can read Tidewell,
the baseline has an interval, and there are two engines to check against. From this week
the course works on `aeolab.web2()`: the same web with week 3's access fixes applied,
plus the sites weeks 5 and 6 need.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Lint passages for the four problems that cost a quote (B) · rewrite the pitcher and shower pages (S) |
| Tue | `day-2/` | Extract the facts a passage carries (B) · rewrite the UX3 and RO-5 pages (S) |
| Wed | `day-3/` | Give your engine the panel's boosts, and see what that does (B) · restructure the FAQ (S) |
| Thu | `day-4/` | Measure a rewrite on any engine (B) · measure yours on two (S) |
| Fri | `milestone/` | **Project 1. B:** the complete engine and a three-engine report · **S:** five pages and the lift |

The Strategists' pages live in `week-04/snapshot/tidewell.example/`: copies of the five
pages as they are now. Edit them there.

---

## The rule from this week on

**Move facts, never invent them.** Every number in a rewrite must already be on
Tidewell's site. The tests check it. An answer engine will quote your sentence with
your name next to it.

---

## Before Monday

Read `aeolab/engine_b.py`'s docstring: the second engine, and how it differs from the
panel. Run `python3 -c "from aeolab import web2; from aeolab.panel import Panel; print(len(Panel(web2()).passages))"`.

---

## Outside-view question

> *Newspaper editors cut stories from the bottom to fit the page. How does knowing that
> change the way a reporter writes the first paragraph?*
