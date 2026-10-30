# Week 5 — Structured data and entities

> **Destination**
> You can read, validate and fact-check a page's JSON-LD by hand, find every place the
> web describes a company differently, and show with an experiment whether structured
> data changes what an engine cites, and say what that experiment cannot tell you.

Structured data is the second thing people reach for, and often the first. Google says
AI features have "no additional requirements"; vendors sell schema as the key to AI
answers. This week you test the claim on the two engines you can read, and find that
the most useful thing to check in markup is whether it is true.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Extract and validate JSON-LD, and catch markup that disagrees with its page (B) · mark up three Tidewell pages (S) |
| Tue | `day-2/` | Find every name, year and city the web gives a company (B) · write Tidewell's entity sheet (S) |
| Wed | `day-3/` | Run the experiment: with and without structured data, two engines (both) |
| Thu | `day-4/` | The structured-data module for the audit tool (B) · the structured-data audit (S) |
| Fri | `milestone/` | **B:** audit tool v2 · **S:** a recommendation the client can act on |

---

## The rule from this week on

**Valid is not true.** A validator checks shape. Check every fact in markup against the
page it sits on.

---

## Before Monday

Read the JSON-LD on three pages with
`python3 week-05/day-4/strategy/show_schema.py | head -40`.

---

## Outside-view question

> *A pharmacist reads the label, not the leaflet. What must be on the label, and what
> happens when the label and the leaflet disagree?*
