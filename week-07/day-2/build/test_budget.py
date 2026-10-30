import pytest
from aeolab import HERE

PRICES = {"engines": {"a": {"search_per_1k": 10.0, "input_per_mtok": 4.0, "output_per_mtok": 20.0},
                      "b": {"search_per_1k": 5.0, "input_per_mtok": 1.0, "output_per_mtok": 1.0},
                      "free": {"search_per_1k": 0.0, "input_per_mtok": 0.0, "output_per_mtok": 0.0},
                      "x": {"search_per_1k": None, "input_per_mtok": 1.0, "output_per_mtok": 1.0}},
          "assumptions": {"searches_per_answer": 2, "input_tokens_per_answer": 8000, "output_tokens_per_answer": 600}}


def test_cost_per_answer(load):
    b = load("budget.py")
    assert b.cost_per_answer(PRICES, "a") == pytest.approx(0.064)
    assert b.cost_per_answer(PRICES, "free") == 0.0
    assert b.cost_per_answer(PRICES, "x") is None, "unpriced is not free"


def test_run_cost(load):
    b = load("budget.py")
    assert b.run_cost(PRICES, ["a", "b"], 30, 10) == 19.2 + round(0.0186 * 300, 2)
    assert b.run_cost(PRICES, ["a", "x"], 30, 10) is None


def test_max_samples(load):
    b = load("budget.py")
    assert b.max_samples(PRICES, ["a"], 30, 50) == 26
    assert b.max_samples(PRICES, ["free"], 30, 50) is None
    assert b.unpriced(PRICES, ["a", "x", "free"]) == ["x"]


def test_finding_what_week_2_costs_live(load):
    b = load("budget.py")
    prices = b.load_prices(HERE / "data" / "prices.json")
    assert b.run_cost(prices, ["claude"], 30, 10) == 19.2, "week 2's ten samples per prompt, on Claude: $19.20 a run"
    assert b.run_cost(prices, ["panel", "engine_b"], 30, 10) == 0.0
    assert b.unpriced(prices, ["claude", "openai", "perplexity"]) == ["openai", "perplexity"], \
        "two of three live engines cannot be planned until someone fills in their prices"
