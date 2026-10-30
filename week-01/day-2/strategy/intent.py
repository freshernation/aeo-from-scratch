# Day 2 - what kind of question is this?
#
# Read aeolab/prompts.csv. Each prompt has an intent:
#   brand          names Tidewell (and is not a head-to-head comparison)
#   howto          asks how to do something, or about installing
#   comparison     X vs Y, or which is better
#   commercial     best, worth it, should I buy
#   informational  everything else
#
#   INTENTS   the five intent names above, as a tuple of strings
#
#   classify(prompt) -> str
#       One of INTENTS, decided by rules you write over the lowercased prompt.
#       The ORDER of your rules matters: "Tidewell Pitcher vs ClearFlow Pitcher" names
#       Tidewell AND is a comparison - it is labelled comparison.
#       classify("Is a shower filter worth it?") == "commercial"
#
#   accuracy(prompts) -> float
#       prompts: a list of dicts with "prompt" and "intent", as load_prompts() returns.
#       The share whose classify() matches "intent".
#
# Why: an engine treats "best X" and "what is X" differently, and so should your
# content plan. You will break your visibility down by intent on Friday.
