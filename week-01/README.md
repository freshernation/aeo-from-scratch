# Week 1 — How an answer engine answers

> **Destination**
> You can draw the seven steps an answer engine takes from prompt to cited answer, and
> for any of the thirty course prompts point to the step where Tidewell's best page was
> lost. Builders have an engine that answers and cites; Strategists have a labelled
> prompt set and a gap map.

Nothing can be optimised that cannot be drawn. Most AEO advice skips this week and goes
straight to "write in a Q&A format". By Friday you will know why that advice sometimes
works, and that on this web half of Tidewell's losses have nothing to do with how its
pages are written.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Split a page into passages (B) · read the panel's trace for ten prompts (S) |
| Tue | `day-2/` | Score passages with BM25 by hand (B) · classify prompts by intent (S) |
| Wed | `day-3/` | Attribute each answer sentence to a passage (B) · score passages on a quotability checklist (S) |
| Thu | `day-4/` | Fan a query out and fuse the results (B) · find the searches Tidewell has no answer for (S) |
| Fri | `milestone/` | **B:** an engine that answers and cites · **S:** a 40-prompt set and where Tidewell is cited |

B = `build/`, S = `strategy/`. Do your track's folder. Read every day's README; both
tracks share the ideas.

---

## The rule from this week on

**Draw it before you change it.** Before you touch any page or any code, draw the seven
steps and mark the one you think failed. A fix at step 6 for a failure at step 1 is
the most common mistake in this field.

---

## Before Monday

Run `python3 -c "from aeolab.panel import Panel; print(Panel().ask('Do water filters remove lead?').sentences)"`
and read the docstring at the top of `aeolab/panel.py`. Nothing else to set up.

---

## Outside-view question

> *A reference librarian hands you one book, not ten. What did they check before they
> chose it, and what would make them hand you the wrong one?*
