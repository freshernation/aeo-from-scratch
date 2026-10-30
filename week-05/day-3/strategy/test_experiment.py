import re


def part(text, heading):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).split(f"## {heading}", 1)[1].split("\n## ")[0]


def test_written(source):
    text = source("SCHEMA_EXPERIMENT.md")
    assert "<!--" not in text, "Delete the instructions comment."
    for heading, words in (("What Google says", 40), ("What the experiment did", 50), ("What changed", 40),
                           ("What this cannot tell us", 80)):
        assert len(part(text, heading).split()) >= words, f"'{heading}' needs {words} words."
    assert "no additional requirements" in part(text, "What Google says"), "quote Google's sentence"
    assert re.search(r"\b0\b", part(text, "What changed")), "report the count of changed answers"
