# Week 1 milestone - an answer engine that answers and cites.
#
# Copy passages.py, bm25.py, cite.py and fanout.py into this folder first (see README).
# You may import FakeModel from aeolab.llm. Nothing else from aeolab.
#
#   class Engine(pages, model=None, k=4)
#       pages: {url: html}, as aeolab.load_pages() returns.
#       model: a FakeModel; make a new FakeModel() when none is given.
#       On creation: split every page into passages and build one BM25 over all of them.
#
#       .answer(query) -> dict with exactly these keys:
#           "citations"    the urls of the passages cited, best first. Walk the top 20
#                          passages from search_fanout and keep a passage unless
#                          - its url is already cited, or
#                          - two passages from its domain (the host part of the url)
#                            are already cited.
#                          Stop at k.
#           "sentences"    model.synthesize(query, cited_passages)
#           "unsupported"  the sentences your cite.unsupported() finds, threshold 0.5
#
# Why: these are the seven steps of the panel's docstring minus the crawl and the
# boosts. Next week you measure it; week 3 gives it a crawler; week 4 its boosts.
