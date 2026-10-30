import re

from strategy_checks import check_sections, part


def test_written(source):
    text = source("MONITORING_PLAN.md")
    check_sections(text, (("What we watch", 60), ("How often", 40), ("What it costs", 40), ("Alerts and who acts", 80),
                          ("What we check by hand", 50)))
    assert re.search(r"\$\d", part(text, "What it costs"))
    alerts = part(text, "Alerts and who acts")
    assert re.search(r"p\s*<\s*0\.05|0\.05", alerts), "state the alert rule"
    assert len(re.findall(r"^\d+\.", alerts, re.M)) >= 3, "the first three checks, numbered"
