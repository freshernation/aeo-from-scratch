import re

SECTIONS = (("Summary", 40), ("The three runs", 60), ("Rerun against baseline", 50),
            ("Fixed against baseline", 50), ("Decision", 60))


def part(text, heading):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


def test_instructions_removed(source):
    assert "<!--" not in source("VISIBILITY_REPORT.md"), "Delete the instructions comment."


def test_sections(source):
    text = source("VISIBILITY_REPORT.md")
    for heading, words in SECTIONS:
        assert f"## {heading}" in text, f"No '{heading}' section."
        assert len(part(text, heading).split()) >= words, f"'{heading}' needs {words} words."


def test_the_numbers(source):
    text = source("VISIBILITY_REPORT.md")
    rerun, fixed = part(text, "Rerun against baseline"), part(text, "Fixed against baseline")
    assert "9" in rerun and "8" in rerun, "rerun: 9 better, 8 worse"
    assert re.search(r"1\.0", rerun), "rerun: sign test p = 1.0"
    assert "15" in fixed and "4" in fixed, "fixed: 15 better, 4 worse"
    assert re.search(r"0\.0(19|2)", fixed), "fixed: sign test p = 0.019"


def test_decision(source):
    d = part(source("VISIBILITY_REPORT.md"), "Decision").lower()
    assert "noise" in d and "real" in d, "say which difference is noise and which is real"
