# Day 4 - the baseline report, generated.
#
# Copy metrics.py, sampling.py and stats.py into this folder. stability_check.py is given.
#
#   pct(x) -> str          73.0% style: pct(0.73) == "73.0%"
#
#   by_intent(rows, prompts, domain) -> dict
#       prompts: load_prompts(). {intent: citation rate of domain over the rows of that
#       intent's prompts}, intents in alphabetical order.
#
#   report(rows, prompts, domain, brand, title="Visibility report") -> str
#       Markdown, exactly these sections in this order:
#         "# {title}"
#         "## Summary"   one sentence:
#             "{brand} is cited in {pct} of {N} answers ({pct lo} to {pct hi}, 95% bootstrap
#              over {P} prompts) and cited first in {pct first}."
#             N = rows, P = distinct prompts, lo/hi from stats.prompt_bootstrap.
#         "## By site"   a table: | Site | Cited | First | Share of voice | with one row per
#                        domain in share_of_voice order
#         "## By intent" a table: | Intent | {brand} cited |
#         "## Noise"     "{U} of {P} prompts cite {brand} on some samples and not others."
#                        with U from stability_check.unstable_count
#
# Why generated: next week, and every week after, you will re-run this on a new run file.
# A report typed by hand is a report nobody re-runs.
