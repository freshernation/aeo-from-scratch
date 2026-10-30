# Week 7 Milestone — A monitor, and the plan

> **Builders** ship `monitor.py`: one command that checks the budget, runs the engines,
> stores the run and alerts on drift. **Strategists** ship the monitoring plan.

---

## Builders — `build/`

| File | Where it comes from |
|---|---|
| `adapters.py`, `budget.py`, `store.py` | **copy** from this week |
| `metrics.py`, `sampling.py`, `stats.py` | **copy** from week 2's milestone |
| `monitor.py` | new |

```bash
python3 week-07/milestone/build/monitor.py monitor.json --date 2026-11-02
```

A config names the prompts, engines, samples, budget, store and prices. Live engines go
through `aeolab/live.py`; the tests use a fake.

## Strategists — `strategy/`

| File | Where it comes from |
|---|---|
| `MONITORING_PLAN.md` | new: what, how often, cost, alerts and who acts, what a person checks |

---

## Check it

```bash
pytest week-07/milestone/build -v       # or
pytest week-07/milestone/strategy -v
```

## Friday

The defence starts with two log lines on the board. See `DEFEND.md`.
