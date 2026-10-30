# Day 4 - did a rewrite help, and on which engine?
#
# Copy metrics.py, sampling.py and stats.py from week-02/milestone/build.
# An engine here is anything with .run(prompts, samples, temperature, seed) that
# returns week 2's rows: the panel, EngineB, and (on Friday) yours.
#
#   firsts(rows) -> list[dict]
#       Copies of the rows with cited_domains cut to the first one, so week 2's
#       functions measure first-cited instead of cited.
#
#   lift(make_engine, before_web, after_web, prompts, domain,
#        samples=20, temperature=0.3, seed=4) -> dict
#       make_engine(web) builds an engine. Run one on each web with the same samples,
#       temperature and seed, and return exactly:
#         "cited"         (citation rate before, after)
#         "first"         (first-cited rate before, after)
#         "paired"        stats.paired(before_rows, after_rows, domain)
#         "paired_first"  the same on firsts(...) of both
#
#   verdict(result) -> str
#       From paired_first: "helps" if p < 0.05 and wins > losses, "hurts" if p < 0.05
#       and losses >= wins, else "no clear change".
#
# Why first-cited: on this web Tidewell is already cited in most answers. Being the
# first source is what a rewrite can still change.
