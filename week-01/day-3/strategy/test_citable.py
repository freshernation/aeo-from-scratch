import pytest

GOOD = ("Do filters remove lead?",
        "Yes: filters certified to NSF/ANSI 53 reduce lead by at least 99%. Most pitchers and "
        "under-sink carbon filters carry that certification, and boiling does not remove lead.")
BAD = ("Why people love the pitcher", "It is great.")


class TestChecks:
    def test_first_sentence(self, load):
        c = load("citable.py")
        assert c.first_sentence("It is good. Buy it.") == "It is good."
        assert c.first_sentence("No full stop here") == "No full stop here"

    def test_good_passage(self, load):
        s = load("citable.py").score(*GOOD)
        assert s == {"short_first": True, "no_pronoun_start": True, "has_number": True,
                     "right_length": True, "names_subject": True, "total": 5}

    def test_bad_passage(self, load):
        s = load("citable.py").score(*BAD)
        assert s["no_pronoun_start"] is False and s["has_number"] is False and s["right_length"] is False
        assert s["names_subject"] is False, "'It is great.' shares no word with the heading"
        assert s["total"] == 1

    def test_pronoun_with_punctuation(self, load):
        assert load("citable.py").score("x", "This, of course, is it.")["no_pronoun_start"] is False

    def test_mean(self, load):
        c = load("citable.py")
        assert c.mean_score([{"heading": GOOD[0], "text": GOOD[1]}, {"heading": BAD[0], "text": BAD[1]}]) == 3.0
        assert c.mean_score([]) == 0.0


def test_finding_tidewell_scores_below_its_rivals(load, panel):
    """The day's finding: the checklist over every passage the panel indexed, by site."""
    c = load("citable.py")
    by_site = {}
    for p in panel.passages:
        by_site.setdefault(p.domain, []).append({"heading": p.heading, "text": p.text})
    means = {d: round(c.mean_score(ps), 2) for d, ps in by_site.items()}
    assert means["tidewell.example"] == 3.46
    assert means["clearflow.example"] == 3.93 and means["aquaminder.example"] == 4.17
    assert sorted(means, key=means.get)[:2] == ["waterforum.example", "tidewell.example"], \
        "only the forum writes less quotable passages than the client"
