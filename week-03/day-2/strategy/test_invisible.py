import re

from aeolab.fakeweb import FakeWeb
from aeolab.panel import Panel

REASONS = {"robots": "robots", "noindex-meta": "noindex", "noindex-header": "noindex",
           "no-text": "javascript", "canonical-elsewhere": "canonical"}


def rows(text):
    out = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and cells and cells[0].startswith("https://"):
            out.append(cells)
    return out


def test_every_invisible_page_found(source):
    panel = Panel()
    truth = {u: REASONS[panel.readable(u)[1]] for u in FakeWeb().page_urls("tidewell.example")
             if not panel.readable(u)[0]}
    found = {r[0]: r[1].lower() for r in rows(source("INVISIBLE.md"))}
    missing = sorted(set(truth) - set(found))
    extra = sorted(set(found) - set(truth))
    assert not missing, f"{len(missing)} invisible page(s) not listed yet"
    assert not extra, f"these are readable by the panel: {extra}"
    wrong = [u for u in truth if truth[u] not in found[u]]
    assert not wrong, f"check the reason for {wrong}"


def test_fixes(source):
    for r in rows(source("INVISIBLE.md")):
        assert len(r) >= 3 and len(r[2].split()) >= 1, f"{r[0]} needs a fix, or 'none'"
    canon = [r for r in rows(source("INVISIBLE.md")) if "canonical" in r[1].lower()]
    assert canon and canon[0][2].lower().startswith("none"), \
        "the Harbour Blue page points at the main pitcher page on purpose - that one needs no fix"


def test_written(source):
    text = source("INVISIBLE.md")
    assert "<!--" not in text, "Delete the instructions comment."
    part = text.split("## What surprised me", 1)[1]
    assert len(part.split()) >= 60
