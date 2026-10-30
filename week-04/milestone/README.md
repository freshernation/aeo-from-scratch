# Week 4 Milestone — Project 1

> **Builders** ship the engine, complete, and a report comparing three engines.
> **Strategists** ship five rewritten pages and the measured lift on two engines.

---

## Builders — `build/`

| File | Where it comes from |
|---|---|
| `passages.py`, `bm25.py`, `cite.py`, `fanout.py` | **copy** from week 1's milestone |
| `robots.py`, `fetchcheck.py`, `sitemap.py` | **copy** from week 3's milestone |
| `boosts.py`, `compare.py` | **copy** from this week |
| `metrics.py`, `sampling.py`, `stats.py` | **copy** from week 2's milestone (for `compare.py`) |
| `engine2.py` | new: `crawl()` and `Engine` with `answer()` and `run()` |
| `mine/tidewell.example/learn/lead-in-water.html` | rewrite it, under the Strategists' rules |
| `ENGINE_REPORT.md` | new: three engines, the fixtures, your rewrite, what your engine gets wrong |

## Strategists — `strategy/`

| File | Where it comes from |
|---|---|
| `week-04/snapshot/tidewell.example/` | your five pages, finished |
| `PROJECT1.md` | new |

| Section | What goes in it |
|---|---|
| Summary | What you changed and what it did |
| The five pages | Page, main change, prompts it is for |
| The numbers | Both engines, before and after, paired |
| Two engines | Why the lift differs, and why you would ship |
| What I would not claim | Three things this does not show |

---

## Check it

```bash
pytest week-04/milestone/build -v       # or
pytest week-04/milestone/strategy -v
```

The Strategists' tests run 2,400 answers across two engines. Allow a minute.

## Friday

The defence starts with a passage you have not seen, rewritten aloud. See `DEFEND.md`.
