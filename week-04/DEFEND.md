# Week 4 — Friday defence (Project 1)

Forty minutes. It starts with a passage the student has not seen.

---

## Phase 0 — Rewrite live (5 min)

The instructor pastes one passage from a competitor or a third party (for example
WaterForum's PFAS answer) and the student rewrites it aloud as if it were Tidewell's:
named subject, answer first, a fact from the page, nothing invented. Then they say which
panel rule each change answers.

## Phase 1 — Explain (10 min)

1. *"The rewrite moved the panel 20 points on first-cited and Engine B 3. Why ship?"* —
   it did not hurt B; it targeted rules, not one engine's quirks; the best question of
   the week.
2. *"The keyword-stuffed page got cited more. Why not do that?"* — the answer then
   quotes a string of keywords; cited and useful differ; and it was no clear change.
3. *"Why is 'six months' not a fact to your extractor, and does it matter?"*
4. *(B)* *"You added the panel's boosts and your engine agreed with it less. Why?"* —
   boosts reorder candidates; the candidates come from BM25 over different passages.
   *(S)* *"Which of your changes did the 12-word floor force, and is the floor real?"* —
   a course assumption, marked as such in the panel's docstring.
5. *"Name a prompt your rewrite lost, and the step."*

## Phase 2 — Mutate (10 min)

- *"The panel now cites three passages, not four."* Which of your pages lose most? (B:
  where in the engine; S: which prompts, from the trace.)
- *"Tidewell's legal team forbids naming competitors."* What changes in which page?

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | (B) `lint_passage` checks the pronoun after stripping only "." | "It," passes as clean |
| Medium | (B) `extract_facts` keeps overlapping matches | "$2026" yields a price and a year; the hand-written test with "$189 ... 2016" still passes, so ask for an input that shows it |
| Medium | (S) a rewrite adds "rated 4.8 stars" | the honesty test names 4.8 |
| Nasty | (B) `lift` uses a different seed for after than before | Nothing errors; every rewrite shows a few extra wins and losses of pure noise, and a small real change can flip verdict |

The **Nasty** one: comparing two runs with different random seeds adds noise that is
not the change. Same seed for both is common random numbers; it is why the panel's
noise is keyed by seed, sample and prompt.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Rewrite live** | Answer first, nothing invented, rules named | Good rewrite, rules vague | Adds a fact |
| **Explain** | Separates "cited" from "useful" unprompted | With a nudge | Optimises for the panel only |
| **Mutate** | Names every line or page before typing | Gets there | Cannot place the change |
| **Debug** | Suspects the silent one | Finds it | Guesses |

---

## Instructor: framing week 5

> **Tidewell's pitcher page now says $34 everywhere a reader looks, and $29 in the one
> place a machine reads.** Next week is structured data: what it is, whether the panel
> reads it (it does not, mostly), and why a wrong price in it is still a problem.
