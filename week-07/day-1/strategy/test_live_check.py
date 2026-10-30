import re

from strategy_checks import check_sections, part


def test_written(source):
    text = source("LIVE_CHECK.md")
    check_sections(text, (("Live or fixture", 40), ("What they cited", 80), ("Against the panel", 60),
                          ("What I would check live first", 60)))
    which = part(text, "Live or fixture").lower()
    assert "live" in which or "fixture" in which
    if "fixture" in which:
        assert "invented" in which, "say that the fixtures' content is invented"
    assert re.search(r"utm_|#|trailing", part(text, "What they cited")), "show how one page arrives as different strings"
    assert len(re.findall(r"^\d+\.|^- ", part(text, "What I would check live first"), re.M)) >= 3
