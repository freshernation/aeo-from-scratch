# Week 8 — Concept fence

## Allowed

**Everything from weeks 1 to 7**, plus:

- `aeolab.snapshot` (a polite crawler for your own site and a few others)
- `FakeWeb(root=...)` on your snapshot; `week-08/measure.py`; `week-08/audit_site.py`
- Your own week 6 audit tool and week 7 monitor (Builders)
- `ai/advisor.md` week 8 mode and `ai/interviewer.md`

## Not yet

Ever: snapshotting a site whose robots.txt says no, committing other sites' pages
(`site/snapshot/` is ignored by git), inventing a fact on your own site, using any of
week 6's manipulation tactics.

---

## Why a snapshot and not the live site

Live engines take days or weeks to re-read a site. A snapshot lets you measure a change
the same day, on two engines you can read, and leaves the live engines a fair test thirty
days later. The snapshot answers "did the change do what we meant?"; the live check answers
"did it matter out there?". Week 8 answers the first and books the second.
