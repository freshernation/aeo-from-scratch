from strategy_checks import check_sections, part


def test_written(source):
    text = source("DRIFT.md")
    check_sections(text, (("The weeks", 40), ("The alerts", 40), ("What happened", 60), ("What a weekly check cannot see", 50)))
    alerts = part(text, "The alerts")
    assert "2026-08-24" in alerts or "24 August" in alerts, "the drop"
    assert "2026-09-07" in alerts or "7 September" in alerts, "the recovery"
