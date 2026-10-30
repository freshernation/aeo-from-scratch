# Week 4 milestone (Project 1) - the engine, complete.
#
# Copy into this folder: passages.py, bm25.py, cite.py, fanout.py (week 1),
# robots.py, fetchcheck.py, sitemap.py (week 3), boosts.py (week 4 day 3).
# You may import FakeModel from aeolab.llm. Nothing else from aeolab.
#
#   crawl(web, bot, limit=500) -> dict
#       {final url: html} for every page your crawler can index, as `bot`. For each
#       domain in web.domains(): start from https://{domain}/ and every <loc> in its
#       sitemap.xml (if that answers 200), then breadth-first: check() each url with
#       your fetchcheck; skip unreadable ones and final urls already kept; keep the html
#       (fetch the final url again); queue every same-domain <a href> not yet seen
#       (resolved, without its #fragment). Stop a domain after `limit` urls seen.
#
#   class Engine(web, bot="MyEngine", model=None, k=4)
#       On creation: crawl, split every page, build one BM25.
#       .answer(query, temperature=0.0, seed=0, sample=0) -> dict
#           search_fanout(top 20) -> rerank -> then, if temperature > 0, re-sort by
#           exp(N(0, temperature)) / (1 + position) using
#           random.Random(f"{seed}|{sample}|{query}") -> cite as in week 1 (k urls, at
#           most 2 per domain) -> {"sentences", "citations", "unsupported"} as in week 1.
#       .run(prompts, samples=1, temperature=0.0, seed=0, run_id="my-engine") -> rows
#           week 2's row format, one per prompt per sample, cited_domains from the urls.
#
# Why: from here on your engine is a third opinion. Week 7 adds a fourth, live.
