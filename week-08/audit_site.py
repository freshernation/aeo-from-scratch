"""Given. A quick audit of the site in week-08/site/snapshot/, with the course's own code.
Builders: use your week 6 aeo_audit.py instead, with --web pointing here (see day 2).

    python3 week-08/audit_site.py
"""
import json
import re
from datetime import date

from bs4 import BeautifulSoup

from aeolab.fakeweb import FakeWeb
from aeolab.panel import Panel, split_passages

from measure import SITE, load

BOTS = ["OAI-SearchBot", "Claude-SearchBot", "PerplexityBot", "GPTBot", "ClaudeBot", "Google-Extended"]


def main():
    info, prompts, _ = load()
    d = info["domain"]
    web = FakeWeb(root=SITE / "snapshot")
    urls = web.page_urls(d)
    print(f"# {d}: {len(urls)} pages in the snapshot\n\n## Access (robots.txt, status, noindex, canonical; not CDN rules)\n")
    for u in urls:
        row = [Panel(web, bot=b).readable(u) for b in BOTS]
        if not all(ok for ok, _ in row):
            print(f"  {u}: " + ", ".join(f"{b} {why}" for b, (ok, why) in zip(BOTS, row) if not ok))
    print("\n## Passages that open with a pronoun, or are under 12 words\n")
    for u in urls:
        for p in split_passages(u, web.fetch(u).text):
            w = p.text.split()
            if w and (w[0].lower().strip(",.") in ("it", "this", "they", "these", "those", "that") or len(w) < 12):
                print(f"  {u} [{p.heading}]: {' '.join(w[:12])}...")
    print("\n## Structured data prices not shown on the page\n")
    for u in urls:
        html = web.fetch(u).text
        soup = BeautifulSoup(html, "html.parser")
        shown = set(re.findall(r"\$(\d[\d,]*(?:\.\d+)?)", soup.get_text(" ")))
        for tag in soup.find_all("script", type="application/ld+json"):
            for price in re.findall(r'"price"\s*:\s*"?([\d.]+)', tag.string or ""):
                if price.removesuffix(".00") not in {s.removesuffix(".00") for s in shown}:
                    print(f"  {u}: markup says {price}")
    print("\n## Pages dated more than two years ago\n")
    for u in urls:
        t = BeautifulSoup(web.fetch(u).text, "html.parser").find("time")
        if t and t.get("datetime") and (date.today() - date.fromisoformat(t["datetime"][:10])).days > 730:
            print(f"  {u}: {t['datetime'][:10]}")
    print("\n## Best pages the panel does not cite today\n")
    panel = Panel(web)
    for p in prompts:
        if p["best_url"] and p["best_url"] not in [c.url for c in panel.ask(p["prompt"]).citations]:
            print(f"  {p['id']} {p['prompt']}  ->  {p['best_url']}")


if __name__ == "__main__":
    main()
