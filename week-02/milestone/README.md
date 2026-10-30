# Week 2 Milestone — A report that says whether a change was real

> One command (B) or one document (S) that reports Tidewell's visibility with its
> interval, and says whether a second run differs by more than noise.

---

## Builders — `build/`

| File | Where it comes from |
|---|---|
| `metrics.py`, `sampling.py`, `stats.py`, `report.py` | **copy** from this week's days |
| `stability_check.py` | given |
| `visibility.py` | new: `build()` and a command line around `report()` and `paired()` |

```bash
python3 week-02/milestone/build/visibility.py fixed.jsonl --against baseline.jsonl
```

## Strategists — `strategy/`

| File | Where it comes from |
|---|---|
| `VISIBILITY_REPORT.md` | new: baseline, rerun and fixed, compared |

| Section | What goes in it |
|---|---|
| Summary | What changed, in two or three sentences |
| The three runs | Each run's rate and interval |
| Rerun against baseline | Wins, losses, ties, p |
| Fixed against baseline | The same |
| Decision | Which is noise, which is real, and what next |

---

## Check it

```bash
pytest week-02/milestone/build -v       # or
pytest week-02/milestone/strategy -v
```

## Friday

The instructor makes a run file with a seed you have not seen. You compare it with the
baseline and say whether anything changed, before reading p aloud. See `DEFEND.md`.
