"""Given. Measure your site before and after your changes, on two engines.

    python3 week-08/measure.py            # writes week-08/site/results.json

Reads week-08/site/:
    site.json     {"domain": "www.your-site.com", "competitors": [...]}
    prompts.csv   your 30 prompts: id, prompt, intent, best_url
    fanout.json   {prompt: [the searches an engine would also run]} - yours to write
    snapshot/     your site and its competitors as they are (aeolab.snapshot)
    after/        only the files you changed, laid over the snapshot

Runs the panel and Engine B on both, 20 samples per prompt at temperature 0.3, seed 8,
the same as the rest of the course, and records, per engine: cited and first-cited rates
before and after, the paired result on each, and best pages cited at temperature 0.
"""
import csv
import json
import math
import sys
from datetime import date
from pathlib import Path

from aeolab.engine_b import EngineB
from aeolab.fakeweb import FakeWeb
from aeolab.llm import FakeModel
from aeolab.panel import Panel

SITE = Path(__file__).parent / "site"
SAMPLES, TEMPERATURE, SEED = 20, 0.3, 8


def load(site=SITE):
    site = Path(site)
    info = json.loads((site / "site.json").read_text())
    with open(site / "prompts.csv", newline="") as f:
        prompts = list(csv.DictReader(f))
    fanout = json.loads((site / "fanout.json").read_text()) if (site / "fanout.json").exists() else {}
    return info, prompts, fanout


def _rate(rows, domain, first=False):
    hit = (lambda r: r["cited_domains"][:1] == [domain]) if first else (lambda r: domain in r["cited_domains"])
    return round(sum(map(hit, rows)) / len(rows), 3) if rows else 0.0


def _paired(before, after, domain, first=False):
    def by(rows):
        g = {}
        for r in rows:
            ok = r["cited_domains"][:1] == [domain] if first else domain in r["cited_domains"]
            g.setdefault(r["prompt_id"], []).append(ok)
        return {p: sum(v) / len(v) for p, v in g.items()}
    a, b = by(before), by(after)
    wins = sum(b[p] > a[p] for p in a)
    losses = sum(b[p] < a[p] for p in a)
    n, k = wins + losses, min(wins, losses)
    p = 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)
    return {"wins": wins, "losses": losses, "p": round(p, 4)}


def compute(site=SITE):
    site = Path(site)
    info, prompts, fanout = load(site)
    domain = info["domain"]
    before_web = FakeWeb(root=site / "snapshot")
    after_web = FakeWeb(root=site / "snapshot", overlay=site / "after")
    out = {"domain": domain, "prompts": len(prompts), "samples": SAMPLES, "engines": {}}
    for name, engine in (("panel", Panel), ("engine_b", EngineB)):
        model = FakeModel(fanout=fanout, extras={})
        b, a = engine(before_web, model=model), engine(after_web, model=model)
        rb = b.run(prompts, SAMPLES, TEMPERATURE, SEED)
        ra = a.run(prompts, SAMPLES, TEMPERATURE, SEED)
        best = lambda e: sum(p["best_url"] in [c.url for c in e.ask(p["prompt"]).citations] for p in prompts if p["best_url"])
        out["engines"][name] = {
            "cited": [_rate(rb, domain), _rate(ra, domain)],
            "first": [_rate(rb, domain, True), _rate(ra, domain, True)],
            "paired_cited": _paired(rb, ra, domain),
            "paired_first": _paired(rb, ra, domain, True),
            "best_pages": [best(b), best(a)],
        }
    return out


def main():
    result = compute()
    result["date"] = date.today().isoformat()
    (SITE / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
