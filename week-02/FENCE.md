# Week 2 — Concept fence

## Allowed

**Everything from week 1**, plus:

- Run files; `aeolab.load_runs`; citation rate, first-cited rate, share of voice,
  mention rate, mentioned-not-cited
- Samples per prompt; spread by subsampling; unstable prompts
- Wilson interval; bootstrap over prompts (B); exact sign test, paired by prompt
- `random.Random(seed)`, `math.comb`, `argparse` (B milestone)

## Not yet

Changing the web (week 3 onward) · running the panel to make new run files (week 3) ·
t-tests, regression, Bayesian methods (cut) · live engines (week 7)

---

## Why the sign test and not a t-test

A t-test on 30 per-prompt differences would work, and it assumes the differences are
roughly normal. Many of these prompts sit at 0% or 100%, so they are not. The sign test
asks only "did this prompt go up or down", fits on one line, and a client can follow it.
It throws information away; that is the price of an argument nobody can pick apart.
