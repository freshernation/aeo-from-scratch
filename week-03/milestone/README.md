# Week 3 Milestone — The audit tool, and the fix

> **Builders** ship `aeo_audit.py` version 1: one command, every page against every
> crawler, and the sitemap. **Strategists** fix a copy of Tidewell's site and show,
> with the panel and last week's paired test, that the fix is real.

---

## Builders — `build/`

| File | Where it comes from |
|---|---|
| `robots.py`, `fetchcheck.py`, `sitemap.py`, `access.py` | **copy** from this week's days |
| `aeo_audit.py` | new: `audit()`, `render()`, and a command line |

```bash
python3 week-03/milestone/build/aeo_audit.py tidewell.example
python3 week-03/milestone/build/aeo_audit.py tidewell.example --web week-03/milestone/strategy/snapshot
```

The second command audits the Strategists' fixed copy. Weeks 5 and 6 add modules to
this tool; week 8 points it at your own site.

## Strategists — `strategy/`

| File | Where it comes from |
|---|---|
| `snapshot/tidewell.example/` | a copy of Tidewell's site: **fix it here**, never in `aeolab/web/` |
| `FIXES.md` | new |

| Section | What goes in it |
|---|---|
| Summary | What you changed and what it did |
| What I fixed | One table row per change |
| What I left alone | The deliberate things, and why |
| Training crawlers | `GPTBot: allow` or `block`, and the other two |
| The lift | Citation rate, first-cited rate, the paired result |
| What this does not prove | At least two limits |

---

## Check it

```bash
pytest week-03/milestone/build -v       # or
pytest week-03/milestone/strategy -v
```

The Strategists' last test runs the panel on your snapshot, 600 answers, and needs a
real lift: above 80% cited and at least 15 prompts up.

## Friday

The instructor plants one fault you have not seen in an overlay folder. You find it
with your tool before reading any code. See `DEFEND.md`.
