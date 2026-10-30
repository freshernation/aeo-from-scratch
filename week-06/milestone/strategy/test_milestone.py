import re

from strategy_checks import check_sections, part


def test_written(source):
    text = source("AUDIT_REPORT.md")
    check_sections(text, (("Summary", 80), ("Access", 60), ("Content", 60), ("Structured data", 50), ("Off-site", 80),
                          ("Competitors' tactics", 50), ("What we will measure next", 50)))


def test_the_evidence(source):
    text = source("AUDIT_REPORT.md")
    assert "403" in part(text, "Access") and re.search(r"\d+(\.\d+)?%", part(text, "Access"))
    assert re.search(r"\d+(\.\d+)?%", part(text, "Content"))
    assert "$29" in part(text, "Structured data") or "29.00" in part(text, "Structured data")
    off = part(text, "Off-site")
    for needle in ("$149", "100 litres", "Seattle"):
        assert needle in off, f"'Off-site' should mention {needle}"
    tactics = part(text, "Competitors' tactics")
    assert "hidden" in tactics.lower() and "cloak" in tactics.lower()
    fixes = re.findall(r"^\d+\.", part(text, "Fix order"), re.M)
    assert len(fixes) >= 8, f"{len(fixes)} fixes; at least eight"
