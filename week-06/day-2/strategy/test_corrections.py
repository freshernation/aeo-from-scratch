from strategy_checks import check_sections, part


def test_written(source):
    text = source("CORRECTIONS.md")
    check_sections(text, (("Summary", 40), ("Requests", 100), ("On Tidewell's own site", 60), ("What we cannot control", 40)))
    rows = [l for l in part(text, "The contradictions").splitlines() if l.startswith("|") and not l.startswith(("| Page", "|---"))]
    assert len(rows) >= 3, "at least three contradictions: the UX3 price, the cartridge life, the company's details"
    table = "\n".join(rows)
    for needle in ("filterreviews.example", "waterforum.example", "waterdirectory.example", "$149", "$189", "100", "150", "Seattle"):
        assert needle in table, f"the table should include {needle}"
