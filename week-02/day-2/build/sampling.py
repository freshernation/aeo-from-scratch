# Day 2 - how many samples does a number need?
#
# Copy metrics.py from day-1/build; import citation_rate from it.
# The recorded runs have 20 samples per prompt. Today you pretend you had fewer.
#
#   NS = (1, 2, 3, 5, 10, 15)       the sample counts you will try
#
#   by_prompt(rows) -> dict         {prompt_id: [its rows, in file order]}
#
#   subsample(rows, n, rng) -> list
#       For every prompt, rng.choices(that prompt's rows, k=n) - drawn WITH
#       replacement, the way a fresh run would draw n new answers. All prompts' picks
#       together, prompts in first-seen order. rng is a random.Random.
#
#   spread(rows, domain, n, trials=200, seed=0) -> tuple[float, float]
#       rng = random.Random(seed). Do `trials` subsamples of n per prompt and compute
#       citation_rate on each. Sort the rates; return
#           (rates[int(0.025 * trials)], rates[int(0.975 * trials) - 1])
#       - the range 95% of re-runs at this n would land in.
#
#   stable_at(rows, domain, width=0.05, trials=200, seed=0) -> int | None
#       The first n in NS whose spread is no wider than width. None if none is.
#
# Why: one screenshot of an answer engine is a sample of one. Today you find out how
# wrong a sample of one can be.
