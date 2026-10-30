# Day 4 - query fan-out, and reciprocal rank fusion.
#
# Copy passages.py and bm25.py from day-2/build into this folder.
#
#   rrf(rankings, k=60) -> list[tuple[str, float]]
#       rankings: several ranked lists of ids, best first. Each id scores the sum of
#       1 / (k + rank) over the lists it appears in, rank counting from 1.
#       Returns (id, score) pairs, highest first; ties in the order ids were first seen.
#       rrf([["a", "b"], ["b"]]) == [("b", 1/62 + 1/61), ("a", 1/61)]
#
#   search_fanout(bm25, model, query, k=10) -> list[dict]
#       model.fan_out(query) gives the searches an engine would run (aeolab.llm.FakeModel).
#       Run bm25.search(q, k) for each, fuse the rankings of passage "id"s with rrf,
#       and return the top k passage dicts in fused order.
#
# Why: no answer engine searches your exact words once. The page that wins the fused
# ranking is often not the one that wins any single search.
