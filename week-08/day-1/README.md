# Day 1 — The site, and thirty questions

> **By the end of today** you have a site you may change, two or three sites that compete
> for its customers' questions, thirty prompts with the page that should answer each, and
> the searches an engine would fan each one out to.

---

## Read first

- [ ] `ai/advisor.md`, week 8 mode · run it, 30 min
- [ ] Your week 1 `PROMPT_SET.md` or `intent.py` · 10 min: the same job, for Tidewell

---

## What you need to know

### Where good prompts come from

Support emails, site search logs, the questions sales hears, and the comparisons customers
make. Not keyword tools: a keyword is not a question.

### best_url

For each prompt, the page on your site that should answer it, or empty if none does. An
empty best_url is a content gap, which is a finding.

### fanout.json

The panel fans out only what you script. For at least five prompts, write the two or three
searches an engine would also run. This is a judgement you will defend.

---

## Exercises

Fill `week-08/site/site.json`, `prompts.csv`, `fanout.json`, then `day-1/SITE.md`.

```bash
pytest week-08/day-1 -v
```

---

## Predict-then-run

Before tomorrow's audit: how many of your thirty will the panel cite your best page for?

---

## Before you close the laptop

Commit, push, fill in the signal log.
