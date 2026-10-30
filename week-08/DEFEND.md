# Week 8 — Friday: Project 3 defence and mock interview

Ninety minutes in all: forty for the defence, fifty for the mock interview
(`ai/interviewer.md`, run by the instructor, not a chat window).

---

## Phase 0 — Live (5 min)

The student runs `python3 week-08/measure.py` on their site in front of the instructor
and reads the panel's first-cited rates aloud before opening `CASE_STUDY.md`.

## Phase 1 — Explain (10 min)

1. *"Which of your thirty prompts did you lose at which step, before you changed anything?"*
   — the week 1 rule, on their own site. The best question of the course.
2. *"Your cited rate went up a lot. What is it about?"* — the size of the snapshot; first-cited
   and paired results are the evidence.
3. *"Which change would you undo if you could keep only two, and why?"*
4. *"What would the live re-measure have to show for you to say this did not work?"*
5. *"What does your audit get wrong about your site?"* (for example a brand that is a
   common word, or a CDN rule the snapshot cannot see)

## Phase 2 — Mutate (10 min)

- *"The client will not let you touch robots.txt."* What is left, and what do you expect it to move?
- *"Add a fourth competitor that answers everything answer-first."* What happens to your
  numbers, and which do you still trust?

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | a best_url with `http://` where the snapshot is `https://` | that prompt can never be "cited"; best_pages drops |
| Medium | a changed page saved at a different path in `after/` | the overlay adds a new page instead of replacing one |
| Medium | fanout.json keys that differ from the prompts by one character | the searches silently never run |
| Nasty | `after/` contains an unchanged robots.txt copied from the live site after a redeploy | Nothing errors and the numbers look plausible; the snapshot's robots.txt is replaced by a different one and part of the "lift" is not the student's change |

The **Nasty** one: an overlay replaces whole files. Anything in `after/` is a change,
whether you meant it or not. Ask the student to list every file in `after/` and say why
each is there.

---

## Mock interview (50 min)

Run `ai/interviewer.md` yourself: design (25), debug a loss (20), judgement (15). Score it
with its SIGNAL block. The student's `INTERVIEW.md` shows two rehearsals; compare.

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Live** | Reads the numbers and says what they are about | Reads them | Leads with the cited rate |
| **Explain** | Attributes every loss to a step | Most of them | "The content was weak" |
| **Mutate** | Plans the change and predicts the effect | Plans it | Cannot place it |
| **Debug** | Suspects the silent one | Finds it | Guesses |
| **Interview** | Hire | Not yet, one phase weak | Not yet |
