# Week 2 — Friday defence

Forty minutes. It starts with a run file the student has not seen.

---

## Phase 0 — Live (5 min)

The instructor makes a new run file from the panel with a seed the student has not
seen (`Panel().run(load_prompts(), 20, 0.3, seed=7)`, saved with `save_runs`). The
student runs their report against `baseline.jsonl` (B: `visibility.py`; S: their
`compare.py`) and says, before reading the p-value aloud, whether they expect a real change.

## Phase 1 — Explain (10 min)

1. *"Tidewell is cited in 73% of answers. Why is that not the number to lead with?"* —
   first-cited is 21.5%; 91 answers name Tidewell and cite someone else.
2. *"Wilson says 69% to 76%. Your bootstrap says 61% to 84%. Which do you report, and
   why are they different?"* — the 600 answers are 30 prompts asked 20 times; answers
   to one prompt move together; resampling prompts respects that. The best question of
   the week.
3. *"The baseline and fixed intervals overlap. Is the fix real?"* — yes: the paired
   test compares each prompt with itself and removes the between-prompt spread.
4. *"How many samples per prompt would you pay for?"* — one sample spans 63% to 83%;
   ten narrow it to 70%–77%; even fifteen do not reach five points. Past ten, pair the
   runs instead of buying samples.
5. *"Rerun: 9 better, 8 worse. What does that tell a client who asks 'did anything move'?"*

## Phase 2 — Mutate (10 min)

- *"Report share of voice against ClearFlow only, not all sites."* Which function
  changes and which stays.
- *"A prompt counts as a win only if it moved by at least 10 points."* Where the
  threshold goes, and what it does to ties and to p.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `first_rate` checks `domain in cited_domains[:2]` | The finding test's 21.5% fails |
| Medium | `wilson` uses `z*z/n` where it needs `z*z/(2n)` in the centre | Hand-computed test fails; the student explains the formula |
| Medium | `paired` passes the runs in the wrong order | Wins and losses swap; p is unchanged. Does the report say "worse"? |
| Nasty | `subsample` uses `rng.sample` (without replacement) instead of `rng.choices` | Nothing errors and the spread still shrinks with n, only faster: drawing 15 of the same 20 recorded answers makes 15 samples look nearly certain, and stable_at reports 10 at five points |

The **Nasty** one: sampling with and without replacement both look like "random
samples". The question is what a fresh run would do, and a fresh run draws new answers;
only knowing that catches it. The author of this course made this exact mistake first.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Live** | Predicts the verdict and explains the prediction | Reads the verdict correctly | Reads p backwards |
| **Explain** | Explains clustering without the word "cluster" | Says "prompts" with a nudge | Defends the narrow interval |
| **Mutate** | Names every line before typing | Gets there | Cannot place the change |
| **Debug** | Suspects the silent one | Finds it | Guesses |

---

## Instructor: framing week 3

> **The fix you measured on Friday was one line of robots.txt.** Next week you find
> every other way Tidewell is invisible: a noindex in an HTTP header, a page that only
> exists after JavaScript runs, and a CDN that refuses Claude's and Perplexity's
> crawlers while robots.txt welcomes them.
