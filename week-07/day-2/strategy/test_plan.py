import re

import pytest
from strategy_checks import check_sections, part


def test_monthly_cost(load):
    p = load("plan.py")
    assert p.monthly_cost(30, 10, {"claude": 0.064}, 52 / 12) == 83.2
    assert p.monthly_cost(30, 10, {"claude": 0.064, "pplx": None}, 4) is None
    assert p.monthly_cost(30, 10, {"panel": 0.0}, 4) == 0.0


def test_affordable(load):
    p = load("plan.py")
    assert p.affordable_samples(30, {"claude": 0.064}, 52 / 12, 100) == 12
    assert p.affordable_samples(30, {"panel": 0.0}, 4, 100) is None


def test_written(source):
    text = source("SAMPLING_PLAN.md")
    check_sections(text, (("The plan", 60), ("The cost", 50), ("What we cannot price", 40), ("What we give up", 50)))
    assert re.search(r"\$\d", part(text, "The cost"))
    cannot = part(text, "What we cannot price").lower()
    assert "perplexity" in cannot and "openai" in cannot
