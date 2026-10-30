"""Given. What each live-shaped answer cites, as raw strings, next to the panel's citations.

    python3 week-07/day-1/strategy/show_live.py            # the course's invented fixtures
    python3 week-07/day-1/strategy/show_live.py --live 10  # ask live engines (keys needed, costs money)
"""
import json
import sys

from aeolab import HERE, live, load_prompts, web2
from aeolab.panel import Panel


def raw_urls(vendor, resp):
    if vendor == "claude":
        return [c["url"] for b in resp.get("content", []) if b.get("type") == "text" for c in (b.get("citations") or [])]
    if vendor == "openai":
        return [a["url"] for i in resp.get("output", []) if i.get("type") == "message"
                for p in i.get("content", []) for a in p.get("annotations", [])]
    return resp.get("citations") or [r["url"] for r in resp.get("search_results", [])]


def main():
    n = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "--live" else None
    prompts = load_prompts()[: n or 10]
    panel = Panel(web2())
    fixtures = {v: json.loads((HERE / "data" / "live" / f"{v}.json").read_text()) for v in ("claude", "openai", "perplexity")}
    print("LIVE" if n else "FIXTURES (invented content - see aeolab/data/live/README.md)\n")
    for p in prompts:
        print(f"{p['id']}  {p['prompt']}")
        print("   panel      ", [c.url for c in panel.ask(p["prompt"]).citations])
        for vendor in fixtures:
            resp = live.ask(vendor, p["prompt"]) if n else fixtures[vendor][p["id"]]
            print(f"   {vendor:<11}", raw_urls(vendor, resp))
        print()


if __name__ == "__main__":
    main()
