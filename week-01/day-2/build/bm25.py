# Day 2 - BM25, by hand.
#
# Copy passages.py from day-1/build into this folder first. Import tokenize from it:
#     from passages import tokenize
#
#   class BM25(passages, k1=1.2, b=0.75)
#       passages: a list of passage dicts from split_passages. Each is indexed as
#       tokenize(heading + " " + text).
#       For a term t in a passage d, with N passages and df(t) passages containing t:
#           idf(t)   = ln((N - df(t) + 0.5) / (df(t) + 0.5) + 1)
#           part(t)  = idf(t) * f * (k1 + 1) / (f + k1 * (1 - b + b * len(d) / avgdl))
#       where f is how often t occurs in d, len(d) is d's token count and avgdl the
#       mean token count over all passages.
#
#       .score(query, i) -> float
#           the sum of part(t) for every token t of tokenize(query), against passage
#           number i. A query token repeated twice counts twice. A token no passage
#           contains adds nothing.
#       .search(query, k=10) -> list[tuple[float, dict]]
#           (score, passage) for the k best passages, highest first; ties go to the
#           passage that came first in the list. Passages scoring 0 are left out.
#
# Why by hand: you will tune and break this engine for three weeks. A library you have
# not opened is one you cannot attribute a failure to.
