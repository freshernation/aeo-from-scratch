from aeolab import load_pages, web2

A = '<html><body><nav>Tidewell</nav><p>Tidewell Water Co. was founded in 2016 in Portland, Oregon.</p>' \
    '<p>See tidewell.example</p></body></html>'
B = '<html><head><script type="application/ld+json">{"@type": "Organization", "name": "TideWell Inc.", ' \
    '"foundingDate": "2015-03-01", "address": {"addressLocality": "Seattle"}}</script></head>' \
    '<body><li>TideWell Inc. is based in Seattle, Washington.</li></body></html>'


def mod(load):
    load("jsonld.py")
    return load("entities.py")


def test_paragraphs(load):
    assert mod(load).paragraphs(A) == ["Tidewell Water Co. was founded in 2016 in Portland, Oregon.", "See tidewell.example"]


def test_name_forms(load):
    assert mod(load).name_forms({"a": A, "b": B}, "Tidewell") == {"Tidewell Water Co.": 1, "TideWell Inc.": 1}


def test_claims(load):
    c = mod(load).claims({"a": A, "b": B}, "Tidewell")
    assert sorted(c) == [("a", "city", "Portland"), ("a", "founded", "2016"),
                         ("b", "city", "Seattle"), ("b", "city", "Seattle"), ("b", "founded", "2015")]


def test_conflicts(load):
    e = mod(load)
    assert e.conflicts([("a", "founded", "2016"), ("b", "founded", "2015"), ("a", "city", "X")]) == \
        {"founded": {"2016": ["a"], "2015": ["b"]}}


def test_finding_one_page_disagrees_on_everything(load):
    e = mod(load)
    pages = load_pages(web2())
    assert e.name_forms(pages, "Tidewell") == {"Tidewell": 16, "Tidewell Water Co.": 2, "TideWell Inc.": 1}
    D, T, W = "https://waterdirectory.example/tidewell", "https://tidewell.example/about", "https://wikiwater.example/wiki/Tidewell"
    assert e.conflicts(e.claims(pages, "Tidewell")) == {
        "founded": {"2016": [T, W], "2015": [D]}, "city": {"Portland": [T, W], "Seattle": [D]}}, \
        "one directory page gives a different name, year and city"
