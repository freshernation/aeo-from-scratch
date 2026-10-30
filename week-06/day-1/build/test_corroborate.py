from aeolab import load_pages, web2

PAGES = {
    "https://a.example/x": '<p>We love Tidewell.</p><p>See <a href="https://t.example/">tidewell.example</a></p>',
    "https://b.example/y": '<nav>Tidewell</nav><p>TIDEWELL UX3 is certified for PFOA.</p><a href="/z">z</a>',
    "https://t.example/": '<p>Tidewell UX3 PFOA</p>',
}


def test_host(load):
    assert load("corroborate.py").host("https://a.example/x/y") == "a.example"


def test_mentions(load):
    assert load("corroborate.py").mentions(PAGES, "Tidewell", "t.example") == {"a.example": 1, "b.example": 1}


def test_inbound(load):
    assert load("corroborate.py").inbound(PAGES, "t.example") == ["a.example"]
    assert load("corroborate.py").inbound(PAGES, "b.example") == [], "a page linking to its own site is not inbound"


def test_corroborating(load):
    assert load("corroborate.py").corroborating(PAGES, ["UX3", "pfoa"], own="t.example") == ["b.example"]


def test_finding_five_independent_voices(load):
    c = load("corroborate.py")
    pages = load_pages(web2())
    assert c.mentions(pages, "Tidewell", "tidewell.example") == {
        "dailyhome.example": 1, "filterreviews.example": 4, "waterdirectory.example": 1,
        "waterforum.example": 4, "wikiwater.example": 2}
    assert len(c.inbound(pages, "tidewell.example")) == 5 and len(c.inbound(pages, "clearflow.example")) == 4
    assert c.corroborating(pages, ["UX3", "PFOA"], "tidewell.example") == [
        "dailyhome.example", "filterreviews.example", "waterforum.example", "wikiwater.example"], \
        "four other sites repeat the UX3's PFOA certification - and one of them also quotes the wrong price"
