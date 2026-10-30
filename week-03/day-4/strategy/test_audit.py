import re

SECTIONS = (("Summary", 40), ("Blocked by robots.txt", 50), ("Blocked by the server", 50),
            ("Not indexable", 40), ("Not in the HTML", 40), ("Fix order", 80))


def part(text, heading):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


def test_instructions_removed(source):
    assert "<!--" not in source("ACCESS_AUDIT.md"), "Delete the instructions comment."


def test_sections(source):
    text = source("ACCESS_AUDIT.md")
    for heading, words in SECTIONS:
        assert f"## {heading}" in text, f"No '{heading}' section."
        assert len(part(text, heading).split()) >= words, f"'{heading}' needs {words} words."


def test_the_facts(source):
    text = source("ACCESS_AUDIT.md")
    server = part(text, "Blocked by the server")
    assert "403" in server and "Claude-SearchBot" in server and "PerplexityBot" in server
    assert re.search(r"\b19\b", part(text, "Summary") + server), "say how many pages: all 19"
    fixes = re.findall(r"^\d+\.", part(text, "Fix order"), re.M)
    assert len(fixes) >= 4, "a numbered list of at least four fixes"
