# Day 1 - visibility metrics over a run file.
#
# A run file is JSON lines; aeolab.load_runs("baseline.jsonl") gives a list of dicts:
#     {"run_id", "prompt_id", "sample", "cited_urls", "cited_domains", "answer"}
# One row per prompt per sample. cited_domains is in citation order, best first.
#
#   citation_rate(rows, domain) -> float     share of rows whose cited_domains include domain
#   first_rate(rows, domain) -> float        share of rows whose FIRST citation is domain
#   prompt_rates(rows, domain) -> dict       {prompt_id: citation rate over that prompt's rows}
#   share_of_voice(rows) -> dict             {domain: its citations / all citations}, ordered
#                                            most cited first (ties: first seen first)
#   mention_rate(rows, brand) -> float       share of rows whose answer contains brand as a
#                                            whole word, any case ("Tidewell's" counts,
#                                            "Tidewellness" does not)
#   mentioned_not_cited(rows, brand, domain) -> int
#                                            rows that mention brand but do not cite domain
#   Every rate is 0.0 for no rows.
#
# Why five numbers: "are we visible?" has at least five answers, and a client will pick
# whichever flatters them unless the report shows all of them.
