# Week 5 — Concept fence

## Allowed

**Everything from weeks 1 to 4**, plus:

- JSON-LD: `@context`, `@type`, `@graph`, nesting; `json`
- schema.org types Product, Offer, Organization, FAQPage, Question, Answer, Article
- The course's minimum required properties (a subset of Google's, said as such)
- `sameAs`; an entity's name, founding year and city across sites
- An experiment with and without a change, on two engines, same seed

## Not yet

Fixing other sites' pages (week 6) · freshness and manipulation (week 6) · live engines
(week 7) · microdata and RDFa (cut: JSON-LD is what the vendors document) · schema
libraries and validators (you write the check)

---

## Why no validator library

A validator tells you markup is well formed. The most expensive fault on this web, a
$29 price on a $34 page, passes every validator. Writing your own check means you decide
what "correct" includes, and "matches the page" is the part libraries leave out.
