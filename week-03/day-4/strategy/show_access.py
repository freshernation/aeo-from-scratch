"""Given. Every Tidewell page against every AI crawler, as the panel's rules see it.

    python3 week-03/day-4/strategy/show_access.py
"""
from aeolab.fakeweb import FakeWeb
from aeolab.panel import Panel

BOTS = ["GPTBot", "ClaudeBot", "Google-Extended", "OAI-SearchBot", "Claude-SearchBot",
        "PerplexityBot", "ChatGPT-User", "Claude-User", "Perplexity-User"]


def main():
    urls = FakeWeb().page_urls("tidewell.example")
    panels = {b: Panel(bot=b) for b in BOTS}
    print(f"{'page':<42}" + "".join(f"{b[:11]:>12}" for b in BOTS))
    for u in urls:
        cells = []
        for b in BOTS:
            ok, why = panels[b].readable(u)
            cells.append("ok" if ok else why)
        print(f"{u.split('.example', 1)[1]:<42}" + "".join(f"{c[:11]:>12}" for c in cells))


if __name__ == "__main__":
    main()
