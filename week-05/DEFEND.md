# Week 5 — Friday defence

Forty minutes. It starts with a JSON-LD block on paper.

---

## Phase 0 — Read it (5 min)

The instructor shows a Product block and its page side by side, with one fault planted
(a currency missing, a price that differs, a sameAs to a page that says something else).
The student finds it without running anything, then runs their tool to confirm.

## Phase 1 — Explain (10 min)

1. *"Removing all structured data changed 0 of 600 answers on both engines. What does
   that prove?"* — that these two engines ignore it, which their source already showed;
   nothing about live engines. The best question of the week.
2. *"Then why fix the pitcher's markup?"* — it is false; anything that trusts markup
   repeats $29; rich results in ordinary search still use it.
3. *"Why split into paragraphs, not sentences, to find 'founded in'?"* — "Co." and "Inc."
   end a sentence and cut the brand off its claim.
4. *"What can sameAs fix, and what can it not?"*
5. *"The directory says Seattle. Which engine step lets that into an answer?"* — retrieval
   finds it; nothing scores truth; the answer quotes it next to Portland.

## Phase 2 — Mutate (10 min)

- *"Treat a Product without a brand as a problem."* (B) one line in REQUIRED; (S) which
  of the nine pages now fail.
- *"Prices may be written '34 USD' on the page."* (B) where `mismatches` changes; (S) what
  the audit would have reported wrongly.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | (B) `extract` ignores `@graph` | the test's graph nodes vanish |
| Medium | (B) `mismatches` does not drop ".00" | every correct price is reported as a mismatch |
| Medium | (B) `name_forms` drops the lookahead | "tidewell" appears as a form, from a link |
| Nasty | (B) `validate` does not recurse into a list of offers | Nothing errors, and every test with a single offer passes; a Product with two offers, one without a price, is reported clean |

The **Nasty** one: JSON-LD lets most properties be one thing or a list. Code that handles
one shape passes on every page that happens to use it.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Read it** | Finds the fault by eye, then confirms | Finds it with the tool | Calls it valid |
| **Explain** | Says what the experiment cannot show, unprompted | With a nudge | "Schema doesn't matter" |
| **Mutate** | Names every line before typing | Gets there | Cannot place the change |
| **Debug** | Suspects the silent one | Finds it | Guesses |

---

## Instructor: framing week 6

> **Tidewell has fixed everything it controls.** Next week is everything it does not:
> a review site quoting a price two years old, a forum post with a cartridge life from
> 2023, a directory in the wrong city, and a competitor's page with instructions hidden
> for AI assistants. Project 2 is the audit that finds all of it.
