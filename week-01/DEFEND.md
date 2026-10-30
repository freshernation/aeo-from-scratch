# Week 1 — Friday defence

Forty minutes. It starts at the whiteboard, with no laptop.

---

## Phase 0 — Draw (5 min)

Draw the seven steps from prompt to cited answer, from memory. Then the instructor
names a prompt (say P10, the UX3's price) and the student marks the step where
Tidewell's own page was lost, and says how they know.

## Phase 1 — Explain (10 min)

1. *"Why passages and not pages?"* — an engine quotes a span; one page answers several
   questions; a heading is where one answer stops.
2. *"P10 cites a review saying $149 when Tidewell charges $189. Which step failed?"* —
   the crawl: the UX3 page is noindexed, so the only page about its price is a third
   party's, old. The best question of the week: it separates a content problem from an
   access problem.
3. *"What does fan-out change, and what does it not?"* — it moves the winner on 12 of
   30 prompts but adds Tidewell's best page to the top 4 on only one more prompt.
4. *(B)* *"Your engine cites Tidewell's best page on 20 prompts, the panel on 10. Why?"*
   — yours reads every page on disk; the panel crawls, and robots.txt, a noindex and a
   JavaScript page hide Tidewell's best pages. *(S)* *"Brand prompts: 7 of 7 cited.
   Why is that the misleading number?"* — Tidewell is cited through its about or
   returns page while a third party gives the answer.
5. *"Word overlap caught 1 of 4 invented claims at 0.5. Raise the threshold and it
   catches 4. Is the problem solved?"* — no: overlap says the words are present, not
   that the claim is true; it also flags a true "No." at every threshold.

## Phase 2 — Mutate (10 min)

- *"Cite three passages, not four."* (B) the `k` default and nothing else; (S) which
  of your ten traced prompts would lose Tidewell entirely — name them from the trace.
- *"A passage now starts at h2 only; h3 joins its parent."* (B) the heading condition
  in `split_passages`; predict what happens to the 104. (S) which checklist scores
  change, and why "right_length" is the one that moves.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | (B) `tokenize` stops stripping plurals | "filters" no longer matches "filter"; BM25 test fails loudly |
| Medium | (B) `avgdl` computed over unique tokens | scores shift; the hand-computed test catches it |
| Medium | (S) `classify` checks "tidewell" before " vs " | P07 becomes brand; accuracy drops to 29/30 |
| Nasty | (B) `rrf` counts rank from 0, (S) `gaps` does not skip the first search | Nothing errors when the engine runs: (B) every score shifts slightly and the top results barely move; (S) the prompt itself is counted as a search and the gap count quietly grows |

The **Nasty** one: an off-by-one in a ranking formula changes almost nothing you can see
in the output. Only a hand-computed expected value catches it, which is why every day's
tests include one. Ask the student which test would have caught it.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Draw** | Seven steps, and the right step for P10 with the evidence | Steps right, P10 placed at retrieval or scoring | Cannot draw the pipeline |
| **Explain** | Separates access losses from content losses unprompted | Gets there with a nudge | Talks about "AI quality" |
| **Mutate** | Names every line before typing | Gets there | Cannot place the change |
| **Debug** | Suspects the silent one | Finds it | Guesses |

---

## Instructor: framing week 2

> **Run the panel again and the answer changes.** At temperature 0.3 the same prompt
> cites different pages on different runs, as live engines do. Next week we find out
> how many runs a number needs before you can believe it, and the answer is more than
> any one-off screenshot of ChatGPT.
