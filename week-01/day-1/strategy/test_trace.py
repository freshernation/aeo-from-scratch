import re

IDS = ["P01", "P03", "P04", "P07", "P08", "P10", "P13", "P18", "P22", "P26"]
STEPS = ("rrf", "retrieval", "self_contained", "answer_first", "specific", "corroborated",
         "fresh", "crawl", "candidate", "fan-out", "boost")


def section(text, heading):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


def test_instructions_removed(source):
    assert "<!--" not in source("TRACE.md"), "Delete the instructions comment in TRACE.md."


def test_every_prompt_traced(source):
    text = source("TRACE.md")
    for pid in IDS:
        assert f"## {pid}" in text, f"TRACE.md has no '{pid}' section."
        part = section(text, pid)
        assert len(part.split()) >= 40, f"{pid} is {len(part.split())} words; it needs 40."
        assert re.search(r"[a-z]+\.example", part), f"{pid} names no page - quote the URL that won."
        assert any(s in part.lower() for s in STEPS), \
            f"{pid} does not say WHY it won: name the boost, or say it was retrieval (rrf)."


def test_pattern(source):
    part = section(source("TRACE.md"), "What I noticed")
    assert len(part.split()) >= 80, f"'What I noticed' is {len(part.split())} words; it needs 80."
