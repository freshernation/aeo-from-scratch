"""Given. Show how the panel answered one prompt, step by step.

    python3 week-01/day-1/strategy/show_trace.py P01
"""
import sys

from aeolab import load_prompts
from aeolab.panel import Panel


def main(pid):
    prompt = {p["id"]: p for p in load_prompts()}[pid]
    a = Panel().ask(prompt["prompt"])
    print(f"{pid}: {prompt['prompt']}\n")
    print("1. Fan-out searches:")
    for q in a.trace["queries"]:
        print(f"     - {q}")
    print("\n2. Top candidates (rrf = retrieval score before boosts):")
    print(f"     {'score':>7} {'rrf':>7}  boosts that are not 1.0              passage")
    for r in a.trace["candidates"]:
        b = ", ".join(f"{k} {v:.2f}" for k, v in r["boosts"].items() if v != 1.0)
        mark = "*" if r["id"] in a.trace["cited"] else " "
        print(f"   {mark}{r['score']:7.4f} {r['rrf']:7.4f}  {b:<36} {r['url'].removeprefix('https://')} [{r['heading']}]")
    print("\n   * = cited\n\n3. Answer:")
    for s in a.sentences:
        print(f"     {s}")
    print(f"\nTidewell's best page for this prompt: {prompt['best_url'] or '(none)'}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "P01")
