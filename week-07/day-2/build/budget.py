# Day 2 - what a measurement costs, before you run it.
#
# aeolab/data/prices.json holds, per engine: search_per_1k (dollars per 1,000 searches),
# input_per_mtok and output_per_mtok (dollars per million tokens) - null where the course
# could not verify a price - and "assumptions": searches, input tokens and output tokens
# per answer. The assumptions are guesses: replace them after your first live run.
#
#   load_prices(path) -> dict          the JSON
#
#   cost_per_answer(prices, engine) -> float | None
#       searches x search price / 1000 + input tokens x input price / 1e6
#       + output tokens x output price / 1e6, from the assumptions. None if any of the
#       engine's three prices is null: an unpriced engine has no cost, not a zero cost.
#
#   run_cost(prices, engines, prompts, samples) -> float | None
#       every engine's cost_per_answer, summed, x prompts x samples, rounded to cents.
#       None if any engine is unpriced.
#
#   max_samples(prices, engines, prompts, budget) -> int | None
#       the most samples per prompt the budget pays for, rounded down. None if any
#       engine is unpriced or the run is free.
#
#   unpriced(prices, engines) -> list[str]      the engines with no cost, in order
#
# Why: week 2 said ten samples per prompt. Today you find out what that costs on a live
# engine, and what you cannot plan until someone looks up a price.
