# Day 2 - which prompts give a different answer each time?
#
#   cited_counts(rows, domain) -> dict
#       {prompt_id: (rows citing domain, rows for that prompt)}
#       e.g. {"P01": (20, 20), "P03": (7, 20), ...}
#
#   unstable(rows, domain) -> list[str]
#       Sorted prompt ids where domain is cited on some samples but not on all.
#
# Why: if a prompt is unstable, a single check of it - yours or a client's - is a coin
# toss, and so is any "before and after" built on one.
