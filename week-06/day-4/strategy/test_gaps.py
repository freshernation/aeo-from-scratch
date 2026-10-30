import re

from strategy_checks import check_sections, part


def test_written(source):
    text = source("COMPETITOR_GAPS.md")
    check_sections(text, (("Summary", 40), ("Out-scored", 80), ("Not retrieved", 60), ("Who wins first", 50),
                          ("What to change first", 60)))
    s = part(text, "Summary")
    assert "17" in s and "12" in s and re.search(r"\b4\b", s), "17 cited, 12 out-scored, 4 not retrieved"
    assert len(set(re.findall(r"P\d\d", part(text, "Out-scored")))) >= 2
    assert "clearflow.example" in part(text, "Who wins first").lower() or "ClearFlow" in part(text, "Who wins first")
