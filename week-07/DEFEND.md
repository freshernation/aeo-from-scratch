# Week 7 — Friday defence

Forty minutes. It starts with a log line on the board.

---

## Phase 0 — Read it (5 min)

The instructor writes one log line claiming to be OAI-SearchBot from an address the
student has not seen, and one with a ChatGPT referer. The student says what each is, how
they would verify the first, and what the second tells Tidewell, without running code.

## Phase 1 — Explain (10 min)

1. *"Why normalise URLs before counting citations?"* — the same page arrives as several
   strings; counting them separately inflates every number.
2. *"Perplexity has no price in the table. What does your budget code do, and why not
   treat it as free?"* — returns None; an unpriced engine has an unknown cost, not zero.
   The best question of the week.
3. *"Why did 31 August not alert, when the rate was still low?"* — the comparison is with
   the week before, which was already low; drift alerts on changes, not levels.
4. *"400 hits say GPTBot. Why are they not OpenAI?"*
5. *"Which of the panel's rules would you test first on a live engine, and how?"*

## Phase 2 — Mutate (10 min)

- *"Alert on the first-cited rate instead of cited."* (B) where in `drift`; (S) which
  week of the history would change.
- *"Run the monitor fortnightly."* What the plan gains and what it cannot see.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | (B) `normalise_url` keeps the fragment | the finding's 45 pages become 60-odd |
| Medium | (B) `cost_per_answer` treats a null price as 0 | Perplexity becomes free and the budget passes |
| Medium | (B) `verified` checks the GPTBot ranges for every bot | Claude's crawlers all become "spoofed" |
| Nasty | (B) `drift` compares every run with the first run, not the previous one | Nothing errors; on the history the drop alerts twice (24 and 31 August) and the fix on 7 September is reported as "no change" (3 up, 9 down, p = 0.146) |

The **Nasty** one: what you compare against decides what you can see. Ask the student
what the team would conclude on 7 September from each version.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Read it** | Both lines, and how to verify | One of the two | Trusts the user agent |
| **Explain** | Separates unknown from zero unprompted | With a nudge | Calls fixtures evidence |
| **Mutate** | Names every line before typing | Gets there | Cannot place the change |
| **Debug** | Suspects the silent one | Finds it | Guesses |

---

## Instructor: framing week 8

> **Everything so far was Tidewell.** Next week is a site you can change, with competitors
> nobody wrote up: thirty questions, a snapshot, an audit, three changes, a re-measure, and
> a date thirty days out when the live engines get their say.
