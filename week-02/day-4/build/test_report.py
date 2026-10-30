from aeolab import load_prompts, load_runs


def loaded(load):
    for f in ("metrics.py", "sampling.py", "stats.py", "stability_check.py"):
        load(f)
    return load("report.py")


def test_pct(load):
    assert loaded(load).pct(0.73) == "73.0%" and loaded(load).pct(1) == "100.0%"


def test_by_intent(load):
    r = loaded(load).by_intent(load_runs("baseline.jsonl"), load_prompts(), "tidewell.example")
    assert list(r) == ["brand", "commercial", "comparison", "howto", "informational"]
    assert round(r["brand"], 3) == 0.921 and round(r["commercial"], 3) == 0.35


def test_report(load):
    text = loaded(load).report(load_runs("baseline.jsonl"), load_prompts(), "tidewell.example", "Tidewell")
    assert text.startswith("# Visibility report\n")
    heads = [l for l in text.splitlines() if l.startswith("## ")]
    assert heads == ["## Summary", "## By site", "## By intent", "## Noise"]
    assert ("Tidewell is cited in 73.0% of 600 answers (61.0% to 84.0%, 95% bootstrap over 30 prompts) "
            "and cited first in 21.5%.") in text
    assert "| clearflow.example | 76.7% | 36.3% | 31.2% |" in text, "the By site row for ClearFlow"
    assert "| brand | 92.1% |" in text
    assert "19 of 30 prompts cite Tidewell on some samples and not others." in text
