# Day 4 - for every prompt Tidewell loses, the step that lost it.
#
# The panel's answer has a trace: trace["all"] holds every candidate passage with its
# "id", "url" and final "score"; trace["cited"] the ids it cited. Read aeolab/panel.py.
#
#   attribute(panel, prompt) -> str
#       prompt: a dict with "prompt" and "best_url". At temperature 0, one of:
#         "no-page"        best_url is empty: Tidewell has no page for this
#         "cited"          best_url is among the citations
#         "not-crawled"    panel.readable(best_url) is False
#         "not-retrieved"  no passage of best_url is among the candidates
#         "capped"         its best passage scored above the lowest cited passage, and was
#                          still not cited (the 2-per-domain or one-per-url rule)
#         "out-scored"     otherwise: it was a candidate and scored too low
#
#   attribute_all(panel, prompts) -> dict      {prompt id: attribute(...)}
#
#   first_cited_by(panel, prompts) -> Counter  domain of each answer's first citation
#
# Why: the rule from week 1 - attribute the loss to one step before changing anything -
# as code you can run after every change.
