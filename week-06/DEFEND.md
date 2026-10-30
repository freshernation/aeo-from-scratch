# Week 6 — Friday defence (Project 2)

Forty minutes. It starts with the audit run on a site the student did not prepare.

---

## Phase 0 — Live (5 min)

B: run `aeo_audit.py clearflow.example --web aeolab/web2 --brand ClearFlow` and read the
"Fix first" list aloud, saying which items are real. S: read ClearFlow's pages with the
day 1 and day 3 scripts (edit the brand in one line) and name ClearFlow's single biggest
off-site risk.

## Phase 1 — Explain (10 min)

1. *"Your finder reports four UX3 prices. How many are contradictions?"* — one ($149
   against $189); $59 is a cartridge set, $150 is "under $150". The best question of the
   week.
2. *"The panel quotes $149 first for 'Which Tidewell filter should I buy?'. Which steps
   let a stale page win a brand prompt?"* — the compare page was not retrieved; the review
   is answer-first and specific; the 0.85 freshness penalty was not enough.
3. *"Why does the hidden text win AquaMinder a citation but not a quoted instruction?"* —
   the hidden keywords help retrieval; the panel quotes the passage's first sentence,
   which is visible.
4. *"After week 3, no Tidewell loss is 'not-crawled'. What does that tell you about where
   to spend next?"*
5. *"What would you say to a client who asks you to copy AquaMinder's trick?"*

## Phase 2 — Mutate (10 min)

- *"Stale now means one year, not two."* (B) one argument; (S) which pages join the list.
- *"Report only contradictions where Tidewell's own site states one of the values."* (B)
  where in `fix_first`; (S) which row of the table goes.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | (B) `mentions` counts Tidewell's own domain | Tidewell "mentions" itself dozens of times |
| Medium | (B) `hidden_text` checks only `display:none` with no space | `DISPLAY: none` is missed |
| Medium | (B) `attribute` checks retrieval before crawling | on the original web, P03 becomes "not-retrieved" instead of "not-crawled": the right fix (robots.txt) is hidden behind the wrong one |
| Nasty | (B) `cloaked` fetches both versions as the same user agent | Nothing errors; every page has similarity 1.0 and the tool reports no cloaking anywhere, which looks like good news |

The **Nasty** one: a detector that can never fire looks exactly like a clean web. Every
detector needs one known positive in its tests; ask which test is that for each of theirs.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Live** | Reads the list and says which items are real | Reads it | Treats every finding as true |
| **Explain** | Separates candidates from contradictions unprompted | With a nudge | Trusts the finder |
| **Mutate** | Names every line before typing | Gets there | Cannot place the change |
| **Debug** | Suspects the silent one | Finds it | Guesses |

---

## Instructor: framing week 7

> **Everything so far was measured on engines we built.** Next week the same thirty
> prompts go to Claude, ChatGPT and Perplexity with their search tools on: what they cite,
> what it costs, how it drifts, and what the server logs say about who actually came.
