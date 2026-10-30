from aeolab import load_pages, web2

PAGES = {
    "https://t.example/ux3": "<h1>UX3 filter</h1><p>It costs $189.</p><p>Nothing here.</p>",
    "https://r.example/rev": "<h1>Review</h1><p>The UX3 costs $149.</p><p>Other filters cost $99.</p>",
}


def mod(load):
    load("corroborate.py")
    load("facts.py")
    return load("contradict.py")


def test_normalise(load):
    c = mod(load)
    assert c.normalise("150 Litres") == "150 litre" and c.normalise("2.4-litre") == "2.4 litre"
    assert c.normalise("3 liters") == "3 litre"


def test_claims_use_the_h1(load):
    assert sorted(mod(load).fact_claims(PAGES, "ux3", "price")) == [
        ("https://r.example/rev", "$149"), ("https://t.example/ux3", "$189")]


def test_near(load):
    pages = {"u": "<h1>The Pitcher</h1><p>Holds 2.4 litres.</p><p>A cartridge lasts 150 litres.</p>"}
    assert mod(load).fact_claims(pages, "pitcher", "volume", near="cartridge") == [("u", "150 litre")]


def test_contradictions(load):
    c = mod(load)
    assert c.contradictions([("a", "$1"), ("b", "$2"), ("c", "$1")]) == {"$1": ["a", "c"], "$2": ["b"]}
    assert c.contradictions([("a", "$1"), ("b", "$1")]) == {}


def test_finding_candidates_are_not_conflicts(load):
    c = mod(load)
    pages = load_pages(web2())
    ux3 = c.contradictions(c.fact_claims(pages, "UX3", "price"))
    assert list(ux3) == ["$149", "$150", "$189", "$59"], \
        "four values; one real conflict ($149 vs $189). $59 is a cartridge set, $150 is 'under $150'"
    life = c.contradictions(c.fact_claims(pages, "Tidewell Pitcher", "volume", near="cartridge"))
    assert list(life) == ["100 litre", "150 litre", "2.4 litre"], \
        "one real conflict (a 2023 forum post says 100); 2.4 litres is the jug, not the cartridge"
