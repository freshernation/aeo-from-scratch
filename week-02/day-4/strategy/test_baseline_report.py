import re

SECTIONS = (("Summary", 40), ("The numbers", 60), ("By intent", 50), ("How sure we are", 60),
            ("What this does not tell us", 50))


def part(text, heading):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


def test_instructions_removed(source):
    assert "<!--" not in source("BASELINE_REPORT.md"), "Delete the instructions comment."


def test_sections(source):
    text = source("BASELINE_REPORT.md")
    for heading, words in SECTIONS:
        assert f"## {heading}" in text, f"No '{heading}' section."
        assert len(part(text, heading).split()) >= words, f"'{heading}' needs {words} words."


def test_numbers_are_right(source):
    text = source("BASELINE_REPORT.md")
    assert re.search(r"73(\.0)?\s?%", part(text, "Summary")), "the headline: cited in 73% of answers"
    assert len(re.findall(r"\d+(\.\d+)?\s?%", part(text, "The numbers"))) >= 3
    sure = part(text, "How sure we are")
    assert "61" in sure and "84" in sure, "give the interval resampled over prompts"
    assert "prompt" in sure.lower()
