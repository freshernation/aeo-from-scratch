"""Week 4 checks shared by the rewrite labs. Given; the tests import it.

The Strategists' rewrites live in week-04/snapshot/tidewell.example/; the tests lay
that folder over aeolab.web2() and run the engines on the result.
"""
import re
from pathlib import Path

from bs4 import BeautifulSoup

from aeolab import web2
from aeolab.panel import split_passages

SNAPSHOT = Path(__file__).parent / "snapshot"
NUMBER = re.compile(r"\d[\d,.]*\d|\d")
PRONOUNS = ("it", "this", "they", "these", "those", "that")


def visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "nav", "header", "footer", "title", "time"]):
        t.decompose()
    return " ".join((soup.find("main") or soup).get_text(" ", strip=True).split())


def numbers(text):
    return {n.rstrip(".,") for n in NUMBER.findall(text)}


def site_numbers():
    web = web2()
    out = set()
    for url in web.page_urls("tidewell.example"):
        out |= numbers(visible_text(web.fetch(url, render_js=True).text))
    return out


def rewrite_problems(path, folder=SNAPSHOT):
    """Everything wrong with one rewritten page, as a list of sentences. [] is good."""
    url = "https://tidewell.example" + path
    rel = path.strip("/") + ".html"
    mine = (folder / "tidewell.example" / rel).read_text()
    original = web2().fetch(url).text
    problems = []
    if visible_text(mine) == visible_text(original):
        return [f"{path} has not been rewritten yet"]
    invented = numbers(visible_text(mine)) - site_numbers()
    if invented:
        problems.append(f"{path}: numbers that appear nowhere on Tidewell's site: {sorted(invented)} - move facts, do not invent them")
    for p in split_passages(url, mine):
        words = p.text.split()
        first = re.split(r"(?<=[.!?])\s+", p.text, maxsplit=1)[0]
        if words and words[0].lower().strip(",.:") in PRONOUNS:
            problems.append(f"{path} [{p.heading}] opens with '{words[0]}'")
        if len(first.split()) > 30:
            problems.append(f"{path} [{p.heading}] first sentence is {len(first.split())} words; 30 at most")
        if len(words) < 12:
            problems.append(f"{path} [{p.heading}] is {len(words)} words; under 12 the panel drops it")
    return problems


def best_cited(engine, prompts):
    """{prompt id: is its best_url among the citations}, at temperature 0."""
    return {x["id"]: x["best_url"] in [c.url for c in engine.ask(x["prompt"]).citations] for x in prompts}



def paired_first(before, after, domain="tidewell.example"):
    """Week 2's paired sign test, on first-cited, prompt by prompt."""
    import math
    from collections import defaultdict

    rate = lambda rows: {p: sum(v) / len(v) for p, v in _group(rows, domain).items()}
    a, b = rate(before), rate(after)
    wins = sum(b[p] > a[p] for p in a)
    losses = sum(b[p] < a[p] for p in a)
    n, k = wins + losses, min(wins, losses)
    p = 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)
    return {"wins": wins, "losses": losses, "p": p}


def _group(rows, domain):
    from collections import defaultdict
    g = defaultdict(list)
    for r in rows:
        g[r["prompt_id"]].append(r["cited_domains"][:1] == [domain])
    return g


def doc_sections(text, spec):
    """spec: ((heading, min words), ...). Returns the first problem, or None."""
    if "<!--" in text:
        return "delete the instructions comment"
    clean = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for heading, words in spec:
        if f"## {heading}" not in clean:
            return f"no '{heading}' section"
        part = clean.split(f"## {heading}", 1)[1].split("\n## ")[0]
        if len(part.split()) < words:
            return f"'{heading}' is {len(part.split())} words; it needs {words}"
    return None
