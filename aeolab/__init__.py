"""aeolab - the course's shared, given code.

    from aeolab import load_prompts, load_runs, save_runs, load_pages
    from aeolab.fakeweb import FakeWeb      # the offline web
    from aeolab.llm import FakeModel        # the scripted model
    from aeolab.panel import Panel          # the engine you measure against
    from aeolab.engine_b import EngineB     # a second engine, from week 4
    from aeolab import web2                 # the web weeks 4 to 6 work on

You may read all of it. You do not change it; if a lab needs something different, the
lab says so.
"""

import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
PROMPTS = HERE / "prompts.csv"
RUNS = HERE / "runs"
WEB2 = HERE / "web2"
PROMPTS_MORE = HERE / "prompts_more.csv"
TIDEWELL = "tidewell.example"
BRAND = "Tidewell"


def load_prompts(path=PROMPTS):
    """The course prompt set: list of dicts with id, prompt, intent, best_url."""
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def web2(*overlays):
    """The web weeks 4 to 6 work on: Tidewell with week 3's access fixes, structured
    data, and more sites. Pass your snapshot folders to lay them on top (first wins).

        web = web2("week-04/milestone/strategy/snapshot")
    """
    from aeolab.fakeweb import FakeWeb

    return FakeWeb(overlay=[*overlays, WEB2])


def load_runs(path):
    """A run file (JSON lines) -> list of dicts."""
    path = Path(path)
    if not path.is_absolute() and not path.exists():
        path = RUNS / path
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def save_runs(rows, path):
    Path(path).write_text("".join(json.dumps(r) + "\n" for r in rows))


def load_pages(web=None):
    """Every page on disk as {url: html}, ignoring robots.txt, status codes and
    everything else a crawler obeys. Week 1 builds an engine on this; week 3 finds
    out what a real crawler would not have seen."""
    from aeolab.fakeweb import FakeWeb

    web = web or FakeWeb()
    pages = {}
    for domain in web.domains():
        for url in web.page_urls(domain):
            r = web.fetch(url, render_js=True, user_agent="Mozilla/5.0 (course loader)")
            if r.status == 200:
                pages[url] = r.text
            else:  # redirects and server blocks: read the file directly
                for root in web.roots:
                    from aeolab.fakeweb import path_to_file, split_url
                    d, p = split_url(url)
                    f = root / d / path_to_file(p)
                    if f.is_file():
                        pages[url] = f.read_text()
                        break
    return pages
