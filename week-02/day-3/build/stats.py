# Day 3 - intervals, and a paired test.
#
# Copy metrics.py (day 1) and sampling.py (day 2) into this folder.
#
#   wilson(k, n, z=1.96) -> tuple[float, float]
#       The Wilson score interval for k successes in n trials:
#           p = k / n
#           centre = (p + z²/2n) / (1 + z²/n)
#           half   = z * sqrt(p(1-p)/n + z²/4n²) / (1 + z²/n)
#       Return (centre - half, centre + half), clipped to [0, 1]. (0.0, 1.0) when n is 0.
#
#   sign_test(wins, losses) -> float
#       Two-sided exact sign test: with n = wins + losses and k = min(wins, losses),
#       p = 2 * sum(comb(n, i) for i in 0..k) / 2**n, capped at 1.0. 1.0 when n is 0.
#
#   paired(a_rows, b_rows, domain) -> dict
#       Compare two runs prompt by prompt with metrics.prompt_rates. A prompt is a
#       win if b's rate is higher, a loss if lower, a tie if equal.
#       {"wins": int, "losses": int, "ties": int, "p": sign_test(wins, losses)}
#
#   prompt_bootstrap(rows, domain, trials=1000, seed=0) -> tuple[float, float]
#       rng = random.Random(seed). Each trial: rng.choices(the prompts' row groups,
#       k=number of prompts) - prompts drawn WITH replacement, each bringing all its
#       rows - and compute citation_rate over the rows drawn. Sort the rates; return
#       (rates[int(0.025 * trials)], rates[int(0.975 * trials) - 1]).
#       Use sampling.by_prompt for the groups.
#
# Why two intervals: Wilson treats 600 answers as 600 independent coin tosses. They are
# not: they are 30 prompts asked 20 times each. Today you see how much that matters.
