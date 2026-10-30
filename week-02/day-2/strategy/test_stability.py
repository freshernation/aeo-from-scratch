import re

from aeolab import load_runs

ROWS = [{"prompt_id": p, "cited_domains": d} for p, d in
        [("A", ["t"]), ("A", ["t"]), ("B", ["t"]), ("B", []), ("C", []), ("C", [])]]


def test_counts(load):
    assert load("stability.py").cited_counts(ROWS, "t") == {"A": (2, 2), "B": (1, 2), "C": (0, 2)}


def test_unstable(load):
    assert load("stability.py").unstable(ROWS, "t") == ["B"]


def test_finding(load):
    u = load("stability.py").unstable(load_runs("baseline.jsonl"), "tidewell.example")
    assert len(u) == 19, f"{len(u)} unstable prompts; expected 19 of 30"


def test_written(source):
    text = source("STABILITY.md")
    assert "<!--" not in text, "Delete the instructions comment in STABILITY.md."
    for heading, words in (("The unstable prompts", 60), ("How many samples", 60),
                           ("What a single screenshot proves", 50)):
        assert f"## {heading}" in text, f"STABILITY.md has no '{heading}' section."
        part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(part.split()) >= words, f"'{heading}' is {len(part.split())} words; it needs {words}."
    assert "19" in text.split("## The unstable prompts", 1)[1].split("\n## ")[0], "say how many: 19 of 30"
    assert re.search(r"\d+ samples", text), "name a number of samples"
