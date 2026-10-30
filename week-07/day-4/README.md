# Day 4 — What the server saw

> **By the end of today** you can tell real AI crawlers from impostors, see when a fix
> took effect, and count people sent by answer engines (B), and write it up (S).

---

## Read first

- [ ] OpenAI — [crawlers and their IP lists](https://platform.openai.com/docs/bots) · 10 min
- [ ] Perplexity — [crawlers and their IP lists](https://docs.perplexity.ai/guides/bots) · 5 min

---

## What you need to know

### A user agent is a claim

Anyone can send "GPTBot". OpenAI and Perplexity publish JSON lists of the address ranges
their crawlers use (`{"prefixes": [{"ipv4Prefix": ...}]}`); Anthropic's crawler page
links its own list. A hit is verified when its address is inside its bot's range. The
course's ranges use documentation addresses, in the same format.

### Referrals

A person who clicks a citation arrives with a referer (chatgpt.com, perplexity.ai,
claude.ai, gemini.google.com), sometimes with a utm tag too.

### Today's finding

**580 hits claim to be GPTBot; 400 come from outside its range. Claude's and Perplexity's
crawlers got 403s on every request until 15 September and 200s from then on: the day the
CDN fix landed. Answer engines sent 148 visits: ChatGPT 73, Gemini 39, Claude 21,
Perplexity 15.**

---

## Exercises

**Builders** — `pytest week-07/day-4/build -v`. Write `logs.py`.

**Strategists** — `python3 week-07/day-4/strategy/show_logs.py`, then
`pytest week-07/day-4/strategy -v`. Write `LOG_REPORT.md`.

---

## Predict-then-run

What share of "GPTBot" hits do you expect to be real? Then check.

---

## Before you close the laptop

Commit, push, fill in the signal log.
