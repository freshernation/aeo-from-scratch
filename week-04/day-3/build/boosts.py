# Day 3 - make your engine reward what the panel rewards.
#
# Copy passages.py, bm25.py and fanout.py from week-01/milestone/build.
# The panel's rules R6 to R8 are in the docstring of aeolab/panel.py. Write your own.
#
#   first_sentence(text) -> str
#       Split at the first . ! or ? followed by whitespace and then a capital letter,
#       digit, quote or "(" - so "2.4 litres" and "$12.50" do not end a sentence.
#
#   boosts(passage, query) -> dict
#       passage: a dict with "text". Exactly these keys:
#         "self_contained"  0.7 if the first word (lowercased, stripped of , . :) is one of
#                           it this they these those that he she, else 1.0
#         "answer_first"    1.25 if the first sentence is 35 words or fewer AND holds at
#                           least half of the query's distinct tokens, else 1.0
#         "specific"        1 + 0.08 x the number of numbers in the text, counting at most 3
#                           (a number: digits, with , or . between digits allowed)
#
#   rerank(passages, query) -> list[dict]
#       passages: in retrieval order, best first. Score each 1 / (60 + rank) times the
#       product of its boosts (rank from 1); return them highest first, ties in the
#       original order.
#
# Why: the panel rewards answer-first, self-contained, specific passages. Today you
# find out whether copying those rules makes your engine agree with it.
