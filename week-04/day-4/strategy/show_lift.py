"""Given. Run both engines on web2 with and without your snapshot and print the lift.

    python3 week-04/day-4/strategy/show_lift.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))
from aeolab import load_prompts, web2  # noqa: E402
from aeolab.engine_b import EngineB  # noqa: E402
from aeolab.panel import Panel  # noqa: E402
from rewrite_checks import SNAPSHOT, paired_first  # noqa: E402

D = "tidewell.example"


def rate(rows, first=False):
    hit = (lambda r: r["cited_domains"][:1] == [D]) if first else (lambda r: D in r["cited_domains"])
    return sum(map(hit, rows)) / len(rows)


def main():
    prompts = load_prompts()
    for name, engine in (("panel", Panel), ("Engine B", EngineB)):
        before = engine(web2()).run(prompts, 20, 0.3, seed=4)
        after = engine(web2(SNAPSHOT)).run(prompts, 20, 0.3, seed=4)
        p = paired_first(before, after)
        print(f"{name:9} cited {rate(before):.1%} -> {rate(after):.1%}   first {rate(before, True):.1%} -> "
              f"{rate(after, True):.1%}   first-cited by prompt: {p['wins']} up, {p['losses']} down, p = {p['p']:.4f}")


if __name__ == "__main__":
    main()
