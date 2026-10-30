"""Given. For each prompt, whether Tidewell's best page was cited, and if not, where it
was lost; and who was cited first.

    python3 week-06/day-4/strategy/show_losses.py
"""
from aeolab import PROMPTS_MORE, load_prompts, web2
from aeolab.panel import Panel


def why(panel, x, a):
    if not x["best_url"]:
        return "no-page"
    if x["best_url"] in [c.url for c in a.citations]:
        return "cited"
    if not panel.readable(x["best_url"])[0]:
        return "not-crawled"
    mine = [r for r in a.trace["all"] if r["url"] == x["best_url"]]
    if not mine:
        return "not-retrieved"
    low = min(r["score"] for r in a.trace["all"] if r["id"] in a.trace["cited"])
    return "capped" if max(r["score"] for r in mine) > low else "out-scored"


def main():
    panel = Panel(web2())
    for x in load_prompts() + load_prompts(PROMPTS_MORE):
        a = panel.ask(x["prompt"])
        print(f"{x['id']}  {why(panel, x, a):<14} first: {a.citations[0].domain:<22} {x['prompt']}")


if __name__ == "__main__":
    main()
