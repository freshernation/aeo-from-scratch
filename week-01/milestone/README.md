# Week 1 Milestone — An engine, and a prompt set

> **Builders** ship an answer engine that answers and cites. **Strategists** ship a
> 40-prompt set and the first picture of where Tidewell is cited.

---

## Builders — `build/`

| File | Where it comes from |
|---|---|
| `passages.py` | **copy** from day 1 |
| `bm25.py` | **copy** from day 2 |
| `cite.py` | **copy** from day 3 |
| `fanout.py` | **copy** from day 4 |
| `engine.py` | new: the four joined into `Engine(pages).answer(query)` |

The last test compares your engine with the panel on all thirty prompts. Expect a
surprise about Tidewell's best pages, and be ready to explain it on Friday.

## Strategists — `strategy/`

| File | Where it comes from |
|---|---|
| `prompts_plus.csv` | `aeolab/prompts.csv` plus your ten from day 2, as N01..N10, with a `best_url` each |
| `PROMPT_SET.md` | new |

### `PROMPT_SET.md`

| Section | What goes in it |
|---|---|
| The prompt set | How many, which intents, and why those |
| Where Tidewell is cited | The panel's numbers, by intent |
| The gaps | Day 4's gaps, plus any your new prompts expose |
| What I will measure next week | Three questions, each a number |

---

## Check it

```bash
pytest week-01/milestone/build -v       # or
pytest week-01/milestone/strategy -v
```

## Friday

The defence starts at the whiteboard: the seven steps from memory, then one prompt the
instructor picks, and the step where Tidewell lost it. See `DEFEND.md`.
