import json
import re
import sys
from datetime import date
from pathlib import Path

from site_checks import SITE, check_sections, part

sys.path.insert(0, str(Path(__file__).parents[1]))
import measure  # noqa: E402


def results():
    f = SITE / "results.json"
    assert f.exists(), "run python3 week-08/measure.py"
    return json.loads(f.read_text())


def test_results_are_current():
    r = results()
    fresh = measure.compute()
    assert {k: v for k, v in r.items() if k != "date"} == fresh, \
        "results.json does not match your site as it is now - run measure.py again"


def test_case_study(source):
    text = source("CASE_STUDY.md")
    check_sections(text, (("Summary", 60), ("The questions", 40), ("What was wrong", 60), ("What I changed", 50),
                          ("The numbers", 60), ("What this does not show", 60)))
    r = results()["engines"]["panel"]
    nums = part(text, "The numbers")
    assert f"{100 * r['first'][0]:.1f}" in nums and f"{100 * r['first'][1]:.1f}" in nums, \
        "quote the panel's first-cited rates from results.json as percentages to one decimal"


def test_remeasure(source):
    text = source("REMEASURE.md")
    check_sections(text, (("When", 20), ("What", 40), ("What would change my mind", 30)))
    when = re.search(r"\d{4}-\d{2}-\d{2}", part(text, "When"))
    assert when, "write the date as YYYY-MM-DD"
    measured = date.fromisoformat(results()["date"])
    assert (date.fromisoformat(when.group(0)) - measured).days >= 30, "at least 30 days after you measured"
    block = re.search(r"```json\n(.*?)```", part(text, "The config"), re.S)
    assert block, "a ```json block"
    cfg = json.loads(block.group(1))
    for key in ("domain", "prompts", "engines", "samples", "temperature", "budget_usd", "store", "prices"):
        assert key in cfg, f"the config needs {key}"
