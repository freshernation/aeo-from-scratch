import re

from aeolab import load_prompts, web2
from aeolab.engine_b import EngineB
from aeolab.panel import Panel
from rewrite_checks import SNAPSHOT, doc_sections, paired_first


def test_wins_on_the_panel_without_losing_on_b():
    prompts = load_prompts()
    for engine, must_win in ((Panel, True), (EngineB, False)):
        p = paired_first(engine(web2()).run(prompts, 20, 0.3, seed=4), engine(web2(SNAPSHOT)).run(prompts, 20, 0.3, seed=4))
        if must_win:
            assert p["p"] < 0.05 and p["wins"] > p["losses"], f"panel, first-cited by prompt: {p}"
        else:
            assert not (p["p"] < 0.05 and p["losses"] > p["wins"]), f"your rewrite hurts on Engine B: {p}"


def test_written(source):
    text = source("LIFT.md")
    problem = doc_sections(text, (("The numbers", 60), ("Why they differ", 80), ("A prompt that went the wrong way", 60)))
    assert problem is None, problem
    nums = text.split("## The numbers", 1)[1].split("\n## ")[0]
    assert len(re.findall(r"\d+(\.\d+)?\s?%", nums)) >= 4, "at least four percentages"
    assert re.search(r"P\d\d", text.split("## A prompt that went the wrong way", 1)[1]), "name the prompt by id"
