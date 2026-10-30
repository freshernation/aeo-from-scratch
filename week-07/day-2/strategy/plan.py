# Day 2 - what monitoring costs a month.
#
#   monthly_cost(prompts, samples, cost_per_answer, runs_per_month) -> float | None
#       cost_per_answer: {engine: dollars per answer, or None if unpriced}.
#       prompts x samples x (sum of the engines' costs) x runs_per_month, rounded to cents.
#       None if any engine is unpriced.
#       monthly_cost(30, 10, {"claude": 0.064}, 52 / 12) == 83.2
#
#   affordable_samples(prompts, cost_per_answer, runs_per_month, monthly_budget) -> int | None
#       the most samples per prompt the monthly budget pays for, rounded down.
#       None if any engine is unpriced or nothing costs anything.
#
# Why: the client will ask what monitoring costs before they ask what it shows.
