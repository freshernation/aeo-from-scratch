# Day 3 - is it a real change, or noise?
#
#   wilson(k, n, z=1.96) -> tuple[float, float]
#       The Wilson score interval for k successes out of n:
#           p = k / n
#           centre = (p + z*z/(2n)) / (1 + z*z/n)
#           half   = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
#       Return (centre - half, centre + half), clipped to 0..1. (0.0, 1.0) when n is 0.
#
#   prompt_rates(rows, domain) -> dict      {prompt_id: share of its rows citing domain}
#
#   wins_losses(a_rows, b_rows, domain) -> tuple[int, int, int]
#       Prompt by prompt: a win when b's rate is higher than a's, a loss when lower,
#       a tie when equal. Returns (wins, losses, ties).
#
#   sign_test(wins, losses) -> float
#       n = wins + losses, k = the smaller of the two.
#       p = 2 * (sum of math.comb(n, i) for i from 0 to k) / 2**n, capped at 1.0.
#       1.0 when n is 0. Below 0.05 is the usual line for "not noise".
#
# Why: "citations went from 73% to 74%" sounds like progress. Today you can say whether
# it is.
