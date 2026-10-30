import re


def part(text, heading):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).split(f"## {heading}", 1)[1].split("\n## ")[0]


def test_written(source):
    text = source("ENTITY.md")
    assert "<!--" not in text, "Delete the instructions comment."
    for heading, words in (("The facts", 40), ("Where they differ", 60), ("Corrections", 80),
                           ("What sameAs can and cannot do", 50)):
        assert len(part(text, heading).split()) >= words, f"'{heading}' needs {words} words."


def test_the_facts(source):
    facts = part(source("ENTITY.md"), "The facts")
    assert re.search(r"^Name: Tidewell Water Co\.", facts, re.M)
    assert re.search(r"^Founded: 2016", facts, re.M) and re.search(r"^City: Portland", facts, re.M)


def test_the_odd_one_out(source):
    differ = part(source("ENTITY.md"), "Where they differ")
    for needle in ("waterdirectory.example", "Seattle", "2015", "TideWell Inc."):
        assert needle in differ, f"'Where they differ' should mention {needle}"
