from strategy_checks import check_sections, part


def test_written(source):
    text = source("FRESHNESS.md")
    check_sections(text, (("Stale pages", 60), ("Hidden instructions", 60), ("Cloaking", 60),
                          ("What Tidewell should do", 60), ("What Tidewell must never do", 50)))
    assert "microplastics" in part(text, "Stale pages") and "2021" in part(text, "Stale pages")
    assert "aquaminder.example" in part(text, "Hidden instructions")
    assert "purepath.example" in part(text, "Cloaking") and "100%" in part(text, "Cloaking"), \
        "quote what the cloaked page tells crawlers"
