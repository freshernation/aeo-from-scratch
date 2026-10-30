# Day 1 — robots.txt, properly

> **By the end of today** you can say for any path and any crawler what robots.txt
> decides and which rule decided it (B), and write a crawler policy that treats
> training, search and user fetchers as three separate decisions (S).

---

## Read first

- [ ] RFC 9309, section 2.2 — [Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309.html) · 15 min
- [ ] The vendors' pages — [OpenAI](https://platform.openai.com/docs/bots) · [Anthropic](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) · [Perplexity](https://docs.perplexity.ai/guides/bots) · [Google](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) · 20 min

---

## What you need to know

### Three kinds of crawler

**Training** (GPTBot, ClaudeBot, Google-Extended): collects pages for future models.
**Search** (OAI-SearchBot, Claude-SearchBot, PerplexityBot): builds the index an answer
engine retrieves and cites from. **User** (ChatGPT-User, Claude-User, Perplexity-User):
fetches a page because someone asked a question now. Blocking the first does not block
the second. OpenAI says robots.txt "may not apply" to ChatGPT-User; Perplexity says its
user fetcher "generally ignores" it. Google-Extended is a token, not a crawler, and
Google says it also governs grounding in Gemini apps.

### Longest match wins

RFC 9309: of the rules that match a path, the longest pattern decides; on a tie, allow
wins. A named group replaces `*` for that crawler; it does not add to it.

### Today's finding

**Python's `urllib.robotparser` takes the first matching rule, not the longest. On
Tidewell's robots.txt it blocks three guides (`/learn/guides/...`) that RFC 9309 allows.**
Any audit tool built on it reports those pages as blocked. Check which rule your tools
follow before you trust their output.

---

## Exercises

**Builders** — `pytest week-03/day-1/build -v`. Write `robots.py`.

**Strategists** — `pytest week-03/day-1/strategy -v`. Write `robots.txt` and
`ROBOTS_POLICY.md`. The tests check your file with an RFC 9309 parser.

---

## Predict-then-run

`Disallow: /learn/` then `Allow: /learn/guides/`. Is `/learn/guides/pfas` allowed? Is
`/learn/guide` allowed? Write both answers, then check.

---

## Before you close the laptop

Commit, push, fill in the signal log.
