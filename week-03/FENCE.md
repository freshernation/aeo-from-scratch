# Week 3 — Concept fence

## Allowed

**Everything from weeks 1 and 2**, plus:

- robots.txt and RFC 9309: groups, longest match, wildcards, `/robots.txt` always allowed
- Training, search and user-fetch crawlers, from the vendors' own pages
- Status codes 200, 301/302/307/308, 403, 404; redirect chains and loops
- `noindex` in a meta tag and in an `X-Robots-Tag` header; `rel="canonical"`
- JavaScript-only pages; what a crawler that does not render receives
- Sitemaps (`xml.etree.ElementTree`); the llms.txt proposal
- `aeolab.fakeweb.FakeWeb`, including `overlay=` for a fixed copy
- `argparse`, `json` (B milestone)

## Not yet

Rewriting content (week 4) · structured data (week 5) · other sites' pages about you
(week 6) · server logs and verifying a bot's IP (week 7) · live crawling of a real site (week 8)

---

## Why no real site this week

A real site's crawler problems are real, and you would learn them faster with Tidewell's
planted ones, where every answer can be checked. Week 8 points the same tool at your
own site. By then you will know what each reason looks like when it is true.
