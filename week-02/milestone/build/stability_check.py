# Given - counts prompts whose answer changes between samples.

from collections import defaultdict


def unstable_count(rows, domain):
    seen = defaultdict(set)
    for r in rows:
        seen[r["prompt_id"]].add(domain in r["cited_domains"])
    return sum(len(v) == 2 for v in seen.values())
