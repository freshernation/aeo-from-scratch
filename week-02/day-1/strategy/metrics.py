# Day 1 - three visibility numbers a client understands.
#
# A run file is JSON lines; aeolab.load_runs("baseline.jsonl") gives a list of dicts:
#     {"run_id", "prompt_id", "sample", "cited_urls", "cited_domains", "answer"}
# One row per answer. cited_domains lists the sites cited, best first.
#
#   citation_rate(rows, domain) -> float
#       The share of rows whose cited_domains include domain. 0.0 for no rows.
#   share_of_voice(rows) -> dict
#       {domain: that domain's citations / all citations, over every row}
#   mention_rate(rows, brand) -> float
#       The share of rows whose answer contains brand, ignoring case. 0.0 for no rows.
#
# Why: these are the three numbers every AEO tool sells. Today you compute them
# yourself, so next week you know exactly what a vendor's dashboard is counting.
