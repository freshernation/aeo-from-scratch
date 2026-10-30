import re

from aeolab.llm import FakeModel


def test_gaps_shape(load, panel):
    out = load("gaps.py").gaps(panel, FakeModel(), [{"id": "X", "prompt": "Do water filters remove lead?"}])
    assert out == [{"prompt_id": "X", "subquery": "NSF 53 lead reduction filter"}], \
        "skip the first fan-out search (it is the prompt itself). Tidewell's lead page answers this one - and robots.txt hides it"


def test_other_domain(load, panel):
    out = load("gaps.py").gaps(panel, FakeModel(), [{"id": "X", "prompt": "Do water filters remove lead?"}],
                              domain="clearflow.example")
    assert out == [], "ClearFlow answers both of these searches"


def test_finding_eight_gaps(load, panel, prompts):
    out = load("gaps.py").gaps(panel, FakeModel(), prompts)
    assert len(out) == 8, f"expected 8 gaps out of 62 fan-out searches, got {len(out)}"
    assert sum(g["prompt_id"] == "P18" for g in out) == 2, "'best pitcher' has two searches with no Tidewell answer"


def test_written(source):
    text = source("GAPS.md")
    assert "<!--" not in text, "Delete the instructions comment in GAPS.md."
    for heading, words in (("The gaps", 60), ("The three to fill first", 80), ("What I cannot tell yet", 50)):
        assert f"## {heading}" in text, f"GAPS.md has no '{heading}' section."
        part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(part.split()) >= words, f"'{heading}' is {len(part.split())} words; it needs {words}."
    assert re.search(r"\d", text.split("## The gaps", 1)[1].split("\n## ")[0]), "'The gaps' needs the numbers"
