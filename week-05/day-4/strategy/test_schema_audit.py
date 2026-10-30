import re


def part(text, heading):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).split(f"## {heading}", 1)[1].split("\n## ")[0]


def test_written(source):
    text = source("SCHEMA_AUDIT.md")
    assert "<!--" not in text, "Delete the instructions comment."
    for heading, words in (("Summary", 40), ("Tidewell", 60), ("Competitors", 60), ("Valid is not true", 40), ("Fix order", 40)):
        assert len(part(text, heading).split()) >= words, f"'{heading}' needs {words} words."


def test_the_findings(source):
    text = source("SCHEMA_AUDIT.md")
    assert "29" in part(text, "Valid is not true") and "34" in part(text, "Valid is not true")
    comp = part(text, "Competitors")
    assert "PurePath" in comp and re.search(r"invalid|not valid|broken", comp, re.I)
    assert "offers" in comp, "AquaMinder's Product has no offers"
    assert len(re.findall(r"^\d+\.", part(text, "Fix order"), re.M)) >= 3
