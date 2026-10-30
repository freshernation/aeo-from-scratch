# Day 3 - which passage supports each sentence of an answer?
#
# Copy passages.py from day-1/build into this folder and import tokenize from it.
#
#   support(sentence, passage_text) -> float
#       Of the DISTINCT tokens in the sentence, the share that also occur in the
#       passage's tokens. A sentence with no tokens at all has support 0.0.
#       support("Lead pipes leak lead.", "Old pipes contain lead.") == 2 / 3
#           (sentence tokens {lead, pipe, leak}; the passage has lead and pipe)
#
#   attribute(sentences, passages, threshold=0.5) -> list[str | None]
#       passages: dicts with "url" and "text". For each sentence, the url of the
#       passage that supports it most (the first such passage on a tie), or None if
#       even the best support is below threshold.
#
#   unsupported(sentences, passages, threshold=0.5) -> list[str]
#       The sentences attribute() gives None, in order.
#
# Why: an engine's citations are only worth something if each sentence came from the
# passage it cites. Today you find out how weak a word-overlap check is.
