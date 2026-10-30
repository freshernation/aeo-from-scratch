"""Day 3: the FAQ - every heading a question, every answer in its first sentence."""
import re

from aeolab import load_prompts, web2
from aeolab.panel import Panel, split_passages, tokenize
from rewrite_checks import SNAPSHOT, doc_sections, rewrite_problems


def passages():
    html = (SNAPSHOT / "tidewell.example" / "faq.html").read_text()
    return split_passages("https://tidewell.example/faq", html)


def test_faq_rewritten():
    assert rewrite_problems("/faq") == []


def test_questions_answered_first():
    for p in passages():
        assert p.heading.endswith("?"), f"'{p.heading}' is not a question"
        first = re.split(r"(?<=[.!?])\s+", p.text, maxsplit=1)[0]
        assert set(tokenize(p.heading)) & set(tokenize(first)), f"'{p.heading}': the first sentence does not answer it"


def test_fluoride_answer_now_first(snapshot_web):
    x = next(x for x in load_prompts() if x["id"] == "P11")
    cited = [c.url for c in Panel(snapshot_web).ask(x["prompt"]).citations]
    assert cited[0].startswith("https://tidewell.example/") and "https://tidewell.example/faq" in cited, \
        f"P11 asks whether the Tidewell Pitcher removes fluoride: a Tidewell page should be the first source (PurePath's was), with the FAQ cited. Got {cited}"


def test_before_after(source):
    problem = doc_sections(source("BEFORE_AFTER.md"), (("FAQ", 80),))
    assert problem is None, problem
