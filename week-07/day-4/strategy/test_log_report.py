from strategy_checks import check_sections, part


def test_written(source):
    text = source("LOG_REPORT.md")
    check_sections(text, (("Who came", 60), ("Who pretended", 50), ("Before and after the fix", 50), ("Who sent people", 50),
                          ("What logs cannot tell us", 40)))
    assert "400" in part(text, "Who pretended") and "GPTBot" in part(text, "Who pretended")
    assert "403" in part(text, "Before and after the fix")
    assert "73" in part(text, "Who sent people") and "ChatGPT" in part(text, "Who sent people")
