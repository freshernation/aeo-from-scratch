import re
import sys
from pathlib import Path

from aeolab import load_prompts, web2
from aeolab.engine_b import EngineB
from aeolab.panel import Panel

sys.path.insert(0, str(Path(__file__).parents[2]))
from rewrite_checks import SNAPSHOT, best_cited, doc_sections, paired_first, rewrite_problems  # noqa: E402

PAGES = ["/filters/pitcher", "/filters/shower", "/filters/under-sink", "/filters/reverse-osmosis", "/faq"]


def test_all_five_pages_clean():
    problems = [p for page in PAGES for p in rewrite_problems(page)]
    assert problems == [], "\n".join(problems)


def test_best_pages_cited():
    got = best_cited(Panel(web2(SNAPSHOT)), load_prompts())
    assert sum(got.values()) >= 19, f"the panel cites Tidewell's best page on {sum(got.values())} of 30 (15 before); aim for 19"


def test_lift_on_both_engines():
    prompts = load_prompts()
    panel = paired_first(Panel(web2()).run(prompts, 20, 0.3, seed=4), Panel(web2(SNAPSHOT)).run(prompts, 20, 0.3, seed=4))
    b = paired_first(EngineB(web2()).run(prompts, 20, 0.3, seed=4), EngineB(web2(SNAPSHOT)).run(prompts, 20, 0.3, seed=4))
    assert panel["p"] < 0.05 and panel["wins"] >= 15, f"panel: {panel}"
    assert b["wins"] >= b["losses"], f"Engine B: {b} - a rewrite that loses on one engine is not done"


def test_written(source):
    text = source("PROJECT1.md")
    problem = doc_sections(text, (("Summary", 40), ("The numbers", 60), ("Two engines", 80), ("What I would not claim", 60)))
    assert problem is None, problem
    rows = [l for l in text.split("## The five pages", 1)[1].split("\n## ")[0].splitlines()
            if l.startswith("|") and not l.startswith(("| Page", "|---"))]
    assert len(rows) == 5, f"{len(rows)} rows in 'The five pages'"
    assert len(re.findall(r"\d+(\.\d+)?\s?%", text.split("## The numbers", 1)[1].split("\n## ")[0])) >= 4
