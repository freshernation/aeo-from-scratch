import pytest
from aeolab import web2
from aeolab.panel import Panel


def test_extract(load):
    f = load("facts.py")
    assert f.extract_facts("The UX3 costs $189 and lasts 3,000 litres or six months; certified to "
                           "NSF/ANSI 53 since 2016, 99% lead.") == [
        ("price", "$189"), ("volume", "3,000 litres"), ("standard", "NSF/ANSI 53"), ("year", "2016"), ("percent", "99%")]


def test_trailing_comma_is_not_part_of_a_price(load):
    assert load("facts.py").extract_facts("the best under $150, with $1,299.00 for the big one") == [
        ("price", "$150"), ("price", "$1,299.00")]


def test_hyphens_and_overlap(load):
    f = load("facts.py")
    assert f.extract_facts("A 2.4-litre pitcher with a 2-year warranty") == [("volume", "2.4-litre"), ("duration", "2-year")]
    assert f.extract_facts("NSF/ANSI Standard 58") == [("standard", "NSF/ANSI Standard 58")]


def test_density(load):
    f = load("facts.py")
    assert f.fact_density("It costs $34 and lasts 150 litres.") == pytest.approx(100 * 2 / 7)
    assert f.fact_density("") == 0.0
    assert f.first_sentence_has_fact("Buy it. It costs $34.") is False


def test_finding_tidewell_says_less(load):
    f = load("facts.py")
    by = {}
    for p in Panel(web2()).passages:
        by.setdefault(p.domain, []).append({"text": p.text})
    tw, cf = f.site_facts(by["tidewell.example"]), f.site_facts(by["clearflow.example"])
    assert (round(tw[0], 2), round(tw[1], 2)) == (2.95, 0.2)
    assert (round(cf[0], 2), round(cf[1], 2)) == (7.7, 0.57), \
        "ClearFlow carries 2.6 times the facts per word, and puts one in the first sentence 57% of the time to Tidewell's 20%"
