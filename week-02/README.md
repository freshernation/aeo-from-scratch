# Week 2 — Measure before you change

> **Destination**
> Given any run file, you can report a site's citation rate with an interval that
> resamples prompts, and say whether a second run differs from the first by more than
> noise, with a paired test and its p-value.

Every later week claims "this change helped". This week makes that claim mean
something. Answer engines do not give the same answer twice, and most AEO reporting is
a screenshot, a sample of one. By Friday you will know how wrong a sample of one is,
and why the obvious interval is three times too confident.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Compute citation rate, first-cited rate, share of voice and mentions (both tracks) |
| Tue | `day-2/` | Show how the number moves with the sample count (B) · find the unstable prompts (S) |
| Wed | `day-3/` | Wilson and bootstrap intervals, and a paired sign test (B) · interval and sign test (S) |
| Thu | `day-4/` | Generate the baseline report (B) · write it for a client (S) |
| Fri | `milestone/` | A visibility report that says whether a change was real |

The run files are in `aeolab/runs/`: the panel at temperature 0.3, 30 prompts, 20
samples each. `baseline` is the web as it is, `rerun` the same web again, and `fixed`
the web with one robots.txt line removed. You will meet that line properly next week.

---

## The rule from this week on

**No number without its denominator, its interval and its run file.** "73%" is not a
result. "73% of 600 answers, 61% to 84% over prompts, baseline.jsonl" is.

---

## Before Monday

Nothing to install. Look at one line of `aeolab/runs/baseline.jsonl` and say what each
field is.

---

## Outside-view question

> *A pollster calls a thousand people, not ten. How did they choose a thousand, and
> what do they do when the people in one town all answer alike?*
