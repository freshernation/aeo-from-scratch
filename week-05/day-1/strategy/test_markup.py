"""Day 1: structured data on three Tidewell pages, in week-05/snapshot/tidewell.example/."""
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

SNAP = Path(__file__).parents[2] / "snapshot" / "tidewell.example"
WIKI = "https://wikiwater.example/wiki/Tidewell"


def nodes(rel):
    soup = BeautifulSoup((SNAP / rel).read_text(), "html.parser")
    out = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string)
        except json.JSONDecodeError as e:
            raise AssertionError(f"{rel}: the JSON-LD is not valid JSON ({e})")
        out += data if isinstance(data, list) else data.get("@graph", [data])
    return out, " ".join(soup.body.get_text(" ").split())


def one(rel, kind):
    found, text = nodes(rel)
    match = [n for n in found if kind in ([n.get("@type")] if isinstance(n.get("@type"), str) else n.get("@type", []))]
    assert match, f"{rel} has no {kind} markup"
    return match[0], text


def offer_ok(product, text, name):
    assert name in product.get("name", ""), f"the Product's name should be '{name}'"
    offer = product.get("offers")
    offer = offer[0] if isinstance(offer, list) else offer
    assert offer and offer.get("priceCurrency") == "USD", "an offers object with priceCurrency USD"
    price = str(offer.get("price", "")).replace(".00", "")
    assert f"${price}" in text, f"the markup says {offer.get('price')}; the page shows {re.findall(r'[$][0-9]+', text)}"


def test_pitcher_tells_the_truth():
    p, text = one("filters/pitcher.html", "Product")
    offer_ok(p, text, "Tidewell Pitcher")


def test_shower_has_product_markup():
    p, text = one("filters/shower.html", "Product")
    offer_ok(p, text, "Tidewell")


def test_organization_is_one_entity():
    o, text = one("about.html", "Organization")
    assert o.get("name") == "Tidewell Water Co.", "use the name the About page uses"
    assert o.get("url") == "https://tidewell.example/" and str(o.get("foundingDate", "")).startswith("2016")
    same = o.get("sameAs", [])
    assert WIKI in (same if isinstance(same, list) else [same]), "sameAs should point at the encyclopedia entry"
