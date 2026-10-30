from aeolab import web2


def mod(load):
    load("passages.py")
    return load("lint.py")


class TestLint:
    def test_clean(self, load):
        assert mod(load).lint_passage("Lead filters",
                                      "Lead filters certified to NSF/ANSI 53 reduce lead in tap water by at least 99%.") == []

    def test_pronoun(self, load):
        assert "pronoun-opener" in mod(load).lint_passage("x", "It, of course, reduces chlorine taste in every glass of water you pour.")

    def test_long_first(self, load):
        assert "long-first-sentence" in mod(load).lint_passage("x", " ".join(["word"] * 36) + ".")

    def test_thin(self, load):
        assert mod(load).lint_passage("Price", "The pitcher costs $34.") == ["thin"]

    def test_buried(self, load):
        codes = mod(load).lint_passage("Cartridges", "We know you are busy and want things simple. Cartridges last 150 litres each and cost $12.")
        assert codes == ["buried-answer"], codes

    def test_order(self, load):
        assert mod(load).lint_passage("Cartridges", "It is easy. Cartridges are cheap.") == ["pronoun-opener", "thin", "buried-answer"]


def test_finding_three_times_the_problems(load):
    lint = mod(load)
    web = web2()
    t, c = lint.flag_rate(web, "tidewell.example"), lint.flag_rate(web, "clearflow.example")
    assert (round(t, 3), round(c, 3)) == (0.423, 0.133), \
        "42% of Tidewell's passages have at least one problem; 13% of ClearFlow's"
    from collections import Counter
    codes = Counter(c for ps in lint.lint_site(web, "tidewell.example").values() for _, cs in ps for c in cs)
    assert codes == {"thin": 10, "pronoun-opener": 9, "buried-answer": 5}
