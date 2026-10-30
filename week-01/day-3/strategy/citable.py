# Day 3 - would an engine quote this passage? Five checks you can explain to a client.
#
#   first_sentence(text) -> str
#       Everything up to and including the first ".", "!" or "?" that is followed by
#       whitespace - or the whole text if there is none.
#       first_sentence("It is good. Buy it.") == "It is good."
#
#   score(heading, text) -> dict
#       Five checks, each True or False, under exactly these keys, plus "total":
#         "short_first"       the first sentence is 30 words or fewer
#         "no_pronoun_start"  the first word, lowercased and stripped of , . :
#                             is not one of: it this they these those that
#         "has_number"        the text contains at least one digit
#         "right_length"      the text is 20 to 120 words, inclusive
#         "names_subject"     the first sentence shares at least one word with the
#                             heading, ignoring: a an the of to and or for in on is do
#                             does how what which why can i my your our you we
#                             (compare lowercase runs of letters and digits)
#         "total"             how many of the five are True
#
#   mean_score(passages) -> float
#       passages: dicts with "heading" and "text". The mean "total"; 0.0 for none.
#
# Why: these five are the course's checklist for a passage that survives being quoted
# alone. They are not the panel's rules - compare them with the docstring of
# aeolab/panel.py, and notice which ones the panel does not reward.
