from strategy_checks import check_sections, part


def test_written(source):
    text = source("MENTIONS.md")
    check_sections(text, (("Who mentions Tidewell", 50), ("Who links to Tidewell", 40),
                          ("What they repeat", 50), ("What they get wrong", 60)))
    who = part(text, "Who mentions Tidewell")
    for site in ("filterreviews.example", "waterforum.example", "wikiwater.example", "waterdirectory.example", "dailyhome.example"):
        assert site in who, f"{site} names Tidewell too"
    wrong = part(text, "What they get wrong")
    for needle in ("$149", "100 litres", "Seattle"):
        assert needle in wrong, f"'What they get wrong' should mention {needle}"
