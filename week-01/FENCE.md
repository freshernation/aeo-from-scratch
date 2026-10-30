# Week 1 — Concept fence

## Allowed

Your prerequisite (Python; Builders: retrieval and an eval set; Strategists: SEO), plus:

- The seven steps: crawl, split, fan out, retrieve, score, cite, answer
- Passages, tokens, stopwords; BM25 (B); reciprocal rank fusion
- `bs4.BeautifulSoup`, `re`, `math`, `collections.Counter`, `csv`
- `aeolab.load_pages`, `aeolab.load_prompts`, `aeolab.llm.FakeModel`, `aeolab.panel.Panel`
  (reading its trace and its search; you do not change it)
- Word overlap as a support check; the course's five-point quotability checklist (S)
- Intent: brand, howto, comparison, commercial, informational

## Not yet

Citation rate and share of voice (week 2) · sampling and intervals (week 2) ·
robots.txt, status codes, noindex, JavaScript (week 3) · rewriting a page (week 4) ·
schema and JSON-LD (week 5) · live engines (week 7) · embeddings (cut)

---

## Why no rewriting this week

You will see Tidewell's weak passages on Monday and want to fix them. Don't. On Friday
you will find that on half the prompts Tidewell's best page never reached the
candidates at all, which no rewrite can change. Rewriting first is how people spend a
month on the wrong step.
