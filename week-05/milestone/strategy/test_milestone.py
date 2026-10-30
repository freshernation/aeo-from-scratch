import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "day-1" / "strategy"))
import test_markup  # noqa: E402


def part(text, heading):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).split(f"## {heading}", 1)[1].split("\n## ")[0]


def test_markup_still_true():
    test_markup.test_pitcher_tells_the_truth()
    test_markup.test_shower_has_product_markup()
    test_markup.test_organization_is_one_entity()


def test_written(source):
    text = source("RECOMMENDATION.md")
    assert "<!--" not in text, "Delete the instructions comment."
    for heading, words in (("The question", 20), ("What we measured", 60), ("What Google says", 40),
                           ("What it is still worth", 80), ("Recommendation", 60)):
        assert len(part(text, heading).split()) >= words, f"'{heading}' needs {words} words."
    assert re.search(r"\b0\b", part(text, "What we measured"))
    assert "no additional requirements" in part(text, "What Google says")
