# Week 6 Milestone — Project 2: the audit

> **Builders** ship `aeo_audit.py` v3: access, structured data, entity, off-site,
> manipulation and lost prompts, with one numbered fix list. **Strategists** ship the
> audit report Tidewell's leadership will act on.

---

## Builders — `build/`

| File | Where it comes from |
|---|---|
| `robots.py`, `fetchcheck.py`, `sitemap.py`, `access.py` | **copy** from week 3 |
| `jsonld.py`, `entities.py`, `schema.py` | **copy** from week 5 |
| `facts.py` | **copy** from week 4 day 2 |
| `corroborate.py`, `contradict.py`, `offsite.py`, `attribution.py` | **copy** from this week |
| `aeo_audit.py` | week 5's, with the changes in the stub |

```bash
python3 week-06/milestone/build/aeo_audit.py tidewell.example --web aeolab/web2 \
    --fact "UX3:price" --fact "Tidewell Pitcher:volume:cartridge" \
    --prompts aeolab/prompts.csv --prompts aeolab/prompts_more.csv
```

## Strategists — `strategy/`

| File | Where it comes from |
|---|---|
| `AUDIT_REPORT.md` | new: everything since week 1, with a fix order |

| Section | What goes in it |
|---|---|
| Summary | Five sentences |
| Access, Content, Structured data | What each week found, fixed and measured |
| Off-site | Mentions, contradictions, stale pages, the entity |
| Competitors' tactics | What you found and what Tidewell does about it |
| Fix order | At least eight, most valuable first, each with its evidence |
| What we will measure next | What week 7 must check live |

---

## Check it

```bash
pytest week-06/milestone/build -v       # or
pytest week-06/milestone/strategy -v
```

## Friday

The defence runs the audit on ClearFlow, which nobody prepared for. See `DEFEND.md`.
