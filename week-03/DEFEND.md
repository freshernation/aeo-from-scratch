# Week 3 — Friday defence

Forty minutes. It starts with a site the student has not audited.

---

## Phase 0 — Live (5 min)

The instructor makes an overlay folder with one fault the student has not seen (for
example `_server.json` with `{"headers": {"/faq": {"X-Robots-Tag": "noindex, nofollow"}}}`,
or a robots.txt with `Disallow: /*?` and `Allow: /filters/`). B: run `aeo_audit.py
tidewell.example --web DIR`. S: run `view_as_bot.py` and `show_access.py` against it
(set the overlay in a one-line change). Find the fault before reading the code.

## Phase 1 — Explain (10 min)

1. *"robots.txt allows Claude-SearchBot. Why can it read none of Tidewell's pages?"* —
   the server refuses it with a 403, robots.txt included; robots.txt is a request, the
   server is the door. The best question of the week.
2. *"Why are the /learn/guides/ pages readable when /learn/ is disallowed?"* — RFC 9309,
   longest match; a first-match parser (Python's) blocks them.
3. *"Why must you never block a noindexed page in robots.txt?"* — the crawler never
   fetches it, so it never sees the noindex.
4. *"The comparison page shows a table in your browser. What does a crawler get?"*
5. *"Blocking GPTBot: what does it cost Tidewell in answer engines? And Google-Extended?"*
   — GPTBot: nothing in ChatGPT search, which uses OAI-SearchBot. Google-Extended: Google
   says it also governs grounding in Gemini apps.

## Phase 2 — Mutate (10 min)

- *"Treat a 401 like a 403."* (B) where in `fetchcheck`; (S) which audit section changes.
- *"Audit a second domain in the same run."* (B) what changes in `main`; (S) what a
  comparison table across ClearFlow and Tidewell would show.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `matched_rule` picks the first matching rule | The finding test's three guides fail |
| Medium | `check` follows redirects without re-checking robots on the target | The redirect-into-/learn/ test fails |
| Medium | `check` looks for `noindex` in the meta tag only | /warranty becomes readable |
| Nasty | `rules_for` falls back to `*` rules AND adds them to a named group | Nothing errors; GPTBot gets `/cart` rules it already had and the tests pass — until a site's named group allows something the `*` group disallows, and the bot is wrongly blocked |

The **Nasty** one: RFC 9309 says a named group replaces the `*` group, not adds to it.
On Tidewell's file the two readings agree. Ask the student to write the robots.txt on
which they disagree.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Live** | Finds the fault and names its reason before opening code | Finds it with the tool | Reads robots.txt only |
| **Explain** | Separates robots, server and page-level reasons unprompted | Gets there with a nudge | "The bot is blocked" |
| **Mutate** | Names every line before typing | Gets there | Cannot place the change |
| **Debug** | Suspects the silent one | Finds it | Guesses |

---

## Instructor: framing week 4

> **Every crawler can read Tidewell now, and ClearFlow still gets cited first.** Next
> week is content: passages that open with "It", answers in the second sentence,
> numbers buried. Project 1 rewrites five pages and has to win on two engines at once.
