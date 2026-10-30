import re
import sys
from pathlib import Path

from aeolab import load_prompts, web2
from aeolab.engine_b import EngineB
from aeolab.fakeweb import FakeWeb
from aeolab.panel import Panel

sys.path.insert(0, str(Path(__file__).parents[2]))
from rewrite_checks import doc_sections, rewrite_problems  # noqa: E402

FILES = ("passages.py", "bm25.py", "cite.py", "fanout.py", "robots.py", "fetchcheck.py", "sitemap.py", "boosts.py")


def mod(load):
    for f in FILES:
        load(f)
    return load("engine2.py")


def test_crawl_obeys_access(load):
    pages = mod(load).crawl(FakeWeb(), "MyEngine")
    assert len(pages) == 43, f"{len(pages)} pages; the panel's crawler indexes 43 on the original web"
    assert "https://tidewell.example/learn/lead-in-water" not in pages and "https://tidewell.example/faq" in pages


def test_answer_and_run(load):
    e = mod(load).Engine(web2())
    a = e.answer("Do water filters remove lead?")
    assert set(a) == {"sentences", "citations", "unsupported"} and len(a["citations"]) == 4
    rows = e.run(load_prompts()[:2], samples=3, temperature=0.3, seed=1)
    assert len(rows) == 6 and set(rows[0]) == {"run_id", "prompt_id", "sample", "cited_urls", "cited_domains", "answer"}
    assert e.answer("Which water filters remove PFAS?") == e.answer("Which water filters remove PFAS?")


def test_finding_three_engines_three_opinions(load):
    e = mod(load).Engine(web2())
    p, b = Panel(web2()), EngineB(web2())
    urls = lambda engine, q: {c.url for c in engine.ask(q).citations}
    mine_panel = mine_b = panel_b = 0
    for x in load_prompts():
        m = set(e.answer(x["prompt"])["citations"])
        mine_panel += len(m & urls(p, x["prompt"]))
        mine_b += len(m & urls(b, x["prompt"]))
        panel_b += len(urls(p, x["prompt"]) & urls(b, x["prompt"]))
    assert (mine_panel, mine_b, panel_b) == (74, 54, 63), (mine_panel, mine_b, panel_b)


def test_my_rewrite():
    assert rewrite_problems("/learn/lead-in-water", folder=Path(__file__).parent / "mine") == []


def test_report(source):
    text = source("ENGINE_REPORT.md")
    problem = doc_sections(text, (("Three engines", 40), ("The fixtures", 60), ("My rewrite", 60),
                                  ("What my engine still gets wrong", 50)))
    assert problem is None, problem
    three = text.split("## Three engines", 1)[1].split("\n## ")[0]
    assert all(n in three for n in ("74", "54", "63")), "give the three shared-citation counts"
