# Week 5 Milestone — Audit tool v2, and a recommendation

> **Builders** add structured data and entity checks to `aeo_audit.py`. **Strategists**
> keep their markup true and tell the client what structured data is worth.

---

## Builders — `build/`

| File | Where it comes from |
|---|---|
| `robots.py`, `fetchcheck.py`, `sitemap.py`, `access.py` | **copy** from week 3's milestone |
| `jsonld.py`, `entities.py`, `schema.py` | **copy** from this week |
| `aeo_audit.py` | week 3's, with the changes listed in the stub |

```bash
python3 week-05/milestone/build/aeo_audit.py tidewell.example --web aeolab/web2
```

## Strategists — `strategy/`

| File | Where it comes from |
|---|---|
| `week-05/snapshot/tidewell.example/` | your markup from day 1, still true |
| `RECOMMENDATION.md` | new |

| Section | What goes in it |
|---|---|
| The question | What the client asked |
| What we measured | The experiment and its result |
| What Google says | With the quotation |
| What it is still worth | Reasons that do not depend on citations, and the risk of wrong markup |
| Recommendation | What to do, how long, what not to promise |

---

## Check it

```bash
pytest week-05/milestone/build -v       # or
pytest week-05/milestone/strategy -v
```

## Friday

The defence starts with a JSON-LD block and its page on paper. See `DEFEND.md`.
