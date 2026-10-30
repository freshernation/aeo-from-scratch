"""Given. Section checks shared by week 6's Strategist tests."""
import re


def part(text, heading):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).split(f"## {heading}", 1)[1].split("\n## ")[0]


def check_sections(text, spec):
    assert "<!--" not in text, "Delete the instructions comment."
    for heading, words in spec:
        assert f"## {heading}" in re.sub(r"<!--.*?-->", "", text, flags=re.S), f"No '{heading}' section."
        n = len(part(text, heading).split())
        assert n >= words, f"'{heading}' is {n} words; it needs {words}."
