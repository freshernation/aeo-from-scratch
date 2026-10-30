import re
from pathlib import Path

from aeolab.panel import Panel

HERE = Path(__file__).parent
LINK = re.compile(r"^- \[([^\]]+)\]\((https?://[^)]+)\)(: .+)?$")


def lines():
    return (HERE / "llms.txt").read_text().splitlines()


def test_format():
    ls = [l for l in lines() if l.strip()]
    assert ls and ls[0].startswith("# "), "line 1 is the H1: '# Tidewell'"
    assert ls[1].startswith("> "), "then a '> ' summary"
    assert sum(l.startswith("## ") for l in ls) >= 2, "at least two '## ' sections"
    bad = [l for l in ls[2:] if l.startswith("-") and not LINK.match(l)]
    assert not bad, f"not in '- [title](url): note' form: {bad}"


def test_links_are_readable_tidewell_pages():
    links = [LINK.match(l).group(2) for l in lines() if LINK.match(l)]
    assert len(links) >= 6, f"{len(links)} links; at least six"
    panel = Panel()
    for u in links:
        assert u.startswith("https://tidewell.example/"), f"{u} is not a Tidewell page"
        ok, why = panel.readable(u)
        assert ok, f"{u} cannot be indexed today ({why}) - do not point agents at it"


def test_written(source):
    text = source("LLMS_NOTE.md")
    assert "<!--" not in text, "Delete the instructions comment."
    for heading, words in (("What it is", 60), ("Who reads it", 60), ("What I would tell the client", 50)):
        part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(part.split()) >= words, f"'{heading}' needs {words} words."
    assert "proposal" in text.lower(), "say what llms.txt is: a proposal, not a standard"
