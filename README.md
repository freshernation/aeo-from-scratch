# AEO From Scratch

Eight weeks from "I know SEO" or "I can build retrieval" to measuring, fixing and
defending a site's visibility in AI answer engines, with numbers.

Answer engines (ChatGPT search, Claude with web search, Perplexity, Google's AI Mode)
do not rank ten links. They rewrite your question into several searches, pull passages
from a handful of pages, write an answer and cite some of them. Getting cited is a
different job from ranking, and most advice about it is untested. This course builds
an answer engine you can read, measures against it, and only then changes content,
then checks on live engines which of the lessons hold.

---

## Who this is for

Two kinds of advanced student, in two tracks through the same weeks:

| Track | You arrive with | You leave with |
|---|---|---|
| **Builder** | You finished *Retrieval Under Test*, or can build a BM25 retriever and an eval set | An answer engine, an audit tool and a monitor you wrote |
| **Strategist** | You have run SEO for real sites (technical audits, schema, Search Console) and can write a Python function with a loop and a dict | A measured rewrite, an audit report with a fix order, and a case study on your own site |

Both tracks share the day's reading, the live hour, the milestone theme and the Friday
defence. Each day folder has a `build/` lab and a `strategy/` lab: do the one for your
track. Doing both is allowed and slow.

Before week 1 you run a short baseline interview so that you, and your instructor,
know which gaps to watch.

---

## The rules

**1. The twenty-minute rule.** Stuck for twenty minutes: open the tutor. Still stuck:
bring it to the live hour. Log every stuck moment in `logs/stuck-log.md`.

**2. You may not commit a line you could not have written and cannot explain on
Friday.**

**3. Nothing counts until the tests pass and it is pushed.**

**4. No change without a measured delta, and no claim about a real engine you have not
checked.** "This should help AI visibility" is an opinion. "Tidewell's citation rate
went from 0.73 to 0.84 over 600 samples, paired by prompt" is a result.

---

## The eight weeks

| Week | | Milestone |
|---|---|---|
| 1 | [How an answer engine answers](week-01/README.md) | Builder: an engine that answers and cites. Strategist: a labelled prompt set and a gap map |
| 2 | [Measure before you change](week-02/README.md) | A visibility report with confidence intervals |
| 3 | [Can it read you?](week-03/README.md) | Audit tool v1: every page against every AI crawler |
| 4 | [**Content an engine can lift**](week-04/README.md) | **Project 1**: the engine, and five rewritten pages that win on two engines |
| 5 | [Structured data and entities](week-05/README.md) | Audit tool v2, with schema · a recommendation on what markup is worth |
| 6 | [**Off-site: authority, consistency, freshness**](week-06/README.md) | **Project 2**: the audit tool, one command, one report · the audit report |
| 7 | [Live engines and monitoring](week-07/README.md) | Builder: a monitor with budgets and drift alerts. Strategist: a monitoring plan |
| 8 | [**Your own site**](week-08/README.md) | **Project 3**: a case study, defended, and a mock interview |

Every test runs offline. The web the course works on is in `aeolab/web/`: a water-filter
maker called Tidewell, three competitors, a review site, a forum and a news site, all
invented. No account or key is needed until week 7, and even then the tests use a
scripted fake; a key is only for the optional live runs.

---

## How a week works

| | |
|---|---|
| **Monday to Thursday** | One live hour, then the day's folder: read, build, make the tests pass |
| **Friday** | No new content. Ship the milestone, then defend it |

Run a day's tests with `pytest week-NN/day-N/build -v` or `pytest week-NN/day-N/strategy -v`.

---

## What is in the repo

| Path | What it is |
|---|---|
| `aeolab/` | Given code: the offline web, the scripted model, and **the panel**, the answer engine you measure against |
| `aeolab/web/` | The seeded sites, as HTML |
| `aeolab/web2/` | The web from week 4: week 3's access fixes, structured data, and more sites. `aeolab.web2()` |
| `aeolab/engine_b.py` | A second answer engine, from week 4, built to disagree with the panel |
| `aeolab/live.py` | Week 7: asks Claude, ChatGPT and Perplexity with web search on (your keys; never called by the tests) |
| `aeolab/snapshot.py` | Week 8: a polite crawler that copies your site into the offline web's format |
| `aeolab/prompts.csv` | The course prompt set: 30 questions a Tidewell customer might ask (six more in `prompts_more.csv`, from week 5) |
| `aeolab/runs/` | Recorded panel runs, for week 2 |
| `week-01/` … | One folder per week |
| `ai/` | The AI roles. Read `ai/README.md` first |
| `logs/` | Your baseline, your stuck log and your signal log |
| `SETUP.md` | Day zero |
| `CUT_LIST.md` | What this course does not teach, and why |
| `SOURCES.md` | What to read, and what to ignore |

Start with `SETUP.md`.
