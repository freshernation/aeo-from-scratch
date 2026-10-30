"""Given. Run both engines three ways and count how many answers change.

    python3 week-05/day-3/strategy/show_experiment.py

  as is      web2 as it stands
  stripped   every piece of JSON-LD on every site removed
  yours      your week-05/snapshot/ laid over web2 (your markup)
"""
import re
import tempfile
from pathlib import Path

from aeolab import load_prompts, web2
from aeolab.engine_b import EngineB
from aeolab.panel import Panel

SNAP = Path(__file__).parents[2] / "snapshot"
JSONLD = re.compile(r'\s*<script type="application/ld\+json">.*?</script>', re.S)


def stripped_folder():
    folder = Path(tempfile.mkdtemp())
    web = web2()
    for d in web.domains():
        for url in web.page_urls(d):
            r = web.fetch(url)
            if r.status == 200 and "ld+json" in r.text:
                rel = url.split(d, 1)[1].strip("/") or "index"
                out = folder / d / (rel + ".html")
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(JSONLD.sub("", r.text))
    return folder


def changed(a, b):
    return sum(x["cited_urls"] != y["cited_urls"] for x, y in zip(a, b))


def main():
    prompts = load_prompts()
    stripped = stripped_folder()
    for engine in (Panel, EngineB):
        base = engine(web2()).run(prompts, 20, 0.3, seed=4)
        none = engine(web2(stripped)).run(prompts, 20, 0.3, seed=4)
        yours = engine(web2(SNAP)).run(prompts, 20, 0.3, seed=4)
        print(f"{engine.__name__:8} answers changed of {len(base)}:  stripped {changed(base, none)}   yours {changed(base, yours)}")


if __name__ == "__main__":
    main()
